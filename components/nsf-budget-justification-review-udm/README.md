# NSF Budget Justification Review — UDM

Validates and polishes a drafted NSF budget-justification array against its source structured budget and NSF narrative conventions. The component is the QA step of the multi-step budget-justification pipeline: it checks section completeness and ordering, fixes misplaced content (for example graduate tuition in the wrong section), ensures required NSF disclosures are present, and consolidates terminology across sections. Its revised array is the input to the downstream render step that emits Word-pasteable Markdown and HTML.

**Current version:** 1.0.0
**Category:** review
**Domain:** research-administration
**Status:** experimental
**Manifestations:** prompt
**Output contract:** delegates to [`../nsf-budget-justification-udm/schema.json`](../nsf-budget-justification-udm/schema.json) (`#/$defs/output`)
**Contract scope:** delegated wrapper over a repo-local NSF budget-justification output contract

## Inputs

- Required: a drafted eight-section JSON array matching `#/$defs/output` of `../nsf-budget-justification-udm/schema.json`.
- Optional: the structured budget that produced the draft, matching `#/$defs/input` of the same schema. When supplied, the review can trace individual dollar figures and percentages back to the budget; when absent, the review relies only on internal consistency of the draft.

## Outputs

A single JSON array, same contract as the draft: eight section objects (A..H) with `key`, `title`, and `content`. The deliverable IS the revised array — no side-channel review notes or change logs.

## Contract Scope

Delegated wrapper. This component does not define its own JSON schema; it validates input and emits output against the contract owned by `nsf-budget-justification-udm`. The review rubric (category placement rules, required disclosures, zero-section handling) is repo-local and sponsor-specific.

## Triad Integration

- **Evaluation datasets:** none yet; initial coverage is repo-local only.
- **Harness notes:** invoke after a drafting step that produced an eight-section array. Validate input and output against `components/nsf-budget-justification-udm/schema.json` at `#/$defs/output`; when the structured budget is provided as additional context, it validates against `#/$defs/input` of the same schema.
- **Shared UDM relationship:** can feed UDM-backed proposal workflows; the review rubric itself is prompt-library repo-local.

## Manifestations

- [`prompt.md`](prompt.md) — canonical prompt

## Evals

See [`evals/`](evals/). No golden cases are checked in yet; future cases should pair a deliberately-flawed draft array with the expected revised array, demonstrating a specific check (misplaced tuition, missing participant-support disclosure, fabricated figure, zero-section invention, and so on).

## Provenance

Created 2026-04-24 to serve as the review step in the `nsf-budget-justification-multistep` workflow, where it runs after spreadsheet ingestion and section drafting and feeds the downstream render step.
