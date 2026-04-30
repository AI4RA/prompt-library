# Changelog

All notable changes to this component. Versions follow semver: MAJOR for output-contract breaks, MINOR for backward-compatible additions, PATCH for wording or clarity.

## [0.1.0] — 2026-04-30

- Initial experimental release.
- Schema derived from the `effort-reporting-extraction` v2 Vandalizer workflow in `ui-insight/ProcessMapping` (single Extraction task + Formatting task; 13 source fields).
- `key_personnel_commitments` realized as an array of `{name, role, committed_effort, person_months, cost_shared_effort, notes}` objects (rather than the source `Table` field) so per-row effort details attach to the right individual.
- `reporting_frequency` enum matches the source `Reporting_Frequency` Enum_Values (`Monthly`, `Quarterly`, `Semi-Annual`, `Annual`).
- `certification_method` enum matches the source `Certification_Method` Enum_Values (`After-the-Fact`, `Plan-Confirmation`, `Payroll-Based`).
- UDM column bindings preserved: `award_number` → `Award.Award_Number`; `pi_name` → `Personnel.First_Name`/`Last_Name`; `project_title` → `Award.Award_Title`; `certification_method` → `Effort.Certification_Method`; `pi_committed_effort` → `Effort.Committed_Percent`; `pi_person_months` → `Effort.Committed_Person_Months`; `cost_shared_effort` → `CostShare.Committed_Amount`; `record_retention` → `Terms.Record_Retention_Years`.
- No eval cases yet — status `experimental` until at least one golden extraction is added under `evals/cases/`.
