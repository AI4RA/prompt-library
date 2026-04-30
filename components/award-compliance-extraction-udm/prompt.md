---
name: award-compliance-extraction-udm
version: 0.1.0
category: extraction
domain: research-administration
status: experimental
tags: [post-award, compliance, financial-management, federal-awards, terms-and-conditions, 2-cfr-200, audit, udm, structured-extraction, json]
audience: [sponsored-programs-staff, post-award-teams, ingest-pipelines]
owner: ui-insight
created: 2026-04-30
updated: 2026-04-30
---

# Award Compliance & Financial Overview Extraction — UDM JSON

> **Purpose:** Extract the compliance framework and financial-management requirements from a federal award document into a single structured JSON object that drives a consolidated "Award Compliance & Financial Overview" deliverable for post-award setup and monitoring.
> **Expected input:** Full text of a federal award notice / agreement / terms-and-conditions document.
> **Expected output:** A single JSON object that validates against [`schema.json`](schema.json). No prose, no markdown outside the JSON.

## When to use this contract

This is the post-award setup cut of a federal award. It produces two main blocks — `compliance_framework` (10 fields covering Uniform Guidance applicability, RTC applicability, financial reporting, progress reporting, prior approvals, budget modification, property, deliverables, high-risk conditions, and a normalized compliance calendar) and `financial_management` (10 fields covering total award amount, budget periods, cost-share, F&A rate and base, performance period, budget categories, FFR cadence, audit requirements, and record retention).

UDM-aligned: `total_award_amount` → `Award.Current_Total_Funded`; `budget_period_amounts` → `AwardBudgetPeriod`; `cost_share_requirements` → `CostShare.Committed_Amount`; `fa_rate` → `IndirectRate.Rate_Percentage`; `fa_rate_base` → `IndirectRate.Base_Type`; `performance_period` → `Award.Original_Start_Date`; `budget_categories` → `AwardBudget`; `ffr_requirements` and `financial_reporting_requirements` → `Terms.Reporting_Requirements`; `progress_reporting_requirements` and `deliverable_requirements` → `AwardDeliverable`; `prior_approval_requirements` → `Modification.Requires_Prior_Approval`; `property_requirements` → `Terms.Property_Requirements`; `record_retention` → `Terms.Record_Retention_Years`; `high_risk_conditions` → `Terms.Special_Conditions`.

This component does **not** cover the FFR submission cadence in detail — that lives in `ffr-management-extraction-udm`. It does not cover the prior-approval procedures table — that lives in `prior-approval-extraction-udm`.

---

## Prompt

You are extracting the compliance framework and financial-management requirements from a federal award document. Capture both the **regulatory framework** that governs the award (Uniform Guidance, RTC, agency policy, high-risk conditions) and the **financial management** structure (award amounts, budget structure, cost share, F&A, FFR cadence, audit thresholds).

**Be 100% accurate.** Numeric fields and string fields have different rendering rules — the contract is the schema, not the surface form:

- **Schema fields typed as `number` (`total_award_amount`, `budget_period_amounts[].amount`, `budget_categories[].approved_amount`)** must be emitted as JSON numbers — no quotes, no currency symbol, no thousand-separators. `$1,234,567.89` in the document → `1234567.89` in JSON. Use the document's exact value; do not round or truncate.
- **Schema fields typed as `string` (`fa_rate`, `fa_rate_base`, `cost_share_requirements`, `performance_period`, etc.)** must be quoted verbatim — preserve the document's exact rendering including currency symbols, percent signs, and date format.

When a field is not specified, set it to `null` (or — for arrays/tables — return an empty array). Do not invent values.

Search the entire document for content in or near sections titled *Terms and Conditions*, *Special Terms and Conditions*, *Administrative Requirements*, *Programmatic Requirements*, *High Risk Terms*, *Federal Requirements*, *Award Amount*, *Budget Information*, *Financial Management*, *Cost Sharing/Matching*, *Indirect Costs*, or *Financial Reporting*. Keywords to follow: condition, requirement, must, shall, comply, report, submit, approve, prior, deadline, CFR, federal, audit, monitor, budget, cost, financial, funding, allowable, FFR, PMS, drawdown, match, share, indirect, record.

Return a single JSON object that validates against [`schema.json`](schema.json) with these top-level keys:

- `award_number` — federal award identification number (FAIN). String or `null`.
- `compliance_framework` — object covering the regulatory framework:
  - `uniform_guidance_applicability` — string or `null`.
  - `rtc_applicability` — string or `null`.
  - `financial_reporting_requirements` — string. Required.
  - `progress_reporting_requirements` — string or `null`.
  - `prior_approval_requirements` — array of strings categorized by approval type. Empty when not applicable.
  - `budget_modification_restrictions` — string or `null`.
  - `property_requirements` — string or `null`.
  - `deliverable_requirements` — array of strings. Empty when none.
  - `high_risk_conditions` — array of strings naming each high-risk condition. Empty when not high-risk.
  - `compliance_calendar` — array of `{requirement_type, deadline, responsible_party, consequences}` objects. Required, empty array when no calendar can be derived.
- `financial_management` — object covering the financial structure:
  - `total_award_amount` — number (decimal). Required.
  - `budget_period_amounts` — array of `{period, start_date, end_date, amount}` objects. Empty when single-period.
  - `cost_share_requirements` — string or `null`.
  - `fa_rate` — string with rate percentage as stated (e.g., `"42.5%"`) or `null`.
  - `fa_rate_base` — string (e.g., `"MTDC"`, `"TDC"`) or `null`.
  - `performance_period` — string with date range (e.g., `"2026-07-01 to 2031-06-30"`). Required.
  - `budget_categories` — array of `{category_name, approved_amount, restrictions, prior_approval_required}` objects.
  - `ffr_requirements` — string or `null`.
  - `audit_requirements` — one of `"Single Audit"`, `"A-133"`, `"Program-Specific Audit"`, `"Not applicable"`, or `null`.
  - `record_retention` — one of `"3 years"`, `"5 years"`, `"7 years"`, `"Per sponsor requirements"`, or `null`.

### Encoding rules

1. **`compliance_calendar` is the consolidated deadline view.** Every requirement that has a recurring or fixed deadline (FFR, progress reports, equipment inventory, audit submission, RTC milestones) becomes one row. Pull from across the document, not just the calendar section.
2. **`prior_approval_requirements` is a categorized list, not a table.** This component exposes only the *categories* (e.g., `"Equipment over $5,000 requires PO approval"`); the procedural mechanics (threshold / timeline / consequences) belong in `prior-approval-extraction-udm`.
3. **`budget_period_amounts` covers multi-year awards.** For single-period awards, return an empty array; the total still lives in `total_award_amount`.
4. **`high_risk_conditions` is for designations the document calls out** — enhanced monitoring, additional reporting, specific restrictions tied to the recipient's risk classification.
5. **`fa_rate` and `fa_rate_base` are two distinct strings.** `"42.5% MTDC"` is two fields: `fa_rate: "42.5%"` (string, percent sign preserved), `fa_rate_base: "MTDC"`.
6. **`total_award_amount` is a JSON number, not a quoted string.** `budget_period_amounts[].amount` and `budget_categories[].approved_amount` are also JSON numbers. The sum of `budget_period_amounts[].amount` must reconcile to `total_award_amount` (downstream cross-field check CFR-01).
7. Do not output any text outside the single JSON object.

### Output

A single JSON object. No surrounding markdown.
