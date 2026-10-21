# Updating: dates on the late-indexed reports

Inputs for Chapter 11. Checked on 2026-10-21.

## What this is

`late-indexed.csv` lists the seven included reports that the CLEF re-runs of CD010558 and CD011787 did not return because their MEDLINE indexing was completed after each strategy's entry-date limit (see `case-pack/reference-sets/README.md`). For each, it gives three PubMed dates as windows:

| Column | PubMed field | Meaning, per the PubMed User Guide |
|---|---|---|
| `created_crdt` | `[crdt]` Create Date | When the PubMed record was first created |
| `entered_edat` | `[edat]` Entry Date | When the citation was added to PubMed |
| `completed_dcom` | `[dcom]` Completion Date | When NLM completed the record's MEDLINE indexing |

Ovid MEDLINE's `ed` field holds the completion date (see `claims/register.csv`), so the two reviews' limits (`ed` up to 2017-05-16 for CD010558; `ED` up to 2016-08-30 for CD011787) are limits on `completed_dcom`.

## How the dates were found

PubMed does not display these dates on the abstract page, and the metadata service used for the case pack does not return them. Each window was found by searching PubMed for the PMID combined with a date range in the field, through the PubMed connector, narrowing the range until the record was in one window and not in its neighbours. For example, `27100125[pmid] AND 2017/07/01:2017/09/30[dcom]` returns the record, while the same search for July and for August does not, so its completion date is in September 2017. Windows are as narrow as the searches made them, from a fortnight to a year.

Dates in PubMed can change when records are revised, so these reflect PubMed on the check date, not the database when CLEF re-ran the strategies in 2019.

## What the dates show

Every one of the seven was created in, and entered, PubMed before its review's limit ended; every one had its indexing completed afterwards. Six of the seven also entered PubMed before the limit ended. The exception, Sobo 2016, was created in early 2016 but has an entry date between September and December 2016, after the CD011787 limit; the entry date and the create date are different fields and need not agree.

Which of the seven an update search would catch depends on the field it uses to define "new since last time":

| Update window, starting the day after the original limit | CD010558 (4 reports) | CD011787 (3 reports) |
|---|---|---|
| Ovid `ed` (completion date), or PubMed `[dcom]` | 4 | 3 |
| PubMed `[edat]` | 0 | 1 (Sobo 2016) |
| PubMed `[crdt]` | 0 | 0 |
| Publication year from the year after the limit (2018 or 2017) | 0 | 0 |
| Publication year from the limit's own year (2017 or 2016) | 2 (the 2017 reports) | 3 |

The original limit and the update window must be defined on the same field, or the records whose dates differ between the fields fall between the two searches.
