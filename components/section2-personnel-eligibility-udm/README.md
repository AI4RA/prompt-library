# Section 2 Personnel Eligibility Verification — UDM JSON

Automates the VERAS Section 2 review at the University of Idaho — the most-requested SPA automation in the source process map. Extracts every PI / Co-PI / Senior Key Person from VERAS Section 2, verifies employment via Banner NBAJOBS, cross-references each PI / Co-PI job title against APM Section 45.22 eligibility criteria, compiles timesheet org codes, maps org codes to Departmental Grant Administrators (DGAs) using the institutional Department List, and cross-references required DGAs against Section 2 participants. Covers the source `PROC-SPA-SECTION2-REVIEW` process (13 steps, 77% automatable per the source process map).

**Current version:** 0.1.0
**Category:** extraction
**Domain:** research-administration
**Status:** experimental
**Manifestations:** prompt
**Output contract:** [`schema.json`](schema.json)
**Contract scope:** repo-local, UDM-aligned

## Inputs

Three workflow documents must be uploaded together in Vandalizer:

1. **VERAS proposal package** — at minimum Sections 2.1 (PI + Co-PIs) and 2.2A (Senior / Key Personnel).
2. **Banner NBAJOBS extract** — current employment records for every person on the proposal (export, CSV, or PDF).
3. **Institutional Department List** — the org-code → department → DGA mapping table.

The **APM 45.22 eligible-titles list** is referenced from the knowledge base / search corpus. The source workflow notes that an APM 45.22 custom knowledge base must be built and loaded before the workflow runs in production.

When any of the three workflow documents is missing, the contract requires the workflow to emit non-compliant defaults (`found_in_banner: false`, `eligibility_status: "Review Required"`, empty `dga_names`) and capture the gap in `verification_summary.notes`. The contract never silently assumes employment, eligibility, or DGA mapping.

## Outputs

A single JSON object with seven structured blocks:

- **`personnel_extraction`** — Section 2.1 personnel (PI + Co-PIs, required minItems 1), Section 2.2A personnel (Senior / Key), total count, and the two derived sub-lists (`pi_copis_requiring_eligibility`, `personnel_requiring_org_code_only`)
- **`personnel_verification`** — per-person `{name, found_in_banner, current_employee, job_title, timesheet_org_code, notes}` records
- **`eligibility_check`** — per-PI / Co-PI `{name, role, job_title, eligibility_status, evidence}` records with three-value status enum (`Eligible`, `Not Eligible`, `Review Required`)
- **`org_code_compilation`** — per-org-code `{org_code, personnel_names, count}` records
- **`dga_mapping`** — per-org-code `{org_code, department_name, dga_names}` records (supports multiple DGAs per code)
- **`dga_cross_reference`** — per-DGA `{dga_name, org_codes, listed_in_section_2, action_needed}` records with two-value action enum
- **`verification_summary`** — aggregate counts, lists of flagged personnel / DGAs / unmapped codes, and source-document gap notes

See [`schema.json`](schema.json) for the authoritative definition and [`prompt.md`](prompt.md) for encoding rules (ambiguous-title flagging, no-assumption rules, dual-DGA handling).

## Contract scope

Repo-local, UDM-aligned. The proposal record resolves to UDM `Proposal`; personnel resolve to UDM `Personnel.First_Name` / `Personnel.Last_Name`. The org-code → DGA mapping, the APM 45.22 eligibility surface, and the verification matrices are repo-local extensions that do not (yet) correspond to shared UDM tables.

## Relationship to other components

| Concern | Source of truth |
|---|---|
| Section 2 PI / Co-PI eligibility (APM 45.22) + DGA mapping | `section2-personnel-eligibility-udm` (this component) |
| SFI disclosure + RST completion compliance | [`compliance-personnel-verification-udm`](../compliance-personnel-verification-udm/) |
| Proposal-document completeness gap analysis | [`proposal-document-completeness-udm`](../proposal-document-completeness-udm/) |

The three pre-award compliance components are versioned independently and intended to run together on a single proposal upload to produce a comprehensive readiness review.

## Triad integration

- **Evaluation datasets:** none yet — planned: a synthetic UI proposal exercise with three PI / Co-PI personnel (one eligible Professor, one ineligible Lecturer, one ambiguous Clinical Assistant Professor) and at least one missing DGA, validated by a Sponsored Programs Administrator.
- **Harness notes:** canonical manifestation is `prompt.md`. Validation surface is `schema.json`. The three-document input model is identical to `compliance-personnel-verification-udm` — the harness needs a workflow runner that can pass multiple workflow documents simultaneously.
- **Shared UDM relationship:** aligned, not owning. Personnel resolve to UDM Personnel; the org-code → DGA mapping, APM 45.22 eligibility, and verification matrices are repo-local.

## Runtime topology — the Vandalizer workflow

The canonical runtime for this component is the [`section2-personnel-eligibility` workflow](https://github.com/AI4RA/prompt-library/tree/main/workflows/section2-personnel-eligibility) shipped at the top level of this repo. The single source of truth is [`workflows/section2-personnel-eligibility/manifest.yaml`](https://github.com/AI4RA/prompt-library/blob/main/workflows/section2-personnel-eligibility/manifest.yaml); the companion `.vandalizer.json` envelope is generated by [`scripts/build_vandalizer_workflows.py`](https://github.com/AI4RA/prompt-library/blob/main/scripts/build_vandalizer_workflows.py) and committed alongside. The runtime mirrors the source [`ui-insight/ProcessMapping/workflows/section2-personnel-eligibility/`](https://github.com/ui-insight/ProcessMapping/tree/main/workflows/section2-personnel-eligibility) workflow:

- **Step 1 (parallel Extraction)** — two Extraction tasks mirror the source workflow one-for-one: personnel-extraction (Sections 2.1 + 2.2A with derived sub-lists) and eligibility-and-DGA-verification (Banner NBAJOBS lookups + APM 45.22 cross-references + Department List org-code → DGA mapping + Section 2 DGA cross-reference).
- **Step 2 (Consolidation Prompt)** — assembles the two JSON fragments into the schema-conformant seven-block object, derives the `verification_summary` counts and flag arrays, and enforces the three cross-field rules (every PI / Co-PI has an eligibility determination; every unique org code has a `dga_mapping` row; every DGA pulled from `dga_mapping` is cross-referenced in `dga_cross_reference`).

Regenerate the workflow JSON whenever this component bumps MINOR or MAJOR (or whenever the workflow manifest changes); CI fails if the committed `.vandalizer.json` drifts from a fresh build.

## Manifestations

- [`prompt.md`](prompt.md) — canonical, LLM-agnostic prompt

## Evals

See [`evals/`](evals/) for reference inputs and known-good outputs. Initial case pending: a synthetic UI proposal exercise with mixed-eligibility personnel and at least one missing DGA, validated by an SPA.

## Provenance

Authored 2026-05-20 against the `section2-personnel-eligibility` (Workflow_ID: `WF-SECTION2-PERSONNEL-ELIGIBILITY`) process-mapping workflow in `ui-insight/ProcessMapping` at commit `2c1f47f46474130743af5aee44d074bcd21787e9`, which was built from the `PROC-SPA-SECTION2-REVIEW` process map (13 steps, 77% automatable). Built explicitly in response to Michele Mattoon's request for an APM 45.22 auto-check; created to make the SPA's Section 2 review a harness-evaluatable, versioned artifact.
