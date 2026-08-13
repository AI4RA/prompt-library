# Proposal Document Completeness Checker

Uploads a proposal package (VERAS upload bundle, NSF or NIH proposal, plus the relevant solicitation) and returns a single structured JSON gap-analysis covering senior key personnel, budget personnel, subaward presence, the four per-person required documents, conditional requirements, and a prioritized list of missing items the analyst should ask the PI about.

**Workflow version:** 1.0.0
**Vandalizer schema version:** 2
**Status:** experimental
**Components manifested:** `proposal-document-completeness-udm@0.1.0`
**Eval posture:** workflow-local — see [`evals/`](evals/)

> **v1.0.0 (KB step removed):** the optional Knowledge Base lookup step was removed (MAJOR, 3 steps → 2) — it was inert on import (Vandalizer blanks `kb_uuid`). Extraction tasks now read the uploaded documents directly. Mirrors `rfa-checklist-extraction` v1.0.0. See the [CHANGELOG](CHANGELOG.md).

## What this workflow does

Two-step runtime mirroring the source `ui-insight/ProcessMapping/workflows/proposal-document-completeness/` workflow:

**Step 1 — Parallel Extraction (2 Extraction tasks):**

| Task | Schema target | SearchSet items |
|---|---|---|
| `extract-proposal-components` | as-found inventory | `uploaded_documents`, `senior_key_personnel`, `budget_personnel`, `has_postdocs_or_grad_students`, `has_subawards`, `subaward_documents_inventory`, `per_person_document_matrix_inventory`, `proposal_track_type`, `personnel_discrepancies` |
| `extract-sponsor-requirements` | sponsor requirements | `sponsor_name`, `rfa_foa_number`, `review_type` (enum), `required_documents_checklist`, `conditional_requirements`, `per_person_required_documents`, `subaward_required_documents` |

**Step 2 — Consolidation & Gap Analysis (1 Prompt task):** `proposal-document-completeness-consolidation` joins the two fragments, sets `present` booleans on the required-documents checklist, derives `triggered` flags on conditional requirements, computes the per-person `missing` lists, computes the per-subawardee `missing` lists, surfaces personnel discrepancies, and ranks `prioritized_missing` (compliance-critical first, then per-person, then conditional-triggered, then optional).

## Components

- [`proposal-document-completeness-udm@0.1.0`](../../components/proposal-document-completeness-udm/) — the sole component.

## Validation plan

| Check | Type | Severity |
|---|---|---|
| `CHK-01` Personnel list completeness | completeness | error |
| `CHK-02` Required documents coverage | completeness | error |
| `CHK-03` Per-person document verification | completeness | error |

## Eval posture

Workflow-local — see [`evals/`](evals/). The Consolidation Prompt does substantial work — it joins the as-found inventory with the sponsor requirements, derives `present` and `triggered` booleans, computes per-person and per-subawardee `missing` lists, and ranks `prioritized_missing` — so per [`docs/contracts.md`](../../docs/contracts.md) workflow-local cases are required.

## Building

```bash
python3 scripts/build_vandalizer_workflows.py
```

## Sharing

The committed `proposal-document-completeness.vandalizer.json` can be uploaded directly into Vandalizer via the workflow import UI.

## Triad integration

- **Evaluation datasets:** none yet — planned: cases at `components/proposal-document-completeness-udm/evals/cases/`.
- **Shared UDM relationship:** inherits from the component's UDM alignment (Proposal, Personnel, Sponsor_Organization, Subaward).

## Provenance

Authored 2026-04-30 alongside the initial `proposal-document-completeness-udm` component, against `ui-insight/ProcessMapping` at commit `b7176b0c913833a205efdb5e4ba00c17ff88af0f`.
