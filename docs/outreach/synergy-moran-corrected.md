# Draft: query to the SYNERGY maintainers

Status: draft for the author to post. Not sent.  
Where to post: a new issue at https://github.com/asreview/synergy-dataset/issues

---

**Title:** Status of the `Moran_2021_corrected` dataset

Hello, and thank you for SYNERGY.

I am preparing an open (CC BY 4.0) textbook for evidence-synthesis librarians and would like to use Moran et al. (2021) as a teaching case. I noticed `datasets/Moran_2021_corrected/` in the repository (checked at commit `dc2dadf`). It is not listed in `datasets.toml`, so I would like to check its status before relying on it.

What I see:

- `Moran_2021_corrected_ids.csv` has 5,453 records, 626 with `label_abstract_included = 1` and 142 with `label_included = 1`. The first two numbers match the article's report of 5,453 records screened at title and abstract and 626 selected for full text.
- The `openalex_id` column is empty for all records, and 497 records have no DOI.
- `compose.py` joins the OSF screening files (`osf.io/gmvxy` and `osf.io/5zw46`) on exact title.

Questions:

1. Is `Moran_2021_corrected` intended for a future release, and should it replace `Moran_2021` (5,214 records and 111 inclusions in version 1)?
2. Is it safe to use the title-and-abstract labels as they stand, given the exact-title join?
3. Would you prefer users to cite version 1 of SYNERGY and the OSF project for these labels in the meantime?

I would credit SYNERGY, the original authors and the OSF project (CC BY 4.0) wherever the labels are used.

Thank you.

---

Note for the author: the article says 147 studies met the inclusion criteria after full-text screening, which included 15 records from outside the database searches. The variant's 142 full-text inclusions are consistent with five of the 147 coming from those other sources, but that is an inference; do not state it as fact unless the maintainers or the OSF screening database confirm it.
