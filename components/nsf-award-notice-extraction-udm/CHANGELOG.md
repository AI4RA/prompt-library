# Changelog — nsf-award-notice-extraction-udm

All notable changes to this component. Versions follow semver: MAJOR for output-contract breaks (schema changes that drop or rename fields), MINOR for backward-compatible additions (new optional fields, new enum values, new manifestations), PATCH for wording or clarity with no behavior change expected.

The `schema.json` version is kept in lockstep with the component version.

## [1.1.0] — 2026-04-20

- Added top-level optional `fees` scalar (USD, nullable) to cover NSF budget tables that print a distinct Fees row between category J and the Amount of this Request (category L). Previously callers had to either widen the `budget_categories.code` regex (which would break schema consumers) or hide the value inside `special_conditions`. The `budget_categories.code` enum remains `^[A-M]$`; Fees is now a first-class sibling scalar instead.
- Added optional `source_provenance` object carrying `extractor`, `extractor_version`, `source_document`, `upstream_extractor`, `upstream_extractor_version`, `extracted_at`, `review_annotations[]`, and `notes`. Enables audit trails for both direct extractors and translators that convert upstream extractor output into this UDM shape. `review_annotations` items carry `label`, `value`, `target_field`, and `description` so reviewer signals (e.g., "highlighted yellow in source") survive translation without a fixed taxonomy.
- Updated `prompt.md` and `skill/SKILL.md` with extraction rules for both new fields. Extractors populate `source_provenance` only when the runtime provides a source document id or timestamp — no fabrication.
- Backward-compatible. Consumers reading 1.0.0 output will see no missing required fields; consumers targeting 1.1.0 should treat `fees` and `source_provenance` as optional.
- Driven by the `vandalizer-to-udm-translation` translator (v0.1.0) that converts flat Vandalizer NSF extractions into this UDM shape. The Vandalizer output carries a `Fees` field and a reviewer-highlight annotation that neither fit cleanly under the 1.0.0 contract.

## [1.0.0] — 2026-04-18

- Initial version.
- JSON Schema (`schema.json`) covering identity scalars, dates and funding, nested `recipient_organization` and `current_budget_period`, and eight categorized arrays (project personnel, sponsor contacts, NSF-format budget categories A–M, subawards, linked awards, terms and conditions, special conditions).
- Canonical prompt (`prompt.md`) including the Amendment 000 vs. subsequent-amendment distinction, NSF-format budget line subcoding, and an explicit subaward inference rule for notices where Co-PIs at non-recipient institutions imply subrecipient arrangements not individually itemized in the notice.
- Claude Skill manifestation (`skill/SKILL.md`) tuned for NSF NOA / award letter / award notice triggers.
- First golden eval case: FAIN 2427549 — Standard Grant, Amendment 000, single prime (University of Idaho) with an inferred subaward to a Co-PI at Southern Utah University, exercising the subaward inference rule and the NSF-format budget table capture.
