# AI4RA Prompt Library Agent Guide

This repository is the prompt-library leg of the AI4RA triad. It owns prompts, skills, agents, schemas, and component contracts.

## Read order

1. `README.md`
2. `TRIAD.md`
3. `triad.workspace.yaml`
4. `component_catalog.json`
5. `component_catalog_overrides.yaml`
6. `docs/contracts.md` and `docs/ecosystem.md`
7. the specific `components/<slug>/` directory you are changing

## Default scope

- Start in this repository first.
- Do not read all triad repos by default.
- Open sibling repos when the task touches dataset expectations, harness vendoring or discovery, shared UDM scope, or observed upstream refs.

## Contract boundaries

- `component_catalog.json` is the repo-level machine discovery surface.
- `component_catalog_overrides.yaml` is the editable source for repo-level triad metadata and observed upstream refs.
- `components/<slug>/schema.json` is authoritative for that component's structured output contract when present.
- `components/<slug>/workflows/<wf-slug>/manifest.yaml` is the authored source for a Vandalizer-workflow manifestation; the sibling `<wf-slug>.vandalizer.json` is generated and must not be hand-edited.
- A `-udm` suffix in a component slug does not automatically mean the checked-in schema is the shared UDM contract from `ui-insight/AI4RA-UDM`.
- Record contract scope explicitly as repo-local, UDM-aligned repo-local, delegated wrapper, or shared UDM backed.

## Cross-repo triggers

Open `AI4RA/evaluation-data-sets` when:

- a component contract change affects expected outputs, golden cases, or dataset-side validation language
- a dataset relationship or scoring reference described in this repo changed
- observed dataset refs need to be refreshed

Open `AI4RA/evaluation-harness` when:

- vendored prompt snapshots, harness discovery, or runnable dataset registration needs to reflect a new component state
- harness-local scoring surfaces or catalog notes mention a changed component contract
- observed harness refs need to be refreshed

Open `ui-insight/AI4RA-UDM` when:

- the change depends on a shared UDM field definition or contract boundary
- you need to prove a schema is shared UDM rather than only UDM-aligned repo-local

## Validation

Run the commands that match your change:

```bash
python3 scripts/build_component_catalog.py
python3 scripts/build_vandalizer_workflows.py
python3 .github/scripts/lint_components.py
python3 scripts/build_docs.py
python3 -m mkdocs build --strict
```

## Editing rules

- Keep human-facing docs, component manifests, and `component_catalog.json` aligned in the same change.
- Prefer pinning observed upstream SHAs over floating branch names.
- When a change is repo-local only, say that clearly instead of implying wider harness, dataset, or UDM support.
