---
name: export-to-banner-extraction-udm
version: 0.1.0
category: extraction
domain: research-administration
status: experimental
tags: [export-to-banner, post-award, banner-erp, award-notice, financial, billing, sponsor-classification, udm, structured-extraction, json]
audience: [sponsored-programs-staff, post-award-teams, ingest-pipelines]
owner: ui-insight
created: 2026-05-20
updated: 2026-05-20
---

# Export to Banner Award Extraction — UDM JSON

> **Purpose:** Extract operational setup data from a fully-executed federal award document into the specific fields needed to populate the VERAS Export to Banner form. Focuses on Banner ERP-specific data: award identification, dates and performance period, sponsor entity classification, budget structure and indirect-cost terms, billing and payment terms, and reporting / special-conditions text. Complements `award-compliance-extraction-udm` (broader compliance monitoring) by targeting only the operational fields Banner needs.
> **Expected input:** A fully-executed federal award notice / agreement / cooperative agreement / contract (or an award modification that updates Banner-relevant fields) — typically 5–50+ pages with budget attachments and terms-and-conditions.
> **Expected output:** A single JSON object that validates against [`schema.json`](schema.json). No prose, no markdown outside the JSON.

## When to use this contract

This is the **Banner-setup** cut of an award document. It produces the six structured blocks a Post-Award Specialist uses to fill in the VERAS Export to Banner form on its way into Banner ERP: award identification (FAIN / title / PI / type / pass-through / CFDA / NAICS / agency), dates and performance period (current and overall), sponsor entity classification (entity type / agency hierarchy / address / UEI), budget structure (line-item categories + F&A + cost share + program income), billing and payment terms (billing type / frequency / address / PMS LOC code), and reporting / special requirements (reports table + record retention + carry forward + prior-approval matrix + special terms + closeout).

This component does **not** cover the broader post-award compliance framework (high-risk conditions, audit thresholds, deliverable schedules) — that lives in `award-compliance-extraction-udm`. It does not cover FFR / SF-425 submission cadence — that lives in `ffr-management-extraction-udm`. It does not cover modification intake (which is its own cut of an amendment document) — that lives in `award-modification-intake-udm`.

---

## Prompt

You are extracting the contents of a fully-executed federal award document into the operational fields needed to populate VERAS's Export to Banner form. The downstream consumer enters these values into Banner ERP.

**Be 100% accurate.** Quote the document for every identifier, date, amount, rate, and contact field; never paraphrase a numeric value or deadline. When the document does not specify a value, set the field to `null` (or, for required string fields where the source workflow specified `"Not specified in the document"`, emit `null` — the schema accepts `null` for these).

Search the entire document with attention to sections titled *Award Notice*, *Cover Page*, *Award Information*, *Federal Award Information*, *Period of Performance*, *Budget*, *Funding Information*, *Sponsor Information*, *Federal Agency*, *Recipient Information*, *Payment Information*, *Billing*, *Invoice*, *Reporting Requirements*, *Terms and Conditions*, *Special Terms*, *Record Retention*, *Carry Forward*, *Prior Approval*, *Closeout*. Keywords to follow: `award number`, `FAIN`, `grant number`, `contract number`, `principal investigator`, `pass-through`, `subaward`, `CFDA`, `NAICS`, `period of performance`, `effective date`, `total awarded`, `budget`, `indirect`, `F&A`, `MTDC`, `TDC`, `cost share`, `cost reimbursable`, `fixed price`, `letter of credit`, `PMS`, `drawdown`, `invoice`, `Net 30`, `final invoice`, `closeout`, `2 CFR 200`, `prior approval`, `carry forward`, `unobligated`.

Return a single JSON object that validates against [`schema.json`](schema.json) with these top-level keys:

- `award_identification` — object covering core identifiers, project title, PI, award type, pass-through, CFDA, NAICS, agency.
- `dates_and_performance` — object covering award and performance dates plus the optional multi-year budget-period table.
- `sponsor_entity` — object covering sponsor name + entity type + agency hierarchy + address + sponsor and awardee UEIs.
- `budget_financial` — object covering total amounts, line-item budget breakdown, F&A rate / base, cost share, program income.
- `billing_payment` — object covering billing type / frequency / address / email / PMS LOC code / payment terms / invoice requirements / final invoice deadline / billing contact.
- `reporting_special` — object covering reporting requirements table + record retention + carry-forward policy + prior-approval list + special terms + closeout + governing regulations.

