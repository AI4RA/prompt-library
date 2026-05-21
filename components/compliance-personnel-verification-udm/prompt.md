---
name: compliance-personnel-verification-udm
version: 0.1.0
category: extraction
domain: research-administration
status: experimental
tags: [compliance, sfi, rst, personnel-verification, veras, pre-award, conflict-of-interest, research-security-training, udm, structured-extraction, json]
audience: [sponsored-programs-staff, pre-award-teams, compliance-officers]
owner: ui-insight
created: 2026-05-20
updated: 2026-05-20
---

# Compliance Personnel Verification (SFI & RST) — UDM JSON

> **Purpose:** Automate the SFI (Significant Financial Interest) disclosure and RST (Research Security Training) compliance check on every person named in a federal research proposal. Extract personnel from VERAS Sections 2 and 6.6, cross-reference each person against SFI disclosure records and the daily RST completion spreadsheet, and produce a per-person compliance matrix that a Sponsored Programs Administrator (SPA) can review without manually searching email folders and spreadsheets.
> **Expected input:** The VERAS proposal package PLUS the institutional SFI disclosure records and the most recent daily RST completion spreadsheet, all uploaded into Vandalizer as workflow documents. The workflow runs against the federation of these documents.
> **Expected output:** A single JSON object that validates against [`schema.json`](schema.json). No prose, no markdown outside the JSON.

## When to use this contract

This component automates the most repetitive part of an SPA's pre-award review on federal research proposals. The SPA must confirm that every PI, Co-PI, and Senior/Key Person:

- has a current Significant Financial Interest (SFI) disclosure on file (valid within 365 days of submission), and
- has completed Research Security Training (RST) per the institution's record.

The source process-mapping workflow (`PROC-SFI-RST-COMPLIANCE-CHECK`) is 80% automatable but currently requires an SPA to email-search the SFI records folder and spreadsheet-lookup the daily RST export. This component produces the same compliance matrix from the same three input documents.

**Federal research proposals only.** SFI and RST checks do **not** apply to non-research proposals or non-federal sponsors. The contract captures `proposal_type` and `sponsor_type` explicitly, and the boolean `sfi_rst_required` drives whether the consumer (SPA, downstream automation) should act on the compliance matrix at all.

This component does **not** cover Section 2 PI eligibility against APM 45.22 — that lives in `section2-personnel-eligibility-udm`. It does not cover Conflict-of-Interest management plans beyond the SFI disclosure presence check.

---

## Prompt

You are verifying SFI disclosure and RST completion status for every person named on a federal research proposal. You will receive THREE document sources as workflow input:

1. The VERAS proposal package (Section 2 = PI / senior key personnel; Section 6.6 = personnel requiring SFI disclosures),
2. The institutional SFI disclosure records (extracted, emailed, or scanned), and
3. The most recent daily RST completion spreadsheet from UI Bridge.

If any of the three is missing, emit `null` in the corresponding output fields and flag the missing source explicitly in `verification_status.notes`. Do **not** assume compliance without positive evidence.

Be 100% accurate. Quote dates verbatim. Use ISO `YYYY-MM-DD` for SFI disclosure dates whenever the source is unambiguous. When in doubt about an ambiguous name match (e.g., two people share a last name and you cannot disambiguate by department), flag the person as `"Review Required"` rather than guessing.

Return a single JSON object that validates against [`schema.json`](schema.json) with these top-level keys:

- `proposal_metadata` — object describing the proposal and the determination of whether SFI / RST checks apply.
- `personnel_identification` — object describing the personnel pulled from VERAS Sections 2 and 6.6 and the consolidated check list.
- `sfi_verification` — array of per-person SFI status records.
- `rst_verification` — object with the spreadsheet metadata and array of per-person RST status records.
- `non_compliant_personnel` — array of per-person flags for any compliance issue.
- `verification_status` — object summarizing overall compliance.

### proposal_metadata

- `proposal_type` — one of `"Research"`, `"Non-Research"`, `"Not specified"`. **Required.**
- `sponsor_type` — one of `"Federal"`, `"State"`, `"Non-Federal"`, `"Not specified"`. **Required.**
- `sfi_rst_required` — boolean. **Required.** `true` when `proposal_type == "Research"` AND `sponsor_type == "Federal"`. `false` in every other combination.

