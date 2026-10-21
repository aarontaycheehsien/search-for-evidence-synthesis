# Case pack

Status: sources selected and licences checked on 2026-10-21; first data, logs and the synthetic collection built the same day.  
Machine-readable record: [`case-pack/sources.csv`](../case-pack/sources.csv).

The case pack supplies the inputs and worked answers for every exercise in the book, so that instructors do not have to prepare them.

## What is built

| Artefact | Location | Supports |
|---|---|---|
| CD010558 reference set: the review's 6 included studies and 20 listed references, mapped to identifiers and compared with the CLEF pool | [`case-pack/reference-sets/`](../case-pack/reference-sets/README.md) | Chapters 1, 2, 10, 11 |
| CD010558 screening logs from three CLEF 2019 participant runs | [`case-pack/data/clef-2019/CD010558/`](../case-pack/data/clef-2019/CD010558/README.md) | Chapter 9 |
| Moran et al. (2021) labels (4,882 records) and three ASReview simulation logs | [`case-pack/data/moran-2021/`](../case-pack/data/moran-2021/README.md) | Chapters 9, 10 |
| Synthetic collection v0.1 (33 records, 9 eligible studies) with generated worked answers | [`case-pack/synthetic/`](../case-pack/synthetic/README.md) | Chapters 1, 2, 3, 7, 8, 11 |
| Scripts and offline tests | `case-pack/scripts/`, `case-pack/tests/` | Rebuilding all of the above |

Run the tests with `python -m unittest discover -s case-pack/tests`.

## Rules for the case pack

1. **Commit identifiers, labels and our own derived files. Do not commit third-party titles, abstracts or database exports.** Fetch them at build time with a script and record the fetch date. NLM states that PubMed abstracts may be protected by copyright and that it gives no permission to redistribute them (National Library of Medicine [NLM], n.d.). Web of Science and Scopus exports are covered by their providers' terms.
2. **Record provenance for every file:** source, version or commit, licence, retrieval date and every transformation.
3. **Label synthetic material as synthetic.**
4. **State the contamination risk.** Public review topics and labels may be in the training data of language models. Any exercise that tests an AI tool on these topics must say so.
5. **State what each reference set can and cannot show.** See the next section.
6. **Check benchmark labels before using them.** SYNERGY version 1's Moran labels turned out to be wrong; see below.

## What these datasets can and cannot show

All the candidate sources build their labels from a review's own search results. A study that the review found only by another route, or that its search missed entirely, is usually absent.

- **CLEF TAR** gives the PubMed records returned when the organisers re-ran each review's Ovid MEDLINE strategy with the review's date range, and drops cited studies outside that result (Kanoulas et al., 2019). It can test screening order and stopping, and whether an *alternative* query loses records the original admitted. It cannot show what the original strategy missed.
- **SYNERGY** labels each review's screened pool. The same limit applies.

The CD010558 reference set shows the size of the gap in one case: the CLEF pool contains reports of 4 of the review's 6 included studies, and 10 of its 16 PubMed-indexed publications. One missing study has no PubMed record; for the other, the leading explanation is that Ovid's `ed` field holds the Date Completed, so re-running the review's entry-date limit later excludes records indexed after the cut-off (Wolters Kluwer, n.d.). That explanation is not yet confirmed.

## Sources

### SYNERGY (screening, stopping and the non-health case)

| | |
|---|---|
| Citation | De Bruin et al. (2023), version 1 |
| Repository checked | `asreview/synergy-dataset` at commit `dc2dadf`, 2026-10-21 |
| Licence | CC0 1.0 (repository `LICENSE` and DataverseNL record). Records are OpenAlex work objects; OpenAlex metadata is CC0. |
| Contents | 26 active reviews, 169,288 records and 2,834 inclusions. Each review carries its eligibility criteria as text, which suits the Chapter 1 contrast between topical relevance and eligibility. |
| Labels | `label_included` marks inclusion after full-text screening. A record that passed title and abstract screening but was excluded at full text is labelled 0. |
| Commit | Identifiers and labels for the chosen reviews; our simulation logs |
| Fetch | Titles and abstracts, using the `synergy-dataset` package (OpenAlex) or, for Moran, the authors' export |
| Attribution | Credit the original review authors listed in the repository's `ATTRIBUTION.md` as well as the dataset. |

The metadata file lists 46 reviews, of which 20 are inactive with stated reasons, including one licence problem. Use only active reviews.

