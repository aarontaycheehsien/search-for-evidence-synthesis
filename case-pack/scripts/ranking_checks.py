"""Rank the Moran pool with BM25 and measure what a result cap would keep.

The Moran pool (4,882 records the review's Web of Science and Scopus
searches returned, with title-and-abstract and full-text labels) is ranked
by BM25 over title and abstract with two queries:

- title_query: the words of the review's title, as a searcher might type
  them;
- strategy_query: the words of the authors' search strategy, without its
  Boolean structure, phrases or proximity, the way some shared-task teams
  built BM25 queries from a review's Boolean strategy.

A truncated term (ending in *) is expanded through the pool's vocabulary
and treated as one term: its frequency is the sum over the matching words
and its document frequency counts records containing any of them. A term
starting with * matches any word containing the rest.

BM25 uses k1 = 1.2, b = 0.75 and IDF = ln(1 + (N - df + 0.5) / (df + 0.5)).
Ties are broken by record order in the pool file, which is sorted by DOI.

Writes case-pack/data/moran-2021/ranking/ranks.csv (identifier, labels and
the two ranks), term-weights.csv (each query term's document frequency,
IDF and the number of included records containing it) and summary.md.
Titles and abstracts stay in the cache.

Usage:
  python case-pack/scripts/ranking_checks.py
"""

import csv
import math
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import CACHE, DATA  # noqa: E402

WORD = re.compile(r"[a-z0-9]+")

TITLE_QUERY = ["poor", "nutritional", "condition", "promotes", "high", "risk", "behaviours"]
STRATEGY_QUERY = [
    "*nutrition*", "*nourish*", "calori*", "hunger", "starv*", "diet*", "food", "restrict*", "depriv*",
    "condition*", "bold*", "explorat*", "risk*", "novel*", "predat*", "refuge", "neophobi*", "neophil*",
    "personalit*", "temperament*", "coping", "behavio*", "plasticity", "flexibil*", "trait*", "syndrome*",
]
CUTOFFS = (100, 250, 500, 1000, 2000)
K1, B = 1.2, 0.75


def words(text):
    return WORD.findall((text or "").lower())


def expand(term, vocabulary):
    """Return the set of vocabulary words a query term matches."""
    if term.startswith("*") and term.endswith("*"):
        core = term.strip("*")
        return {w for w in vocabulary if core in w}
    if term.endswith("*"):
        stem = term[:-1]
        return {w for w in vocabulary if w.startswith(stem)}
    return {term} & vocabulary


def bm25_scores(docs, query):
    """docs: list of token lists. Returns one score per document."""
    n = len(docs)
    lengths = [len(d) for d in docs]
    average = sum(lengths) / n
    counts = [Counter(d) for d in docs]
    vocabulary = set().union(*counts)
    scores = [0.0] * n
    for term in query:
        forms = expand(term, vocabulary)
        if not forms:
            continue
        tfs = [sum(c[f] for f in forms) for c in counts]
        df = sum(1 for tf in tfs if tf)
        idf = math.log(1 + (n - df + 0.5) / (df + 0.5))
        for i, tf in enumerate(tfs):
            if tf:
                scores[i] += idf * tf * (K1 + 1) / (tf + K1 * (1 - B + B * lengths[i] / average))
    return scores


def term_weights(docs, query, labels):
    """Document frequency, IDF and included-record count for each query term."""
    n = len(docs)
    sets = [set(d) for d in docs]
    vocabulary = set().union(*sets)
    rows = []
    for term in query:
        forms = expand(term, vocabulary)
        df = sum(1 for d in sets if d & forms)
        rows.append({
            "term": term,
            "matching_words": len(forms),
            "document_frequency": df,
            "idf": round(math.log(1 + (n - df + 0.5) / (df + 0.5)), 2),
            "included_records_containing": sum(1 for d, label in zip(sets, labels) if label and d & forms),
        })
    return rows


def ranks(scores):
    order = sorted(range(len(scores)), key=lambda i: (-scores[i], i))
    result = [0] * len(scores)
    for position, i in enumerate(order, start=1):
        result[i] = position
    return result


def recall_at(ranked, labels, k):
    relevant = sum(labels)
    return sum(1 for r, label in zip(ranked, labels) if label and r <= k) / relevant


def expected_last_rank(n, k):
    """Expected rank of the last of k eligible records when n records are in random order."""
    return k * (n + 1) / (k + 1)


def main():
    csv.field_size_limit(sys.maxsize)
    rows = list(csv.DictReader((CACHE / "moran-2021" / "pool.csv").open(encoding="utf-8")))
    docs = [words(r["title"]) + words(r["abstract"]) for r in rows]
    ta = [int(r["label_ta"]) for r in rows]
    ft = [int(r["label_ft"]) for r in rows]
    rank_title = ranks(bm25_scores(docs, TITLE_QUERY))
    rank_strategy = ranks(bm25_scores(docs, STRATEGY_QUERY))

    out_dir = DATA / "moran-2021" / "ranking"
    out_dir.mkdir(parents=True, exist_ok=True)
    with (out_dir / "ranks.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["id", "label_ta", "label_ft", "rank_title_query", "rank_strategy_query"])
        for r, a, f, t, s in zip(rows, ta, ft, rank_title, rank_strategy):
            writer.writerow([r["id"], a, f, t, s])

    weights = term_weights(docs, STRATEGY_QUERY + [t for t in TITLE_QUERY if t not in STRATEGY_QUERY], ft)
    with (out_dir / "term-weights.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(weights[0]))
        writer.writeheader()
        writer.writerows(weights)

    n = len(rows)
    lines = [
        "| Records screened (top k) | Random order, expected | Title query | Strategy query |",
        "|---|---|---|---|",
    ]
    for k in CUTOFFS:
        lines.append(
            f"| {k:,} | {k / n:.2f} | {recall_at(rank_title, ft, k):.2f} | {recall_at(rank_strategy, ft, k):.2f} |"
        )
    last_title = max(r for r, f in zip(rank_title, ft) if f)
    last_strategy = max(r for r, f in zip(rank_strategy, ft) if f)
    lines.append(f"| Rank of the last included record | about {round(expected_last_rank(n, sum(ft))):,} | {last_title:,} | {last_strategy:,} |")
    ta_lines = [
        "| Records screened (top k) | Random order, expected | Title query | Strategy query |",
        "|---|---|---|---|",
    ]
    for k in CUTOFFS:
        ta_lines.append(
            f"| {k:,} | {k / n:.2f} | {recall_at(rank_title, ta, k):.2f} | {recall_at(rank_strategy, ta, k):.2f} |"
        )
    text = "\n".join(
        [
            "# BM25 ranking of the Moran pool",
            "",
            "Generated by `case-pack/scripts/ranking_checks.py`. Do not edit by hand.",
            "",
            f"Pool: {n:,} records; {sum(ta)} pass title-and-abstract screening; {sum(ft)} are included after full text.",
            "",
            f"Title query: `{' '.join(TITLE_QUERY)}`",
            "",
            f"Strategy query: `{' '.join(STRATEGY_QUERY)}`",
            "",
            "## Recall of full-text inclusions within the top k",
            "",
            *lines,
            "",
            "## Recall of title-and-abstract inclusions within the top k",
            "",
            *ta_lines,
            "",
        ]
    )
    (out_dir / "summary.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
