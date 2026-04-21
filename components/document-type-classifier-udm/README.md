# Document Type Classifier — UDM

Classifies a research-administration document into a controlled type vocabulary so downstream pipelines can route it to the correct extractor or reviewer. One call in, one small JSON object out.

**Current version:** 1.0.0
**Category:** classification
**Domain:** research-administration
**Status:** experimental
**Manifestations:** prompt, skill
**Output contract:** see [`schema.json`](schema.json)

## Inputs

Text of the document, typically the first N pages (or the full body for short files) as OCR markdown or plain text. The component is text-only; upstream is responsible for PDF-to-text conversion.

Optional metadata the caller may include inline at the top of the input (the prompt ignores these when they conflict with the visible content):

- `Filename:` — the originating filename
- `Source:` — the originating system (email attachment, Grants.gov download, internal upload)

## Outputs

One JSON object with:

- `document_type` — the top-ranked code from the controlled vocabulary
- `confidence` — 0–1
- `evidence_excerpt` — a verbatim quote from the input that grounds the classification
- `rationale` — one short sentence explaining the decision
- `secondary_candidates` — zero or more runner-up types, each with `document_type`, `confidence`, and `rationale`. Emit entries only when the top confidence is below 0.8 or when a plausible alternative exceeds 0.3.

See [`schema.json`](schema.json) for the authoritative definition.

## Controlled vocabulary

| Code | Covers |
| --- | --- |
| `solicitation` | RFP, RFA, FOA, NOFO, program announcement |
| `proposal_narrative` | Project description, research plan, specific aims |
| `biosketch` | NSF or NIH biographical sketch |
| `current_pending` | Current and Pending (Other) Support |
| `facilities` | Facilities, Equipment, and Other Resources |
| `data_mgmt` | Data Management Plan or Data Management & Sharing plan |
| `letter_support` | Letter of support, commitment, or collaboration |
| `budget` | Budget workbook, budget table, or budget form |
| `budget_justification` | Narrative budget justification |
| `award_notice` | Initial award notice / Notice of Award |
| `award_amendment` | Amendment or modification to an existing award |
| `jit_response` | Just-in-Time submission |
| `closeout_letter` | Closeout notification or final report package |
| `other` | None of the above |

The `code` values here are shared with other prompt-library components used in UDM-oriented pipelines. `solicitation` is what `solicitation-doc-modifications-udm` classifies on; `award_notice` / `award_amendment` gate `award-document-extraction-udm`; the proposal-component codes (`biosketch`, `current_pending`, `facilities`, `data_mgmt`, `letter_support`, `budget_justification`) align with `sponsor-doc-defaults-udm`.

## Manifestations

- [`prompt.md`](prompt.md) — canonical, LLM-agnostic prompt
- [`skill/SKILL.md`](skill/SKILL.md) — Claude Skill form

## Schema

[`schema.json`](schema.json) is a JSON Schema (draft 2020-12) defining the full output contract. Validates with any conforming validator; routing layers should gate on it.

## Evals

See [`evals/`](evals/) for reference inputs and known-good outputs. The initial set exercises one clear solicitation, one clear award notice from a non-NSF sponsor, and one deliberately ambiguous short letter that should produce a dominant choice plus a plausible secondary candidate.

## Provenance

Schema designed 2026-04-18 in response to issue [#8](https://github.com/AI4RA/prompt-library/issues/8). Vocabulary derived from the set of document types already consumed by sibling UDM components so that the classifier's output can route directly into those extractors and reviewers.
