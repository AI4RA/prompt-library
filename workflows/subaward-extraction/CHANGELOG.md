# Changelog

All notable changes to this workflow. Versions follow semver.

## [0.1.0] — 2026-04-30

- Initial experimental release.
- Two-step runtime mirroring the source `subaward-extraction` v2 workflow in `ui-insight/ProcessMapping`: six parallel Extraction tasks (Core Award Information; Contact Information with 18 flat items; Dates & Monetary Values; Financial Policies; Reporting Requirements; Compliance Requirements) plus a Consolidation Prompt that composes the 18 contact items into six `{name, email, phone}` objects, normalizes the two enums, and enforces CFR-01 reconciliation.
- `cost_type` enum (`Cost Reimbursement`, `Fixed Price`, `Time and Materials`); `invoicing_frequency` enum (`Monthly`, `Quarterly`, `Semi-Annual`, `Annual`) — match the source workflow's enums.
- Validation plan carries CHK-01 (Monetary cross-reference, arithmetic/error), CHK-02 (Date consistency, consistency/error), CHK-03 (Contact info format, format/warning) — matches the source `Validation_Plan`.
- Pins `subaward-extraction-udm@0.1.0`.
