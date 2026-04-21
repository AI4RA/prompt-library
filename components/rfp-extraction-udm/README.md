# RFP Extraction — UDM JSON

Extracts any federal funding announcement (RFP, RFA, FOA, NOFO, BAA, Dear Colleague Letter, or program solicitation) into a single JSON object conforming to this repo's UDM-aligned extraction contract. Companion to [`rfp-extraction`](../rfp-extraction/), which produces the human-readable checklist form from the same source.

**Current version:** 1.0.0
**Category:** extraction
**Domain:** research-administration
**Status:** stable
**Manifestations:** prompt, skill
**Output contract:** see [`schema.json`](schema.json)

## Inputs

Full text of a funding announcement — pasted text, attached document, or URL.

## Outputs

A single JSON object with two layers:

- **Scalar opportunity metadata** — `rfa_id`, `rfa_number`, `rfa_title`, `sponsor_name`, `program_code`, `announcement_url`, `opportunity_number`, `cfda_number`, `announcement_date`, `submission_deadline`, `loi_deadline`, `preproposal_deadline`, `funding_floor`, `funding_ceiling`, `expected_awards`, `max_duration_months`, `submission_method`, `rfa_status`
- **Nine requirement arrays**, each always present (`[]` when empty):
  - `required_documents`, `formatting`, `review_criteria`, `eligibility`, `budget_constraints`, `compliance`, `submission_requirements`, `special_conditions`, `pappg_deviations`

Every requirement entry shares a single shape: `label`, `code`, `description`, `page_limit`, `format_spec`, `is_required`, `source_section`, `structured_rule_type`, `structured_rule_value`. See [`schema.json`](schema.json) for the authoritative definition and [`prompt.md`](prompt.md) for the encoding rules the extractor follows (date formats, currency, multi-round handling, structured rule types, etc.). The schema is repo-local and UDM-aligned rather than a checked-in copy of the shared UDM repo.

## Relationship to `rfp-extraction`

| Concern | `rfp-extraction` | `rfp-extraction-udm` |
| --- | --- | --- |
| Audience | Humans (PIs, OSP reviewers) | Ingest pipelines, downstream systems |
| Output format | Markdown with GFM checkboxes | JSON matching `schema.json` |
| Structure | Section-ordered narrative checklist | Flat scalars + nine categorized arrays |
| Eval artifact | `expected.md` | `expected.json` |

The two components are versioned independently. They are not required to share a version number; the canonical source for a given case (e.g., NSF 26-508) lives in both eval directories as the two different target formats.

## Manifestations

- [`prompt.md`](prompt.md) — canonical, LLM-agnostic prompt
- [`skill/SKILL.md`](skill/SKILL.md) — Claude Skill form

## Schema

[`schema.json`](schema.json) is a JSON Schema (draft 2020-12) that defines the full output contract. Downstream consumers can validate extractor outputs programmatically; the eval suite uses it to validate `expected.json`. The schema's version matches the component version.

## Evals

See [`evals/`](evals/) for reference inputs and known-good outputs. The initial case is NSF 26-508 (TechAccess), a multi-round solicitation exercising LOI handling, per-institution proposal limits, cost-sharing prohibition, and several parent-guide deviations.

## Provenance

Companion to `rfp-extraction` 1.0.0, built for workflows where a downstream system ingests the opportunity metadata and requirements into a UDM-backed data store. Schema designed 2026-04-18 alongside the NSF 26-508 golden case.
