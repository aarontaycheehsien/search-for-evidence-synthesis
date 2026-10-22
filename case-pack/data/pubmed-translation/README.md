# How PubMed translated some queries, observed

Input for Chapter 7. Each query was run in PubMed through the PubMed connector on 2026-10-22, which returns PubMed's own query translation (the "Details" PubMed shows) and the result count. `observed.csv` records the query, the translation and the count.

These are observations of one system on one day. Counts grow daily, and PubMed's mapping tables change with each year's MeSH, so rerun a query before relying on it. The behaviour they illustrate is documented in the PubMed User Guide (`claims/register.csv`).

What the rows show:

- Untagged words are rewritten by automatic term mapping into a heading, exploded, plus word variants; one variant added here is the German spelling "psychotherapie".
- A heading given in a non-standard form (`treatment-resistant depression[mh]`) was mapped silently to the official heading. A heading that does not exist, or uses British spelling (`"Cognitive Behavioural Therapy"[mh]`), returned no records and no warning.
- Truncating a word turns automatic term mapping off: `psychotherap* AND depress*` searched All Fields only and returned 37,587 records, against 53,914 for the untagged words.
- A plausible heading name that is not the heading, in quotes (`"Treatment Resistant Depression"[Mesh]`), returned no records. When such terms are ORed with a real heading, PubMed drops them from the translation without a message: the line still returns records, so nothing looks wrong.

## A drafted strategy, checked line by line

`draft-check.csv` is a PubMed strategy for CD010558's question, written for Chapter 7's exercise in the style of the errors reported for language-model drafts (headings that do not exist, British spellings of headings). It is not the output of a model. Each line was run on 2026-10-22, and the combined strategy was run against the 16 included CD010558 reports that have a PubMed record (`case-pack/reference-sets/CD010558.csv`), in batches of seven PMIDs because the connector allows at most 20 Boolean operators per query.

- Line 1 matches nothing. Line 3's two non-existent headings match nothing either, but its third heading, *Psychotherapy*, is exploded and so covers *Cognitive Behavioral Therapy*.
- The combined strategy returns 186 records; with line 1 replaced by the real heading, *Depressive Disorder, Treatment-Resistant*, it returns 209. Both admit the same 12 of the 16 included reports.
- The four not admitted are two that fail the condition block (Feldman 2009, PMID 19232571, and the Nakagawa 2014 protocol, 25335963, neither of which uses the block's phrases or carries the heading) and the two that fail the trial-design block (the CoBalT letter, 23588772, and the ACP Journal Club commentary, 23706799).
