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

## Term mining on the translation

`term-mining.md`, built by `case-pack/scripts/term_mining.py`, asks whether the words the title-and-abstract translation misses can be found by mining, in the way of the objective approach (Hausner et al., 2012), and whether the additions hold on records not used to choose them.

- The 137 included records were split at random (seed 7) into 69 for development and 68 for validation.
- For each block, the development records that fail it were mined for words in at least 20% of them and at most 5% of the pool, and checked for the block's head word elsewhere in the text.
- Three additions were chosen from the development lists only: `behavio*` on its own in the behaviour block (12 of the 17 development failures on that block contain it, but not within five words of the block's other terms), `activ*` in the behaviour block, and `conspecific*` and `competit*` in the risk block.

| Strategy | Development (of 69) | Validation (of 68) | Pool records retrieved |
|---|---|---|---|
| Original, title and abstract | 43 (62%) | 41 (60%) | 1,829 |
| All three additions | 57 (83%) | 58 (85%) | 2,598 |

`term-mining.md` gives each addition separately.

**A note on method.** A first, exploratory look mined the failures among all 137 included records, and suggested `forag*` for the risk block. That word is not in the development-only list and is not used: an addition chosen with sight of the validation records would make the validation meaningless.

**Limits.**
- The pool is what the original search retrieved, not the database. The 769 extra pool records are a floor for the cost: in a database, `behavio*` on its own would add far more.
- Ten of the 68 validation records still fail. Mining repairs part of the loss from dropping keyword fields, not all of it.
- The additions are one searcher's judgement from the development lists; another might choose differently.
