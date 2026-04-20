---
name: nsf-award-notice-extraction-udm
version: 1.1.0
description: Extracts an NSF Award Notice (or amendment notice) into a single structured JSON object conforming to this library's Unified Data Model extension for research administration. Use when the input is an NSF-formatted Notice of Award — an initial obligation (Amendment 000) or any subsequent amendment — typically arriving as a PDF printed from Outlook. Also use when a user uploads an "NSF NOA", "NSF award letter", or "NSF award notice" and wants machine-readable output for ingest into a grants management system, database, or compliance workflow. Output is a flat JSON with identity scalars, funding scalars, indirect cost fields, recipient and budget-period objects, eight categorized arrays (project personnel, sponsor contacts, budget categories, subawards, linked awards, terms and conditions, special conditions), a top-level fees scalar, and an optional source_provenance audit object. For the human-readable summary form or for non-NSF award notices, use a different component.
---

# NSF Award Notice Structured Extraction — UDM JSON Skill

Extracts an NSF Award Notice into one JSON object suitable for direct ingest into a UDM-conformant data store. Output is machine-readable — not a human summary.

## When to use

- The input is an NSF Award Notice (initial or amendment), typically a PDF printed from an emailed NSF notification
- The user wants structured award data for ingest, database loading, compliance automation, or diffing
- The user references "NOA", "award letter", "award notice", or provides an NSF-formatted notice
- The user wants to populate an Award or AwardModification record from a notice

For non-NSF award documents (NIH NOA, DOE award letters, foundation grants), this skill's extraction heuristics may not apply cleanly — prefer a sponsor-specific skill when available.

## Output contract

Emit exactly one JSON object. No preamble, no commentary, no markdown outside the JSON itself.

The object contains:

- **Identity scalars:** `award_id`, `award_number` (FAIN), `sponsor_award_number`, `award_title`, `sponsor_name`, `managing_division`, `award_instrument`, `award_status`, `is_research_and_development`, `is_collaborative_research`, `funding_opportunity_number`, `funding_opportunity_title`, `cfda_number`, `cfda_name`, `proposal_number`, `amendment_number`, `amendment_type`, `amendment_date`, `amendment_description`
- **Date and funding scalars:** `award_date`, `award_received_date`, `start_date`, `end_date`, `amount_obligated_this_amendment`, `total_intended_amount`, `total_obligated_to_date`, `cost_share_approved_amount`, `expenditure_limitation`, `indirect_cost_rate_percent`, `indirect_cost_base`, `fees`
- **Nested objects:** `recipient_organization` (legal name, address, email, UEI), `current_budget_period` (period_number, start/end dates, direct/indirect cost, obligated amount), optional `source_provenance` (extractor identity, version, source document id, reviewer annotations)
- **Eight required arrays** (always present, emit `[]` when empty): `project_personnel`, `sponsor_contacts`, `budget_categories`, `subawards`, `linked_awards`, `terms_and_conditions`, `special_conditions`

See `schema.json` in this component for the authoritative definition.

## Amendment 000 vs. subsequent amendments

Both produce the same output shape. The ingest service uses `amendment_number` to decide whether to create an Award record (000) or an AwardModification record (001+).

## Key rules

- **Dates:** ISO `YYYY-MM-DD`. US-format `09/10/2024` → `2024-09-10`.
- **Currency:** plain numbers. `$4,546,903` → `4546903`.
- **Indirect cost rate:** plain number, no `%`. `38.0000%` → `38.0`.
- **Indirect cost base:** map verbatim phrase to enum — "Modified Total Direct Costs" → `"MTDC"`, "Total Direct Costs" → `"TDC"`, "Total Federal Funds Awarded" → `"TFFA"`, "Salaries and Wages" → `"SWB"`, otherwise `"Other"`.
- **Cost share:** emit `0` (not null) when the notice explicitly says no cost share.
- **Fees:** populate the top-level `fees` scalar when the NSF budget prints a distinct Fees row between J and L. Do not also emit a `budget_categories` entry for it (code enum is A–M only).
- **Received date:** use the email header's `Date:` line (the notice is typically a printed email). Null when absent.
- **Sponsor name:** always the full name (e.g., `"National Science Foundation"`). Do not abbreviate.
- **Source provenance:** populate the optional `source_provenance` object when the runtime supplies a source document identifier or expects an audit trail (extractor name, version, source document id, timestamp). Emit `null` when no provenance info is available.

## Budget categories

Emit one entry per line item actually printed in the NSF-format budget (A–M). Include stated totals (H, J, L) as their own entries; do not recompute. Use conventional subcodes:

- B: `PostDoctoral`, `OtherProfessionals`, `GraduateStudents`, `UndergraduateStudents`, `SecretarialClerical`, `Other`
- E: `Domestic`, `International`
- F: `Stipends`, `Travel`, `Subsistence`, `Other`, `TotalParticipants`, `Total`
- G: `MaterialsSupplies`, `Publication`, `ConsultantServices`, `ComputerServices`, `Subawards`, `Other`, `Total`
- H / I / J / K / L / M: null subcode for single-line totals

For personnel lines, also fill `count`, `calendar_months`, `academic_months`, `summer_months` from the printed values.

## Subaward inference

NSF notices rarely itemize subrecipients with allocations — they show a single `G.Subawards` line and a Co-PI list. Two entry types:

1. **Explicit:** when the notice names a subrecipient, emit with `inferred: false`.
2. **Inferred:** when at least one Co-PI has `is_at_recipient_institution: false` AND `G.Subawards` is non-zero, emit one entry per non-recipient Co-PI organization with `inferred: true`, Co-PI name/email in the entry, and a description explaining the basis. Amounts (`obligated_amount`, `anticipated_amount`) stay null.

## Collaborative Research

Set `is_collaborative_research: true` when the title begins `"Collaborative Research:"` or the notice explicitly says so. Sibling FAINs go in `linked_awards` with `relationship: "collaborative_sibling"` — only when the notice names them.

## Terms and conditions

One entry per distinct cited authority. Typical NSF citations:

- National Science Foundation Act of 1950 (statutory, applicability note `"42 U.S.C. 1861-75"`)
- Research Terms and Conditions (dated)
- NSF Agency Specific Requirements (dated)
- PAPPG (usually cited by chapter for a specific purpose; put the chapter in `applicability_notes`)

## Special conditions

Walk the Amendment Description and other narrative; emit one entry per distinct condition. Categorize via the schema enum (`reporting`, `scope`, `budget`, `subaward`, `participant_support`, `personnel`, `compliance`, `publications`, `data_sharing`, `other`). Set `action_required: true` when the recipient must take action (maintain segregated accounts, obtain prior approval, submit something). Preserve the condition's wording in `description`; set `source_section` to the notice section the condition came from.

## Quality standards

1. Completeness — every printed value appears in the output.
2. Precision — the notice's exact wording for prescribed text; numbers preserved after format normalization.
3. Typed fidelity — JSON types, not strings.
4. Schema conformance — validates against `schema.json`; all eight arrays present.
5. No fabrication — the only inference is the subaward rule above.
6. Preserve anomalies — internal inconsistencies recorded verbatim with a note, not silently corrected.
