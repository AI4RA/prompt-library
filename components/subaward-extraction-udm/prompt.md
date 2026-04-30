---
name: subaward-extraction-udm
version: 0.1.0
category: extraction
domain: research-administration
status: experimental
tags: [subaward, post-award, agreement, pte, subrecipient, financial-policies, contacts, udm, structured-extraction, json]
audience: [sponsored-programs-staff, post-award-teams, ingest-pipelines]
owner: ui-insight
created: 2026-04-30
updated: 2026-04-30
---

# Subaward Agreement Extraction — UDM JSON

> **Purpose:** Extract a fully executed subaward agreement into a structured JSON object covering nine sections used for research-administration setup and ongoing monitoring of subawards: basic info, project periods, PTE contacts, subrecipient contacts, financial summary, financial policies, reporting requirements, prior-approval handling, and key compliance requirements.
> **Expected input:** Full text of an executed subaward agreement (PTE → Subrecipient), typically including attachments.
> **Expected output:** A single JSON object that validates against [`schema.json`](schema.json). No prose, no markdown outside the JSON.

## When to use this contract

This is the subaward setup-and-monitoring cut of an executed subaward agreement. It produces six logical blocks — **core award info**, **contacts**, **dates and monetary values**, **financial policies**, **reporting requirements**, and **compliance requirements** — pre-shaped so the downstream consumer (Banner setup, Vandalizer monitoring, manual SP analyst review) does not have to re-adjudicate which section a fact belongs to.

UDM-aligned: `pte_name` and `subrecipient_name` → `Organization.Organization_Name`; `federal_award_number` → `Award.Federal_Award_ID`; `subaward_number` → `Subaward.Subaward_Number`; `project_title` → `Award.Award_Title`; `subrecipient_pi.name` → `Subaward.PI_Name`; PTE/subrecipient PI / admin / financial contacts → `Personnel.First_Name`/`Last_Name` and `ContactDetails.ContactDetails_Value`; `budget_period_start`/`end` → `Subaward.Start_Date`/`End_Date`; `amount_funded` → `Subaward.Subaward_Amount`; `invoicing_frequency` → `Terms.Invoicing_Frequency`; `fa_rate` → `IndirectRate.Rate_Percentage`; `fa_base` → `IndirectRate.Base_Type`; `cost_sharing_required` → `CostShare.Is_Mandatory`; technical/financial reports → `AwardDeliverable`; `prior_approval_handling` → `Modification.Requires_Prior_Approval`; `coi_policy` → `ConflictOfInterest`; `record_retention` → `Terms.Record_Retention_Years`.

This component does **not** cover the prime federal award's compliance framework — that lives in `award-compliance-extraction-udm`. It does not cover prime-award prior-approval procedures — that lives in `prior-approval-extraction-udm`.

---

## Prompt

You are extracting a fully executed subaward agreement (PTE = Pass-Through Entity → Subrecipient) into a single structured JSON object covering core award information, all PTE and Subrecipient contact details, dates and monetary values, financial policies, reporting requirements, and compliance requirements.

**Be 100% accurate.** Subaward agreements have **character-perfect** requirements — but match the schema's type for each field exactly:

- **Number-typed fields** (`amount_funded`, `total_direct_costs`, `total_indirect_costs`) — emit as JSON numbers. `$1,234,567.89` in the document → `1234567.89` in JSON. No quotes, no `$`, no thousand-separators. Use the document's exact value; do not round.
- **String-typed fields** (every other extracted field, including all contact emails and phone numbers, all date strings, `fa_rate`, etc.) — quote character-perfectly. Preserve currency symbols when they appear in narrative (`carryforward_policy`), preserve email format exactly (`first.last@institution.edu`), preserve phone format exactly (`(208) 555-1234`), preserve date format exactly.
- **Boolean-typed fields** (`cost_sharing_required`) — emit as `true`/`false`/`null`.

When a field is not specified, set it to `null` or — for arrays — return an empty array. Do not invent values.

