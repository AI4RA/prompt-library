# Proposal Budget Personnel & Compliance Requirements Extraction

Uploads a proposal budget document (NSF-style budget tables / NIH PHS 398 / agency budget form) and returns a single structured JSON object covering personnel identification (senior key, postdocs, grad students, undergraduates, other personnel) and budget structure compliance triggers (subaward recipients, equipment over $5,000, F&A rate and base, cost sharing, total costs).

**Workflow version:** 0.1.0
**Vandalizer schema version:** 2
**Status:** experimental
**Components manifested:** `proposal-budget-personnel-extraction-udm@0.1.0`
**Eval posture:** workflow-local — see [`evals/`](evals/)

## What this workflow does

Two-step runtime mirroring the source `ui-insight/ProcessMapping/workflows/proposal-budget-personnel-extraction/` workflow:

**Step 1 — Parallel Extraction (2 Extraction tasks):**

| Task | Schema target | SearchSet items |
|---|---|---|
| `extract-personnel-identification` | personnel listings | `senior_key_personnel`, `postdoc_count`, `postdoc_details`, `graduate_student_count`, `graduate_student_details`, `undergraduate_count`, `other_personnel`, `total_personnel_cost` |
| `extract-budget-structure-and-compliance-triggers` | budget structure | `budget_categories`, `subaward_recipients`, `equipment_items`, `travel_summary`, `fa_rate`, `fa_base` (enum), `cost_sharing`, `total_costs`, `budget_periods` |

**Step 2 — Consolidation (1 Prompt task):** `budget-personnel-consolidation` assembles the two fragments, **derives** the four boolean triggers (`has_postdocs_or_grad_students`, `mentoring_plan_required`, `has_subawards`, `has_equipment_over_5k`) from list lengths, combines `fa_rate` + `fa_base` into the nested `fa_rate_and_base` object, and verifies cost-totals reconciliation.

## Components

- [`proposal-budget-personnel-extraction-udm@0.1.0`](../../components/proposal-budget-personnel-extraction-udm/) — the sole component.

## Validation plan

| Check | Type | Severity |
|---|---|---|
| `CHK-01` Personnel count consistency | consistency | warning |
| `CHK-02` Boolean flag derivation | consistency | warning |
| `CHK-03` Cost totals validation | arithmetic | error |

## Eval posture

Workflow-local — see [`evals/`](evals/). The Consolidation Prompt **derives** the four boolean compliance triggers from list lengths — that derivation is the workflow's primary value-add and the workflow-local cases must verify it.

## Building

```bash
python3 scripts/build_vandalizer_workflows.py
```

## Sharing

The committed `proposal-budget-personnel-extraction.vandalizer.json` can be uploaded directly into Vandalizer via the workflow import UI.

## Triad integration

- **Evaluation datasets:** none yet — planned: cases at `components/proposal-budget-personnel-extraction-udm/evals/cases/`.
- **Shared UDM relationship:** inherits from the component's UDM alignment (Personnel, IndirectRate, CostShare).
- **Pairs with:** `proposal-document-completeness` workflow consumes the four derived booleans.

## Provenance

Authored 2026-04-30 alongside the initial `proposal-budget-personnel-extraction-udm` component, against `ui-insight/ProcessMapping` at commit `b7176b0c913833a205efdb5e4ba00c17ff88af0f`.
