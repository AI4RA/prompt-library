# Vandalizer → UDM NSF Award Notice Translation

Converts a Vandalizer NSF-extraction JSON object (flat key/value form) into a single JSON object conforming to the `nsf-award-notice-extraction-udm` schema. This is a pure transformation — no information is invented, and fields Vandalizer does not capture emit as `null` or documented defaults.

**Current version:** 0.1.0
**Category:** transformation
**Domain:** research-administration
**Status:** experimental
**Manifestations:** prompt
**Output contract:** validates against [`../nsf-award-notice-extraction-udm/schema.json`](../nsf-award-notice-extraction-udm/schema.json) (v1.1.0)

## Inputs

One JSON object produced by the Vandalizer NSF extraction task. Shape:

- Flat, single-level key/value — all values are strings.
- Standard Vandalizer convention: `"N/A"` denotes absent values.
- US-format dates (`MM/DD/YYYY`), currency with `$` and commas (`"$584,845"`), percentages with `%` (`"50.0000%"`), semicolon-delimited lists for multi-value fields (Co-PI names/emails/organizations).
- Flat NSF-format budget line items keyed by label (`Senior Personnel Amount`, `Post Doctoral Scholars Count`, etc.), mirroring the 18-category table.
- A trailing review-metadata field: `"what data was highlighted yellow in the original document?"`.

See [`evals/cases/vandalizer-trial-2511003/`](evals/cases/vandalizer-trial-2511003/) for the seed input.

## Outputs

A single JSON object conforming to `nsf-award-notice-extraction-udm` v1.1.0. See [`prompt.md`](prompt.md) for the field-by-field translation rules.

## Scope and non-scope

**In scope.** Deterministic field-by-field translation. Format normalization (ISO dates, plain currency, plain percents, typed booleans). NSF-format budget line → UDM `budget_categories` code/subcode assignment. Subaward inference using the UDM rule (Co-PI at non-recipient org + non-zero G.Subawards). Carrying the Vandalizer review-highlight annotation through `source_provenance.review_annotations`.

**Out of scope.** Re-extracting missing fields from the original PDF. Vandalizer does not capture amendment metadata (number, type, date, description), recipient address/UEI/email, proposal number, or the email header's received-date. The translator emits `null` / documented defaults for these and does not attempt to recover them. Downstream systems that need these fields should run the full `nsf-award-notice-extraction-udm` extractor on the PDF instead, or extend Vandalizer's output schema.

## Defaults and data-quality notes

- `amendment_number` is required by UDM but absent from Vandalizer output. Translator emits `"000"` (new project / initial obligation) by default. Do not deploy this translator against amendment notices without first adding amendment fields to Vandalizer.
- `recipient_organization.legal_name` is taken from `Principal Investigator Organization`. Address, email, and UEI are always `null`. Ingest consumers should treat recipient records produced by this translator as needing enrichment from a separate organization-resolution step.
- `subawards` entries are always `inferred: true` (Vandalizer never itemizes subrecipients).
- `linked_awards` is always `[]`.
- `fees` is populated from Vandalizer's `Fees` field (schema v1.1.0 scalar).
- `source_provenance.extractor = "vandalizer-to-udm-translation"`, `upstream_extractor = "Vandalizer"`. The Vandalizer's `"what data was highlighted yellow in the original document?"` field, when not `"N/A"`, is emitted as a `review_annotations` entry with `label: "highlighted-yellow"`.

## Relationship to other components

| Concern | `nsf-award-notice-extraction-udm` | `vandalizer-to-udm-translation` |
| --- | --- | --- |
| Input | NSF Award Notice PDF (or pasted text) | Vandalizer flat-JSON extraction output |
| Category | extraction | transformation |
| Output schema | owns it | conforms to it |
| Field coverage | Full UDM contract | Subset — amendment metadata, recipient contact info, received-date all null |
| Subaward entries | explicit or inferred | always inferred |

## Manifestations

- [`prompt.md`](prompt.md) — canonical, LLM-agnostic prompt

## Evals

See [`evals/cases/vandalizer-trial-2511003/`](evals/cases/vandalizer-trial-2511003/) for the seed case — FAIN 2511003 (MRI: Track 1 AVITI System), a Vandalizer extraction of an NSF Standard Grant Amendment 000 notice from 2025.

## Provenance

Authored 2026-04-20 in response to a trial Vandalizer extraction produced against an NSF-26-508-era award notice at the University of Idaho. The schema v1.1.0 bump (`fees`, `source_provenance`) was driven by gaps surfaced during the initial translator spec review.
