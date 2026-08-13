# Changelog

All notable changes to this workflow. Versions follow semver: MAJOR for step-structure changes, MINOR for additive changes (e.g., new search_set_items, validation checks), PATCH for display-name or wording edits.

## [1.0.0] — 2026-08-13

**MAJOR — remove the KB lookup step (3 steps → 2).** The optional `KnowledgeBaseQuery` Step 0 was inert on a fresh import (Vandalizer blanks `kb_uuid` by design, so the operator always had to attach a KB manually) and confused operators comparing the imported workflow against their live Vandalizer copies. Mirrors `rfa-checklist-extraction` v1.0.0 (PR #50) and `export-to-banner-extraction` v1.0.0 (PR #52).

- The parallel extraction tasks now read `input_sources: [workflow_documents]` only; the vestigial `step_input` (which carried the removed KB step's output) is dropped. Consolidation is unchanged.
- No prompt-body or validation-plan changes. `vandalizer.json` rebuilt (export name now carries the version per the build-script convention).
- KBs will be reintroduced once the right approach is settled.

## [0.2.0] — 2026-05-22

- **MAJOR step-structure change + output-contract change** for end-user Vandalizer use.
- Parallel "Extraction" tasks converted from Vandalizer Extraction (SearchSet keyword retrieval) to Vandalizer Prompt tasks (full-document LLM reading via `input_sources: [step_input, workflow_documents]`). Grant documents don't use the literal field labels SearchSet retrieval expects, so the SearchSet path returned empty fragments and the Consolidation step had nothing to assemble. Prompt tasks pass the full OCR'd document into the LLM, which then reads with NLU.
- Output contract changed from JSON-against-schema to RA-friendly Markdown deliverable, mirroring the source `ui-insight/ProcessMapping` workflow's `consolidation.md` (or `formatting.md`) conventions. The paired `*-udm` COMPONENT remains JSON-emitting and is the evaluation-harness target via its `prompt.md`; this WORKFLOW is the Vandalizer end-user (sponsored-programs analyst) deliverable.
- Step 0 `KnowledgeBaseQuery` placeholder added — `kb_uuid` blanked by Vandalizer's importer; the embedded `knowledge_base_hint.title` becomes an `_import_note` telling the operator which KB title to select in Vandalizer's UI. Downstream Prompt tasks read `input_sources: [step_input, workflow_documents]` so the KB chunks (when attached) plus the uploaded PDF reach the LLM context together. Returns empty output gracefully when no KB is attached — the workflow runs end-to-end either way.
- Extraction prompts tightened with explicit "flat strings, not nested objects" discipline for descriptive fields, plus a worked WRONG/CORRECT example, after the v0.1.0 → v0.2.0 dry run on real RFA documents showed nested JSON leaking into the Markdown deliverable.
- Consolidation prompts updated to skip empty sub-bullets (no "Field: —" placeholder lines when a field is null) and to rewrite any nested JSON arriving from upstream into Markdown prose rather than passing through `{...}` literals.

## [0.1.0] — 2026-05-20

- Initial experimental release.
- Two-step runtime mirroring the source `compliance-personnel-verification` v1 workflow in `ui-insight/ProcessMapping`: two parallel Extraction tasks (personnel identification + compliance status verification) with embedded SearchSets, plus a Consolidation Prompt that assembles the two JSON fragments into a single schema-conformant object and derives `non_compliant_personnel` + the five `verification_status` counts from the per-person SFI / RST status records.
- Multi-source input model: requires the operator to upload the VERAS proposal, the SFI disclosure records, and the daily RST completion spreadsheet together as workflow documents. When any source is missing, the workflow emits non-compliant defaults and captures the gap in `verification_status.notes` rather than silently assuming compliance.
- `proposal_type` and `sponsor_type` enums match the source workflow exactly. `sfi_verification[].status` exposed as the five-value enum from the source (`Valid`, `Expiring Soon`, `Expired`, `Not Found`, `Review Required`). `rst_verification.records[].status` as the three-value enum (`Complete`, `Incomplete`, `Review Required`). `non_compliant_personnel[].priority` as three-value (`Critical`, `High`, `Medium`). `verification_status.overall_status` as three-value (`All Compliant`, `Non-Compliance Found`, `Not Applicable`).
- Validation plan carries CHK-01..CHK-04 — matches the source `Validation_Plan` with field-target paths updated to reflect the schema's six-block shape.
- Source `Cross_Field_Rules` (CFR-01..CFR-02) enforced by the Consolidation Prompt at runtime: CFR-01 (Section 6.6 ⊆ Section 2) emits entries to `personnel_discrepancies`; CFR-02 (365-day validity) drives the per-person SFI status enum.
- Pins `compliance-personnel-verification-udm@0.1.0`.
