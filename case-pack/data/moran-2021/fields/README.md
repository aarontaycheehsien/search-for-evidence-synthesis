# The Moran strategy on title and abstract only

Input for Chapter 7. Built on 2026-10-22 by `case-pack/scripts/field_checks.py`.

## The question

The Moran et al. (2021) strategy was run as `TS=` in Web of Science and `TITLE-ABS-KEY` in Scopus. Both search more than the title and abstract: Web of Science's Topic field adds author keywords and Keywords Plus, words taken from the titles of the works a record cites; Scopus adds author keywords and index terms (`claims/register.csv`: `wos-ts-fields`, `wos-keywords-plus`, `scopus-title-abs-key`). A translation of the strategy to a title-and-abstract field, such as Ovid's `.ti,ab.` or PubMed's `[tiab]`, keeps the words and drops those fields. How many of the review's included studies would it lose?

## Method

The script applies the strategy's three blocks (condition, risk and behaviour; see `case-pack/cases/moran-translation.md`) to each record's title and abstract, with wildcards, phrases and proximity emulated as described in the script. It checks three versions of the text:

- the pool's text, from SYNERGY and OpenAlex (all 4,882 records);
- the title and abstract in the authors' initial Web of Science export, where the record is in it;
- the title and abstract in the authors' initial Scopus export, where the record is in it.

A record that fails on every database's own text could only have been admitted through a field beyond title and abstract. The exports contain no keyword fields, so the script cannot say which keyword field admitted it.

`ti-ab-only.csv` holds identifiers and flags only: the three blocks on pool text, whether each record is in each export, and whether it matches on each text.

## Results

| Text checked | Included at full text | Passed title and abstract | Whole pool |
|---|---|---|---|
| Pool text (SYNERGY and OpenAlex) | 53 of 137 (39%) | 289 of 586 (49%) | 3,053 of 4,882 (63%) |
| Web of Science export text | 32 of 111 (29%) | 89 of 344 (26%) | 975 of 2,527 (39%) |
| Scopus export text | 36 of 115 (31%) | 232 of 513 (45%) | 2,310 of 4,056 (57%) |
| Either database's own text | 53 of 137 (39%) | 290 of 586 (49%) | 3,049 of 4,882 (62%) |

Of the 53 included records that fail on pool text, 36 fail the behaviour block, 15 the risk block and 7 the condition block; some fail more than one.

**Robustness.** Widening the proximity windows by up to ten word positions changes the count of included records that fail from 53 to between 51 and 56. The result does not depend on the proximity emulation.

## Limits

- Scopus's lemmatisation and loose-phrase matching are emulated only as far as the strategy's wildcards reach, so a few records may match in Scopus on title and abstract that fail here.
- Records added by the 2019 update searches are not in the initial exports; all 137 included records were found in at least one export.
- The figures describe this strategy in these two databases. A strategy written for title and abstract from the start would use more synonyms and would not lose as much.
