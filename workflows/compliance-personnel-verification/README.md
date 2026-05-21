# Compliance Personnel Verification (SFI & RST)

Uploads a VERAS proposal package together with the institutional SFI disclosure records and the most recent daily RST completion spreadsheet, and returns a per-person compliance matrix with non-compliance priorities and overall summary counts.

**Workflow version:** 0.1.0
**Vandalizer schema version:** 2
**Status:** experimental
**Components manifested:** `compliance-personnel-verification-udm@0.1.0`
**Eval posture:** workflow-local — see [`evals/`](evals/)

## What this workflow does

The operator uploads three documents together into Vandalizer:

1. The VERAS proposal package (PDF, DOCX, or CSV-exported sections),
2. The institutional SFI disclosure records (PDF, XLSX, or `.msg` correspondence), and
3. The most recent daily RST completion spreadsheet (XLSX or CSV).

The workflow runs as two steps:

**Step 1 — Parallel Extraction (2 Extraction tasks):**

| Task | Schema target | SearchSet items |
|---|---|---|
| `extract-personnel-identification` | `proposal_metadata` + `personnel_identification` | `section_66_personnel`, `section_2_personnel`, `consolidated_personnel`, `proposal_type` (enum), `sponsor_type` (enum), `sfi_rst_required`, `personnel_discrepancies` |
| `extract-compliance-status` | `sfi_verification` + `rst_verification` | `sfi_verification`, `rst_spreadsheet_date`, `rst_spreadsheet_source`, `rst_records`, `notes_about_missing_sources` |

**Step 2 — Consolidation (1 Prompt task):** `compliance-personnel-verification-consolidation` assembles the two JSON fragments into the schema-conformant six-block object, derives `non_compliant_personnel` and `verification_status` from the per-person SFI / RST status records, and enforces the no-assumption-of-compliance rule (missing source documents produce `"Not Found"` / `"Incomplete"` defaults plus a `verification_status.notes` gap-flag, never silent compliance).

The runtime mirrors the source `ui-insight/ProcessMapping/workflows/compliance-personnel-verification/` workflow one-for-one.

## Components

- [`compliance-personnel-verification-udm@0.1.0`](../../components/compliance-personnel-verification-udm/) — the sole component. The two Extraction tasks carry focused `prompt_inline` bodies in [`manifest.yaml`](manifest.yaml); the canonical full-document prompt at [`components/compliance-personnel-verification-udm/prompt.md`](../../components/compliance-personnel-verification-udm/prompt.md) remains the single-call reference for harness invocations.

## Input model — three workflow documents

This workflow is one of two pre-award compliance ports that require **multiple input documents** uploaded together. The SFI records and RST spreadsheet are not retrieved by API calls from inside Vandalizer; the operator must include them in the same workflow run as the VERAS proposal. When any of the three sources is missing:

- The contract emits non-compliant defaults (`"Not Found"` / `"Incomplete"`) rather than silently assuming compliance.
- `verification_status.notes` carries a single-string description of the gap.
- The operator decides whether to re-run the workflow with the missing source or proceed with the partial result.

## Validation plan

Carried into the Vandalizer export at the workflow level (mirrors the source ProcessMapping `Validation_Plan`):

| Check | Type | Severity |
|---|---|---|
| `CHK-01` Personnel list consistency | completeness | error |
| `CHK-02` SFI verification completeness | completeness | error |
| `CHK-03` RST verification completeness | completeness | error |
| `CHK-04` SFI expiration date check | format | error |

The two source `Cross_Field_Rules` (CFR-01 Section 6.6 ⊆ Section 2; CFR-02 SFI date within 365 days) are enforced by the Consolidation Prompt at runtime — CFR-01 produces a `personnel_discrepancies` entry rather than failing the workflow, and CFR-02 drives the per-person SFI `status` enum value (`Valid` / `Expiring Soon` / `Expired`).

## Eval posture

Workflow-local — see [`evals/`](evals/). The workflow is **not** a 1:1 repackaging of the canonical component prompt: each Extraction task carries a focused `prompt_inline` body covering a different source-document subset, and the Consolidation Prompt derives `non_compliant_personnel` and the four `verification_status` counts from the per-person status records, so per [`docs/contracts.md`](../../docs/contracts.md) workflow-local cases are required to cover behavior that emerges from the three-task topology.

Workflow-local cases should target the five-value SFI `status` enum coverage, the missing-source-document gap-flagging path, the ambiguous-name `"Review Required"` propagation, and the `overall_status: "Not Applicable"` path when `sfi_rst_required` is false. The component-level evals at [`components/compliance-personnel-verification-udm/evals/`](../../components/compliance-personnel-verification-udm/evals/) remain the right signal for the component contract itself; record both signals in harness campaigns when both are available.

## Building

Re-generate the Vandalizer export from `manifest.yaml`:

```bash
python3 scripts/build_vandalizer_workflows.py
```

CI fails when the committed `compliance-personnel-verification.vandalizer.json` differs from a fresh build, so treat `manifest.yaml` as the source of truth and never hand-edit the generated JSON.

## Sharing

The committed `compliance-personnel-verification.vandalizer.json` can be uploaded directly into Vandalizer via the workflow import UI. Its `x_ai4ra` block traces it back to this manifest, the pinned component version, and the content hash of the embedded prompt bodies.

## Triad integration

- **Evaluation datasets:** none yet — planned: a synthetic federal research proposal exercise with a deliberately-mixed compliance profile, paired with stub SFI records and RST spreadsheet fixtures.
- **Harness notes:** the three-document input model means the harness needs a workflow runner that can pass multiple workflow documents simultaneously. Score post-consolidation JSON against the schema; track `verification_status.notes` for missing-source warnings.
- **Shared UDM relationship:** inherits from the `compliance-personnel-verification-udm` component's UDM alignment (`section_2_personnel[].name` resolves to UDM `Personnel`; the verification matrices themselves are repo-local).

## Provenance

Authored 2026-05-20 alongside the initial `compliance-personnel-verification-udm` component, against `ui-insight/ProcessMapping` at commit `2c1f47f46474130743af5aee44d074bcd21787e9`. Built from the `PROC-SFI-RST-COMPLIANCE-CHECK` source process map.
