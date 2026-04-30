# Evals — effort-reporting-extraction-udm

Each case lives under `cases/<case-slug>/` with at minimum `metadata.yaml`, `input-source.md`, `expected.json`, and optional `notes.md`. Run artifacts go under `runs/` (gitignored).

## Planned cases

- **NIH R01 with summer-month commitment** — exercises `pi_committed_effort: "2.0 summer months"`, `pi_person_months: "2.0"`, and `certification_method: "After-the-Fact"`.
- **NSF award with cost-shared academic-year effort** — exercises `cost_shared_effort` populated and a non-empty cost-shared row in `key_personnel_commitments`.
- **HHS-funded award using Plan-Confirmation** — exercises the `Plan-Confirmation` certification method enum.
- **Award with a single PI, no co-PIs** — exercises `key_personnel_commitments` as a single-element array mirroring the PI scalars.

## `validated_against_version`

Every case must declare the component version that its `expected.json` was validated against.
