# Evals — prior-approval-extraction-udm

Each case lives under `cases/<case-slug>/` with at minimum:

- `metadata.yaml` — case identity plus **`validated_against_version`** (required)
- `input-source.md` — where to obtain the source award notice
- `expected.json` — the known-good extraction, validated against `../../schema.json`
- `notes.md` — optional

Run artifacts go under `runs/` (gitignored).

## Planned cases

- **NSF standard award (RTC-eligible)** — exercises `rtc_waivers` with the standard expanded-authority delegations.
- **NIH R01 with explicit thresholds** — exercises `approval_procedures` with the equipment / foreign-travel / PI-substitution rows fully populated.
- **High-risk award with no RTC waivers** — exercises `rtc_waivers: []` and a fully-populated `approval_procedures` table.
- **Award with subaward approval requirement** — exercises `budget_approvals.subaward_approvals` and the corresponding `approval_procedures` row.

## `validated_against_version`

Every case must declare the component version that its `expected.json` was validated against.

## Triad alignment reminder

If this component gains a relationship to a dataset in `AI4RA/evaluation-data-sets`, update `component_catalog_overrides.yaml` at the repo root in the same PR.
