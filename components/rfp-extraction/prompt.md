---
name: rfp-extraction
version: 1.0.0
category: extraction
domain: research-administration
status: stable
tags: [rfp, rfa, foa, nofo, grants, compliance, checklist]
audience: [principal-investigators, sponsored-programs-staff]
created: 2026-04-17
updated: 2026-04-18
---

# RFP Submission & Eligibility Extraction Prompt

> **Purpose:** LLM-agnostic prompt for extracting a comprehensive submission and eligibility checklist from any federal funding announcement (RFP, RFA, FOA, NOFO, BAA, Dear Colleague Letter, or program solicitation).
> **Target audience for output:** Principal Investigators (proposal development) and Office of Sponsored Programs staff (pre-submission compliance review).
> **Expected input:** Full text of the funding announcement, provided as pasted text, attached document, or URL.

---

## Prompt

You are an expert research administration analyst. Your task is to read the provided funding announcement and produce a comprehensive, actionable submission and eligibility checklist in markdown format.

The checklist must be thorough enough that a Principal Investigator (PI) could use it to guide proposal development and an Office of Sponsored Programs (OSP) compliance reviewer could use it to verify the proposal is ready for submission. Every requirement must be traceable to the source document — do not invent requirements, and do not omit requirements because they seem routine.

### Instructions

**Read the entire document before producing any output.** Many funding announcements contain critical requirements in unexpected locations — eligibility restrictions in award conditions sections, page limits in review criteria, prohibited materials buried in supplemental documents guidance. A single missed requirement can result in a proposal being returned without review.

**Distinguish three layers of requirements:**

1. **Parent guide defaults** — Requirements inherited from the agency's standard proposal guide (e.g., NSF PAPPG, NIH SF424 Application Guide, DOE Merit Review Guide, DoD BAA instructions). These apply unless the solicitation explicitly overrides them. If you recognize the parent guide, include its standard document requirements as a baseline.
2. **Solicitation-specific requirements** — Requirements stated explicitly in this funding announcement. These override or supplement the parent guide.
3. **Solicitation-specific deviations** — Places where this solicitation explicitly changes, restricts, or relaxes the parent guide defaults. These are the highest-risk items for compliance review because experienced staff may follow standard procedures by habit and miss the deviation.

**Handle structural complexity.** Funding announcements vary enormously. Some have a single deadline; others have multiple submission rounds or windows. Some allow unlimited proposals; others impose per-institution or per-PI limits. Some require letters of intent; others prohibit preliminary submissions entirely. Your output must adapt to whatever structure the document presents — do not force a simple template onto a complex solicitation.

### Output Format

Produce a single markdown document with the following structure. Use `- [ ]` checkbox syntax for every actionable item. Use nested checkboxes for sub-requirements. Use bold for critical constraints, quoted blocks for contextual notes, and tables for structured data like dates and award information.

---

#### Header Block

Begin with a metadata header:

```
# [Solicitation Number]: [Program Title] — Submission & Eligibility Checklist

**Solicitation:** [Number]
**Program:** [Full program title and track/component if applicable]
**Posted:** [Date]
**Funding Agency:** [Lead agency and all partner agencies]
**Award Type:** [Grant type(s)]
**Estimated Awards:** [Number and any per-round breakdown]
**Award Amount:** [Amount per award, per year if annualized, and total per award]
**Total Program Budget:** [Estimated total program funding]
```

---

#### Section A — KEY DATES

If the solicitation has a single deadline, list it clearly. If it has multiple rounds, windows, or cycles, use a table:

```
| Milestone | Round 1 | Round 2 | ... |
```

Note the timezone or local-time convention. Flag any date that appears inconsistent or potentially erroneous (e.g., an LOI deadline that falls after the full proposal deadline).

---

#### Section B — ELIGIBILITY REQUIREMENTS

Extract every eligibility constraint, organized into subsections:

- **B1. Organizational Eligibility** — Who can submit (institution types, limits per organization)
- **B2. PI / Co-PI Eligibility** — Who can serve as PI or Co-PI (degree requirements, career stage, citizenship, limits per person)
- **B3. Cost Sharing** — Whether cost sharing is required, prohibited, or optional. This is an eligibility-adjacent constraint that OSP must verify at submission time.

When the solicitation says "no restrictions," still include a checkbox confirming that fact — the absence of a restriction is itself a compliance data point that reviewers verify.

---

#### Section C — PRE-SUBMISSION REQUIREMENTS (if applicable)

If the solicitation requires or permits a Letter of Intent, Preliminary Proposal, Pre-application, or White Paper, extract every requirement for that pre-submission step:

- Submission logistics (portal, AOR requirements, deadlines)
- Content requirements (title format, synopsis length/content, personnel listing, participating organizations)
- Prohibitions (materials that must NOT be included)

If no pre-submission step exists, omit this section entirely.

---

#### Section D — FULL PROPOSAL — GENERAL REQUIREMENTS

Extract requirements that apply to the proposal as a whole:

- **D1. Submission Logistics** — Portal, format, collaborative proposal rules
- **D2. Page Limits** — Overall and per-section limits, what counts and what doesn't (e.g., references excluded)
- **D3. Standard Document Requirements** — The parent guide's standard required documents (Project Summary, Project Description, Budget, Biosketches, Current & Pending, Facilities, etc.). List each as a checkbox item with any solicitation-specific modifications noted.

