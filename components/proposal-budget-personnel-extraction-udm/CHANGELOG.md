# Changelog

All notable changes to this component. Versions follow semver.

## [0.1.0] — 2026-04-30

- Initial experimental release.
- Schema derived from the `proposal-budget-personnel-extraction` v2 Vandalizer workflow in `ui-insight/ProcessMapping` (two parallel Extraction tasks + Formatting task; 20 source fields).
- Four derivable boolean triggers (`has_postdocs_or_grad_students`, `mentoring_plan_required`, `has_subawards`, `has_equipment_over_5k`) computed from list lengths so downstream consumers (proposal-document-completeness-udm) can rely on internal consistency.
- `senior_key_personnel`, `postdoc_details`, `graduate_student_details`, `other_personnel`, `subaward_recipients`, `equipment_items`, `budget_categories`, `budget_periods` realized as arrays of typed objects (rather than the source `Table` fields) so per-row attributes attach to the right entry.
- `graduate_student_details.type` enum (`RA`, `TA`); `fa_rate_and_base.base` enum (`MTDC`, `TDC`, `Salary & Wages`) — match the source workflow's `FA_Rate_And_Base` Enum_Values.
- Equipment threshold ($5,000) encoded structurally via `equipment_items.cost.minimum: 5000.01`.
- Cross-field rule from the source workflow (CFR-01: mentoring_plan_required derives from postdoc/graduate counts) is encoded by the schema's required-derivation rule for the boolean fields.
- UDM column bindings preserved: `senior_key_personnel` → `Personnel`; `fa_rate_and_base` → `IndirectRate`; `cost_sharing` → `CostShare`.
- No eval cases yet — status `experimental` until at least one golden extraction is added under `evals/cases/`.
