# Changelog — document-type-classifier-udm

All notable changes to this component. Versions follow semver: MAJOR for output-contract breaks (schema changes that drop or rename fields, or remove / rename vocabulary codes), MINOR for backward-compatible additions (new vocabulary codes, new optional fields, new manifestations), PATCH for wording or clarity with no behavior change expected.

The `schema.json` version is kept in lockstep with the component version.

## [1.0.0] — 2026-04-18

- Initial version.
- JSON Schema (`schema.json`) defining a single output object with `document_type`, `confidence`, `evidence_excerpt`, `rationale`, and a `secondary_candidates` array.
- Controlled 14-code vocabulary covering the most common research-administration document types (solicitation, proposal components, budget, award notice / amendment / JIT / closeout, plus `other`). Codes chosen to align with the document codes consumed by sibling UDM components so classifier output can route directly into those extractors.
- Canonical prompt (`prompt.md`) with per-type indicator cues, a confidence calibration rule, and an explicit rule for when to emit `secondary_candidates`.
- Claude Skill manifestation (`skill/SKILL.md`) tuned for "what kind of document is this" triggers.
- First three golden eval cases: a clear NSF solicitation, a clear NIH Notice of Award (proving sponsor generality beyond NSF), and an ambiguous short letter that exercises the `secondary_candidates` rule.
