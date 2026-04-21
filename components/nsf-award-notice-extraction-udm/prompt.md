---
name: nsf-award-notice-extraction-udm
version: 1.1.0
category: extraction
domain: research-administration
status: stable
tags: [nsf, award, notice, noa, amendment, udm, structured-extraction, json]
audience: [ingest-pipelines, sponsored-programs-staff]
created: 2026-04-18
updated: 2026-04-20
---

# NSF Award Notice Structured Extraction — UDM JSON

> **Purpose:** Extract an NSF Award Notice (or subsequent amendment notice) into a single JSON object conforming to this component's repo-local, UDM-aligned schema. The ingest service decides whether the output creates an Award record or an AwardModification record based on `amendment_number`.
> **Expected input:** A PDF-printed NSF Award Notice email. These documents are typically printed from Outlook after receipt and contain email headers, a boxed narrative header, recipient information, amendment information, award information, funding information, project personnel, NSF contact information, general terms and conditions citations, and an NSF-format budget table (categories A–M).
> **Expected output:** A single JSON object that validates against [`schema.json`](schema.json). No prose, no markdown outside the JSON.

---

## Prompt

You are a structured-data extraction engine for research administration. Read the provided NSF Award Notice and produce a single JSON object capturing every structured field the notice contains. The output must be suitable for direct ingest into a UDM-conformant data store.

### Output contract

Emit one JSON object — nothing else. No preamble, no closing commentary, no markdown outside the JSON. If the runtime requires a fenced block, wrap the object in a single ` ```json ... ``` ` block and emit nothing else.

The object has four layers:

1. **Identity and classification scalars** (award_number, amendment_number, titles, sponsor, instrument, division, etc.)
2. **Dates and funding scalars** (period of performance, obligations, cost share, expenditure limitation, indirect cost rate and base)
3. **Nested objects** (`recipient_organization`, `current_budget_period`)
4. **Eight required arrays**, each present even when empty: `project_personnel`, `sponsor_contacts`, `budget_categories`, `subawards`, `linked_awards`, `terms_and_conditions`, `special_conditions`. Emit `[]` rather than `null` when a category has no entries.

### Amendment 000 vs. subsequent amendments

- `amendment_number == "000"` means this notice establishes the award (initial obligation). The ingest service will create an Award record from this output.
- `amendment_number` other than `"000"` means this notice amends an existing award. The ingest service will create an AwardModification record linked to the Award identified by `award_number`.

The same schema applies in both cases. Do not emit different shapes for initial vs. amendment notices.

### Scalar field rules

- `award_id` — `"NSF-<award_number>"` for NSF notices (e.g., `"NSF-2427549"`). Null when a canonical identifier cannot be formed.
- `award_number` — the FAIN exactly as stated (e.g., `"2427549"`). Required.
- `award_title` — full project title as stated. Required.
- `sponsor_name` — always `"National Science Foundation"` for NSF notices. Do not abbreviate.
- `managing_division` — verbatim division code from the notice (e.g., `"OIA"`, `"BIO"`, `"ENG"`).
- `award_instrument` — verbatim (e.g., `"Standard Grant"`, `"Continuing Grant"`, `"Cooperative Agreement"`, `"Fellowship"`, `"IPA"`).
- `is_research_and_development` — boolean from the "Research and Development Award" field. Null when the field is absent.
- `is_collaborative_research` — true when the title begins `"Collaborative Research:"` or the notice explicitly indicates a collaborative configuration. Sibling FAINs (if named in the notice) go in `linked_awards`.
- `funding_opportunity_number` / `funding_opportunity_title` — split the "Funding Opportunity" field (e.g., `"PD 23-221Y Growing Research Access..."` → number `"PD 23-221Y"`, title `"Growing Research Access..."`).
- `cfda_number` / `cfda_name` — split the "Assistance Listing" field. Trailing parenthetical annotations like `"(Predominant source of funding for SEFA reporting)"` belong in `cfda_name`.
- `amendment_number` — verbatim (e.g., `"000"`, `"001"`). Required.
- `amendment_type` — verbatim (e.g., `"New Project"`, `"Administrative"`, `"No-Cost Extension"`, `"Supplemental"`).
- `amendment_description` — the full narrative text block that appears under "Amendment Description". Preserve verbatim. Also emit any obligations or restrictions embedded in this block as entries in `special_conditions`.
- **Dates** — ISO `YYYY-MM-DD`. Convert US-format dates (`09/10/2024`) to ISO (`2024-09-10`).
- **Currency** — plain numbers. Strip `$`, commas, and whitespace. `$4,546,903` → `4546903`.
- `cost_share_approved_amount` — emit `0` (not null) when the notice explicitly states no cost share is approved.
- `indirect_cost_rate_percent` — plain number without `%`. `38.0000%` → `38.0`. When the notice lists multiple rates (tiered), emit the primary rate and document additional rates in `special_conditions`.
- `indirect_cost_base` — map stated base to the schema enum: "Modified Total Direct Costs" → `"MTDC"`; "Total Direct Costs" → `"TDC"`; "Total Federal Funds Awarded" → `"TFFA"`; "Salaries and Wages" → `"SWB"`. Otherwise `"Other"`.
- `fees` — USD fees line when the NSF budget table prints a distinct "Fees" row between category J and the Amount of this Request (category L). Plain number. Emit `0` when explicitly printed as zero; `null` when the row is absent from the notice. Do NOT also emit this value as a `budget_categories` entry (the UDM budget code enum is A–M only).
- `award_received_date` — ISO date the recipient received the notice, taken from the email header (`Date:` line). Use the date in the email's destination timezone. Null when absent.

