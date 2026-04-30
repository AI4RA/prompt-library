# Changelog

All notable changes to this component. Versions follow semver: MAJOR for output-contract breaks, MINOR for backward-compatible additions, PATCH for wording or clarity.

## [0.1.0] — 2026-04-30

- Initial experimental release.
- Schema derived from the `award-compliance-extraction` v2 Vandalizer workflow in `ui-insight/ProcessMapping` (two parallel Extraction tasks + Formatting task; 20 source fields).
- Two-block shape: `compliance_framework` (10 keys) + `financial_management` (10 keys).
- `compliance_calendar` realized as an array of `{requirement_type, deadline, responsible_party, consequences}` objects (rather than the source `Table` field) so per-deadline ownership and consequences are attached to the right entry.
- `budget_period_amounts` realized as an array of `{period, start_date, end_date, amount}` objects (rather than the source `Table` field) so the cross-field reconciliation rule (CFR-01: sum should equal total_award_amount) can be checked structurally.
- `budget_categories` realized as an array of `{category_name, approved_amount, restrictions, prior_approval_required}` objects so per-category restrictions and prior-approval flags are attached to the right category.
- `audit_requirements` enum matches the source `Audit_Requirements` Enum_Values (`Single Audit`, `A-133`, `Program-Specific Audit`, `Not applicable`).
- `record_retention` enum matches the source `Record_Retention` Enum_Values (`3 years`, `5 years`, `7 years`, `Per sponsor requirements`).
- Cross-field rule from the source workflow (CFR-01: sum(budget_period_amounts) == total_award_amount) is encoded by the schema shape and validation_plan rather than as a constraint.
- UDM column bindings preserved verbatim (see prompt.md): `total_award_amount` → `Award.Current_Total_Funded`; `budget_period_amounts` → `AwardBudgetPeriod`; `cost_share_requirements` → `CostShare.Committed_Amount`; `fa_rate` → `IndirectRate.Rate_Percentage`; `fa_rate_base` → `IndirectRate.Base_Type`; `performance_period` → `Award.Original_Start_Date`; `budget_categories` → `AwardBudget`; `ffr_requirements` and `financial_reporting_requirements` → `Terms.Reporting_Requirements`; `progress_reporting_requirements` and `deliverable_requirements` → `AwardDeliverable`; `prior_approval_requirements` → `Modification.Requires_Prior_Approval`; `property_requirements` → `Terms.Property_Requirements`; `record_retention` → `Terms.Record_Retention_Years`; `high_risk_conditions` → `Terms.Special_Conditions`.
- No eval cases yet — status `experimental` until at least one golden extraction is added under `evals/cases/`.
