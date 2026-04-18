# Changelog — rfp-extraction-udm

All notable changes to this component. Versions follow semver: MAJOR for output-contract breaks (schema changes that drop or rename fields, or change array semantics), MINOR for backward-compatible additions (new optional fields, new structured rule types, new manifestations), PATCH for wording or clarity with no behavior change expected.

The `schema.json` version is kept in lockstep with the component version.

## [1.0.0] — 2026-04-18

- Initial version.
- JSON Schema (`schema.json`) defining the flat output: 18 scalar opportunity fields plus nine categorized requirement arrays, each holding a shared requirement-entry shape.
- Canonical prompt (`prompt.md`) covering date/currency/duration normalization, multi-round deadline handling, parent-guide inheritance, "no restriction" confirmations, and structured rule encodings.
- Claude Skill manifestation (`skill/SKILL.md`) with a description tuned for skill-router matching on machine-readable extraction intents.
- First golden eval case: NSF 26-508 (TechAccess) — `expected.json` covering multi-round scheduling, LOI requirements, per-institution proposal limit, cost-sharing prohibition, five mandated project-description section headers, five solicitation-specific review criteria, and four parent-guide deviations.
