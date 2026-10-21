# Plan

Date: 2026-10-21  
Status: Planning. Nothing has been drafted.

## Decision record

| Date | Decision |
|---|---|
| 2026-10-21 | Write a separate, independent textbook in its own repository. Do not restructure *How Search Decides What You See*, and do not write a companion that depends on links into it. |

This plan descends from three planning records in the earlier book's repository: the [initial proposal](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/ce9db34/reviews/evidence-synthesis-plan-2026-10-21.md), the [reconsidered recommendation](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/342cd92/reviews/evidence-synthesis-plan-reconsidered-2026-10-21.md) and the [third iteration](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/bec8eb3/reviews/evidence-synthesis-plan-rethought-2026-10-21.md). The third iteration recommended a linked companion volume. The decision above supersedes that recommendation; the rest of its analysis still applies.

**Consequence of independence.** The book must explain every retrieval mechanism it relies on. Material adapted from the earlier book is rewritten around evidence-synthesis examples rather than copied, so the two books diverge deliberately instead of needing parallel corrections.

## Reader and promise

The reader can build structured Boolean searches and supports or conducts evidence syntheses. The book does not teach how to conduct a review or basic database searching.

The promise: **understand how retrieval decisions change the evidence available to a review, diagnose where eligible studies were lost, and evaluate proposed tools and workflows against the claim being made for them.**

## Principles

1. **Start from the reader's tools.** Each mechanism is introduced inside a system the reader already uses, then generalised. PubMed is the running case through Part II because its query mapping, ranking, similar-articles feature and automated indexing are documented well enough to examine.
2. **Teach consequences, not taxonomy.** For each mechanism: what evidence it preserves, what it can lose, and a test the reader can run.
3. **Build on the information-specialist literature.** Search validation, filter development, peer review and reporting already have a substantial evidence base (Sampson et al., 2006; Hausner et al., 2012, 2015; Bramer et al., 2017; McGowan et al., 2016; Rethlefsen et al., 2021). The book connects that work to retrieval evaluation rather than replacing it.
4. **Treat stopping as one problem.** Deciding when to stop searching and when to stop screening share an unknown denominator (Booth, 2010; Kastner et al., 2009).
5. **Align AI guidance with existing governance.** The joint Cochrane, Campbell, JBI and CEE position statement (Flemyng et al., 2025) and the RAISE guidance (RAISE, 2025) set expectations. The book explains mechanisms so readers can meet them; it does not propose a parallel framework.
6. **Date every product claim.** Mechanism explanations must survive product changes.
7. **Supply the data.** Every exercise has inputs and worked answers.

## Structure

Eleven chapters in three parts, with four appendices.

| Part | Chapter | Decision the reader can make |
|---|---|---|
| I. The problem | 1. Where eligible studies go missing | Locate a loss at coverage, indexing, query, ranking or export limit, deduplication, prioritisation or stopping |
| II. How the systems work | 2. Boolean admission, indexes and analysers | Predict how truncation, phrases, proximity and fields change which records are admitted, on each platform |
| | 3. Subject indexing, search filters and inherited classifiers | Judge when a subject heading, search filter or study-design classifier can be relied on, and how to test it |
| | 4. Ranking, relevance sorts and result limits | Distinguish a change in order from a change in what can be exported or screened |
| | 5. Learnt representations and what they were trained to find | Assess whether a model's training signal and indexed text suit the review's task |
| | 6. Multi-stage pipelines, AI research assistants and agentic search | Locate which stage can add evidence, which only reorders it, and what the trace shows |
| III. Practice | 7. Developing and translating the strategy | Turn eligibility criteria into a strategy, use term mining and LLM drafting with checks, and translate without changing intent |
| | 8. Citation, similarity and other supplementary routes | Decide what a route can add, under what coverage, and how to record it |
| | 9. Stopping in searching and screening | Separate ranking efficiency from a defensible decision to stop |
| | 10. Validating a search, route or tool | Choose the comparison a claim needs and state what it cannot show |
| | 11. Recording, reporting and updating | Produce a record another librarian can rerun, audit and update |

Appendices: A. Review types and what they ask of the search; B. Measures reference; C. Case-pack documentation; D. Terminology map.

[`chapter-map.md`](chapter-map.md) gives each chapter's sources, treatment and new material.

## Validation: the central contribution

