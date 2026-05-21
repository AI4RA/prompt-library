# Award Modification Intake & Classification

Uploads a federal award amendment / modification document and returns a single structured JSON object covering the three blocks a Post-Award Specialist uses to enter the modification into Banner: identification (with seven-value modification-type classification), financial impact, and compliance.

**Workflow version:** 0.1.0
**Vandalizer schema version:** 2
**Status:** experimental
**Components manifested:** `award-modification-intake-udm@0.1.0`
**Eval posture:** workflow-local — see [`evals/`](evals/)

## What this workflow does

The operator uploads a federal award modification document (PDF, DOCX, or `.msg`) into Vandalizer. The workflow runs as two steps:

**Step 1 — Parallel Extraction (3 Extraction tasks):**

| Task | Schema target | SearchSet items |
|---|---|---|
| `extract-modification-type-identification` | `identification` block | `award_number`, `amendment_number`, `modification_type` (enum), `execution_status` (enum), `effective_date`, `sponsor_name`, `pi_name`, `old_pi`, `new_pi`, `new_end_date`, `pms_code`, `point_of_contact_changes` |
| `extract-financial-impact` | `financial` block | `modification_amount`, `current_award_amount`, `total_obligated_amount`, `fa_rate`, `fa_amount`, `budget_breakdown`, `rebudget_source_account`, `rebudget_destination_account`, `cost_share_changes` |
| `extract-compliance-requirements` | `compliance` block | `prior_approval_required`, `approval_date`, `sponsor_conditions`, `regulatory_references`, `end_date_change`, `requires_financial_unit`, `ibc_protocols_required` |

**Step 2 — Consolidation (1 Prompt task):** `award-modification-intake-consolidation` assembles the three JSON fragments into a single schema-conformant object, enforces the four cross-field rules (CFR-01..CFR-04 from the source `Cross_Field_Rules`), and converts any quoted dollar strings into JSON numbers.

The runtime mirrors the source `ui-insight/ProcessMapping/workflows/award-modification-intake/` workflow's Step 1 + Step 2. The source workflow's **Step 3 ApprovalNode** (Post-Award Specialist review before Banner entry) is omitted from this manifestation — operator review is handled by Vandalizer's UI and is not a contract concern.

## Components

- [`award-modification-intake-udm@0.1.0`](../../components/award-modification-intake-udm/) — the sole component. The three Extraction tasks carry focused `prompt_inline` bodies in [`manifest.yaml`](manifest.yaml); the canonical full-document prompt at [`components/award-modification-intake-udm/prompt.md`](../../components/award-modification-intake-udm/prompt.md) remains the single-call reference for harness invocations.

## Validation plan

Carried into the Vandalizer export at the workflow level (mirrors the source ProcessMapping `Validation_Plan`):

| Check | Type | Severity |
|---|---|---|
| `CHK-01` Modification type classification | completeness | error |
| `CHK-02` Amendment number format | format | error |
| `CHK-03` Monetary amount format | format | error |
| `CHK-04` Date validity | format | error |
| `CHK-05` Compliance requirements completeness | completeness | warning |

The four source `Cross_Field_Rules` (CFR-01..CFR-04) are enforced by the Consolidation Prompt as runtime flags rather than separate validation entries (see `manifest.yaml` for the exact rule text).

## Eval posture

Workflow-local — see [`evals/`](evals/). The workflow is **not** a 1:1 repackaging of the canonical component prompt: each Extraction task carries a focused `prompt_inline` body covering a single block, and the Consolidation Prompt assembles the three fragments and enforces the four cross-field rules, so per [`docs/contracts.md`](../../docs/contracts.md) workflow-local cases are required to cover behavior that emerges from the four-task topology rather than the single-call surface.

Workflow-local cases should target the seven-value `modification_type` enum coverage (one case per major type), the CFR-04 totals-reconciliation flag emission for additional-funds modifications, and the conditional population rules for `old_pi` / `new_pi` (PI Change) and `new_end_date` (NCE). The component-level evals at [`components/award-modification-intake-udm/evals/`](../../components/award-modification-intake-udm/evals/) remain the right signal for the component contract itself; record both signals in harness campaigns when both are available.

## Building

Re-generate the Vandalizer export from `manifest.yaml`:

```bash
python3 scripts/build_vandalizer_workflows.py
```

CI fails when the committed `award-modification-intake.vandalizer.json` differs from a fresh build, so treat `manifest.yaml` as the source of truth and never hand-edit the generated JSON.

## Sharing

The committed `award-modification-intake.vandalizer.json` can be uploaded directly into Vandalizer via the workflow import UI. Its `x_ai4ra` block traces it back to this manifest, the pinned component version, and the content hash of the embedded prompt bodies.

## Triad integration

- **Evaluation datasets:** none yet — planned: representative additional-funds, NCE, PI-change, and rebudget modifications under the component's `evals/cases/`.
- **Harness notes:** the four-task runtime is not identical to running the canonical full-document prompt in one shot. Harness campaigns that score the component prompt directly are still the primary signal for the contract, but workflow-level scoring (post-consolidation JSON) is the right signal for the v0.1.0 runtime — record both when both are available.
- **Shared UDM relationship:** inherits from the `award-modification-intake-udm` component's UDM alignment (`award_number` to `Award`; `pi_name` to `Personnel`; `modification_amount` to `Modification.Funding_Amount_Change`; `current_award_amount` to `Award.Current_Total_Funded`; `budget_breakdown` to `AwardBudget`; `prior_approval_required` to `Modification.Requires_Prior_Approval`).

## Provenance

Authored 2026-05-20 alongside the initial `award-modification-intake-udm` component, against `ui-insight/ProcessMapping` at commit `2c1f47f46474130743af5aee44d074bcd21787e9`. The source workflow's STEP-03 ApprovalNode is omitted from the Vandalizer manifestation as a runtime UI concern.
