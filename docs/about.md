# About the AI4RA Prompt Library

The AI4RA Prompt Library is a versioned store of prompts, skills, agents, schemas, and component contracts for research-administration work. It is the prompt-library leg of the AI4RA evaluation triad: the evaluation harness discovers components here, pairs them with datasets from `AI4RA/evaluation-data-sets`, and applies the shared `ui-insight/AI4RA-UDM` foundation where a component is UDM-aligned.

## What's in a component

Every component lives under `components/<slug>/` and may ship with:

- `README.md` — human-readable overview, scope, provenance, and relationships.
- `prompt.md` — canonical prompt body plus YAML frontmatter.
- `skill/SKILL.md` — Claude Skill manifestation, when present.
- `agent/AGENT.md` — agent/subagent manifestation, when present.
- `schema.json` — structured contract for machine validation, when present.
- `CHANGELOG.md` — per-component semver history.
- `evals/cases/<case>/` — golden cases with validation metadata.
- `evals/reports/<run-id>/` — published evaluation runs, when available.

Components share controlled vocabulary for `category`, `domain`, and `status`; see the [Taxonomy](taxonomy.md) page.

## Machine-readable discovery

Start with [`component_catalog.json`](https://github.com/AI4RA/prompt-library/blob/main/component_catalog.json). It records:

- manifestations present for each component
- output-contract format and scope
- evaluation posture, including last fully evaluated version
- related components and harness notes
- observed upstream refs for `AI4RA/evaluation-data-sets` and `ui-insight/AI4RA-UDM`

The catalog exists so harness consumers do not have to infer repo-level semantics from README prose alone.

## Contract scope

This repo uses a few different contract classes, and the distinction matters:

- **Repo-local contract** — owned entirely in this repository. Examples include human-readable markdown outputs and local JSON schemas that model sponsor defaults or solicitation diffs.
- **UDM-aligned repo-local schema** — a local schema whose field meanings align with shared UDM concepts, but whose extraction surface is maintained here rather than in `ui-insight/AI4RA-UDM`.
- **Delegated wrapper contract** — a component whose local schema explicitly delegates to another repo-local schema so downstream tools have a concrete contract surface without relying on prose.

A `-udm` suffix signals UDM-oriented intent, not automatic ownership by the shared UDM repo.

## Relationship to the shared UDM

The canonical shared UDM lives at [`ui-insight/AI4RA-UDM`](https://github.com/ui-insight/AI4RA-UDM). This prompt library does not redefine that repository's role.

Instead, components in this repo do one of three things:

- align a local extraction schema to shared UDM semantics
- maintain a repo-local vocabulary that supports UDM-oriented workflows
- remain entirely repo-local because the contract is human-facing or sponsor-specific

When a change has shared-UDM implications, contributors should update the prompt-library component, the catalog metadata, and the cross-repo notes together so the triad stays pinned to the same assumption set.

## Versioning and evaluation posture

Each component follows semver independently, and manifestations within one component stay in lockstep. Eval cases carry `validated_against_version`, which means a component can be `stable` while still having a current version that is ahead of its last fully revalidated golden set. The generated component pages surface that distinction directly.

## This site

This site is generated from the checked-in component files plus the repo-level catalog metadata. Edit the source component, regenerate the catalog/docs, and the site will stay aligned without copy-pasted documentation forks.
