"""What does a general-purpose learnt representation find in the case pack?

Chapter 5 uses this to show that a learnt representation ranks records by
the kind of similarity it was trained on, which is not eligibility. The
encoder is all-MiniLM-L6-v2 (see encoder.py), a general-purpose sentence
encoder; each record is embedded from its title and abstract, truncated to
256 word pieces as the model requires.

Moran pool (case-pack/cache/moran-2021/pool.csv):

1. Dense ranking. Records are ranked by cosine similarity to two queries:
   the review's title, as in Chapter 4's BM25 ranking, and a question
   written for the case pack in the way a searcher might type it into an AI
   research tool (QUESTION, below). Recall of included records within the
   top k is compared with Chapter 4's BM25 rankings and with random order.
2. Nearest neighbours. For each included record, the labels of its nearest
   records by cosine similarity: how often is a near neighbour of an
   eligible record itself eligible?
3. A head trained on eligibility. The same embeddings are given a logistic
   regression trained on the title-and-abstract decisions for a random half
   of the pool (seed 7), and the other half is ranked by it. This changes
   only the training signal of the final layer.
4. Truncation. How many records are longer than the 256 word pieces the
   encoder reads.

Synthetic collection (case-pack/synthetic/records.json): all 33 records are
ranked by dense similarity and by BM25 against the fictional review's
question, to show where eligible studies, topically related but ineligible
records and off-topic records that share its words fall.

Writes case-pack/data/moran-2021/representations/ranks.csv (identifiers,
labels and ranks), summary.md, and synthetic-ranks.csv. Embeddings are
cached in case-pack/cache/ and not committed.

Requires: onnxruntime, tokenizers, numpy, scikit-learn.

Usage:
  python case-pack/scripts/representation_checks.py
"""

import csv
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import CACHE, CASE_PACK, DATA  # noqa: E402
from encoder import MODEL_NAME, MAX_TOKENS, Encoder  # noqa: E402
from ranking_checks import bm25_scores, ranks, recall_at, words  # noqa: E402

TITLE = "Poor nutritional condition promotes high-risk behaviours"
QUESTION = ("Does poor nutritional condition, such as food restriction or starvation, "
            "make animals bolder, more exploratory or more willing to take risks?")
SYNTHETIC_QUESTION = "Does structured peer tutoring improve reading comprehension in primary-school pupils?"
CUTOFFS = (100, 250, 500, 1000, 2000)
HALF_CUTOFFS = (50, 125, 250, 500, 1000)
NEIGHBOURS = 10
SEED = 7


def synthetic_category(record):
    number = int(record["id"][1:])
    if record["study_eligible"]:
        return "eligible study"
    if 14 <= number <= 23:
        return "on topic, ineligible"
    if 24 <= number <= 33:
        return "off topic, shares words"
    return "other"


def neighbour_labels(vectors, ta, ft, k):
    """For each included record, the labels of its k nearest other records."""
    sims = vectors @ vectors.T
    np.fill_diagonal(sims, -np.inf)
    counts = {"included": 0, "title and abstract only": 0, "excluded": 0}
    first = dict(counts)
    for i in np.flatnonzero(ft):
        order = np.argsort(-sims[i])[:k]
        for position, j in enumerate(order):
            label = "included" if ft[j] else ("title and abstract only" if ta[j] else "excluded")
            counts[label] += 1
            if position == 0:
                first[label] += 1
    return first, counts


