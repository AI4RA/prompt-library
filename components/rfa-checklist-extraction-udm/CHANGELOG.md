# Changelog

All notable changes to this component. Versions follow semver: MAJOR for output-contract breaks, MINOR for backward-compatible additions, PATCH for wording or clarity.

## [0.1.0] — 2026-04-24

- Initial experimental release.
- Schema derived from the `rfa-checklist-extraction` v2 Vandalizer workflow in `ui-insight/ProcessMapping` (six parallel extraction tasks + consolidation, 17 source fields).
- Scalar metadata (`rfa_id`, `rfa_number`, `rfa_title`, `sponsor_name`, `program_code`, `announcement_url`, `opportunity_number`, `cfda_number`) aligned with `rfp-extraction-udm` 1.0.0 conventions.
- Eight structured sections each given a distinct shape to enforce the de-duplication / placement contract at schema level.
- `cost_sharing.status` enum matches the Cost_Sharing Enum_Values from the source workflow (`Required`, `Voluntary`, `Prohibited`, `Not Specified`).
- UDM column bindings preserved: `cost_sharing` → `CostShare`, `fa_policy` → `IndirectRate`, `personnel_effort` → `Effort`.
- No eval cases yet — status `experimental` until at least one golden extraction is added under `evals/cases/`.
