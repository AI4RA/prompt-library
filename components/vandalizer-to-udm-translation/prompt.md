---
name: vandalizer-to-udm-translation
version: 0.1.0
category: transformation
domain: research-administration
status: experimental
tags: [nsf, award, notice, udm, translation, vandalizer, structured-transformation, json]
audience: [ingest-pipelines, sponsored-programs-staff]
created: 2026-04-20
updated: 2026-04-20
---

# Vandalizer → UDM NSF Award Notice Translation — Prompt

> **Purpose:** Convert a Vandalizer NSF-extraction JSON object (flat key/value form) into a single JSON object conforming to the `nsf-award-notice-extraction-udm` schema v1.1.0. This is a pure transformation — no information is invented, and fields Vandalizer does not capture emit as `null` or documented defaults.
> **Expected input:** One JSON object produced by the Vandalizer NSF extraction task (flat, string-valued fields; `"N/A"` used for missing values).
> **Expected output:** One JSON object validating against [`schema.json`](schema.json), which delegates to `nsf-award-notice-extraction-udm` v1.1.0. No prose, no markdown outside the JSON.

---

## Prompt

You are a deterministic translator. Read one Vandalizer NSF extraction object and emit one UDM NSF Award Notice JSON object. Do not paraphrase, re-order, or summarize; map field by field using the rules below. The same input must always produce the same output.

### Output contract

Emit one JSON object. No preamble, no trailing commentary. If the runtime requires a fenced block, wrap the object in a single ` ```json ... ``` ` block and emit nothing else. Every required UDM array (`project_personnel`, `sponsor_contacts`, `budget_categories`, `subawards`, `linked_awards`, `terms_and_conditions`, `special_conditions`) must be present; emit `[]` when empty.

### Normalization rules

- **Missing values.** Treat any Vandalizer value of `"N/A"`, `""`, or the literal string `"null"` (case-insensitive) as absent. Emit `null` for scalars and omit the would-be list item for arrays.
- **Currency.** Strip `$`, commas, whitespace. `"$584,845"` → `584845`. `"$0"` → `0` (not `null`).
- **Dates.** US `MM/DD/YYYY` → ISO `YYYY-MM-DD`. Missing → `null`.
- **Percent.** Strip `%`. `"50.0000%"` → `50.0`.
- **Booleans.** `"Yes"` → `true`, `"No"` → `false`, absent → `null`.
- **JSON types.** Emit `0` not `"0"`, `false` not `"false"`, `null` not `"null"`.

### Scalar mappings

- `award_number` ← `Award Number` (required; never null).
- `award_id` ← `"NSF-" + Award Number`.
- `sponsor_name` ← `"National Science Foundation"` (constant for this translator).
- `sponsor_award_number` ← `null` (Vandalizer does not distinguish it from `award_number`).
- `award_title` ← `Project Title`.
- `award_instrument` ← `Award Instrument`.
- `managing_division` ← `Managing Division Abbreviation`.
- `award_status` ← `null`.
- `is_research_and_development` ← `Research And Development Award` (Yes/No/absent).
- `is_collaborative_research` ← `true` iff `Project Title` starts with `"Collaborative Research:"` (case-insensitive), else `false`.
- `proposal_number` ← `null`.
- `award_date` ← `Award Date`.
- `award_received_date` ← `null` (Vandalizer does not capture the email header date).
- `start_date` ← `Award Period Start Date`.
- `end_date` ← `Award Period End Date`.
- `amount_obligated_this_amendment` ← `Amount Obligated By This Amendment`.
- `total_intended_amount` ← `Total Intended Award Amount`.
- `total_obligated_to_date` ← `Total Amount Obligated To Date`.
- `cost_share_approved_amount` ← `Total Approved Cost Share Or Matching Amount` (emit `0`, not `null`, when input is `"$0"`).
- `expenditure_limitation` ← `Expenditure Limitation`.
- `indirect_cost_rate_percent` ← `Indirect Cost Rate` (percent stripped).
- `indirect_cost_base` ← `"MTDC"` if `Modified Total Direct Costs` is a numeric amount (presence of the field as a number); otherwise `null`. The Vandalizer field names the base by way of being present; when it is `"N/A"` we cannot determine the base.
- `fees` ← `Fees` (currency stripped). `"$0"` → `0`; absent → `null`.

