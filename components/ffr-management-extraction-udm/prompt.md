---
name: ffr-management-extraction-udm
version: 0.1.0
category: extraction
domain: research-administration
status: experimental
tags: [ffr, sf-425, post-award, financial-reporting, federal-financial-report, compliance, udm, structured-extraction, json]
audience: [sponsored-programs-staff, post-award-teams, ingest-pipelines]
owner: ui-insight
created: 2026-04-30
updated: 2026-04-30
---

# FFR Management Extraction — UDM JSON

> **Purpose:** Extract Federal Financial Report (FFR / SF-425) requirements and post-award financial reporting obligations from a federal award notice or agreement into a single structured JSON object that downstream tooling can use to drive an FFR preparation and submission calendar.
> **Expected input:** Full text of a federal award notice / agreement / terms-and-conditions document.
> **Expected output:** A single JSON object that validates against [`schema.json`](schema.json). No prose, no markdown outside the JSON.

## When to use this contract

This is the post-award financial-reporting cut of an award document. It produces five buckets a sponsored-programs analyst uses when scheduling FFR submissions: the **submission schedule**, the **submission system and procedures**, the **required financial data** categories, the **compliance and consequences** language, and a **preparation timeline** countdown. UDM-aligned scalar fields (`award_number`, `pi_name`) resolve cleanly to UDM `Award` and `Personnel` entities; the `expenditure_categories` list and `preparation_timeline` table support downstream `AwardBudget` and `Terms` ingest.

This component does **not** cover the broader post-award compliance framework (high-risk conditions, prior approvals, audit thresholds) — that lives in `award-compliance-extraction-udm`. It does not cover effort certification — that lives in `effort-reporting-extraction-udm`.

---

## Prompt

You are extracting Federal Financial Report (FFR / SF-425) requirements and post-award financial reporting obligations from a federal award notice or agreement.

**Be 100% accurate.** Quote the document for any threshold, deadline, or system name; never paraphrase a number, deadline, or required system. When the document does not specify a value, set the field to `null` or — for arrays/tables — return an empty array. Do not invent values.

Search the entire document for content in or near sections titled *Financial Reporting Requirements*, *SF-425*, *Federal Financial Report*, *Payment Management System*, *Reporting Schedule*, or *Financial Monitoring*. Keywords to follow: `FFR`, `SF-425`, `financial report`, `PMS`, `expenditure`, `deadline`, `submit`, `days`, `budget period`, `project end`, `liquidation`, `drawdown`.

Return a single JSON object that validates against [`schema.json`](schema.json) with these top-level keys:

- `award_number` — federal award identification number (FAIN). String or `null`.
- `pi_name` — principal investigator full name. String or `null`.
- `submission_schedule` — object covering annual / final / interim cadence:
  - `annual_ffr_due` — string (e.g., `"90 days after each budget period end"`). **Required.** When the document does not state it, use `"Not specified in the document"` (do not use null).
  - `final_ffr_due` — string (e.g., `"120 days after project end"`). **Required.** When the document does not state it, use `"Not specified in the document"`.
  - `interim_reporting` — string description or `null`.
  - `cash_transaction_reporting` — string description or `null`.
- `submission_system` — object covering the platform and access:
  - `platform` — one of `"Payment Management System"`, `"ASAP"`, `"ACH"`, `"Grants.gov"`, `"Other"`, or `null`.
  - `access_requirements` — string or `null`.
  - `era_commons_integration` — string or `null` (set when the award is NIH/HHS).
  - `submission_authorization` — string describing roles / responsibilities, or `null`.
- `required_financial_data` — array of strings naming each required category exactly as the document states it (e.g., `"Personnel"`, `"Fringe benefits"`, `"Equipment"`, `"Subawards"`, `"Cost share"`, `"Program income"`). Empty array if not specified.
- `compliance_consequences` — object covering enforcement language:
  - `late_submission_penalties` — string or `null`.
  - `account_restrictions` — string or `null`.
  - `impact_on_future_funding` — string or `null`.
  - `required_documentation` — string or `null`.
- `preparation_timeline` — array of `{milestone, days_before_period_end, action, owner}` objects describing the countdown the document implies. Empty array when the document does not specify timing.

### Encoding rules

1. **Quote dollar amounts and day-counts verbatim.** `"90 days"`, not `"three months"`. `"$500,000"`, not `"$0.5M"`.
2. **Preserve sponsor terminology.** If the document says *Payment Management System (PMS)*, set `platform: "Payment Management System"` and put the abbreviation in the `access_requirements` text only when needed for clarity.
3. **Do not synthesize a `preparation_timeline`** from generic best practices. Only populate this array when the document itself describes a countdown (e.g., "30 days prior to period end the recipient shall begin reconciliation"). Empty array otherwise.
4. **Required financial data is a flat list of category labels**, not a paragraph. If the document says "expenditures must be reported by salary, fringe, equipment, travel, and indirect costs", emit `["Salary", "Fringe", "Equipment", "Travel", "Indirect costs"]`.
5. The `cash_transaction_reporting` field is for the SF-272 / cash transaction language only; do not duplicate generic FFR cadence here.
6. Do not output any text outside the single JSON object.

### Output

A single JSON object. No surrounding markdown.
