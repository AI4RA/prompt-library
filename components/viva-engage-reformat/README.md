# viva-engage-reformat

Reformats a table of proposal-submission information (one proposal per
row) into fixed-format "Proposal Submission" announcement blocks
suitable for pasting into Microsoft Teams / Viva Engage.

- **Category**: transformation
- **Domain**: research-administration
- **Status**: experimental
- **Contract scope**: repo-local. The output is plain announcement
  text, not JSON; there is no `schema.json` and no UDM binding.

## Input

Tabular proposal data supplied as step input — typically rows copied
from an Excel export of recent proposal submissions carrying, per
proposal: proposal number, proposal title, sponsor, prime sponsor,
principal investigator, and budget total.

## Output

For each input row, one block:

```
Proposal Submission

Proposal Number:

Proposal Title:

Sponsor:

Prime Sponsor:

Principal Investigator:

Budget Total: $
```

with each field populated from the corresponding row.

## Provenance

Captured 2026-08-18 from the University of Idaho RA team's live
Vandalizer saved prompt "Viva Engage" (used by the workflow of the
same name). The prompt body is recorded verbatim as v0.1.0; hardening
(empty-cell handling, header-row detection, verbatim-value anchors)
can follow once a baseline test run is logged.

## Used by

- `workflows/viva-engage` (single-step Vandalizer workflow)
