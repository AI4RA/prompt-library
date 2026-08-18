# Changelog

All notable changes to this workflow. Versions follow semver adapted to
workflow semantics: MAJOR for step-structure changes, MINOR for prompt
tracking a referenced component MINOR or additive options, PATCH for
display-name / description polish.

## [0.2.0] — 2026-08-18

- **RA feedback refinement (Tami Clabough, pre-award SPA).** Tami had
  been correcting the output with a Vandalizer "Formatter"
  post-processing prompt (a second LLM pass on the task's Output tab,
  not carried in workflow exports). Her rules are folded into the main
  prompt instead — prompt tracks `viva-engage-reformat` 0.1.0 → 0.2.0:
  - Prime Sponsor and Budget Total always left blank (PreAward SPA
    completes them), even when the input carries values.
  - PI name reordered from the input's "last name, first name middle"
    to "first name, middle initial/name, last name".
  - Compact single-spaced entries matching her example (v0.1.0 had
    blank lines between fields).
- Validation plan extended 4 → 6 checks: blank-field enforcement
  (VE-04) and PI name order (VE-05) added; verbatim check narrowed to
  number/title/sponsor.
- MINOR: topology unchanged (single output step, `step_input`).

## [0.1.0] — 2026-08-18

- Initial capture from the University of Idaho RA team's live
  Vandalizer workflow "Viva Engage" (exported 2026-08-18). Single
  output step, one Prompt task reading `step_input`; prompt body
  recorded in `components/viva-engage-reformat` v0.1.0 and inlined at
  build time (the export carried only a `saved_prompt_uuid`
  reference). The live copy's `qwen/qwen3.6-27b` model pin is
  intentionally dropped — the run dialog's model applies. Four-check
  `VE-*` validation plan authored in the Vandalizer runtime schema.
