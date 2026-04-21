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
| [`taxonomy.md`](https://github.com/AI4RA/prompt-library/blob/main/taxonomy.md) | Controlled vocabulary for categories, domains, and lifecycle status. |

## Reading contract scope

The component catalog records contract scope explicitly because not every `-udm` component means the same thing.

- `repo_local_*` scopes mean the contract is owned in this repository.
- `shared_udm_semantics_repo_local_schema` means the schema aligns to shared UDM concepts but is still maintained here.
- `delegated_repo_local_schema` means the local component exposes a wrapper contract that delegates to another repo-local schema.

If a consumer needs the canonical shared UDM itself, the source of truth is [`ui-insight/AI4RA-UDM`](https://github.com/ui-insight/AI4RA-UDM), not a prompt-library component name.

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
