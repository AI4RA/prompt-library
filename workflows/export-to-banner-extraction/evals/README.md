# Evals — export-to-banner-extraction (workflow-local)

This workflow carries its own cases under `cases/` because it is **not** a 1:1 repackaging of the `export-to-banner-extraction-udm` component's canonical prompt. Each Extraction task carries a focused `prompt_inline` body covering a single block, and the Consolidation Prompt converts quoted-dollar strings to JSON numbers and emits CFR-01 / CFR-02 flag strings to `reporting_special.special_terms`. The workflow's behavior emerges from step interactions that no component-level eval can cover on its own.

Each case lives under `cases/<case-slug>/` with the same shape as component evals:

- `metadata.yaml` — case identity plus `validated_against_version` (the **workflow** version)
- `input-source.md` — where to obtain the source award document (sponsor URL, document version, date retrieved)
- `expected.json` — the known-good consolidated workflow output, validated by a Post-Award Specialist; conforms to [`components/export-to-banner-extraction-udm/schema.json`](https://github.com/AI4RA/prompt-library/blob/main/components/export-to-banner-extraction-udm/schema.json)
- `notes.md` — optional; qualitative observations from review

Run artifacts go under `runs/` (gitignored).

## What workflow-local cases need to exercise

The component contract (single-call extraction) is already covered by `components/export-to-banner-extraction-udm/evals/`. Workflow-local cases here should target behavior that only emerges from the seven-task topology:

- **Multi-year cooperative agreement** — `award_type: "Cooperative Agreement"`, `is_multi_year: true`, populated `budget_periods` array, distinct `total_award_amount` and `total_anticipated_amount`. Exercises the dates-and-performance multi-row table consolidation.
- **Cost-reimbursable contract with quarterly invoicing** — `billing_type: "Cost Reimbursement"`, `billing_frequency: "Quarterly"`, populated `invoice_requirements` array.
- **Fixed-price subcontract with prime sponsor** — `is_pass_through: true`, populated `prime_sponsor_name`, `award_type: "Subcontract"`, `billing_type: "Fixed Price"`.
- **F&A rate cap with base annotation** — `fa_rate` string carries `"% MTDC"` suffix, `fa_rate_base: "MTDC"`, non-null `cost_share_amount` as a JSON number.
- **Quoted-dollar-to-JSON-number conversion** — when extractor surfaces quoted strings (`"$1,234,567.89"`), the consolidator converts them to JSON numbers.
- **CFR-01 / CFR-02 flag emission** — when the source document is internally inconsistent (`award_start_date >= award_end_date` or `performance_period_start > award_start_date`), the consolidator appends a flag string to `reporting_special.special_terms` without altering the dates.

## `validated_against_version`

Every case must declare the **workflow** version at which the expected output was last human-validated. This is distinct from the component's `validated_against_version`: when the workflow's step structure changes (MAJOR bump) or the consolidation prompt changes (MINOR bump), the expected output may need re-validation even though the underlying component is unchanged.

Capture the resolved component versions in `component_versions_at_validation` for reproducibility.

## Status

The initial scaffolded case (`federal-cooperative-agreement-stub`) is a placeholder pending Post-Award Specialist review against an authorized, de-identified federal cooperative agreement with multi-year incremental funding. It should be replaced with the validated case before this workflow is promoted from `experimental` to `stable`.
