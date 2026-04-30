# Changelog

All notable changes to this component. Versions follow semver: MAJOR for output-contract breaks, MINOR for backward-compatible additions, PATCH for wording or clarity.

## [0.1.0] — 2026-04-30

- Initial experimental release.
- Schema derived from the `proposal-document-completeness` v2 Vandalizer workflow in `ui-insight/ProcessMapping` (two parallel Extraction tasks + Formatting task; 16 source fields).
- Three-layer shape: as-found inventory (8 keys), sponsor requirements (4 keys), gap analysis (4 keys).
- `per_person_document_matrix` realized as an array of `{person_name, biosketch, current_and_pending, collaboration_and_affiliation, synergistic_activities, missing}` objects (rather than the source `Table` field) so the per-person `missing` list is attached directly to the row.
- `subaward_documents` realized as an array of `{subawardee_name, commitment_form, budget, budget_justification, senior_key_docs, scope_of_work, facilities_equipment, missing}` objects so the per-subawardee gap is computed inline.
- `review_type` enum matches the source `Review_Type` Enum_Values (`7-day basic review`, `10-day full review`, `Not specified`).
- Cross-field rules from the source workflow (CFR-01 budget vs. senior-key match, CFR-02 mentoring plan trigger, CFR-03 subaward verification) are encoded by the schema shape itself and re-asserted in the prompt's encoding rules.
- UDM column bindings preserved: `sponsor_name` → `Sponsor_Organization`; `senior_key_personnel` → `Personnel`; `has_subawards` triggers `Subaward` presence; the proposal record itself → `Proposal`.
- No eval cases yet — status `experimental` until at least one golden extraction is added under `evals/cases/`.
