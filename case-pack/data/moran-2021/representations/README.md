# A general-purpose learnt representation on the Moran pool

Input for Chapter 5. Built on 2026-10-22 by `case-pack/scripts/representation_checks.py`.

## The question

A learnt representation ranks records by the kind of similarity it was trained on. How does a general-purpose sentence encoder rank the Moran pool against the review's question, how often are the nearest neighbours of an eligible record eligible, and what changes when the final layer is trained on the review's own decisions?

## Method

- **Encoder.** `sentence-transformers/all-MiniLM-L6-v2`, a six-layer general-purpose sentence encoder, in the ONNX export that Chroma distributes. `case-pack/scripts/encoder.py` downloads it into the ignored cache and checks its SHA-256. Each record is embedded from its title and abstract, truncated to 256 word pieces, mean-pooled and normalised, so a dot product is a cosine similarity.
- **Queries.** The review's title, as in Chapter 4's BM25 ranking, and a question written for the case pack in the way a searcher might type it into an AI research tool (given in `summary.md`).
- **Nearest neighbours.** For each of the 137 included records, the labels of its 10 nearest records by cosine similarity.
- **A head trained on eligibility.** A logistic regression with balanced class weights, trained on the embeddings and title-and-abstract decisions of a random half of the pool (seed 7), ranks the other half.
- **Synthetic collection.** The 33 synthetic records are ranked by dense similarity and by BM25 against the fictional review's question (`synthetic-ranks.csv`).

`ranks.csv` holds identifiers, labels and dense ranks only. The embeddings stay in the cache.

## Results

See `summary.md`. In brief:

- With the written question, the dense ranking performs about as well as BM25 with the strategy's words (recall of included records 0.55 against 0.59 in the top 1,000) and better than either BM25 or the dense ranking with the title alone.
- The nearest neighbour of an included record is itself included in 55 of 137 cases (40%), against 3% of the pool, and excluded at title and abstract in 49 (36%). Counted once each, the 10 nearest neighbours of the included records are 614 distinct records, 17% of them included; every included neighbour is one of the 137.
- The same embeddings with a head trained on half the review's decisions find 94% of the held-out half's included records in its top 1,000 of 2,441, against 79% for the dense question ranking.
- Under the title query, 78 of the top 100 records mention human-health words and 22 animal words, against 37% and 68% of the pool; under the question, 14 and 94. The title never says "animals" (a rough word-list check, defined in the script).
- 79% of the records, and 108 of the 137 included records, are longer than 256 word pieces, so the encoder never reads the end of their abstracts.
- In the synthetic collection, the three records ranked most similar to the question are all ineligible (a systematic review, a secondary-school trial and a single-group study), while the off-topic records that share the question's words fall to the bottom; BM25 ranks one of those, about ventilation in primary-school classrooms, fourth.

## Limits

- **One small, general-purpose encoder.** Models trained on scientific citations (SPECTER) or search logs (MedCPT) would rank differently; they could not be downloaded in the build environment. These figures describe this encoder, not any product.
- **A pre-filtered pool.** All 4,882 records were admitted by the authors' Boolean searches, so every ranking starts from records that already share the topic's vocabulary.
- **One wording of the question.** Another wording would give another ranking.
- **Possible contamination.** The encoder's training data include scientific titles and abstracts, which may include some of these records.
- **The head trained on eligibility** is a simplified version of what active-learning screening tools do (Chapter 9), trained once on half the labels rather than incrementally.

## Contamination risk

The Moran review and its records are public, and the encoder was trained on large public text collections; see `case-pack/data/moran-2021/README.md`.
