# Reference sets

A reference set lists every report of every study a review included, taken from the review's own published reference list and matched to identifiers by a recorded method. It exists because the CLEF TAR labels cover only records that the review's MEDLINE strategy returned when the organisers re-ran it, so they cannot show what that strategy missed (Kanoulas et al., 2019).

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

The two studies with no report in the pool:

- **Wiles 2007** (the CoBalT pilot trial). Its only publication has no PubMed record, so no MEDLINE strategy could have found it. This is a coverage boundary.
- **Town 2017** (the Halifax ISTDP trial). Its report is in PubMed and appears to satisfy the strategy, but it is not in the pool.

Of the reports missing from the pool:

- **Two carry the Letter or Comment publication types** (PMIDs 23706799 and 23588772). The strategy's exclusion lines (`letter/`, `comment/`) are designed to remove such records. Here the exclusion cost two reports but no study, because other reports of CoBalT were retrieved.
- **Two are 2017 trial reports** (Nakagawa 2017 and Town 2017). The strategy ends with `limit 32 to ed = "19480101-20170516"`. In Ovid MEDLINE, `ed` holds NLM's Date Completed, the date indexing finished, not the date the record first appeared (Wolters Kluwer, n.d.). When CLEF re-ran the strategy in 2019, any record indexed after 16 May 2017 would fall outside the limit even if it was published before. **This is the leading explanation but has not been confirmed**: it needs the Date Completed values for PMIDs 28252882 and 28266318, which this environment could not fetch.
- **Two 2016 reports are absent for no reason identified** (PMIDs 26777773 and 27100125). Both carry the subject heading `Depressive Disorder, Treatment-Resistant`, and their records appear to satisfy the strategy. Possible causes include the content of the Ovid demonstration interface CLEF used, but that is untested.

### Uses in the book

- **Chapter 1, record, report and study.** Ten eligible records in the pool are reports of four studies; six of them are CoBalT. The Nakagawa study is represented only by its protocol.
- **Chapter 10, validation.** Measured against the review's included studies, the re-run MEDLINE strategy recovers 4 of 6 studies and 10 of 16 PubMed-indexed publications. A benchmark that counts only the pool would report complete recall.
- **Chapter 11, updating.** The entry-date case shows why a date limit's field matters when a strategy is re-run.
- **Chapter 2, exclusions.** The `NOT` block's effect on letters and comments that a review later cites.

### To confirm before publication

1. Date Completed for PMIDs 28252882 and 28266318.
2. Whether PMIDs 26777773 and 27100125 are retrieved when the strategy is run in Ovid MEDLINE today without the date limit.
3. The mapping of the ACP Journal Club entry (PMID 23588772), where the review's authors differ from PubMed's.

## References

Ijaz, S., Davies, P., Williams, C. J., Kessler, D., Lewis, G., & Wiles, N. (2018). Psychological therapies for treatment-resistant depression in adults. *Cochrane Database of Systematic Reviews*, (5), CD010558. https://doi.org/10.1002/14651858.CD010558.pub2

Kanoulas, E., Li, D., Azzopardi, L., & Spijker, R. (2019). CLEF 2019 technology assisted reviews in empirical medicine overview. In *CLEF 2019 Working Notes* (CEUR Workshop Proceedings, Vol. 2380, paper 250). https://ceur-ws.org/Vol-2380/paper_250.pdf

Wolters Kluwer. (n.d.). *Ovid MEDLINE database guide: Entry Date (ED)*. Retrieved 21 October 2026, from https://ospguides.ovid.com/OSPguides/medline.htm
