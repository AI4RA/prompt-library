# FFR Management Extraction

Uploads a federal award notice or agreement and returns a single structured JSON object covering the five buckets a sponsored-programs analyst uses when preparing FFR (SF-425) submissions: submission schedule, submission system and procedures, required financial data, compliance consequences, and preparation timeline.

**Workflow version:** 0.1.0
**Vandalizer schema version:** 2
**Status:** experimental
**Components manifested:** `ffr-management-extraction-udm@0.1.0`
**Eval posture:** workflow-local — see [`evals/`](evals/)

## What this workflow does

The operator uploads a federal award notice or agreement into Vandalizer. The workflow runs as two steps:

**Step 1 — Extraction (1 Extraction task):**

| Task | Schema target | SearchSet items |
|---|---|---|
| `extract-ffr-management` | full schema | `award_number`, `pi_name`, `annual_ffr_due`, `final_ffr_due`, `interim_reporting`, `cash_transaction_reporting`, `submission_system_platform` (enum), `submission_system_access_requirements`, `era_commons_integration`, `submission_authorization`, `required_financial_data`, `late_submission_penalties`, `account_restrictions`, `impact_on_future_funding`, `required_documentation`, `preparation_timeline` |

**Step 2 — Consolidation (1 Prompt task):** `ffr-management-consolidation` collapses the flat searchset outputs into the schema's nested `submission_schedule`, `submission_system`, and `compliance_consequences` objects, normalizes the `submission_system.platform` enum, and ensures `preparation_timeline` is an array of `{milestone, days_before_period_end, action, owner}` objects only when the source document describes a countdown.

The runtime mirrors the source `ui-insight/ProcessMapping/workflows/ffr-management-extraction/` workflow one-for-one (the source's TASK-01 + Formatting becomes one Extraction + one Consolidation Prompt here).

## Components

- [`ffr-management-extraction-udm@0.1.0`](../../components/ffr-management-extraction-udm/) — the sole component. The Extraction task carries a focused `prompt_inline` body in [`manifest.yaml`](manifest.yaml); the canonical full-document prompt at [`components/ffr-management-extraction-udm/prompt.md`](../../components/ffr-management-extraction-udm/prompt.md) remains the single-call reference for harness invocations.

## Validation plan

Carried into the Vandalizer export at the workflow level (mirrors the source ProcessMapping `Validation_Plan`):

| Check | Type | Severity |
|---|---|---|
| `CHK-01` Date format checks | format | error |
| `CHK-02` Deadline consistency | consistency | warning |

## Eval posture

Workflow-local — see [`evals/`](evals/). The workflow is **not** a 1:1 repackaging of the canonical component prompt: the Extraction task carries a focused `prompt_inline` body and the Consolidation Prompt collapses flat searchset outputs into the schema's nested objects, so per [`docs/contracts.md`](../../docs/contracts.md) workflow-local cases are required to cover behavior that emerges from the two-task topology rather than the single-call surface.

Workflow-local cases should target the consolidator's flat-to-nested mapping (especially the `submission_system.platform` enum normalization), the `preparation_timeline` empty-array rule when no countdown is stated, and the two `validation_plan` checks. The component-level evals at [`components/ffr-management-extraction-udm/evals/`](../../components/ffr-management-extraction-udm/evals/) remain the right signal for the component contract itself; record both signals in harness campaigns when both are available.

## Building

Re-generate the Vandalizer export from `manifest.yaml`:

```bash
python3 scripts/build_vandalizer_workflows.py
```

CI fails when the committed `ffr-management-extraction.vandalizer.json` differs from a fresh build, so treat `manifest.yaml` as the source of truth and never hand-edit the generated JSON.

## Sharing

The committed `ffr-management-extraction.vandalizer.json` can be uploaded directly into Vandalizer via the workflow import UI. Its `x_ai4ra` block traces it back to this manifest, the pinned component version, and the content hash of the embedded prompt body.

## Triad integration

- **Evaluation datasets:** none yet — planned: federal award notice case under the component's `evals/cases/`.
- **Harness notes:** the two-task runtime is **not** identical to running the canonical full-document prompt in one shot. Harness campaigns that score the component prompt directly are still the primary signal for the contract, but workflow-level scoring (post-consolidation JSON) is the right signal for the v0.1.0 runtime — record both when both are available.
- **Shared UDM relationship:** inherits from the `ffr-management-extraction-udm` component's UDM alignment (`award_number`, `pi_name` resolve to UDM `Award` and `Personnel`).

## Provenance

Authored 2026-04-30 alongside the initial `ffr-management-extraction-udm` component, to give the `ui-insight/ProcessMapping` FFR Management Extraction workflow a versioned, catalog-discoverable Vandalizer manifestation that can be regenerated from the prompt-library source rather than hand-built in the Vandalizer UI.
