# Pilot: facilitator guide

For whoever runs the pilot. This file is in a public repository, so participants could read the answers below; ask them not to, and send the knowledge check and capstone task as separate documents.

## Knowledge check

Send the same eight items before reading (part A) and after the last chapter (part B). Ask for short answers, a sentence or two each, without looking anything up. Score each item 0, 0.5 or 1 against the answer given here. Items 1 to 3 test Chapter 1, items 4 to 6 Chapter 3, and items 7 and 8 Chapter 10.

**1.** A benchmark built from a Cochrane review's re-run MEDLINE strategy labels ten records as included, and a screening tool finds all ten. The review itself included six studies, of which the re-run results contain reports of four. What is the strategy's recall at study level, and why does it differ from the tool's 100%?

> *Answer:* 4 of 6, or 67%. The benchmark's labels were built from the strategy's own results, so they cannot count studies the strategy missed. The tool's 100% is recall within the pool, a different stage and a different denominator. *Half credit* for the figure without the reason, or the reason without the figure.

**2.** A strategy ends with a limit on Ovid's entry-date field. Re-run two years later, it no longer retrieves a trial report published within the date range. Name the most likely cause.

> *Answer:* In Ovid MEDLINE the `ed` field holds the date indexing was completed, not the publication date; the report's indexing was completed after the limit's end date, so the limit excludes it. *Half credit* for "a date limit" without the indexing date.

**3.** The pool contains a trial's protocol but not its results paper. Has the search found the study?

> *Answer:* It has found a report of the study, so the study can be identified, but its results have not been found; someone must follow the protocol up. *Half credit* for yes or no with a partial reason.

**4.** A strategy relies on a subject heading introduced in 2012. The review's studies were published from 2005 to 2020. What will a heading-only line miss, and what would you add?

> *Answer:* Records indexed before the heading existed, which are not normally re-indexed, and later records whose indexer chose a different heading. Add the heading's previous indexing for earlier years and text words for the concept. *Half credit* for one of the two parts.

**5.** How is a MeSH heading on a MEDLINE record added in 2026 assigned, and from what?

> *Answer:* Automatically, by NLM's MTIX algorithm (a neural network), from the title, abstract, publication year, indexing year and journal, not from the full text; selected sets are reviewed by people. *Half credit* for "automatically" without the inputs, or the reverse.

**6.** A qualitative search filter is reported to have 95% sensitivity. Against what was that measured, and what would you check before relying on it in a review?

> *Answer:* Against the reference set its developers used, for example hand-searched clinical journals from one year. Check the filter's purpose and date, how its reference set was built, its exact syntax on the platform being searched, and how it performs on the review's own known studies. *Half credit* for either half.

**7.** A vendor says its semantic search "retrieves 95% of the included studies from 50 Cochrane reviews, so Boolean searching is no longer necessary." Which kind of claim is this, and name two things the evidence cannot show.

> *Answer:* A claim that one route can replace another. The evidence cannot show studies that the reviews' own searches missed (the reference set was built mostly by Boolean searching); it does not show what the 5% missed were or why; published reviews may be in the tool's training data; and one set of topics does not establish general substitution. *Half credit* for the claim type, or two limits without the claim type.

**8.** In one simulation, stopping after 50 consecutive irrelevant records found every included study. What evidence would you need before adopting that rule?

> *Answer:* The number of eligible studies missed at the stopping point across many runs (different starting records or seeds) and several reviews, with the range reported, because a stopping rule's result varies more than ranking efficiency and depends on how common eligible records are. *Half credit* for "more runs" without the reason, or the reason without the evidence.

**Reporting.** For each participant, record the part A and part B scores per item. Do not report averages as if they measured learning: with five to eight participants, the useful information is which items stay wrong after reading.

## Capstone task

Send this after Chapter 10. Ask for no more than 300 words.

> Your library supports a rapid review of interventions to reduce loneliness in older adults. A colleague proposes adopting an AI research assistant whose vendor reports that it "finds 96% of the studies included in 40 published Cochrane reviews". The colleague suggests using it instead of searching Embase, to save time. Write a recommendation to the review team.

**Criteria (two points each, ten in all):**

1. **Names the claim.** The proposal is to replace a database, so the evidence must address replacement, not supplementation.
2. **Bounds the reference set.** The 40 reviews' included studies were found mostly by conventional searching, which may include Embase, so 96% shows how much of what those searches found the tool also finds, not what both miss; 4% of known studies missed is itself a loss if Embase would have found them.
3. **Names at least two further gaps**, such as: topic transfer from Cochrane reviews to a social-care rapid review; possible training-data contamination; the tool's coverage and record fields; run-to-run variation; the product version and date of the evaluation.
4. **Makes a clear recommendation consistent with the evidence.** For example: do not replace Embase on this evidence; consider the tool as a supplementary route.
5. **Proposes a test.** For example: run it alongside the usual searches on this or recent reviews, count eligible studies it adds and misses, record time, repeat runs, and report use as the joint position statement asks.

A recommendation that declines the tool with good reasons scores as highly as one that adopts it with good reasons.

## Debrief

Sixty minutes, individually or in a group of up to four. Record notes against participant codes (P1, P2 and so on), not names.

1. Where did you stop or slow down, and why?
2. Which terms or ideas were new to you? Which did the book assume you knew that you did not?
3. Take one exercise you got wrong or only partly right. What led you to your answer?
4. In Chapter 3, how much detail about how indexing and filters work did you want: more, less or the same? Which parts would you cut first?
5. Which tables helped, and which did you skip?
6. Was the running case (the treatment-resistant depression review) easy to follow across chapters? Was the behavioural-ecology contrast case useful, or a distraction?
7. What will you do differently at work after reading these chapters?
8. What would make you recommend the book to a colleague, and what would stop you?

## Logging findings

After each feedback form, knowledge check and debrief, add one row per distinct finding to [`findings.md`](findings.md): which participant, which chapter and section, what kind of finding, a short description, severity, the decision and its status. Merge duplicates into one row and note how many participants raised it, since the protocol's decision rules depend on that count.
