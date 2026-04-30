# Changelog

All notable changes to this workflow. Versions follow semver.

## [0.1.0] — 2026-04-30

- Initial experimental release.
- Two-step runtime mirroring the source `prior-approval-extraction` v2 workflow in `ui-insight/ProcessMapping`: one Extraction task with an embedded SearchSet (9 items) plus one Consolidation Prompt that collapses the flat outputs into the schema's nested `budget_approvals`, `scope_timeline_approvals`, and `approval_procedures` shapes.
- Validation plan carries CHK-01 (Threshold format validation, format/warning) and CHK-02 (Approval procedure completeness, completeness/warning) — matches the source `Validation_Plan`.
- Pins `prior-approval-extraction-udm@0.1.0`.
