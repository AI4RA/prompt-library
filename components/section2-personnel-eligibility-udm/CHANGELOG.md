# Changelog

All notable changes to this component. Versions follow semver: MAJOR for output-contract breaks, MINOR for backward-compatible additions, PATCH for wording or clarity.

## [0.1.0] — 2026-05-20

- Initial experimental release.
- Schema derived from the `section2-personnel-eligibility` v1 Vandalizer workflow in `ui-insight/ProcessMapping` (two parallel extraction tasks, 11 source fields, three cross-field rules, four validation-plan checks).
- Seven-block shape (`personnel_extraction` + `personnel_verification` + `eligibility_check` + `org_code_compilation` + `dga_mapping` + `dga_cross_reference` + `verification_summary`) preserves the source workflow's per-step table structure and adds explicit derivations for the summary counts and flag arrays.
- `eligibility_check[].eligibility_status` exposed as the three-value enum (`Eligible`, `Not Eligible`, `Review Required`) from the source workflow's task language. `dga_cross_reference[].action_needed` exposed as the two-value enum (`No action needed`, `FLAG — Must be added to Section 2`).
- `section_21_personnel` typed with `minItems: 1` (every proposal has a PI). `section_22_personnel` typed as a possibly-empty array (Senior / Key Personnel section often blank).
- Senior / Key Personnel are explicitly excluded from `eligibility_check` per the source workflow's task instructions — only PI / Co-PI need APM 45.22 verification.
- Source `Is_Required: true` fields mirrored into `required` lists at the block level (`section_21_personnel`, `total_personnel_count`, `pi_copis_requiring_eligibility`, every block's identifying fields).
- Counts (`total_personnel_count`, `total_personnel_verified`, `pi_copis_eligible_count`, `unique_org_codes_count`, `dgas_required_count`, `dgas_in_section_2_count`) typed as JSON integers, not quoted strings.
- UDM column bindings preserved at the leaf level: `section_21_personnel[].name` and `section_22_personnel[].name` → `Personnel.First_Name` / `Personnel.Last_Name`. The org-code → DGA mapping, APM 45.22 eligibility, and verification matrices are repo-local — no shared UDM table exists for them yet.
- Multi-source input model documented explicitly: the contract requires the VERAS proposal, Banner NBAJOBS extract, and Department List uploaded as workflow documents (APM 45.22 list is consumed from the knowledge base / search corpus). When any source is missing, the contract requires non-compliant defaults and a `verification_summary.notes` gap-flag.
- No eval cases yet — status `experimental` until at least one golden extraction is added under `evals/cases/`.
