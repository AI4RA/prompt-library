---
name: document-type-classifier-udm
version: 1.0.0
description: Classifies a research-administration document into one of a controlled 14-code vocabulary (solicitation, proposal_narrative, biosketch, current_pending, facilities, data_mgmt, letter_support, budget, budget_justification, award_notice, award_amendment, jit_response, closeout_letter, other) so upstream routing can dispatch to the correct extractor or reviewer. Use when a user uploads a grants-related document and asks "what is this?", when routing an incoming file through an ingest pipeline, or when triaging a mixed folder of proposal and award documents. Input is plain text or OCR markdown of the document (typically the first N pages, or the whole body for short files). Output is one small JSON object with document_type, confidence, a verbatim evidence excerpt, a one-sentence rationale, and a secondary_candidates array that is only populated when the classification is ambiguous. Sponsor-agnostic — an NIH NOA, an NSF NOA, and a DoE award letter all classify as award_notice. For extracting the structured contents of a document rather than identifying its type, use a type-specific extraction component.
---

# Document Type Classifier — UDM Skill

Classifies a research-administration document into one of 14 controlled codes so downstream systems can route it to the right extractor. Output is a small JSON object — not a human summary.

## When to use

- The user wants to know what kind of document they have ("is this an award notice or an amendment?", "what is this PDF?")
- An ingest pipeline needs to dispatch a document to a type-specific extractor
- A mixed folder of proposal and award documents needs triage before bulk processing
- The user uploads a document and asks for classification before extraction

For extracting the structured contents of a document rather than identifying its type, use a type-specific component (e.g., `award-document-extraction-udm`, `nsf-award-notice-extraction-udm`, `rfp-extraction-udm`).

## Output contract

Emit exactly one JSON object. No preamble, no commentary, no markdown outside the JSON itself.

The object contains:

- `document_type` — one of the 14 controlled codes (see below)
- `confidence` — number 0–1, calibrated
- `evidence_excerpt` — a verbatim substring of the input that grounds the classification
- `rationale` — one short sentence
- `secondary_candidates` — array (possibly empty); populated only when the classification is ambiguous

See `schema.json` in this component for the authoritative definition.

## Controlled vocabulary

`solicitation`, `proposal_narrative`, `biosketch`, `current_pending`, `facilities`, `data_mgmt`, `letter_support`, `budget`, `budget_justification`, `award_notice`, `award_amendment`, `jit_response`, `closeout_letter`, `other`.

These codes are shared with sibling prompt-library components so classifier output can route directly into UDM-oriented workflows without a second vocabulary map.

## Key rules

- **Self-identifying phrases win.** A boxed header or explicit label ("NSF Award Notice", "Data Management Plan", "Biographical Sketch") is the highest-signal indicator; quote it in `evidence_excerpt` and set confidence 0.9+.
- **Structural indicators** (section headings, tabular layouts, writing voice) justify 0.7–0.9 when no literal label is present.
- **Initial vs. amendment:** an award document with "Amendment Number" other than "000", "Administrative Amendment", "No-Cost Extension", "Supplemental", or an NIH Type 3 / 4 / 5 marker is `award_amendment`, not `award_notice`.
- **Sponsor-agnostic:** do not refuse to classify because the sponsor is unfamiliar. An NIH NOA, an NSF NOA, and a DoE award letter are all `award_notice`.
- **Prefer `other` over a guess.** Low-confidence `other` routes better downstream than a speculative code.
- **Evidence-grounded:** `evidence_excerpt` must be a verbatim substring, not a paraphrase.

## Confidence bands

- 0.9–1.0 — canonical header or explicit self-identifying phrase
- 0.7–0.9 — strong structural indicators without a literal label
- 0.5–0.7 — multiple types plausibly fit; populate `secondary_candidates`
- Below 0.5 — weak evidence; classify as `other` and list plausible candidates as secondary

## `secondary_candidates` rule

Emit entries only when the top confidence is below 0.8 or a plausible alternative exceeds 0.3. Each secondary entry's `document_type` must differ from the top-level code; its `confidence` must not exceed the top-level confidence. Sort descending by confidence. Emit `[]` — not `null` — when unambiguous.

## Quality standards

1. Evidence-grounded — every classification cites a verbatim substring.
2. Controlled vocabulary only — no invented codes.
3. Calibrated confidence — follow the bands; over-confidence is a worse failure than cautious `other`.
4. Sponsor-agnostic — the vocabulary does not encode sponsor identity.
5. No fabrication — if the input is truncated or unreadable, classify as `other` and say so.
6. Schema conformance — output validates against `schema.json`.
