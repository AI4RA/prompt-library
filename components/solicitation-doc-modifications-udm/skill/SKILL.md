---
name: solicitation-doc-modifications-udm
version: 1.0.0
description: Given a solicitation text (markdown, typically OCR-derived) and a sponsor-defaults JSON object (the output of sponsor-doc-defaults-udm), emits the subset of document requirements the solicitation modifies and the net-new documents it introduces — as a structured JSON list. Use when a pre-award team has a baseline sponsor checklist and needs to adapt it to a specific program, when an ingest pipeline needs to resolve a solicitation's document requirements on top of a sponsor prior, or when a user asks "what does this solicitation change or add beyond the sponsor defaults?". Every entry links back to the default it overrides via modifies_default (null for net-new) and carries a verbatim source_excerpt grounding the modification. Output is one JSON object with sponsor_name / sponsor_division / solicitation_id / solicitation_notes / document_requirements — where document_requirements contains only the diff, not the full merged checklist. Uses the same controlled code vocabulary as sponsor-doc-defaults-udm. Pairs with sponsor-doc-defaults-udm to form a two-pass requirements pipeline.
---

# Solicitation Document Modifications — UDM Skill

Given a solicitation and a sponsor-defaults prior, emits only the **diff** — modifications to the defaults and net-new documents the solicitation introduces. A downstream merge replaces defaults by `code` when `modifies_default` is set, and appends entries where `modifies_default` is null.

## When to use

- A pre-award team has a baseline sponsor checklist and needs to adapt it to a specific program
- An ingest pipeline has resolved sponsor defaults and is now resolving solicitation-specific overrides and additions
- The user asks "what does this solicitation change or add beyond the NSF / NIH defaults?"
- The output will be merged with a sponsor-defaults output to produce the final solicitation checklist

For the baseline set of sponsor defaults, use `sponsor-doc-defaults-udm` first and feed its output into this component.

## Inputs

1. Solicitation text (markdown; OCR-derived is fine).
2. Sponsor-defaults JSON object — the output of `sponsor-doc-defaults-udm`.

## Output contract

Emit exactly one JSON object. No preamble, no commentary, no markdown outside the JSON.

The object contains:

- `sponsor_name` — echoed from the sponsor-defaults input
- `sponsor_division` — echoed from the sponsor-defaults input
- `solicitation_id` — the solicitation's printed identifier (e.g., `"NSF 24-507"`), or null when not discoverable
- `solicitation_notes` — free-text caveats; null when none
- `document_requirements` — array of requirement entries; empty when the solicitation makes no changes

Each entry is a full requirement object (the same fields as `sponsor-doc-defaults-udm`) plus:

- `modifies_default` — the default `code` this entry overrides, or null for net-new
- `source_excerpt` — verbatim text from the solicitation grounding the entry

See `schema.json` in this component for the authoritative definition.

## Controlled `code` vocabulary

`cover_sheet`, `cover_letter`, `project_summary`, `project_narrative`, `proposal_narrative`, `specific_aims`, `references_cited`, `biosketch`, `current_pending`, `collaborators_and_affiliations`, `facilities`, `equipment`, `budget`, `budget_justification`, `data_mgmt`, `postdoc_mentoring`, `mentoring_plan`, `results_prior_support`, `resource_sharing`, `authentication_key_resources`, `leadership_plan`, `human_subjects`, `vertebrate_animals`, `select_agent`, `inclusion_enrollment_report`, `letter_support`, `letter_collaboration`, `letter_of_intent`, `other`.

Same vocabulary as `sponsor-doc-defaults-udm`. Use `other` only when no enumerated code fits.

## Key rules

- **Emit only the diff.** Defaults the solicitation leaves unchanged must not appear. Downstream treats absent codes as pass-through.
- **Verbatim excerpts only.** `source_excerpt` is a literal quote from the solicitation. If you cannot quote grounding text, omit the entry.
- **Full object on modification.** A modification emits every required field, carrying over unchanged values from the default. Downstream replaces the default wholesale.
- **modifies_default is a real default code.** When set, it must be a code present in the sponsor-defaults input.
- **Net-new uses modifies_default: null.** Even when the new document is thematically close to a default, if it is a separate document in the solicitation, it is net-new.
- **No invention.** If the solicitation is silent on a field, do not guess — carry the default's value (for modifications) or use null (for net-new).

## Modification detection

A modification applies when the solicitation changes any of: `page_limit`, `format_spec`, `is_required`, `is_per_person`, `conditional_on`, or the material meaning of `description`. A restatement of a default without change is not a modification.

## Net-new detection

Net-new documents include program-specific plans (Strategic Plan, Knowledge Transfer Plan, Community Benefits Plan), solicitation-specific supplements (Milestones and Timeline, Letters of Commitment from specific entities), and program-required narratives distinct from the default `proposal_narrative`.

## Ordering

Modifications first (grouped by the order of the defaults they override), then net-new documents last. Convention only; downstream should not rely on it.

## Quality standards

1. Verbatim grounding in `source_excerpt`.
2. Only the diff — no unchanged defaults echoed back.
3. `modifies_default` targets a code present in the sponsor-defaults input.
4. Modifications emit full requirement objects, not partial diffs.
5. Vocabulary fidelity — enumerated codes only; `other` is a fallback.
6. Schema conformance — output validates against `schema.json`.
