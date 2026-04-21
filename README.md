# AI4RA Prompt Library

Versioned prompts, skills, agents, schemas, and repo-local component contracts for AI4RA research-administration workflows.

This repository is the prompt-library leg of the AI4RA evaluation triad:

- `AI4RA/prompt-library` — prompts, skills, agents, schemas, and component contracts
- `AI4RA/evaluation-data-sets` — datasets, artifacts, and scoring references
- [`AI4RA/evaluation-harness`](https://github.com/AI4RA/evaluation-harness) — discovers components and datasets, runs evaluation campaigns, and publishes run artifacts
- `ui-insight/AI4RA-UDM` — shared UDM foundation where applicable

A change in one leg often implies a change in the others. Human-facing docs in this repo should line up with the machine-readable catalog so harness consumers are not forced to infer contract scope from prose.

**Browse the library:** [https://ai4ra.github.io/prompt-library/](https://ai4ra.github.io/prompt-library/)

**Machine-readable discovery:** [`component_catalog.json`](component_catalog.json)

## What lives here

Each component is a directory under `components/` named by a short slug. A component represents a single task and may expose one or more manifestations:

- `prompt.md` — the canonical, LLM-agnostic prompt
- `skill/SKILL.md` — Claude Skill form when a skill manifestation exists
- `agent/AGENT.md` — agent/subagent manifestation when orchestration behavior is part of the contract
- `schema.json` — machine-readable contract for structured outputs when the component has one
- `README.md` — human-readable overview, scope, provenance, and relationships
- `CHANGELOG.md` — per-component version history
- `evals/` — golden cases and, where present, published run reports

## Contract surfaces

Harness and automation consumers should start with these surfaces, in this order:

1. [`component_catalog.json`](component_catalog.json) — repo-level machine discovery surface for manifestations, contract scope, evaluation posture, related components, and observed upstream refs.
2. `components/<slug>/prompt.md` — canonical prompt manifestation.
3. `components/<slug>/skill/SKILL.md` or `agent/AGENT.md` — runtime-specific manifestations when a caller needs them.
4. `components/<slug>/schema.json` — authoritative structured-output contract when present.
5. `components/<slug>/evals/cases/*/metadata.yaml` plus `expected.*` — golden-case validation surface.

Important nuance: a component name that ends in `-udm` does **not** automatically mean the checked-in `schema.json` is the shared UDM contract from `ui-insight/AI4RA-UDM`. In this repo, many `-udm` components are repo-local extraction or routing contracts that align to shared UDM semantics without redefining the shared UDM itself. `component_catalog.json` records which contract scope applies per component.

## Versioning and evaluation

Each component is versioned independently with semver. Manifestations within one component stay in lockstep.

- **MAJOR** — output contract break for downstream consumers
- **MINOR** — backward-compatible capability or contract addition
- **PATCH** — wording, clarity, or non-behavioral cleanup

Evaluation posture is tracked per component by `validated_against_version` in each eval case's `metadata.yaml`. The repo computes a component's **last fully evaluated version** as the minimum validated version across its cases.

That distinction matters:

- `stable` means the contract is intended for downstream use and has validated reference coverage.
- `stable` does **not** mean every checked-in version has been fully revalidated against every case.
- Consumers should pin commit SHA + component version and check the component's last fully evaluated version before treating a run as release-grade evidence.

## Adding or updating a component

1. Copy `templates/new-component/` into `components/<slug>/`.
2. Fill in `README.md`, `prompt.md`, and `CHANGELOG.md`.
3. If the component has structured output, add `schema.json` and keep its version expectations aligned with the component's current version.
4. Add at least one eval case under `evals/cases/` with `metadata.yaml` and `expected.*`.
5. Add the component's triad metadata to [`component_catalog_overrides.yaml`](component_catalog_overrides.yaml) and regenerate [`component_catalog.json`](component_catalog.json).
6. Register any new controlled vocabulary in [`taxonomy.md`](taxonomy.md).
7. Regenerate docs so the site and catalog stay aligned.

## Local validation

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

If `mkdocs` is already on `PATH`, the bare `mkdocs` command is equivalent; the `python3 -m mkdocs` form is more robust across environments.

## CI

Two GitHub Actions workflows run on pushes to `main`:

- [`lint.yml`](.github/workflows/lint.yml) checks component manifests, taxonomy usage, eval validation metadata, lockstep manifestation versions, and that [`component_catalog.json`](component_catalog.json) matches the generated catalog.
- [`pages.yml`](.github/workflows/pages.yml) regenerates [`component_catalog.json`](component_catalog.json), rebuilds generated docs from components, and publishes the MkDocs site.

## Observed upstream refs

The current triad alignment in this repo was refreshed against these observed upstream heads on **2026-04-21**:

| Upstream | Branch | Observed commit |
| --- | --- | --- |
| `AI4RA/evaluation-harness` | `main` | `02a7583abdade86877f9f1b4a70fde078f982d40` |
| `AI4RA/evaluation-data-sets` | `main` | `85c2d11d5f4d808b218716e90f590b1863bdffde` |
| `ui-insight/AI4RA-UDM` | `main` | `9e85e44cf181dbb54c573cde2a89df2a287af2d0` |

These refs are recorded in [`component_catalog.json`](component_catalog.json) so downstream consumers do not have to infer cross-repo assumptions from floating `main` links.

## License and citation

This repository is licensed under the [GNU General Public License v3.0](LICENSE).

**Any use of this work requires citation.** This includes research publications, derivative components, downstream software, internal tooling, and production deployments. The citation requirement is a condition of use alongside — not in place of — the GPL's obligations.

Machine-readable citation metadata lives in [`CITATION.cff`](CITATION.cff). When citing a specific state of the repository, pin to the commit SHA and the component version you used:

> Robison, B. (2026). *AI4RA Prompt Library* (commit `<sha>`, component `<slug>` v`<version>`). https://github.com/AI4RA/prompt-library