def main():
    csv.field_size_limit(sys.maxsize)
    encoder = Encoder()

    pool = list(csv.DictReader((CACHE / "moran-2021" / "pool.csv").open(encoding="utf-8")))
    bm25 = {r["id"]: r for r in csv.DictReader(
        (DATA / "moran-2021" / "ranking" / "ranks.csv").open(encoding="utf-8"))}
    texts = [f"{r['title']} {r['abstract']}".strip() for r in pool]
    ta = np.array([int(r["label_ta"]) for r in pool])
    ft = np.array([int(r["label_ft"]) for r in pool])
    n = len(pool)

    cache_file = CACHE / "moran-2021" / "minilm-embeddings.npy"
    if cache_file.exists() and np.load(cache_file).shape[0] == n:
        vectors = np.load(cache_file)
    else:
        vectors = encoder.embed(texts)
        np.save(cache_file, vectors)
    lengths = np.array([encoder.token_count(t) for t in texts])

    queries = encoder.embed([TITLE, QUESTION])
    rank_title = ranks(list(vectors @ queries[0]))
    rank_question = ranks(list(vectors @ queries[1]))
    rank_bm25_title = [int(bm25[r["id"]]["rank_title_query"]) for r in pool]
    rank_bm25_strategy = [int(bm25[r["id"]]["rank_strategy_query"]) for r in pool]

    out = DATA / "moran-2021" / "representations"
    out.mkdir(parents=True, exist_ok=True)
    with (out / "ranks.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["id", "label_ta", "label_ft", "rank_dense_title", "rank_dense_question"])
        for r, a, f, t, q in zip(pool, ta, ft, rank_title, rank_question):
            writer.writerow([r["id"], a, f, t, q])

    def table(labels, columns, cutoffs, size):
        rows = ["| Records screened (top k) | Random order, expected | "
                + " | ".join(name for name, _ in columns) + " |",
                "|---" * (len(columns) + 2) + "|"]
        for k in cutoffs:
            rows.append(f"| {k:,} | {k / size:.2f} | "
                        + " | ".join(f"{recall_at(r, labels, k):.2f}" for _, r in columns) + " |")
        rows.append("| Rank of the last one | about " + f"{size:,} | "
                    + " | ".join(f"{max(x for x, l in zip(r, labels) if l):,}" for _, r in columns) + " |")
        return rows

    columns = [("BM25, title", rank_bm25_title), ("BM25, strategy words", rank_bm25_strategy),
               ("Dense, title", rank_title), ("Dense, question", rank_question)]

    first, tenth = neighbour_labels(vectors, ta, ft, NEIGHBOURS)
    n_ft = int(ft.sum())

    # A logistic-regression head trained on half the title-and-abstract decisions.
    from sklearn.linear_model import LogisticRegression

    rng = np.random.default_rng(SEED)
    order = rng.permutation(n)
    train, test = order[: n // 2], order[n // 2:]
    head = LogisticRegression(class_weight="balanced", max_iter=5000)
    head.fit(vectors[train], ta[train])
    test_scores = head.decision_function(vectors[test])
    half_columns = [
        ("BM25, strategy words", ranks([-rank_bm25_strategy[i] for i in test])),
        ("Dense, question", ranks([float(vectors[i] @ queries[1]) for i in test])),
        ("Dense with a head trained on eligibility", ranks(list(test_scores))),
    ]

    lines = [
        "# A general-purpose learnt representation on the Moran pool",
        "",
        "Generated by `case-pack/scripts/representation_checks.py`. Do not edit by hand.",
        "",
        f"Encoder: {MODEL_NAME} (ONNX export distributed by Chroma), mean-pooled and normalised; "
        f"each record embedded from its title and abstract, truncated to {MAX_TOKENS} word pieces.",
        "",
        f"Pool: {n:,} records; {int(ta.sum())} pass title-and-abstract screening; {n_ft} are included after full text.",
        "",
        f"Title query: `{TITLE}`",
        "",
        f"Question query (written for the case pack): `{QUESTION}`",
        "",
        "## Recall of full-text inclusions within the top k",
        "",
        *table(list(ft), columns, CUTOFFS, n),
        "",
        "## Recall of title-and-abstract inclusions within the top k",
        "",
        *table(list(ta), columns, CUTOFFS, n),
        "",
        f"## Nearest neighbours of the {n_ft} included records",
        "",
        "| Neighbour's label | Nearest neighbour | All of the 10 nearest | Share of the pool |",
        "|---|---|---|---|",
    ]
    base = {"included": n_ft / n, "title and abstract only": (int(ta.sum()) - n_ft) / n,
            "excluded": (n - int(ta.sum())) / n}
    for label in first:
        lines.append(f"| {label} | {first[label]} of {n_ft} ({first[label] / n_ft:.0%}) | "
                     f"{tenth[label]} of {n_ft * NEIGHBOURS:,} ({tenth[label] / (n_ft * NEIGHBOURS):.0%}) | "
                     f"{base[label]:.0%} |")
    held_ft = list(ft[test])
    lines += [
        "",
        f"## The same embeddings with a head trained on eligibility (held-out half, {len(test):,} records, "
        f"{sum(held_ft)} included)",
        "",
        f"A logistic regression (balanced class weights) trained on the title-and-abstract decisions for the "
        f"other {len(train):,} records (seed {SEED}). Recall of full-text inclusions in the held-out half:",
        "",
        *table(held_ft, half_columns, HALF_CUTOFFS, len(test)),
        "",
        "## Truncation",
        "",
        f"{int((lengths > MAX_TOKENS).sum()):,} of {n:,} records ({(lengths > MAX_TOKENS).mean():.0%}) are longer "
        f"than {MAX_TOKENS} word pieces, so the encoder never reads the end of their abstracts; "
        f"{int((lengths[ft == 1] > MAX_TOKENS).sum())} of the {n_ft} included records are.",
    ]

    # Synthetic collection.
    records = json.loads((CASE_PACK / "synthetic" / "records.json").read_text(encoding="utf-8"))["records"]
    syn_texts = [f"{r['title']} {r.get('abstract') or ''}".strip() for r in records]
    syn_vectors = encoder.embed(syn_texts)
    syn_query = encoder.embed([SYNTHETIC_QUESTION])[0]
    syn_cos = syn_vectors @ syn_query
    syn_dense = ranks(list(syn_cos))
    syn_bm25 = ranks(bm25_scores([words(t) for t in syn_texts], words(SYNTHETIC_QUESTION)))
    with (out / "synthetic-ranks.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["id", "study_id", "category", "rank_dense", "rank_bm25", "cosine"])
        for r, d, b, c in zip(records, syn_dense, syn_bm25, syn_cos):
            writer.writerow([r["id"], r["study_id"], synthetic_category(r), d, b, f"{c:.3f}"])

    lines += [
        "",
        "## Synthetic collection (33 records, all synthetic)",
        "",
        f"Question: `{SYNTHETIC_QUESTION}`. Median rank (1 = most similar) by category; see `synthetic-ranks.csv`.",
        "",
        "| Category | Records | Median rank, dense | Median rank, BM25 |",
        "|---|---|---|---|",
    ]
    for category in ("eligible study", "on topic, ineligible", "off topic, shares words", "other"):
        idx = [i for i, r in enumerate(records) if synthetic_category(r) == category]
        if idx:
            lines.append(f"| {category} | {len(idx)} | {np.median([syn_dense[i] for i in idx]):g} | "
                         f"{np.median([syn_bm25[i] for i in idx]):g} |")

    (out / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
