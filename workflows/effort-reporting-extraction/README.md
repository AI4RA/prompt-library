# Effort Reporting Compliance Extraction

Uploads a federal award notice or agreement and returns a single structured JSON object covering effort-reporting and personnel-compliance requirements: cadence, certification method (per 2 CFR 200.430(i)), PI commitments, per-person key-personnel commitments, cost-shared effort, governing regulation, record-retention requirement, and referenced governing documents.

**Workflow version:** 0.1.0
**Vandalizer schema version:** 2
**Status:** experimental
**Components manifested:** `effort-reporting-extraction-udm@0.1.0`
**Eval posture:** workflow-local — see [`evals/`](evals/)

## What this workflow does

Two-step runtime mirroring the source `ui-insight/ProcessMapping/workflows/effort-reporting-extraction/` workflow:

**Step 1 — Extraction (1 Extraction task):** `extract-effort-compliance` carries an embedded SearchSet whose item titles mirror the schema field names; `reporting_frequency` and `certification_method` carry their enums.

**Step 2 — Consolidation (1 Prompt task):** `effort-compliance-consolidation` assembles the JSON fragment into the schema-conformant object, normalizes the two enums, and ensures the PI's row in `key_personnel_commitments` mirrors `pi_committed_effort` and `pi_person_months` exactly.

## Components

- [`effort-reporting-extraction-udm@0.1.0`](../../components/effort-reporting-extraction-udm/) — the sole component.

## Validation plan

| Check | Type | Severity |
|---|---|---|
| `CHK-01` Effort percentages sum | arithmetic | error |
| `CHK-02` Person-months consistency | consistency | warning |
| `CHK-03` Personnel table completeness | completeness | warning |

## Eval posture

Workflow-local — see [`evals/`](evals/). The workflow is **not** a 1:1 repackaging of the canonical component prompt; the Consolidation Prompt enforces the PI-mirror rule across `pi_committed_effort` / `pi_person_months` / `key_personnel_commitments` and normalizes the two enums, so per [`docs/contracts.md`](../../docs/contracts.md) workflow-local cases are required.

## Building

```bash
python3 scripts/build_vandalizer_workflows.py
```

## Sharing

The committed `effort-reporting-extraction.vandalizer.json` can be uploaded directly into Vandalizer via the workflow import UI.

## Triad integration

- **Evaluation datasets:** none yet — planned: federal award notice cases under the component's `evals/cases/`.
- **Shared UDM relationship:** inherits from the `effort-reporting-extraction-udm` component's UDM alignment (Award, Personnel, Effort, ProjectRole, CostShare, Terms).

## Provenance

Authored 2026-04-30 alongside the initial `effort-reporting-extraction-udm` component, against `ui-insight/ProcessMapping` at commit `b7176b0c913833a205efdb5e4ba00c17ff88af0f`.
