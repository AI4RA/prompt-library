---
name: viva-engage-reformat
version: "0.2.0"
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
> **Expected output:** One fixed-format "Proposal Submission" entry per input row. Prime Sponsor and Budget Total are always left blank for the PreAward SPA to complete.
> **Contract scope:** repo-local. Plain-text output; no structured-output schema.

---

## Prompt

For each row in the input, produce one entry in exactly this format, with a blank line between entries:

Proposal Submission
Proposal Number:
Proposal Title:
Sponsor:
Prime Sponsor:
Principal Investigator:
Budget Total: $

Rules:

1. Fill in Proposal Number, Proposal Title, and Sponsor exactly as they appear in the row — do not paraphrase, abbreviate, or correct them.
2. Leave "Prime Sponsor:" blank. Output nothing after the colon, even when the input row has a prime sponsor value. The PreAward SPA completes this field if applicable.
3. Leave "Budget Total: $" blank. Output nothing after the "$", even when the input row has a budget amount. The PreAward SPA completes this field if applicable.
4. The input lists the Principal Investigator as "last name, first name middle". Reorder it to first name, then middle initial or middle name (when present), then last name.
   - Input "Smith, Jane A" → output "Principal Investigator: Jane A. Smith"
   - Input "Garcia, Luis" (no middle) → output "Principal Investigator: Luis Garcia"
5. Produce one entry per input row — never drop, merge, or invent rows. Skip header rows.
6. Output only the entries. No introduction, commentary, or closing remarks.
