# RFA Checklist Extraction — UDM JSON

Extracts a federal funding announcement (RFA / FOA / NOFO / program solicitation) into a structured JSON object organized around the **eight-section pre-award checklist** that a sponsored-programs analyst actually uses when triaging a new opportunity. The shape enforces placement rules — award amount lives in `award_information` only, detailed financial rules in `budget_requirements` only — so downstream consolidation does not have to re-adjudicate where a fact belongs.

**Current version:** 0.1.0
**Category:** extraction
**Domain:** research-administration
**Status:** experimental
**Manifestations:** prompt
**Output contract:** [`schema.json`](schema.json)
**Contract scope:** repo-local, UDM-aligned

## Inputs

Full text of a funding announcement — pasted text, attached PDF/DOCX/HTML, or URL. Optional knowledge-base context from Uniform Guidance (2 CFR 200), NSF PAPPG, or NIH Grants Policy Statement is injected by the runtime workflow but not required by the prompt itself.

## Outputs

A single JSON object with:

- **Scalar opportunity metadata** — `rfa_id`, `rfa_number`, `rfa_title`, `sponsor_name`, `program_code`, `announcement_url`, `opportunity_number`, `cfda_number`
- **Eight structured sections** matching the consolidated checklist:
  - `dates_and_deadlines` — array of `{item, date_time, notes}`
  - `eligible_institutions` — array of `{type, subcategory, examples, compliance_requirements}`
  - `eligible_individuals` — array of `{type, criteria, compliance_requirements, conditions}`
  - `award_information` — `{award_duration, amount_per_award, number_of_awards, anticipated_award_date}`
  - `required_components` / `optional_components` — arrays of `{name, description, special_requirements}`
  - `budget_requirements` — `{funding_limits, cost_sharing: {status, details}, fa_policy, allowable_costs, unallowable_costs, personnel_effort, other_considerations}`
  - `submission_details` — string
  - `special_requirements` — array of strings
  - `important_notes` — array of strings

See [`schema.json`](schema.json) for the authoritative definition and [`prompt.md`](prompt.md) for the encoding rules (date formats, placement contract, quotation requirements, extraction strategy).

## Contract scope

Repo-local, UDM-aligned. The scalar fields (`rfa_id`, `rfa_number`, `rfa_title`, `sponsor_name`, `cfda_number`, ...) follow the conventions set by `rfp-extraction-udm` 1.0.0 and resolve downstream to UDM entities (`RFA`, `Sponsor_Organization`). The structured sections do not duplicate any shared UDM schema — they are repo-local to this component and mirror the eight-section deliverable produced by the [`rfa-checklist-extraction` Vandalizer workflow](https://github.com/ui-insight/ProcessMapping/tree/main/workflows/rfa-checklist-extraction) in the ui-insight/ProcessMapping process-mapping corpus. Selected leaf fields reference UDM columns: `cost_sharing` → `CostShare`, `fa_policy` → `IndirectRate`, `personnel_effort` → `Effort`.

## Relationship to `rfp-extraction-udm`

| Concern | [`rfp-extraction-udm`](../rfp-extraction-udm/) | `rfa-checklist-extraction-udm` |
| --- | --- | --- |
| Audience | Ingest pipelines (flat arrays of typed requirements) | Pre-award offices (eight-section checklist) |
| Shape | 18 scalars + nine requirement arrays with a common requirement shape | 8 scalars + eight typed section objects/arrays, each with a distinct field shape |
| De-duplication | Not enforced by shape — every requirement is independent | Enforced by shape — award amount lives only in `award_information`, financial rules only in `budget_requirements` |
| Checklist reconstruction | Requires caller to re-group by category | Direct 1:1 map to the eight-section markdown deliverable |
| Typical downstream | UDM ingest service | Consolidation Prompt node rendering a markdown checklist |

The two components are versioned independently. A single announcement can be extracted through both contracts for different consumers.

## Triad integration

- **Evaluation datasets:** none yet — planned: add an RFA case to `real.nsf_awards` or a new `real.rfa_checklists` dataset with `expected.json` produced from a sponsored-programs-reviewed extraction.
- **Harness notes:** canonical manifestation is `prompt.md`. Validation surface is `schema.json`. Vendored into runners via `harness prompts vendor --source-ref=<sha>`; pinned in `prompts.lock.json`.
- **Shared UDM relationship:** aligned, not owning. `rfa_id`, `sponsor_name`, and the three UDM-column leaf fields match the naming conventions in AI4RA-UDM but this component does not redefine UDM tables.

## Runtime topology — the Vandalizer workflow

The canonical runtime for this component is the [`rfa-checklist-extraction` workflow](https://github.com/AI4RA/prompt-library/tree/main/workflows/rfa-checklist-extraction) shipped at the top level of this repo. The single source of truth is [`workflows/rfa-checklist-extraction/manifest.yaml`](https://github.com/AI4RA/prompt-library/blob/main/workflows/rfa-checklist-extraction/manifest.yaml); the companion `.vandalizer.json` envelope is generated by [`scripts/build_vandalizer_workflows.py`](https://github.com/AI4RA/prompt-library/blob/main/scripts/build_vandalizer_workflows.py) and committed alongside. The runtime mirrors the source [`ui-insight/ProcessMapping/workflows/rfa-checklist-extraction/`](https://github.com/ui-insight/ProcessMapping/tree/main/workflows/rfa-checklist-extraction) workflow:

- **Step 1 (parallel Extraction)** — seven Extraction tasks. Six mirror the source workflow one-for-one (dates, eligible institutions, eligible individuals, award info, application components, budget). A seventh `extract-opportunity-metadata` task captures the eight UDM-aligned scalar opportunity fields the schema adds on top of the source workflow. Each task carries an embedded SearchSet whose item titles match this component's schema field names; `cost_sharing_status` is exposed as the four-value enum.
- **Step 2 (consolidation Prompt)** — assembles the seven JSON fragments into the schema-conformant object, including the nested `cost_sharing: {status, details}` rebuild and `important_notes` synthesis from cross-section signals.

Regenerate the workflow JSON whenever this component bumps MINOR or MAJOR (or whenever the workflow manifest changes); CI fails if the committed `.vandalizer.json` drifts from a fresh build.

## Manifestations

- [`prompt.md`](prompt.md) — canonical, LLM-agnostic prompt

## Evals

See [`evals/`](evals/) for reference inputs and known-good outputs. Initial case pending: NSF-published RFA with a multi-round structure, cost-sharing prohibition, and explicit allowable/unallowable categories to exercise the placement contract.

## Provenance

Authored 2026-04-24 against the existing `rfa-checklist-extraction` process-mapping workflow (v2) in `ui-insight/ProcessMapping`, which was built from walkthrough transcripts of University of Idaho sponsored-programs staff reviewing NSF and NIH announcements. Created to make that workflow a harness-evaluatable, versioned artifact rather than a runtime-embedded configuration.
