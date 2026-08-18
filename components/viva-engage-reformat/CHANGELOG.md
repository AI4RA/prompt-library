# Changelog

## [0.2.0] — 2026-08-18

- **RA feedback refinement (Tami Clabough, Sponsored Programs
  Administrator II, pre-award).** Tami reviewed live output and had
  been compensating with a Vandalizer "Formatter" post-processing
  prompt on the task's Output tab; her rules are now folded into the
  main prompt so a single pass produces the final format:
  - **Prime Sponsor and Budget Total always left blank** (nothing
    after "Prime Sponsor:" / nothing after "Budget Total: $") — the
    PreAward SPA completes them if applicable, even when the input
    row carries values.
  - **PI name reordered**: input arrives "last name, first name
    middle"; output renders "first name, middle initial or name (if
    present), last name", with worked examples for both the
    middle-initial and no-middle cases.
  - **Compact entry format** matching her example: single-spaced
    field lines (v0.1.0 had a blank line between fields), blank line
    between entries.
  - Explicit anchors added: verbatim number/title/sponsor, one entry
    per row, skip header rows, no surrounding prose.

## [0.1.0] — 2026-08-18

- Initial capture. Prompt body recorded verbatim from the University of
  Idaho RA team's live Vandalizer saved prompt "Viva Engage" (exported
  2026-08-18): for each input row, emit a fixed six-field "Proposal
  Submission" block (Proposal Number, Proposal Title, Sponsor, Prime
  Sponsor, Principal Investigator, Budget Total). No hardening applied
  yet — this version establishes the baseline before any prompt
  iteration.
