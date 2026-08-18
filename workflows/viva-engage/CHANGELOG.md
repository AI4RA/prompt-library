# Changelog

All notable changes to this workflow. Versions follow semver adapted to
workflow semantics: MAJOR for step-structure changes, MINOR for prompt
tracking a referenced component MINOR or additive options, PATCH for
display-name / description polish.

## [0.1.0] — 2026-08-18

- Initial capture from the University of Idaho RA team's live
  Vandalizer workflow "Viva Engage" (exported 2026-08-18). Single
  output step, one Prompt task reading `step_input`; prompt body
  recorded in `components/viva-engage-reformat` v0.1.0 and inlined at
  build time (the export carried only a `saved_prompt_uuid`
  reference). The live copy's `qwen/qwen3.6-27b` model pin is
  intentionally dropped — the run dialog's model applies. Four-check
  `VE-*` validation plan authored in the Vandalizer runtime schema.
