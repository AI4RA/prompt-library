---
name: prior-approval-extraction-udm
version: 0.1.0
category: extraction
domain: research-administration
status: experimental
tags: [prior-approval, post-award, modifications, federal-awards, rtc, 2-cfr-200, compliance, udm, structured-extraction, json]
audience: [sponsored-programs-staff, post-award-teams, ingest-pipelines]
owner: ui-insight
created: 2026-04-30
updated: 2026-04-30
---

# Prior Approval Extraction — UDM JSON

> **Purpose:** Extract all prior-approval requirements from a federal award document into a structured JSON object suitable for driving a tracking system of activities that need federal-agency authorization before they can be executed.
> **Expected input:** Full text of a federal award notice / agreement / terms-and-conditions document, optionally with Research Terms and Conditions (RTC) or 2 CFR 200 as knowledge-base context.
> **Expected output:** A single JSON object that validates against [`schema.json`](schema.json). No prose, no markdown outside the JSON.

## When to use this contract

This is the prior-approval cut of a federal award. It produces three logical buckets — **budget-related**, **scope and timeline**, and **administrative** approvals — plus a normalized **approval procedures** table (threshold / documentation / authority / timeline / consequences) and a list of **RTC waivers** delegated to the recipient. UDM-aligned: `requires_prior_approval` flags resolve to UDM `Modification.Requires_Prior_Approval`; subaward approval requirements resolve to `Subaward`.

This component does **not** cover the broader compliance framework (financial reporting, high-risk conditions, audit thresholds) — that lives in `award-compliance-extraction-udm`. It does not cover the FFR submission cadence — that lives in `ffr-management-extraction-udm`.

---

## Prompt

You are extracting prior-approval requirements from a federal award document. Federal awards typically distinguish three families of activities that require sponsor authorization before they can occur: budget changes, scope/timeline changes, and administrative changes (PI substitutions, foreign travel, subawards, etc.). Capture **every** approval the document calls out, plus the procedures the recipient must follow.

**Be 100% accurate.** Quote thresholds (`"$25,000"`, `"25%"`, `"three months"`) verbatim; never paraphrase a numeric threshold. When a category is not addressed, set the field to `null`. When the document explicitly waives an approval (typically via Research Terms and Conditions or expanded authorities), capture the waiver in `rtc_waivers`.

Search the entire document for content in or near sections titled *Prior Approval*, *Pre-approval*, *Written Approval*, *Agency Approval*, *2 CFR 200*, or *Research Terms and Conditions*. Keywords to follow: `prior approval`, `pre-approval`, `written approval`, `agency approval`, `permission`, `authorize`, `CFR 200`, `RTC`, `waive`, `delegate`, `threshold`.

Return a single JSON object that validates against [`schema.json`](schema.json) with these top-level keys:

- `award_number` — federal award identification number (FAIN). String or `null`.
- `budget_approvals` — object covering money-driven approvals:
  - `rebudgeting_thresholds` — string or `null`.
  - `equipment_approvals` — string or `null`.
  - `subaward_approvals` — string or `null`.
- `scope_timeline_approvals` — object covering scope and time-driven approvals:
  - `pi_change_requirements` — string or `null`.
  - `nce_requirements` — string or `null`.
  - `foreign_travel_approvals` — string or `null`.
- `approval_procedures` — array of `{approval_type, threshold, documentation, authority, timeline, consequences}` objects. Each row in the source approval-procedures table becomes one entry. Empty array when the document has no procedures table.
- `rtc_waivers` — array of strings naming each Research Terms and Conditions waiver or expanded-authority delegation the document calls out. Empty array when none are stated.

### Encoding rules

1. **One row per approval type in `approval_procedures`.** A single row that says "Equipment > $5,000 requires written approval from PO within 30 days" becomes one entry with `approval_type: "Equipment over $5,000"`, `threshold: "$5,000"`, `authority: "Program Officer"`, `timeline: "30 days"`. Quote dollar thresholds and day-counts verbatim.
2. **Per-row text goes on the row, not in the top-level bucket.** If the procedures table covers an approval type, the corresponding `budget_approvals.*` or `scope_timeline_approvals.*` field should be a *narrative* description; the procedure mechanics belong in the table row.
3. **`rtc_waivers` is for waived approvals only** — items that the RTC or agency expanded authority lets the recipient handle without sponsor sign-off. Do not duplicate the *kept* approvals here.
4. **Boolean flags must be derivable.** Downstream UDM ingest expects to be able to compute `Modification.Requires_Prior_Approval` from the presence of an entry; only state an approval requirement when the document actually requires one.
5. Do not output any text outside the single JSON object.

### Output

A single JSON object. No surrounding markdown.
