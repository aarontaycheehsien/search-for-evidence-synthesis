# Case pack

Status: sources selected and licences checked on 2026-10-21. No data has been committed yet.  
Machine-readable record: [`case-pack/sources.csv`](../case-pack/sources.csv).

The case pack supplies the inputs and worked answers for every exercise in the book, so that instructors do not have to prepare them.

## Rules for the case pack

1. **Commit identifiers, labels and our own derived files. Do not commit third-party titles, abstracts or database exports.** Fetch them at build time with a script and record the fetch date. NLM states that PubMed abstracts may be protected by copyright and that it gives no permission to redistribute them (National Library of Medicine [NLM], n.d.). Web of Science and Scopus exports are covered by their providers' terms.
2. **Record provenance for every file:** source, version or commit, licence, retrieval date and every transformation.
3. **Label synthetic material as synthetic.**
4. **State the contamination risk.** Public review topics and labels may be in the training data of language models. Any exercise that tests an AI tool on these topics must say so.
5. **State what each reference set can and cannot show.** See the next section.

## What these datasets can and cannot show

All three candidate sources build their labels from a review's own search results. A study that the review found only by another route, or that its search missed entirely, is usually absent.

- **CLEF TAR** gives the PubMed records returned by each review's MEDLINE strategy, with labels for those records only. By construction, the original strategy therefore retrieves every labelled eligible record. The data can test screening order and stopping, and whether an *alternative* query loses records the original admitted. It cannot show what the original strategy missed.
- **SYNERGY** labels each review's screened pool. The same limit applies.

For the validation exercises in Chapter 10, derive a separate reference set: take the included studies from the review's own published reference list, map them to PubMed identifiers or DOIs ourselves, and record the method. Bibliographic facts in a reference list can be compiled without copying copyrighted text. Then compare that set with what the strategy returned.

## Sources

### SYNERGY (screening, stopping and the non-health case)

| | |
|---|---|
| Citation | De Bruin et al. (2023), version 1 |
| Repository checked | `asreview/synergy-dataset` at commit `dc2dadf`, 2026-10-21 |
| Licence | CC0 1.0 (repository `LICENSE` and DataverseNL record). Records are OpenAlex work objects; OpenAlex metadata is CC0. |
| Contents | 26 active reviews, 169,288 records and 2,834 inclusions. Each review carries its eligibility criteria as text, which suits the Chapter 1 contrast between topical relevance and eligibility. |
| Labels | `label_included` marks inclusion after full-text screening. A record that passed title and abstract screening but was excluded at full text is labelled 0. |
| Commit | OpenAlex identifiers and labels for the chosen reviews; our simulation logs |
| Fetch | Titles and abstracts, using the `synergy-dataset` package |
| Attribution | Credit the original review authors listed in the repository's `ATTRIBUTION.md` as well as the dataset. |

The metadata file lists 46 reviews, of which 20 are inactive with stated reasons, including one licence problem. Use only active reviews.

### CLEF TAR 2017–2019 (health running case, translation, screening)

| | |
|---|---|
| Citation | Kanoulas et al. (2017, 2019) |
| Repository checked | `CLEF-TAR/tar` at commit `dbc13d0`, 2026-10-21 |
| Licence | MIT, copyright 2017 Leif Azzopardi |
| Contents | For each topic: Cochrane review identifier, title, the review's Ovid MEDLINE strategy, the PubMed identifiers it returned, and relevance labels at title-and-abstract and full-text level in TREC format. The 2019 test set has 8 diagnostic accuracy, 20 intervention, 1 prognosis and 2 qualitative topics. |
| Commit | Topic identifiers, PubMed identifiers and labels for the chosen topics; strategies quoted with attribution |
| Fetch | PubMed records through NCBI E-utilities |

**Limits.** The strategies were taken from Cochrane reviews. The repository's MIT licence may not cover rights that Cochrane or Wiley hold in them, so quote individual strategies with attribution to the Cochrane review and do not redistribute them in bulk without confirmation. Later users have reported format errors and deleted PubMed identifiers in the release. Running a strategy today will not return the 2017–2019 set, because of indexing changes and the move to automated MeSH indexing in 2022. Chapter 11's update case can use that difference.

**Candidate topics** (2019 test set; to be confirmed after reading each strategy and review):

| Topic | Review | Pool | Eligible at title and abstract | Eligible at full text | Proposed use |
|---|---|---|---|---|---|
| CD010558 | Psychological therapies for treatment-resistant depression in adults | 2,815 | 37 | 10 | Running case: moderate pool, mixed MeSH and free text, complex-intervention vocabulary |
| CD011787 | Parents' and informal caregivers' views and experiences of communication about routine childhood vaccination (qualitative) | 4,369 | 111 | 28 | Chapter 3: a strategy built mainly on subject headings; qualitative synthesis |
| CD012069 | Methylphenidate for ADHD in children and adolescents | 3,479 | 320 | 245 | Chapter 9: enough eligible records for stable screening simulations |

Counts come from the repository's 2019 test qrels. The gap between title-and-abstract and full-text eligibility (for example 78 against 5 in CD009069) is itself teaching material for Chapter 1.

### Scells et al. (2017) collection (not adopted)

| | |
|---|---|
| Repository checked | `ielab/sigir2017-pico-collection` at commit `218cc82`, 2026-10-21 |
| Licence | None stated. Treat as all rights reserved. |
| Contents | 94 Cochrane topics, queries as published and as PICO-annotated variants, and citation lists marking included studies |

