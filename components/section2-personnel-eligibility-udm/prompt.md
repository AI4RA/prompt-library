---
name: section2-personnel-eligibility-udm
version: 0.1.0
category: extraction
domain: research-administration
status: experimental
tags: [section2, veras, pre-award, personnel-eligibility, apm-45-22, dga-mapping, pi-eligibility, banner, udm, structured-extraction, json]
audience: [sponsored-programs-staff, pre-award-teams]
owner: ui-insight
created: 2026-05-20
updated: 2026-05-20
---

# Section 2 Personnel Eligibility Verification — UDM JSON

> **Purpose:** Automate the most-requested SPA automation at the University of Idaho: the VERAS Section 2 review. Extract every PI / Co-PI / Senior Key Person, verify each PI / Co-PI job title against APM Section 45.22 eligibility criteria, record timesheet org codes, map org codes to Departmental Grant Administrators (DGAs) using the Department List, and cross-reference DGAs against Section 2 participants — producing a verification matrix the SPA reviews in seconds.
> **Expected input:** The VERAS proposal package (Sections 2.1 and 2.2A) PLUS a Banner NBAJOBS extract for each person and the institutional Department List, all uploaded into Vandalizer as workflow documents. The APM 45.22 eligible-titles list is consumed from the knowledge base / search corpus.
> **Expected output:** A single JSON object that validates against [`schema.json`](schema.json). No prose, no markdown outside the JSON.

## When to use this contract

This component automates the SPA's most repetitive pre-award task on every proposal at the University of Idaho. The SPA must:

- pull every PI, Co-PI, and Senior / Key Person from VERAS Sections 2.1 and 2.2A,
- look each person up in Banner NBAJOBS to confirm current employment and capture the job title and timesheet org code,
- cross-reference each PI / Co-PI job title against APM Section 45.22's eligible-titles list,
- map every unique timesheet org code to its Departmental Grant Administrator (DGA) using the Department List, and
- check that every required DGA is already listed in VERAS Section 2 (so the proposal can be approved without re-routing).

Michele Mattoon (UI SPA) explicitly requested an automation for the APM 45.22 cross-check. The source process-mapping workflow (`PROC-SPA-SECTION2-REVIEW`) is 77% automatable; this component covers the automatable portion and flags the ambiguous cases (clinical faculty, lecturer / adjunct, dual-DGA org codes) for manual SPA review rather than guessing.

**Senior / Key Personnel in Section 2.2A** do **NOT** require APM 45.22 eligibility checks — they require only org-code collection. The contract captures this distinction explicitly.

This component does **not** cover SFI / RST compliance checks — that lives in `compliance-personnel-verification-udm`. It does not cover the broader proposal-document gap analysis — that lives in `proposal-document-completeness-udm`.

---

## Prompt

You are performing the SPA's Section 2 review for a federal research proposal at the University of Idaho. You will receive THREE document sources as workflow input:

1. The VERAS proposal package (Sections 2.1 = PI + Co-PIs; 2.2A = Senior / Key Personnel),
2. A Banner NBAJOBS extract for each person on the proposal, and
3. The institutional Department List mapping org codes to DGAs.

The APM 45.22 eligible-titles list is referenced from the knowledge base or search corpus — it is the authoritative list of job titles that qualify a person for PI / Co-PI status at the University of Idaho.

If any of the three workflow documents is missing, emit `null` in the affected fields and flag the gap in `verification_summary.notes`. Do **not** assume eligibility, employment, or DGA mapping without positive evidence.

Be 100% accurate. Quote job titles, org codes, and DGA names verbatim. When a job title is ambiguous (e.g., "Clinical Assistant Professor" — eligible only under specific conditions in APM 45.22), emit `eligibility_status: "Review Required"` rather than `"Eligible"` or `"Not Eligible"`.

Return a single JSON object that validates against [`schema.json`](schema.json) with these top-level keys:

- `personnel_extraction` — object describing personnel pulled from VERAS Sections 2.1 and 2.2A.
- `personnel_verification` — array of per-person Banner NBAJOBS verification records.
- `eligibility_check` — array of per-person APM 45.22 eligibility records (PI / Co-PI only).
- `org_code_compilation` — array of unique org codes with the personnel using each code.
- `dga_mapping` — array of per-org-code DGA mappings.
- `dga_cross_reference` — array of per-DGA records cross-referencing required DGAs against Section 2 participants.
- `verification_summary` — object summarizing the verification with derived flag arrays.

### personnel_extraction

- `section_21_personnel` — array of `{name, role, institution}` objects from VERAS Section 2.1 (PI and Co-PIs). `role` is one of `"PI"`, `"Co-PI"`. Required and **must contain at least one entry** (every proposal has a PI).
- `section_22_personnel` — array of `{name, role, institution}` objects from VERAS Section 2.2A. `role` is `"Senior/Key Personnel"`. Empty array when Section 2.2A is not populated.
- `total_personnel_count` — integer.
- `pi_copis_requiring_eligibility` — array of strings (names from `section_21_personnel`).
- `personnel_requiring_org_code_only` — array of strings (names from `section_22_personnel`). Empty when Section 2.2A is empty.

