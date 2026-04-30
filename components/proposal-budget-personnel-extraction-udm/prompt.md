---
name: proposal-budget-personnel-extraction-udm
version: 0.1.0
category: extraction
domain: research-administration
status: experimental
tags: [pre-award, proposal, budget, personnel, mentoring-plan, compliance-triggers, nsf, udm, structured-extraction, json]
audience: [sponsored-programs-staff, pre-award-teams, ingest-pipelines]
owner: ui-insight
created: 2026-04-30
updated: 2026-04-30
---

# Proposal Budget Personnel & Compliance Triggers — UDM JSON

> **Purpose:** Extract personnel information and compliance-requirement triggers from a proposal budget document into a structured JSON object. Identifies senior key personnel, postdocs, graduate students, undergraduates, and other personnel; the budget category structure; subaward recipients, equipment over $5,000, travel summary, F&A rate and base, cost sharing, and total costs. The output drives a downstream pre-award document-completeness review.
> **Expected input:** A proposal budget document (NSF-style budget tables / NIH PHS 398 / agency budget form), optionally with a budget justification.
> **Expected output:** A single JSON object that validates against [`schema.json`](schema.json). No prose, no markdown outside the JSON.

## When to use this contract

This is the proposal-budget cut for compliance-trigger derivation. It pairs with `proposal-document-completeness-udm` — the gap-analysis component consumes `senior_key_personnel`, `has_postdocs_or_grad_students`, `has_subawards`, and `has_equipment_over_5k` from this output to compute its conditional requirements.

UDM-aligned: `senior_key_personnel` rows resolve to `Personnel`; `fa_rate_and_base` resolves to `IndirectRate`; `cost_sharing` resolves to `CostShare`.

This component does **not** cover the full document-completeness gap analysis — that lives in `proposal-document-completeness-udm`. It does not cover the post-award budget structure — that lives in `award-compliance-extraction-udm.financial_management`.

---

## Prompt

You are extracting personnel information and compliance-requirement triggers from a proposal budget document. Your output drives a downstream document-completeness review, so the booleans (`has_postdocs_or_grad_students`, `has_subawards`, `has_equipment_over_5k`, `mentoring_plan_required`) must be **derivable from the extracted lists** — never set a boolean except by counting the corresponding list.

**Be 100% accurate.** Quote dollar amounts and effort percentages verbatim. When a category is empty, return an empty array; when a scalar is not specified, return `null`. Do not invent personnel, subawardees, or equipment items.

Search the entire budget for content in or near sections titled *Senior/Key Personnel*, *Other Personnel*, *Personnel*, *Section A — Senior/Key Person*, *Section B — Other Personnel*, *Salary and Wages*, *Personnel Justification*, *Budget*, *Budget Summary*, *Cumulative Budget*, *Subaward*, *Subcontract*, *Equipment*, *Travel*, *Other Direct Costs*, *Indirect Costs*.

Return a single JSON object that validates against [`schema.json`](schema.json) with these top-level keys:

- `senior_key_personnel` — array of `{name, role, institution, effort, salary_requested}` objects. One row per senior/key person.
- `postdoc_count` — integer (count of postdoctoral researchers in the budget).
- `postdoc_details` — array of `{name, effort, salary_or_stipend}` objects (use empty string or `"TBN"` for unnamed slots). Empty when `postdoc_count: 0`.
- `graduate_student_count` — integer.
- `graduate_student_details` — array of `{name, type, stipend, tuition_remission}` objects. `type` is `"RA"` or `"TA"`. Empty when count is 0.
- `undergraduate_count` — integer.
- `other_personnel` — array of `{role, cost}` objects (technicians, programmers, administrative staff). Empty when none.
- `total_personnel_cost` — number (decimal). Total personnel costs including salary and fringe.
- `has_postdocs_or_grad_students` — boolean. Must equal `(postdoc_count > 0) OR (graduate_student_count > 0)`.
- `mentoring_plan_required` — boolean. Equals `has_postdocs_or_grad_students` for NSF; for non-NSF sponsors set per agency policy.
- `budget_categories` — array of `{category_name, amount, notes}` objects.
- `subaward_recipients` — array of `{institution_name, sub_pi_name, amount}` objects.
- `has_subawards` — boolean. Must equal `len(subaward_recipients) > 0`.
- `equipment_items` — array of `{description, cost}` objects (items over $5,000 only).
- `has_equipment_over_5k` — boolean. Must equal `len(equipment_items) > 0`.
- `travel_summary` — string with domestic/foreign travel summary or `null`.
- `fa_rate_and_base` — object `{rate, base}` where `base` is one of `"MTDC"`, `"TDC"`, `"Salary & Wages"`, or `null`.
- `cost_sharing` — string with cost-sharing amount and type or `null`.
- `total_costs` — object `{total_direct_costs, total_indirect_costs, total_project_cost}`. All numbers.
- `budget_periods` — array of `{period_number, start_date, end_date, amount}` objects (multi-year). Empty for single-period.

### Encoding rules

1. **Booleans are derived, not transcribed.** `has_postdocs_or_grad_students`, `mentoring_plan_required`, `has_subawards`, and `has_equipment_over_5k` are computed from the corresponding list lengths/counts. Setting a boolean inconsistent with its derivation is a downstream `CHK-02` failure.
2. **Equipment threshold is $5,000.** Items below the threshold do not appear in `equipment_items` (regardless of whether the budget calls them "equipment").
3. **Postdoc / graduate-student names may be unknown.** If the budget lists a "Postdoc to be named" or "GRA TBN", use `name: "TBN"` so per-person document workflows can flag a missing-name dependency without dropping the row.
4. **`fa_rate_and_base` is two-part.** `"42.5% MTDC"` → `{rate: "42.5%", base: "MTDC"}`.
5. **`total_costs` reconciliation.** `total_project_cost == total_direct_costs + total_indirect_costs` (downstream `CHK-03`).
6. **`graduate_student_details.type` enum.** Use `"RA"` (Research Assistant) or `"TA"` (Teaching Assistant) per the budget's classification.
7. Do not output any text outside the single JSON object.

### Output

A single JSON object. No surrounding markdown.
