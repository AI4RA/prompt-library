# Changelog

All notable changes to this workflow. Versions follow semver adapted to workflow semantics:

- **MAJOR** — step structure changes (add or remove a step, change `input_source`, change `is_output`, re-pin the component across a MAJOR).
- **MINOR** — prompt body tracking a referenced component MINOR, or additive step/task options that preserve the existing operator flow.
- **PATCH** — step or task display-name edits, description polish, non-semantic manifest cleanup.

## [0.3.0] — 2026-05-22

- **MAJOR step-structure change + output-contract change.** Two-part overhaul to fix the broken-on-real-documents v0.2.0 runtime:
  1. **Parallel tasks: Extraction → Prompt.** Vandalizer's `Extraction` task type drives keyword-based SearchSet retrieval, which expects the document to use the literal search-term wording (e.g., "Due Date") it was given. Grant documents in practice use varied phrasings ("Full Proposal Deadline", "Closing Date", "Application Deadline" — for the same concept), so SearchSet retrieval returns empty fragments and the Consolidation step has nothing to assemble. The seven parallel tasks are now Vandalizer `Prompt` tasks (the default kind) that receive the full uploaded document via `input_source: workflow_documents` and let the LLM read with NLU to find the right content regardless of wording. The `kind: Extraction`, `searchset:` blocks, and `_embedded_search_set` / `searchphrases` fields are removed.
  2. **Output contract: JSON → Markdown.** The Consolidation step now emits an RA-friendly Markdown checklist (eight sections per the source `ui-insight/ProcessMapping` `consolidation.md` conventions) rather than a schema-conformant JSON object. The pinned `rfa-checklist-extraction-udm` COMPONENT remains JSON-emitting and is the evaluation-harness target via its `prompt.md`; this WORKFLOW is the Vandalizer end-user (sponsored-programs analyst) deliverable. Mid-pipeline handoff between the seven parallel tasks and the Consolidation step uses JSON fragments (Variant A) — a side-by-side variant `rfa-checklist-extraction-md` tests the Markdown-chunks alternative for comparison.
- `validation_plan` rewritten to target the Markdown deliverable structure (eight sections present, placement contract, monetary preservation, eligibility completeness) rather than per-field JSON validation.
- Eval golden cases shifted from `expected.json` to `expected.md` — the workflow is now a Markdown-output workflow with workflow-local evals separate from the JSON-against-schema component evals.
- Component pin unchanged at `rfa-checklist-extraction-udm@0.1.0`.

## [0.2.0] — 2026-04-24

- **MAJOR step-structure change.** Replaced the v0.1.0 single-Prompt runtime with the multi-extraction shape that mirrors the `ui-insight/ProcessMapping/workflows/rfa-checklist-extraction/` source workflow:
  - **Step 1 — Parallel Extraction:** seven Extraction tasks, each with an embedded SearchSet whose item titles match the `rfa-checklist-extraction-udm@0.1.0` schema field names. Six of the tasks (dates-and-deadlines, eligible-institutions, eligible-individuals, award-information, application-components, budget-requirements) mirror the source ProcessMapping workflow's six parallel extractions one-for-one. A seventh `extract-opportunity-metadata` task captures the eight scalar UDM-aligned opportunity fields the schema adds on top of the source workflow (`rfa_id`, `rfa_number`, `rfa_title`, `sponsor_name`, `program_code`, `announcement_url`, `opportunity_number`, `cfda_number`).
  - **Step 2 — Consolidation:** single Prompt task that assembles the seven JSON fragments into one object that validates against `schema.json`, enforces the placement contract (award amount only in `award_information`; detailed financial rules only in `budget_requirements`), maps the flat `cost_sharing_status` / `cost_sharing_details` extraction fields into the schema's nested `cost_sharing: {status, details}` object, and synthesizes `important_notes` from cross-section signals.
- `cost_sharing_status` is exposed in the SearchSet with `enum_values: [Required, Voluntary, Prohibited, "Not Specified"]`, matching the existing Vandalizer enum.
- Top-level `validation_plan` carried into the export (4 checks: date format, monetary format, eligibility completeness, de-duplication) — sourced from the ProcessMapping workflow's Validation_Plan.
- Component pin unchanged at `rfa-checklist-extraction-udm@0.1.0`. The prompt body for each Extraction task is workflow-runtime (authored as `prompt_inline` in `manifest.yaml`) and therefore intentionally does **not** carry a `prompt_sha256` provenance entry; the canonical full-document component prompt remains available at `components/rfa-checklist-extraction-udm/prompt.md` as the single-call reference.

## [0.1.0] — 2026-04-24

- Initial workflow, Prompt-only shape: single step, single Prompt task invoking the full `rfa-checklist-extraction-udm@0.1.0` canonical prompt against the uploaded document.
- Pinned to component 0.1.0.
- `input_source: workflow_documents` so Vandalizer feeds the uploaded announcement directly to the prompt.
