# Evals — cost-allowability-analysis workflow

Workflow-local evals. Each case lives under `cases/<case-slug>/` with at minimum `metadata.yaml`, `input-source.md`, `expected.md`, and optional `notes.md`. Run artifacts go under `runs/` (gitignored).

The workflow's final output is the Markdown determination from `cost-allowability-determination`, so workflow golden outputs are `expected.md`.

## Planned cases

- **Clean routine supply purchase** — end-to-end **Allowable** determination.
- **Travel charge over an award per-trip cap** — end-to-end **Not allowable** via the award-terms conformance check.
- **Participant-incentive gift cards with no IRB records** — end-to-end **Missing info** with the compliance-oversight flag raised by the protocol-approval check.

## `validated_against_version`

Every case must declare the workflow version that its `expected.md` was validated against.
