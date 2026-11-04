# Changelog

## [0.3.0] — 2026-11-04

- Reads `research_topic` (a noun phrase) in place of `activity_phrase`.
  New sentence patterns for personnel and non-personnel lines ending
  "... the research supported by this award on <topic>.", cost-fitting
  verbs, and a WRONG/CORRECT example of the dangling "supported by
  this award" ending seen in the first CSV run.

## [0.2.0] — 2026-11-04

- Output changed from a Markdown report to a JSON array of the OSP
  billing sheet's rows (the sheet's own column headers as keys, values
  copied unchanged, justification column filled), so Vandalizer's CSV
  download yields the completed sheet. Reads the new `columns` /
  `cells` fields from the draw-lines fragment. Drops the subaccount
  paragraph and reviewer notes. Adds a plain-ASCII rule. Raw-JSON-only
  anchor (no code fence), since a fence stops the CSV download from
  splitting columns.

## [0.1.0] — 2026-11-04

- Initial version. Drafts HHS PMS payment justifications from the
  draw-lines and award-purpose fragments of
  `workflows/hhs-draw-justification`: per-line sentences in the HHS
  "sufficient" pattern (cost, role, timeframe, link to the award),
  HHS's F&A wording verbatim for indirect lines, a paste-ready block
  for the billing spreadsheet, one combined justification per PMS
  subaccount, and reviewer notes. Written against Deborah Stenkamp's
  hand-completed CB7897 sheet for the 10/23/2026 draw.
