# Evals — effort-reporting-extraction (workflow-local)

This workflow carries its own cases under `cases/` because the Consolidation Prompt enforces the PI-mirror rule across `pi_committed_effort` / `pi_person_months` / `key_personnel_commitments` and normalizes the `reporting_frequency` and `certification_method` enums, so the workflow's behavior emerges from step interactions that no component-level eval can cover on its own.

## What workflow-local cases need to exercise

- **Enum normalization** — `reporting_frequency` and `certification_method` mapped from document phrasings to enum values.
- **PI-mirror rule** — the PI's row in `key_personnel_commitments` mirrors `pi_committed_effort` and `pi_person_months` exactly.
- **Cost-shared effort propagation** — when the document records cost-shared effort against a specific person, the per-row `cost_shared_effort` field must populate (not just the top-level scalar).
- **Validation-plan checks** — effort percentages sum (CHK-01), person-months consistency (CHK-02), personnel table completeness (CHK-03).

## Status

The initial scaffolded case (`nih-r01-summer-months-stub`) is a placeholder pending sponsored-programs review against an authorized, de-identified NIH R01 award notice with summer-month commitment.
