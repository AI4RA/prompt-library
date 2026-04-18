---
name: rfp-extraction-udm
version: 1.0.0
description: Extracts a federal funding announcement (RFP, RFA, FOA, NOFO, BAA, Dear Colleague Letter, or program solicitation) into a single structured JSON object conforming to this library's Unified Data Model extension. Use when the user wants machine-readable output — for ingest pipelines, database loading, compliance automation, or programmatic analysis — rather than a human-readable checklist. Output is a flat JSON with scalar opportunity metadata plus nine categorized requirement arrays (documents, formatting, review criteria, eligibility, budget constraints, compliance, submission requirements, special conditions, parent-guide deviations).
---

# RFP Structured Extraction — UDM JSON Skill

Extracts a funding announcement into a single JSON object suitable for ingest into a UDM-conformant data store. The output is NOT a human-readable checklist — it is structured data keyed for programmatic consumption. For the human-readable checklist form, use `rfp-extraction` instead.

## When to use

- The user wants a machine-readable output (ingest pipeline, database load, validation, diffing)
- The user references a schema, data model, UDM, or "structured extraction"
- The output will be consumed by another system rather than read by a person
- The user asks for a JSON version of an earlier checklist extraction

## Output contract

Emit exactly one JSON object. No preamble, no commentary, no markdown outside the JSON itself. If the runtime requires a fence, use a single ` ```json ... ``` ` block and emit nothing else.

The object contains:

- **Scalar fields** — opportunity metadata: `rfa_id`, `rfa_number`, `rfa_title`, `sponsor_name`, `program_code`, `announcement_url`, `opportunity_number`, `cfda_number`, `announcement_date`, `submission_deadline`, `loi_deadline`, `preproposal_deadline`, `funding_floor`, `funding_ceiling`, `expected_awards`, `max_duration_months`, `submission_method`, `rfa_status`.
- **Nine requirement arrays** — every one MUST be present (emit `[]` when empty): `required_documents`, `formatting`, `review_criteria`, `eligibility`, `budget_constraints`, `compliance`, `submission_requirements`, `special_conditions`, `pappg_deviations`.

Each requirement entry has: `label` (required), `code`, `description`, `page_limit`, `format_spec`, `is_required` (required boolean), `source_section`, `structured_rule_type`, `structured_rule_value`. See `schema.json` in this component for the authoritative definition.

## Key rules

- **Dates:** ISO `YYYY-MM-DD`. Drop times; document timezone as a `submission_requirements` entry.
- **Currency:** plain numbers in USD (no `$`, no commas, no strings).
- **Durations:** months. Convert years by `× 12`. Document conditional extensions (e.g., "4th year with phase-out") in `special_conditions`.
- **Multi-round announcements:** scalar deadlines hold the LAST round's date; emit one `special_conditions` entry per round with `label` like `"Round N — Full Proposal Deadline"` and the round's ISO date in `description`.
- **Sponsor name:** full agency name (e.g., `"National Science Foundation"`). Do not abbreviate. Lead sponsor only in `sponsor_name`; list partner agencies in `special_conditions`.
- **Parent-guide inheritance:** when the announcement defers to PAPPG / SF424 / Merit Review Guide / BAA instructions, include that guide's standard requirements with `source_section` pointing to the guide. Where the announcement overrides the guide, also emit a `pappg_deviations` entry naming what changed.
- **"No restriction" confirmations:** emit as `eligibility` entries with `is_required: true` and a description recording the non-restriction. Absence of a restriction is a compliance fact.
- **Structured rules:** encode enforceable rules (cost sharing, salary caps, proposal limits, PI degree) via `structured_rule_type` + `structured_rule_value` using stable snake_case identifiers. Common types: `cost_sharing` (values: `prohibited` / `required` / `optional` / `required_<N>_percent`), `proposal_limit_per_institution` (integer), `pi_degree_required`, `salary_cap_annual_usd`, `indirect_cost_cap_percent`.

## Extraction procedure

1. Read the entire announcement before emitting output — critical constraints hide in unexpected sections.
2. Populate every scalar. Parse dates to ISO, currency to numbers, duration to months.
3. Walk each of the nine requirement categories. Extract every entry the announcement states; do not omit routine items; do not invent items not stated.
4. For each entry, populate `source_section` whenever traceable. Use the announcement's exact wording for prescribed headers and titles; preserve numbers verbatim.
5. For any ambiguity or apparent error, emit the item as stated and flag it in `description`. Do not silently pick an interpretation.

## Quality standards

1. Completeness — every stated requirement appears as an entry.
2. Precision — exact wording for prescribed text; numbers preserved verbatim.
3. Actionability — each entry describes a verifiable fact.
4. Typed fidelity — JSON types, not strings. Never emit `"null"` as a string.
5. Schema conformance — validates against `schema.json`. All nine requirement arrays present.
