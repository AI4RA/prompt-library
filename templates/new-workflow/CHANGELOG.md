# Changelog

All notable changes to this workflow. Versions follow semver adapted to workflow semantics:

- **MAJOR** — step structure changes (add or remove a step, change `input_source`, change `is_output`, re-pin a component across a component MAJOR).
- **MINOR** — prompt body tracking a referenced component MINOR, or additive step/task options that preserve the existing operator flow.
- **PATCH** — step or task display-name edits, description polish, non-semantic manifest cleanup.

When a referenced component bumps MAJOR, this workflow must either re-pin (and bump its own MAJOR) or be marked retired in `manifest.yaml`.

## [1.0.0] — YYYY-MM-DD

- Initial workflow.
