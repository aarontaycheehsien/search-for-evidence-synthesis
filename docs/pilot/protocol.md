# Pilot protocol

Version 2, 2026-10-30. For the author. Version 1 (2026-10-22) was written when only Chapters 1 to 4 and 10 were drafted; version 2 reflects the complete first draft and adds an invitation ([`invitation.md`](invitation.md)). The procedure and decision rules are unchanged except where noted.

## Aims

The pilot asks three questions.

1. **Where do readers fail?** Which explanations, tables and exercises do practising evidence-synthesis librarians misread, find too hard or get wrong, and why?
2. **Is the depth right?** Does Chapter 3 give the amount of retrieval mechanism readers want, too much or too little? The answer decides the depth of the rest of Part II, and in particular whether Chapters 5 and 6, drafted at a provisional depth, keep their depth, lose detail or gain optional boxes.
3. **Does the book deliver its promise?** After reading, can participants locate where an eligible study was lost, and judge a proposed tool against the claim made for it?

The pilot is formative. It is not an evaluation of the book's effectiveness and does not support claims of that kind.

## Participants

- **Number:** five to eight. Five is enough to find most recurring problems; more than eight adds little for a first pilot and multiplies the analysis.
- **Who:** librarians or information specialists who have built at least one search for a systematic or scoping review in the last two years.
- **Mix:** aim for at least one participant from outside health (social science, education, environment or similar), at least one who works mainly on rapid reviews, and at least one with no formal training in information retrieval. The book is health-led with a non-health contrast case, so the pilot should test whether non-health readers can follow it.
- **Recruitment:** personal invitation through professional networks. Do not recruit from a single institution.

## Materials

- The online draft: <https://aarontaycheehsien.github.io/search-for-evidence-synthesis/>, with Chapters 1, 3 and 10 as the pilot chapters.
- The case pack in the repository, which holds every input the exercises need.
- [`invitation.md`](invitation.md), a draft invitation to personalise and send.
- [`participant-guide.md`](participant-guide.md), sent with the invitation.
- The knowledge check and capstone task in [`facilitator-guide.md`](facilitator-guide.md), sent separately at the start and the end.

**Record the commit.** Note the `main` commit participants read (the site's footer date and the repository log), so findings can be matched to the text they refer to. If the text changes during the pilot, note which participants saw which version.

## Procedure

| Week | Participant does | Time asked |
|---|---|---|
| Before | Knowledge check (part A), without reading the chapters | 15 minutes |
| 1 | Chapter 1 and its core exercises (1.1, 1.2) | About 1.5 hours |
| 2 | Chapter 3 and its core exercises (3.1, 3.2) | About 1.5 hours |
| 3 | Chapter 10 and its core exercises (10.1, 10.3); the capstone task | About 2 hours |
| After | Knowledge check (part B); a 60-minute debrief, individually or in a small group | 1 hour 15 minutes |

The chapters total about 13,500 words; the time estimates allow for careful reading and for attempting each core exercise before opening its worked answer. The remaining exercises are optional.

Participants give feedback on each chapter through the **Pilot feedback** issue form, or privately by email to the author if they prefer not to post publicly. Errors go through the **Error report** form at any time.

## What is recorded

For each participant and chapter:

- time spent reading and on exercises (self-reported);
- for each core exercise: whether their attempt matched the worked answer, partly matched or did not, and what they got wrong;
- sections they found unclear, too long or unnecessary, and anything they think is missing;
- errors of fact, citation or arithmetic;
- the knowledge-check answers before and after, scored against the answers in the facilitator guide;
- the capstone recommendation, scored against the criteria in the facilitator guide;
- debrief notes.

Everything goes into [`findings.md`](findings.md) as one row per finding, with a decision.

## How decisions follow

These rules are set now, before the data, so that the pilot cannot be read to suit a preference.

- **A recurring failure is a revision.** If two or more participants fail the same core exercise, or misread the same passage in the same way, revise the section and its exercise before the first edition, and check whether the same problem recurs in other chapters.
- **A single failure is a check.** One participant's failure is logged and checked against the text; revise if the text is ambiguous or wrong, otherwise note it.
- **Every reported error is checked and answered.** Confirmed errors are fixed and the fix recorded; claims about products are re-checked against current documentation and dated in `claims/register.csv`.
- **Depth of Part II.** If most participants rate Chapter 3's mechanism coverage as about right, keep that depth for Chapters 5 and 6. If most rate it too much, cut mechanism detail in Chapters 2 and 4 to 6 to what an exercise needs. If most rate it too little, add optional boxes rather than lengthening the main text.
- **The promise.** If, after reading, fewer than half the participants can locate the boundary in knowledge-check items 1 to 3 or identify the claim type in items 7 and 8, revise Chapters 1 and 10 before anything else.

Record each decision in the plan's decision record, with the date.

## Consent and data

The pilot collects feedback on a draft text, not data about people. Even so:

- tell participants how their feedback will be used and that public issue comments are visible to anyone;
- offer the private email route;
- ask before naming anyone in the acknowledgements, and name no one in `findings.md` (use P1, P2 and so on);
- check whether a participant's institution requires approval for taking part in this kind of activity; most do not, but some do.

## Timeline

About five weeks from invitation to the end of the debriefs, then one to two weeks to analyse the findings and revise. Every chapter was drafted before the pilot (Chapters 5 and 6 at a provisional depth), so revisions follow the decision rules above across the whole book, starting with Chapters 1, 3 and 10 and the depth of Chapters 5 and 6.
