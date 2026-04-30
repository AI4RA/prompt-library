# Effort Reporting Compliance Extraction — UDM JSON

Extracts effort-reporting and personnel-compliance requirements from a federal award document into a structured JSON object that drives an "Effort Compliance Brief" for post-award compliance tracking. Captures the reporting cadence, certification method (per 2 CFR 200.430(i)), PI commitments, per-person key-personnel commitments, cost-shared effort, governing regulation, record-retention requirement, and referenced governing documents.

**Current version:** 0.1.0
**Category:** extraction
**Domain:** research-administration
**Status:** experimental
**Manifestations:** prompt
**Output contract:** [`schema.json`](schema.json)
**Contract scope:** repo-local, UDM-aligned

## Inputs

Full text of a federal award notice / agreement / terms-and-conditions document — pasted text, attached PDF/DOCX, or URL. Optional knowledge-base context from 2 CFR 200 (Uniform Guidance) or the Research Terms and Conditions is injected by the runtime workflow but not required by the prompt itself.

## Outputs

A single JSON object with award-identifying scalars (`award_number`, `pi_name`, `project_title`), an effort-reporting cadence (`reporting_frequency` enum, `certification_deadline`, `certification_method` enum), PI commitments (`pi_committed_effort`, `pi_person_months`), a per-person `key_personnel_commitments` table, `cost_shared_effort`, `governing_regulation`, `record_retention`, and a `referenced_documents` list.

See [`schema.json`](schema.json) for the authoritative definition and [`prompt.md`](prompt.md) for the encoding rules (verbatim effort-phrasing quotation, one-row-per-individual rule, the distinction between `governing_regulation` and `referenced_documents`).

## Contract scope

Repo-local, UDM-aligned. Selected leaf fields reference UDM columns: `award_number` → `Award.Award_Number`; `pi_name` → `Personnel.First_Name`/`Last_Name`; `project_title` → `Award.Award_Title`; `certification_method` → `Effort.Certification_Method`; `pi_committed_effort` → `Effort.Committed_Percent`; `pi_person_months` → `Effort.Committed_Person_Months`; per-row `key_personnel_commitments` → `Effort` + `ProjectRole`; `cost_shared_effort` → `CostShare.Committed_Amount`; `record_retention` → `Terms.Record_Retention_Years`. The structured shape does not duplicate any shared UDM schema — it is repo-local to this component and mirrors the deliverable produced by the [`effort-reporting-extraction` Vandalizer workflow](https://github.com/ui-insight/ProcessMapping/tree/main/workflows/effort-reporting-extraction) in the ui-insight/ProcessMapping process-mapping corpus.

## Triad integration

- **Evaluation datasets:** none yet — planned: NIH R01 with explicit summer-month commitment; NSF award with cost-shared academic-year effort; HHS-funded award using After-the-Fact certification.
- **Harness notes:** canonical manifestation is `prompt.md`. Validation surface is `schema.json`. The companion top-level `workflows/effort-reporting-extraction` Vandalizer workflow at v0.1.0 implements the contract as a single Extraction task plus a Consolidation Prompt; record both single-call and post-consolidation signals when both are available.
- **Shared UDM relationship:** aligned, not owning. UDM column bindings preserved verbatim; the shape itself is repo-local.

## Runtime topology — the Vandalizer workflow

The canonical runtime is the [`effort-reporting-extraction` workflow](https://github.com/AI4RA/prompt-library/tree/main/workflows/effort-reporting-extraction) shipped at the top level of this repo.

- **Step 1 (Extraction)** — one Extraction task with an embedded SearchSet whose item titles mirror this component's schema field names. `reporting_frequency` and `certification_method` carry their respective enums.
- **Step 2 (Consolidation Prompt)** — assembles the extraction fragment into the schema-conformant object, normalizes the enums, and ensures the PI's row in `key_personnel_commitments` mirrors the `pi_committed_effort` and `pi_person_months` scalars.

## Manifestations

- [`prompt.md`](prompt.md) — canonical, LLM-agnostic prompt

## Evals

See [`evals/`](evals/) for reference inputs and known-good outputs.

## Provenance

Authored 2026-04-30 against the `effort-reporting-extraction` (Workflow_ID: `WF-EFFORT-REPORTING-EXTRACTION`) process-mapping workflow in `ui-insight/ProcessMapping` at commit `b7176b0c913833a205efdb5e4ba00c17ff88af0f`.
