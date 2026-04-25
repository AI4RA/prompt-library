# Changelog

All notable changes to this workflow. Versions follow semver adapted to workflow semantics:

- **MAJOR** — step structure changes (add or remove a step, change `input_source`, change `is_output`, re-pin the component across a MAJOR).
- **MINOR** — prompt body tracking a referenced component MINOR, or additive step/task options that preserve the existing operator flow.
- **PATCH** — step or task display-name edits, description polish, non-semantic manifest cleanup.

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
