# Changelog

All notable changes to this workflow. Versions follow semver: MAJOR for step-structure changes, MINOR for additive changes (e.g., new search_set_items, validation checks), PATCH for display-name or wording edits.

## [0.1.0] — 2026-05-20

- Initial experimental release.
- Two-step runtime mirroring the source `section2-personnel-eligibility` v1 workflow in `ui-insight/ProcessMapping`: two parallel Extraction tasks (Section 2 personnel extraction + eligibility / DGA verification) with embedded SearchSets, plus a Consolidation Prompt that assembles the two JSON fragments into a single schema-conformant object and derives the seven `verification_summary` counts and four flag arrays from the per-person / per-org-code / per-DGA records.
- Multi-source input model: requires the operator to upload the VERAS proposal, Banner NBAJOBS extract, and Department List together as workflow documents. The APM 45.22 eligible-titles list is consumed from the knowledge base / search corpus. When any source is missing, the workflow emits non-compliant defaults and captures the gap in `verification_summary.notes`.
- `eligibility_check[].eligibility_status` exposed as the three-value enum (`Eligible`, `Not Eligible`, `Review Required`). `dga_cross_reference[].action_needed` exposed as the two-value enum (`No action needed`, `FLAG — Must be added to Section 2`).
- Validation plan carries CHK-01..CHK-04 — matches the source `Validation_Plan` with field-target paths updated to reflect the schema's seven-block shape.
- Source `Cross_Field_Rules` (CFR-01..CFR-03) enforced by the Consolidation Prompt at runtime.
- Pins `section2-personnel-eligibility-udm@0.1.0`.
