---
name: rfa-checklist-field-mapper
version: 1.0.0
category: extraction
domain: research-administration
status: experimental
tags: [rfa, checklist, field-mapping, evaluation, plain-prompt, clef, json]
audience: [evaluation-staff]
owner: ui-insight
created: 2026-10-29
updated: 2026-10-29
---

# RFA Checklist Field Mapper

> **Purpose:** Moves the text of a free-form RFA checklist into the 28 fields of the RFA Plan B gold, by copying passages only, so the checklist can be scored with the CLEF judge like the `rfa-checklist-extraction` workflow v3.1.0 field output.
> **Expected input:** One checklist as plain text or Markdown, inserted at `{{CHECKLIST}}`. Nothing else: not the announcement, not the gold.
> **Expected output:** One JSON object with all 28 field names as keys; each value is a list of passages copied exactly from the checklist. See [`schema.json`](schema.json).

## Relationship to other components

The field names and their descriptions are copied unchanged from [`rfa-checklist-extraction-udm`](../rfa-checklist-extraction-udm/) `schema.json` v1.0.0 (commit 098ab80), which mirrors the workflow v3.1.0 fields one for one. Those descriptions were written for extracting from an announcement; the prompt tells the model to use them only to decide where a passage belongs. The caller checks every passage against the checklist in code and drops any passage that is not a verbatim substring. This component is an evaluation instrument, not a checklist generator.

---

## Prompt

You will receive a checklist that someone wrote from a funding announcement (RFA). Your job is to sort the checklist's own text into the fields listed below. You are not writing a checklist and you are not extracting from the announcement. You only copy.

Rules:

1. For each field, list the passages from the checklist that give that field's information. Copy each passage exactly as it appears in the checklist: the same words, numbers, spelling and punctuation. Do not rewrite, summarize, shorten inside a passage, combine passages, correct, or complete anything.
2. A passage is a contiguous piece of the checklist's text: a whole line, a sentence, or part of a line. Do not include list bullets or numbering at its start. If a line is a heading and the information is on the lines under it, copy the lines with the information; include the heading only when it carries information itself.
3. Use only the checklist. Do not add anything from your own knowledge, the sponsor's standard rules, or what the announcement probably says. If the checklist does not give a field's information, return an empty list for that field.
4. Do not copy "Not stated" or similar placeholders as a field's information.
5. Look through the whole checklist for every field, not only the section whose name matches. The same passage may go in more than one field.
6. The field descriptions say what information belongs in each field. Use them only to decide which passages belong where. Ignore anything in them about how a value should be written, formatted, resolved, merged with sponsor defaults, or filled in when absent.

Fields:

- `rfa_number` (single value): The sponsor's announcement number without agency prefix (e.g., '26-508', 'PA-24-246').
- `rfa_title` (single value): Full title of the funding opportunity, including any track or component designation.
- `sponsor_name` (single value): Full name of the lead sponsoring agency (e.g., 'National Science Foundation'); never an abbreviation. Resolved downstream to Sponsor_Organization_ID.
- `program_code` (single value): Sponsor's internal program or division code (e.g., 'NSF/TIP/ITE'). Null when not stated.
- `announcement_url` (single value): Canonical URL of the announcement on the sponsor's site. Null when not present.
- `opportunity_number` (single value): Grants.gov or portal opportunity ID when distinct from rfa_number.
- `cfda_number` (single value): CFDA / Assistance Listing number(s); comma-separated when multiple.
- `funding_instrument_type` (single value): Award mechanism in the document's own term ('Grant', 'Cooperative Agreement', 'Contract', ...). Null when not stated; never guessed from the sponsor.
- `dates_and_deadlines` (list): Every unique date or time-bound event, chronologically. Recurring / relative deadline rules are resolved to a concrete date, with the rule text kept in notes.
- `eligible_institutions` (list): One entry per institution category the sponsor names, including a separate 'Subrecipients / Subawardees' entry when the document states subrecipient rules. A single 'Not specified in this document' entry when nothing is stated.
- `eligible_individuals` (list): One entry per PI / Co-PI / senior-personnel category. A single 'Not specified in this document' entry when nothing is stated.
- `award_duration` (single value): Anticipated duration as stated; 'Not specified in the document' when absent.
- `amount_per_award` (single value): Per-award amount with its basis (total vs direct costs), in the sponsor's formatting; 'Not specified in the document' when absent.
- `number_of_awards` (single value): Anticipated count as stated: text such as '10-15' or 'Subject to availability of funds', or a bare integer count. Null only when absent.
- `anticipated_award_date` (single value): As stated; ISO YYYY-MM-DD when given, otherwise free text (e.g., 'Spring 2027'). Null when absent.
- `submission_details` (paragraph): One coherent paragraph: the submission portal the announcement names, file formats, naming, collaboration rules. Null only when there is no submission guidance at all.
- `formatting_requirements` (paragraph): Document-wide preparation rules: the announcement's own rules verbatim, else the sponsor default prefixed 'Sponsor default (<SPONSOR>):', or both combined. Null for a non-backbone sponsor that states none.
- `required_components` (list): Every required proposal component, merged with the sponsor backbone (NSF, NIH, USDA-NIFA, DOE, NASA): announcement-sourced components first, then the backbone.
- `optional_components` (list): Optional and '(if applicable)' components, including Subaward Documents. Empty array when none.
- `funding_limits` (paragraph): Program-wide or per-year caps and category-specific limits.
- `cost_sharing_status` (single value): Cost-sharing status (UDM CostShare).
- `cost_sharing_details` (paragraph): Type, rate, basis, documentation and source restrictions in one paragraph. Null when the status is 'Prohibited' or 'Not Specified'.
- `fa_policy` (paragraph): F&A / indirect-cost policy: rate, base, exclusions (UDM IndirectRate).
- `personnel_effort` (paragraph): Effort floors or ceilings, salary caps, student / postdoc support, consultant limits (UDM Effort).
- `other_considerations` (paragraph): Pre-award costs, program income, budget revisions, required travel, sponsor-specific budget forms.
- `allowable_costs` (list): Categories the sponsor explicitly enumerates as allowable.
- `unallowable_costs` (list): Categories the sponsor explicitly enumerates as unallowable.
- `special_requirements` (list): Unique RFA aspects that fit no other section (conference travel obligations, data sharing beyond federal defaults, workshop participation). Empty array when none.

Return only one JSON object, with no other text before or after it. It must have exactly these 28 keys, in the order above, and each value must be a list of strings (an empty list when the checklist gives nothing for that field):

```json
{"rfa_number": ["..."], "rfa_title": ["..."], "...": []}
```

The checklist:

<checklist>
{{CHECKLIST}}
</checklist>

---

## Quality Standards

- Use the prompt text above verbatim, from the line after `## Prompt` to the line before the closing `---`, with `{{CHECKLIST}}` replaced by the checklist text. Record any change as a new version in `CHANGELOG.md`.
- The caller must check every returned passage against the checklist and drop any that is not a verbatim substring after the normalization the evaluation plan states. The model's output is never trusted on its own.
