# Changelog — solicitation-doc-modifications-udm

All notable changes to this component. Versions follow semver: MAJOR for output-contract breaks (schema changes that drop or rename fields, or remove / rename vocabulary codes), MINOR for backward-compatible additions (new vocabulary codes, new optional fields, new manifestations), PATCH for wording or clarity with no behavior change expected.

The `schema.json` version is kept in lockstep with the component version. The controlled `code` vocabulary is shared with `sponsor-doc-defaults-udm`; vocabulary changes must be coordinated across both components.

## [1.0.0] — 2026-04-19

- Initial version.
- JSON Schema (`schema.json`) defining a single output object with `sponsor_name`, `sponsor_division`, `solicitation_id`, `solicitation_notes`, and a `document_requirements` array. Each requirement object extends the `sponsor-doc-defaults-udm` requirement shape with `modifies_default` (nullable code) and `source_excerpt` (verbatim solicitation text).
- Diff-only output semantics: defaults the solicitation leaves unchanged are not echoed back; downstream merging treats absent codes as pass-through.
- Controlled 29-code vocabulary shared with `sponsor-doc-defaults-udm`, `document-type-classifier-udm`, and (when introduced) `proposal-completeness-review-udm`.
- Canonical prompt (`prompt.md`) defining what counts as a modification, what counts as net-new, verbatim-grounding requirements, and the empty-output case.
- Claude Skill manifestation (`skill/SKILL.md`) tuned for "what does this solicitation change or add beyond the sponsor defaults?" triggers.
- Three golden eval cases: modify-only, net-new-only, and a case that exercises both shapes.
