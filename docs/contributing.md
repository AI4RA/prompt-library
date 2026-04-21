# Contributing

This site is generated directly from the [`AI4RA/prompt-library`](https://github.com/AI4RA/prompt-library) repository. When you add or change a component, keep the human-facing docs and machine-facing catalog aligned in the same change.

## Adding a new component

1. Pick a lowercase, hyphenated slug under `components/`.
2. Copy `templates/new-component/` to `components/<slug>/`.
3. Fill in `prompt.md`, `README.md`, and `CHANGELOG.md`.
4. If the output is structured, add `schema.json` and state clearly whether it is repo-local, UDM-aligned repo-local, or a delegated wrapper contract.
5. Add at least one eval case under `evals/cases/<case>/` with `metadata.yaml` and `expected.*`.
6. Add the component's triad metadata to [`component_catalog_overrides.yaml`](https://github.com/AI4RA/prompt-library/blob/main/component_catalog_overrides.yaml).
7. Regenerate [`component_catalog.json`](https://github.com/AI4RA/prompt-library/blob/main/component_catalog.json) and the docs site.
8. If you introduced new controlled vocabulary, update [Taxonomy](taxonomy.md) in the same PR.

## Keeping human docs and machine metadata in sync

When a component changes, update all of the surfaces that express the same fact:

- `README.md` for the human explanation
- `prompt.md` / `skill/SKILL.md` / `agent/AGENT.md` for the manifestations
- `schema.json` for the structured contract, when present
- `component_catalog_overrides.yaml` for triad relationships, contract scope, and harness notes
- `evals/cases/*/metadata.yaml` when validation posture changed

If one of those is intentionally unchanged, the PR description should make that clear.

## Rebuilding the catalog and site locally

```bash
python3 scripts/build_component_catalog.py
python3 .github/scripts/lint_components.py
python3 scripts/build_docs.py
python3 -m mkdocs build --strict
```

For local preview:

```bash
python3 -m mkdocs serve
```

Open <http://127.0.0.1:8000/>. `python3 -m mkdocs serve` watches `docs/` for changes. If you edit a component or the catalog overrides file, rerun the relevant generator before refreshing.

## Cross-repo contracts

If a change depends on `AI4RA/evaluation-data-sets` or `ui-insight/AI4RA-UDM`:

1. update the human prose that describes the dependency,
2. update `component_catalog_overrides.yaml`, and
3. refresh the observed upstream ref recorded in `component_catalog.json`.

That keeps the prompt-library leg of the triad pinned to a concrete upstream observation instead of a floating branch assumption.

## CI

Every push to `main` runs lint and pages workflows. Lint now checks that `component_catalog.json` matches generated repo state; Pages regenerates the catalog before rebuilding the docs site.
