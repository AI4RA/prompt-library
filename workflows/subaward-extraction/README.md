# Subaward Agreement Extraction

Uploads a fully executed subaward agreement (Pass-Through Entity → Subrecipient) and returns a single structured JSON object covering nine sections used for research-administration setup and ongoing monitoring.

**Workflow version:** 1.0.0
**Vandalizer schema version:** 2
**Status:** experimental
**Components manifested:** `subaward-extraction-udm@0.1.0`
**Eval posture:** workflow-local — see [`evals/`](evals/)

> **v1.0.0 (KB step removed):** the optional Knowledge Base lookup step was removed (MAJOR, 3 steps → 2) — it was inert on import (Vandalizer blanks `kb_uuid`). Extraction tasks now read the uploaded documents directly. Mirrors `rfa-checklist-extraction` v1.0.0. See the [CHANGELOG](CHANGELOG.md).

## What this workflow does

Two-step runtime mirroring the source `ui-insight/ProcessMapping/workflows/subaward-extraction/` workflow:

**Step 1 — Parallel Extraction (6 Extraction tasks):**

| Task | Source counterpart | Schema target |
|---|---|---|
| `extract-core-award-information` | TASK-01 | core block (6 fields) |
| `extract-contact-information` | TASK-02 | six contact fields exposed as 18 flat searchset items (3 per contact) |
| `extract-dates-and-monetary-values` | TASK-03 | dates & monetary block (6 fields, `cost_type` enum) |
| `extract-financial-policies` | TASK-04 | financial policies block (6 fields, `invoicing_frequency` enum) |
| `extract-reporting-requirements` | TASK-05 | three typed report arrays |
| `extract-compliance-requirements` | TASK-06 | compliance block (7 fields, `governing_regulations` required) |

**Step 2 — Consolidation (1 Prompt task):** `subaward-summary-consolidation` composes the 18 flat contact items into six `{name, email, phone}` objects, normalizes the two enums (`cost_type`, `invoicing_frequency`), and verifies the CFR-01 reconciliation between `amount_funded`, `total_direct_costs`, and `total_indirect_costs`.

## Components

- [`subaward-extraction-udm@0.1.0`](../../components/subaward-extraction-udm/) — the sole component.

## Validation plan

| Check | Type | Severity |
|---|---|---|
| `CHK-01` Monetary cross-reference | arithmetic | error |
| `CHK-02` Date consistency | consistency | error |
| `CHK-03` Contact info format | format | warning |

## Eval posture

Workflow-local — see [`evals/`](evals/). The Consolidation Prompt does substantial work — it composes 18 flat contact searchset items into six structured `{name, email, phone}` objects, normalizes the two enums, and enforces the CFR-01 reconciliation — emergent behavior the component-level evals cannot cover.

## Building

```bash
python3 scripts/build_vandalizer_workflows.py
```

## Sharing

The committed `subaward-extraction.vandalizer.json` can be uploaded directly into Vandalizer via the workflow import UI.

## Triad integration

- **Evaluation datasets:** none yet — planned: cases at `components/subaward-extraction-udm/evals/cases/`.
- **Shared UDM relationship:** inherits from the component's broad UDM alignment (Award, Subaward, Organization, Personnel, ContactDetails, IndirectRate, CostShare, AwardDeliverable, Modification, Terms, ConflictOfInterest).

## Provenance

Authored 2026-04-30 alongside the initial `subaward-extraction-udm` component, against `ui-insight/ProcessMapping` at commit `b7176b0c913833a205efdb5e4ba00c17ff88af0f`.
