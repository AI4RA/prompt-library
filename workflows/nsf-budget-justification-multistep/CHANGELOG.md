# Changelog

All notable changes to this workflow. Versions follow semver adapted to workflow semantics:

- **MAJOR** — step structure changes (add or remove a step, change `input_source`, change `is_output`, re-pin any component across a component MAJOR).
- **MINOR** — prompt body tracking a referenced component's MINOR, or additive step/task options that preserve the existing operator flow.
- **PATCH** — step or task display-name edits, description polish, non-semantic manifest cleanup.

When any referenced component bumps MAJOR, this workflow must either re-pin (and bump its own MAJOR) or be marked retired in `manifest.yaml`.

## [2.0.0] — 2026-04-24

- Added a fourth step that renders the reviewed eight-section array into Word-pasteable Markdown and HTML strings, pinning the new `nsf-budget-justification-render-udm@1.0.0` component.
- Moved `is_output: true` from step 3 (review) to step 4 (render). The workflow's deliverable is now a JSON object with `markdown` and `html` fields validating against `components/nsf-budget-justification-render-udm/schema.json` — a breaking change from the eight-section array deliverable in 1.0.0.
- The earlier intermediate artifacts (structured budget after step 1, drafted array after step 2, reviewed array after step 3) remain available to Vandalizer operators as step results.

## [1.0.0] — 2026-04-24

- Initial workflow. Three steps (ingest → draft → review) pinning `nsf-budget-spreadsheet-ingest-udm@1.0.0`, `nsf-budget-justification-udm@1.0.0`, and `nsf-budget-justification-review-udm@1.0.0`.
