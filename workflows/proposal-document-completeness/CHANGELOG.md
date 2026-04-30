# Changelog

All notable changes to this workflow. Versions follow semver.

## [0.1.0] — 2026-04-30

- Initial experimental release.
- Two-step runtime mirroring the source `proposal-document-completeness` v2 workflow in `ui-insight/ProcessMapping`: two parallel Extraction tasks (proposal components inventory + sponsor requirements) plus a Consolidation & Gap Analysis Prompt that joins the two fragments and computes the per-person and per-subawardee missing lists.
- `review_type` enum (`7-day basic review`, `10-day full review`, `Not specified`) — matches the source workflow's enum.
- Validation plan carries CHK-01 (Personnel list completeness, completeness/error), CHK-02 (Required documents coverage, completeness/error), CHK-03 (Per-person document verification, completeness/error) — matches the source `Validation_Plan`.
- Pins `proposal-document-completeness-udm@0.1.0`.
