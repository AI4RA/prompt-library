# Export to Banner Award Extraction

Uploads a fully-executed federal award document and returns a single structured JSON object covering the six blocks needed to populate the VERAS Export to Banner form.

**Workflow version:** 0.1.0
**Vandalizer schema version:** 2
**Status:** experimental
**Components manifested:** `export-to-banner-extraction-udm@0.1.0`
**Eval posture:** workflow-local — see [`evals/`](evals/)

## What this workflow does

The operator uploads a fully-executed federal award document (notice of award, cooperative agreement, contract, or modification) into Vandalizer. The workflow runs as two steps:

**Step 1 — Parallel Extraction (6 Extraction tasks):**

| Task | Schema target | SearchSet items (highlights) |
|---|---|---|
| `extract-award-identification` | `award_identification` | `award_number`, `project_title`, `pi_name`, `award_type` (enum), `is_pass_through`, `prime_sponsor_name`, `cfda_number`, `naics_code`, `federal_agency_name` |
| `extract-dates-and-performance` | `dates_and_performance` | `award_start_date`, `award_end_date`, `performance_period_start`, `performance_period_end`, `budget_periods`, `is_multi_year` |
| `extract-sponsor-and-entity` | `sponsor_entity` | `sponsor_name`, `sponsor_entity_type` (enum), `federal_agency_hierarchy`, `sponsor_address`, `sponsor_uei`, `awardee_organization`, `awardee_uei` |
| `extract-budget-and-financial` | `budget_financial` | `total_award_amount` (JSON number), `total_anticipated_amount`, `budget_categories`, `total_direct_costs`, `total_indirect_costs`, `fa_rate`, `fa_rate_base` (enum), `is_fa_waived`, `cost_share_amount`, `cost_share_type`, `program_income` |
| `extract-billing-and-payment` | `billing_payment` | `billing_type` (enum), `billing_frequency`, `billing_address`, `invoice_email`, `pms_loc_code`, `payment_terms`, `invoice_requirements`, `final_invoice_deadline`, `billing_contact` |
| `extract-reporting-and-special` | `reporting_special` | `reporting_requirements` (typed-row table), `record_retention_period`, `carry_forward_policy`, `prior_approval_requirements`, `special_terms`, `closeout_requirements`, `governing_regulations` |

**Step 2 — Consolidation (1 Prompt task):** `export-to-banner-extraction-consolidation` assembles the six JSON fragments into the schema-conformant six-block object, converts quoted dollar strings to JSON numbers (this is the boss's number-vs-string requirement), normalizes the four enums (`award_type`, `sponsor_entity_type`, `fa_rate_base`, `billing_type`), and enforces the two source cross-field rules (CFR-01 `award_start < award_end`; CFR-02 `performance_period_start <= award_start_date`) as flag strings appended to `reporting_special.special_terms` rather than altering the dates.

The runtime mirrors the source `ui-insight/ProcessMapping/workflows/export-to-banner-extraction/` workflow one-for-one.

## Components

- [`export-to-banner-extraction-udm@0.1.0`](../../components/export-to-banner-extraction-udm/) — the sole component. The six Extraction tasks carry focused `prompt_inline` bodies in [`manifest.yaml`](manifest.yaml); the canonical full-document prompt at [`components/export-to-banner-extraction-udm/prompt.md`](../../components/export-to-banner-extraction-udm/prompt.md) remains the single-call reference for harness invocations.

## Validation plan

Carried into the Vandalizer export at the workflow level (mirrors the source ProcessMapping `Validation_Plan`):

| Check | Type | Severity |
|---|---|---|
| `CHK-01` Date range consistency | consistency | error |
| `CHK-02` Monetary amount formatting | format | error |
| `CHK-03` UEI format validation | format | warning |
| `CHK-04` CFDA number format | format | warning |

The two source `Cross_Field_Rules` (CFR-01 `award_start_date < award_end_date`, CFR-02 `performance_period_start <= award_start_date`) are enforced by the Consolidation Prompt at runtime as flag strings on `reporting_special.special_terms` rather than as separate validation entries.

## Eval posture

Workflow-local — see [`evals/`](evals/). The workflow is **not** a 1:1 repackaging of the canonical component prompt: each Extraction task carries a focused `prompt_inline` body covering a single block, and the Consolidation Prompt converts quoted-dollar strings to JSON numbers and emits CFR-01 / CFR-02 flag strings, so per [`docs/contracts.md`](../../docs/contracts.md) workflow-local cases are required to cover behavior that emerges from the seven-task topology.

Workflow-local cases should target the four enum coverages (`award_type`, `sponsor_entity_type`, `fa_rate_base`, `billing_type`), the quoted-dollar-to-JSON-number conversion, the `budget_periods` array population for multi-year incremental awards, and the CFR-01 / CFR-02 flag-emission paths.

## Building

Re-generate the Vandalizer export from `manifest.yaml`:

```bash
python3 scripts/build_vandalizer_workflows.py
```

CI fails when the committed `export-to-banner-extraction.vandalizer.json` differs from a fresh build, so treat `manifest.yaml` as the source of truth and never hand-edit the generated JSON.

## Sharing

The committed `export-to-banner-extraction.vandalizer.json` can be uploaded directly into Vandalizer via the workflow import UI. Its `x_ai4ra` block traces it back to this manifest, the pinned component version, and the content hash of the embedded prompt bodies.

## Triad integration

- **Evaluation datasets:** none yet — planned: an authorized, de-identified federal cooperative agreement with multi-year incremental funding and a structured reporting table.
- **Harness notes:** the seven-task runtime is not identical to running the canonical full-document prompt in one shot. Harness campaigns that score the component prompt directly are still the primary signal for the contract, but workflow-level scoring (post-consolidation JSON) is the right signal for the v0.1.0 runtime — record both when both are available.
- **Shared UDM relationship:** inherits from the `export-to-banner-extraction-udm` component's UDM alignment (broad bindings to `Award`, `Personnel`, `Organization`, `AwardBudget`, `AwardBudgetPeriod`, `IndirectRate`, `CostShare`, `ContactDetails`, `Terms`).

## Provenance

Authored 2026-05-20 alongside the initial `export-to-banner-extraction-udm` component, against `ui-insight/ProcessMapping` at commit `2c1f47f46474130743af5aee44d074bcd21787e9`. Built from the `PROC-EXPORT-TO-BANNER-REVIEW` source process map.
