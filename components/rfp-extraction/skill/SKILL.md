---
name: rfp-extraction
version: 1.0.0
description: Extracts a complete submission and eligibility checklist from a federal funding announcement (RFP, RFA, FOA, NOFO, BAA, Dear Colleague Letter, program solicitation). Use when the user provides or references a funding announcement and wants a PI- or OSP-ready compliance checklist. Also use when the user mentions preparing a proposal and needs to know page limits, required documents, deadlines, or deviations from the agency's standard proposal guide.
---

# RFP Extraction Skill

Produces a comprehensive, actionable submission and eligibility checklist from a federal funding announcement. The output must let a Principal Investigator guide proposal development and an Office of Sponsored Programs (OSP) compliance reviewer verify the proposal is ready for submission. Every requirement must be traceable to the source document — do not invent requirements, and do not omit requirements because they seem routine.

## When to use

- The user provides the full text, a URL, or an attached document for a funding announcement
- The user asks for a submission checklist, eligibility review, or compliance review of a solicitation
- The user is preparing a proposal and asks about page limits, required sections, or prohibited materials

## Instructions

**Read the entire document before producing any output.** Critical requirements often appear in unexpected locations — eligibility restrictions in award conditions, page limits in review criteria, prohibited materials in supplemental guidance. A single missed requirement can result in a proposal being returned without review.

**Distinguish three layers of requirements:**

1. **Parent guide defaults** — Requirements inherited from the agency's standard proposal guide (NSF PAPPG, NIH SF424 Application Guide, DOE Merit Review Guide, DoD BAA instructions). Apply unless explicitly overridden. If you recognize the parent guide, include its standard document requirements as a baseline.
2. **Solicitation-specific requirements** — Requirements stated explicitly in this announcement. Override or supplement the parent guide.
3. **Solicitation-specific deviations** — Places where this solicitation explicitly changes, restricts, or relaxes the parent guide defaults. These are the highest-risk items for compliance review.

**Adapt to structural complexity.** Do not force a simple template onto a complex solicitation. Some have single deadlines, others multiple rounds. Some allow unlimited proposals, others impose per-institution or per-PI limits. Some require letters of intent, others prohibit preliminary submissions.

## Output format

Produce a single markdown document. Use `- [ ]` for every actionable item, nested checkboxes for sub-requirements, bold for critical constraints, quoted blocks for contextual notes, and tables for structured data (dates, award amounts).

Required sections, in order:

- **Header block** — Solicitation number, program title, posted date, funding agency, award type, estimated awards, award amount, total program budget
- **A. Key Dates** — Single deadline or multi-round table; note timezone; flag inconsistent dates
- **B. Eligibility Requirements** — B1 Organizational, B2 PI/Co-PI, B3 Cost Sharing
- **C. Pre-Submission Requirements** — Only if the solicitation includes LOI / preliminary / white paper / pre-application steps
- **D. Full Proposal General Requirements** — D1 Submission Logistics, D2 Page Limits, D3 Standard Document Requirements
- **E. Project Description / Narrative Required Sections** — Exact required headers, content elements, and any "consider" items (flagged as guidance)
- **F. Supplemental Materials** — F1 Required, F2 Prohibited
- **G. Budgetary Requirements** — Caps, F&A, cost sharing, equipment thresholds, participant support, subawards
- **H. Merit Review Criteria** — Standard + solicitation-specific criteria, weights, review mechanism
- **I. Special Award Conditions & Post-Award Requirements** — Informational; acknowledge during development
- **J. Deviations from Parent Guide** — Numbered list specifically for OSP compliance review
- **K. Contacts & Resources** — Program officer, help desk, CFDA / Assistance Listing numbers, parent guide links
- **Footer** — `*Checklist extracted from [Number], posted [Date]. Always verify against the current solicitation and the applicable version of [Parent Guide Name].*`

## Quality standards

1. **Completeness** — Every requirement stated in the document appears in the checklist.
2. **Precision** — Use the solicitation's exact language for section headers and prescribed text. Preserve specific numbers, limits, and constraints verbatim.
3. **Actionability** — Every checkbox describes something a person can verify or do.
4. **Explicitness about absence** — When the solicitation says "no restrictions," include a checkbox confirming that fact.
5. **Severity signaling** — When noncompliance has a stated consequence (e.g., "returned without review"), note it in bold adjacent to the item.
6. **Conditional requirements** — State the condition explicitly (e.g., "Mentoring Plan required if proposal requests postdoc funding").
7. **Disambiguation** — Flag ambiguities or apparent errors rather than silently picking an interpretation.
