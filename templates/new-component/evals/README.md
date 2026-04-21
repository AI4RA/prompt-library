# Evals — [component-slug]

Each case lives under `cases/<case-slug>/` with at minimum:

- `metadata.yaml` — case identity plus **`validated_against_version`** (required): the component version at which the expected output was last human-validated
- `input-source.md` — where to obtain the source input (URL, document version, date retrieved)
- `expected.md` / `expected.json` / etc. — the known-good output, validated by a human reviewer
- `notes.md` — optional; qualitative observations from review

Run artifacts go under `runs/` (gitignored).

## `validated_against_version`

Every case must declare the component version that its `expected.*` was validated against. The linter computes the component's "last fully evaluated version" as the minimum `validated_against_version` across all its cases, and warns when the component's current version has moved ahead.

When you re-run evals and confirm the output is still correct at a new version:

- If the expected output did not need to change, update only `validated_against_version` (and optionally `validated_at`).
- If the expected output did change, update the output file **and** `validated_against_version`.

## Triad alignment reminder

If this component also gains or changes a relationship to `AI4RA/evaluation-data-sets` or the shared UDM foundation, update `component_catalog_overrides.yaml` in the same PR so the human docs and machine-readable catalog stay aligned.

## Case selection

Prefer cases that each exercise a distinct edge case or structural feature of the component's input. A case that only duplicates coverage from an existing case is noise.