Search the entire agreement, including attachments, for content in or near sections titled *Award Information*, *Subaward Header*, *Parties*, *Attachment A*, *Attachment B*, *Contact Information*, *Award Amount*, *Budget*, *Period of Performance*, *Financial Information*, *Terms and Conditions*, *Special Conditions*, *Financial Terms*, *Attachment 4*, *Reporting and Prior Approval Terms*, *General Terms*, *Certifications*, *Flow-Down Requirements*.

Return a single JSON object that validates against [`schema.json`](schema.json) with these top-level keys grouped into six blocks:

**Core award information:**
- `pte_name` — Pass-Through Entity name. Required.
- `subrecipient_name` — Subrecipient organization name. Required.
- `federal_award_number` — PTE's Federal Award Number (FAIN). **Required.**
- `subaward_number` — Subaward number. Required.
- `project_title` — full project title. Required.
- `federal_awarding_agency` — federal awarding agency name. **Required.**

**Contacts:**
- `pte_pi`, `pte_admin_contact`, `pte_financial_contact`, `subrecipient_pi`, `subrecipient_admin_contact`, `subrecipient_financial_contact` — each `{name, email, phone}` or `null`. `pte_pi` and `subrecipient_pi` are required; the four "contact" fields are optional.

**Dates & monetary values:**
- `budget_period_start` — date string. Required.
- `budget_period_end` — date string. Required.
- `amount_funded` — number (decimal). Required.
- `total_direct_costs`, `total_indirect_costs` — numbers or `null`.
- `cost_type` — one of `"Cost Reimbursement"`, `"Fixed Price"`, `"Time and Materials"`, or `null`.

**Financial policies:**
- `invoicing_frequency` — one of `"Monthly"`, `"Quarterly"`, `"Semi-Annual"`, `"Annual"`. **Required.**
- `final_invoice_due` — string or `null`.
- `fa_rate` — string with rate percentage or `null`.
- `fa_base` — string (e.g., `"MTDC"`, `"TDC"`) or `null`.
- `cost_sharing_required` — boolean or `null`.
- `carryforward_policy` — string or `null`.

**Reporting requirements:**
- `technical_reports` — array of `{report_name, frequency, due, recipient}` objects. Empty when none.
- `financial_reports` — array of `{report_name, frequency, due, recipient}` objects. Empty when none.
- `invention_reporting` — array of `{requirement, timing}` objects. Empty when none.

**Compliance requirements:**
- `governing_regulations` — array of `{regulation, source}` objects. Required.
- `prior_approval_handling` — string describing general prior-approval policy, or `null`.
- `coi_policy` — string describing whose COI policy applies, or `null`.
- `data_rights` — string or `null`.
- `audit_requirements` — string or `null`.
- `termination_clauses` — string or `null`.
- `record_retention` — string or `null`.

### Encoding rules

1. **Each contact is a `{name, email, phone}` object or `null`.** Quote emails and phone numbers character-perfectly — these are downstream notification targets.
2. **`amount_funded == total_direct_costs + total_indirect_costs`** when all three are present (downstream cross-field check `CHK-01`). All three are JSON numbers, not quoted strings. When the agreement does not reconcile, preserve the document's reported values.
3. **Reporting arrays are typed.** `technical_reports` and `financial_reports` use `{report_name, frequency, due, recipient}`; `invention_reporting` uses `{requirement, timing}`. Each report row is one required deliverable — do not collapse multiple deliverables into a single row.
4. **`governing_regulations` is required** and must list every governing instrument the agreement names with its source attribution (the document section / attachment that calls it out).
5. **Strict inclusion criteria for `technical_reports` and `financial_reports`.** Only include reports the agreement explicitly requires. Do not synthesize standard reports the agreement does not mandate.
6. **`cost_type` enum** matches the source workflow: `Cost Reimbursement`, `Fixed Price`, `Time and Materials`. Most subawards are `Cost Reimbursement`; quote whatever the document states.
7. Do not output any text outside the single JSON object.

### Output

A single JSON object. No surrounding markdown.