### Critical: monetary fields are JSON numbers, not strings

This is the contract requirement that the boss flagged on the previous batch. Convert any quoted dollar amount to a JSON number:

- `"$1,234,567.89"` → `1234567.89`
- `"$500,000"` → `500000`

Apply this rule to every numeric field below:

- `budget_financial.total_award_amount`
- `budget_financial.total_anticipated_amount`
- `budget_financial.total_direct_costs`
- `budget_financial.total_indirect_costs`
- `budget_financial.cost_share_amount`
- `budget_financial.budget_categories[].approved_amount`

`fa_rate` is a **string** (preserve the document's percentage notation, e.g., `"56.5%"`, `"30% MTDC"`). `fa_rate_base` is a string enum.

### Dates use ISO YYYY-MM-DD

When the document is unambiguous (e.g., `"July 1, 2026"`), emit `"2026-07-01"`. When the document gives a qualitative period (e.g., `"period of performance: 5 years from award acceptance"`), preserve the document's stated form as a string. Apply this rule to:

- `dates_and_performance.award_start_date`, `award_end_date`
- `dates_and_performance.performance_period_start`, `performance_period_end`
- `dates_and_performance.budget_periods[].start_date`, `end_date`

### Enums — match exactly

- `award_identification.award_type`: `"Grant"`, `"Cooperative Agreement"`, `"Contract"`, `"Subcontract"`
- `sponsor_entity.sponsor_entity_type`: `"Federal"`, `"State Government"`, `"Non-Profit"`, `"Private Industry"`, `"Foundation"`, `"University"`, `"Other"`
- `budget_financial.fa_rate_base`: `"MTDC"`, `"TDC"`, `"Salary & Wages"`, `"Other"`, or `null`
- `billing_payment.billing_type`: `"Cost Reimbursement"`, `"Fixed Price"`, `"Letter of Credit"`, `"Milestone"`

### Required-field policy

Mirror the source workflow's `Is_Required: true` fields into the schema's `required` lists at the block level:

- `award_identification`: `award_number`, `project_title`, `pi_name`, `award_type`, `is_pass_through`, `federal_agency_name`
- `dates_and_performance`: `award_start_date`, `award_end_date`, `performance_period_start`, `performance_period_end`
- `sponsor_entity`: `sponsor_name`, `sponsor_entity_type`, `awardee_organization`
- `budget_financial`: `total_award_amount`, `budget_categories`
- `billing_payment`: `billing_type`
- `reporting_special`: `reporting_requirements`

`reporting_special.reporting_requirements` is a required array of `{report_type, frequency, due_date_or_timing, submission_method}` objects.

### budget_categories shape

`budget_categories` is a required array of `{category, approved_amount}` objects. `category` is the sponsor's exact category label (e.g., `"Salary"`, `"Fringe"`, `"Equipment"`, `"Travel"`, `"Operating/Supplies"`, `"Subcontracts"`, `"Other"`). `approved_amount` is a JSON number.

### Cross-field rules (from source workflow)

1. `award_start_date < award_end_date` (when both are populated).
2. `performance_period_start <= award_start_date` (when both are populated). When this does not hold, the consolidator should flag it in `reporting_special.special_terms` rather than altering the dates.

### Encoding rules

1. **Monetary values are JSON numbers.** No quoted dollar amounts.
2. **Dates use ISO YYYY-MM-DD when unambiguous**, otherwise preserve the document's stated form as a string.
3. **Booleans are JSON booleans.**
4. **UEIs**, when present, are 12-character alphanumeric strings. Preserve case.
5. **CFDA numbers** are stored as strings (preserves leading zeros and `XX.XXX` format).
6. **Empty optional fields use `null`** (scalars) or `[]` (arrays). Do not invent values.
7. **Reporting requirements table** is a flat array of typed rows; do not nest sub-tables.

### Output

A single JSON object. No surrounding markdown.
