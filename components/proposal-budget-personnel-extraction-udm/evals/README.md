# Evals — proposal-budget-personnel-extraction-udm

Each case lives under `cases/<case-slug>/` with at minimum `metadata.yaml`, `input-source.md`, `expected.json`, and optional `notes.md`. Run artifacts go under `runs/` (gitignored).

## Planned cases

- **NSF proposal with postdocs and grad students** — exercises `mentoring_plan_required: true`, non-empty postdoc and graduate-student details with at least one TBN slot.
- **NSF proposal with subaward and equipment > $5K** — exercises `has_subawards: true` and `has_equipment_over_5k: true`.
- **NIH proposal with cost-share commitment** — exercises `cost_sharing` populated.
- **Single-PI bare-bones proposal** — exercises `mentoring_plan_required: false`, all triggers false, single-period budget.

## `validated_against_version`

Every case must declare the component version that its `expected.json` was validated against.
