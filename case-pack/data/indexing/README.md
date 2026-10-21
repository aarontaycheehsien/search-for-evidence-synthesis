# Which strategy lines admit each included record

Built on 2026-10-22 by `case-pack/scripts/indexing_checks.py`. For every included-study record of CD010558 and CD011787 that has a PubMed record, the script applies lines of the review's Ovid MEDLINE strategy (as distributed by CLEF 2019) to the record's title, abstract, MeSH headings, publication types and language as PubMed holds them today. Each file has one row per record, with 1 or 0 for each group of lines. No title or abstract text is stored here.

The PubMed records were fetched on 2026-10-22 through the PubMed connector into `case-pack/cache/pubmed/records.json`, which Git ignores. NCBI's E-utilities were not reachable from the build environment, so the fields were transcribed from the connector's output; `case-pack/scripts/fetch_pubmed.py` can rebuild the cache directly where NCBI is reachable.

## The emulation is an approximation

It is not Ovid. The script's docstring lists every simplification. The main ones:

- Text is split into words at every character that is not a letter or digit; `adjN` is read as "within N words, either order, same field".
- Author keywords (`kf`) and most other Ovid fields are unavailable and treated as empty.
- `exp` headings are matched without their narrower headings.
- Headings and publication types are today's, which may differ from when CLEF ran the strategy in 2019.
- Ovid's "qualitative (maximizes sensitivity)" limit is `interview:.tw. or px.fs. or exp health services administration/` (OvidGO, reviewed 2024-11-25). Only its text part can be emulated, because the cached records have no subheadings and no MeSH tree.
- Entry-date limits are not emulated.

**Check against the CLEF pools.** Every included record that is in the CLEF pool passes every emulated line, as it must, and every included record missing from the pool is explained: the four CD010558 reports and three CD011787 reports outside the date limit pass every emulated line, and the two CD010558 letters fail the trial-design block and match the `NOT` block.

## CD010558 (`CD010558-lines.csv`, 16 records)

| Lines | Admit | Of the 10 in the pool |
|---|---|---|
| Line 1, the heading Depressive Disorder, Treatment-Resistant | 11 | 6 |
| Lines 2 to 6, text words for the condition | 16 | 10 |
| Line 8 or 9, trial publication types (or the Randomized Controlled Trials as Topic heading) | 13 | 10 |
| Lines 10 to 14, text words for trial design | 14 | 10 |
| Every line before the date limit | 14 | 10 |

The heading was introduced in 2012, with previous indexing under Depressive Disorder from 1981 to 2011 (MeSH Browser record D061218). Of the five records without it, two date from 2008 and 2009, two from 2013 and 2014 carry other depression headings, and one, a journal-club commentary, has no MeSH headings at all.

## CD011787 (`CD011787-lines.csv`, 34 records)

| Lines | Admit | Of the 31 in the pool |
|---|---|---|
| Line 70: vaccination, population and communication headings combined | 26 | 23 |
| Line 84: text words for vaccination and communication, with the population block | 34 | 31 |
| Text part of Ovid's qualitative limit (`interview:` in title or abstract) | 25 | 22 |
| The review's own qualitative block (line 87) | 31 | 29 |
| Either of the two rows above | 34 | 31 |

The review's own qualitative block finds 17 records through its headings (Qualitative Research or Interviews as Topic) and 31 through its text words. Three included records match neither: Brunson 2015 and Hussain 2012, both in the pool, and Sobo 2016, outside the date limit. All three are admitted by `interview:` in Ovid's limit. Sobo 2016 matches `interview:` but not `interview?`, the form shown on McMaster's hedges page, so the difference between the two published versions of the filter changes the result for one included study.

## Reference

The strategies are from the CLEF TAR 2019 topic files (`CLEF-TAR/tar` at commit `dbc13d0`, MIT licence). Kanoulas, E., Li, D., Azzopardi, L., & Spijker, R. (2019). CLEF 2019 technology assisted reviews in empirical medicine overview. In *CLEF 2019 Working Notes* (CEUR Workshop Proceedings, Vol. 2380, paper 250). https://ceur-ws.org/Vol-2380/paper_250.pdf
