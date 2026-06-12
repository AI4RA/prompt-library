# Changelog

All notable changes to this workflow. Versions follow semver: MAJOR for step-structure changes, MINOR for additive changes (e.g., new search_set_items, validation checks), PATCH for display-name or wording edits.

## [0.2.0] — 2026-05-22

- **MAJOR step-structure change + output-contract change** for end-user Vandalizer use.
- Parallel "Extraction" tasks converted from Vandalizer Extraction (SearchSet keyword retrieval) to Vandalizer Prompt tasks (full-document LLM reading via `input_sources: [step_input, workflow_documents]`). Grant documents don't use the literal field labels SearchSet retrieval expects, so the SearchSet path returned empty fragments and the Consolidation step had nothing to assemble. Prompt tasks pass the full OCR'd document into the LLM, which then reads with NLU.
- Output contract changed from JSON-against-schema to RA-friendly Markdown deliverable, mirroring the source `ui-insight/ProcessMapping` workflow's `consolidation.md` (or `formatting.md`) conventions. The paired `*-udm` COMPONENT remains JSON-emitting and is the evaluation-harness target via its `prompt.md`; this WORKFLOW is the Vandalizer end-user (sponsored-programs analyst) deliverable.
- Step 0 `KnowledgeBaseQuery` placeholder added — `kb_uuid` blanked by Vandalizer's importer; the embedded `knowledge_base_hint.title` becomes an `_import_note` telling the operator which KB title to select in Vandalizer's UI. Downstream Prompt tasks read `input_sources: [step_input, workflow_documents]` so the KB chunks (when attached) plus the uploaded PDF reach the LLM context together. Returns empty output gracefully when no KB is attached — the workflow runs end-to-end either way.
- Extraction prompts tightened with explicit "flat strings, not nested objects" discipline for descriptive fields, plus a worked WRONG/CORRECT example, after the v0.1.0 → v0.2.0 dry run on real RFA documents showed nested JSON leaking into the Markdown deliverable.
- Consolidation prompts updated to skip empty sub-bullets (no "Field: —" placeholder lines when a field is null) and to rewrite any nested JSON arriving from upstream into Markdown prose rather than passing through `{...}` literals.

## [0.1.0] — 2026-05-20

- Initial experimental release.
- Two-step runtime mirroring the source `export-to-banner-extraction` v2 workflow in `ui-insight/ProcessMapping`: six parallel Extraction tasks (award-identification, dates-and-performance, sponsor-and-entity, budget-and-financial, billing-and-payment, reporting-and-special) with embedded SearchSets, plus a Consolidation Prompt that assembles the six JSON fragments into a single schema-conformant object, converts quoted-dollar strings to JSON numbers, normalizes the four enums, and enforces the two source cross-field rules as flag emissions on `reporting_special.special_terms`.
- Four enums match the source workflow exactly: `award_type` (Grant, Cooperative Agreement, Contract, Subcontract); `sponsor_entity_type` (Federal, State Government, Non-Profit, Private Industry, Foundation, University, Other); `fa_rate_base` (MTDC, TDC, Salary & Wages, Other); `billing_type` (Cost Reimbursement, Fixed Price, Letter of Credit, Milestone).
- Monetary fields explicitly typed and prompted as JSON numbers, not quoted strings — applies CFR-04-style number-vs-string handling from the boss's PR #33 review feedback to every monetary leaf in the schema.
- Validation plan carries CHK-01..CHK-04 — matches the source `Validation_Plan` with field-target paths updated to reflect the schema's six-block shape.
- Source `Cross_Field_Rules` (CFR-01 `award_start < award_end`; CFR-02 `performance_period_start <= award_start_date`) enforced by the Consolidation Prompt at runtime as flag strings on `reporting_special.special_terms` rather than altering the dates.
- Pins `export-to-banner-extraction-udm@0.1.0`.
