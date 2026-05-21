# Changelog

All notable changes to this workflow. Versions follow semver: MAJOR for step-structure changes, MINOR for additive changes (e.g., new search_set_items, validation checks), PATCH for display-name or wording edits.

## [0.1.0] — 2026-05-20

- Initial experimental release.
- Two-step runtime mirroring the source `budget-justification-generator` v2 workflow in `ui-insight/ProcessMapping`: four parallel Extraction tasks (each extracting structured budget data AND generating professional narrative text for its assigned R&R Budget / SF-424A sections) with embedded SearchSets, plus a Consolidation Prompt that assembles the four JSON fragments, computes the four arithmetic checks, and renders `final_justification_document` as a single Markdown string.
- Drafting workflow — the workflow's primary deliverable is generated narrative text rather than extracted structured data; the schema captures both the structured budget data (for arithmetic verification) and the narrative strings (for human review).
- Monetary structured-data fields typed as JSON numbers, not quoted strings: every total, every line-item cost, every rate. `fa_rate_percentage` is a JSON number (0-100), not the string `"56.5%"`. Narrative text preserves `$X,XXX.XX` format. Applies the boss's PR #33 review feedback consistently.
- Validation plan carries CHK-01..CHK-03 — matches the source `Validation_Plan` with field-target paths updated to reflect the schema's seven-block shape.
- Source `Cross_Field_Rules` (CFR-01 `total_direct + total_indirect = total_project`) enforced by the Consolidation Prompt's arithmetic-check generation; surfaces as a `status: "FAIL"` entry in `cross_validation.arithmetic_checks` when violated, without altering the budget form's numbers.
- Pins `budget-justification-generator-udm@0.1.0`.
