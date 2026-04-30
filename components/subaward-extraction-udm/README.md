# Subaward Agreement Extraction — UDM JSON

Extracts a fully executed subaward agreement (Pass-Through Entity → Subrecipient) into a single structured JSON object covering nine sections used for research-administration setup and ongoing monitoring: basic info, project periods, PTE contacts, subrecipient contacts, financial summary, financial policies, reporting requirements, prior-approval handling, and key compliance requirements.

**Current version:** 0.1.0
**Category:** extraction
**Domain:** research-administration
**Status:** experimental
**Manifestations:** prompt
**Output contract:** [`schema.json`](schema.json)
**Contract scope:** repo-local, UDM-aligned

## Inputs

Full text of an executed subaward agreement (PTE → Subrecipient), typically including attachments.

## Outputs

A single JSON object covering six logical blocks:

- **Core award info** — `pte_name`, `subrecipient_name`, `federal_award_number`, `subaward_number`, `project_title`, `federal_awarding_agency`
- **Contacts** — six `{name, email, phone}` objects (PTE PI / admin / financial; Subrecipient PI / admin / financial)
- **Dates & monetary values** — `budget_period_start`, `budget_period_end`, `amount_funded`, `total_direct_costs`, `total_indirect_costs`, `cost_type` (enum)
- **Financial policies** — `invoicing_frequency` (enum), `final_invoice_due`, `fa_rate`, `fa_base`, `cost_sharing_required`, `carryforward_policy`
- **Reporting requirements** — typed arrays of `technical_reports`, `financial_reports`, `invention_reporting`
- **Compliance requirements** — `governing_regulations` (with source attribution), `prior_approval_handling`, `coi_policy`, `data_rights`, `audit_requirements`, `termination_clauses`, `record_retention`

See [`schema.json`](schema.json) for the authoritative definition and [`prompt.md`](prompt.md) for the encoding rules (character-perfect emails / phone numbers / dollar amounts; the strict-inclusion rule for `technical_reports` and `financial_reports`; the `amount_funded == total_direct_costs + total_indirect_costs` reconciliation).

## Contract scope

Repo-local, UDM-aligned. Extensive UDM column bindings preserved (see prompt.md). The structured shape mirrors the deliverable produced by the [`subaward-extraction` Vandalizer workflow](https://github.com/ui-insight/ProcessMapping/tree/main/workflows/subaward-extraction) in the ui-insight/ProcessMapping process-mapping corpus.

## Triad integration

- **Evaluation datasets:** none yet — planned: PTE → academic-subrecipient subaward (with full Attachment A and Attachment 4); subaward with cost-share commitment; subaward with non-default invoicing cadence; subaward with explicit COI flow-down language.
- **Harness notes:** canonical manifestation is `prompt.md`. The companion top-level `workflows/subaward-extraction` Vandalizer workflow at v0.1.0 implements the contract as six parallel Extraction tasks plus a Consolidation Prompt.

## Runtime topology — the Vandalizer workflow

The canonical runtime is the [`subaward-extraction` workflow](https://github.com/AI4RA/prompt-library/tree/main/workflows/subaward-extraction).

- **Step 1 (parallel Extraction)** — six Extraction tasks mirroring the source ProcessMapping workflow one-for-one (Core Award Information; Contact Information; Dates & Monetary Values; Financial Policies; Reporting Requirements; Compliance Requirements).
- **Step 2 (Consolidation Prompt)** — assembles the six fragments into a single schema-conformant object, normalizes the two enums (`cost_type`, `invoicing_frequency`), and verifies the `amount_funded == total_direct_costs + total_indirect_costs` reconciliation.

## Manifestations

- [`prompt.md`](prompt.md) — canonical, LLM-agnostic prompt

## Evals

See [`evals/`](evals/) for reference inputs and known-good outputs.

## Provenance

Authored 2026-04-30 against the `subaward-extraction` (Workflow_ID: `WF-SUBAWARD-EXTRACTION`) process-mapping workflow in `ui-insight/ProcessMapping`.