#### Funding Opportunity split
Tokenize `Funding Opportunity` on whitespace. The `funding_opportunity_number` is the sponsor-style prefix up through the first token that matches `^[A-Z0-9][A-Z0-9\-]*$` *after* a leading alpha prefix (in practice the first two tokens: `"NSF 23-519"`, `"PD 23-221Y"`). The remainder is the `funding_opportunity_title`; strip trailing punctuation (`:`, `.`).

- Example: `"NSF 23-519 Major Research Instrumentation Program:"` → number `"NSF 23-519"`, title `"Major Research Instrumentation Program"`.
- Example: `"PD 23-221Y Growing Research Access for Nationally Transformative Equity and Diversity"` → number `"PD 23-221Y"`, title `"Growing Research Access for Nationally Transformative Equity and Diversity"`.

If the input value does not match this pattern, emit the whole stripped string as `funding_opportunity_title` and `funding_opportunity_number` as `null`.

#### Assistance Listing split
Split `Assistance Listing Number And Name` on the first whitespace run following the leading dotted number (`^\d{2}\.\d{3}`). The number goes into `cfda_number`; the remainder, verbatim including any trailing parenthetical annotation, goes into `cfda_name`.

- Example: `"47.074 Biological Sciences (Predominant source of funding for SEFA reporting)"` → number `"47.074"`, name `"Biological Sciences (Predominant source of funding for SEFA reporting)"`.

### Amendment fields

Vandalizer does not capture amendment metadata. Emit the following defaults:

- `amendment_number` = `"000"` (required by UDM; represents initial obligation).
- `amendment_type` = `null`.
- `amendment_date` = `null`.
- `amendment_description` = `null`.

This default is correct for new-project notices. If a translator operator later determines the input represents an amendment, the `amendment_number` must be overridden out-of-band; this prompt does not infer amendment status.

### recipient_organization

- `legal_name` ← `Principal Investigator Organization`.
- `address`, `email`, `uei` ← `null` (Vandalizer does not extract these).

Fallback: if `Principal Investigator Organization` is absent, use the first semicolon-separated value of `Co Principal Investigator Organization`. If still absent, emit `legal_name` as `"UNKNOWN"` — the ingest service will surface this as a data-quality issue.

### current_budget_period

Populate from the scalars:

- `period_number` = `1`
- `period_label` = `null`
- `start_date` ← `Award Period Start Date`
- `end_date` ← `Award Period End Date`
- `direct_cost` ← `Total Direct Costs`
- `indirect_cost` ← `Indirect Costs`
- `obligated_amount` ← `Amount Obligated By This Amendment`

Emit `current_budget_period: null` only when `Award Period Start Date`, `Award Period End Date`, or `Amount Obligated By This Amendment` is absent (the UDM schema requires these three).

### project_personnel

Emit one entry for the PI when `Principal Investigator Name` is present:

```json
{"role": "PI", "name": <PI Name>, "email": <PI Email or null>, "organization": <PI Org or null>, "is_at_recipient_institution": true}
```

Then split `Co Principal Investigator Name`, `Co Principal Investigator Email`, and `Co Principal Investigator Organization` on `";"`, trim whitespace, and zip by index. Emit one `role: "co-PI"` entry per name.

- When there are fewer emails than names, the trailing entries get `email: null`.
- When there are fewer organizations than names (the common case — Vandalizer often collapses a shared recipient org into a single string), reuse the last organization string for all trailing entries.
- `is_at_recipient_institution`: `true` when the entry's `organization` equals `recipient_organization.legal_name` compared case-insensitively and stripped of punctuation; `false` otherwise.

### sponsor_contacts

For each of the three contact blocks, emit an entry only when Name is not absent:

- `Managing Grants Official Name` / `Email` / `Phone` → role `"Managing Grants Official"`
- `Awarding Official Name` / `Email` → role `"Awarding Official"` (phone: `null`)
- `Managing Program Officer Name` / `Email` / `Phone` → role `"Managing Program Officer"`

