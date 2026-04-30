# Award Compliance & Financial Overview Extraction — UDM JSON

Extracts the compliance framework and financial-management requirements from a federal award document into a single structured JSON object that drives a consolidated "Award Compliance & Financial Overview" deliverable for post-award setup and monitoring. Produces two main blocks (compliance framework with 10 fields including a normalized compliance calendar; financial management with 10 fields including budget periods and budget categories).

**Current version:** 0.1.0
**Category:** extraction
**Domain:** research-administration
**Status:** experimental
**Manifestations:** prompt
**Output contract:** [`schema.json`](schema.json)
**Contract scope:** repo-local, UDM-aligned

## Inputs

Full text of a federal award notice / agreement / terms-and-conditions document.

## Outputs

A single JSON object with two main blocks:

- `compliance_framework` — `{uniform_guidance_applicability, rtc_applicability, financial_reporting_requirements, progress_reporting_requirements, prior_approval_requirements[], budget_modification_restrictions, property_requirements, deliverable_requirements[], high_risk_conditions[], compliance_calendar[]}`
- `financial_management` — `{total_award_amount, budget_period_amounts[], cost_share_requirements, fa_rate, fa_rate_base, performance_period, budget_categories[], ffr_requirements, audit_requirements (enum), record_retention (enum)}`

See [`schema.json`](schema.json) for the authoritative definition and [`prompt.md`](prompt.md) for the encoding rules (verbatim quotation of dollar amounts and rates; one-row-per-deadline `compliance_calendar`; single-period awards return empty `budget_period_amounts`; the placement contract that keeps procedural prior-approval mechanics in `prior-approval-extraction-udm`).

## Contract scope

Repo-local, UDM-aligned. Extensive UDM column bindings preserved verbatim (see prompt.md). The structured shape does not duplicate any shared UDM schema — it mirrors the deliverable produced by the [`award-compliance-extraction` Vandalizer workflow](https://github.com/ui-insight/ProcessMapping/tree/main/workflows/award-compliance-extraction) in the ui-insight/ProcessMapping process-mapping corpus.

## Relationship to sibling components

| Concern | This component | Related |
| --- | --- | --- |
| Award-level compliance framework + financial overview | `award-compliance-extraction-udm` | — |
| FFR submission detail (cadence, system, preparation timeline) | (drives `ffr_requirements` summary only) | `ffr-management-extraction-udm` |
| Prior-approval procedural mechanics (threshold/timeline/consequences table) | (drives `prior_approval_requirements[]` category list only) | `prior-approval-extraction-udm` |
| Effort and personnel commitments | — | `effort-reporting-extraction-udm` |

## Triad integration

- **Evaluation datasets:** none yet — planned: NSF cooperative agreement (multi-year, complex compliance calendar); NIH R01 (single-year, RTC-eligible); high-risk recipient award (enhanced monitoring, special conditions).
- **Harness notes:** canonical manifestation is `prompt.md`. Validation surface is `schema.json`. The companion top-level `workflows/award-compliance-extraction` Vandalizer workflow at v0.1.0 implements the contract as two parallel Extraction tasks (compliance framework + financial management) plus a Consolidation Prompt; record both single-call and post-consolidation signals when both are available.

## Runtime topology — the Vandalizer workflow

The canonical runtime is the [`award-compliance-extraction` workflow](https://github.com/AI4RA/prompt-library/tree/main/workflows/award-compliance-extraction) shipped at the top level of this repo.

- **Step 1 (parallel Extraction)** — two Extraction tasks. `extract-compliance-framework` covers the regulatory framework; `extract-financial-management` covers the financial structure.
- **Step 2 (Consolidation Prompt)** — assembles the two fragments into the schema-conformant object, normalizes the `audit_requirements` and `record_retention` enums, and ensures `compliance_calendar` consolidates deadlines from across both fragments.

## Manifestations

- [`prompt.md`](prompt.md) — canonical, LLM-agnostic prompt

## Evals

See [`evals/`](evals/) for reference inputs and known-good outputs.

## Provenance

Authored 2026-04-30 against the `award-compliance-extraction` (Workflow_ID: `WF-AWARD-COMPLIANCE-EXTRACTION`) process-mapping workflow in `ui-insight/ProcessMapping` at commit `b7176b0c913833a205efdb5e4ba00c17ff88af0f`.
