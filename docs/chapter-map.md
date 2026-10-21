# Chapter map

For each planned chapter: the sections of *How Search Decides What You See* it draws on, how they are treated, what is new, and which product claims must be verified before publication.

**Source edition:** `search-textbook.html` at commit [`99bfb9c`](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/99bfb9c5f4aaa8a9722c28559950ea17e8c399c5/search-textbook.html) of [Information-retrieval-crashcourse](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse). Section anchors below refer to that file; the [published edition](https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/search-textbook.html) may have moved on.

**Treatment key:**

- **Adapt:** keep the explanation, replace the examples with evidence-synthesis cases, and cut what the chapter does not need.
- **Compress:** keep only what explains a consequence for review searching.
- **New:** no usable source text.

Record the source commit in the commit message whenever adapted text is added.

## Part I. The problem

### 1. Where eligible studies go missing

**Drafted 2026-10-21** as new text built on the case pack; no source text was adapted. The source sections below remain available if a later revision needs them.

| Source section | Anchor | Treatment |
|---|---|---|
| Ch 1 The retrieval problem: "What does 'relevant' actually mean?" | `#intro` | Adapt |
| Ch 14 Measuring whether retrieval worked: precision, recall and the unknown denominator | `#evaluation` | Adapt |
| App F: boundary figure (F.3), candidate retrieval versus screening, deduplication paragraph | `#appendix-evidence-synthesis-high-recall-retrieval` | Adapt |

**New:** opening case of a review that missed an eligible study; topical relevance versus eligibility; a boundary diagram that adds search stopping and deduplication; record, report and study; the synthetic 100/90/81 example.

## Part II. How the systems work

PubMed is the running case through this part. Every PubMed and NLM claim goes into the evidence register with a check date.

### 2. Boolean admission, indexes and analysers

| Source section | Anchor | Treatment |
|---|---|---|
| Ch 2 Boolean admission and the inverted index | `#boolean-admission` | Adapt; replace the slang examples with review vocabulary |
| Ch 4 Lexical search beyond strict Boolean: "A bad term", "What might have happened to a missing query word" | `#beyond-boolean` | Adapt |
| App C Advanced inverted-index execution | `#appendix-advanced-inverted-index-execution` | Omit, or a short optional box |

**New:** truncation, phrase, proximity and field behaviour as analyser and index decisions, compared across PubMed, Ovid, EBSCOhost, Embase, Scopus and Web of Science; why a syntax translation can change which records are admitted.

**Claims to verify:** each platform's documented truncation, phrase and proximity behaviour.

### 3. Subject indexing, search filters and inherited classifiers

**Drafted 2026-10-22** as new text built on the case pack (`case-pack/data/indexing/`); no source text was adapted. All product claims are in `claims/register.csv`. The MTIX date, NLM's re-indexing practice, Ovid's qualitative limit and Embase's indexing method were verified on 2026-10-22. ERIC and the Cochrane RCT Classifier's current deployment were not checked; the chapter makes no claim about either.

| Source section | Anchor | Treatment |
|---|---|---|
| Ch 11: controlled-term and structured-expression routes | `#query-transformation` | Compress |
| Ch 6 From language model to retrieval encoder: training signals | `#retrieval-encoder` | Compress |
| Ch 13 Diagnosing retrieval failure: out-of-distribution | `#diagnosing-failure` | Adapt |

**New (most of the chapter):** human versus automated subject indexing; MEDLINE's move to automated indexing in 2022 and MTIX, a neural model, from 2024, trained on 2007–2022 citations and indexing from title and abstract (National Library of Medicine [NLM], 2021, 2024, n.d.-b); what a heading-only block now inherits; indexing lag for new concepts; study-design search filters as hand-built classifiers judged by sensitivity and precision; machine-learning RCT classifiers as learnt ones (Marshall et al., 2018; Thomas et al., 2021).

**Claims to verify:** NLM indexing documentation; Embase indexing practice; whether ERIC or the chosen non-health database uses automated indexing; current status of the Cochrane RCT classifier.

### 4. Ranking, relevance sorts and result limits

| Source section | Anchor | Treatment |
|---|---|---|
| Ch 3 BM25 and ranked lexical retrieval | `#bm25-ranking` | Adapt |
| Ch 4 Lexical search beyond strict Boolean | `#beyond-boolean` | Compress |
| Ch 7 Dense retrieval at collection scale: candidate boundaries and top-k | `#dense-at-scale` | Adapt the boundary material only |
| Ch 9 Reranking: the PubMed Best Match and Primo pipelines | `#reranking-and-hybrid` | Adapt the PubMed part |
| App E Learning to rank: click logs | `#appendix-rank-fusion-and-learning-to-rank` | Compress |

**New:** a relevance sort changes order, not the Boolean result set, while a display or export limit changes what can be screened; Best Match as BM25 followed by LambdaMART reranking of the top 500, trained on search-log data (Fiorini et al., 2018); suitability of search systems for systematic searching (Gusenbauer & Haddaway, 2020).

