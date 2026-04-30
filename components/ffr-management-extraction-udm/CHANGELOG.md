# Changelog

All notable changes to this component. Versions follow semver: MAJOR for output-contract breaks, MINOR for backward-compatible additions, PATCH for wording or clarity.

## [0.1.0] — 2026-04-30

- Initial experimental release.
- Schema derived from the `ffr-management-extraction` v2 Vandalizer workflow in `ui-insight/ProcessMapping` (single Extraction task + Formatting task; 7 source fields).
- Five structured buckets (`submission_schedule`, `submission_system`, `required_financial_data`, `compliance_consequences`, `preparation_timeline`) match the Five Output Sections produced by the canonical extraction prompt (FFR Submission Schedule, Submission System & Procedures, Required Financial Data, Compliance & Consequences, Preparation Timeline).
- Scalar `award_number` and `pi_name` fields added on top of the source workflow's seven Extraction fields so a single FFR extraction resolves cleanly to UDM `Award` + `Personnel` entities.
- `submission_system.platform` enum matches the source workflow's `Submission_System` Enum_Values (`Payment Management System`, `ASAP`, `ACH`, `Grants.gov`, `Other`).
- Source-workflow requiredness preserved: `submission_schedule.annual_ffr_due` and `submission_schedule.final_ffr_due` are required non-null strings (matching the source workflow's `Is_Required: true`); when the document does not state a value, use `"Not specified in the document"`.
- UDM column binding preserved: `required_financial_data` mirrors the source `Expenditure_Categories` field's UDM AwardBudget reference.
- `preparation_timeline` realized as an array of `{milestone, days_before_period_end, action, owner}` objects (rather than the source `Table` field) so the per-row owner is attached to the right milestone rather than implied.
- No eval cases yet — status `experimental` until at least one golden extraction is added under `evals/cases/`.
