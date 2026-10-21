# Search for Evidence Synthesis

An independent textbook on how search systems find and miss studies, written for evidence-synthesis librarians and information specialists.

Working title: *How Search Finds and Misses Studies: Information Retrieval for Evidence Synthesis*.

**Status:** early draft. Chapters 1 and 10 have first drafts; chapters marked "Not yet drafted" are outlines. Start with the [plan](docs/plan.md), the [chapter map](docs/chapter-map.md) and the [case pack](docs/case-pack.md).

## Who it is for

Librarians and information specialists who can already build structured Boolean searches and who support or conduct systematic, scoping, rapid or other evidence syntheses. The book does not teach how to conduct a review or basic database searching.

## What it promises

Readers should be able to:

- explain how retrieval decisions change the evidence available to a review;
- diagnose where an eligible study was lost; and
- evaluate a proposed search tool or workflow against the claim actually being made for it.

## Relationship to *How Search Decides What You See*

This book is independent of [*How Search Decides What You See*](https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/) ([repository](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse)), which remains a general retrieval book for librarians. Some explanations are adapted from it under its CC BY 4.0 licence. Adapted material is rewritten around evidence-synthesis examples rather than copied, and each adaptation is recorded in the [chapter map](docs/chapter-map.md) with its source section and commit.

Third-party figures and product screenshots in the earlier book are not carried over.

## Repository map

| Location | Purpose |
|---|---|
| `_quarto.yml`, `index.qmd`, `chapters/`, `appendices/`, `references.qmd` | The Quarto book: configuration, preface, chapters and appendices |
| `references.bib`, `assets/apa.csl` | Verified bibliography and the APA citation style (CC BY-SA 3.0, from the Citation Style Language project) |
| `.github/workflows/publish.yml` | Renders the book and publishes it to GitHub Pages on each push to `main` |
| `docs/plan.md` | Scope, structure, principles, open decisions and implementation sequence |
| `docs/chapter-map.md` | For each planned chapter: source sections, treatment, new material and product claims to verify |
| `docs/case-pack.md` | Datasets for the exercises: what each can show, licences checked, and the chosen cases |
| `case-pack/sources.csv` | Machine-readable provenance and licence record for every case-pack source |
| `case-pack/reference-sets/`, `case-pack/data/`, `case-pack/synthetic/` | Exercise data: identifiers, labels, screening logs and the synthetic collection, each with a README |
| `case-pack/scripts/`, `case-pack/tests/` | Scripts that rebuild the data, and their offline tests |
| `case-pack/cases/` | Worked teaching cases built on the data, such as the Moran translation case |
| `claims/register.csv` | Dated register of product claims and the documentation each rests on |
| `docs/outreach/` | Drafts of messages to other projects, not sent |
| `AGENTS.md` | Working rules for contributors and coding agents |
| `LICENSE` | CC BY 4.0, with the exclusions listed there |

## Building the book

Install [Quarto](https://quarto.org/) 1.10 or later, then run `quarto render` in the repository root. The site is written to `_site/`, which Git ignores. Chapters contain no executable code; figures and counts come from the committed case-pack data.

## Licence

Text, tables, diagrams and code are licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). See [`LICENSE`](LICENSE) for what the licence does not cover, including the citation style file.
