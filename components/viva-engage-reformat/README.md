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

For each input row, one compact entry (blank line between entries):

```
Proposal Submission
Proposal Number: <verbatim from row>
Proposal Title: <verbatim from row>
Sponsor: <verbatim from row>
Prime Sponsor:
Principal Investigator: <reordered: first name, middle initial/name, last name>
Budget Total: $
```

Prime Sponsor and Budget Total are **always left blank** — the
PreAward SPA completes them if applicable. The PI name arrives in the
input as "last name, first name middle" and is reordered on output.

## Provenance

Captured 2026-08-18 from the University of Idaho RA team's live
Vandalizer saved prompt "Viva Engage" (used by the workflow of the
same name); recorded verbatim as v0.1.0. v0.2.0 folds in pre-award
reviewer feedback from Tami Clabough (blank Prime Sponsor / Budget
Total, PI name reordering, compact format), replacing the "Formatter"
post-processing prompt she had been using to fix the output after the
fact.

## Used by

- `workflows/viva-engage` (single-step Vandalizer workflow)
