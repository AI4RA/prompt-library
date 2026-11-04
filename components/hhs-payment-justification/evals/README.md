# Evals — hhs-payment-justification

Experimental; **no validated golden cases yet**.

The first case should be the CB7897 (sponsor award REY012146F) OSP
billing sheet for the 10/23/2026 draw, which the PI completed by hand.
Ten lines: three salary, two fringe, five F&A; total $8,470.30. Check:

- one output object per sheet row, in row order, keyed by the sheet's
  15 headers (PMSCode … Amount, then "ACTIVITY 10/10-23/2026 PER
  PI/DGA"), with every copied cell unchanged (total $8,470.30);
- raw JSON only, so Vandalizer's CSV download opens as the sheet;
- payroll lines say 9/27/2026 to 10/10/2026 (the pay period), not the
  10/23 pay date or the "10/10-23/2026" column header;
- roles, never names; no account codes in the text;
- general wording only ("the research activities supported by this
  award"), no research topic, journal, purchase purpose, or
  approved-budget claim;
- with the PI's earlier completed sheet uploaded, payroll sentences
  match the PI's, with the dates updated.

The billing sheet and the PI's correspondence are not committed (they
carry staff names and grant financials). Add a case under
`cases/<case-slug>/` only with de-identified inputs, after a human
reviewer validates the expected output and records
`validated_against_version`.