**Claims to verify:** current Best Match documentation; Google Scholar display and export limits; relevance-sort documentation for Scopus and Web of Science.

### 5. Learnt representations and what they were trained to find

| Source section | Anchor | Treatment |
|---|---|---|
| Ch 5 Embeddings | `#embeddings` | Compress heavily; drop the Word2Vec analogy sequence |
| Ch 6 From language model to retrieval encoder | `#retrieval-encoder` | Adapt |
| Ch 7 Dense retrieval at collection scale | `#dense-at-scale` | Compress |
| Ch 8 Representations and indexed units | `#representations-and-units` | Adapt; indexed units are central |
| App A The Transformer; App B How neural models receive text | `#appendix-the-transformer`, `#appendix-character-and-byte-tokenisation` | Omit, or one short optional box |

**New:** the training signal decides what "related" means: citation links (SPECTER, already discussed in Ch 6) versus searchers' clicks (Jin et al., 2023) versus eligibility criteria; one worked contrast between a topically related report and an eligible one; abstract versus full-text indexing and what a "searches full text" claim does not settle.

**Excluded:** the Mikolov et al. PCA figure and any other third-party figure.

### 6. Multi-stage pipelines, AI research assistants and agentic search

| Source section | Anchor | Treatment |
|---|---|---|
| Ch 9 Reranking and multi-stage retrieval | `#reranking-and-hybrid` | Compress |
| Ch 10 Hybrid retrieval and rank fusion | `#hybrid-and-fusion` | Compress |
| Ch 12 Agentic search | `#agentic-search` | Adapt |
| App G Retrieval-augmented generation | `#appendix-rag` | Compress |

**New:** each route evaluated as a possible supplementary search; what an inspectable execution trace must show; documented, observed and unknown behaviour kept apart.

**Claims to verify:** every product claim, afresh. Do not carry dated claims over without re-checking.

**Excluded:** all product screenshots.

## Part III. Practice

### 7. Developing and translating the strategy

| Source section | Anchor | Treatment |
|---|---|---|
| Ch 11 Understanding, transforming and routing queries | `#query-transformation` | Adapt |
| Ch 4: "The words sent to retrieval may not be the words you typed" | `#beyond-boolean` | Adapt |

**New:** eligibility criteria versus search concepts, and why not every criterion becomes a block; term mining and the objective approach (Hausner et al., 2012, 2015); PubMed automatic term mapping (NLM, n.d.-a); LLM-drafted Boolean strategies (Wang et al., 2023; Staudinger et al., 2024); one worked translation with a quiet error; the separate roles of PRESS and PRISMA-S.

### 8. Citation, similarity and other supplementary routes

| Source section | Anchor | Treatment |
|---|---|---|
| Ch 11: seeds, citation edges and feedback | `#query-transformation` | Adapt |
| Ch 12: seed dependence in agentic tools | `#agentic-search` | Compress |

**New:** citation searching terminology and reporting (Hirt et al., 2024); citation-index coverage as a boundary; seed selection and iteration; registers, grey literature and other sources treated briefly as coverage questions.

### 9. Stopping in searching and screening

| Source section | Anchor | Treatment |
|---|---|---|
| App F: TAR, ASReview, prioritisation versus stopping, SAFE, statistical stopping, TAR metrics, controlled TAR comparison | `#appendix-evidence-synthesis-high-recall-retrieval` | Adapt; this is the chapter's core |

**New:** stopping a search (Booth, 2010; Kastner et al., 2009) alongside stopping screening; published screening logs from SYNERGY simulations, so the exercise needs no code.

**Claims to verify:** ASReview documentation; the stopping-method comparisons cited in App F.

### 10. Validating a search, route or tool

**Drafted 2026-10-21** as new text built on the case pack; no source text was adapted. The source sections below remain available if a later revision needs them.

| Source section | Anchor | Treatment |
|---|---|---|
| Ch 14: test collections, building an evaluation set, what a number cannot settle | `#evaluation` | Adapt |
| Ch 13: diagnose before choosing a remedy | `#diagnosing-failure` | Compress |
| Evaluation kit companion | `evaluation-kit.html` | Rebuild for supplement, replacement and screening comparisons |

**New (most of the chapter):** the claim-by-claim evaluation table and protocol in [`plan.md`](plan.md); relative recall, development and validation sets, and database-combination studies; review-specific test collections; RAISE's evaluation expectations.

### 11. Recording, reporting and updating

| Source section | Anchor | Treatment |
|---|---|---|
| Ch 15 Implications for library practice: reproducibility and inspectability | `#library-practice` | Adapt |
| App F: "Applying Chapter 15 to active learning" | `#appendix-evidence-synthesis-high-recall-retrieval` | Adapt |
| Vendor questionnaire companion | `vendor-questionnaire.html` | Select the questions that matter for evidence synthesis |

