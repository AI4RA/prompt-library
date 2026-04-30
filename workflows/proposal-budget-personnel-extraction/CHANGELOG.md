# Changelog

All notable changes to this workflow. Versions follow semver.

## [0.1.0] — 2026-04-30

- Initial experimental release.
- Two-step runtime mirroring the source `proposal-budget-personnel-extraction` v2 workflow in `ui-insight/ProcessMapping`: two parallel Extraction tasks (personnel identification + budget structure) plus a Consolidation Prompt that derives the four boolean compliance triggers (`has_postdocs_or_grad_students`, `mentoring_plan_required`, `has_subawards`, `has_equipment_over_5k`) from list lengths and combines `fa_rate` + `fa_base` into the nested `fa_rate_and_base` object.
- `fa_base` enum (`MTDC`, `TDC`, `Salary & Wages`) — matches the source `FA_Rate_And_Base` Enum_Values.
- Validation plan carries CHK-01 (Personnel count consistency, consistency/warning), CHK-02 (Boolean flag derivation, consistency/warning), CHK-03 (Cost totals validation, arithmetic/error) — matches the source `Validation_Plan`.
- Pins `proposal-budget-personnel-extraction-udm@0.1.0`.
