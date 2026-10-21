# BM25 ranking of the Moran pool

Built on 2026-10-22 by `case-pack/scripts/ranking_checks.py` from the cached Moran pool (`case-pack/cache/moran-2021/pool.csv`, rebuilt by `build_moran_pool.py`). For Chapter 4.

The pool is the 4,882 records of the authors' Web of Science and Scopus searches that join to the corrected SYNERGY labels (see `../README.md`): 586 pass title-and-abstract screening and 137 are included after full text. The script ranks the pool by BM25 over title and abstract with two queries, and records where each record falls.

| File | Contents |
|---|---|
| `ranks.csv` | One row per record: identifier (DOI), both labels, and its rank under each query |
| `term-weights.csv` | For each query term: how many vocabulary words it matches, its document frequency in the pool, its IDF, and how many included records contain it |
| `summary.md` | Recall of included records within the top k, for each query and for random order |

## Queries

- **Title query:** the words of the review's title, as a searcher might type them into a relevance-ranked system.
- **Strategy query:** the words of the authors' search strategy, without its Boolean structure, phrases or proximity. Truncated terms are expanded through the pool's vocabulary and treated as one term.

## What the files show

- **A cap turns ranking quality into recall.** If only the top 1,000 records could be seen, the strategy query would keep 59% of the included records, the title query 35%, and random order about 20%.
- **No ranking finds everything early.** The last included record sits at rank 4,494 under the strategy query and 4,797 under the title query.
- **Rarity is not relevance.** *behavio\** occurs in 124 of the 137 included records but in 3,497 of the 4,882 pool records, so its IDF is the lowest of any query term (0.33). The highest-weighted terms (*neophil\**, *promotes*, *calori\**) occur in no included record. Within a pool built by the strategy, the words every record had to contain carry little weight.

## Limits

This ranks records within the pool the authors' Boolean searches had already admitted. A relevance-ranked system with a display cap, such as a web-scale search engine, ranks its whole index, so its top 1,000 would be drawn from a far larger and noisier set. These figures are therefore not an estimate of any product's recall. BM25 here uses one common variant (k1 = 1.2, b = 0.75, IDF = ln(1 + (N − df + 0.5)/(df + 0.5))) with a plain analyser and no stemming; other settings would give other numbers.

Titles and abstracts are not committed; they remain in the ignored cache.
