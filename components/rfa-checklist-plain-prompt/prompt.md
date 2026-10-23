---
name: rfa-checklist-plain-prompt
version: 1.0.0
category: extraction
domain: research-administration
status: experimental
tags: [rfa, foa, nofo, grants, pre-award, checklist, plain-prompt, baseline, markdown]
audience: [sponsored-programs-staff, pre-award-teams]
owner: ui-insight
created: 2026-10-23
updated: 2026-10-23
---

# RFA Checklist — Plain RA Prompt

> **Purpose:** A single prompt of the kind a research administrator might write, used to ask a general-purpose AI tool for an RFA checklist. It is the plain-prompt comparison condition for the governed [`rfa-checklist-extraction`](../../workflows/rfa-checklist-extraction/) workflow v3.1.0.
> **Expected input:** The funding announcement (RFA / FOA / NOFO / program solicitation), attached to the conversation as the user would supply it.
> **Expected output:** A free-form checklist in whatever format the tool chooses, organized under the 11 sections named in the prompt. No schema.

## Relationship to other components

This prompt keeps the 11 checklist sections of the `rfa-checklist-extraction` workflow v3.1.0 (Red Flags, Dates & Deadlines, Eligibility, Award Information, Budget Requirements & Policies, Submission Details, Application Components, Compliance Risks, Foreign Influence & International Components, Special Requirements, Important Notes). It deliberately leaves out the workflow's machinery: the ten parallel extraction prompts, JSON fragments and field schemas, sponsor-standard component merging, the consolidation rendering rules, and institution-specific routing. Keep it that way. Adding structure would remove the difference this condition exists to measure.

---

## Prompt

I work in a sponsored programs office. I've attached a funding announcement (RFA). Please read the whole document and make a checklist I can share with the PI and the proposal team, so we know what's required before we start writing.

Organize the checklist into these sections:

1. **Red flags**: anything that means extra work, a long lead time, or that our office needs to look at early. For example: cost sharing or matching, limits on indirect costs, a limit on how many proposals our institution can submit, letters or signatures from institutional officials, and unusual terms (intellectual property, publication restrictions, indemnification, foreign involvement, or classified or controlled information).
2. **Dates and deadlines**: every deadline and key date, such as letters of intent, preliminary proposals, full proposals, and required reports, with times and time zones.
3. **Eligibility**: which kinds of institutions can apply, who can be a PI or senior personnel, and any limits on the number of proposals.
4. **Award information**: how long awards last, how much each award can be, how many awards are expected, and when they'll be made.
5. **Budget requirements and policies**: funding limits, cost sharing, indirect cost (F&A) rules, allowable and unallowable costs, and any requirements for personnel effort.
6. **Submission details**: how and where to submit, and who has to submit it.
7. **Application components**: every document the proposal needs, with page limits, any sections the announcement requires inside those documents, optional documents, and formatting rules.
8. **Compliance risks**: human subjects, animals, biosafety, export control, data security, or anything similar the announcement mentions.
9. **Foreign influence and international components**: foreign collaborators, work or travel outside the U.S., and any related disclosures.
10. **Special requirements**: anything specific to this program that doesn't fit above, such as required partnerships, evaluation plans, or mentoring plans.
11. **Important notes**: anything else we shouldn't miss.

Only use information from the announcement. If something isn't stated, write "Not stated" instead of guessing.

---

## Quality Standards

- Use the prompt text above verbatim. Record any change as a new version in `CHANGELOG.md`.
- Supply the announcement the way a user would in the tool being tested, and record how it was supplied.