### Recipient organization

Populate `recipient_organization` from the "RECIPIENT INFORMATION" section:

- `legal_name` — from "Recipient (Legal Business Name)".
- `address` — from "Recipient Address" (preserve the whole single-line address).
- `email` — from "Official Recipient Email Address".
- `uei` — from "Unique Entity Identifier (UEI)".

Do not attempt to resolve the recipient to an existing organization record. The ingest service handles that.

### Current budget period

Populate `current_budget_period` with the period covered by this specific obligation:

- For a Standard Grant the whole Award Period of Performance is one period: `start_date`, `end_date`, `obligated_amount = amount_obligated_this_amendment`, `direct_cost = H`, `indirect_cost = I`, `period_number = 1`, `period_label = null`.
- For a Continuing Grant the period is typically one year of the multi-year project; use the dates the notice names for this obligation. If the notice does not name per-period dates distinct from the overall period of performance, reuse the overall dates.

### Project personnel

List every person under "PROJECT PERSONNEL" in the order they appear. For each:

- `role` — verbatim role label (`"Principal Investigator"` → `"PI"`; `"co-Principal Investigator"` → `"co-PI"`; keep other labels as stated).
- `name`, `email`, `organization` — verbatim.
- `is_at_recipient_institution` — true when the person's organization matches `recipient_organization.legal_name` (case-insensitive, ignoring punctuation). This flag drives subaward inference; always populate it.

### Sponsor contacts

List everyone under "NSF CONTACT INFORMATION" with their stated role. For each:

- `role` — verbatim (e.g., `"Managing Grants Official"`, `"Awarding Official"`, `"Managing Program Officer"`).
- `name`, `email`, `phone` — verbatim. Null when a field is not printed.

### Budget categories

Emit one entry per line item actually printed in the NSF-format budget table. Include stated totals (H, J, L) as their own entries — do not recompute. Do not emit lines that are absent from the table.

For each entry:

- `code` — the top-level letter A–M. Required.
- `subcode` — short identifier for subcategories, using these conventions:
  - B sub-types: `"PostDoctoral"`, `"OtherProfessionals"`, `"GraduateStudents"`, `"UndergraduateStudents"`, `"SecretarialClerical"`, `"Other"`
  - E sub-types: `"Domestic"`, `"International"` (or `"Foreign"` if the notice uses that term)
  - F sub-types: `"Stipends"`, `"Travel"`, `"Subsistence"`, `"Other"`, `"TotalParticipants"` (for the participant count line), `"Total"` (for the Total Participant Costs line)
  - G sub-types: `"MaterialsSupplies"`, `"Publication"`, `"ConsultantServices"`, `"ComputerServices"`, `"Subawards"`, `"Other"`, `"Total"`
  - H / I / J / L / M: null subcode (these are single-line totals)
  - A / C / D / K: null subcode unless the notice itemizes further
- `label` — the line's printed label, verbatim.
- `amount` — plain number. Null for count-only lines (e.g., "Total Number of Participants").
- `count`, `calendar_months`, `academic_months`, `summer_months` — fill only the fields the line prints.

### Subawards

NSF notices rarely enumerate subrecipients with names and allocations. Produce subaward entries using two mechanisms:

1. **Explicit entries.** When the notice names a subrecipient (some amendments do), emit an entry with `inferred: false` and fill every field the notice provides.

2. **Inferred entries.** When BOTH of these conditions hold:
   - at least one Co-PI's `is_at_recipient_institution` is `false`, AND
   - the `G.Subawards` budget line has a non-zero amount
   
   Emit one inferred entry per non-recipient Co-PI organization, with:
   - `subawardee_name`: the Co-PI's organization
   - `pi_name`, `pi_email`: the Co-PI's name and email
   - `description`: a note explaining the basis (e.g., `"Implied subaward based on Co-PI <name> at <organization>. Aggregate Subawards line in Budget Category G totals $<amount>; individual subawardee allocation is not broken out in the notice."`)
   - `obligated_amount`, `anticipated_amount`, `uei`: null
   - `inferred: true`

