# Changelog

All notable changes to this component. Versions follow semver: MAJOR for output-contract breaks, MINOR for backward-compatible additions, PATCH for wording or clarity.

## [0.1.0] — 2026-05-20

- Initial experimental release.
- Schema derived from the `compliance-personnel-verification` v1 Vandalizer workflow in `ui-insight/ProcessMapping` (two parallel extraction tasks, 10 source fields, two cross-field rules, four validation-plan checks).
- Six-block shape (`proposal_metadata` + `personnel_identification` + `sfi_verification` + `rst_verification` + `non_compliant_personnel` + `verification_status`) covers both the per-person verification matrices and the proposal-level applicability metadata + summary counts.
- `proposal_type` exposed as the three-value enum (`Research`, `Non-Research`, `Not specified`) and `sponsor_type` as the four-value enum (`Federal`, `State`, `Non-Federal`, `Not specified`) — matches the source workflow.
- SFI per-person `status` exposed as a five-value enum (`Valid`, `Expiring Soon`, `Expired`, `Not Found`, `Review Required`) per the source workflow's task instructions; RST per-person `status` as three-value (`Complete`, `Incomplete`, `Review Required`); non-compliance `priority` as three-value (`Critical`, `High`, `Medium`); overall `overall_status` as three-value (`All Compliant`, `Non-Compliance Found`, `Not Applicable`).
- Source `Is_Required: true` fields mirrored into `required` lists at the block level (`proposal_type`, `sponsor_type`, `sfi_rst_required`, `section_66_personnel`, `section_2_personnel`, `consolidated_personnel`, `spreadsheet_date`, the five summary counts).
- Counts (`total_personnel_checked`, `sfi_compliant_count`, `rst_compliant_count`, `fully_compliant_count`) typed as JSON integers, not quoted strings. `days_since_disclosure` is a JSON integer with `minimum: 0`.
- UDM column bindings preserved at the leaf level: `section_2_personnel[].name` → `Personnel.First_Name` / `Personnel.Last_Name`. The verification matrices themselves are repo-local — no shared UDM compliance table exists for them yet.
- Multi-source input model documented explicitly: the contract assumes the SFI disclosure records and RST completion spreadsheet are uploaded as workflow documents alongside the VERAS proposal. When any input is missing, the contract requires the workflow to emit `null` and capture the gap in `verification_status.notes` rather than silently assuming compliance.
- No eval cases yet — status `experimental` until at least one golden extraction is added under `evals/cases/`.
