# Evals — proposal-budget-personnel-extraction (workflow-local)

This workflow carries its own cases under `cases/` because the Consolidation Prompt **derives** four boolean compliance triggers from list lengths and combines `fa_rate` + `fa_base` into a nested object — emergent behavior that no component-level eval can cover on its own.

## What workflow-local cases need to exercise

- **Boolean derivation** — `has_postdocs_or_grad_students = (postdoc_count > 0) OR (graduate_student_count > 0)`; `mentoring_plan_required = has_postdocs_or_grad_students` (default); `has_subawards = len(subaward_recipients) > 0`; `has_equipment_over_5k = len(equipment_items) > 0`. CHK-02 fails if any boolean disagrees with its derivation.
- **F&A rate-and-base composition** — `fa_rate` and `fa_base` from the upstream extractor combine into a single `fa_rate_and_base: {rate, base}` object on output.
- **Equipment threshold** — items below $5,000 must not appear in `equipment_items`.
- **Cost totals reconciliation** — CHK-03: `total_costs.total_project_cost == total_costs.total_direct_costs + total_costs.total_indirect_costs`.
- **TBN handling** — to-be-named postdoc / graduate-student slots appear in details with `name: "TBN"` rather than being dropped.

## Status

The initial scaffolded case (`nsf-with-postdocs-and-subawards-stub`) is a placeholder pending sponsored-programs review against an authorized, de-identified NSF proposal that includes both postdocs and a subaward.