Not adopted, because it cannot be redistributed and CLEF TAR covers the same ground. Its included-study lists would suit the Chapter 10 reference sets; ask the authors for permission if that saves enough work. Otherwise cite it as background only.

### Non-health contrast case: Moran et al. (2021)

*Poor nutritional condition promotes high-risk behaviours: a systematic review and meta-analysis*, a preregistered behavioural-ecology review published open access under CC BY-NC.

**Why this review.**

- It is in SYNERGY (5,214 records and 111 inclusions in version 1), with its eligibility criteria.
- The authors' public repository holds the Web of Science and Scopus strategies, raw exports from each database, the combined count before deduplication (7,208: 2,729 from Web of Science and 4,479 from Scopus) and the screening data.
- The same logic appears in two syntaxes (`TS=` with `NEAR/10` against `TITLE-ABS-KEY` with `W/10`, including leading truncation such as `"*nutrition*"`). That is the Chapter 7 translation case and Chapter 2's analyser case without any controlled vocabulary.
- Some eligibility criteria cannot sensibly be searched, such as excluding domesticated and laboratory breeds and micronutrient manipulations. This illustrates why not every criterion becomes a search block.
- The vocabulary is varied (boldness, neophobia, exploration, risk-taking, coping style), which suits Chapters 5 and 13 on vocabulary mismatch.
- An unreleased "corrected" SYNERGY variant has both title-and-abstract labels (626) and full-text labels (142) for 5,453 records. This would support teaching both screening stages, but its status must be confirmed with the SYNERGY maintainers first.

**Checks before use.**

1. The search script's comments are inconsistent. The header dates the searches 10 November 2019, while the per-database comments say `10_11_18`. The Web of Science string reads `"asset protection" residual reproductive value")` where the Scopus string reads `"asset protection" OR "residual reproductive value"`. Compare both with the article's supplementary search record. If the published Web of Science string has the same defect, it is a genuine example of a quiet translation error. If not, it is a transcription slip in the script comment and must not be presented as the executed search.
2. The authors' repository has no licence file, and the OSF project's licence could not be reached from this environment. Until confirmed: link to the repository, quote the strategies with attribution, and use SYNERGY's CC0 identifiers and labels. Do not redistribute the `.bib` exports, which contain Web of Science and Scopus records.

Repository checked: `NPMoran/metah06_condition-dependence-of-boldness_OSF` at commit `b25a3c2`, 2026-10-21.

**Reserve:** Smid et al. (2020) in SYNERGY, a social-science methods review (2,627 records, 27 inclusions). Its search strategy has not been checked.

### Synthetic teaching collection (to build)

A small, fully labelled collection written for the book, licensed CC BY 4.0 and always labelled synthetic. It supports controlled experiments where every eligible record is known.

## Next steps

1. Check the two Moran items above against the published supplement, and confirm the OSF licence.
2. Ask the SYNERGY maintainers about the status of the `Moran_2021_corrected` variant.
3. Read the three candidate CLEF strategies and their reviews, and confirm the running case.
4. Build the Chapter 10 reference sets from the reviews' published included studies, mapped to identifiers by a recorded method.
5. Write fetch scripts that place third-party records in an ignored cache, never in Git.
6. Run screening simulations on Moran 2021 and one health review, and commit the logs with their software versions and settings.
7. Write the synthetic collection.

## References

De Bruin, J., Ma, Y., Ferdinands, G., Teijema, J., & Van de Schoot, R. (2023). *SYNERGY: Open machine learning dataset on study selection in systematic reviews* (Version 1) [Data set]. DataverseNL. https://doi.org/10.34894/HE6NAQ

Kanoulas, E., Li, D., Azzopardi, L., & Spijker, R. (2017). CLEF 2017 technologically assisted reviews in empirical medicine overview. In *CLEF 2017 Working Notes* (CEUR Workshop Proceedings). https://openalex.org/W2785937154

Kanoulas, E., Li, D., Azzopardi, L., & Spijker, R. (2019). CLEF 2019 technology assisted reviews in empirical medicine overview. In *CLEF 2019 Working Notes* (CEUR Workshop Proceedings, Vol. 2380, paper 250). https://ceur-ws.org/Vol-2380/paper_250.pdf

Moran, N. P., Sánchez-Tójar, A., Schielzeth, H., & Reinhold, K. (2021). Poor nutritional condition promotes high-risk behaviours: A systematic review and meta-analysis. *Biological Reviews, 96*(1), 269–288. https://doi.org/10.1111/brv.12655

National Library of Medicine. (n.d.). *Copyright information and downloading National Library of Medicine data*. Retrieved 21 October 2026, from https://www.nlm.nih.gov/databases/download.html

Scells, H., Zuccon, G., Koopman, B., Deacon, A., Azzopardi, L., & Geva, S. (2017). A test collection for evaluating retrieval of studies for inclusion in systematic reviews. In *Proceedings of the 40th International ACM SIGIR Conference on Research and Development in Information Retrieval* (pp. 1237–1240). https://doi.org/10.1145/3077136.3080707

Smid, S. C., McNeish, D., Miočević, M., & Van de Schoot, R. (2020). Bayesian versus frequentist estimation for structural equation models in small sample contexts: A systematic review. *Structural Equation Modeling, 27*(1), 131–161. https://doi.org/10.1080/10705511.2019.1577140