**Version 1's Moran labels are wrong.** Of the 107 records it labels as included that have a DOI, 2 are full-text inclusions in the corrected labels and 7 passed title-and-abstract screening. The maintainers added a corrected variant in January 2025 and say version 1 will stay unchanged for comparability, with fixes going into a future SYNERGY PLUS (repository issue 184). The case pack uses the corrected variant; details in [`case-pack/data/moran-2021/README.md`](../case-pack/data/moran-2021/README.md). Whether other version 1 reviews have similar problems has not been checked.

### CLEF TAR 2017–2019 (health running case, translation, screening)

| | |
|---|---|
| Citation | Kanoulas et al. (2017, 2019) |
| Repository checked | `CLEF-TAR/tar` at commit `dbc13d0`, 2026-10-21 |
| Licence | MIT, copyright 2017 Leif Azzopardi |
| Contents | For each topic: Cochrane review identifier, title, the review's Ovid MEDLINE strategy, the PubMed identifiers it returned, and relevance labels at title-and-abstract and full-text level in TREC format. The 2019 test set has 8 diagnostic accuracy, 20 intervention, 1 prognosis and 2 qualitative topics. Participant runs are included. |
| Commit | Topic identifiers, PubMed identifiers, labels and participant-run orderings for the chosen topics; strategies quoted with attribution |
| Fetch | PubMed records through NCBI E-utilities |

**Limits.** The strategies were taken from Cochrane reviews. The repository's MIT licence may not cover rights that Cochrane or Wiley hold in them, so quote individual strategies with attribution to the Cochrane review and do not redistribute them in bulk without confirmation. Later users have reported format errors and deleted PubMed identifiers in the release. Running a strategy today will not return the 2017–2019 set, because of indexing changes and the move to automated MeSH indexing in 2022.

**Recommended running case: CD010558**, *Psychological therapies for treatment-resistant depression in adults* (Ijaz et al., 2018). Its 33-line strategy has a subject heading, free text with proximity and field codes, a randomised-trial filter, a `NOT` block for animals and publication types, and an entry-date limit. Its pool is moderate (2,815 records; 37 eligible at title and abstract, 10 at full text), and its six included studies are few enough to map completely. Awaiting the author's confirmation.

**Other candidates kept:**

| Topic | Review | Pool | Eligible at title and abstract | Eligible at full text | Use |
|---|---|---|---|---|---|
| CD011787 | Parents' and informal caregivers' views and experiences of communication about routine childhood vaccination (qualitative) | 4,369 | 111 | 28 | Chapter 3: a strategy built mainly on subject headings; qualitative synthesis |
| CD012069 | Methylphenidate for ADHD in children and adolescents (adverse events in non-randomised studies) | 3,479 | 320 | 245 | Chapter 9: many eligible records; a long strategy for Chapter 7's peer-review exercise |

### Scells et al. (2017) collection (not adopted)

| | |
|---|---|
| Repository checked | `ielab/sigir2017-pico-collection` at commit `218cc82`, 2026-10-21 |
| Licence | None stated. Treat as all rights reserved. |
| Contents | 94 Cochrane topics, queries as published and as PICO-annotated variants, and citation lists marking included studies |

Not adopted, because it cannot be redistributed and CLEF TAR covers the same ground.

### Non-health contrast case: Moran et al. (2021)

*Poor nutritional condition promotes high-risk behaviours: a systematic review and meta-analysis*, a preregistered behavioural-ecology review published open access under CC BY-NC.

**Why this review.**

- The authors' public repository holds the Web of Science and Scopus strategies, raw exports from each database, the combined count before deduplication (7,208: 2,729 from Web of Science and 4,479 from Scopus) and the screening export.
- The same logic appears in two syntaxes (`TS=` with `NEAR/10` against `TITLE-ABS-KEY` with `W/10`, including leading truncation such as `"*nutrition*"`): the Chapter 7 translation case and Chapter 2's analyser case, with no controlled vocabulary.
- Some eligibility criteria cannot sensibly be searched, such as excluding domesticated and laboratory breeds and micronutrient manipulations.
- The vocabulary is varied (boldness, neophobia, exploration, risk-taking, coping style).
- The article reports 15 records found outside the database searches, 5 of which contributed data (Moran et al., 2021): a ready example for Chapter 8.
- The corrected SYNERGY labels match the article's counts (5,453 records screened at title and abstract, 626 sent to full text), so both screening stages can be taught.

**Checks.**

