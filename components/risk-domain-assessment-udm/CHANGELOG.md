# Changelog

All notable changes to this component. Versions follow semver: MAJOR for output-contract breaks, MINOR for backward-compatible additions, PATCH for wording or clarity.

## [0.1.0] — 2026-05-20

- Initial experimental release.
- Schema derived from the `risk-domain-assessment` v2 Vandalizer workflow in `ui-insight/ProcessMapping` (six parallel extraction tasks, 14 domain scores + evidence fields, three cross-field rules, three validation-plan checks).
- Three-block shape (`award_metadata` + `domain_scores` + `aggregate_metrics`) preserves the source workflow's per-domain rubric structure and adds explicit aggregate-metric derivations.
- **Scores typed as JSON integers in `[1, 5]`** via a shared `$defs/domain_score_integer` definition. Mirrors the source workflow's `Field_Type: Integer`. The source workflow's `Enum_Values: ["1","2","3","4","5"]` on some domain scores is treated as documentation, not as a string-enum encoding — the schema enforces JSON integer encoding. Applies the boss's PR #33 review feedback (number vs string) to all scoring fields.
- `aggregate_metrics.total_risk_score` typed as JSON integer in `[14, 70]`. `aggregate_metrics.average_risk_score` typed as JSON number in `[1.0, 5.0]`. `aggregate_metrics.overall_risk_level` exposed as the four-value enum (`Low`, `Moderate`, `High`, `Very High`).
- Every domain block requires both `score` and `justification` — mirrors source workflow's CFR-01 (justification not empty when score ≥ 3) by enforcing `minLength: 1` on every justification. The prompt strengthens this further by requiring justifications to be evidence-cited.
- Domain-specific evidence fields preserved from the source workflow:
  - Monetary evidence fields (`domain_2.total_federal_funding`, `total_anticipated_funding`, `cost_share_amount`) typed as JSON numbers. Mirrors source `Field_Type: Decimal`.
  - `domain_2.cost_share_required`, `domain_4.export_control_concerns`, `domain_6.evaluator_required`, `domain_6.data_use_agreements_required`, `domain_8.pass_through_indicator`, `domain_2.multiple_funding_streams`, `domain_3.foreign_partners_present` typed as JSON booleans.
- Source `Is_Required: true` fields mirrored into `required` lists per domain block.
- UDM column bindings preserved at the leaf level:
  - `award_metadata`: `award_number` → `Award.Award_Number`; `cfda_number` → `Award.CFDA_Number`; `sponsor_name` → `Organization.Organization_Name`; `award_period_start` / `award_period_end` → `Award.Original_Start_Date` / `Original_End_Date`.
  - `domain_1.project_title` → `Award.Award_Title`.
  - `domain_2.total_federal_funding` → `Award.Current_Total_Funded`; `total_anticipated_funding` → `Award.Total_Anticipated_Funding`; `cost_share_required` → `CostShare.Is_Mandatory`; `cost_share_amount` → `CostShare.Committed_Amount`; `idc_rate_restriction` → `IndirectRate.Rate_Percentage`.
  - `domain_3.subrecipient_risk_level` → `Subaward.Risk_Level`; `subrecipient_monitoring_requirements` → `Subaward.Monitoring_Plan`.
  - `domain_5.compliance_requirement_type` → `ComplianceRequirement.Requirement_Type`; `compliance_risk_level` → `ComplianceRequirement.Risk_Level`.
  - `domain_6.reporting_frequency` → `Terms.Invoicing_Frequency`; `reporting_requirements_detail` → `Terms.Reporting_Requirements`.
  - `domain_8.pass_through_indicator` → `Award.Flow_Through_Indicator`.
  - `domain_10.closeout_requirements` → `Terms.Closeout_Requirements`; `property_equipment_obligations` → `Terms.Property_Requirements`.
  - `domain_12.publication_requirements` → `Terms.Publication_Requirements`.
  - `domain_13.special_conditions` → `Terms.Special_Conditions`.
- The 14-domain rubric and aggregate-metrics shape are repo-local — no shared UDM risk-rubric table exists yet.
- No eval cases yet — status `experimental` until at least one golden extraction is added under `evals/cases/`.