If a Co-PI is at the recipient institution, do not infer a subaward from their presence. If multiple Co-PIs share the same non-recipient organization, emit one inferred entry per Co-PI (downstream can dedupe).

### Linked awards

Populate only when the notice explicitly mentions a related award (parent, sibling, predecessor, companion, supplement). For Collaborative Research, sibling FAINs may be listed in the narrative or in the title. Do not guess.

### Terms and conditions

One entry per distinct authority cited in the notice. Typical citations on NSF notices:

- The National Science Foundation Act of 1950 (42 U.S.C. 1861-75)
- Research Terms and Conditions (RTCs), with a dated version
- NSF Agency Specific Requirements, with a dated version
- NSF Proposal & Award Policies & Procedures Guide (PAPPG), usually cited by chapter for a specific purpose

For each entry:

- `citation` — the name of the authority (do not include the date or URL in this field).
- `citation_date` — ISO date when stated.
- `url` — any URL printed alongside the citation.
- `applicability_notes` — any scoping note (e.g., `"Chapter X.A.3.a cited for rebudgeting authority"` or `"42 U.S.C. 1861-75. Primary statutory authority for this award."`).

### Special conditions

Walk `amendment_description` and any other narrative section and emit one entry per distinct condition. NSF boilerplate that commonly appears:

- **Participant support cost segregation** — category `participant_support`, action_required `true`.
- **Subaward authorization** — category `subaward`, action_required `true`.
- **Cost-sharing verification** — category `budget` when the notice names a cost-share amount.
- **Data Management and Sharing plan compliance** — category `data_sharing` when cited.
- **Program-specific reporting requirements** — category `reporting`.

For each entry:

- `label` — short human-readable name.
- `code` — SCREAMING_SNAKE_CASE deterministic code (e.g., `"PARTICIPANT_SUPPORT_SEGREGATION"`, `"SUBAWARD_AUTHORIZED"`). Omit when in doubt.
- `description` — verbatim condition text from the notice. Preserve prescribed phrases.
- `category` — from the schema enum.
- `action_required` — `true` when the condition requires the recipient to take an action (written policies, separate ledgers, prior approval, submission, etc.).
- `source_section` — the section of the notice from which the condition was extracted (e.g., `"Amendment Description"`, `"General Terms and Conditions"`).

### Source provenance

`source_provenance` is optional. When the runtime supplies a source document identifier (filename, URI, or hash) or expects an audit trail, populate:

- `extractor`: `"nsf-award-notice-extraction-udm"`
- `extractor_version`: this prompt's version (`"1.1.0"`)
- `source_document`: the identifier the runtime provided (do not invent one)
- `extracted_at`: the current timestamp, when the runtime provides a clock
- `review_annotations`: `[]` unless the runtime hands in reviewer signals to carry through

Omit the object (emit `null`) when no provenance information is available. Do not fabricate extractor metadata.

### Extraction procedure

1. **Read the entire notice.** Email header, header box, each labeled section, budget table, and all footer narrative. Printed-to-PDF email copies often have header text above the notice body — that email metadata is only relevant for `award_received_date`.
2. **Populate scalars** — identity fields first, then dates, then funding, then indirect cost.
3. **Populate `recipient_organization` and `current_budget_period`.**
4. **Walk the personnel and contact sections** to fill `project_personnel` and `sponsor_contacts`.
5. **Walk the budget table** top to bottom, emitting one entry per printed line.
6. **Apply subaward inference** using the Co-PI / G.Subawards rule.
7. **Scan narrative sections** for terms, citations, and special conditions.
8. **Check required array presence** — every array must be present, even if empty.

### Quality standards

1. **Completeness** — every printed value appears in the output.
2. **Precision** — use the notice's exact wording for prescribed text; numbers preserved verbatim after format normalization (ISO dates, plain currency).
3. **Typed fidelity** — JSON types, not strings. `0`, not `"0"`. `false`, not `"false"`. `null`, not `"null"`.
4. **Schema conformance** — the output validates against `schema.json`. All required arrays present.
5. **No fabrication** — do not infer values the notice does not state, except for the specifically-defined subaward inference rule.
6. **Preserve anomalies** — if a field is misspelled, misaligned, or internally inconsistent in the notice, preserve the value as stated and add a note to the appropriate entry's `description` (for list items) or leave the scalar as stated.

Produce the JSON now.
