# Contract Surfaces

This repository has both human-facing documentation and machine-facing contract surfaces. Downstream harness consumers should rely on the machine-facing surfaces first, then use the prose pages for context and interpretation.

## Primary machine-readable surfaces

| Surface | Role |
| --- | --- |
| [`component_catalog.json`](https://github.com/AI4RA/prompt-library/blob/main/component_catalog.json) | Primary repo-level discovery surface for components, manifestations, contract scope, evaluation posture, and observed upstream refs. |
| `components/<slug>/prompt.md` | Canonical prompt manifestation. |
| `components/<slug>/skill/SKILL.md` | Claude Skill manifestation when a skill exists. |
| `components/<slug>/agent/AGENT.md` | Agent manifestation when orchestration behavior is part of the contract. |
| `components/<slug>/schema.json` | Structured output contract when the component has one. |
| `components/<slug>/evals/cases/*/metadata.yaml` | Validation metadata, including `validated_against_version`. |
| `components/<slug>/workflows/<wf-slug>/manifest.yaml` | Authored single-component Vandalizer-workflow source. Declares workflow version, pinned component version, steps, and eval posture. |
| `components/<slug>/workflows/<wf-slug>/<wf-slug>.vandalizer.json` | Generated Vandalizer export, rebuilt from the manifest. Carries an `x_ai4ra` provenance block (workflow source path, pinned component versions, embedded-prompt SHA256). Never hand-edited. |
| `workflows/<wf-slug>/manifest.yaml` | Authored multi-component orchestration source. Same shape as the component-scoped manifest, pins two or more components. Used when a workflow does not belong to a single component. |
| `workflows/<wf-slug>/<wf-slug>.vandalizer.json` | Generated Vandalizer export for the multi-component orchestration. Same provenance conventions as single-component exports. |
| [`taxonomy.md`](https://github.com/AI4RA/prompt-library/blob/main/taxonomy.md) | Controlled vocabulary for categories, domains, and lifecycle status. |

## Reading contract scope

The component catalog records contract scope explicitly because not every `-udm` component means the same thing.

- `repo_local_*` scopes mean the contract is owned in this repository.
- `shared_udm_semantics_repo_local_schema` means the schema aligns to shared UDM concepts but is still maintained here.
- `delegated_repo_local_schema` means the local component exposes a wrapper contract that delegates to another repo-local schema.

If a consumer needs the canonical shared UDM itself, the source of truth is [`ui-insight/AI4RA-UDM`](https://github.com/ui-insight/AI4RA-UDM), not a prompt-library component name.

## Workflow manifestations

A workflow is a Vandalizer-shaped manifestation of one or more components. Each `components/<slug>/workflows/<wf-slug>/` directory has an authored `manifest.yaml` (source of truth) and a generated `<wf-slug>.vandalizer.json` (the uploadable export). The two are kept consistent by `scripts/build_vandalizer_workflows.py`; CI runs the builder's `--check` mode via the lint script.

- Manifests pin the component version(s) they manifest. A workflow MAJOR re-pins a component MAJOR; when any referenced component bumps MAJOR the workflow must re-pin and bump its own MAJOR, or be marked retired.
- **Single-component workflows** live under `components/<slug>/workflows/<wf-slug>/` and belong to that one component's lifecycle. **Multi-component orchestrations** live under top-level `workflows/<wf-slug>/` because they pin two or more components and no single component owns them.
- A workflow's eval posture is either **inherited** (1:1 repackaging of a component's canonical prompt — reuses the component's evals) or **workflow-local** (multi-step orchestration, parameterization, or prompt override — carries its own `evals/cases/` under the workflow directory). Multi-component orchestrations are always `workflow_local` because the pipeline's behavior emerges from step interactions.
- The generated export's `x_ai4ra` block makes round-tripped exports traceable back to a specific prompt-library commit, including the SHA256 of each embedded prompt body.
- `component_catalog.json` surfaces workflows in two places: each component's entry carries a `workflows: [...]` array for its own single-component workflows, and the top-level `workflows: [...]` array surfaces multi-component orchestrations. Optional triad metadata lives in `component_catalog_overrides.yaml` under either the component's `workflows:` mapping or the top-level `workflows:` mapping.

## Harness expectations

A harness integrating this repo should:

1. start with `component_catalog.json`,
2. choose the manifestation it can execute,
3. validate output against the declared schema or golden-case surface,
4. respect the component's last fully evaluated version, and
5. use the triad integration notes when pairing components to datasets or UDM-aligned workflows.

## Observed upstream refs

These are the upstream observations recorded in this repo as of **2026-04-21**:

| Upstream | Branch | Observed commit |
| --- | --- | --- |
| `AI4RA/evaluation-data-sets` | `main` | `85c2d11d5f4d808b218716e90f590b1863bdffde` |
| `ui-insight/AI4RA-UDM` | `main` | `9e85e44cf181dbb54c573cde2a89df2a287af2d0` |

The values above are mirrored in `component_catalog.json` so downstream tools do not have to scrape this page.
