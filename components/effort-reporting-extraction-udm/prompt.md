---
name: effort-reporting-extraction-udm
version: 0.1.0
category: extraction
domain: research-administration
status: experimental
tags: [effort-reporting, post-award, certification, personnel, cost-share, 2-cfr-200, compliance, udm, structured-extraction, json]
audience: [sponsored-programs-staff, post-award-teams, ingest-pipelines]
owner: ui-insight
created: 2026-04-30
updated: 2026-04-30
---

# Effort Reporting Compliance Extraction — UDM JSON

> **Purpose:** Extract effort-reporting and personnel-compliance requirements from a federal award document into a structured JSON object that drives an "Effort Compliance Brief" for post-award compliance tracking.
> **Expected input:** Full text of a federal award notice / agreement / terms-and-conditions document, optionally with 2 CFR 200 (Uniform Guidance) or Research Terms and Conditions as knowledge-base context.
> **Expected output:** A single JSON object that validates against [`schema.json`](schema.json). No prose, no markdown outside the JSON.

## When to use this contract

This is the effort-and-personnel cut of a federal award. It produces award-identifying scalars (`award_number`, `pi_name`, `project_title`), an effort-reporting cadence (`reporting_frequency`, `certification_deadline`, `certification_method`), PI-specific commitments (`pi_committed_effort`, `pi_person_months`), a normalized **personnel commitments table** with cost-shared effort, and a list of **referenced governing documents** (RTCs, CA-FATC, 2 CFR 200.430).

UDM-aligned: `award_number` → `Award.Award_Number`; `pi_name` → `Personnel.First_Name`/`Last_Name`; `project_title` → `Award.Award_Title`; `certification_method` → `Effort.Certification_Method`; `pi_committed_effort` → `Effort.Committed_Percent`; `pi_person_months` → `Effort.Committed_Person_Months`; per-row `key_personnel_commitments` → `Effort`; `cost_shared_effort` → `CostShare.Committed_Amount`; `record_retention` → `Terms.Record_Retention_Years`.

This component does **not** cover the broader compliance framework or the FFR submission cadence — those live in `award-compliance-extraction-udm` and `ffr-management-extraction-udm`.

---

## Prompt

You are extracting effort-reporting and personnel-compliance requirements from a federal award document. Capture the cadence and method of effort certification, the PI's committed effort, all key-personnel commitments, any cost-shared effort, the governing regulation (typically 2 CFR 200.430), the record-retention requirement, and the list of referenced governing documents.

**Be 100% accurate.** Quote effort percentages, person-months, and day-counts verbatim (`"2.0 summer months"`, `"25%"`, `"6 years"`); never paraphrase. When a field is not specified, set it to `null` or — for arrays — return an empty array. Do not invent values.

Search the entire document for content in or near sections titled *Effort Reporting*, *Time and Effort*, *Personnel*, *Key Personnel*, *Budget Justification*, or *Research Terms and Conditions*. Keywords to follow: `effort reporting`, `time and effort`, `personnel`, `key personnel`, `salary`, `certification`, `2 CFR 200.430`, `cost share effort`, `person-months`, `summer months`, `FATC`, `RTC`, `principal investigator`, `co-principal investigator`.

Return a single JSON object that validates against [`schema.json`](schema.json) with these top-level keys:

- `award_number` — federal award identification number. String or `null`.
- `pi_name` — principal investigator full name. String or `null`.
- `project_title` — full project title as stated in the award. String or `null`.
- `reporting_frequency` — one of `"Monthly"`, `"Quarterly"`, `"Semi-Annual"`, `"Annual"`, or `null`.
- `certification_deadline` — string (e.g., `"30 days after period end"`) or `null`.
- `certification_method` — one of `"After-the-Fact"`, `"Plan-Confirmation"`, `"Payroll-Based"`, or `null`.
- `pi_committed_effort` — string with sponsor's effort phrasing (e.g., `"2.0 summer months"`, `"25% academic year"`). Required.
- `pi_person_months` — string converting to person-months when the document provides it (e.g., `"2.0"`). Null otherwise.
- `key_personnel_commitments` — array of `{name, role, committed_effort, person_months, cost_shared_effort, notes}` objects. One row per named individual. Required, may be a single-element array if only the PI is named.
- `cost_shared_effort` — string describing total cost-shared effort obligations or `null`.
- `governing_regulation` — string naming the primary governing regulation (e.g., `"2 CFR 200.430"`) or `null`.
- `record_retention` — string with retention period (e.g., `"3 years"`, `"per sponsor requirements"`) or `null`.
- `referenced_documents` — array of strings naming each referenced governing document (RTCs, CA-FATC, etc.). Empty array when none are stated.

### Encoding rules

1. **One row per named individual in `key_personnel_commitments`.** A row that says "Dr. Jane Smith (PI), 2.0 summer months committed, 0.5 cost-shared" becomes one entry with `name: "Dr. Jane Smith"`, `role: "PI"`, `committed_effort: "2.0 summer months"`, `cost_shared_effort: "0.5 summer months"`.
2. **Quote effort phrasing verbatim.** `"2.0 summer months"` not `"two summer months"`. `"25% academic year"` not `"a quarter of the academic year"`.
3. **`pi_committed_effort` and `pi_person_months` are required.** They are the most important post-award commitment to track. The PI's row in `key_personnel_commitments` should mirror these scalars exactly.
4. **`certification_method` enum values follow 2 CFR 200.430(i).** Use the standard term that matches what the document describes.
5. **`reporting_frequency` is the certification cadence**, not the FFR cadence. If the document does not specify, return `null`.
6. **`referenced_documents` is for governing instruments only** — RTCs, CA-FATC, NSF PAPPG, NIH GPS — not for cited regulations (those go in `governing_regulation`).
7. Do not output any text outside the single JSON object.

### Output

A single JSON object. No surrounding markdown.
