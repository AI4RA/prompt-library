---
name: award-modification-intake-udm
version: 0.1.0
category: extraction
domain: research-administration
status: experimental
tags: [award-modification, post-award, intake, classification, ncne, rebudget, pi-change, additional-funds, udm, structured-extraction, json]
audience: [sponsored-programs-staff, post-award-teams, ingest-pipelines]
owner: ui-insight
created: 2026-05-20
updated: 2026-05-20
---

# Award Modification Intake & Classification — UDM JSON

> **Purpose:** Classify an incoming award amendment document and extract the type-specific fields a Post-Award Specialist needs to enter the modification into Banner. Covers four post-award modification processes — additional funds, no-cost extension (NCE), PI change, rebudget — plus scope change, administrative change, and combined modifications.
> **Expected input:** A single award amendment / modification document (federal notice, sponsor correspondence, executed modification) ranging from one to twenty pages with optional attachments.
> **Expected output:** A single JSON object that validates against [`schema.json`](schema.json). No prose, no markdown outside the JSON.

## When to use this contract

This is the post-award **modification intake** cut of an award document. It produces three structured blocks a Post-Award Specialist uses to set up the modification in Banner: the **identification** block classifies the modification type and captures core identifiers, the **financial** block captures monetary impact and rebudget routing, and the **compliance** block captures sponsor conditions, prior-approval status, and Financial-Unit routing flags.

This component does **not** cover broader post-award compliance monitoring (high-risk conditions, audit thresholds, deliverable schedules) — that lives in `award-compliance-extraction-udm`. It does not cover FFR submission cadence — that lives in `ffr-management-extraction-udm`. It does not cover prior-approval procedural mechanics (threshold / authority / documentation / timeline / consequences) — that lives in `prior-approval-extraction-udm`.

