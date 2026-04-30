# Changelog

All notable changes to this workflow. Versions follow semver.

## [0.1.0] — 2026-04-30

- Initial experimental release.
- Two-step runtime mirroring the source `foa-checklist-extraction` v2 workflow in `ui-insight/ProcessMapping`: six parallel Extraction tasks (FOA Identification & Timeline; Evaluation Criteria; Review Process; Agency Priorities & Goals; Forms & Submission Systems; Formatting Requirements) plus a Consolidation Prompt that assembles the 31-field schema and enforces cross-field consistency.
- `federal_agency` enum (NSF, NIH, DOD, DOE, NASA, USDA, EPA, DOT, DOC, ED, Other) — matches the source workflow's enum.
- Validation plan carries CHK-01 (FOA number format, format/warning), CHK-02 (Date consistency, consistency/error), CHK-03 (Funding vs per-award amounts, arithmetic/warning) — matches the source `Validation_Plan`.
- Pins `foa-checklist-extraction-udm@0.1.0`.
