# Evals — award-compliance-extraction (workflow-local)

This workflow carries its own cases under `cases/` because the Consolidation Prompt does substantial work — it merges `compliance_calendar` entries across both upstream fragments, normalizes the `audit_requirements` and `record_retention` enums, and enforces the CFR-01 cross-field reconciliation rule.

## What workflow-local cases need to exercise

- **Calendar merge / dedupe** — when both `compliance_framework` and `financial_management` produce calendar-relevant entries (e.g., FFR cadence appears in both), the consolidator merges them keyed on `(requirement_type, deadline)`.
- **Enum normalization** — `audit_requirements` and `record_retention` mapped from document phrasings to enum values.
- **Multi-year reconciliation** — `sum(budget_period_amounts.amount) == total_award_amount` (CFR-01); a non-reconciling case should surface in the validation plan.
- **Single-period collapse** — `budget_period_amounts: []` for single-year awards; `total_award_amount` still set.
- **Validation-plan checks** — monetary format (CHK-01), date validity (CHK-02), compliance calendar completeness (CHK-03).

## Status

The initial scaffolded case (`nsf-cooperative-agreement-multi-year-stub`) is a placeholder pending sponsored-programs review against an authorized, de-identified NSF cooperative agreement.
