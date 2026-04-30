# Changelog

All notable changes to this component. Versions follow semver.

## [0.1.0] — 2026-04-30

- Initial experimental release.
- Schema derived from the `subaward-extraction` v2 Vandalizer workflow in `ui-insight/ProcessMapping` (six parallel Extraction tasks + Formatting task; 34 source fields).
- Six-block shape (core award / contacts / dates & monetary / financial policies / reporting / compliance) covering nine deliverable sections.
- All six contact fields realized as `{name, email, phone}` objects (rather than the source `String` fields concatenating "name, email, phone") so each component is structurally addressable for downstream notification routing.
- `technical_reports`, `financial_reports`, `invention_reporting`, and `governing_regulations` realized as arrays of typed objects (rather than the source `List` fields) so per-row attributes attach to the right entry.
- `cost_type` enum (`Cost Reimbursement`, `Fixed Price`, `Time and Materials`); `invoicing_frequency` enum (`Monthly`, `Quarterly`, `Semi-Annual`, `Annual`) — match the source workflow's enums.
- Cross-field rule from the source workflow (CFR-01: amount_funded == total_direct_costs + total_indirect_costs) is encoded in the prompt's encoding rules and the workflow validation_plan.
- UDM column bindings preserved: `pte_name`/`subrecipient_name` → `Organization.Organization_Name`; `federal_award_number` → `Award.Federal_Award_ID`; `subaward_number` → `Subaward.Subaward_Number`; `project_title` → `Award.Award_Title`; `subrecipient_pi.name` → `Subaward.PI_Name`; contact fields → `Personnel` + `ContactDetails`; `budget_period_start`/`end` → `Subaward.Start_Date`/`End_Date`; `amount_funded` → `Subaward.Subaward_Amount`; `invoicing_frequency` → `Terms.Invoicing_Frequency`; `fa_rate` → `IndirectRate.Rate_Percentage`; `fa_base` → `IndirectRate.Base_Type`; `cost_sharing_required` → `CostShare.Is_Mandatory`; reports → `AwardDeliverable`; `prior_approval_handling` → `Modification.Requires_Prior_Approval`; `coi_policy` → `ConflictOfInterest`; `record_retention` → `Terms.Record_Retention_Years`.
- No eval cases yet — status `experimental` until at least one golden extraction is added under `evals/cases/`.
