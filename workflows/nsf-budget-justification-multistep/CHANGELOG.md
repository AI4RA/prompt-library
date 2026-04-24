# Changelog

All notable changes to this workflow. Versions follow semver adapted to workflow semantics:

- **MAJOR** — step structure changes (add or remove a step, change `input_source`, change `is_output`, re-pin any component across a component MAJOR).
- **MINOR** — prompt body tracking a referenced component's MINOR, or additive step/task options that preserve the existing operator flow.
- **PATCH** — step or task display-name edits, description polish, non-semantic manifest cleanup.

When any referenced component bumps MAJOR, this workflow must either re-pin (and bump its own MAJOR) or be marked retired in `manifest.yaml`.

## [1.0.0] — 2026-04-24

- Initial workflow. Three steps (ingest → draft → review) pinning `nsf-budget-spreadsheet-ingest-udm@1.0.0`, `nsf-budget-justification-udm@1.0.0`, and `nsf-budget-justification-review-udm@1.0.0`.
