# Changelog

All notable changes to this component. Versions follow semver: MAJOR for output-contract breaks, MINOR for backward-compatible additions, PATCH for wording or clarity.

## [0.1.0] — 2026-04-30

- Initial experimental release.
- Schema derived from the `prior-approval-extraction` v2 Vandalizer workflow in `ui-insight/ProcessMapping` (single Extraction task + Formatting task; 8 source fields).
- Three logical buckets (`budget_approvals`, `scope_timeline_approvals`, `approval_procedures`) plus `rtc_waivers` match the deliverable produced by the canonical extraction prompt.
- Scalar `award_number` field added on top of the source workflow's eight Extraction fields so a single extraction resolves cleanly to UDM `Award`.
- `approval_procedures` realized as an array of `{approval_type, threshold, documentation, authority, timeline, consequences}` objects (rather than the source `Table` field) so per-row procedure mechanics are attached to the correct approval type.
- UDM column bindings preserved: per-row entries resolve to `Modification.Requires_Prior_Approval`; `budget_approvals.subaward_approvals` resolves to `Subaward`.
- No eval cases yet — status `experimental` until at least one golden extraction is added under `evals/cases/`.
