# Award Compliance & Financial Overview Extraction

Uploads a federal award notice or agreement and returns a single structured JSON object covering both the compliance framework (10 fields including a normalized compliance calendar) and the financial management structure (10 fields including budget periods and budget categories).

**Workflow version:** 0.1.0
**Vandalizer schema version:** 2
**Status:** experimental
**Components manifested:** `award-compliance-extraction-udm@0.1.0`
**Eval posture:** workflow-local — see [`evals/`](evals/)

## What this workflow does

Two-step runtime mirroring the source `ui-insight/ProcessMapping/workflows/award-compliance-extraction/` workflow:

**Step 1 — Parallel Extraction (2 Extraction tasks):**

| Task | Schema target | SearchSet items |
|---|---|---|
| `extract-compliance-framework` | `compliance_framework` block | `uniform_guidance_applicability`, `rtc_applicability`, `financial_reporting_requirements`, `progress_reporting_requirements`, `prior_approval_requirements`, `budget_modification_restrictions`, `property_requirements`, `deliverable_requirements`, `high_risk_conditions`, `compliance_calendar` |
| `extract-financial-management` | `financial_management` block | `total_award_amount`, `budget_period_amounts`, `cost_share_requirements`, `fa_rate`, `fa_rate_base`, `performance_period`, `budget_categories`, `ffr_requirements`, `audit_requirements` (enum), `record_retention` (enum) |

**Step 2 — Consolidation (1 Prompt task):** `award-compliance-consolidation` assembles the two fragments into the schema's two-block shape, normalizes the `audit_requirements` and `record_retention` enums, and merges/dedupes `compliance_calendar` entries from both fragments.

## Components

- [`award-compliance-extraction-udm@0.1.0`](../../components/award-compliance-extraction-udm/) — the sole component.

## Validation plan

| Check | Type | Severity |
|---|---|---|
| `CHK-01` Monetary amount format | format | error |
| `CHK-02` Date validity | format | error |
| `CHK-03` Compliance calendar completeness | completeness | warning |

## Eval posture

Workflow-local — see [`evals/`](evals/). The Consolidation Prompt does substantial work — it merges `compliance_calendar` entries from both fragments, normalizes the enums, and enforces the CFR-01 cross-field reconciliation rule between `total_award_amount` and `budget_period_amounts` — so per [`docs/contracts.md`](../../docs/contracts.md) workflow-local cases are required.

## Building

```bash
python3 scripts/build_vandalizer_workflows.py
```

## Sharing

The committed `award-compliance-extraction.vandalizer.json` can be uploaded directly into Vandalizer via the workflow import UI.

## Triad integration

- **Evaluation datasets:** none yet — planned: cases at `components/award-compliance-extraction-udm/evals/cases/`.
- **Shared UDM relationship:** inherits from the component's broad UDM alignment (Award, AwardBudget, AwardBudgetPeriod, AwardDeliverable, CostShare, IndirectRate, Modification, Terms).

## Provenance

Authored 2026-04-30 alongside the initial `award-compliance-extraction-udm` component.
