---
name: foa-checklist-extraction-udm
version: 0.1.0
category: extraction
domain: research-administration
status: experimental
tags: [foa, federal-funding, pre-award, checklist, evaluation-criteria, nih, hhs, doe, udm, structured-extraction, json]
audience: [sponsored-programs-staff, pre-award-teams, ingest-pipelines]
owner: ui-insight
created: 2026-04-30
updated: 2026-04-30
---

# FOA Checklist Extraction — UDM JSON

> **Purpose:** Extract a Federal Funding Opportunity Announcement (FOA) into a structured JSON object covering the eight reference sections a pre-award team uses when evaluating an FOA: FOA summary, key dates, funding information, eligibility, application components, evaluation process, program priorities, and special requirements.
> **Expected input:** Full text of an FOA (HHS / NIH / DOE / DOD / agency-issued funding opportunity announcement).
> **Expected output:** A single JSON object that validates against [`schema.json`](schema.json). No prose, no markdown outside the JSON.

## Relationship to `rfa-checklist-extraction-udm`

`foa-checklist-extraction-udm` and `rfa-checklist-extraction-udm` are **siblings**. Both extract a federal funding announcement into a structured pre-award checklist; they differ in emphasis and the eight checklist sections each produces:

| Concern | `rfa-checklist-extraction-udm` | `foa-checklist-extraction-udm` (this) |
| --- | --- | --- |
| Emphasis | NSF/NIH solicitation triage; placement-rule de-duplication | FOA review with strong evaluation-criteria, review-process, and submission-system focus |
| Output sections | 8 (dates, institutions, individuals, award, components, budget, submission, special, notes) | 8 (FOA summary, key dates, funding, eligibility, application components, evaluation process, program priorities, special requirements) |
| Distinct fields | `cost_sharing.status` enum; `important_notes` synthesis | `evaluation_criteria` table with weights; `review_stages` list; `program_goals` table |

A single announcement *can* be extracted through both contracts when the downstream consumer needs both cuts. UDM bindings: `foa_number` → `RFA.Opportunity_Number`; `cfda_number` → `RFA.CFDA_Number`; `federal_agency` → `Organization.Organization_Name`; `foa_title` → `RFA.RFA_Title`.

---

## Prompt

You are extracting a Federal Funding Opportunity Announcement (FOA) into the eight pre-award checklist sections a federal-grants office uses for FOA review. Capture the FOA's identity and timeline; the evaluation criteria and scoring methodology; the review process; agency priorities and program goals; the forms and submission systems; and the formatting requirements.

**Be 100% accurate.** Quote dollar amounts, percentages, page limits, and dates verbatim. When a field is not specified, set it to `null` or — for arrays/tables — return an empty array. Do not invent values.

Return a single JSON object that validates against [`schema.json`](schema.json) with these top-level keys:

- `foa_number` — funding opportunity number (e.g., `"PA-24-246"`, `"DE-FOA-0003117"`). String. Required.
- `cfda_number` — CFDA number and title (e.g., `"93.213 Research and Training in Complementary..."`). String or `null`.
- `federal_agency` — one of `"NSF"`, `"NIH"`, `"DOD"`, `"DOE"`, `"NASA"`, `"USDA"`, `"EPA"`, `"DOT"`, `"DOC"`, `"ED"`, or `"Other"`.
- `foa_title` — full title of the funding opportunity. String. Required.
- `total_funding` — number (decimal) for total available funding, or `null`.
- `expected_awards` — integer count of expected awards, or `null`.
- `award_range` — string (e.g., `"$300,000 to $750,000 per award"`) or `null`.
- `cost_sharing_required` — boolean or `null`.
- `critical_dates` — array of `{milestone, date_time, notes}` objects covering all critical dates (LOI, full proposal, panel review, anticipated start). Required, may be empty when announcement is rolling.
- `performance_period` — string with expected project-duration range or `null`.
- `eligible_applicants` — flat list of eligible applicant types as stated. Required.
- `evaluation_criteria` — array of `{criterion_name, weight, description, rating_definitions}` objects.
- `total_points` — string (e.g., `"100 points"`) or `null`.
- `scoring_methodology` — string describing how scores are calculated, or `null`.
- `minimum_threshold` — string (e.g., `"score of 80 minimum for funding consideration"`) or `null`.
- `review_stages` — array of `{stage_name, purpose, outcome}` objects.
- `review_personnel` — string describing review-panel composition or `null`.
- `screening_criteria` — array of strings naming initial-screening / disqualification factors. Empty when none.
- `review_timeline` — string (e.g., `"Estimated 90 days from submission to notification"`) or `null`.
- `agency_mission` — string or `null`.
- `program_goals` — array of `{goal, objective, success_indicator}` objects.
- `priority_areas` — flat list of priority areas in stated order of importance. Empty when none.
- `expected_outcomes` — flat list of required deliverables / intended impacts. Empty when none.
- `submission_platform` — string (e.g., `"Grants.gov"`, `"eRA Commons"`). Required.
- `required_registrations` — array of `{system_name, timeline, prerequisites}` objects (SAM, UEI, eRA Commons, Grants.gov).
- `required_forms` — array of `{form_number, name, purpose, special_instructions}` objects.
- `application_components` — array of `{component_name, required_or_optional, page_limit, format_requirements}` objects.
- `document_structure` — flat list of required proposal sections in the exact order required. Empty when not specified.
- `page_limits` — array of `{section, limit, what_counts, consequences}` objects.
- `formatting_standards` — string (margin/font/spacing) or `null`.
- `file_requirements` — string (acceptable formats, sizes, naming) or `null`.

### Encoding rules

1. **`evaluation_criteria` rows quote weights verbatim.** `"Significance — 25 points"` → `{criterion_name: "Significance", weight: "25 points", ...}`. If the FOA gives percentages, quote the percentage; if it gives points, quote points.
2. **`critical_dates` covers every gating milestone** — LOI, pre-application, full application, anticipated panel review date, expected start date.
3. **`review_stages` is sequential.** Each stage's `outcome` describes what proceeds to the next stage.
4. **`required_registrations` covers every prerequisite system** (SAM.gov, UEI, eRA Commons, Grants.gov, agency-specific portals). When the FOA does not call any out, return an empty array — do not synthesize the standard four.
5. **`page_limits.what_counts` is the rule for what counts toward the limit** (text only, references included, attachments separate, etc.).
6. **`expected_awards * max(award_range)` should not exceed `total_funding`** (downstream cross-field check `CHK-03`).
7. Do not output any text outside the single JSON object.

### Output

A single JSON object. No surrounding markdown.