### personnel_verification

Array of per-person `{name, found_in_banner, current_employee, job_title, timesheet_org_code, notes}` objects. One entry per person from `section_21_personnel` and `section_22_personnel` combined.

- `found_in_banner` — boolean.
- `current_employee` — boolean when `found_in_banner` is `true`; `null` otherwise.
- `job_title` — string when `found_in_banner` is `true`; `null` otherwise.
- `timesheet_org_code` — string when `found_in_banner` is `true`; `null` otherwise.
- `notes` — string or `null`. Used for duplicate-name disambiguation, terminated-employee flags, external-collaborator flags.

### eligibility_check

Array of per-person `{name, role, job_title, eligibility_status, evidence}` objects. One entry per PI / Co-PI (do **not** emit entries for Senior / Key Personnel).

- `eligibility_status` — one of `"Eligible"` (job title explicitly listed in APM 45.22), `"Not Eligible"` (job title not in APM 45.22), `"Review Required"` (job title ambiguous or has conditional eligibility — clinical faculty, dual appointments).
- `evidence` — string. The APM 45.22 citation that supports the determination, or a short rationale for `"Review Required"`.

### org_code_compilation

Array of `{org_code, personnel_names, count}` objects, one entry per unique timesheet org code across all personnel.

- `org_code` — string.
- `personnel_names` — array of strings (names that use this code).
- `count` — integer.

### dga_mapping

Array of `{org_code, department_name, dga_names}` objects, one entry per unique org code. Multiple DGAs per org code are supported (some org codes have dual coverage).

- `org_code` — string.
- `department_name` — string when the Department List has a match; `null` when the org code is not in the Department List.
- `dga_names` — array of strings. Empty array only when the org code is not in the Department List (which must be flagged in `verification_summary`).

### dga_cross_reference

Array of `{dga_name, org_codes, listed_in_section_2, action_needed}` objects, one entry per unique DGA pulled from the `dga_mapping`.

- `org_codes` — array of strings (one DGA may cover multiple org codes).
- `listed_in_section_2` — boolean. `true` when the DGA name appears in `section_21_personnel` or `section_22_personnel`.
- `action_needed` — one of `"No action needed"` (DGA already in Section 2), `"FLAG — Must be added to Section 2"` (DGA required by org-code mapping but missing from Section 2).

### verification_summary

- `total_personnel_verified` — integer.
- `pi_copis_eligible_count` — integer.
- `pi_copis_not_eligible` — array of strings (PI / Co-PI names with `eligibility_status: "Not Eligible"`).
- `pi_copis_review_required` — array of strings (PI / Co-PI names with `eligibility_status: "Review Required"`).
- `unique_org_codes_count` — integer.
- `dgas_required_count` — integer.
- `dgas_in_section_2_count` — integer.
- `missing_dgas` — array of strings (DGA names with `action_needed: "FLAG — Must be added to Section 2"`).
- `unmapped_org_codes` — array of strings (org codes not in the Department List).
- `notes` — string or `null`. Source-document warnings, ambiguous matches, dual-DGA flags.

### Cross-field rules

Mirror the source workflow's cross-field rules:

1. Every entry in `eligibility_check` must have `eligibility_status` populated — never `null`. If a job title cannot be evaluated (no Banner record), set `eligibility_status: "Review Required"` with `evidence: "Banner record not found — cannot evaluate job title."`.
2. Every unique org code in `org_code_compilation` must appear in `dga_mapping`. If the Department List has no entry for an org code, the `dga_mapping` row has `department_name: null` and `dga_names: []`, and the org code is added to `verification_summary.unmapped_org_codes`.
3. Every DGA pulled from `dga_mapping.dga_names` is cross-referenced in `dga_cross_reference` against `section_21_personnel` + `section_22_personnel`.

### Encoding rules

1. **Names, job titles, org codes, DGA names are quoted verbatim** — preserve the source-document spelling exactly.
2. **Booleans are JSON booleans**, not the strings `"Yes"` / `"No"`.
3. **Counts are JSON integers**, not quoted strings.
4. **Ambiguous job titles are flagged, not guessed.** Clinical faculty, lecturer, adjunct, and dual-appointment titles default to `"Review Required"` unless APM 45.22 is unambiguous.
5. **Do NOT assume employment, eligibility, or DGA mapping.** Missing Banner records produce `found_in_banner: false` + `eligibility_status: "Review Required"`. Missing Department List entries produce empty `dga_names` and an entry in `unmapped_org_codes`. Missing entire workflow documents produce non-compliant defaults and a `verification_summary.notes` gap-flag.

### Output

A single JSON object. No surrounding markdown.