The source process-mapping workflow includes a human-review `ApprovalNode` step that pauses for Post-Award Specialist sign-off before Banner entry. That review is a runtime workflow concern (Vandalizer's UI handles operator approval) and is not part of this extraction contract.

---

## Prompt

You are extracting the contents of a federal award modification / amendment document for a Post-Award Specialist's Banner intake.

**Be 100% accurate.** Quote the document for any amount, date, identifier, or sponsor-imposed condition; never paraphrase a monetary value or deadline. When the document does not specify a value, set the field to `null` (or, for required string fields where the source workflow specified a `Not_Found_Value`, use that exact string). Do not invent values.

Search the entire document with attention to sections titled *Cover Page*, *Amendment Information*, *Modification Details*, *Award Information*, *Personnel Changes*, *Budget Information*, *Financial Details*, *Cost Sharing*, *Terms and Conditions*, *Special Conditions*, *Approval Information*, and *Regulatory Requirements*. Keywords to follow: `amendment`, `modification`, `no-cost extension`, `additional funds`, `PI change`, `rebudget`, `FAIN`, `effective date`, `principal investigator`, `budget`, `funding`, `obligated`, `indirect`, `F&A`, `cost share`, `prior approval`, `2 CFR`, `IBC`, `biosafety`.

Return a single JSON object that validates against [`schema.json`](schema.json) with these top-level keys:

- `identification` — object covering core identifiers and modification-type classification.
- `financial` — object covering monetary impact, F&A, cost share, and rebudget routing.
- `compliance` — object covering prior-approval status, sponsor conditions, regulatory references, and operational routing flags.

### Identification block

- `award_number` — string. Federal Award Identification Number (FAIN) or sponsor award number. **Required.** Resolves to UDM `Award.Award_Number` / `Award.Federal_Award_ID`.
- `amendment_number` — string. Amendment or modification number (e.g., `"Amendment 17"`, `"Mod 003"`). **Required.**
- `modification_type` — one of `"Additional Funds"`, `"No-Cost Extension"`, `"PI Change"`, `"Rebudget"`, `"Scope Change"`, `"Administrative Change"`, `"Combined (multiple types)"`. **Required.** Use `"Combined (multiple types)"` only when the document genuinely modifies multiple categories; otherwise pick the single primary type.
- `execution_status` — one of `"Unilateral (fully executed)"`, `"Bilateral (requires signature)"`, `"Not specified in the document"`. **Required.**
- `effective_date` — string in ISO `YYYY-MM-DD` form when the document is unambiguous; otherwise quote the document. `null` when absent.
- `sponsor_name` — string. Full name of the sponsoring agency. `null` when absent. Resolves to UDM `Organization.Organization_Name`.
- `pi_name` — string. Current Principal Investigator on the award. `null` when absent. Resolves to UDM `Personnel.First_Name` / `Personnel.Last_Name`.
- `old_pi`, `new_pi` — strings. Populate both **only** when `modification_type` is `"PI Change"` or `"Combined (multiple types)"` and the document identifies the swap; otherwise `null`.
- `new_end_date` — string in ISO `YYYY-MM-DD` form. Populate **only** when `modification_type` is `"No-Cost Extension"` or `"Combined (multiple types)"`; otherwise `null`.
- `pms_code` — string. Payment Management System code if the document states it; `null` otherwise.
- `point_of_contact_changes` — string. Any changes to sponsor point-of-contact information; `null` when none.

### Financial block

All monetary fields below are JSON numbers, not quoted strings. Convert document language verbatim to a numeric value: `"$1,234,567.89"` → `1234567.89`. `null` when the document does not state a value. Do not invent numeric values from context.

- `modification_amount` — number or `null`. The dollar amount of the modification itself (additional funds added or rebudget amount). Resolves to UDM `Modification.Funding_Amount_Change`.
- `current_award_amount` — number or `null`. Current total award amount **before** this modification. Resolves to UDM `Award.Current_Total_Funded`.
- `total_obligated_amount` — number or `null`. Total obligated amount **after** this modification.
- `fa_rate` — string or `null`. F&A (indirect cost) rate. Preserve the sponsor's format (`"30% MTDC"`, `"56.5%"`). String, not a number, because the rate often carries the base annotation. Resolves to UDM `IndirectRate.Rate_Percentage`.
- `fa_amount` — number or `null`. F&A (overhead) dollar amount attributable to this modification.
- `budget_breakdown` — array of `{category, approved_amount}` objects. `category` is the sponsor's category label exactly as stated (e.g., `"Salaries"`, `"Fringe"`, `"Equipment"`, `"F&A"`). `approved_amount` is a number. Empty array when the document does not break down the modification by category. Resolves to UDM `AwardBudget`.
- `rebudget_source_account` — string or `null`. Source budget account for rebudget (e.g., `"OE/Account 30"`). Populate only when `modification_type` is `"Rebudget"` or `"Combined (multiple types)"`.
- `rebudget_destination_account` — string or `null`. Destination budget account for rebudget. Same applicability as `rebudget_source_account`.
- `cost_share_changes` — string or `null`. Any sponsor-imposed changes to cost-share commitments. Resolves to UDM `CostShare.Committed_Amount`.

### Compliance block

- `prior_approval_required` — boolean. Whether the modification required (or grants) sponsor prior approval. **Required.** Resolves to UDM `Modification.Requires_Prior_Approval`.
- `approval_date` — string in ISO `YYYY-MM-DD` form. Date the sponsor approved the modification; `null` when absent.
- `sponsor_conditions` — array of strings. Conditions, restrictions, or requirements imposed by the sponsor as part of the modification. Empty array when none. Resolves to UDM `Terms.Special_Conditions`.
- `regulatory_references` — array of strings. References to regulatory requirements (`"2 CFR 200.308"`, `"Research Terms and Conditions"`, `"NSF PAPPG VI.D"`). Empty array when none.
- `end_date_change` — boolean. Whether the modification changes the project end date. **Required.**
- `requires_financial_unit` — boolean. Whether the modification requires Financial Unit processing. **Required.** Source workflow rule: `true` for additional funds and NCE; `false` for rebudgets and most administrative changes. Decide from the document and the modification type, not from a default.
- `ibc_protocols_required` — boolean or `null`. Whether Institutional Biosafety Committee protocols must be complete before processing this modification. `null` when the document does not address biosafety.

### Cross-field rules

Mirror the source workflow's cross-field rules — apply them when assembling the JSON, do not violate them silently:

1. If `modification_type` is `"Additional Funds"`, `modification_amount` must be a positive number (`> 0`).
2. If `modification_type` is `"No-Cost Extension"`, `new_end_date` must be populated.
3. If `modification_type` is `"PI Change"`, both `old_pi` and `new_pi` must be populated.
4. If `modification_type` is `"Additional Funds"`, `total_obligated_amount` should equal `current_award_amount + modification_amount` when all three are present. If the document's stated totals do not satisfy this identity, **do not adjust the values** — emit the document's numbers as stated and capture the discrepancy in `compliance.sponsor_conditions` as a flag (e.g., `"Stated totals do not reconcile: $X current + $Y modification != $Z obligated"`).

### Encoding rules

1. **Monetary values are JSON numbers, not strings.** `"$1,234,567"` → `1234567`. `"$0.5M"` → do not invent precision; emit the document's stated number, or `null` if the document only gives a rounded summary without a specific amount.
2. **Dates use ISO `YYYY-MM-DD` whenever the document is unambiguous.** When the document gives a granular qualifier the schema cannot capture (e.g., `"30 days after PO issuance"`), keep the value as a string and place it where the schema allows a string, never invent a date.
3. **Booleans are JSON booleans, not the strings `"true"` / `"false"`.**
4. **Enum values must match exactly.** The classification, execution-status, and other enums are case-sensitive. Pick the closest enum; only use catch-all values (`"Combined (multiple types)"`, `"Administrative Change"`) when no better fit exists.
5. **Do not duplicate facts across blocks.** Award identifiers live in `identification`; monetary values live in `financial`; compliance / approval terms live in `compliance`.
6. **No invention.** When the document does not state a value, emit `null` (scalars) or `[]` (arrays). For the three optional `Not_Found_Value` strings in the source workflow (`"Not specified in the document"`, `"Not applicable"`, `"No changes indicated"`), emit `null` instead — the schema accepts `null` for these fields. The exception is `execution_status`, which has `"Not specified in the document"` as an explicit enum value.

### Output

A single JSON object. No surrounding markdown.
