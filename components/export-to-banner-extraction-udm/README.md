# Export to Banner Award Extraction — UDM JSON

Extracts operational setup data from a fully-executed federal award document into the specific fields needed to populate the VERAS Export to Banner form. Focuses on Banner ERP-specific data points: award identification, dates and performance period, sponsor entity classification, budget structure and indirect-cost terms, billing and payment terms, and reporting / special-conditions text. Complements `award-compliance-extraction-udm` (broader compliance monitoring) by targeting only the operational fields Banner needs.

**Current version:** 0.1.0
**Category:** extraction
**Domain:** research-administration
**Status:** experimental
**Manifestations:** prompt
**Output contract:** [`schema.json`](schema.json)
**Contract scope:** repo-local, UDM-aligned

## Inputs

A fully-executed federal award document — federal notice of award, cooperative agreement, contract, or an award modification that updates Banner-relevant fields. Typically 5–50+ pages, including budget attachments and terms-and-conditions. Accepted file types in the source workflow: `.pdf`, `.docx`.

## Outputs

A single JSON object with six structured blocks:

- **`award_identification`** — `award_number` (FAIN), `project_title`, `pi_name`, `award_type` (four-value enum), `is_pass_through` (boolean), `prime_sponsor_name`, `cfda_number`, `naics_code`, `federal_agency_name`
- **`dates_and_performance`** — `award_start_date`, `award_end_date`, `performance_period_start`, `performance_period_end`, `budget_periods[]` (array of `{period_number, start_date, end_date, amount}`), `is_multi_year`
- **`sponsor_entity`** — `sponsor_name`, `sponsor_entity_type` (seven-value enum), `federal_agency_hierarchy`, `sponsor_address`, `sponsor_uei`, `awardee_organization`, `awardee_uei`
- **`budget_financial`** — `total_award_amount` (number), `total_anticipated_amount` (number), `budget_categories[]` (array of `{category, approved_amount}`), `total_direct_costs`, `total_indirect_costs` (numbers), `fa_rate` (string with base annotation), `fa_rate_base` (four-value enum), `is_fa_waived`, `cost_share_amount` (number), `cost_share_type`, `program_income`
- **`billing_payment`** — `billing_type` (four-value enum), `billing_frequency`, `billing_address`, `invoice_email`, `pms_loc_code`, `payment_terms`, `invoice_requirements[]`, `final_invoice_deadline`, `billing_contact`
- **`reporting_special`** — `reporting_requirements[]` (array of `{report_type, frequency, due_date_or_timing, submission_method}`), `record_retention_period`, `carry_forward_policy`, `prior_approval_requirements[]`, `special_terms[]`, `closeout_requirements`, `governing_regulations[]`

See [`schema.json`](schema.json) for the authoritative definition and [`prompt.md`](prompt.md) for encoding rules (monetary fields as JSON numbers, ISO date handling, enum policies, UEI / CFDA formatting).

## Contract scope

Repo-local, UDM-aligned. Broad UDM bindings via leaf-field column references: `Award`, `Personnel`, `Organization`, `AwardBudget`, `AwardBudgetPeriod`, `IndirectRate`, `CostShare`, `ContactDetails`, `Terms`. The six-block Banner-setup shape itself is repo-local and mirrors the source `ui-insight/ProcessMapping` workflow.

## Relationship to other components

| Concern | Source of truth |
|---|---|
| Operational Banner ERP setup from a fully-executed award | `export-to-banner-extraction-udm` (this component) |
| Broader compliance monitoring (high-risk conditions, audit thresholds, deliverable schedules, FFR / prior-approval categories) | [`award-compliance-extraction-udm`](../award-compliance-extraction-udm/) |
| FFR / SF-425 submission cadence | [`ffr-management-extraction-udm`](../ffr-management-extraction-udm/) |
| Prior-approval procedural mechanics per approval type | [`prior-approval-extraction-udm`](../prior-approval-extraction-udm/) |
| Modification intake on an amendment (vs. the original award) | [`award-modification-intake-udm`](../award-modification-intake-udm/) |

The five post-award components are versioned independently. A single award document may be extracted through more than one when downstream consumers need overlapping concerns.

## Triad integration

- **Evaluation datasets:** none yet — planned: an authorized, de-identified federal cooperative agreement with multi-year incremental funding, an explicit F&A rate cap, and a structured reporting table.
- **Harness notes:** canonical manifestation is `prompt.md`. Validation surface is `schema.json`. Vendored into runners via `harness prompts vendor --source-ref=<sha>`.
- **Shared UDM relationship:** aligned, not owning. Leaf-field bindings track shared UDM award concepts but the six-block Banner-setup surface is repo-local.

## Runtime topology — the Vandalizer workflow

The canonical runtime for this component is the [`export-to-banner-extraction` workflow](https://github.com/AI4RA/prompt-library/tree/main/workflows/export-to-banner-extraction) shipped at the top level of this repo. The single source of truth is [`workflows/export-to-banner-extraction/manifest.yaml`](https://github.com/AI4RA/prompt-library/blob/main/workflows/export-to-banner-extraction/manifest.yaml); the companion `.vandalizer.json` envelope is generated by [`scripts/build_vandalizer_workflows.py`](https://github.com/AI4RA/prompt-library/blob/main/scripts/build_vandalizer_workflows.py) and committed alongside. The runtime mirrors the source [`ui-insight/ProcessMapping/workflows/export-to-banner-extraction/`](https://github.com/ui-insight/ProcessMapping/tree/main/workflows/export-to-banner-extraction) workflow:

- **Step 1 (parallel Extraction)** — six Extraction tasks mirror the source workflow one-for-one (award-identification, dates-and-performance, sponsor-and-entity, budget-and-financial, billing-and-payment, reporting-and-special). Each task carries an embedded SearchSet whose item titles match the schema's block field names.
- **Step 2 (Consolidation Prompt)** — assembles the six JSON fragments into the schema-conformant six-block object, converts quoted dollar strings to JSON numbers, normalizes the four enums (`award_type`, `sponsor_entity_type`, `fa_rate_base`, `billing_type`), enforces the two source cross-field rules (CFR-01 `award_start < award_end`; CFR-02 `performance_period_start <= award_start_date` — flag in `special_terms` when violated rather than altering the dates).

Regenerate the workflow JSON whenever this component bumps MINOR or MAJOR (or whenever the workflow manifest changes); CI fails if the committed `.vandalizer.json` drifts from a fresh build.

## Manifestations

- [`prompt.md`](prompt.md) — canonical, LLM-agnostic prompt

## Evals

See [`evals/`](evals/) for reference inputs and known-good outputs. Initial case pending: an authorized, de-identified federal cooperative agreement with multi-year incremental funding and a structured reporting table, validated by a Post-Award Specialist.

## Provenance

Authored 2026-05-20 against the `export-to-banner-extraction` (Workflow_ID: `WF-EXPORT-BANNER-EXTRACTION`) process-mapping workflow in `ui-insight/ProcessMapping` at commit `2c1f47f46474130743af5aee44d074bcd21787e9`, which was built from the `PROC-EXPORT-TO-BANNER-REVIEW` process map. Created to make the Banner-setup data-entry step a harness-evaluatable, versioned artifact.
