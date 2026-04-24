# Evals — [workflow-slug]

Workflow evals are required only when the workflow is **not** a 1:1 repackaging of a component's canonical prompt. If the workflow has exactly one step, one task, and a `prompt_ref` pointing at a component's canonical prompt body with no `prompt_inline` overrides, set `inherits_from` in `manifest.yaml` and delete this directory.

When workflow-local evals are appropriate — multi-step orchestration, parameterization, or prompt override — each case lives under `cases/<case-slug>/` with the same shape as component evals:

- `metadata.yaml` — case identity plus `validated_against_version`
- `input-source.md` — where to obtain the source input (URL, document version, date retrieved)
- `expected.md` / `expected.json` / etc. — the known-good workflow output, validated by a human reviewer
- `notes.md` — optional; qualitative observations from review

Run artifacts go under `runs/` (gitignored).

## `validated_against_version`

Every workflow-local case must declare the **workflow version** at which the expected output was last human-validated. This is distinct from component `validated_against_version`: a workflow version pins specific component versions, and the workflow's behavior can change even when the component underneath is unchanged (step restructuring, new parameters).

Capture the resolved component versions in `component_versions_at_validation` for reproducibility. When you re-run evals at a new workflow version:

- If the expected output did not need to change, update only `validated_against_version` and `validated_at`.
- If the expected output changed, update the output file **and** `validated_against_version`, and refresh `component_versions_at_validation`.

## Triad alignment reminder

If this workflow starts interacting with `AI4RA/evaluation-data-sets` or the evaluation harness as a runnable target, update `component_catalog_overrides.yaml` in the same PR so the human docs and the machine-readable catalog stay aligned.

## Case selection

Prefer cases that each exercise a distinct step interaction, data-flow edge, or parameterization the workflow adds on top of the underlying component(s). A workflow-local case that only duplicates coverage from a component's evals is noise — inherit instead.