1. **Still open:** the search script's comments are inconsistent. The header dates the searches 10 November 2019, while the per-database comments say `10_11_18`; the preregistration is dated 9 November 2018. The Web of Science string reads `"asset protection" residual reproductive value")` where the Scopus string reads `"asset protection" OR "residual reproductive value"`. The article puts the full strategy in Appendix S2 of its supporting information (`brv12655-sup-0001-Supinfo.docx`), which could not be fetched from this environment. If the published Web of Science string has the same defect, it is a genuine example of a quiet translation error; if not, it is a slip in the script comment and must not be presented as the executed search.
2. **Resolved:** the OSF project (osf.io/3tphj) is licensed CC BY 4.0, checked 2026-10-21. The GitHub repository has no licence file. Quote the strategies with attribution; do not redistribute the `.bib` exports, which contain Web of Science and Scopus records.

Repository checked: `NPMoran/metah06_condition-dependence-of-boldness_OSF` at commit `b25a3c2`, 2026-10-21.

**Reserve:** Smid et al. (2020) in SYNERGY, a social-science methods review (2,627 records, 27 inclusions). Its search strategy and labels have not been checked.

### Synthetic teaching collection

Version 0.1 is built: a fictional education review with 33 records and 9 eligible studies, licensed CC BY 4.0. See [`case-pack/synthetic/README.md`](../case-pack/synthetic/README.md).

## Remaining work

1. Check Appendix S2 of the Moran supplement against the script comments (check 1 above).
2. Confirm Date Completed for PMIDs 28252882 and 28266318, and test why PMIDs 26777773 and 27100125 are missing from the CD010558 pool. `case-pack/scripts/fetch_pubmed.py` records Date Completed but needs network access to NCBI.
3. Decide whether to post the SYNERGY query ([`docs/outreach/synergy-moran-corrected.md`](outreach/synergy-moran-corrected.md)).
4. Run the Moran simulations with several prior pairs and seeds to show variation, not one run.
5. Build reference sets for CD011787 and CD012069 if they are used.
6. Pilot the synthetic collection's exercises and extend it after feedback.

## References

De Bruin, J., Ma, Y., Ferdinands, G., Teijema, J., & Van de Schoot, R. (2023). *SYNERGY: Open machine learning dataset on study selection in systematic reviews* (Version 1) [Data set]. DataverseNL. https://doi.org/10.34894/HE6NAQ

Ijaz, S., Davies, P., Williams, C. J., Kessler, D., Lewis, G., & Wiles, N. (2018). Psychological therapies for treatment-resistant depression in adults. *Cochrane Database of Systematic Reviews*, (5), CD010558. https://doi.org/10.1002/14651858.CD010558.pub2

Kanoulas, E., Li, D., Azzopardi, L., & Spijker, R. (2017). CLEF 2017 technologically assisted reviews in empirical medicine overview. In *CLEF 2017 Working Notes* (CEUR Workshop Proceedings). https://openalex.org/W2785937154

Kanoulas, E., Li, D., Azzopardi, L., & Spijker, R. (2019). CLEF 2019 technology assisted reviews in empirical medicine overview. In *CLEF 2019 Working Notes* (CEUR Workshop Proceedings, Vol. 2380, paper 250). https://ceur-ws.org/Vol-2380/paper_250.pdf

Moran, N. P., Sánchez-Tójar, A., Schielzeth, H., & Reinhold, K. (2021). Poor nutritional condition promotes high-risk behaviours: A systematic review and meta-analysis. *Biological Reviews, 96*(1), 269–288. https://doi.org/10.1111/brv.12655

National Library of Medicine. (n.d.). *Copyright information and downloading National Library of Medicine data*. Retrieved 21 October 2026, from https://www.nlm.nih.gov/databases/download.html

Scells, H., Zuccon, G., Koopman, B., Deacon, A., Azzopardi, L., & Geva, S. (2017). A test collection for evaluating retrieval of studies for inclusion in systematic reviews. In *Proceedings of the 40th International ACM SIGIR Conference on Research and Development in Information Retrieval* (pp. 1237–1240). https://doi.org/10.1145/3077136.3080707

Smid, S. C., McNeish, D., Miočević, M., & Van de Schoot, R. (2020). Bayesian versus frequentist estimation for structural equation models in small sample contexts: A systematic review. *Structural Equation Modeling, 27*(1), 131–161. https://doi.org/10.1080/10705511.2019.1577140

Wolters Kluwer. (n.d.). *Ovid MEDLINE database guide: Entry Date (ED)*. Retrieved 21 October 2026, from https://ospguides.ovid.com/OSPguides/medline.htm
