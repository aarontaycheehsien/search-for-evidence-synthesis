# Reference sets

A reference set lists every report of every study a review included, taken from the review's own published reference list and matched to identifiers by a recorded method.

CLEF TAR 2019 distributes two label sets for each topic. The screening task's (Task 2) labels judge only the records in the topic's pool, the PubMed records that the review's MEDLINE strategy returned when the organisers re-ran it, so they cannot show what that strategy missed. The search task's (Task 1) labels list the included references CLEF mapped to PMIDs, and for most topics some of them are outside the pool, although the overview says such references were left out of both label sets (Kanoulas et al., 2019). `case-pack/data/clef-2019/label-scope.csv` counts them for every test topic.

The reference sets here add what neither label set records: which report belongs to which study, included studies with no PubMed record, trial-registry entries, and corrections where CLEF's mapping is wrong. Each was built from the review's reference list before comparing it with CLEF's labels.

Columns: `reference_short` is a short bibliographic citation (facts, not copied text); `mapping_method` and `mapping_confidence` record how each identifier was found; `in_clef_pool`, `clef_abstract_label` and `clef_fulltext_label` compare the report with the CLEF 2019 topic file and qrels.

## CD010558: Psychological therapies for treatment-resistant depression in adults

Built on 2026-10-21 from the included-studies reference list of Ijaz et al. (2018), read from the PubMed Central version (PMC6494651). Identifiers were checked against PubMed records through the PubMed connector, and against OpenAlex where PubMed had no record. CLEF data: `CLEF-TAR/tar` at commit `dbc13d0`, 2019 test set.

### What it shows

| | Count |
|---|---|
| Included studies | 6 |
| References listed under those studies | 20 |
| Trial-registry records among them | 2 |
| Duplicate entry in the review's own list | 1 (the CoBalT long-term follow-up, listed twice with different author initials) |
| Distinct publications | 17 |
| With a PubMed record | 16 |
| In the CLEF pool, all labelled eligible at both levels | 10 |
| Studies represented in the CLEF pool | 4 of 6 |
| Identical to CLEF's search-task (Task 1) content-level labels | all 16 PubMed records |

The two studies with no report in the pool:

- **Wiles 2007** (the CoBalT pilot trial). Its only publication has no PubMed record, so no MEDLINE strategy could have found it. This is a coverage boundary.
- **Town 2017** (the Halifax ISTDP trial). Its report is in PubMed and appears to satisfy the strategy's search terms, but its indexing was completed after the strategy's date limit (see below).

Of the reports missing from the pool:

- **Two carry the Letter or Comment publication types** (PMIDs 23706799 and 23588772). The strategy's exclusion lines (`letter/`, `comment/`) are designed to remove such records. Here the exclusion cost two reports but no study, because other reports of CoBalT were retrieved.
- **Four were indexed after the date limit** (PMIDs 28252882, 28266318, 26777773 and 27100125). The strategy ends with `limit 32 to ed = "19480101-20170516"`. In Ovid MEDLINE, `ed` holds NLM's Date Completed, the date indexing finished, not the date the record first appeared (Wolters Kluwer, n.d.). A PubMed search on the completion-date field (`[DCOM]`) on 2026-10-21 shows that all four were completed between 17 May and 31 December 2017, while three in-pool controls (23219570, 25335963, 26799332) and both letter or comment records were completed by 16 May 2017. So when CLEF re-ran the strategy in 2019, the limit excluded them, although two of them (26777773 and 27100125) had been published in 2016. Completion dates can change when records are revised, so this reflects PubMed today rather than the database in 2019; the pattern across all four makes the explanation very likely.

Whether the review's own search in May 2017 found these records by another route, such as the in-process segment or other databases, cannot be told from these data.

### Uses in the book

- **Chapter 1, record, report and study.** Ten eligible records in the pool are reports of four studies; six of them are CoBalT. The Nakagawa study is represented only by its protocol.
- **Chapter 10, validation.** Measured against the review's included studies, the re-run MEDLINE strategy recovers 4 of 6 studies and 10 of 16 PubMed-indexed publications. A score computed on the screening labels, which judge only the pool, would report complete recall.
- **Chapter 11, updating.** The entry-date case shows why the field behind a date limit matters when a strategy is re-run: four reports, two of them published in 2016, fall outside a limit that ends in May 2017 because their indexing finished later.
- **Chapter 2, exclusions.** The `NOT` block's effect on letters and comments that a review later cites.

### To confirm before publication