Chapter 10 carries the largest share of new work. It is organised by the claim being tested, because different claims need different comparisons.

| Claim | Main comparison | Essential qualification |
|---|---|---|
| A route adds useful evidence | Eligible records added to the existing search, with extra screening and search effort | Useful additions do not establish complete recall or justify replacing the baseline |
| A route can replace an existing one | Recovery and misses against an explicitly bounded reference set across several topics | Recovering familiar seeds on one topic does not support broad substitution |
| A component performs better | Methods compared on the same corpus, fields and labels | Isolates a mechanism; says little about different commercial collections |
| One product is better than another | Services compared as used, documenting coverage, access and limits | Coverage differences are part of the result; do not attribute it all to ranking |
| Screening prioritisation helps | Relevant records found at fixed effort on a fixed pool | A better order does not enlarge the pool |
| Early stopping is safe | Misses at the stopping point in labelled simulations, with variability | Ranking efficiency does not show the target was reached in a live review |
| An update is adequate | New eligible reports, indexing delays, revised strategies and changed product behaviour | Rerunning a saved query does not establish stable coverage |

The chapter connects these designs to relative recall (Sampson et al., 2006), development and validation sets in the objective approach (Hausner et al., 2012, 2015), database-combination studies (Bramer et al., 2017) and search-system suitability criteria (Gusenbauer & Haddaway, 2020). For example, relative recall inherits the bias of its reference set much as pooled relevance judgements inherit the bias of the pooled runs.

A synthetic example runs throughout: a fully labelled teaching collection holds 100 eligible reports; retrieval admits 90; screening stops after finding 81 of those. Retrieval recall is 90%, recall within the pool is 90%, and end-to-end recovery is 81%. A live review does not know the corresponding total.

## Case pack

- **SYNERGY** (De Bruin et al., 2023): 26 reviews, 169,288 records and 2,834 inclusions, released under CC0. Run screening simulations once and publish the logs, so stopping exercises need no code.
- **CLEF TAR 2017–2019** (Kanoulas et al., 2017) and **Scells et al. (2017)**: review topics with Boolean queries, PubMed identifiers and relevance labels, for diagnosis, translation and validation exercises. Confirm reuse terms before redistributing. Public labels may have appeared in model training data; say so wherever they are used to test AI tools.
- **Non-health contrast case:** check whether any SYNERGY topic outside health is suitable before building one. If a new one is needed, keep it small and document how it was labelled.
- **Synthetic teaching collection:** small and fully labelled, for controlled experiments. Always labelled as synthetic.

## Assessment

Three connected exercises carry the core:

1. Diagnose why a known eligible report was missed, test a remedy and state what the evidence establishes.
2. Evaluate an additional retrieval route against a baseline, reporting overlap, eligible additions, workload and unresolved recall limits.
3. Compare screening order and stopping on the same labelled pool, identifying which reports each simulated stop leaves unseen.

The final assessment is a short recommendation to a review team about a proposed workflow. A well-supported decision not to adopt a tool earns the same credit as a well-supported adoption.

## Open decisions

| Decision | Recommendation | Why it matters |
|---|---|---|
| Source format | Decide before drafting Chapter 1. A mainstream book toolchain with managed citations (for example Quarto with BibTeX) suits a citation-heavy book and avoids rebuilding bespoke tooling. Reusing the earlier book's single-HTML format keeps the author's existing editor and scripts. | Changing format after drafting is expensive |
| Disciplinary balance | Health-led, with one sustained non-health contrast case | Balanced coverage roughly doubles the case work, because vocabularies and labelled datasets differ |
| Product-claim maintenance | Keep a dated evidence register from the first chapter and set an annual re-check | PubMed, NLM and AI-tool behaviour changes faster than the mechanisms |
| Final title | Keep the working title until the pilot | Title should match what readers find most useful |

## Implementation sequence

1. Settle the open decisions above.
2. Build the case pack and record provenance and licences.
3. Draft Chapter 1 and Chapter 10 first: they define the problem and the evidence needed to judge a solution.
4. Draft Chapter 3, the largest gap, then Chapters 2 and 4 around the PubMed running case. Register every product claim with a check date.
5. Pilot Chapters 1, 3 and 10 and their exercises with a small group of practising evidence-synthesis librarians. Record where they fail.
6. Draft the remaining chapters, adjusting the depth of Part II to what the pilot showed readers needed.
7. Publish a first public draft on GitHub Pages.