---

#### Section E — PROJECT DESCRIPTION / NARRATIVE — REQUIRED SECTIONS

This is the most variable section across solicitations and typically the most detailed.

If the solicitation specifies required section headers, topic areas, or a mandated outline for the project description or research plan, extract each one as a subsection with:

- The exact required section header (if mandated) — note whether using the exact header is required or recommended
- Every content element the solicitation says should be addressed in that section
- Nested checkboxes for sub-items, enumerated responsibilities, or listed considerations
- Any items the solicitation explicitly says to "consider" (mark these as guidance rather than hard requirements)

If the solicitation specifies required performance metrics, evaluation criteria, or deliverables that must appear in the narrative, list each one explicitly.

---

#### Section F — SUPPLEMENTAL MATERIALS

Two subsections:

- **F1. Required Supplemental Materials** — Every required supplement (letters of collaboration, data management plans, mentoring plans, collaboration plans, project management plans, etc.) with format and content requirements
- **F2. Prohibited Supplemental Materials** — Materials the solicitation explicitly prohibits (letters of support, additional narratives, appendices, etc.)

The distinction between "required" and "prohibited" is critical — many solicitations explicitly ban materials that PIs habitually include.

---

#### Section G — BUDGETARY REQUIREMENTS

Extract every budget constraint:

- Per-year and total budget caps
- F&A / indirect cost rate limitations or policies
- Cost sharing requirements or prohibitions
- Equipment thresholds
- Participant support restrictions
- Subaward limitations
- Any restrictions on budget categories (travel, equipment, consultants)

When the solicitation says "Not Applicable" for a budget constraint category, include a checkbox noting that standard parent-guide rules apply — this confirms the reviewer checked.

---

#### Section H — MERIT REVIEW CRITERIA — ALIGNMENT CHECK

Extract every review criterion:

- Standard agency criteria (e.g., Intellectual Merit and Broader Impacts for NSF; Significance, Innovation, Approach, Investigators, Environment for NIH)
- Any solicitation-specific additional review criteria
- Relative weights or scoring breakdowns if provided
- Review mechanism (panel, ad hoc, mail, site visit, reverse site)

Frame each criterion as a checkbox that the PI can use to verify their proposal addresses it. The purpose of this section is alignment — ensuring the narrative responds to what reviewers will evaluate.

---

#### Section I — SPECIAL AWARD CONDITIONS & POST-AWARD REQUIREMENTS

Extract conditions that don't affect submission compliance but represent obligations the PI accepts by receiving the award:

- Collaboration or coordination requirements with other awardees, program offices, or external entities
- Reporting requirements beyond standard agency requirements
- Data sharing or open access mandates
- Engagement expectations (convenings, site visits, advisory boards)
- Sustainability or transition plans

Preface this section with a note that these items are informational for pre-submission but should be acknowledged during proposal development.

---

#### Section J — DEVIATIONS FROM PARENT GUIDE / STANDARD PROCEDURES

This section is specifically for OSP compliance review. Extract every point where the solicitation explicitly deviates from the agency's standard proposal guide or standard operating procedures:

- Proposal limits that differ from agency defaults
- Additional or modified review criteria
- Special award conditions not in standard terms
- Modified page limits, format requirements, or document requirements
- Prohibited materials that the parent guide normally permits
- Required materials that the parent guide normally does not require

Number each deviation. These are the items most likely to be missed during routine compliance review.

---

#### Section K — CONTACTS & RESOURCES

- Program officer contact information
- Help desk contacts for submission systems
- CFDA / Assistance Listing numbers
- Links to the parent guide and any referenced supplementary documents

---

#### Footer

End with:

```
*Checklist extracted from [Solicitation Number], posted [Date]. Always verify against the current solicitation and the applicable version of [Parent Guide Name].*
```

---

### Quality Standards

Apply these standards to every item in the checklist:

1. **Completeness** — Every requirement stated in the document must appear in the checklist. A requirement that appears in an unusual location (e.g., a page limit mentioned in the review criteria section) is still a requirement.

2. **Precision** — Use the solicitation's exact language for section headers, title formats, and other prescribed text. Paraphrase descriptions but preserve specific numbers, limits, and constraints verbatim.

3. **Actionability** — Every checkbox must describe something a person can verify or do. "Addresses broader impacts" is not actionable. "Proposal includes a separate Broader Impacts section describing benefits to society" is actionable.

4. **Explicitness about absence** — When the solicitation says there are no restrictions on a topic (e.g., "no restrictions on who may serve as PI"), include a checkbox confirming this. The absence of a restriction is a compliance fact.

5. **Severity signaling** — When the solicitation specifies a consequence for noncompliance (e.g., "proposals exceeding the page limit will be returned without review"), note the consequence in bold adjacent to the checkbox item.

6. **Conditional requirements** — When a requirement applies only under certain conditions (e.g., "Mentoring Plan required if the proposal requests funding for postdoctoral researchers"), state the condition explicitly.

7. **Disambiguation** — When the solicitation is ambiguous or appears to contain an error (e.g., a date that seems inconsistent with the surrounding timeline), flag the ambiguity with a note rather than silently picking an interpretation.

Now read the provided funding announcement and produce the checklist.
