# Evals — rfa-checklist-extraction-udm

Each case lives under `cases/<case-slug>/` with at minimum:

- `metadata.yaml` — case identity plus **`validated_against_version`** (required): the component version at which the expected output was last human-validated
- `input-source.md` — where to obtain the source RFA (sponsor URL, PDF title, retrieval date)
- `expected.json` — the known-good extraction, validated against `../../schema.json` and reviewed by a sponsored-programs analyst
- `notes.md` — optional; qualitative observations from review

Run artifacts go under `runs/` (gitignored).

## Planned cases

The first cases should exercise distinct structural features of the contract, not simply add volume:

- **Multi-round NSF solicitation** — exercises `dates_and_deadlines` round handling, LOI vs. full proposal placement, and round-specific notes.
- **Cost-sharing prohibition (NSF PAPPG-compliant)** — exercises the `cost_sharing.status: "Prohibited"` branch with no `details`.
- **NIH R01 or K-award** — exercises `eligible_individuals.criteria` with career-stage and citizenship rules, and `personnel_effort` with percent-effort minimums.
- **Announcement with explicit allowable/unallowable enumeration** — exercises both `allowable_costs` and `unallowable_costs` as non-empty arrays with sponsor-quoted language.
- **Rolling / open-ended announcement** — exercises `dates_and_deadlines` with `"Rolling"` entries and `submission_deadline` null-equivalent.

## `validated_against_version`

Every case must declare the component version that its `expected.json` was validated against. Re-running evals at a new component version: if the expected output did not change, bump only `validated_against_version`. If it did change, update `expected.json` and `validated_against_version` together.

## Triad alignment reminder

If this component gains a relationship to a dataset in `AI4RA/evaluation-data-sets` (e.g., a new `real.rfa_checklists` dataset), update `component_catalog_overrides.yaml` at the repo root in the same PR.
