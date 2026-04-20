# Input Source — Vandalizer Trial, FAIN 2511003

**Award Number (FAIN):** 2511003
**Project:** Equipment: MRI: Track 1 Acquisition of Element AVITI System to Enable Multi-Omics Research and Research Training.
**Sponsor:** National Science Foundation (DBI / BIO)
**Program:** NSF 23-519 Major Research Instrumentation Program
**Award date:** 2025-08-18
**Period of performance:** 2025-09-15 through 2028-08-31
**Recipient:** Regents of the University of Idaho (per Principal Investigator Organization)
**PI:** Sarah Hendricks (shendricks@uidaho.edu)
**Co-PIs:** Barrie Robison, Paul A Hohenlohe, Diana Mitchell (all at University of Idaho)

## Upstream extractor

- **Extractor:** Vandalizer (University of Idaho NSF-notice extraction tool)
- **Extraction run:** "NSF Extract Trial", 2026-04-20
- **Source filename:** `extraction-NSF Extract Trial-2026-04-20.json`
- **Upstream source document:** the NSF Award Notice PDF for FAIN 2511003 (not committed; this case tests translation from Vandalizer output, not direct PDF extraction).

The Vandalizer input used for this case is committed verbatim as [`input.json`](input.json). Running the Vandalizer extraction itself is out of scope for this component — we validate that given a specific Vandalizer output, our translator produces a specific UDM object.

## Runtime inputs assumed by expected.json

The eval harness is expected to pass these runtime hints to the translator so that `source_provenance` in `expected.json` is deterministic:

- `source_document`: `"extraction-NSF Extract Trial-2026-04-20.json"`
- `extracted_at`: `null` (no clock supplied)
- `upstream_extractor_version`: `null` (Vandalizer does not surface a version in its output)

## Known characteristics preserved in `expected.json`

- **Amendment metadata defaulted.** Vandalizer does not capture amendment fields. Translator emits `amendment_number = "000"` and `null` for `amendment_type`, `amendment_date`, `amendment_description`, `proposal_number`, and `award_received_date`.
- **Recipient contact fields null.** `legal_name` comes from `Principal Investigator Organization`; `address`, `email`, `uei` are all null.
- **No subaward inferred.** All four listed investigators are at the recipient institution, and the `G.Subawards` line is `$0`. Both inference conditions fail, so `subawards = []`.
- **All NSF sponsor contacts absent.** The Vandalizer output carries `"N/A"` for every managing-grants-official, awarding-official, and program-officer field. `sponsor_contacts = []`.
- **All three cited authorities absent.** `terms_and_conditions = []` (Vandalizer `"N/A"` for Authority Act, Research Terms and Conditions Date, NSF Agency Specific Requirements Date).
- **Indirect cost rate present, base absent.** Vandalizer extracts the rate (`50.0000%`) but not the named base; `Modified Total Direct Costs` is `"N/A"`. Translator emits `indirect_cost_rate_percent = 50.0` and `indirect_cost_base = null`.
- **Equipment-dominated budget.** Only line D has a non-trivial non-zero value (`$538,813`). Several B-subcategories have stated zero counts and amounts and emit as `0` (not skipped). Senior Personnel, Post Doctoral Scholars, and Other Professionals are all `"N/A"` and are skipped entirely.
- **Fees row present and zero.** Vandalizer `Fees: "$0"` emits as the top-level `fees` scalar = `0` (requires UDM schema v1.1.0). No corresponding `budget_categories` entry.
- **Yellow-highlight annotation absent.** Vandalizer `"what data was highlighted yellow in the original document?": "N/A"` — `source_provenance.review_annotations = []`.
