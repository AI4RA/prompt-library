# Changelog

All notable changes to this workflow. Versions follow semver: MAJOR for step-structure changes, MINOR for additive changes (e.g., new search_set_items, validation checks), PATCH for display-name or wording edits.

## [0.1.0] — 2026-05-20

- Initial experimental release.
- Two-step runtime mirroring the source `export-to-banner-extraction` v2 workflow in `ui-insight/ProcessMapping`: six parallel Extraction tasks (award-identification, dates-and-performance, sponsor-and-entity, budget-and-financial, billing-and-payment, reporting-and-special) with embedded SearchSets, plus a Consolidation Prompt that assembles the six JSON fragments into a single schema-conformant object, converts quoted-dollar strings to JSON numbers, normalizes the four enums, and enforces the two source cross-field rules as flag emissions on `reporting_special.special_terms`.
- Four enums match the source workflow exactly: `award_type` (Grant, Cooperative Agreement, Contract, Subcontract); `sponsor_entity_type` (Federal, State Government, Non-Profit, Private Industry, Foundation, University, Other); `fa_rate_base` (MTDC, TDC, Salary & Wages, Other); `billing_type` (Cost Reimbursement, Fixed Price, Letter of Credit, Milestone).
- Monetary fields explicitly typed and prompted as JSON numbers, not quoted strings — applies CFR-04-style number-vs-string handling from the boss's PR #33 review feedback to every monetary leaf in the schema.
- Validation plan carries CHK-01..CHK-04 — matches the source `Validation_Plan` with field-target paths updated to reflect the schema's six-block shape.
- Source `Cross_Field_Rules` (CFR-01 `award_start < award_end`; CFR-02 `performance_period_start <= award_start_date`) enforced by the Consolidation Prompt at runtime as flag strings on `reporting_special.special_terms` rather than altering the dates.
- Pins `export-to-banner-extraction-udm@0.1.0`.
