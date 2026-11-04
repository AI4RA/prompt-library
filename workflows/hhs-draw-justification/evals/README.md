# Evals — hhs-draw-justification (workflow-local)

This workflow carries its own cases because its behavior comes from
the step interactions, not from the `hhs-payment-justification`
component alone: `extract-draw-lines` copies the sheet's cells and
resolves cost type, role, timeframe, and the PI's prior wording; the
consolidation rebuilds the sheet's rows from it.

Each case lives under `cases/<case-slug>/`:

- `metadata.yaml` — case identity plus `validated_against_version`
  (the **workflow** version)
- `input-source.md` — where the de-identified billing sheet and award
  documents come from
- `expected.csv` — the filled sheet, validated by the PI or OSP
- `notes.md` — optional review notes

Run artifacts go under `runs/` (gitignored).

## What cases need to exercise

- **Column fidelity**: one object per sheet row, the sheet's headers
  in order, every copied cell unchanged, raw JSON so the CSV download
  splits columns.
- **Payroll timeframe**: the pay-date → pay-period lookup, and a pay
  date outside the table ("for the pay period paid on ...").
- **Service month**: an internal recharge naming its month (e.g. an
  animal facility per diem) uses that month, not the posting date.
- **Roles and names**: generic default roles, `prior_wording`
  carry-forward from an earlier completed sheet, and a person's name in
  Description that stays in the copied cell but never reaches a
  justification.
- **General wording**: no research topic, journal, or purchase
  purpose appears unless it is in the sheet or the PI's prior wording;
  with a prior sheet uploaded, payroll sentences match the PI's,
  dates updated.
- **Total rows**: copied in place with an empty justification.

The CB7897 billing sheets used in development carry staff and grant
financial detail and are not committed. A real case needs a
de-identified sheet.