## References

Booth, A. (2010). How much searching is enough? Comprehensive versus optimal retrieval for technology assessments. *International Journal of Technology Assessment in Health Care, 26*(4), 431–435. https://doi.org/10.1017/S0266462310000966

Bramer, W. M., Rethlefsen, M. L., Kleijnen, J., & Franco, O. H. (2017). Optimal database combinations for literature searches in systematic reviews: A prospective exploratory study. *Systematic Reviews, 6*, 245. https://doi.org/10.1186/s13643-017-0644-y

De Bruin, J., Ma, Y., Ferdinands, G., Teijema, J., & Van de Schoot, R. (2023). *SYNERGY: Open machine learning dataset on study selection in systematic reviews* [Data set]. DataverseNL. https://doi.org/10.34894/HE6NAQ

Flemyng, E., Noel-Storr, A., Macura, B., Gartlehner, G., Thomas, J., et al. (2025). Position statement on artificial intelligence (AI) use in evidence synthesis across Cochrane, the Campbell Collaboration, JBI and the Collaboration for Environmental Evidence 2025. *Environmental Evidence*. https://doi.org/10.1186/s13750-025-00374-5

Gusenbauer, M., & Haddaway, N. R. (2020). Which academic search systems are suitable for systematic reviews or meta-analyses? Evaluating retrieval qualities of Google Scholar, PubMed, and 26 other resources. *Research Synthesis Methods, 11*(2), 181–217. https://doi.org/10.1002/jrsm.1378

Hausner, E., Guddat, C., Hermanns, T., Lampert, U., & Waffenschmidt, S. (2015). Development of search strategies for systematic reviews: Validation showed the noninferiority of the objective approach. *Journal of Clinical Epidemiology, 68*(2), 191–199. https://doi.org/10.1016/j.jclinepi.2014.09.016

Hausner, E., Waffenschmidt, S., Kaiser, T., & Simon, M. (2012). Routine development of objectively derived search strategies. *Systematic Reviews, 1*, 19. https://doi.org/10.1186/2046-4053-1-19

Kanoulas, E., Li, D., Azzopardi, L., & Spijker, R. (2017). CLEF 2017 technologically assisted reviews in empirical medicine overview. In *CLEF 2017 Working Notes* (CEUR Workshop Proceedings). https://openalex.org/W2785937154

Kastner, M., Straus, S. E., McKibbon, K. A., & Goldsmith, C. H. (2009). The capture–mark–recapture technique can be used as a stopping rule when searching in systematic reviews. *Journal of Clinical Epidemiology, 62*(2), 149–157. https://doi.org/10.1016/j.jclinepi.2008.06.001

McGowan, J., Sampson, M., Salzwedel, D. M., Cogo, E., Foerster, V., & Lefebvre, C. (2016). PRESS Peer Review of Electronic Search Strategies: 2015 guideline statement. *Journal of Clinical Epidemiology, 75*, 40–46. https://doi.org/10.1016/j.jclinepi.2016.01.021

RAISE. (2025). *Responsible use of AI in evidence synthesis (RAISE): Recommendations and guidance*. Open Science Framework. https://osf.io/fwaud/

Rethlefsen, M. L., Kirtley, S., Waffenschmidt, S., Ayala, A. P., Moher, D., Page, M. J., Koffel, J. B., & PRISMA-S Group. (2021). PRISMA-S: An extension to the PRISMA statement for reporting literature searches in systematic reviews. *Systematic Reviews, 10*, 39. https://doi.org/10.1186/s13643-020-01542-z

Sampson, M., Zhang, L., Morrison, A., Barrowman, N. J., Clifford, T. J., Platt, R. W., Klassen, T. P., & Moher, D. (2006). An alternative to the hand searching gold standard: Validating methodological search filters using relative recall. *BMC Medical Research Methodology, 6*, 33. https://doi.org/10.1186/1471-2288-6-33

Scells, H., Zuccon, G., Koopman, B., Deacon, A., Azzopardi, L., & Geva, S. (2017). A test collection for evaluating retrieval of studies for inclusion in systematic reviews. In *Proceedings of the 40th International ACM SIGIR Conference on Research and Development in Information Retrieval* (pp. 1237–1240). https://doi.org/10.1145/3077136.3080707
