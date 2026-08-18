---
name: viva-engage-reformat
version: "0.1.0"
category: transformation
domain: research-administration
status: experimental
tags:
  - proposal-submissions
  - reformatting
  - teams
  - viva-engage
  - announcement
audience:
  - research-administrators
  - sponsored-programs-offices
owner: ui-insight
created: 2026-08-18
updated: 2026-08-18
---

# Viva Engage Reformat — Prompt

> **Purpose:** Reformat a table of proposal-submission information (one proposal per row) into per-proposal announcement blocks suitable for pasting into Microsoft Teams / Viva Engage.
> **Expected input:** Tabular proposal data passed as step input — e.g. rows from an Excel export with proposal number, title, sponsor, prime sponsor, principal investigator, and budget total.
> **Expected output:** One fixed-format "Proposal Submission" text block per input row.
> **Contract scope:** repo-local. Plain-text output; no structured-output schema.

---

## Prompt

for each row in the input, produce an output in this format:
Proposal Submission

Proposal Number:

Proposal Title:

Sponsor:

Prime Sponsor:

Principal Investigator:

Budget Total: $
