# Evals — nsf-budget-justification-render-udm

Each case lives under `cases/<case-slug>/` with at minimum:

- `metadata.yaml` — case identity plus `validated_against_version`
- `input.json` — the eight-section array under render (validating against `#/$defs/output` of `../../nsf-budget-justification-udm/schema.json`)
- `expected.json` — the known-good `{ "markdown": "...", "html": "..." }` object, validating against `../../schema.json`
- `notes.md` — optional; qualitative observations

Run artifacts go under `runs/` (gitignored).

The component is a deterministic renderer, so evals should compare expected and actual outputs strictly. Prefer cases that exercise distinct structural features rather than re-stating the same content shape:

- a Section G with multiple `###` sub-subheadings (Materials and Supplies, Publication Costs, Subawards, Other) → `<h2>` mapping in HTML
- a zero-Section-D narrative ("No equipment is requested.") → single-paragraph rendering
- a Section F with a markdown bulleted list of participant-support line items → `<ul>`/`<li>` mapping in HTML
- a Section H with a rate step-change note → faithful preservation of the note in both renderings
- a Section E with a markdown table summarizing trips → `<table>` mapping in HTML
