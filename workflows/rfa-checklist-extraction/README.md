# RFA Checklist Extraction

Uploads a federal funding announcement (RFA / FOA / NOFO / program solicitation) and returns a single structured JSON object covering the eight pre-award checklist sections: dates and deadlines, eligible institutions, eligible individuals, award information, required and optional application components, budget requirements and policies, submission details, special requirements, and important notes. A downstream consolidation step (not part of this workflow) can render the JSON to the eight-section markdown deliverable used by sponsored-programs offices.

**Workflow version:** 0.2.0
**Vandalizer schema version:** 2
**Status:** experimental
**Components manifested:** `rfa-checklist-extraction-udm@0.1.0`
**Eval posture:** inherited from [`components/rfa-checklist-extraction-udm/evals`](../../components/rfa-checklist-extraction-udm/evals/)

## What this workflow does

The operator uploads a funding announcement into Vandalizer (PDF, DOCX, or HTML). The workflow runs as two steps:

**Step 1 — Parallel Extraction (7 Extraction tasks):**

| Task | Schema target | SearchSet items |
|---|---|---|
| `extract-opportunity-metadata` | scalar opportunity fields | `rfa_id`, `rfa_number`, `rfa_title`, `sponsor_name`, `program_code`, `announcement_url`, `opportunity_number`, `cfda_number` |
| `extract-dates-and-deadlines` | `dates_and_deadlines` | `dates_and_deadlines` (JSON array of `{item, date_time, notes}`) |
| `extract-eligible-institutions` | `eligible_institutions` | `eligible_institutions` (JSON array of `{type, subcategory, examples, compliance_requirements}`) |
| `extract-eligible-individuals` | `eligible_individuals` | `eligible_individuals` (JSON array of `{type, criteria, compliance_requirements, conditions}`) |
| `extract-award-information` | `award_information` | `award_duration`, `amount_per_award`, `number_of_awards`, `anticipated_award_date` |
| `extract-application-components` | `required_components`, `optional_components`, `submission_details`, `special_requirements` | the same four fields |
| `extract-budget-requirements` | `budget_requirements` | `funding_limits`, `cost_sharing_status` (enum), `cost_sharing_details`, `fa_policy`, `allowable_costs`, `unallowable_costs`, `personnel_effort`, `other_considerations` |

**Step 2 — Consolidation (1 Prompt task):** `rfa-checklist-consolidation` assembles the seven JSON fragments into a single object that validates against the component's [`schema.json`](../../components/rfa-checklist-extraction-udm/schema.json), enforces the placement contract (award amount only in `award_information`, detailed financial rules only in `budget_requirements`), maps the flat `cost_sharing_status` / `cost_sharing_details` extraction fields into the schema's nested `cost_sharing: {status, details}` object, and synthesizes the `important_notes` array from cross-section signals.

The runtime mirrors the source `ui-insight/ProcessMapping/workflows/rfa-checklist-extraction/` workflow one-for-one for the six logical sections, plus a seventh metadata Extraction task that covers the UDM-aligned scalar opportunity fields the component schema adds on top of that source workflow.

## Components

- [`rfa-checklist-extraction-udm@0.1.0`](../../components/rfa-checklist-extraction-udm/) — the sole component. The workflow does not slice the canonical full-document prompt; each Extraction task carries a focused per-section `prompt_inline` body in [`manifest.yaml`](manifest.yaml). The canonical component prompt at [`components/rfa-checklist-extraction-udm/prompt.md`](../../components/rfa-checklist-extraction-udm/prompt.md) remains the single-call reference for harness invocations and for runtimes that prefer one large extraction.

## Validation plan

Carried into the Vandalizer export at the workflow level (mirrors the source ProcessMapping `Validation_Plan`):

| Check | Type | Severity |
|---|---|---|
| `CHK-01` Date format consistency | format | error |
| `CHK-02` Monetary amount validation | format | error |
| `CHK-03` Eligibility criteria completeness | completeness | warning |
| `CHK-04` De-duplication validation | consistency | info |

## Eval posture

Evals inherit from [`components/rfa-checklist-extraction-udm/evals`](../../components/rfa-checklist-extraction-udm/evals/) because the consolidation prompt is constructed to emit the same schema-conformant object as the canonical component prompt. No workflow-local cases are required at the v0.2.0 boundary; workflow-local cases will be added when the seven-step topology starts to drift from the canonical prompt's output behavior.

## Building

Re-generate the Vandalizer export from `manifest.yaml`:

```bash
python3 scripts/build_vandalizer_workflows.py
```

CI fails when the committed `rfa-checklist-extraction.vandalizer.json` differs from a fresh build, so treat `manifest.yaml` as the source of truth and never hand-edit the generated JSON.

## Sharing

The committed `rfa-checklist-extraction.vandalizer.json` can be uploaded directly into Vandalizer via the workflow import UI. Its `x_ai4ra` block traces it back to this manifest, the pinned component version, and the content hash of the embedded prompt body.

## Triad integration

- **Evaluation datasets:** none yet — planned: NSF multi-round solicitation case under the component's `evals/cases/`.
- **Harness notes:** the seven Extraction-task runtime is **not** identical to running the canonical full-document prompt in one shot. Harness campaigns that score the component prompt directly are still the primary signal for the contract, but workflow-level scoring (post-consolidation JSON) is the right signal for the v0.2.0 runtime — record both when both are available.
- **Shared UDM relationship:** inherits from the `rfa-checklist-extraction-udm` component's UDM alignment (scalar metadata + UDM-column leaf bindings for `cost_sharing`, `fa_policy`, `personnel_effort`).

## Provenance

Authored 2026-04-24 alongside the initial `rfa-checklist-extraction-udm` component, to give the `ui-insight/ProcessMapping` RFA checklist workflow a versioned, catalog-discoverable Vandalizer manifestation that can be regenerated from the prompt-library source rather than hand-built in the Vandalizer UI. Bumped to v0.2.0 the same day to replace the initial Prompt-only runtime with the seven-task Extraction-plus-Consolidation topology that mirrors the source ProcessMapping workflow.
