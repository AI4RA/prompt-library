# Solicitation Document Modifications — UDM

Given a solicitation text and a sponsor's default document requirements, emit only the **diff**: modifications to the defaults and net-new documents the solicitation introduces. Each entry links back to the default it overrides (when applicable) via `modifies_default` and carries a verbatim `source_excerpt` from the solicitation.

**Current version:** 1.0.0
**Category:** extraction
**Domain:** research-administration
**Status:** experimental
**Manifestations:** prompt, skill
**Output contract:** see [`schema.json`](schema.json)

## Inputs

1. **Solicitation text** — markdown, typically OCR-derived from a PDF solicitation.
2. **Sponsor defaults** — a JSON object matching the output shape of [`sponsor-doc-defaults-udm`](../sponsor-doc-defaults-udm/). The `document_requirements` array is the baseline the component diffs against.

The component answers the **solicitation-specific** question: "What does this program change or add, on top of what the sponsor already requires?" The baseline "what does the sponsor require" question is the job of the sibling component `sponsor-doc-defaults-udm`.

## Outputs

One JSON object with:

- `sponsor_name` — echoed from the sponsor-defaults input
- `sponsor_division` — echoed from the sponsor-defaults input
- `solicitation_id` — the solicitation's printed identifier (e.g., `"NSF 24-507"`), or null when not discoverable
- `solicitation_notes` — free-text caveats (version analyzed, sections that could not be resolved)
- `document_requirements` — array of requirement entries; empty when the solicitation makes no changes

Each requirement entry carries the full sponsor-doc-defaults field set (`code`, `label`, `description`, `page_limit`, `format_spec`, `is_required`, `is_per_person`, `conditional_on`) plus:

- `modifies_default` — the default `code` this entry overrides, or null for net-new
- `source_excerpt` — verbatim text from the solicitation grounding the entry

See [`schema.json`](schema.json) for the authoritative definition.

## Controlled `code` vocabulary

`cover_sheet`, `cover_letter`, `project_summary`, `project_narrative`, `proposal_narrative`, `specific_aims`, `references_cited`, `biosketch`, `current_pending`, `collaborators_and_affiliations`, `facilities`, `equipment`, `budget`, `budget_justification`, `data_mgmt`, `postdoc_mentoring`, `mentoring_plan`, `results_prior_support`, `resource_sharing`, `authentication_key_resources`, `leadership_plan`, `human_subjects`, `vertebrate_animals`, `select_agent`, `inclusion_enrollment_report`, `letter_support`, `letter_collaboration`, `letter_of_intent`, `other`.

Same enum as `sponsor-doc-defaults-udm`. Adding a new code is a MINOR change; removing or renaming one is MAJOR. The two components' enums must stay in lockstep.

## Merge semantics

A downstream merge of `sponsor-doc-defaults-udm` output with this component's output should:

1. Start from the defaults `document_requirements` array.
2. For each entry in this component's `document_requirements`:
   - If `modifies_default` is set, replace the default with matching `code` wholesale.
   - If `modifies_default` is null, append the entry.
3. Defaults whose `code` does not appear in any `modifies_default` pass through unchanged — silence means "use the default."

## Why only emit the diff?

Emitting only modifications and net-new keeps the solicitation pass focused, makes the `source_excerpt` requirement enforceable (no grounding, no entry), and keeps the merged result auditable: every deviation from the sponsor default is traceable to a quoted passage in the solicitation.

## Manifestations

- [`prompt.md`](prompt.md) — canonical, LLM-agnostic prompt
- [`skill/SKILL.md`](skill/SKILL.md) — Claude Skill form

## Schema

[`schema.json`](schema.json) is a JSON Schema (draft 2020-12) defining the full output contract.

## Relationship to other components

| Component | Role |
| --- | --- |
| `sponsor-doc-defaults-udm` | Upstream: emits the sponsor's baseline document requirements |
| `solicitation-doc-modifications-udm` (this) | Pairs with defaults: emits only the solicitation's diff |
| `document-type-classifier-udm` | Shares the `code` vocabulary; classifies incoming documents against it |
| `proposal-completeness-review-udm` | Consumes the merged defaults + modifications to check a draft proposal |

## Evals

See [`evals/`](evals/) for reference inputs and known-good outputs. The initial set covers three shapes:

- a solicitation that only modifies defaults,
- a solicitation that only adds net-new documents,
- a solicitation that does both.

## Provenance

Designed 2026-04-19 in response to issue [#3](https://github.com/AI4RA/prompt-library/issues/3). The diff-only output shape was chosen over "emit the full merged checklist" so that every deviation from the sponsor default is grounded in a verbatim solicitation excerpt and so the sponsor and solicitation passes can be evolved independently.
