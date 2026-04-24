# Evals — nsf-budget-justification-review-udm

Each case lives under `cases/<case-slug>/` with at minimum:

- `metadata.yaml` — case identity plus `validated_against_version`
- `input-draft.json` — the drafted eight-section array under review
- `input-budget.json` — optional; the structured budget that produced the draft
- `expected.json` — the known-good revised array, validating against `#/$defs/output` of `../../nsf-budget-justification-udm/schema.json`
- `notes.md` — optional; qualitative observations

Run artifacts go under `runs/` (gitignored).

Prefer cases that exercise distinct review checks: misplaced tuition, missing participant-support disclosure, fabricated figure, inconsistent personnel naming across sections, zero-section invention, section order errors.
