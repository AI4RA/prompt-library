# Evals — solicitation-doc-modifications-udm

## Structure

Each case lives under `cases/<case-slug>/` with:

- `metadata.yaml` — case identity, features exercised, and (required) `validated_against_version`
- `input.md` — the input sent to the component (solicitation text + the sponsor-defaults JSON prior)
- `input-source.md` — provenance of the solicitation text (real source, synthetic, or excerpted; any modifications made for the eval)
- `expected.json` — the known-good output, validated by a human reviewer and conforming to `../schema.json`
- `notes.md` — optional observations from validation

Run artifacts go under `runs/` (gitignored).

## Input convention

`input.md` contains two fenced blocks, in order:

1. A ` ```markdown ... ``` ` block containing the solicitation text.
2. A ` ```json ... ``` ` block containing the sponsor-defaults object (as emitted by `sponsor-doc-defaults-udm`).

Runners are expected to pass both blocks through to the model in the same order.

## Validating `expected.json`

```
check-jsonschema --schemafile components/solicitation-doc-modifications-udm/schema.json \
  components/solicitation-doc-modifications-udm/evals/cases/*/expected.json
```

## Case selection

Prefer cases that each exercise distinct behaviors of the component:

- **Modify-only** — a solicitation that tightens or changes one or more defaults but introduces no net-new documents. Exercises `modifies_default` targeting; exercises full-object emission (carrying unchanged fields over from the default).
- **Net-new-only** — a solicitation that adds program-specific documents with no changes to defaults. Exercises `modifies_default: null`; exercises falling back to `other` when no enumerated code fits.
- **Mixed** — a solicitation that does both. Exercises ordering (modifications first, net-new last) and disambiguation between "tighter default" and "separate new document."
- **Verbatim grounding** — every entry must quote the solicitation in `source_excerpt`. Over time add a case where the solicitation is noisy OCR to exercise excerpt selection under poor text quality.
- **Empty diff** — a reissuance that changes nothing. Output is a valid object with `document_requirements: []`. (Not yet represented in the initial set.)

## Current cases

- `nsf-dcl-narrative-tightened/` — modify-only. A synthetic NSF Dear Colleague Letter supplement shortening `proposal_narrative` from 15 to 10 pages and expanding `data_mgmt` from 2 to 3 pages with a new required subheading. Exercises `modifies_default` targeting, page_limit deltas, and format_spec additions.
- `nsf-erc-net-new-plans/` — net-new-only. A synthetic NSF Engineering Research Center solicitation introducing a Strategic Plan and a Knowledge Transfer Plan. Exercises `modifies_default: null` and the `other`-code fallback with a distinctive `label`.
- `nih-rfa-mixed/` — mixed. A synthetic NIH RFA that shortens the Research Strategy to 6 pages (aligning with an R21-length narrative under an R01 mechanism frame) AND adds a Milestones and Timeline supplement. Exercises ordering (modification first, net-new second) and the full-object-on-modification rule.

## Synthetic solicitations

The three initial cases use synthetic solicitation text designed to be clearly distinguishable from real solicitations (synthetic identifiers, generic program titles). This is intentional: the component is being evaluated on its ability to apply the extraction rules correctly, not on its knowledge of specific real programs. Real-solicitation cases can be added in follow-ups once the extraction rules have stabilized.
