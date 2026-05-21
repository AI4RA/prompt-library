# Changelog

All notable changes to this workflow. Versions follow semver: MAJOR for step-structure changes, MINOR for additive changes (e.g., new search_set_items, validation checks), PATCH for display-name or wording edits.

## [0.1.0] — 2026-05-20

- Initial experimental release.
- Two-step runtime mirroring the source `risk-domain-assessment` v2 workflow in `ui-insight/ProcessMapping`: six parallel Extraction tasks each covering 2–4 of the 14 risk domains (Task 1: Domains 1+9; Task 2: 2+8; Task 3: 3+13; Task 4: 4+5; Task 5: 6+7; Task 6: 10+11+12+14), plus a Consolidation Prompt that assembles the six JSON fragments into a single schema-conformant object, computes `aggregate_metrics` deterministically, and derives the `high_risk_domains` / `key_risk_findings` / `recommended_mitigations` arrays from the per-domain scores and justifications.
- All 14 domain scores typed as JSON integers in `[1, 5]`. `aggregate_metrics.total_risk_score` as JSON integer in `[14, 70]`. `aggregate_metrics.average_risk_score` as JSON number in `[1.0, 5.0]`. Applies the boss's PR #33 number-vs-string review feedback to all scoring fields.
- `aggregate_metrics.overall_risk_level` exposed as the four-value enum (`Low`, `Moderate`, `High`, `Very High`) per the source workflow's rubric language.
- Validation plan carries CHK-01..CHK-03 — matches the source `Validation_Plan` with field-target paths updated to the schema's three-block shape.
- Source `Cross_Field_Rules` (CFR-01 `justification not empty when score >= 3`) enforced by `minLength: 1` on every domain block's `justification` plus the Consolidation Prompt's FLAG path for generic justifications on high-score domains.
- Pins `risk-domain-assessment-udm@0.1.0`.
