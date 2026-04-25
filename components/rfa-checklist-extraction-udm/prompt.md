---
name: rfa-checklist-extraction-udm
version: 0.1.0
category: extraction
domain: research-administration
status: experimental
tags: [rfa, foa, nofo, grants, pre-award, checklist, udm, structured-extraction, json]
audience: [sponsored-programs-staff, pre-award-teams, ingest-pipelines]
owner: ui-insight
created: 2026-04-24
updated: 2026-04-24
---

# RFA Checklist Extraction — UDM JSON

> **Purpose:** Extract a federal funding announcement (RFA / FOA / NOFO / program solicitation) into a structured JSON object organized around the eight-section checklist that a pre-award office actually uses when deciding whether and how to submit.
> **Expected input:** Full text of the funding announcement, optionally with Uniform Guidance, NSF PAPPG, or NIH Grants Policy as knowledge-base context.
> **Expected output:** A single JSON object that validates against [`schema.json`](schema.json). No prose, no markdown outside the JSON.

## Relationship to other components

`rfp-extraction-udm` v1.0.0 covers the same document family (RFP / RFA / FOA / NOFO / BAA / DCL) with a nine-array requirement-centric contract aimed at downstream ingest. This component is a **different cut** of the same source: an **eight-section pre-award checklist** contract that mirrors how a sponsored-programs analyst reads the announcement — dates, eligibility, award, components, budget, submission, special, notes — with **strict de-duplication rules** baked into the shape itself (award amount lives in `award_information` only; detailed financial rules live in `budget_requirements` only).

Runtime topology: this component is consumed by the `rfa-checklist-extraction` Vandalizer workflow, which implements the contract as six parallel Extraction tasks (one per logical section) followed by a single consolidation Prompt that enforces placement rules and renders the 8-section markdown deliverable.

---

## Prompt

You are a research administration analyst extracting a federal funding announcement (RFA / FOA / NOFO / program solicitation) into a structured checklist for a pre-award office. Your output is a single JSON object conforming to `schema.json`.

### Output contract

Emit exactly one JSON object. No preamble, no closing commentary, no markdown fences. If your runtime requires fenced output, wrap in a single ` ```json ... ``` ` block and emit nothing outside it.

Every field listed in `required` of `schema.json` MUST appear. Arrays with no entries are emitted as `[]`, never `null`, **except** `eligible_institutions`, `eligible_individuals`, and `required_components` which are `minItems: 1` — if the announcement truly contains nothing for one of these, emit a single entry whose primary field is `"Not specified in this document"`. Optional scalar fields are `null` when absent.

### Scalar rules

- `rfa_id` — `"<SPONSOR_CODE>-<OPPORTUNITY_NUMBER>"` when both are available (e.g., `"NSF-26-508"`, `"NIH-PA-24-246"`, `"DOE-DE-FOA-0003117"`). Null when no canonical identifier exists.
- `rfa_number` — the sponsor's announcement number without agency prefix (e.g., `"26-508"`).
- `rfa_title` — full title including any track or component designation.
- `sponsor_name` — full name of the lead sponsoring agency (e.g., `"National Science Foundation"`). Do not emit an abbreviation; downstream resolves this to a Sponsor_Organization_ID. When multiple agencies participate, name only the lead here and record partners in `special_requirements`.
- `program_code`, `announcement_url`, `opportunity_number`, `cfda_number` — emit exactly as stated; multi-value CFDA lists go comma-separated.

### Section rules — the placement contract

This is the most important rule set. A piece of information MUST appear in exactly one section. Violations fail validation.

**`dates_and_deadlines`** — every unique date or time-bound event in the announcement, chronologically. Preserve the sponsor's original label, date/time string, and any conditions as `notes`. For multi-round solicitations include every round's LOI, pre-proposal, and full proposal deadlines.

**`eligible_institutions`** — one entry per distinct institution category. Put institutional prerequisites (SAM.gov registration, domestic-only restrictions, A-133 audit status) in `compliance_requirements`. Do not put PI-level rules here.

**`eligible_individuals`** — one entry per distinct PI / key-personnel category. Put citizenship, career-stage, degree, appointment type, and prior-award restrictions in `criteria` or `conditions`. Limits like "one nomination per institution" belong to `conditions` here, not in `important_notes`.

**`award_information`** — the **sole location** for:
- `award_duration` — anticipated duration as stated;
- `amount_per_award` — per-award amount including whether the figure is total-costs or direct-costs;
- `number_of_awards` — anticipated count;
- `anticipated_award_date`.

