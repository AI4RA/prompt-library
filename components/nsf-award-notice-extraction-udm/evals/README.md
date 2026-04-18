# Evals \u2014 nsf-award-notice-extraction-udm

## Structure

Each case lives under `cases/<faIN-or-slug>/` with:

- `metadata.yaml` \u2014 award identifier, source notes, and (required) `validated_against_version`
- `input-source.md` \u2014 where to find the source notice PDF
- `expected.json` \u2014 the known-good extraction output, validated by a human reviewer and conforming to `../schema.json`
- `notes.md` \u2014 optional observations from validation

Run artifacts go under `runs/` (gitignored).

## Validating `expected.json`

```
check-jsonschema --schemafile components/nsf-award-notice-extraction-udm/schema.json \
  components/nsf-award-notice-extraction-udm/evals/cases/*/expected.json
```

## Case selection

Prefer cases that each exercise distinct structural features:

- Initial obligation (Amendment 000) vs. subsequent amendments
- Standard Grant vs. Continuing Grant vs. Cooperative Agreement
- Single prime vs. Collaborative Research
- Subawards: explicitly enumerated vs. inferred from Co-PI organizations
- Cost share required / proposed / prohibited
- Unusual indirect cost arrangements (tiered rates, non-MTDC base)
- Heavy special-conditions narrative vs. minimal narrative
- NSF-format budget variations (personnel-heavy, equipment-heavy, participant-support-heavy)

## Current cases

- `2427549/` \u2014 Standard Grant, Amendment 000, single prime (University of Idaho) with an inferred subaward to a Co-PI at Southern Utah University. Exercises the subaward inference rule, full NSF-format budget table with participant support costs, 38% MTDC indirect rate, and the NSF boilerplate special conditions for participant support segregation and subaward authorization.
