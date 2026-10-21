# Moran et al. (2021): labels and screening logs

The non-health contrast case. Built on 2026-10-21.

## Why not SYNERGY version 1's Moran labels

SYNERGY version 1 built its `Moran_2021` inclusion labels from a file in the authors' repository (`screening_ref_data_rayyan_final.csv`) that does not contain the review's inclusions: its records include, for example, an internet-based health intervention and physical activity in after-school programmes. The authors' search script shows what the file is: the 120 new records from their update search of 4 February 2019 (see below). "Final" meant the final search, not the final inclusions. Of the 107 records version 1 labels as included that have a DOI, 2 are full-text inclusions in the corrected labels and 7 passed title-and-abstract screening. SYNERGY's maintainers added a corrected variant in January 2025 (commit 74b6fde, pull request 128) and have said that version 1 will stay unchanged so that published results remain comparable, with fixes going into a future SYNERGY PLUS (issue 184).

These files therefore use the corrected variant, which reproduces the article's counts: 5,453 records screened at title and abstract, and 626 selected for full text (Moran et al., 2021).

## Files

| File | Contents |
|---|---|
| `labels.csv` | 4,882 records: identifier (DOI), title-and-abstract label, full-text label |
| `manifest.json` | Sources, pinned commits, SHA-256 checksums and join counts |
| `screening/*.csv` | One screening log per simulation: rank, identifier, whether it was a starting (prior) record, and both labels |
| `screening/summary.json` | Recall at fixed effort, effort to reach recall targets, WSS@95 and illustrative stopping rules (streaks of 50, 100 and 200 irrelevant records; a fixed 20% of the pool) |
| `screening-seeds/` | Compact logs and summaries for 30 further simulations (three strategies, ten starting pairs each), with `aggregate.md` |
| `sources-and-deduplication.json` | Deduplication counts under six rules and each database's contribution of eligible studies |

Titles and abstracts are not committed. `case-pack/scripts/build_moran_pool.py` rebuilds them into the ignored cache.

**Losses in the join.** Records are joined by DOI. Of 5,453 labelled records, 497 have no DOI, 5 repeat another record's DOI and 69 do not match the text file, leaving 4,882. The pool keeps 586 of 592 title-and-abstract inclusions and 137 of 139 full-text inclusions that have DOIs (the corrected file has 142 full-text inclusions in all).

## Searches, updates and deduplication

From the authors' search script (`01_conditiontreatments_search.R`) and their exports, read at commit `b25a3c2`.

**Initial searches, 10 November 2018.** Web of Science Core Collection returned 2,729 records and Scopus 4,479; together 7,208. The script header says "10_11_2019", but the Scopus update below is limited to records loaded after 10 November 2018, so the header is a slip.

**Update searches, 4 February 2019.** The two databases were updated by different methods:

- Web of Science: the whole search was re-run (2,813 records) and compared with the initial results by exact title, leaving 92 new records.
- Scopus: the search was re-run with `ORIG-LOAD-DATE > 20181110`, returning 42 records.
- Combined and deduplicated by fuzzy title: 120 records, exported as `screening_ref_data_rayyan_final.csv`.

The Web of Science string echoed by the database in the update ("You searched for: …") reads `"asset protection" OR "residual reproductive value"` and `"risk-taking behavio*"`. The hand-typed comment for the initial search reads `"asset protection" residual reproductive value")`, with unbalanced quotation marks, and `"risk taking behavio*"`. The first is almost certainly a slip in the comment rather than the executed search; the second is a real difference between the initial and update strings. Appendix S2 of the article's supporting information should confirm which strings were reported.

**Deduplication.** `sources-and-deduplication.json`, built by `case-pack/scripts/moran_sources.py`, applies different rules to the 7,208 initial records:

| Rule | Records left |
|---|---|
| DOI only | 5,552 |
| DOI only, after removing BibTeX escapes (Web of Science writes `[` as `{[}` in DOIs) | 5,544 |
| Exact title (letters and digits only) | 5,454 |
| DOI or exact title | 5,402 |
| DOI or title similarity of at least 0.95 | 5,393 |
| DOI or title similarity of at least 0.90 | 5,390 |
| The authors' tool (revtools, fuzzy title), as reported in their script | 5,509 |
| Screened at title and abstract, as reported in the article | 5,453 |

The same export yields anywhere from 5,390 to 5,552 "records after duplicates removed", depending on the rule. Some exact-title matches join records with different DOIs; most are the same article under two DOI forms, but not all.

**Database contribution.** Matching by DOI or exact title, the 137 full-text inclusions in the pool came from both databases (89), Web of Science alone (22) or Scopus alone (26). For the 586 title-and-abstract inclusions the figures are 271, 73 and 242. Either database alone would have missed between 16% and 19% of the eligible studies found; these are properties of this review and this pair of searches, not of the databases in general.

## Simulations

Three runs on the same 4,882 records, using the title-and-abstract labels as the screening decision:

| Run | Feature extractor | Classifier | Query strategy | Balancer |
|---|---|---|---|---|
| `random` | (not used) | (not used) | random | none |
| `tfidf_nb` | TF-IDF | naive Bayes | maximum | balanced |
| `elas_u4` | TF-IDF | support vector machine | maximum | balanced (ASReview's default model) |

All runs start from the same two records (one included, one excluded), chosen with `--prior-seed 535`; model seed `--seed 42`. Software: ASReview 3.0.8, scikit-learn 1.9.1, NumPy 2.5.4, Python 3.13. Each run stops once every title-and-abstract inclusion is found; every record after that point is irrelevant at both stages.

Command for the default model (the others change `--ai` to explicit `-e`, `-c`, `-q`, `-b` options):

```
asreview simulate asreview_ta.csv --ai elas_u4 --n-prior-included 1 --n-prior-excluded 1 \
  --prior-seed 535 --seed 42 -o elas_u4.asreview
```

### Results of the single run

| | Random | TF-IDF + naive Bayes | TF-IDF + SVM |
|---|---|---|---|
| Records screened to find 95% of title-and-abstract inclusions | 4,655 | 2,379 | 2,057 |
| Records screened to find every title-and-abstract inclusion | 4,869 | 3,891 | 3,845 |
| Records screened to find every full-text inclusion | 4,867 | 2,832 | 2,297 |
| WSS@95 (title and abstract) | about 0 | 0.46 | 0.53 |
| Full-text recall after screening 20% (976 records) | 0.14 | 0.77 | 0.80 |
| Stop after 50 consecutive irrelevant records: records screened | 957 | 2,168 | 1,367 |
| Stop after 50 consecutive irrelevant records: full-text recall | 0.14 | 0.97 | 0.88 |
| Stop after 50 consecutive irrelevant records: full-text inclusions unseen | 118 | 4 | 16 |

In this run the better-ranking model stopped earlier and missed more. The ten-start results below show that this was not typical, so do not teach it as a general pattern.

## Ten starting pairs

`screening-seeds/` holds 30 further simulations: each strategy run from ten different starting pairs (`--prior-seed` and `--seed` both set to 1 to 10), with the same settings and software as above. Each seed gives every strategy the same starting records. Logs are compact: they list the starting records and the title-and-abstract inclusions with their ranks; every rank not listed is irrelevant at both stages. `summary.json` has each run's measures and `aggregate.json` and `aggregate.md` the median and range across runs.

Median (minimum to maximum) across the ten runs of each strategy; `elas_u4` is TF-IDF with SVM:

| Measure | elas_u4 (10 runs) | random (10 runs) | tfidf_nb (10 runs) |
|---|---|---|---|
| WSS@95 (title and abstract) | 0.52 (0.52 to 0.52) | 0.00 (-0.02 to 0.01) | 0.46 (0.45 to 0.47) |
| Records screened to find 95% of title-and-abstract inclusions | 2,092.5 (2,081 to 2,102) | 4,632.5 (4,588 to 4,716) | 2,386 (2,352 to 2,419) |
| Records screened to find every full-text inclusion | 2,493.5 (2,303 to 2,530) | 4,852 (4,825 to 4,880) | 2,805 (2,788 to 2,822) |
| Full-text recall after screening 20% | 0.82 (0.80 to 0.82) | 0.18 (0.16 to 0.30) | 0.77 (0.73 to 0.82) |
| Stop after 50 consecutive irrelevant: records screened | 2,259 (1,892 to 2,431) | 2,501.5 (483 to 4,882) | 1,992 (1,599 to 2,470) |
| Stop after 100 consecutive irrelevant: records screened | 2,642 (2,402 to 2,669) | 4,882 (4,882 to 4,882) | 2,737.5 (2,668 to 3,396) |
| Stop after 200 consecutive irrelevant: records screened | 3,429 (2,882 to 3,431) | 4,882 (4,882 to 4,882) | 3,727 (3,722 to 3,735) |
| Stop after 50 consecutive irrelevant: full-text inclusions unseen | 1.5 (0 to 6) | 74.5 (0 to 123) | 6.5 (1 to 12) |
| Stop after 100 consecutive irrelevant: full-text inclusions unseen | 0 (0 to 1) | 0 (0 to 0) | 1 (0 to 1) |
| Stop after 200 consecutive irrelevant: full-text inclusions unseen | 0 (0 to 0) | 0 (0 to 0) | 0 (0 to 0) |

What the exercise can draw out:

- **Ranking efficiency is stable; stopping is not.** WSS@95 hardly moves with the starting records (0.52 in every SVM run), yet the 50-record rule leaves 0 to 6 eligible studies unseen with SVM and 1 to 12 with naive Bayes. The single run above, from a different starting pair, left 16 unseen, outside even this range.
- **One run can mislead.** Across ten starts the better-ranking model usually missed fewer studies at the 50-record stop (median 1.5 against 6.5), the opposite of what the single run suggested.
- **Random order makes a streak rule meaningless.** The 50-record rule stopped anywhere from record 483 to never, leaving between 0 and 123 eligible studies unseen.
- **Longer streaks trade effort for safety.** A 100-record streak left at most one eligible study unseen with either model, after screening about 54% to 56% of the pool (median); a 200-record streak missed none, after about 70% to 76%. These thresholds suit this review's 12% prevalence and do not transfer: in the CD010558 health case, where about 1% of records are relevant, a 100-record streak on one BM25 ranking still left 4 of 10 eligible records unseen.

**Limits.** Ten starting pairs per strategy show variation but do not bound it. The streak thresholds are illustrative, not recommendations. Title-and-abstract labels are the review team's decisions, which can contain errors.

## Reference

Moran, N. P., Sánchez-Tójar, A., Schielzeth, H., & Reinhold, K. (2021). Poor nutritional condition promotes high-risk behaviours: A systematic review and meta-analysis. *Biological Reviews, 96*(1), 269–288. https://doi.org/10.1111/brv.12655