Emit `sponsor_contacts: []` when all three blocks are absent.

### budget_categories

Emit the following entries in this order, preserving `amount` as a number. Skip an entry only when ALL its source fields are absent (`"N/A"`); a stated `$0` or `0.00` is data and must be emitted as `0`.

| Source key(s) | code | subcode | label |
|---|---|---|---|
| `Senior Personnel Amount` (+ `Count`, `Calendar/Academic/Summer Months`) | `"A"` | `null` | `"Senior Personnel"` |
| `Post Doctoral Scholars Amount/Count/Months` | `"B"` | `"PostDoctoral"` | `"Post Doctoral Scholars"` |
| `Other Professionals Amount/Count/Months` | `"B"` | `"OtherProfessionals"` | `"Other Professionals"` |
| `Graduate Students Count/Amount` | `"B"` | `"GraduateStudents"` | `"Graduate Students"` |
| `Undergraduate Students Count/Amount` | `"B"` | `"UndergraduateStudents"` | `"Undergraduate Students"` |
| `Secretarial Clerical Count/Amount` | `"B"` | `"SecretarialClerical"` | `"Secretarial - Clerical"` |
| `Other Personnel Count/Amount` | `"B"` | `"Other"` | `"Other"` |
| `Fringe Benefits` | `"C"` | `null` | `"Fringe Benefits"` |
| `Equipment` | `"D"` | `null` | `"Equipment"` |
| `Travel Domestic` | `"E"` | `"Domestic"` | `"Domestic Travel"` |
| `Travel International` | `"E"` | `"International"` | `"International Travel"` |
| `Participant Support Costs Stipends` | `"F"` | `"Stipends"` | `"Participant Support Costs - Stipends"` |
| `Participant Support Costs Travel` | `"F"` | `"Travel"` | `"Participant Support Costs - Travel"` |
| `Participant Support Costs Subsistence` | `"F"` | `"Subsistence"` | `"Participant Support Costs - Subsistence"` |
| `Participant Support Costs Other` | `"F"` | `"Other"` | `"Participant Support Costs - Other"` |
| `Total Number Of Participants` (count only; `amount: null`) | `"F"` | `"TotalParticipants"` | `"Total Number of Participants"` |
| `Total Participant Costs` | `"F"` | `"Total"` | `"Total Participant Costs"` |
| `Materials Supplies` | `"G"` | `"MaterialsSupplies"` | `"Materials and Supplies"` |
| `Publication Costs` | `"G"` | `"Publication"` | `"Publication Costs"` |
| `Consultant Services` | `"G"` | `"ConsultantServices"` | `"Consultant Services"` |
| `Computer Services` | `"G"` | `"ComputerServices"` | `"Computer Services"` |
| `Subawards` | `"G"` | `"Subawards"` | `"Subawards"` |
| `Other Direct Costs Other` | `"G"` | `"Other"` | `"Other"` |
| `Total Other Direct Costs` | `"G"` | `"Total"` | `"Total Other Direct Costs"` |
| `Total Direct Costs` | `"H"` | `null` | `"Total Direct Costs"` |
| `Indirect Costs` | `"I"` | `null` | `"Indirect Costs"` |
| `Total Direct And Indirect Costs` | `"J"` | `null` | `"Total Direct and Indirect Costs"` |
| `Total Amount Of Request` | `"L"` | `null` | `"Amount of this Request"` |
| `Cost Sharing Proposed Level` | `"M"` | `null` | `"Cost Sharing Proposed Level"` |

Do **not** emit entries for `Total Salaries And Wages` or `Total Salaries Wages Fringe Benefits` — they are computed rollups, not letter-coded lines in the NSF form, and are recoverable from the component rows.

Do **not** emit a `budget_categories` entry for `Fees`; it lives in the top-level `fees` scalar. The UDM budget code enum is `^[A-M]$`.

### subawards

Apply the UDM subaward inference rule using the `project_personnel` entries produced above and the `G.Subawards` line:

- If at least one co-PI has `is_at_recipient_institution == false` **AND** the `G.Subawards` amount is greater than 0, emit one inferred entry per non-recipient co-PI:

  ```json
  {
    "subawardee_name": <co-PI's organization>,
    "pi_name": <co-PI's name>,
    "pi_email": <co-PI's email or null>,
    "description": "Implied subaward based on Co-PI <name> at <organization>. Aggregate Subawards line in Budget Category G totals $<amount>; individual subawardee allocation is not broken out in the notice.",
    "obligated_amount": null,
    "anticipated_amount": null,
    "uei": null,
    "inferred": true
  }
  ```

- Otherwise emit `[]`.

Vandalizer never provides explicit subaward enumerations, so `inferred` is always `true` in this translator's output. If multiple co-PIs share the same non-recipient organization, emit one entry per co-PI (downstream can dedupe by `subawardee_name`).

### linked_awards

Emit `[]`. Vandalizer does not capture linked-award references.

### terms_and_conditions

For each of these Vandalizer fields, emit a `terms_and_conditions` entry only when the value is not absent:

- `Authority Act` → `{"citation": <value>, "citation_date": null, "url": null, "applicability_notes": null}`
- `Research Terms And Conditions Date` → `{"citation": "Research Terms and Conditions", "citation_date": <ISO date>, "url": null, "applicability_notes": null}`
- `NSF Agency Specific Requirements Date` → `{"citation": "NSF Agency Specific Requirements", "citation_date": <ISO date>, "url": null, "applicability_notes": null}`

Emit `[]` when all three are absent.

### special_conditions

Emit `[]`. Vandalizer does not capture narrative conditions.

### source_provenance

Always populate `source_provenance`:

- `extractor`: `"vandalizer-to-udm-translation"`
- `extractor_version`: `"0.1.0"` (this prompt's version)
- `upstream_extractor`: `"Vandalizer"`
- `upstream_extractor_version`: the version identifier when the runtime provides one; otherwise `null`
- `source_document`: the source document identifier the runtime provides (Vandalizer input filename, hash, or URI); otherwise `null`
- `extracted_at`: the timestamp the runtime provides; otherwise `null`
- `notes`: `null` unless the runtime supplies one
- `review_annotations`: see below

If the Vandalizer input's `"what data was highlighted yellow in the original document?"` field is present and not absent (`"N/A"`, `""`, or `"null"`), emit one entry:

```json
{
  "label": "highlighted-yellow",
  "value": <the verbatim value>,
  "target_field": null,
  "description": "Reviewer highlighted this content in the original document during Vandalizer extraction."
}
```

Otherwise `review_annotations` is `[]`.

### Procedure

1. Normalize every string scalar (trim whitespace; convert `"N/A"`, `""`, `"null"` to absent).
2. Fill all UDM scalars (identity, dates, funding, indirect cost, `fees`).
3. Build `recipient_organization` and `current_budget_period`.
4. Build `project_personnel` (PI first, then co-PIs from zipped semicolon lists).
5. Build `sponsor_contacts`.
6. Emit every budget row per the mapping table.
7. Apply the subaward inference rule against the `project_personnel` and the `G.Subawards` row.
8. Emit `terms_and_conditions` and `special_conditions` (the latter always `[]`).
9. Build `source_provenance`, including the `review_annotations` entry for the yellow-highlight field when present.
10. Ensure every required array is present; re-check that `amendment_number` is `"000"`.

### Quality standards

1. **Determinism.** The same Vandalizer input must always produce the same UDM output.
2. **No fabrication.** If Vandalizer lacks a field, emit `null` or the documented default — never invent values.
3. **Schema conformance.** Output validates against `components/nsf-award-notice-extraction-udm/schema.json` v1.1.0.
4. **Typed fidelity.** Numbers as numbers, booleans as booleans, ISO dates as strings.
5. **Preserve zeros.** A stated `$0` or `0.00` remains `0` — it is data, not absence.
6. **Provenance always emitted.** `source_provenance.extractor` and `source_provenance.upstream_extractor` are always populated so downstream ingest can distinguish translator output from direct-extractor output.

Produce the JSON now.
