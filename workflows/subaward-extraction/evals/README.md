# Evals — subaward-extraction (workflow-local)

This workflow carries its own cases under `cases/` because the Consolidation Prompt does substantial work — it composes 18 flat contact searchset items into six structured `{name, email, phone}` objects, normalizes the two enums (`cost_type`, `invoicing_frequency`), and enforces the CFR-01 reconciliation between `amount_funded`, `total_direct_costs`, and `total_indirect_costs`.

## What workflow-local cases need to exercise

- **Contact composition** — each PI/admin/financial contact gets a single `{name, email, phone}` object on output; missing-name contacts collapse to `null` rather than `{name: null, ...}`.
- **Enum normalization** — `cost_type` and `invoicing_frequency` mapped from document phrasings to enum values.
- **CFR-01 reconciliation** — `amount_funded == total_direct_costs + total_indirect_costs` when all three present; surface the conflict via validation_plan when not.
- **Strict-inclusion rule** — `technical_reports` and `financial_reports` empty arrays when the agreement does not require any (no synthesis of "standard" reports).
- **Validation-plan checks** — monetary cross-reference (CHK-01), date consistency (CHK-02), contact info format (CHK-03).

## Status

The initial scaffolded case (`pte-academic-subrecipient-stub`) is a placeholder pending sponsored-programs review against an authorized, de-identified PTE → academic-subrecipient subaward.
