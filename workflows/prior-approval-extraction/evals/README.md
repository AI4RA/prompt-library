# Evals — prior-approval-extraction (workflow-local)

This workflow carries its own cases under `cases/` because it is **not** a 1:1 repackaging of the `prior-approval-extraction-udm` component's canonical prompt. The Extraction task carries a focused `prompt_inline` body, and the Consolidation Prompt collapses the flat searchset outputs into the schema's nested objects (`budget_approvals`, `scope_timeline_approvals`) and normalizes the `approval_procedures` table.

Each case lives under `cases/<case-slug>/` with the same shape as component evals.

## What workflow-local cases need to exercise

- **Flat-to-nested collapse** — three rebudgeting/equipment/subaward items collapse into `budget_approvals`; three pi/nce/foreign-travel items collapse into `scope_timeline_approvals`.
- **Per-row procedures table** — the consolidator must produce one entry in `approval_procedures` per approval type, with thresholds and timelines quoted verbatim.
- **`rtc_waivers` waived-only rule** — kept approvals must NOT appear in `rtc_waivers`.
- **Validation-plan checks** — threshold format (CHK-01), approval procedure completeness (CHK-02).

## Status

The initial scaffolded case (`federal-award-rtc-stub`) is a placeholder pending sponsored-programs review against an authorized, de-identified federal award notice.
