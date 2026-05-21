# Changelog

All notable changes to this component. Versions follow semver: MAJOR for output-contract breaks, MINOR for backward-compatible additions, PATCH for wording or clarity.

## [0.1.0] — 2026-05-20

- Initial experimental release.
- Schema derived from the `export-to-banner-extraction` v2 Vandalizer workflow in `ui-insight/ProcessMapping` (six parallel extraction tasks, 52 source fields, two cross-field rules, four validation-plan checks).
- Six-block shape (`award_identification` + `dates_and_performance` + `sponsor_entity` + `budget_financial` + `billing_payment` + `reporting_special`) preserves the source workflow's per-extraction-task separation.
- Monetary fields typed as JSON numbers, not quoted strings: `total_award_amount`, `total_anticipated_amount`, `total_direct_costs`, `total_indirect_costs`, `cost_share_amount`, `budget_categories[].approved_amount`, `budget_periods[].amount`. Mirrors source `Decimal` field types. `fa_rate` typed as a string because the rate often carries a base annotation (e.g., `"30% MTDC"`).
- Enums match the source workflow exactly: `award_type` (4 values: `Grant`, `Cooperative Agreement`, `Contract`, `Subcontract`), `sponsor_entity_type` (7 values: `Federal`, `State Government`, `Non-Profit`, `Private Industry`, `Foundation`, `University`, `Other`), `fa_rate_base` (4 values + null: `MTDC`, `TDC`, `Salary & Wages`, `Other`), `billing_type` (4 values: `Cost Reimbursement`, `Fixed Price`, `Letter of Credit`, `Milestone`).
- Source `Is_Required: true` fields mirrored into `required` lists at the block level: `award_number`, `project_title`, `pi_name`, `award_type`, `is_pass_through`, `federal_agency_name`, `award_start_date`, `award_end_date`, `performance_period_start`, `performance_period_end`, `sponsor_name`, `sponsor_entity_type`, `awardee_organization`, `total_award_amount`, `budget_categories`, `billing_type`, `reporting_requirements`.
- `reporting_requirements` typed as an array of `{report_type, frequency, due_date_or_timing, submission_method}` objects per the source `Table` field type.
- Broad UDM column bindings preserved at leaf level: `Award.Award_Number`, `Award.Award_Title`, `Personnel.First_Name` / `Personnel.Last_Name`, `Award.Flow_Through_Indicator`, `Award.CFDA_Number`, `Organization.Organization_Name`, `Award.Original_Start_Date` / `Original_End_Date`, `AwardBudgetPeriod.Start_Date` / `End_Date`, `Organization.Organization_Type`, `Organization.UEI`, `Award.Current_Total_Funded`, `Award.Total_Anticipated_Funding`, `AwardBudget`, `AwardBudget.Approved_Indirect_Cost`, `IndirectRate.Rate_Percentage` / `Base_Type`, `CostShare.Committed_Amount`, `ContactDetails.ContactDetails_Value`, `Terms.Payment_Method` / `Invoicing_Frequency`, `Terms`. The six-block Banner-setup shape itself is repo-local.
- No eval cases yet — status `experimental` until at least one golden extraction is added under `evals/cases/`.
