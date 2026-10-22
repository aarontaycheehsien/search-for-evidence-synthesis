# Citation searching: would it have found what the MEDLINE searches missed?

Inputs for Chapter 8. Checked in OpenAlex on 2026-10-22, through the OpenAlex connector (the OpenAlex API is not reachable from the build environment, so these results were not produced by a script). OpenAlex data are CC0.

## The question

For CD010558 and CD011787, the CLEF re-runs of the reviews' MEDLINE strategies returned only some of each review's included reports (`case-pack/reference-sets/README.md`). Suppose the review team had then done one round of backward and forward citation searching in OpenAlex, starting from the included reports the MEDLINE search did return. Which of the missing reports would it have reached, and how many records would it have produced to screen?

- **Seeds** (`seeds.csv`): the included reports in each review's CLEF pool, 10 for CD010558 and 31 for CD011787.
- **Targets** (`targets.csv`): the included reports outside the pool that are journal publications: 7 for CD010558 (registry records excluded) and 7 for CD011787.

## Method

A target is reached by **forward** citation searching if it cites a seed, and by **backward** citation searching if a seed cites it. For each target, OpenAlex was asked for the target's references and the works citing it, each restricted to the seeds, for example:

```
get works where it's cited by (W2592399410) and openalex id is (W2093437418 or ... or W2140815719)
```

The `reproduce_url` of each query reruns it against the live API. Candidate-set sizes are the number of unique works that cite a seed or are cited by a seed, published before the day after the original strategy's limit (17 May 2017 for CD010558; 31 August 2016 for CD011787), so they approximate what one round would have produced at the time.

## Results

| | CD010558 | CD011787 |
|---|---|---|
| Missing reports (targets) | 7 | 7 |
| Not in PubMed at all | 1 (the CoBalT pilot) | 4 |
| Reached by forward citation searching | 4 | 5 |
| Reached by backward citation searching | 1 | 0 |
| Not reached | 2 | 2 |
| Unique records produced by one round, at the time of the original search | 678 | 1,318 |

**CD010558.** One round reaches both studies that the pool lacked entirely: Town 2017, which cites the CoBalT Lancet paper and Souza 2016, and the CoBalT pilot (Wiles 2008, not in PubMed), which three CoBalT seeds cite. It also reaches Abel 2016, Wiles 2016 and the CoBalT authors' reply. It does not reach:

- the Nakagawa 2017 results paper, because OpenAlex holds no reference list for it, so no forward link to any seed, including the study's own protocol, can be followed;
- the ACP Journal Club commentary, whose only OpenAlex reference is a different trial: the CoBalT paper it comments on appears only as text in its abstract field.

**CD011787.** One round reaches the three late-indexed reports and two of the four studies not in PubMed (Figueiredo 2011 and Guillaume 2004), all by forward citation searching. It does not reach Tadesse 2009, whose seven OpenAlex references include no seed and which no seed cites, or Tomlinson 2013, which is not in OpenAlex.

## Limits

- **One index, one date.** Citation links in OpenAlex change as references are added and records are merged or split. Another index (Web of Science, Scopus, Google Scholar, Lens) would give different links, and might, for example, hold Nakagawa 2017's references.
- **Candidate counts are upper bounds on new screening.** Many of the records would duplicate the database results and be removed before screening. The counts also include records that OpenAlex has mismatched: among the CD010558 seeds' references is a record credited with 169,710 citations, which is not what the seeds cited.
- **Seeds chosen with hindsight.** The seeds are the included reports in the pool, which a review team would know only after screening. Starting earlier, from fewer or different seeds, would reach a different set.
- **One round only.** A second round from newly found reports could reach more. For CD010558, none of the five newly reached reports cites Nakagawa 2017.
- **Reports, not studies.** Reaching a report does not mean the team would have recognised it as eligible.
