# Changelog

All notable changes to this workflow. Versions follow semver.

## [0.1.0] — 2026-04-30

- Initial experimental release.
- Two-step runtime mirroring the source `effort-reporting-extraction` v2 workflow in `ui-insight/ProcessMapping`: one Extraction task with an embedded SearchSet (13 items) plus one Consolidation Prompt that normalizes the two enums and enforces the PI-mirror rule between `pi_committed_effort`/`pi_person_months` and the PI's row in `key_personnel_commitments`.
- `reporting_frequency` enum (`Monthly`, `Quarterly`, `Semi-Annual`, `Annual`) and `certification_method` enum (`After-the-Fact`, `Plan-Confirmation`, `Payroll-Based`) — match the source workflow's enums.
- Validation plan carries CHK-01 (Effort percentages sum, arithmetic/error), CHK-02 (Person-months consistency, consistency/warning), CHK-03 (Personnel table completeness, completeness/warning) — matches the source `Validation_Plan`.
- Pins `effort-reporting-extraction-udm@0.1.0`.
