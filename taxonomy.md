# Taxonomy

Shared vocabulary for the `tags`, `category`, `domain`, and `manifestations` fields on components. Keep this file authoritative — PRs that introduce new components may propose additions here in the same change.

## Categories

High-level grouping of what the component *does*.

- `extraction` — pulls structured information from unstructured input
- `drafting` — produces new content (proposals, reports, summaries, correspondence)
- `review` — evaluates or critiques existing content
- `transformation` — converts between formats or representations
- `classification` — assigns labels or categories
- `research` — surveys literature, standards, or existing knowledge
- `planning` — produces plans, outlines, or roadmaps

## Domains

The subject-matter area the component operates in.

- `research-administration` — grants, RFPs, proposal development, compliance
- `scientific-writing` — manuscripts, abstracts, figure captions
- `education` — curriculum, instruction, assessment
- `code` — software engineering tasks
- `general` — no specific domain

## Manifestations

Supported platform-specific forms of a component.

- `prompt` — LLM-agnostic raw prompt, stored as `prompt.md`
- `skill` — Claude Skill, stored as `skill/SKILL.md`
- `agent` — subagent or agent definition, stored as `agent/AGENT.md`
- `system-prompt` — system-prompt-style variant, stored as `system.md`

## Status

Lifecycle stage of a component.

- `experimental` — under active development; output contract may change
- `stable` — intended for downstream use and backed by validated reference coverage, but consumers should still pin versions and check the component's last fully evaluated version
- `deprecated` — superseded; consult `README.md` for the replacement

## Draft kinds

File kinds allowed in a draft collection's `drafts.json`. See [`drafts/README.md`](drafts/README.md).

- `vandalizer-skill` — Vandalizer chat Skill import file: `export_type: search_set` with one `set_type: prompt` item whose instructions are in `extraction_config.content`
- `vandalizer-workflow` — Vandalizer workflow import file (`export_type: workflow`) stored as generated, not built from a `manifest.yaml`

## Draft groups

How a draft relates to what already exists in Vandalizer's catalog.

- `new` — covers a task the catalog does not
- `companion` — used beside an existing catalog item
- `variant` — a modified copy of an existing catalog item, for side-by-side comparison
