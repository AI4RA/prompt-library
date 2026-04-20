# Changelog — vandalizer-to-udm-translation

All notable changes to this component. Versions follow semver: MAJOR for output-contract breaks, MINOR for backward-compatible additions, PATCH for wording or clarity with no behavior change expected.

This component conforms to (does not own) `nsf-award-notice-extraction-udm/schema.json`. When that schema's version changes, bump this component's version in the same PR.

## [0.1.0] — 2026-04-20

- Initial version.
- Canonical prompt (`prompt.md`) translating Vandalizer flat-JSON NSF extractions to UDM v1.1.0 output.
- Deterministic field-by-field mapping with documented defaults for fields Vandalizer does not capture (`amendment_number` defaults to `"000"`; amendment type/date/description, recipient address/UEI/email, proposal number, and received-date emit `null`).
- NSF-format budget mapping table covering categories A through M, including B/E/F/G subcategories and the explicit skip of form rollups (`Total Salaries And Wages`, `Total Salaries Wages Fringe Benefits`).
- `fees` scalar populated from Vandalizer's `Fees` field (requires schema v1.1.0).
- `source_provenance` always emitted, with `upstream_extractor = "Vandalizer"` and a `review_annotations` entry for the Vandalizer yellow-highlight field when present.
- Subaward inference: always `inferred: true`, since Vandalizer never enumerates subrecipients.
- `linked_awards` and `special_conditions` always `[]` — Vandalizer does not capture them.
- First eval case: `vandalizer-trial-2511003` — MRI Track 1 AVITI System acquisition, Standard Grant, new-project obligation, Co-PI configuration at a single institution.
