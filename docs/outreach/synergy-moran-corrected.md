# Draft: comment to the SYNERGY maintainers

Status: draft for the author to post. Not sent.  
Where to post: as a comment on the open "Data quality" issue, https://github.com/asreview/synergy-dataset/issues/184, which the maintainers use to collect data-quality problems for SYNERGY PLUS.

Background: the maintainers added `Moran_2021_corrected` in January 2025 (pull request 128) and state in issue 184 that version 1 will stay unchanged so that published results remain comparable. A new issue is not needed; the useful contribution is the measured size of the version 1 problem and two questions about the corrected variant.

---

Thank you for SYNERGY, and for adding the corrected Moran data.

I am preparing an open (CC BY 4.0) textbook for evidence-synthesis librarians that uses Moran et al. (2021) as a teaching case, so I compared the two versions at commit `dc2dadf`. In case it helps the SYNERGY PLUS work:

- Of the 107 records that `Moran_2021` (version 1) labels as included and that have a DOI, 2 are full-text inclusions in `Moran_2021_corrected` and 7 passed title-and-abstract screening. Version 1's labels come from `screening_ref_data_rayyan_final.csv` in the authors' repository, which appears not to contain the review's inclusions.
- `Moran_2021_corrected` reproduces the article's counts (5,453 records screened at title and abstract; 626 sent to full text). Its `openalex_id` column is empty, 497 records have no DOI, and labels are joined on exact title in `compose.py`.

Two questions:

1. Do you expect the corrected labels to change before SYNERGY PLUS, for example after matching records to OpenAlex?
2. Until then, would you prefer users to cite SYNERGY version 1 together with the OSF project (osf.io/3tphj, CC BY 4.0) for these labels?

I would credit SYNERGY, the original authors and the OSF project wherever the labels are used.

---

Note for the author: the article reports 147 studies eligible after full-text screening, which included 15 records from outside the database searches. The corrected variant's 142 full-text inclusions are consistent with five of the 147 coming from those other sources, but that is an inference; do not state it as fact unless the maintainers or the OSF screening database confirm it.
