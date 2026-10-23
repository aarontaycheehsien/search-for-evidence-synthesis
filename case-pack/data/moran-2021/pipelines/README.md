# Reranking, fusion and union on the Moran pool

Input for Chapter 6. Built on 2026-10-22 by `case-pack/scripts/pipeline_checks.py` from the BM25 ranking (`../ranking/`) and the dense ranking (`../representations/`).

## The question

Products combine retrieval stages in different ways. Which stages can bring an eligible record into view, and which can only change its position?

## Method

Two complete rankings of the 4,882 records are combined three ways:

- **Reranking:** the top 1,000 records by BM25 with the strategy's words are reordered by dense similarity to the written question; the rest keep their order below.
- **Reciprocal rank fusion:** each record scores 1 / (60 + its rank) in each ranking, summed (Cormack et al., 2009).
- **Union:** the top 250, 500 or 1,000 records of each ranking are pooled.

## Results

See `summary.md`. Reranking roughly doubles the included records in the top 100 (from 0.09 to 0.16 of them) but leaves recall at 1,000 unchanged at 0.59. Fusion raises recall at 1,000 to 0.64. Each route's top 500 contains included records the other's lacks (29 and 23), yet the 876-record union holds 58% of the included records, little more than the 55% that BM25 alone reaches with the same 876 records.

## Limits

The two routes rank a pool the authors' Boolean searches had already built, so neither can reach records outside it, and the figures describe these two rankings only. A product's own stages, candidate sizes and fusion rules are usually undocumented (Chapter 6).
