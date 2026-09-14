# Evals — narrative-to-budget-worksheet

Each case lives under `cases/<case-slug>/` with at minimum:

- `metadata.yaml` — case identity plus **`validated_against_version`** (required)
- `input.md` — the narrative and/or announcement supplied, and the scripted replies to the Step 2 questions, one per turn (an empty reply means skip)
- `input-source.md` — where the documents came from
- `expected.md` — the known-good worksheet described block by block: inputs with origins, which cells are yellow, the formulas in the summary block, and the checks

Run artifacts go under `runs/` (gitignored).

## Case selection

- Narrative only, no rates: every rate is an estimate and yellow.
- Announcement only: template team proposed and labelled; ceiling and caps become checks.
- Narrative plus a full rates block: no yellow cells in the inputs block except PI decisions left to estimates.
- A subaward above $25,000 across years: MTDC excludes the excess correctly.
- NSF senior personnel asking for three summer months: the two-month check reads "Over".

No cases yet.
