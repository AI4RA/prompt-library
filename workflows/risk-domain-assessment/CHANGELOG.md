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
- Two-step runtime mirroring the source `risk-domain-assessment` v2 workflow in `ui-insight/ProcessMapping`: six parallel Extraction tasks each covering 2–4 of the 14 risk domains (Task 1: Domains 1+9; Task 2: 2+8; Task 3: 3+13; Task 4: 4+5; Task 5: 6+7; Task 6: 10+11+12+14), plus a Consolidation Prompt that assembles the six JSON fragments into a single schema-conformant object, computes `aggregate_metrics` deterministically, and derives the `high_risk_domains` / `key_risk_findings` / `recommended_mitigations` arrays from the per-domain scores and justifications.
- All 14 domain scores typed as JSON integers in `[1, 5]`. `aggregate_metrics.total_risk_score` as JSON integer in `[14, 70]`. `aggregate_metrics.average_risk_score` as JSON number in `[1.0, 5.0]`. Applies the boss's PR #33 number-vs-string review feedback to all scoring fields.
- `aggregate_metrics.overall_risk_level` exposed as the four-value enum (`Low`, `Moderate`, `High`, `Very High`) per the source workflow's rubric language.
- Validation plan carries CHK-01..CHK-03 — matches the source `Validation_Plan` with field-target paths updated to the schema's three-block shape.
- Source `Cross_Field_Rules` (CFR-01 `justification not empty when score >= 3`) enforced by `minLength: 1` on every domain block's `justification` plus the Consolidation Prompt's FLAG path for generic justifications on high-score domains.
- Pins `risk-domain-assessment-udm@0.1.0`.
