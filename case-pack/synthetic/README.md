# Synthetic teaching collection (version 0.1)

**Everything here is invented for teaching.** No study, author, journal or DOI refers to real work. DOIs use the unassigned prefix `10.0000`, and every journal name contains "Synthetic" or is plainly fictional. Licensed CC BY 4.0.

The collection supports controlled exercises in which every eligible study is known, so readers can see exactly what a search, a deduplication rule or a screening decision lost. It is a non-health topic on purpose.

## The fictional review

**Question:** Does structured peer tutoring improve reading comprehension in primary-school pupils?

**Eligibility criteria:**

- **Population:** pupils aged about 5 to 11 in mainstream primary or elementary schools.
- **Intervention:** structured tutoring in which the tutors are pupils, same-age or cross-age.
- **Comparison:** a group that does not receive the tutoring, allocated randomly or otherwise.
- **Outcome:** reading comprehension, measured by a test.
- **Design:** randomised or non-randomised controlled studies. Single-group, qualitative, review and opinion publications are excluded.

## Files

| File | Contents |
|---|---|
| `records.json` | 33 records. Each has bibliographic fields, assigned headings from a fictional thesaurus, the sources it appears in, its study, whether that study is eligible, its role (primary report, duplicate record, additional report, protocol and so on) and a `planted` note saying what it tests |
| `studies.csv` | 29 studies (9 eligible), their reports, the reason for ineligibility, and which studies each one cites (for citation searching) |
| `answer_key.py` | Runs six illustrative strategies and four deduplication rules over the records |
| `answer-key.md` | Its output; regenerate it after any change to the records |

## What is planted

| Feature | Records | Chapter |
|---|---|---|
| Same study, several reports (journal article, conference abstract, protocol, dissertation) | R001, R003; R005, R006; R011, R012 | 1, 11 |
| True duplicate from a second database, with no DOI and different formatting | R002 | 11 |
| Different study with a near-identical title and a shared author | R013 | 11 |
| Eligible study described without the obvious terms (cross-age, pupil-led, coached one another, reading for meaning) | R004, R009 | 2, 5, 7 |
| Hyphenation and acronym variants (PALS, peer assisted) | R006 | 2 |
| No abstract | R007 | 2, 3 |
| Indexing error: wrong heading assigned | R008 | 3 |
| Eligible study removed by a `NOT` line | R010 | 2, 7 |
| Non-English record with a translated title, only in one database | R012 | 2, 8 |
| Studies only in a trial register or theses index | R005, R011 | 8 |
| Topically relevant but ineligible on population, intervention, outcome, design, setting or publication type | R014 to R023 | 1 |
| Off-topic records that match the search terms (peer review, tutorial, meter reading, machine reading comprehension) | R024 to R033 | 2, 5 |
| A review whose references are the hardest-to-find eligible studies | R018 cites S02, S04, S06 | 8 |

## Results at a glance

From `answer-key.md`: a narrow free-text search of one database finds 4 of the 9 eligible studies; headings alone miss the mis-indexed study; adding `NOT "secondary school*"` removes an eligible study; and deduplicating by title similarity at 0.90 merges two different studies, losing one. A threshold of 0.95 merges the true duplicate without that loss in this collection; that is a property of these records, not a general recommendation.

## Limits

The strategies in `answer_key.py` are a simplified model of Boolean searching: they search title and abstract text and assigned headings, with truncation and phrases, but no database's actual syntax, stemming or field rules. Use them to reason about mechanisms, not to predict how a particular platform behaves.