1. Optionally, the exact Date Completed values for the four late-indexed records, with `case-pack/scripts/fetch_pubmed.py` once NCBI is reachable.
2. The mapping of the ACP Journal Club entry (PMID 23588772), where the review's authors differ from PubMed's. CLEF's search-task labels map it to the same PMID, an independent agreement.

## CD011787: Parents' and informal caregivers' views and experiences of communication about routine childhood vaccination (qualitative evidence synthesis)

Built on 2026-10-21 from the included-studies reference list of Ames et al. (2017), read from the PubMed Central version (PMC5461870), using the same method as above. CLEF data: 2019 test set, qualitative topics.

| | Count |
|---|---|
| Included studies (one listed report each) | 38 |
| With a PubMed record | 34 |
| In the CLEF pool | 31 |
| Labelled eligible at full text in CLEF's screening labels | 28 |
| In CLEF's search-task labels (34 PMIDs) | 31 match ours; 3 are wrong mappings |

**Not in PubMed (4).** Figueiredo 2011, Guillaume 2004, Tadesse 2009 and Tomlinson 2013 have no PubMed record that could be found by citation, title, author or DOI. Qualitative studies in nursing, health informatics and regional journals are a familiar coverage gap for MEDLINE-only searching; the review also searched Embase, CINAHL and Anthropology Plus.

**In PubMed, missing from the pool (3).** Blaisdell 2016, Dubé 2016 and Sobo 2016. The strategy ends with `limit 103 to ED=19460101-20160830`, and a PubMed completion-date search shows all three were completed after 30 August 2016, while five in-pool 2014–2015 controls were completed before it. The same entry-date mechanism as CD010558.

**In the pool, labelled not eligible (3).** Barbieri 2015, Berhanel 2000 and Harmsen 2015 are included studies, but CLEF's screening labels mark their records not relevant at both levels. CLEF's search-task labels show why: they map each of these references to a different, wrong PMID, none of them in the pool. Each review citation has a quirk, and each wrong record shares the cited journal and year:

| Study | Correct PMID (in pool) | CLEF's PMID | What CLEF's record is |
|---|---|---|---|
| Barbieri 2015 (cited as volume "49.(18)") | 25830870 | 25741653 | Another 2015 *Revista de Saúde Pública* article, on healthy life expectancy |
| Berhanel 2000 | 11132351 | 11144875 | A 2000 *Ethiopian Medical Journal* article on ultrasound-guided aspiration |
| Harmsen 2015 (cited as page 1; it is article 1229) | 26654538 | 25563658 | A 2015 *BMC Public Health* article on alcohol and mortality |

The overview says included references were checked by hand when a title search did not match closely (Kanoulas et al., 2019); these three were not caught. A method that ranks the correct records highly is marked down for it on the screening labels.

**A mapping error of our own.** PubMed's citation matcher returned PMID 25563658 for Harmsen 2015, the same wrong record that CLEF's labels contain, because the review gives the page as 1. Checking every match against OpenAlex caught it. Automated mapping needs a verification step.

### Uses in the book

- **Chapter 3, search filters and headings.** The MEDLINE strategy combines a large subject-heading block with Ovid's built-in "qualitative (maximizes sensitivity)" filter and a language limit.
- **Chapter 8, coverage.** Four of 38 included studies are not in PubMed at all.
- **Chapter 10, validation.** Against the review's included studies, the CLEF screening labels recover 28 of 38 (74%): 4 lost to coverage, 3 to the entry-date limit and 3 to wrong mappings. A score computed on the screening labels cannot see any of these.
- **Chapter 11, updating.** A second instance of the entry-date mechanism.

## References

Ames, H. M., Glenton, C., & Lewin, S. (2017). Parents' and informal caregivers' views and experiences of communication about routine childhood vaccination: A synthesis of qualitative evidence. *Cochrane Database of Systematic Reviews*, (2), CD011787. https://doi.org/10.1002/14651858.CD011787.pub2

Ijaz, S., Davies, P., Williams, C. J., Kessler, D., Lewis, G., & Wiles, N. (2018). Psychological therapies for treatment-resistant depression in adults. *Cochrane Database of Systematic Reviews*, (5), CD010558. https://doi.org/10.1002/14651858.CD010558.pub2

Kanoulas, E., Li, D., Azzopardi, L., & Spijker, R. (2019). CLEF 2019 technology assisted reviews in empirical medicine overview. In *CLEF 2019 Working Notes* (CEUR Workshop Proceedings, Vol. 2380, paper 250). https://ceur-ws.org/Vol-2380/paper_250.pdf

Wolters Kluwer. (n.d.). *Ovid MEDLINE database guide: Entry Date (ED)*. Retrieved 21 October 2026, from https://ospguides.ovid.com/OSPguides/medline.htm
