# NSF Award Notice Extraction — UDM JSON

Extracts an NSF Award Notice (initial obligation or amendment) into a single JSON object conforming to this repo's UDM-aligned extraction contract. Designed for the NSF notice format that arrives as a PDF printed from Outlook after OSP receipt — the email header, boxed notice body, and NSF-format 18-category budget table.

**Current version:** 1.1.0
**Category:** extraction
**Domain:** research-administration
**Status:** stable
**Manifestations:** prompt, skill
**Output contract:** see [`schema.json`](schema.json)

## Inputs

A PDF (or pasted text) of an NSF Award Notice. Typical structure:

- Email header (`Subject`, `Date`, `From`, `To`, `CC`)
- "NATIONAL SCIENCE FOUNDATION — Award Notice" boxed header with Award Number (FAIN) and Amendment Number
- Recipient Information (legal name, address, email, UEI)
- Amendment Information (type, date, number, proposal number, narrative description)
- Award Information (instrument, dates, title, managing division, R&D flag, funding opportunity, assistance listing)
- Funding Information (amount obligated, total intended, cost share, total to date, expenditure limitation)
- Project Personnel (PI and Co-PIs, each with email and organization)
- NSF Contact Information (managing grants official, awarding official, program officer)
- General Terms and Conditions (citations to the NSF Act, RTCs, Agency Specific Requirements, PAPPG)
- Budget table in NSF-format (categories A–M plus subcategories)
- Indirect Cost Rate table (rate + base)

## Outputs

A single JSON object with:

- **Identity scalars** — award number, title, sponsor, managing division, instrument, amendment info, funding opportunity, CFDA
- **Date and funding scalars** — period of performance, obligations, cost share, indirect cost rate and base, `fees`
- **Nested objects** — `recipient_organization`, `current_budget_period`, optional `source_provenance`
- **Eight arrays** (always present; `[]` when empty) — `project_personnel`, `sponsor_contacts`, `budget_categories`, `subawards`, `linked_awards`, `terms_and_conditions`, `special_conditions`

See [`schema.json`](schema.json) for the authoritative definition and [`prompt.md`](prompt.md) for the extraction rules the prompt follows. This schema is repo-local and UDM-aligned; it is not a copy of the canonical shared UDM repo schema.

## Amendment 000 vs. subsequent amendments

The same schema covers both. `amendment_number == "000"` indicates an initial obligation (the ingest service creates an Award record); other values indicate modifications (the ingest service creates an AwardModification record linked to the Award named by `award_number`).

## Subaward inference

NSF notices rarely itemize subrecipients. The extractor infers a subaward entry when a Co-PI's organization differs from the recipient AND the budget shows a non-zero Subawards line in category G; inferred entries carry `inferred: true` and leave amounts null. Explicit subrecipient enumerations (uncommon but possible in amendments) are emitted with `inferred: false` and all provided fields populated. See [`prompt.md`](prompt.md) for the precise rule.

## Collaborative Research

Detected heuristically from the title prefix `"Collaborative Research:"` and/or explicit narrative. Sibling FAINs, when named in the notice, go in `linked_awards` with `relationship: "collaborative_sibling"`.

## Manifestations

- [`prompt.md`](prompt.md) — canonical, LLM-agnostic prompt
- [`skill/SKILL.md`](skill/SKILL.md) — Claude Skill form

## Schema

[`schema.json`](schema.json) is a JSON Schema (draft 2020-12) defining the full output contract. Validates with any conforming validator; downstream ingest pipelines should gate on this schema.

## Relationship to other components

| Concern | `rfp-extraction-udm` | `nsf-award-notice-extraction-udm` |
| --- | --- | --- |
| Input | Funding announcement (pre-award) | Award notice (post-award) |
| Ingest target | RFA record | Award or AwardModification |
| Requirements | Nine categorized requirement arrays | Budget categories, terms, special conditions, etc. |
| Multi-round | Handled in `special_conditions` | Not applicable (one notice per amendment) |

## Evals

See [`evals/`](evals/) for reference inputs and known-good outputs. The initial case is FAIN 2427549 — a Standard Grant new-project notice to a single prime institution with an implied subaward to a Co-PI at a different institution, exercising the subaward inference rule.

## Provenance

Schema designed 2026-04-18 from the NSF Award Notice template as exemplified by FAIN 2427549 (Amendment 000, September 2024).