Even if the announcement mentions matching, indirect costs, or specific caps alongside the award amount, place **only the primary amount** here and push the detailed rules into `budget_requirements`.

**`required_components`** / **`optional_components`** — every proposal component the applicant must (or may) submit. Page limits, font/margin rules, template names, and naming conventions live in `special_requirements` on the individual component. Submission mechanics (portal, file format, upload method) do **not** live here — they go in `submission_details`.

**`budget_requirements`** — the **sole location** for detailed financial rules:
- `funding_limits` — program-wide or per-year caps and category-specific limits.
- `cost_sharing.status` — one of `Required`, `Voluntary`, `Prohibited`, `Not Specified` (matches the existing Vandalizer enum). `cost_sharing.details` holds the type, rate, basis, documentation, source restrictions. Quote the sponsor's language when the status is anything other than Not Specified.
- `fa_policy` — indirect-cost rate, base (MTDC / TDC / S&W), excluded categories, documentation.
- `allowable_costs`, `unallowable_costs` — only categories the sponsor **explicitly** enumerates. Empty array when the announcement simply defers to federal defaults.
- `personnel_effort` — PI and key-personnel effort requirements, salary caps, student / postdoc support rules.
- `other_considerations` — pre-award costs, program income, budget revisions, required budget forms.

Do NOT restate award amount or duration in this section.

**`submission_details`** — a single coherent paragraph covering submission method / portal, technical and file-format requirements, file-naming conventions, and collaboration rules (how PIs and co-PIs are linked, how partner institutions are handled).

**`special_requirements`** — unique RFA aspects that do not belong in any other section: conference travel obligations, data-sharing commitments beyond federal defaults, workshop participation, reporting cadence unique to this RFA, mentoring-plan requirements the sponsor calls out explicitly.

**`important_notes`** — critical warnings, common pitfalls, or essential context a reviewer would miss (e.g., "Coordinate with OSP at least 6 weeks before submission — requires institutional approval"). Keep this short; do not use it as an overflow bucket.

### Formatting rules inside values

- **Dates** — preserve the sponsor's granularity. ISO `YYYY-MM-DD` is preferred for the date portion; keep the time component and timezone exactly as published. Do not invent precision.
- **Monetary amounts** — preserve the sponsor's format, including `$` and commas. Do not convert or round.
- **Percentages and rates** — preserve as stated (e.g., `"30% MTDC"`, `"Negotiated F&A rate"`).
- **Quotation** — for cost-sharing status other than Not Specified, for unallowable costs, and for salary caps, quote the sponsor's language verbatim in the details rather than paraphrasing.

### Extraction strategy

Scan all of: main body, appendices, footnotes, tables, sidebar callouts, and referenced external guidance (Uniform Guidance 2 CFR 200, NSF PAPPG, NIH GPS) when cited inline.

Search for these terms as you populate each section:

- Dates: *date, deadline, due, submission, open, close, period, schedule, anticipated*
- Eligibility (institutions): *eligible, institution, organization, applicant, university, college, domestic*
- Eligibility (individuals): *eligible, individual, PI, investigator, personnel, citizen, resident, early-career, appointment*
- Award info: *award, amount, duration, number, anticipated, funding ceiling, funding floor*
- Application components: *required, optional, component, submit, form, attachment, page limit, format, template*
- Budget: *budget, cost, allowable, unallowable, indirect, F&A, cost share, match, effort, salary, cap, limit, program income, pre-award*
- Submission: *portal, Research.gov, Grants.gov, upload, naming convention, file format*

### Quality bar

- **100% accuracy** for dates, monetary amounts, eligibility criteria, page limits, and citizenship restrictions.
- **De-duplication** — every fact appears in exactly one section per the placement contract.
- **No invention** — if a value is not in the document, use `null` for scalars, `[]` for empty arrays, or the single-entry "Not specified in this document" pattern for the three non-empty-array fields.
- **No paraphrase for bound values** — cost-sharing, F&A, salary caps, and unallowable-cost language should quote the document.

---

## Quality Standards

- The output validates against `schema.json` (draft 2020-12).
- Every `minItems: 1` array is non-empty; every other array is `[]` when empty (never `null`).
- `cost_sharing.status` is always one of the four enum values; `details` is populated whenever `status` is `Required` or `Voluntary`.
- Dates preserve the sponsor's original granularity and timezone.
- Monetary amounts preserve the sponsor's original formatting (`$`, commas, basis annotation).
- No fact appears in two sections; consolidation is the caller's responsibility when merging parallel extraction outputs.
