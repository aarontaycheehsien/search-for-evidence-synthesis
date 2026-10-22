# Stopping: statistical criterion and capture–recapture

Inputs for Chapter 9. Built on 2026-10-22.

## Files

| File | Contents | Built by |
|---|---|---|
| `statistical-stop.csv` | For each screening log: where a statistical stopping criterion first allows stopping, the share of the pool screened, title-and-abstract recall at that point and full-text inclusions still unseen | `case-pack/scripts/stopping_checks.py` |
| `summary.md` | The same results as tables: median and range for the 30 Moran ten-start runs, and each single run | `case-pack/scripts/stopping_checks.py` |
| `capture-recapture.csv` | Two-source capture–recapture estimates for the Moran searches (Web of Science and Scopus), at full text and at title and abstract | `case-pack/scripts/capture_recapture.py` |

The screening logs themselves are in `case-pack/data/moran-2021/screening/`, `case-pack/data/moran-2021/screening-seeds/` and `case-pack/data/clef-2019/CD010558/`. The streak and fixed-effort rules for the same logs are in their `summary.json` files.

## Statistical stopping criterion

The criterion is Callaghan and Müller-Hansen's (2020) "ranked quasi-sampling" test, computed with their package `buscarpy` (version 0.0.2, MIT licence; function `calculate_h0`). After each block of screening it asks: if recall were still below the target, how likely is it that the most recently screened records would contain as few eligible records as they do? It treats every recent stretch of the screening order as if it were a random sample of what remained, and takes the smallest of the resulting p-values. Screening may stop when that p-value falls below 0.05.

Settings: recall target 95% of title-and-abstract inclusions; confidence 95%; unbiased urns (`bias = 1`, the package default). The test is evaluated every 5 records, so each stop is reported at the first multiple of 5 at which p < 0.05; the true first record can be up to 4 earlier. Callaghan and Müller-Hansen evaluated the test after every record. Running all 36 logs takes about 13 minutes.

The screening decision is the title-and-abstract label, as in the simulations. The column that matters to the review is `ft_unseen_at_stop`: full-text inclusions not yet screened when the criterion allows stopping.

### Results

From `summary.md`, median (minimum to maximum) across ten starting pairs; the Moran pool has 4,882 records, 586 title-and-abstract inclusions and 137 full-text inclusions.

| Strategy | Records screened at the stop | Title-and-abstract recall at the stop | Full-text inclusions unseen |
|---|---|---|---|
| TF-IDF + SVM (`elas_u4`) | 2,927.5 (2,860 to 3,195) | 0.991 (0.990 to 0.997) | 0 (0 to 0) |
| TF-IDF + naive Bayes (`tfidf_nb`) | 3,445 (3,430 to 3,530) | 0.995 (0.995 to 0.997) | 0 (0 to 0) |
| Random order | 4,602.5 (4,375 to 4,700) | 0.94 (0.87 to 0.97) | 7.5 (3 to 19) |

For comparison, from `case-pack/data/moran-2021/screening-seeds/summary.json`, the number of runs (of ten) that stopped below 95% title-and-abstract recall:

| Strategy | 50 consecutive irrelevant | 100 consecutive irrelevant | Statistical criterion |
|---|---|---|---|
| TF-IDF + SVM | 4 | 0 | 0 |
| TF-IDF + naive Bayes | 7 | 0 | 0 |
| Random order | 9 | 0 (a 100-record streak never occurred, so screening ran to the end) | 6 |

CD010558 (2,815 records, 37 title-and-abstract and 10 full-text eligible records): the criterion allowed stopping at records 2,645 (Sheffield BM25), 2,715 (Padua BM25) and 2,625 (Padua active learning), 93% to 96% of the pool, with every eligible record found.

### What the results show, and what they do not

- **In prioritised order the criterion never stopped short of its target here, and cost more screening than a streak rule.** With the SVM model it stopped a median 835 records after the point at which 95% of title-and-abstract inclusions had in fact been found (2,092.5). That extra screening is the price of being able to state a confidence level.
- **With few eligible records, the criterion must screen most of what remains.** In CD010558, recall of 37 out of 39 would be below 95%, so the test must rule out that two eligible records remain. After the last eligible record in the Sheffield ranking (rank 2,055), 760 records remain. If two of them were eligible, the chance of seeing neither in the next 590 records is (170 × 169) / (760 × 759) = 0.0498, just under 0.05; hence the stop at record 2,645. `calculate_h0` returns the same value.
- **The guarantee depends on the order.** Callaghan and Müller-Hansen describe the ranked test as conservative on the assumption that records chosen by machine learning are not less likely to be relevant than records chosen at random. In random order that assumption holds only with equality, nothing offsets the repeated testing (the paper notes that it did not address multiple testing formally), and the criterion stopped below the target in 6 of 10 runs. No one would use the test this way, but it shows that a confidence statement holds only under the conditions it was derived for.
- **These are 36 runs on two reviews.** They illustrate the mechanism. They are not an evaluation of the criterion; for that, see Repke et al. (2026), which simulated 223 prioritised screening runs on 81 datasets.

## Capture–recapture on the Moran searches

`capture_recapture.py` treats the Web of Science and Scopus searches as two independent "captures" of the eligible records, using the database overlap in `case-pack/data/moran-2021/sources-and-deduplication.json` (matching by DOI or exact title). It reports the Lincoln–Petersen and Chapman estimators and a normal-approximation 95% interval for Chapman's estimate, floored at the number found. The test suite checks that the code reproduces Spoor et al.'s (1996) published estimate (160, 95% CI 158 to 164).

| Stage | Web of Science | Scopus | Both | Found | Chapman estimate (95% interval) | Estimated missed by both |
|---|---|---|---|---|---|---|
| Full text | 111 | 115 | 89 | 137 | 143.4 (137.1 to 149.6) | 6.4 |
| Title and abstract | 344 | 513 | 271 | 586 | 650.9 (626.5 to 675.4) | 64.9 |

**Limits.** The estimates assume that the two searches find records independently and that every eligible record is equally likely to be found. Neither holds: both databases were searched with the same strategy, so a study whose title and abstract use none of its terms is missed by both, and some studies are much easier to find than others. Both violations make the estimate too low. The estimate is also only of studies that searches like these could reach; it says nothing about studies in sources neither database indexes. The counts cover records in the case pack's pool, which loses some records without DOIs (see `case-pack/data/moran-2021/README.md`).

## References

Callaghan, M. W., & Müller-Hansen, F. (2020). Statistical stopping criteria for automated screening in systematic reviews. *Systematic Reviews, 9*, 273. https://doi.org/10.1186/s13643-020-01521-4

Repke, T., Tinsdeall, F., Danilenko, D., Graziosi, S., Müller-Hansen, F., Schmidt, L., Thomas, J., & van Valkenhoef, G. (2026). Don't stop me now, 'cause I'm having a good time screening: Evaluation of stopping methods for safe use of priority screening in systematic reviews. *Cochrane Evidence Synthesis and Methods, 4*(1), e70068. https://doi.org/10.1002/cesm.70068

Spoor, P., Airey, M., Bennett, C., Greensill, J., & Williams, R. (1996). Use of the capture–recapture technique to evaluate the completeness of systematic literature searches. *BMJ, 313*(7053), 342–343. https://doi.org/10.1136/bmj.313.7053.342
