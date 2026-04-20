# About the AI4RA Prompt Library

The AI4RA Prompt Library is a versioned store of LLM components — prompts, skills, and agents — designed for research-administration work. Components here are authored once and reused across AI4RA applications so the same underlying task (for example, "extract structure from an NSF award notice") stays consistent regardless of which client — raw prompt, Claude Skill, or agent — invokes it.

## What's in a component

Every component lives under `components/<slug>/` and ships with:

- **`README.md`** — human-readable overview: what it does, inputs, outputs, relationship to other components, provenance.
- **`prompt.md`** — the canonical, LLM-agnostic prompt body with YAML frontmatter describing the component (name, version, category, domain, status, tags, audience, dates).
- **`CHANGELOG.md`** — version history. Per-component semver; bumped in lockstep across all manifestations when the component changes.
- **`schema.json`** (when the output contract is structured) — JSON Schema (draft 2020-12) describing the emitted shape.
- **`skill/SKILL.md`** (optional) — Claude Skill manifestation with trigger description.
- **`agent/AGENT.md`** (optional) — subagent or agent manifestation.
- **`evals/cases/<case>/`** — golden input/output pairs with metadata.

Components share a controlled vocabulary for `category`, `domain`, and `manifestations` — see the [Taxonomy](taxonomy.md) page.

## Relationship to the canonical UDM

Many components produce JSON that ingests into a **Unified Data Model (UDM)**-conformant store. The canonical UDM — a relational schema covering Award, Modification, AwardBudget, Subaward, and related research-administration tables — lives at [`ui-insight/AI4RA-UDM`](https://github.com/ui-insight/AI4RA-UDM). This library does not redefine the UDM; its per-component `schema.json` files are *output contracts* aligned with the UDM's semantics. Schema changes with UDM implications are discussed in issues on that repo before landing here.

## Versioning

Each component is versioned independently using semver:

| Bump | Meaning |
| --- | --- |
| **MAJOR** | Output contract breaks — fields dropped or renamed, required-field changes, enum narrowing. |
| **MINOR** | Backward-compatible additions — new optional fields, new enum values, new manifestations. |
| **PATCH** | Wording or clarity — no behavior change expected. |

The `version` field in every manifestation's YAML frontmatter, the header in `README.md`, and the `schema.json` `version` field are kept in lockstep.

## This site

This site is generated directly from the contents of [the GitHub repository](https://github.com/AI4RA/prompt-library). Every component page is built from that component's files — no duplicated content. To propose a change, edit the component in the repo (see [Contributing](contributing.md)).
