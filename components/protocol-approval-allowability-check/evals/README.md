# Evals — protocol-approval-allowability-check

Each case lives under `cases/<case-slug>/` with at minimum `metadata.yaml`, `input-source.md`, `expected.json`, and optional `notes.md`. Run artifacts go under `runs/` (gitignored).

## Planned cases

- **No regime flagged** — exercises `not_applicable`.
- **Animal per-diem with a current in-scope IACUC protocol** — exercises `pass`.
- **Participant payment with no IRB evidence supplied** — exercises `needs_info`.
- **Viral-vector reagent dated before IBC approval** — exercises `not_allowable`.

## `validated_against_version`

Every case must declare the component version that its `expected.json` was validated against.
