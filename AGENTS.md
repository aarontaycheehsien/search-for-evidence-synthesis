# Repository working rules

## Commit every completed change

When you modify repository files, finish the task by committing your changes.

- Treat a request to edit files as authorisation to create a local Git commit.
- Commit each coherent change after completing relevant checks.
- Before committing, review the diff and stage only files belonging to your task.
- Preserve unrelated changes made by the user or another agent. Never include
  them in your commit without explicit authorisation.
- Use a concise commit message describing the change.
- Do not amend existing commits, rewrite history, merge branches, or push
  remotely unless explicitly requested.
- If checks fail, fix the problem before committing. If you cannot finish,
  preserve the work and explain why it remains uncommitted.
- In the final response, report the commit hash, relevant verification results,
  and any changes left uncommitted.
- Read-only reviews and tasks that produce no file changes need no commit.

An explicit user instruction such as "do not commit" overrides this default.

## Parallel development

- Work in the development worktree assigned to the current task.
- Confirm the working directory and branch before editing.
- Do not switch branches or change another worktree as part of ordinary edits.
- Commit locally on the current development branch; merging back is a separate
  action requiring an explicit request.

## Writing the book

- Use UK spelling, except in quoted titles and product names.
- Verify every citation against a bibliographic record (DOI, PubMed or
  OpenAlex) before adding it. Never cite from memory.
- Date every product claim and record the documentation it rests on. Product
  behaviour changes; mechanisms explained in the text should not depend on an
  undated claim.
- When adapting text from *How Search Decides What You See*, rewrite it around
  evidence-synthesis examples and record the source section and commit in
  `docs/chapter-map.md`.
- Do not carry over third-party figures or product screenshots from the earlier
  book without a fresh rights assessment.
- Label synthetic examples and data as synthetic. State the provenance and
  licence of any real records, labels or datasets.
- Every exercise needs supplied inputs and worked answers, not only
  instructions to obtain them.
