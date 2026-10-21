# Moran et al. (2021): labels and screening logs

The non-health contrast case. Built on 2026-10-21.

## Why not SYNERGY version 1's Moran labels

SYNERGY version 1 built its `Moran_2021` inclusion labels from a file in the authors' repository (`screening_ref_data_rayyan_final.csv`) that does not contain the review's inclusions: its records include, for example, an internet-based health intervention and physical activity in after-school programmes. Of the 107 records version 1 labels as included that have a DOI, 2 are full-text inclusions in the corrected labels and 7 passed title-and-abstract screening. SYNERGY's maintainers added a corrected variant in January 2025 (commit 74b6fde, pull request 128) and have said that version 1 will stay unchanged so that published results remain comparable, with fixes going into a future SYNERGY PLUS (issue 184).

These files therefore use the corrected variant, which reproduces the article's counts: 5,453 records screened at title and abstract, and 626 selected for full text (Moran et al., 2021).

## Files

| File | Contents |
|---|---|
| `labels.csv` | 4,882 records: identifier (DOI), title-and-abstract label, full-text label |
| `manifest.json` | Sources, pinned commits, SHA-256 checksums and join counts |
| `screening/*.csv` | One screening log per simulation: rank, identifier, whether it was a starting (prior) record, and both labels |
| `screening/summary.json` | Recall at fixed effort, effort to reach recall targets, WSS@95 and two illustrative stopping rules |

Titles and abstracts are not committed. `case-pack/scripts/build_moran_pool.py` rebuilds them into the ignored cache.

**Losses in the join.** Records are joined by DOI. Of 5,453 labelled records, 497 have no DOI, 5 repeat another record's DOI and 69 do not match the text file, leaving 4,882. The pool keeps 586 of 592 title-and-abstract inclusions and 137 of 139 full-text inclusions that have DOIs (the corrected file has 142 full-text inclusions in all).

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

### Results

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

What the exercise can draw out:

- The better-ranking model (higher WSS@95) triggers the same stopping rule earlier and leaves more eligible studies unseen. Ranking efficiency and a safe stop are different properties.
- Even in random order, a run of 50 irrelevant records occurs early, because about 12% of records are relevant here. A streak threshold means different things at different prevalences.
- The last few inclusions arrive late under both models (records 3,845 and 3,891 of 4,882), the pattern Appendix F of *How Search Decides What You See* describes.

**Limits.** One prior pair and one seed per model, so these figures show one possible run, not the variation across runs. The 50-record and 20% thresholds are illustrative, not recommendations. Title-and-abstract labels are the review team's decisions, which can contain errors.

## Reference

Moran, N. P., Sánchez-Tójar, A., Schielzeth, H., & Reinhold, K. (2021). Poor nutritional condition promotes high-risk behaviours: A systematic review and meta-analysis. *Biological Reviews, 96*(1), 269–288. https://doi.org/10.1111/brv.12655
