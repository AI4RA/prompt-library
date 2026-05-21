# Changelog

All notable changes to this workflow. Versions follow semver: MAJOR for step-structure changes, MINOR for additive changes (e.g., new search_set_items, validation checks), PATCH for display-name or wording edits.

## [0.1.0] — 2026-05-20

- Initial experimental release.
- Two-step runtime mirroring the source `award-modification-intake` v1 workflow in `ui-insight/ProcessMapping`: three parallel Extraction tasks (modification-type identification, financial impact, compliance requirements) with embedded SearchSets, plus a Consolidation Prompt that assembles the three JSON fragments into a single schema-conformant object and enforces the four cross-field rules (CFR-01..CFR-04 from the source).
- `modification_type` exposed as the seven-value enum from the source workflow (`Additional Funds`, `No-Cost Extension`, `PI Change`, `Rebudget`, `Scope Change`, `Administrative Change`, `Combined (multiple types)`).
- `execution_status` exposed as the three-value enum from the source workflow (`Unilateral (fully executed)`, `Bilateral (requires signature)`, `Not specified in the document`).
- Validation plan carries CHK-01..CHK-05 — matches the source `Validation_Plan` with field-target paths updated to reflect the schema's three-block shape.
- Source STEP-03 ApprovalNode (Post-Award Specialist review before Banner entry) intentionally omitted from this manifestation — operator review is handled by Vandalizer's UI outside the workflow manifest.
- Pins `award-modification-intake-udm@0.1.0`.
