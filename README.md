# AI4RA Prompt Library

Versioned storage and evaluation data for prompts, skills, agents, and related components used across AI4RA applications.

## Layout

Each component is a directory under `components/` named by a short slug. A component represents a single *task* (e.g., "extract a submission checklist from an RFP") and may have multiple platform-specific *manifestations*:

- `prompt.md` — the canonical, LLM-agnostic prompt
- `skill/SKILL.md` — Claude Skill form (frontmatter for the Claude Code / Agent SDK skill loader)
- `agent/AGENT.md` — subagent / agent definition (if applicable)
- additional formats as platforms emerge

Every component carries its own:

- `README.md` — what it does, current version, which manifestations exist
- `CHANGELOG.md` — per-component version history (semver)
- `evals/` — test cases and known-good outputs

## Versioning

Each component is versioned independently using semver, declared in the `version:` field of the frontmatter on every manifestation file. When a change lands, bump the version in *every* manifestation of that component and add a `CHANGELOG.md` entry.

- **MAJOR** — output contract changes (breaks downstream consumers)
- **MINOR** — new capability, backward compatible
- **PATCH** — wording or clarity fixes, no behavior change expected

The repository itself is not versioned by tag. Consumers pin to a commit SHA plus a component slug and declared version.

## Adding a component

1. Copy `templates/new-component/` into `components/<slug>/`
2. Fill in `README.md`, at least one manifestation file, and the `CHANGELOG.md` 1.0.0 entry
3. Add at least one eval case under `evals/cases/` — every case's `metadata.yaml` must declare `validated_against_version` (see the evaluation status section below)
4. Register any new tags or categories in `taxonomy.md`

## Evaluation status

Each eval case's `metadata.yaml` carries `validated_against_version`: the component version at which that case's `expected.*` was last human-validated. The component's **last fully evaluated version** is computed as the minimum `validated_against_version` across its cases. The linter warns (non-blocking) when a component's current version has moved ahead.

When you re-run evals after a version bump and the expected output is still correct, update `validated_against_version` in the relevant case(s) to match the new component version. When the expected output changes, update the output file and `validated_against_version` in the same commit.

## CI

A GitHub Actions workflow ([`.github/workflows/lint.yml`](.github/workflows/lint.yml)) runs [`.github/scripts/lint_components.py`](.github/scripts/lint_components.py) on every PR and push to `main`. It checks that each component has `README.md` + `CHANGELOG.md`, that every manifestation has valid YAML frontmatter with the required fields, that `version` is semver, that `category` / `domain` / `status` values exist in `taxonomy.md`, and that all manifestations under one component share the same `version` (lockstep).

To run it locally: `pip install pyyaml && python .github/scripts/lint_components.py`.

## Shared vocabulary

See [`taxonomy.md`](taxonomy.md) for the canonical set of tags, categories, domains, and manifestation types. Prefer existing vocabulary; propose additions in the same PR that introduces a component needing them.

## License and citation

This repository is licensed under the [GNU General Public License v3.0](LICENSE).

**Any use of this work requires citation.** This includes research publications, derivative components, downstream software, internal tooling, and production deployments. The citation requirement is a condition of use alongside — not in place of — the GPL's obligations.

Machine-readable citation metadata lives in [`CITATION.cff`](CITATION.cff); GitHub renders a "Cite this repository" button in the sidebar that exports BibTeX and APA on demand. A DOI will be added once a Zenodo release is minted.

When citing a specific state of the repository, pin to the commit SHA and the component version you used:

> Robison, B. (2026). *AI4RA Prompt Library* (commit `<sha>`, component `<slug>` v`<version>`). https://github.com/AI4RA/prompt-library
