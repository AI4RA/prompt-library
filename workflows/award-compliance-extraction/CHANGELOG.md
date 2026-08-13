# Changelog

All notable changes to this workflow. Versions follow semver.

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

## [0.1.1] — 2026-05-20

- Reworded the `uniform_guidance_applicability` searchphrase from "2 CFR 200 Uniform Guidance applicability details." to "Uniform Guidance (2 CFR 200) applicability details." so it no longer begins with a digit. Vandalizer derives each extraction field name by slugifying the searchphrase; a leading digit made Vandalizer prepend an underscore, which its own field-name validator then rejected on import. The extraction contract is unchanged.

## [0.1.0] — 2026-04-30

- Initial experimental release.
- Two-step runtime mirroring the source `award-compliance-extraction` v2 workflow in `ui-insight/ProcessMapping`: two parallel Extraction tasks (compliance framework + financial management) plus a Consolidation Prompt that merges/dedupes compliance_calendar entries across both fragments and normalizes the audit_requirements and record_retention enums.
- `audit_requirements` enum (`Single Audit`, `A-133`, `Program-Specific Audit`, `Not applicable`) and `record_retention` enum (`3 years`, `5 years`, `7 years`, `Per sponsor requirements`) — match the source workflow's enums.
- Validation plan carries CHK-01 (Monetary amount format, format/error), CHK-02 (Date validity, format/error), CHK-03 (Compliance calendar completeness, completeness/warning) — matches the source `Validation_Plan`.
- Pins `award-compliance-extraction-udm@0.1.0`.
