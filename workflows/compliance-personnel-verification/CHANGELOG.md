# Changelog

All notable changes to this workflow. Versions follow semver: MAJOR for step-structure changes, MINOR for additive changes (e.g., new search_set_items, validation checks), PATCH for display-name or wording edits.

## [0.1.0] — 2026-05-20

- Initial experimental release.
- Two-step runtime mirroring the source `compliance-personnel-verification` v1 workflow in `ui-insight/ProcessMapping`: two parallel Extraction tasks (personnel identification + compliance status verification) with embedded SearchSets, plus a Consolidation Prompt that assembles the two JSON fragments into a single schema-conformant object and derives `non_compliant_personnel` + the five `verification_status` counts from the per-person SFI / RST status records.
- Multi-source input model: requires the operator to upload the VERAS proposal, the SFI disclosure records, and the daily RST completion spreadsheet together as workflow documents. When any source is missing, the workflow emits non-compliant defaults and captures the gap in `verification_status.notes` rather than silently assuming compliance.
- `proposal_type` and `sponsor_type` enums match the source workflow exactly. `sfi_verification[].status` exposed as the five-value enum from the source (`Valid`, `Expiring Soon`, `Expired`, `Not Found`, `Review Required`). `rst_verification.records[].status` as the three-value enum (`Complete`, `Incomplete`, `Review Required`). `non_compliant_personnel[].priority` as three-value (`Critical`, `High`, `Medium`). `verification_status.overall_status` as three-value (`All Compliant`, `Non-Compliance Found`, `Not Applicable`).
- Validation plan carries CHK-01..CHK-04 — matches the source `Validation_Plan` with field-target paths updated to reflect the schema's six-block shape.
- Source `Cross_Field_Rules` (CFR-01..CFR-02) enforced by the Consolidation Prompt at runtime: CFR-01 (Section 6.6 ⊆ Section 2) emits entries to `personnel_discrepancies`; CFR-02 (365-day validity) drives the per-person SFI status enum.
- Pins `compliance-personnel-verification-udm@0.1.0`.
