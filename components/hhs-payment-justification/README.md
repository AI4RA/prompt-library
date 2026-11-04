# hhs-payment-justification

Writes the payment justifications HHS requires with every Payment
Management System (PMS) drawdown on a discretionary award: one
plain-language, PII-free sentence per expense line, returned as the
OSP billing sheet's rows with the justification column filled in.

- **Category**: drafting
- **Domain**: research-administration
- **Status**: experimental
- **Contract scope**: repo-local. JSON row array mirroring the OSP
  sheet; no `schema.json` and no UDM binding.

## Input

Two JSON fragments, produced by the extraction step of
`workflows/hhs-draw-justification`:

1. **Draw lines**: the sheet's column headers plus each row's cells
   verbatim, with its cost type, personnel role, and timeframe already
   resolved.
2. **Award purpose**: the award title, aims, and a plain-language
   research topic taken from the Notice of Award or aims page (may be
   empty).

## Output

A raw JSON array, one flat object per sheet row, keyed by the sheet's
own column headers in order (PMSCode … Amount), with the
justification column header as the last key holding the drafted
sentence. Vandalizer's run download with **CSV** format parses a JSON
string output and writes a list of objects as real columns, so the
download is the completed sheet. The reply must be raw JSON (no code
fence or commentary) for that to work.

## Requirements encoded

The HHS ASFR payment justification guidance as quoted to University of
Idaho PIs by the Vice President for Research on 2026-10-19: identify
the cost, explain how it supports the award, give the timeframe, use
plain language, exclude PII, summarize each cost type per subaccount,
and fit the PMS character limit. HHS's sufficient F&A example is used
verbatim for indirect lines. The per-subaccount summary rule is not
rendered separately: OSP collects justifications per line.

## Used by

- `workflows/hhs-draw-justification` (consolidation / output task)
