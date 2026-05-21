# Changelog

All notable changes to this component. Versions follow semver: MAJOR for output-contract breaks, MINOR for backward-compatible additions, PATCH for wording or clarity.

## [0.1.0] — 2026-05-20

- Initial experimental release.
- Schema derived from the `award-modification-intake` v1 Vandalizer workflow in `ui-insight/ProcessMapping` (three parallel extraction tasks, 28 source fields, four cross-field rules, five validation-plan checks).
- Three-block shape (`identification` + `financial` + `compliance`) preserves source extraction-task separation; flat fields collapse into the relevant block per the placement contract in `prompt.md`.
- `modification_type` exposed as the seven-value enum from the source workflow (`Additional Funds`, `No-Cost Extension`, `PI Change`, `Rebudget`, `Scope Change`, `Administrative Change`, `Combined (multiple types)`).
- `execution_status` exposed as the three-value enum from the source workflow (`Unilateral (fully executed)`, `Bilateral (requires signature)`, `Not specified in the document`).
- Monetary fields (`modification_amount`, `current_award_amount`, `total_obligated_amount`, `fa_amount`, `budget_breakdown[].approved_amount`) typed as JSON numbers, not quoted strings, per the source workflow's `Decimal` field type. `fa_rate` typed as a string because the rate carries a base-type annotation (e.g., `"30% MTDC"`).
- Source `Is_Required: true` fields (`award_number`, `amendment_number`, `modification_type`, `execution_status`, `prior_approval_required`, `end_date_change`, `requires_financial_unit`) mirrored into `required` lists at the block level.
- UDM column bindings preserved: `award_number` → `Award.Award_Number` / `Award.Federal_Award_ID`; `sponsor_name` / `pi_name` → `Organization.Organization_Name` / `Personnel`; `modification_amount` → `Modification.Funding_Amount_Change`; `current_award_amount` → `Award.Current_Total_Funded`; `fa_rate` → `IndirectRate.Rate_Percentage`; `budget_breakdown` → `AwardBudget`; `cost_share_changes` → `CostShare.Committed_Amount`; `sponsor_conditions` → `Terms.Special_Conditions`; `prior_approval_required` → `Modification.Requires_Prior_Approval`.
- Source STEP-03 ApprovalNode (Post-Award Specialist review) omitted from the extraction contract — it is a runtime UI concern of Vandalizer's import surface, not a part of the JSON contract.
- No eval cases yet — status `experimental` until at least one golden extraction is added under `evals/cases/`.
