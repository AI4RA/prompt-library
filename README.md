# AI4RA Prompt Library

Versioned storage and evaluation data for prompts, skills, agents, and related components used across AI4RA applications.

## Install as a Claude Code plugin marketplace

```
/plugin marketplace add AI4RA/prompt-library
/plugin install <component>@prompt-library
```

Installed plugins auto-update via `/plugin update`. Each component in this repo is published as a plugin exposing one Claude Code skill. See [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json) for the full list.

## Source of truth

`components/<name>/prompt.md` (frontmatter + body) and `components/<name>/schema.json` are the **canonical**, LLM-agnostic artifacts for each component. Everything else a platform needs — SKILL.md for Claude Code, plugin.json, marketplace.json, future Gemini/OpenAI wrappers — is **generated** from those two files.

**Canonical (hand-authored):**

- `components/<name>/prompt.md` — frontmatter + prompt body
- `components/<name>/schema.json` — output contract
- `components/<name>/README.md`, `CHANGELOG.md`, `evals/`

**Generated (committed but never hand-edited):**

- [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json) at repo root
- `components/<name>/.claude-plugin/plugin.json`
- `components/<name>/skills/<name>/SKILL.md`

If you edit a generated file directly, CI will fail on the next PR. Always edit the canonical source and rerun the generator.

## Layout

Each component is a directory under `components/` named by a short slug. A component represents a single *task* (e.g., "extract a submission checklist from an RFP"). The canonical prompt + schema carry metadata in YAML frontmatter; derived wrappers are regenerated from them.

Every component carries its own:

- `README.md` — what it does, current version, input/output contract
- `CHANGELOG.md` — per-component version history (semver)
- `evals/` — test cases and known-good outputs

## Versioning

Each component is versioned independently using semver, declared in the `version:` field of `prompt.md` frontmatter. The generator propagates that version into every derived wrapper, so `prompt.md` is the only place you bump it.

- **MAJOR** — output contract changes (breaks downstream consumers)
- **MINOR** — new capability, backward compatible
- **PATCH** — wording or clarity fixes, no behavior change expected

The repository itself is not versioned by tag. Consumers pin to a commit SHA plus a component slug and declared version.

## Adding a component

1. Copy `templates/new-component/` into `components/<slug>/`
2. Fill in `prompt.md` frontmatter (including `description:`), `prompt.md` body, `schema.json`, `README.md`, and the `CHANGELOG.md` 1.0.0 entry
3. Add at least one eval case under `evals/cases/` — every case's `metadata.yaml` must declare `validated_against_version` (see the evaluation status section below)
4. Register any new tags or categories in `taxonomy.md`
5. Run `python .github/scripts/generate_wrappers.py` to produce the derived wrappers
6. Commit canonical files **and** the regenerated wrappers together

## Editing an existing component

1. Edit `prompt.md`, `schema.json`, `README.md`, `CHANGELOG.md`, and/or `evals/` as needed
2. Bump the `version:` field in `prompt.md` frontmatter
3. Run `python .github/scripts/generate_wrappers.py`
4. Commit everything together

## Evaluation status

Each eval case's `metadata.yaml` carries `validated_against_version`: the component version at which that case's `expected.*` was last human-validated. The component's **last fully evaluated version** is computed as the minimum `validated_against_version` across its cases. The linter warns (non-blocking) when a component's current version has moved ahead.

When you re-run evals after a version bump and the expected output is still correct, update `validated_against_version` in the relevant case(s) to match the new component version. When the expected output changes, update the output file and `validated_against_version` in the same commit.

## CI

Two workflows run on every PR and push to `main`:

- [`.github/workflows/lint.yml`](.github/workflows/lint.yml) — runs [`.github/scripts/lint_components.py`](.github/scripts/lint_components.py): validates frontmatter, semver, taxonomy membership, version lockstep across manifestations, and eval-case metadata.
- [`.github/workflows/generate-wrappers.yml`](.github/workflows/generate-wrappers.yml) — runs [`.github/scripts/generate_wrappers.py`](.github/scripts/generate_wrappers.py) and fails on `git diff --exit-code` if any generated wrapper is stale relative to its canonical source.

To run both locally:

```
pip install pyyaml
python .github/scripts/lint_components.py
python .github/scripts/generate_wrappers.py
git diff --exit-code
```

## Shared vocabulary

See [`taxonomy.md`](taxonomy.md) for the canonical set of tags, categories, domains, and manifestation types. Prefer existing vocabulary; propose additions in the same PR that introduces a component needing them.
