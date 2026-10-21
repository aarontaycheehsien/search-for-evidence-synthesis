# CD010558: screening logs from CLEF 2019 participant runs

The health running case. Built on 2026-10-21 by `case-pack/scripts/clef_runs.py` from the CLEF TAR repository (`CLEF-TAR/tar` at commit `dbc13d0`, MIT licence): the 2019 test topic file, the abstract and content qrels, and `2019-TAR/participant-runs/Runs.zip`.

Each log ranks all 2,815 PubMed records that the review's MEDLINE strategy returned when CLEF re-ran it. Labels: 37 eligible at title and abstract, 10 at full text. Those 10 records are reports of 4 of the review's 6 included studies; see `case-pack/reference-sets/README.md` for what the pool leaves out.

## Runs

| Log | Team and run file | Method, as described by the team |
|---|---|---|
| `sheffield_bm25_baseline` | University of Sheffield, `Intervention_sheffield-baseline` | BM25, with a query built from the review title and terms extracted from the Boolean query |
| `padua_bm25_baseline` | University of Padua, `baseline_bm25_t1500` | A simple BM25 baseline |
| `padua_cal_p10_t1500` | University of Padua, `distributed_effort_p10_t1500` | Continuous active learning: interactive BM25 trained on relevance feedback, with effort distributed according to pool size |

Method descriptions are paraphrased from the teams' run descriptions in the archive. Credit the teams and the CLEF 2019 overview (Kanoulas et al., 2019) when using these logs.

## Results

| | Sheffield BM25 | Padua BM25 | Padua active learning |
|---|---|---|---|
| Records screened to find every full-text-eligible record | 1,220 | 1,686 | 178 |
| Records screened to find 95% of title-and-abstract-eligible records | 1,589 | 2,320 | 1,792 |
| WSS@95 (title and abstract) | 0.39 | 0.13 | 0.31 |
| Stop after 50 consecutive irrelevant: records screened | 146 | 62 | 298 |
| Stop after 50 consecutive irrelevant: full-text recall | 0.2 | 0.1 | 1.0 |
| Full-text recall after screening 20% (563 records) | 0.6 | 0.8 | 1.0 |

What the exercise can draw out:

- Two runs both called "BM25 baseline" perform very differently. The label names a scoring family, not a query; what the query contains matters as much as the formula.
- Active learning finds every full-text-eligible record early here, yet takes longer than the Sheffield ranking to reach 95% of title-and-abstract-eligible records. Which recall target you report changes which method looks better.
- On the static rankings, a 50-record streak occurs within the first 150 records. The same rule stops the active-learning run only after it has found every full-text-eligible record.
- Recall here is measured against the pool's 10 eligible records. Against the review's included studies, the pool itself already lacks two of six.

**Limits.** These are single runs submitted to a shared task, with settings chosen by their teams. They are not tuned for this topic and do not show run-to-run variation.

## Reference

Kanoulas, E., Li, D., Azzopardi, L., & Spijker, R. (2019). CLEF 2019 technology assisted reviews in empirical medicine overview. In *CLEF 2019 Working Notes* (CEUR Workshop Proceedings, Vol. 2380, paper 250). https://ceur-ws.org/Vol-2380/paper_250.pdf
