---
name: proposal-document-completeness-udm
version: 0.1.0
category: extraction
domain: research-administration
status: experimental
tags: [pre-award, proposal, completeness, near-final-review, nsf, nih, gap-analysis, udm, structured-extraction, json]
audience: [sponsored-programs-staff, pre-award-teams, ingest-pipelines]
owner: ui-insight
created: 2026-04-30
updated: 2026-04-30
---

# Proposal Document Completeness — UDM JSON

> **Purpose:** Automate the near-final document-completeness review of a proposal package: identify all senior key personnel, the four required documents per person (biosketch, current & pending, collaboration & affiliation, synergistic activities), subaward documents, and conditional-requirement triggers, then produce a comprehensive gap-analysis JSON.
> **Expected input:** A proposal package — VERAS upload bundle, NSF/NIH proposal in PDF/DOCX form, plus the relevant solicitation (RFA / FOA / NOFO).
> **Expected output:** A single JSON object that validates against [`schema.json`](schema.json). No prose, no markdown outside the JSON.

## When to use this contract

This is the gap-analysis cut of a proposal package, designed to be run when the package is close to submission and a sponsored-programs analyst is about to send it back to the PI for final fixes. It produces a single object with three logical layers: the **as-found inventory** (what is uploaded, who is named, what subawards exist), the **sponsor requirements** (what should be there per the solicitation and agency policy), and the **gap analysis** (what is missing, per requirement and per person).

UDM-aligned: senior key personnel resolve to UDM `Personnel`; subaward presence resolves to `Subaward`; sponsor identity resolves to `Sponsor_Organization`; the proposal record itself resolves to `Proposal`.

This component does **not** cover the budget-personnel extraction — that lives in `proposal-budget-personnel-extraction-udm` (which feeds the `Senior_Key_Personnel` and `Has_Postdocs_Or_Grad_Students` signals consumed here). It does not cover the solicitation extraction itself — that lives in `rfa-checklist-extraction-udm` or `foa-checklist-extraction-udm`.

---

## Prompt

You are running a near-final document-completeness review on a proposal package. Your job is to identify everything that is uploaded, everything that should be uploaded per the sponsor's requirements, and everything missing — both in aggregate and per person.

**Be 100% accurate.** The downstream consumer of this output is a sponsored-programs analyst preparing a "missing documents" message to the PI; a fabricated entry costs the analyst a back-and-forth with the PI and erodes trust in the workflow. When a value is not present, set it to `null` or — for arrays/tables — return an empty array. Do not invent personnel, documents, or requirements.

Search the entire upload bundle and the solicitation for content in or near sections titled *Section 2 (Personnel)*, *Section 8 (Subawards)*, *Section 9.2 (Budget)*, *Proposal Documents*, *Senior Key Personnel*, *Solicitation Requirements*, *Proposal Preparation Instructions*, *Required Documents*, or *Submission Requirements*.

Return a single JSON object that validates against [`schema.json`](schema.json) with these top-level keys:

- `sponsor_name` — sponsor agency name (e.g., `"National Science Foundation"`). Required.
- `rfa_foa_number` — solicitation number (e.g., `"NSF 26-508"`). String or `null`.
- `proposal_track_type` — proposal track type that may trigger additional requirements (e.g., `"TTP-P"`, `"standard"`, `"track-2"`). String or `null`.
- `review_type` — one of `"7-day basic review"`, `"10-day full review"`, `"Not specified"`, or `null`.
- `senior_key_personnel` — array of `{name, role, institution}` objects. One row per named person.
- `budget_personnel` — flat list of strings naming personnel as identified from the budget document.
- `has_postdocs_or_grad_students` — boolean.
- `has_subawards` — boolean.
- `uploaded_documents` — flat list of strings naming each currently uploaded document.
- `required_documents_checklist` — array of `{document_name, required_for, present, notes}` objects covering every document the sponsor requires.
- `conditional_requirements` — array of `{condition, document_name, triggered, notes}` objects covering documents that are required only when a condition holds (e.g., mentoring plan when postdocs present).
- `per_person_required_documents` — flat list of document names required per senior key person (typically the four NSF documents).
- `per_person_document_matrix` — array of `{person_name, biosketch, current_and_pending, collaboration_and_affiliation, synergistic_activities, missing}` objects. One row per senior key person; `missing` is a list of the four document names that are missing for that person.
- `subaward_documents` — array of `{subawardee_name, commitment_form, budget, budget_justification, senior_key_docs, scope_of_work, facilities_equipment, missing}` objects (when `has_subawards: true`). Empty array otherwise.
- `subaward_required_documents` — flat list of strings naming the documents required per subawardee per sponsor policy.
- `personnel_discrepancies` — flat list of strings describing discrepancies between budget personnel and senior-key-personnel listings (e.g., duplicates, missing entries, name mismatches). Empty array when none.
- `prioritized_missing` — ordered array of strings describing the missing items the analyst should ask the PI about, ranked by severity (e.g., compliance-critical first).

### Encoding rules

1. **Booleans must be derived from observable signals.** `has_subawards` is `true` only when a subaward commitment form, subaward budget, or subaward narrative is present in the package. `has_postdocs_or_grad_students` is `true` only when the budget actually lists a postdoc or graduate-student line.
2. **`per_person_document_matrix` is keyed on `senior_key_personnel`.** Every named person in `senior_key_personnel` must have exactly one row in the matrix. The four document booleans (`biosketch`, `current_and_pending`, `collaboration_and_affiliation`, `synergistic_activities`) are `true` iff that document is uploaded and matches that person's name; `missing` is the list of `false`-valued document names for that row.
3. **`subaward_documents` rows are keyed on each named subawardee.** When `has_subawards: false`, this is an empty array.
4. **`conditional_requirements.triggered` is the boolean that fires the condition.** For "mentoring plan if postdocs/grads", `triggered` equals `has_postdocs_or_grad_students`; the analyst can cross-check.
5. **`prioritized_missing` is opinionated.** Rank: (a) compliance-critical items the sponsor will reject the proposal for missing, (b) per-person required documents, (c) conditional documents whose condition is triggered, (d) optional improvements. Do not include items that are present.
6. Do not output any text outside the single JSON object.

### Output

A single JSON object. No surrounding markdown.
