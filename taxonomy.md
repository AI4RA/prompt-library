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

- `experimental` — under active development, output contract may change
- `stable` — validated against evals, safe for production use
- `deprecated` — superseded; consult `README.md` for the replacement
