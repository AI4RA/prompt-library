# Budget Justification Generator

Uploads a grant budget form, the project narrative, and optionally the funding opportunity announcement (NOFO / RFA), and returns a single structured JSON object capturing both the per-section extracted financial data AND the generated narrative text for each section, plus the final assembled Markdown document organized in R&R Budget / SF-424A category order (A through I).

**Workflow version:** 0.1.0
**Vandalizer schema version:** 2
**Status:** experimental
**Components manifested:** `budget-justification-generator-udm@0.1.0`
**Eval posture:** workflow-local — see [`evals/`](evals/)

## What this workflow does

This is a **drafting workflow** (not extraction). The operator uploads three documents together into Vandalizer:

1. The budget form (R&R Budget Form, SF-424A, or Excel).
2. The project narrative / research plan.
3. Optionally the NOFO / RFA for agency-specific formatting rules and F&A caps.

The workflow runs as two steps:

**Step 1 — Parallel Extraction + Generation (4 Extraction tasks):** Each task both extracts the structured budget data AND generates the professional narrative text for its assigned sections.

| Task | Schema target | Sections covered |
|---|---|---|
| `extract-personnel-and-fringe` | `personnel_and_fringe` | A (Senior/Key Personnel), B (Other Personnel), C (Fringe Benefits) |
| `extract-equipment-and-travel` | `equipment_and_travel` | D (Equipment), E (Travel: Domestic + Foreign) |
| `extract-participant-support-and-odc` | `participant_support_and_other_direct_costs` | F (Participant Support), G (Other Direct Costs, subcategories G.1–G.9) |
| `extract-indirect-and-summary` | `indirect_costs_and_summary` | H (Indirect Costs / F&A), Cost Sharing, Budget Summary |

**Step 2 — Consolidation + Cross-Validation + Document Assembly (1 Prompt task):** `budget-justification-generator-consolidation` assembles the four JSON fragments into the schema-conformant seven-block object, computes the four arithmetic checks (Personnel & Fringe subtotal; Non-personnel direct subtotal; Total Direct Costs; Total Project Costs), aggregates the items-requiring-clarification list, identifies missing-justification flags, and renders `final_justification_document` as a single Markdown string in R&R Budget / SF-424A category order with the cross-validation notes section clearly marked as not-for-submission.

The runtime mirrors the source `ui-insight/ProcessMapping/workflows/budget-justification-generator/` workflow's TASK-1-1 through TASK-1-4 + Consolidation one-for-one.

## Components

- [`budget-justification-generator-udm@0.1.0`](../../components/budget-justification-generator-udm/) — the sole component. The four Extraction tasks carry focused `prompt_inline` bodies in [`manifest.yaml`](manifest.yaml); the canonical full-document prompt at [`components/budget-justification-generator-udm/prompt.md`](../../components/budget-justification-generator-udm/prompt.md) remains the single-call reference.

## Validation plan

Carried into the Vandalizer export at the workflow level (mirrors the source ProcessMapping `Validation_Plan`):

| Check | Type | Severity |
|---|---|---|
| `CHK-01` Line item sum equals category total | arithmetic | error |
| `CHK-02` Direct plus indirect equals total | arithmetic | error |
| `CHK-03` Personnel costs match FTE | consistency | warning |

The source `Cross_Field_Rules` (CFR-01 `total_direct + total_indirect = total_project`) is enforced by the Consolidation Prompt's arithmetic-check generation and surfaces in `cross_validation.arithmetic_checks` with `status: "FAIL"` and populated discrepancy values when violated.

## Eval posture

Workflow-local — see [`evals/`](evals/). The workflow is **not** a 1:1 repackaging of the canonical component prompt: each Extraction task does both data extraction AND narrative generation, and the Consolidation Prompt computes four arithmetic checks deterministically and renders the final Markdown document. The workflow's behavior emerges from step interactions that no component-level eval can cover on its own.

Workflow-local cases should target the four arithmetic checks (including FAIL cases that exercise the no-alter-values rule), the multi-year `budget_period_summary` table population, the `FORMATTING ADVISORY` block emission when the NOFO specifies page limits, the empty-section narrative defaults (`"No <category> costs are requested..."`), and the cross-validation notes placement (below the main narrative, marked as not-for-submission).

## Building

Re-generate the Vandalizer export from `manifest.yaml`:

```bash
python3 scripts/build_vandalizer_workflows.py
```

CI fails when the committed `budget-justification-generator.vandalizer.json` differs from a fresh build.

## Sharing

The committed `budget-justification-generator.vandalizer.json` can be uploaded directly into Vandalizer via the workflow import UI. Its `x_ai4ra` block traces it back to this manifest, the pinned component version, and the content hash of the embedded prompt bodies.

## Triad integration

- **Evaluation datasets:** none yet — planned: a synthetic R&R Budget + project narrative exercise (multi-year, with cost-sharing, mixed-PI structure) validated by a Pre-Award Analyst end-to-end.
- **Harness notes:** scoring is two-layered. Structured fields (numeric totals, table rows, arithmetic_checks results) validate against `schema.json`. Narrative strings (section narratives + `final_justification_document`) require human review; golden cases should capture validated narrative text for diff-based scoring.
- **Shared UDM relationship:** inherits from the `budget-justification-generator-udm` component's UDM alignment (Personnel, Proposal, ProposalBudget, IndirectRate, CostShare, Organization via leaf fields; the seven-block drafting shape is repo-local).

## Provenance

Authored 2026-05-20 alongside the initial `budget-justification-generator-udm` component, against `ui-insight/ProcessMapping` at commit `2c1f47f46474130743af5aee44d074bcd21787e9`. This is a drafting workflow (rather than a single-process extraction); it does not map to a single `processes/` map and was built to automate the budget-justification drafting step.
