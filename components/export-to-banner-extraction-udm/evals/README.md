# Evals — export-to-banner-extraction-udm

Each case lives under `cases/<case-slug>/` with at minimum:

- `metadata.yaml` — case identity plus **`validated_against_version`** (required): the component version at which the expected output was last human-validated
- `input-source.md` — where to obtain the source award document (sponsor URL, document title, retrieval date)
- `expected.json` — the known-good extraction, validated against `../../schema.json` and reviewed by a Post-Award Specialist
- `notes.md` — optional; qualitative observations from review

Run artifacts go under `runs/` (gitignored).

## Planned cases

The first cases should exercise distinct structural features of the contract, not simply add volume:

- **Federal cooperative agreement with multi-year incremental funding** — exercises the `budget_periods[]` array population, `is_multi_year: true`, the `total_award_amount` vs `total_anticipated_amount` distinction, and the `award_type: "Cooperative Agreement"` enum value.
- **Cost-reimbursable contract with quarterly invoicing** — exercises `billing_type: "Cost Reimbursement"`, `billing_frequency: "Quarterly"`, the `invoice_requirements[]` array, and the `final_invoice_deadline` field.
- **Fixed-price subcontract with prime sponsor** — exercises `is_pass_through: true`, populated `prime_sponsor_name`, `award_type: "Subcontract"`, `billing_type: "Fixed Price"`.
- **F&A rate cap with explicit base** — exercises `fa_rate` with `"% MTDC"` annotation, `fa_rate_base: "MTDC"`, `is_fa_waived: false`, and a non-null `cost_share_amount`.
- **Date inconsistency edge case** — `performance_period_start > award_start_date` (CFR-02 violation). The consolidator must flag this in `reporting_special.special_terms` without altering the dates.

## `validated_against_version`

Every case must declare the component version that its `expected.json` was validated against. Re-running evals at a new component version: if the expected output did not change, bump only `validated_against_version`. If it did change, update `expected.json` and `validated_against_version` together.

## Triad alignment reminder

If this component gains a relationship to a dataset in `AI4RA/evaluation-data-sets` (e.g., a new `real.federal_award_banner_exports` dataset), update `component_catalog_overrides.yaml` at the repo root in the same PR.
