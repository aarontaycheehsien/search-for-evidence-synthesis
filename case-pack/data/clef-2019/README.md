# CLEF TAR 2019 data

From the CLEF TAR repository (`CLEF-TAR/tar` at commit `dbc13d0`, MIT licence).

| Location | Contents |
|---|---|
| `CD010558/` | Screening logs from three participant runs on the health running case; see its README |
| `label-scope.csv` | For each of the 31 test topics, the pool size and the number of relevant labels in the search-task (Task 1) and screening-task (Task 2) qrels, at abstract and content level, with how many Task 1 labels fall outside the pool |

## Two label sets

CLEF 2019 distributes two sets of qrels for each test topic.

- **Screening task (Task 2).** Every record in the topic's pool is judged: the PubMed records the review's Ovid MEDLINE strategy returned when the organisers re-ran it. Nothing outside the pool is labelled.
- **Search task (Task 1).** Only relevant records are listed: the review's included and excluded references (abstract level) and included references (content level) that CLEF mapped to PMIDs.

The overview says that cited studies absent from the Boolean query's results were left out of the label set for both tasks, unlike 2018 (Kanoulas et al., 2019, section 2.3). The distributed Task 1 qrels do not match that description. In 24 of the 31 topics at least one content-level Task 1 label is outside the pool; across all topics, 458 of 1,340 are. Nearly half of those (223) come from one prognosis topic, CD012661. The overview's per-topic tables report the Task 1 counts alongside the pool size, so for CD010558 they give 75 and 16 relevant records where the screening labels have 37 and 10.

Every Task 2 relevant label is also a Task 1 label (`*_task2_not_in_task1` is 0 throughout).

Task 1 labels depend on CLEF's mapping of references to PMIDs. For CD010558 all 16 match the reference set built for this book. For CD011787, 31 of 34 match and three are wrong records; see `case-pack/reference-sets/README.md`. Treat other topics' labels with the same caution.

Rebuild with:

```
python case-pack/scripts/clef_label_scope.py --tar PATH_TO_CLEF_TAR_CHECKOUT
```

## Contamination risk

CLEF TAR's topics, the reviews' search strategies, the PubMed identifiers and the relevance labels were released publicly between 2017 and 2019, and the Cochrane reviews themselves are published. Language models may have been trained on any of this, so a model's performance on these topics is not evidence of how it would perform on a new question. Any exercise that tests an AI tool on these topics must say so (Chapter 10, "Development and validation sets").

## Reference

Kanoulas, E., Li, D., Azzopardi, L., & Spijker, R. (2019). CLEF 2019 technology assisted reviews in empirical medicine overview. In *CLEF 2019 Working Notes* (CEUR Workshop Proceedings, Vol. 2380, paper 250). https://ceur-ws.org/Vol-2380/paper_250.pdf
