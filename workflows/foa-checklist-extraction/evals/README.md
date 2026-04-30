# Evals — foa-checklist-extraction (workflow-local)

This workflow carries its own cases under `cases/` because the Consolidation Prompt assembles six upstream fragments and enforces cross-field consistency (chronological `critical_dates`, `expected_awards * max(award_range) <= total_funding`, `federal_agency` enum normalization) — emergent behavior the component-level evals cannot cover on their own.

## What workflow-local cases need to exercise

- **Six-fragment assembly** — every field from each upstream extraction lands in the right top-level position.
- **`federal_agency` enum normalization** — document phrasings ("National Institutes of Health", "Health and Human Services") map to the closest enum.
- **Date-consistency check** — CHK-02 fires if `critical_dates` entries are not chronologically ordered or LOI/pre-app comes after full-app.
- **Funding-arithmetic check** — CHK-03 fires if `expected_awards * max(award_range)` exceeds `total_funding`.
- **Multi-stage review** — `review_stages` with LOI → full → panel → council sequence preserved in order.

## Status

The initial scaffolded case (`nih-multi-stage-review-stub`) is a placeholder pending sponsored-programs review against an authorized, de-identified NIH PA/PAR FOA with multi-stage review.
