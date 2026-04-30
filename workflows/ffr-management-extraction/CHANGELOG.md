# Changelog

All notable changes to this workflow. Versions follow semver: MAJOR for step-structure changes, MINOR for additive changes (e.g., new search_set_items, validation checks), PATCH for display-name or wording edits.

## [0.1.0] — 2026-04-30

- Initial experimental release.
- Two-step runtime mirroring the source `ffr-management-extraction` v2 workflow in `ui-insight/ProcessMapping`: one Extraction task with an embedded SearchSet (16 items) plus one Consolidation Prompt that collapses the flat outputs into the schema's nested `submission_schedule`, `submission_system`, and `compliance_consequences` objects.
- `submission_system_platform` exposed as the five-value enum (`Payment Management System`, `ASAP`, `ACH`, `Grants.gov`, `Other`) — matches the source workflow's enum.
- Validation plan carries CHK-01 (Date format checks, format/error) and CHK-02 (Deadline consistency, consistency/warning) — matches the source `Validation_Plan`.
- Pins `ffr-management-extraction-udm@0.1.0`.
