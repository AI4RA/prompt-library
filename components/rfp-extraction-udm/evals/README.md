# Evals — rfp-extraction-udm

## Structure

Each case lives under `cases/<case-slug>/` with:

- `metadata.yaml` — solicitation identifier, source URL, notes on which edge cases this case exercises
- `input-source.md` — where to obtain the source announcement (URL, document version, date retrieved)
- `expected.json` — the known-good extraction output, validated by a human reviewer and conforming to `../schema.json`
- `notes.md` — optional; qualitative observations from review

Run outputs go under `runs/` (gitignored).

## Validating `expected.json`

Every `expected.json` must validate against the component's `schema.json`. Quick check with any JSON Schema validator; here using `check-jsonschema` (pipx install check-jsonschema):

```
check-jsonschema --schemafile components/rfp-extraction-udm/schema.json \
  components/rfp-extraction-udm/evals/cases/*/expected.json
```

## Case selection

Prefer cases that exercise distinct schema features alongside distinct structural features of the announcement itself:

- Multi-round scheduling (requires `special_conditions` entries per round)
- LOI required vs. optional vs. prohibited
- Cost sharing encoded via `structured_rule_type: cost_sharing`
- Per-institution and per-PI proposal limits via `structured_rule_type: proposal_limit_per_*`
- Parent-guide deviations (populates `pappg_deviations`)
- Non-standard required or prohibited supplements

## Parity with `rfp-extraction`

Cases should mirror the same solicitation ID used in `components/rfp-extraction/evals/cases/`. This keeps the two components' golden outputs anchored to the same source truth — a change in the source should surface in both eval directories.

## Current cases

- `NSF_26-508/` — TechAccess: AI-Ready America. 3 rounds, LOI required, one proposal per institution, cost sharing prohibited, five mandated project-description section headers, five solicitation-specific review criteria, four parent-guide deviations.
