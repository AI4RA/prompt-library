# Prior Approval Extraction

Uploads a federal award notice or agreement and returns a single structured JSON object covering all prior-approval requirements: budget-related approvals, scope and timeline approvals, a normalized approval-procedures table, and any Research Terms and Conditions waivers.

**Workflow version:** 1.0.0
**Vandalizer schema version:** 2
**Status:** experimental
**Components manifested:** `prior-approval-extraction-udm@0.1.0`
**Eval posture:** workflow-local — see [`evals/`](evals/)

> **v1.0.0 (KB step removed):** the optional Knowledge Base lookup step was removed (MAJOR, 3 steps → 2) — it was inert on import (Vandalizer blanks `kb_uuid`). Extraction tasks now read the uploaded documents directly. Mirrors `rfa-checklist-extraction` v1.0.0. See the [CHANGELOG](CHANGELOG.md).

## What this workflow does

The operator uploads a federal award notice or agreement into Vandalizer. The workflow runs as two steps:

**Step 1 — Extraction (1 Extraction task):**

| Task | Schema target | SearchSet items |
|---|---|---|
| `extract-prior-approvals` | full schema | `award_number`, `rebudgeting_thresholds`, `equipment_approvals`, `subaward_approvals`, `pi_change_requirements`, `nce_requirements`, `foreign_travel_approvals`, `approval_procedures`, `rtc_waivers` |

**Step 2 — Consolidation (1 Prompt task):** `prior-approval-consolidation` collapses the flat searchset outputs into the schema's nested `budget_approvals` and `scope_timeline_approvals` objects, normalizes the `approval_procedures` table into per-row objects, and ensures `rtc_waivers` is a flat list of waived approvals only (not kept approvals).

The runtime mirrors the source `ui-insight/ProcessMapping/workflows/prior-approval-extraction/` workflow one-for-one.

## Components

- [`prior-approval-extraction-udm@0.1.0`](../../components/prior-approval-extraction-udm/) — the sole component. The Extraction task carries a focused `prompt_inline` body in [`manifest.yaml`](manifest.yaml); the canonical full-document prompt at [`components/prior-approval-extraction-udm/prompt.md`](../../components/prior-approval-extraction-udm/prompt.md) remains the single-call reference for harness invocations.

## Validation plan

Carried into the Vandalizer export at the workflow level (mirrors the source ProcessMapping `Validation_Plan`):

| Check | Type | Severity |
|---|---|---|
| `CHK-01` Threshold format validation | format | warning |
| `CHK-02` Approval procedure completeness | completeness | warning |

## Eval posture

Workflow-local — see [`evals/`](evals/). The workflow is **not** a 1:1 repackaging of the canonical component prompt: the Extraction task carries a focused `prompt_inline` body and the Consolidation Prompt collapses flat outputs into the schema's nested objects, so per [`docs/contracts.md`](../../docs/contracts.md) workflow-local cases are required to cover behavior that emerges from the two-task topology rather than the single-call surface.

## Building

Re-generate the Vandalizer export from `manifest.yaml`:

```bash
python3 scripts/build_vandalizer_workflows.py
```

## Sharing

The committed `prior-approval-extraction.vandalizer.json` can be uploaded directly into Vandalizer via the workflow import UI. Its `x_ai4ra` block traces it back to this manifest, the pinned component version, and the content hash of the embedded prompt body.

## Triad integration

- **Evaluation datasets:** none yet — planned: federal award notice cases under the component's `evals/cases/`.
- **Harness notes:** the two-task runtime is **not** identical to running the canonical full-document prompt in one shot. Record both single-call and post-consolidation signals when both are available.
- **Shared UDM relationship:** inherits from the `prior-approval-extraction-udm` component's UDM alignment (per-row entries resolve to UDM `Modification.Requires_Prior_Approval`; `subaward_approvals` resolves to `Subaward`).

## Provenance

Authored 2026-04-30 alongside the initial `prior-approval-extraction-udm` component, to give the `ui-insight/ProcessMapping` Prior Approval Extraction workflow a versioned, catalog-discoverable Vandalizer manifestation, against `ui-insight/ProcessMapping` at commit `b7176b0c913833a205efdb5e4ba00c17ff88af0f`.
