# Changelog

All notable changes to this workflow. Versions follow semver.

## [0.1.0] — 2026-04-30

- Initial experimental release.
- Two-step runtime mirroring the source `award-compliance-extraction` v2 workflow in `ui-insight/ProcessMapping`: two parallel Extraction tasks (compliance framework + financial management) plus a Consolidation Prompt that merges/dedupes compliance_calendar entries across both fragments and normalizes the audit_requirements and record_retention enums.
- `audit_requirements` enum (`Single Audit`, `A-133`, `Program-Specific Audit`, `Not applicable`) and `record_retention` enum (`3 years`, `5 years`, `7 years`, `Per sponsor requirements`) — match the source workflow's enums.
- Validation plan carries CHK-01 (Monetary amount format, format/error), CHK-02 (Date validity, format/error), CHK-03 (Compliance calendar completeness, completeness/warning) — matches the source `Validation_Plan`.
- Pins `award-compliance-extraction-udm@0.1.0`.
