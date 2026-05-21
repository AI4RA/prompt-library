# Evals — regulated-activity-classifier

Each case lives under `cases/<case-slug>/` with at minimum `metadata.yaml`, `input-source.md`, `expected.json`, and optional `notes.md`. Run artifacts go under `runs/` (gitignored).

## Planned cases

- **Participant gift cards** — exercises a `human_subjects` flag from an incentive-payment signal.
- **Vivarium per-diem charge** — exercises an `animal` flag from a housing-recharge signal.
- **Lentiviral vector reagent** — exercises a `biosafety` flag from a viral-vector signal.
- **Routine office supplies** — exercises the all-clear case: no regime triggered.

## `validated_against_version`

Every case must declare the component version that its `expected.json` was validated against.
