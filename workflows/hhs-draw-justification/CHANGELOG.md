# Changelog

All notable changes to this workflow. Versions follow semver adapted to
workflow semantics: MAJOR for step-structure changes, MINOR for prompt
tracking a referenced component MINOR or additive options, PATCH for
display-name / description polish.

## [0.4.1] — 2026-11-04

- Fixes from a Codex re-review of PR #21:
  - "as described in the approved budget" removed from the services
    and publication patterns: nothing the workflow reads shows the
    budget. The PI can add it after checking.
  - Publication sentences now include the month incurred.
  - Prior-wording reuse applies only when the line has a pay period,
    the prior sentence has a date range to replace, and it carries no
    name or code; the missing-period, ASCII, and PII rules always win.
  - Catalog notes and eval docs describe the single input fragment and
    the optional prior sheet (no NoA / aims).
- Tracks `hhs-payment-justification` 0.4.0 → 0.4.1.

## [0.4.0] — 2026-11-04

- **PI review.** Deb reviewed the v0.3.0 CSV ("Not bad! ... would lean
  toward using less specific language") and returned the sheet she
  submitted for the 11/06/2026 draw. Changes to match it:
  - `extract-award-purpose` removed: justifications stay general ("to
    conduct the research activities supported by this award"), so no
    Notice of Award or aims page is needed. Parallel tasks 2 → 1
    (breaking, hence 0.4.0).
  - Sentence patterns follow hers: services and publication costs
    read "..., as described in the approved budget, ..."; supplies
    "purchased in <month> for use in ..."; no journal names or
    purchase purposes are invented.
  - With the PI's last completed sheet uploaded, payroll lines reuse
    her sentence for the same account code with the dates swapped.
  - "LARF PD" → "services provided by the Laboratory Animal Research
    Facility"; publishers → publication costs; retail vendors →
    laboratory supplies.
  - Justification header falls back to "ACTIVITY"; total rows are
    copied in place with an empty justification.
- Validation check HDJ-06 now checks for general wording.
- Tracks `hhs-payment-justification` 0.3.1 → 0.4.0.

## [0.3.1] — 2026-11-04

- Fixes from a Codex review of PR #21:
  - Payroll lines with a pay date outside the table get "for the pay
    period paid on <date>" and a flag, never the pay date as the dates
    worked.
  - The fallback for a missing or misaligned `cells` array uses OSP's
    fixed header list for every row, so CSV columns stay aligned.
  - Names stay in OSP's copied cells but are banned from every derived
    field (resolves a contradiction with verbatim copying).
  - E4135 / E4282 default roles are now "project student research
    assistants"; narrower categories need prior wording or a document.
  - Eval posture changed to `workflow_local: true` with a stub case,
    per `docs/contracts.md` for multi-step workflows.
  - README no longer mentions the removed subaccount paragraph.
- Tracks `hhs-payment-justification` 0.3.0 → 0.3.1.

## [0.3.0] — 2026-11-04

- First v0.2.0 run on the real 11/06/2026 CB7897 sheet (16 lines:
  payroll, animal per diem, publication, supplies, F&A) downloaded as a
  clean 16 × 15 CSV. Two prompt fixes from it:
  - **Sentence shape.** "... to study how thyroid hormone controls
    color vision genes ... supported by this award." left the closing
    phrase dangling. `extract-award-purpose` now returns a noun-phrase
    `research_topic` (was `activity_phrase`) and justifications read
    "... to carry out the research supported by this award on
    <topic>.", with cost-fitting verbs (publication costs "to publish
    findings from ...").
  - **Service month over posting date.** The September 2026 LARF per
    diem posted 10/19 was justified as "October 2026".
    `extract-draw-lines` now uses a service period named in Description
    before TransDate for non-payroll lines.
- Validation checks HDJ-03 and HDJ-06 reworded to match.
- Tracks `hhs-payment-justification` 0.2.0 → 0.3.0.

## [0.2.0] — 2026-11-04

- **The output is now the filled billing sheet.** The first Vandalizer
  run (CB7897) got the content right, but the PI's job is to return
  OSP's spreadsheet with the justification column filled, not to copy
  sentences out of a report. The consolidation now emits a JSON array
  with one object per sheet row, keyed by the sheet's own headers in
  order, with the justification column filled. Vandalizer's
  **Download → CSV** turns it into a spreadsheet that opens in Excel.
- `extract-draw-lines` now captures the sheet's headers (`columns`)
  and each row's cells verbatim (`cells`) so the output can reproduce
  every column.
- Dropped from the deliverable: the Markdown table, paste block, PMS
  subaccount paragraph, and reviewer notes. Line flags are still in the
  Extraction step's output.
- Justifications are plain ASCII so Excel doesn't garble them.
- Validation plan rewritten for the row-array output (8 → 7 checks).
- Tracks `hhs-payment-justification` 0.1.0 → 0.2.0.

## [0.1.0] — 2026-11-04

- Initial version. Two parallel extraction tasks (`extract-draw-lines`,
  `extract-award-purpose`) reading `workflow_documents`, then the
  `hhs-payment-justification` consolidation as the output step.
- Payroll timeframes come from a pay-date → pay-period table
  (pay dates 9/25/2026 through 6/18/2027) embedded in
  `extract-draw-lines`, derived from one confirmed example.
- Eight-check `HDJ-*` validation plan in the Vandalizer runtime schema.
- Not yet run in Vandalizer.
