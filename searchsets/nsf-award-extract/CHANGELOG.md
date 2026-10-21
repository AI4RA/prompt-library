# NSFAwardExtract search-set changelog

Search-set versions are independent of component, fieldmap, and export-format versions.

## 0.2.0 — 2026-10-21

- Preserve the original `NSFAwardExtract 1021.vandalizer.json` export byte for byte
  under `versions/0.2.0/nsf-award-extract.vandalizer.json`.
- Add four required fields: ORCID Number, Graduate Student Full Name, PI SSN,
  and University Mascot (92 → 96 fields). Existing searchphrases, optional flags,
  enums, and relative field order are unchanged.
- Record model `moonshotai/kimi-k3`; retain structured one-pass extraction and
  enabled key chunking with `max_keys: 20`.
- Capture the title `NSFAwardExtract 1021` and schema-v2 export envelope. Items
  carry `searchtype: extraction`; the export omits baseline database item IDs
  and the search-set UUID. No identity continuity is asserted from those IDs.
- Add a version index with provenance and SHA256 hashes. No test cases accompany
  this export; no evaluation results or mappings for the four new fields are added.

## 0.1.0 — baseline captured 2026-06-11

- Retrospectively assign version 0.1.0 on 2026-10-21 to the existing 92-field
  validation-setup capture, leaving the original file unchanged.
- Retain the original search-set UUID and fieldmap v0.1.0 targeting
  `nsf-award-notice-extraction-udm` v1.1.0. No model was recorded in the capture.
