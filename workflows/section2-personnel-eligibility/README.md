# Section 2 Personnel Eligibility Verification

Uploads a VERAS proposal together with the Banner NBAJOBS extract for each person and the institutional Department List, and returns a verification matrix with per-person APM 45.22 eligibility determinations, per-org-code DGA mappings, and flags for ineligible personnel and missing DGAs.

**Workflow version:** 1.0.0
**Vandalizer schema version:** 2
**Status:** experimental
**Components manifested:** `section2-personnel-eligibility-udm@0.1.0`
**Eval posture:** workflow-local — see [`evals/`](evals/)

> **v1.0.0 (KB step removed):** the optional Knowledge Base lookup step was removed (MAJOR, 3 steps → 2) — it was inert on import (Vandalizer blanks `kb_uuid`). Extraction tasks now read the uploaded documents directly. Mirrors `rfa-checklist-extraction` v1.0.0. See the [CHANGELOG](CHANGELOG.md).

## What this workflow does

The operator uploads three documents together into Vandalizer:

1. The VERAS proposal package (PDF, DOCX, or CSV-exported Sections 2.1 and 2.2A),
2. The Banner NBAJOBS extract for every person on the proposal (export, CSV, or PDF), and
3. The institutional Department List (org-code → department → DGA mapping, typically XLSX or CSV).

The APM 45.22 eligible-titles list is applied during the eligibility determination. As of v1.0.0 the inert `KnowledgeBaseQuery` step was removed, so until KBs are reintroduced the APM 45.22 list should be supplied as an uploaded reference document alongside the other inputs.

The workflow runs as two steps:

**Step 1 — Parallel Extraction (2 Extraction tasks):**

| Task | Schema target | SearchSet items |
|---|---|---|
| `extract-section-2-personnel` | `personnel_extraction` | `section_21_personnel`, `section_22_personnel`, `total_personnel_count`, `pi_copis_requiring_eligibility`, `personnel_requiring_org_code_only` |
| `extract-eligibility-and-dga-verification` | `personnel_verification` + `eligibility_check` + `org_code_compilation` + `dga_mapping` + `dga_cross_reference` | `personnel_verification`, `eligibility_check`, `org_code_compilation`, `dga_mapping`, `dga_cross_reference`, `notes_about_missing_sources` |

**Step 2 — Consolidation (1 Prompt task):** `section2-personnel-eligibility-consolidation` assembles the two JSON fragments into the schema-conformant seven-block object, derives `verification_summary` counts and flag arrays from the per-person / per-org-code / per-DGA records, and enforces the three cross-field rules from the source workflow (every PI / Co-PI has an eligibility determination; every unique org code has a `dga_mapping` row; every DGA pulled from `dga_mapping` is cross-referenced).

The runtime mirrors the source `ui-insight/ProcessMapping/workflows/section2-personnel-eligibility/` workflow one-for-one.

## Components

- [`section2-personnel-eligibility-udm@0.1.0`](../../components/section2-personnel-eligibility-udm/) — the sole component. The two Extraction tasks carry focused `prompt_inline` bodies in [`manifest.yaml`](manifest.yaml); the canonical full-document prompt at [`components/section2-personnel-eligibility-udm/prompt.md`](../../components/section2-personnel-eligibility-udm/prompt.md) remains the single-call reference for harness invocations.

## Input model — three workflow documents

This is the second of two pre-award compliance ports that require multiple input documents uploaded together (the other is `compliance-personnel-verification`). The Banner NBAJOBS extract and the Department List are not retrieved by API calls from inside Vandalizer; the operator must include them in the same workflow run as the VERAS proposal. When any of the three is missing:

- The contract emits non-compliant defaults (`found_in_banner: false`, `eligibility_status: "Review Required"`, empty `dga_names`, populated `unmapped_org_codes`).
- `verification_summary.notes` carries a single-string description of the gap.
- The operator decides whether to re-run the workflow with the missing source or proceed with the partial result.

## Validation plan

Carried into the Vandalizer export at the workflow level (mirrors the source ProcessMapping `Validation_Plan`):

| Check | Type | Severity |
|---|---|---|
| `CHK-01` Personnel extraction completeness | completeness | error |
| `CHK-02` Eligibility check completeness | completeness | error |
| `CHK-03` Org code extraction completeness | completeness | error |
| `CHK-04` DGA mapping completeness | completeness | error |

The three source `Cross_Field_Rules` (CFR-01..CFR-03) are enforced by the Consolidation Prompt at runtime — see `manifest.yaml` for the exact derivation logic.

## Eval posture

Workflow-local — see [`evals/`](evals/). The workflow is **not** a 1:1 repackaging of the canonical component prompt: each Extraction task carries a focused `prompt_inline` body covering a different source-document subset, and the Consolidation Prompt derives the seven `verification_summary` counts and four flag arrays from the per-person / per-org-code / per-DGA records, so per [`docs/contracts.md`](../../docs/contracts.md) workflow-local cases are required to cover behavior that emerges from the three-task topology.

Workflow-local cases should target the three-value `eligibility_status` enum coverage, the two-value `action_needed` enum coverage, the unmapped-org-code path (`department_name: null`), the missing-DGA path (`missing_dgas` populated), and the missing-source-document gap-flagging path. The component-level evals at [`components/section2-personnel-eligibility-udm/evals/`](../../components/section2-personnel-eligibility-udm/evals/) remain the right signal for the component contract itself; record both signals in harness campaigns when both are available.

## Building

Re-generate the Vandalizer export from `manifest.yaml`:

```bash
python3 scripts/build_vandalizer_workflows.py
```

CI fails when the committed `section2-personnel-eligibility.vandalizer.json` differs from a fresh build, so treat `manifest.yaml` as the source of truth and never hand-edit the generated JSON.

## Sharing

The committed `section2-personnel-eligibility.vandalizer.json` can be uploaded directly into Vandalizer via the workflow import UI. Its `x_ai4ra` block traces it back to this manifest, the pinned component version, and the content hash of the embedded prompt bodies.

## Triad integration

- **Evaluation datasets:** none yet — planned: a synthetic UI proposal exercise with three PI / Co-PI personnel of mixed APM 45.22 eligibility and at least one missing DGA.
- **Harness notes:** the three-document input model means the harness needs a workflow runner that can pass multiple workflow documents simultaneously. Score post-consolidation JSON against the schema; track `verification_summary.notes` for missing-source warnings.
- **Shared UDM relationship:** inherits from the `section2-personnel-eligibility-udm` component's UDM alignment (personnel names resolve to UDM `Personnel`; the eligibility / DGA mapping surfaces are repo-local).

## Provenance

Authored 2026-05-20 alongside the initial `section2-personnel-eligibility-udm` component, against `ui-insight/ProcessMapping` at commit `2c1f47f46474130743af5aee44d074bcd21787e9`. Built from the `PROC-SPA-SECTION2-REVIEW` source process map; created explicitly in response to Michele Mattoon's request for an APM 45.22 auto-check.