### personnel_identification

- `section_66_personnel` — array of strings. Names listed in VERAS Section 6.6 requiring SFI disclosures. Required (may be empty).
- `section_2_personnel` — array of `{name, role, department}` objects from VERAS Section 2 PIs and Senior/Key Personnel. Required (must contain at least one entry, since every research proposal has a PI). Each `role` is one of `"PI"`, `"Co-PI"`, `"Senior/Key Personnel"`. `department` is `null` when not stated.
- `consolidated_personnel` — array of `{name, role, department, source_sections}` objects representing the deduplicated union of `section_66_personnel` and `section_2_personnel`. Required. `source_sections` is an array containing one or both of `"6.6"`, `"2"`.
- `personnel_discrepancies` — array of strings. Differences between the two source sections (e.g., person in Section 2 but missing from Section 6.6). Empty array when lists match.

### sfi_verification

Array of per-person `{name, disclosure_found, disclosure_date, days_since_disclosure, valid_within_365_days, status}` objects. One entry per person in `consolidated_personnel`.

- `disclosure_found` — boolean.
- `disclosure_date` — string in ISO `YYYY-MM-DD` when found; `null` otherwise.
- `days_since_disclosure` — integer when `disclosure_found` is `true`; `null` otherwise.
- `valid_within_365_days` — boolean when `disclosure_found` is `true`; `null` otherwise.
- `status` — one of `"Valid"`, `"Expiring Soon"` (valid but ≤ 30 days from expiration), `"Expired"`, `"Not Found"`, `"Review Required"` (ambiguous match).

### rst_verification

- `spreadsheet_date` — string in ISO `YYYY-MM-DD`. **Required.** Date of the RST completion spreadsheet used.
- `spreadsheet_source` — string. Source label (e.g., `"UI Bridge daily export"`). **Required.**
- `records` — array of per-person `{name, found_in_spreadsheet, completion_date, status}` objects. One entry per person in `consolidated_personnel`.
  - `found_in_spreadsheet` — boolean.
  - `completion_date` — string in ISO `YYYY-MM-DD` when found; `null` otherwise.
  - `status` — one of `"Complete"`, `"Incomplete"`, `"Review Required"` (ambiguous match).

### non_compliant_personnel

Array of `{name, issue, required_action, priority}` objects. One entry per compliance issue (a single person may have multiple entries if both SFI and RST fail).

- `issue` — short string describing the issue (e.g., `"SFI disclosure not found"`, `"SFI disclosure expired"`, `"RST not completed"`).
- `required_action` — short string describing the remediation (e.g., `"Submit SFI disclosure before proposal submission"`).
- `priority` — one of `"Critical"` (blocks submission), `"High"` (must renew immediately), `"Medium"` (expires within 30 days).

Empty array when every person is compliant.

### verification_status

- `total_personnel_checked` — integer.
- `sfi_compliant_count` — integer.
- `rst_compliant_count` — integer.
- `fully_compliant_count` — integer (both SFI and RST compliant).
- `overall_status` — one of `"All Compliant"`, `"Non-Compliance Found"`, `"Not Applicable"` (when `sfi_rst_required` is `false`).
- `notes` — string or `null`. Use for source-document warnings, e.g., `"SFI disclosure records not provided as a workflow document — cannot determine SFI status."`.

### Encoding rules

1. **Dates are ISO `YYYY-MM-DD`.** When the source spreadsheet uses `MM/DD/YYYY` or another format, convert to ISO.
2. **Booleans are JSON booleans**, not the strings `"true"` / `"false"` or `"Yes"` / `"No"`.
3. **Days-since-disclosure is a JSON integer**, computed from the disclosure date relative to the proposal submission date (or today's date if the proposal date is not in the documents).
4. **Counts are JSON integers**, not quoted strings.
5. **Ambiguous matches are flagged, not guessed.** When two records could match the same name, emit `status: "Review Required"` and capture the ambiguity in `verification_status.notes`.
6. **Do NOT assume compliance.** A person missing from the SFI records is `"Not Found"`, not `"Valid"`. A person missing from the RST spreadsheet is `"Incomplete"`, not `"Complete"`.

### Output

A single JSON object. No surrounding markdown.
