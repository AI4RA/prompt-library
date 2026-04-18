# Changelog — nsf-award-notice-extraction-udm

All notable changes to this component. Versions follow semver: MAJOR for output-contract breaks (schema changes that drop or rename fields), MINOR for backward-compatible additions (new optional fields, new enum values, new manifestations), PATCH for wording or clarity with no behavior change expected.

The `schema.json` version is kept in lockstep with the component version.

## [1.0.0] — 2026-04-18

- Initial version.
- JSON Schema (`schema.json`) covering identity scalars, dates and funding, nested `recipient_organization` and `current_budget_period`, and eight categorized arrays (project personnel, sponsor contacts, NSF-format budget categories A–M, subawards, linked awards, terms and conditions, special conditions).
- Canonical prompt (`prompt.md`) including the Amendment 000 vs. subsequent-amendment distinction, NSF-format budget line subcoding, and an explicit subaward inference rule for notices where Co-PIs at non-recipient institutions imply subrecipient arrangements not individually itemized in the notice.
- Claude Skill manifestation (`skill/SKILL.md`) tuned for NSF NOA / award letter / award notice triggers.
- First golden eval case: FAIN 2427549 — Standard Grant, Amendment 000, single prime (University of Idaho) with an inferred subaward to a Co-PI at Southern Utah University, exercising the subaward inference rule and the NSF-format budget table capture.
