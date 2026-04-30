# Evals — award-compliance-extraction-udm

Each case lives under `cases/<case-slug>/` with at minimum `metadata.yaml`, `input-source.md`, `expected.json`, and optional `notes.md`. Run artifacts go under `runs/` (gitignored).

## Planned cases

- **NSF cooperative agreement (multi-year)** — exercises non-empty `budget_period_amounts`, complex `compliance_calendar`, and the CFR-01 reconciliation rule.
- **NIH R01 (single-year, RTC-eligible)** — exercises `rtc_applicability` populated, empty `budget_period_amounts`.
- **High-risk recipient award** — exercises non-empty `high_risk_conditions` and `Single Audit` audit requirement.
- **Award with significant cost-share** — exercises `cost_share_requirements` populated and a corresponding `compliance_calendar` row.

## `validated_against_version`

Every case must declare the component version that its `expected.json` was validated against.
