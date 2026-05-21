# Evals — award-modification-intake-udm

Each case lives under `cases/<case-slug>/` with at minimum:

- `metadata.yaml` — case identity plus **`validated_against_version`** (required): the component version at which the expected output was last human-validated
- `input-source.md` — where to obtain the source modification document (sponsor URL, document title, retrieval date)
- `expected.json` — the known-good extraction, validated against `../../schema.json` and reviewed by a Post-Award Specialist
- `notes.md` — optional; qualitative observations from review

Run artifacts go under `runs/` (gitignored).

## Planned cases

The first cases should exercise distinct structural features of the contract, not simply add volume:

- **Additional-funds modification with reconciling totals** — exercises `modification_type: "Additional Funds"`, `modification_amount > 0`, and the CFR-04 reconciliation rule between `modification_amount`, `current_award_amount`, and `total_obligated_amount`.
- **No-cost extension with new end date** — exercises `modification_type: "No-Cost Extension"`, populates `new_end_date`, and leaves financial fields at their pre-NCE values.
- **PI change with old / new pair** — exercises `modification_type: "PI Change"`, populates both `old_pi` and `new_pi`, and leaves `modification_amount` null per the source workflow rule.
- **Rebudget with source / destination accounts** — exercises `modification_type: "Rebudget"`, populates both `rebudget_source_account` and `rebudget_destination_account`, captures a multi-row `budget_breakdown`, and sets `requires_financial_unit: false`.
- **Bilateral modification with sponsor conditions** — exercises `execution_status: "Bilateral (requires signature)"`, a non-empty `sponsor_conditions` array, and at least one `regulatory_references` entry pointing at 2 CFR 200.308.

## `validated_against_version`

Every case must declare the component version that its `expected.json` was validated against. Re-running evals at a new component version: if the expected output did not change, bump only `validated_against_version`. If it did change, update `expected.json` and `validated_against_version` together.

## Triad alignment reminder

If this component gains a relationship to a dataset in `AI4RA/evaluation-data-sets` (e.g., a new `real.award_modifications` dataset), update `component_catalog_overrides.yaml` at the repo root in the same PR.
