# Changelog

All notable changes to this workflow. Versions follow semver.

## [0.2.0] — 2026-05-22

- **MAJOR step-structure change + output-contract change** for end-user Vandalizer use.
- Parallel "Extraction" tasks converted from Vandalizer Extraction (SearchSet keyword retrieval) to Vandalizer Prompt tasks (full-document LLM reading via `input_sources: [step_input, workflow_documents]`). Grant documents don't use the literal field labels SearchSet retrieval expects, so the SearchSet path returned empty fragments and the Consolidation step had nothing to assemble. Prompt tasks pass the full OCR'd document into the LLM, which then reads with NLU.
- Output contract changed from JSON-against-schema to RA-friendly Markdown deliverable, mirroring the source `ui-insight/ProcessMapping` workflow's `consolidation.md` (or `formatting.md`) conventions. The paired `*-udm` COMPONENT remains JSON-emitting and is the evaluation-harness target via its `prompt.md`; this WORKFLOW is the Vandalizer end-user (sponsored-programs analyst) deliverable.
- Step 0 `KnowledgeBaseQuery` placeholder added — `kb_uuid` blanked by Vandalizer's importer; the embedded `knowledge_base_hint.title` becomes an `_import_note` telling the operator which KB title to select in Vandalizer's UI. Downstream Prompt tasks read `input_sources: [step_input, workflow_documents]` so the KB chunks (when attached) plus the uploaded PDF reach the LLM context together. Returns empty output gracefully when no KB is attached — the workflow runs end-to-end either way.
- Extraction prompts tightened with explicit "flat strings, not nested objects" discipline for descriptive fields, plus a worked WRONG/CORRECT example, after the v0.1.0 → v0.2.0 dry run on real RFA documents showed nested JSON leaking into the Markdown deliverable.
- Consolidation prompts updated to skip empty sub-bullets (no "Field: —" placeholder lines when a field is null) and to rewrite any nested JSON arriving from upstream into Markdown prose rather than passing through `{...}` literals.

## [0.1.0] — 2026-04-30

- Initial experimental release.
- Two-step runtime mirroring the source `proposal-budget-personnel-extraction` v2 workflow in `ui-insight/ProcessMapping`: two parallel Extraction tasks (personnel identification + budget structure) plus a Consolidation Prompt that derives the four boolean compliance triggers (`has_postdocs_or_grad_students`, `mentoring_plan_required`, `has_subawards`, `has_equipment_over_5k`) from list lengths and combines `fa_rate` + `fa_base` into the nested `fa_rate_and_base` object.
- `fa_base` enum (`MTDC`, `TDC`, `Salary & Wages`) — matches the source `FA_Rate_And_Base` Enum_Values.
- Validation plan carries CHK-01 (Personnel count consistency, consistency/warning), CHK-02 (Boolean flag derivation, consistency/warning), CHK-03 (Cost totals validation, arithmetic/error) — matches the source `Validation_Plan`.
- Pins `proposal-budget-personnel-extraction-udm@0.1.0`.
