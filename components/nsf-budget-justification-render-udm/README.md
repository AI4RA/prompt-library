# NSF Budget Justification Render — UDM

Renders a reviewed eight-section NSF budget-justification array into Word-pasteable Markdown and HTML strings. The component is the formatting tail of a multi-step budget-justification pipeline: it does not draft, review, or reinterpret content — it transforms the structured array into two presentation forms that paste cleanly into a Microsoft Word document.

**Current version:** 1.0.0
**Category:** transformation
**Domain:** research-administration
**Status:** experimental
**Manifestations:** prompt
**Output contract:** [`schema.json`](schema.json)
**Contract scope:** repo-local NSF-specific rendering contract

## Inputs

A reviewed eight-section JSON array matching `#/$defs/output` of [`../nsf-budget-justification-udm/schema.json`](../nsf-budget-justification-udm/schema.json). Each element has `key`, `title`, and `content`; `content` is narrative markdown that may include `###` sub-subheadings (typically under Section G) and lists.

## Outputs

A single JSON object with two parallel string fields:

- `markdown` — section headings as `# Section A: Senior Personnel` (level-1 ATX) followed by the section's `content` verbatim. Pastes into Word as plain text with markdown symbols visible; the user can apply Word heading styles after the paste.
- `html` — section headings as `<h1>`, sub-subheadings as `<h2>`, paragraphs as `<p>`, lists as `<ul>`/`<ol>`. Pastes into Word via *Paste Special → HTML*, preserving the heading and paragraph hierarchy automatically.

Both fields cover sections A..H exactly once, in order, and carry the same prose. They differ only in syntax. See [`schema.json`](schema.json) for the validation contract.

## Contract Scope

Repo-local. The component owns its own output schema (`schema.json`) because the rendering surface is distinct from any other contract in this repo. Input validation delegates to the existing eight-section array contract owned by `nsf-budget-justification-udm`.

## Triad Integration

- **Evaluation datasets:** none yet; initial coverage is repo-local only.
- **Harness notes:** invoke after the review step that produced a polished eight-section array. Validate input against `components/nsf-budget-justification-udm/schema.json` at `#/$defs/output`; validate output against this component's `schema.json`. The component is deterministic in intent (no fabrication, no paraphrase) — golden-case evals should compare outputs strictly against expected renderings.
- **Shared UDM relationship:** the rendering surface is sponsor-specific (NSF section labels) and prompt-library-local; it is not part of the shared AI4RA-UDM contract.

## Manifestations

- [`prompt.md`](prompt.md) — canonical prompt
- [`schema.json`](schema.json) — output schema

## Evals

See [`evals/`](evals/). No golden cases are checked in yet. Future cases should pair a representative eight-section array with the expected `{ "markdown": "...", "html": "..." }` rendering, exercising distinct structural features: a Section G with multiple sub-subheadings, a zero-Section-D narrative ("No equipment is requested."), a Section F with a markdown table or bulleted list of participant-support line items, and a Section H with a step-change rate note.

## Provenance

Created 2026-04-24 as the fourth and final step of the `nsf-budget-justification-multistep` workflow. Added because the array form is the right intermediate contract for evals and downstream tooling, but proposal authors need a Word-pasteable artifact at the end of the pipeline.