**New:** a completed reporting package (PRISMA-S plus AI use reported under the joint position statement); a deduplication record (McKeown & Mir, 2021); an update case in which MeSH, Best Match and an AI tool have all changed.

## Appendices

| Appendix | Source | Treatment |
|---|---|---|
| A. Review types and what they ask of the search | None | New: systematic, scoping, rapid, qualitative and mapping reviews; Campbell and CEE traditions |
| B. Measures reference | Ch 14; App F Table F.2 | Adapt: precision, recall, relative recall, number needed to read, recall at depth, recall at stopping, WSS; MAP and nDCG briefly |
| C. Case-pack documentation | None | New: provenance, licences and known limits of each dataset |
| D. Terminology map | App D `#appendix-search-terminology` | Adapt |

## Not carried over

- The Word2Vec-to-BERT progression, manual vector arithmetic and loss-function detail.
- Advanced index execution (App C), diversification methods (App E) and the Transformer appendix (App A), except as optional boxes where a chapter needs them.
- General discovery-procurement material from Ch 15.
- The three Application exercises, which are replaced by the evidence-synthesis exercises in [`plan.md`](plan.md).
- The interactive labs. Decide after the pilot whether adapted BM25 and vector labs are worth building.
- All videos and promotional material.

## References

Fiorini, N., Canese, K., Starchenko, G., Kireev, E., Kim, W., Miller, V., et al. (2018). Best Match: New relevance search for PubMed. *PLOS Biology, 16*(8), e2005343. https://doi.org/10.1371/journal.pbio.2005343

Hirt, J., Nordhausen, T., Fuerst, T., Ewald, H., & Appenzeller-Herzog, C. (2024). Guidance on terminology, application, and reporting of citation searching: The TARCiS statement. *BMJ, 385*, e078384. https://doi.org/10.1136/bmj-2023-078384

Jin, Q., Kim, W., Chen, Q., Comeau, D. C., Yeganova, L., et al. (2023). MedCPT: Contrastive pre-trained transformers with large-scale PubMed search logs for zero-shot biomedical information retrieval. *Bioinformatics, 39*(11), btad651. https://doi.org/10.1093/bioinformatics/btad651

Marshall, I. J., Noel-Storr, A., Kuiper, J., Thomas, J., & Wallace, B. C. (2018). Machine learning for identifying randomized controlled trials: An evaluation and practitioner's guide. *Research Synthesis Methods, 9*(4), 602–614. https://doi.org/10.1002/jrsm.1287

McKeown, S., & Mir, Z. M. (2021). Considerations for conducting systematic reviews: Evaluating the performance of different methods for de-duplicating references. *Systematic Reviews, 10*, 38. https://doi.org/10.1186/s13643-021-01583-y

National Library of Medicine. (2021). MEDLINE 2022 initiative: Transition to automated indexing. *NLM Technical Bulletin*, (443). https://www.nlm.nih.gov/pubs/techbull/nd21/nd21_medline_2022.html

National Library of Medicine. (2024). MTIX: The next-generation algorithm for automated indexing of MEDLINE. *NLM Technical Bulletin*, (457). https://www.nlm.nih.gov/pubs/techbull/ma24/ma24_mtix.html

National Library of Medicine. (n.d.-a). *PubMed user guide*. Retrieved 21 October 2026, from https://pubmed.ncbi.nlm.nih.gov/help/

National Library of Medicine. (n.d.-b). *Frequently asked questions about indexing for MEDLINE*. Retrieved 21 October 2026, from https://www.nlm.nih.gov/bsd/indexfaq.html

Staudinger, M., Kusa, W., Piroi, F., Lipani, A., & Hanbury, A. (2024). A reproducibility and generalizability study of large language models for query generation. In *Proceedings of the 2024 Annual International ACM SIGIR Conference on Research and Development in Information Retrieval in the Asia Pacific Region* (pp. 186–196). https://doi.org/10.1145/3673791.3698432

Thomas, J., McDonald, S., Noel-Storr, A., Shemilt, I., Elliott, J., Mavergames, C., & Marshall, I. J. (2021). Machine learning reduced workload with minimal risk of missing studies: Development and evaluation of a randomized controlled trial classifier for Cochrane Reviews. *Journal of Clinical Epidemiology, 133*, 140–151. https://doi.org/10.1016/j.jclinepi.2020.11.003

Wang, S., Scells, H., Koopman, B., & Zuccon, G. (2023). Can ChatGPT write a good Boolean query for systematic review literature search? In *Proceedings of the 46th International ACM SIGIR Conference on Research and Development in Information Retrieval* (pp. 1426–1436). https://doi.org/10.1145/3539618.3591703

Citations to Booth (2010), Hausner et al. (2012, 2015) and Kastner et al. (2009) are listed in [`plan.md`](plan.md).
