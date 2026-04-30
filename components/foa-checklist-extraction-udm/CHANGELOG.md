# Changelog

All notable changes to this component. Versions follow semver.

## [0.1.0] — 2026-04-30

- Initial experimental release.
- Schema derived from the `foa-checklist-extraction` v2 Vandalizer workflow in `ui-insight/ProcessMapping` (six parallel Extraction tasks + Formatting task; 31 source fields).
- 31-field shape covering the eight FOA reference sections used by federal-grants offices for FOA review.
- `federal_agency` enum matches the source `Federal_Agency` Enum_Values (NSF, NIH, DOD, DOE, NASA, USDA, EPA, DOT, DOC, ED, Other).
- `evaluation_criteria`, `review_stages`, `program_goals`, `required_registrations`, `required_forms`, `application_components`, `page_limits`, and `critical_dates` realized as arrays of typed objects (rather than the source `Table` fields) so per-row attributes attach to the right entry.
- Cross-field rule from the source workflow (CFR-01: expected_awards * max(award_range) <= total_funding) is encoded in the prompt's encoding rules and the workflow validation_plan.
- UDM column bindings preserved: `foa_number` → `RFA.Opportunity_Number`; `cfda_number` → `RFA.CFDA_Number`; `federal_agency` → `Organization.Organization_Name`; `foa_title` → `RFA.RFA_Title`.
- Sibling of `rfa-checklist-extraction-udm`: same source family, different output cut.
- No eval cases yet — status `experimental` until at least one golden extraction is added under `evals/cases/`.
