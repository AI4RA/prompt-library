# Draft case nsf22624: provenance and open decisions

**Status: DRAFT, not validated.** This case lives in `evals/drafts/`, which the lint and the component catalog
do not read, so it does not count as an evaluated case. A sponsored-programs reviewer has to check every field
marked *drafted* or *decision* below against the source, then move the directory to `evals/cases/` and fill in
`validated_by`, `validated_at` and `validated_against_version` in `metadata.yaml`.

The source is the clean web text `real/nsf_rfa_checklist_eval/corpus/webtext_md/nsf22624.md` in
`AI4RA/evaluation-data-sets`, the same text the Plan B gold was drafted from (see `input-source.md`).

## Where each field comes from

**Gold** means the value restates a Plan B gold row in `evaluation_results/rfa-checklist-extraction/plan-b/answer_key_v3.1.0.jsonl`
that was verified or corrected against the source on 2026-09-17 (row `#` given). **Drafted** means it was written
from the source for this case and has no validated gold.

| field | provenance | gold row(s) | how the gold was mapped |
|---|---|---|---|
| `rfa_id` | drafted | — | `"<SPONSOR_CODE>-<OPPORTUNITY_NUMBER>"` rule |
| `rfa_number` | gold | #1 | gold `NSF 22-624` without the agency prefix, as the prompt asks |
| `rfa_title`, `sponsor_name`, `cfda_number` | gold | #2, #3, #7 | verbatim |
| `program_code` | gold (corrected) | #4 | verbatim |
| `announcement_url` | gold (corrected, rubric v1.1 C1) | #5 | verbatim |
| `opportunity_number` | gold | #6 | "Not specified in the document" → `null` |
| `funding_instrument_type` | gold | #8 | verbatim (`Grant`; the document says "Standard Grant or Continuing Grant") |
| `risk_flags`, 5 escalation checks | gold | #37–#41 | statuses verbatim; `detail` written from the gold notes |
| `risk_flags`, 12 CRU checks | drafted | (#42–#53 are `ra_pending`) | see decisions below |
| `dates_and_deadlines` | gold | #10 | one row, as in the gold |
| `eligible_institutions` | gold | #11, #12 | the two gold elements as two entries |
| `eligible_individuals` | gold | #13 | the gold element as `conditions` |
| `award_information` | gold | #14–#17 | "Not specified" → the prompt's string or `null`; `number_of_awards` as the gold text |
| `required_components` | gold (corrected) + sponsor backbone | #26 | gold's three RFA-explicit components as `Announcement + sponsor standard`, then the NSF backbone stubs |
| `optional_components` | **decision** | #27 | see decisions below |
| `submission_details` | gold + document | #22 | gold text plus the collaborative-proposal rule the gold notes mention |
| `formatting_requirements` | **decision** | #23 | see decisions below |
| `special_requirements` | drafted | (#24–#25 are `descoped`) | three solicitation-specific rules from Section II |
| `mandated_structure` | drafted | (#28 is `deferred`) | see decisions below |
| `budget_requirements` | gold | #29–#36 | verbatim; "Not specified" → `null`; "None enumerated" → `[]` |
| `compliance_risks`, `international_components` | drafted | (#54–#61 `descoped`, #62–#67 `faithfulness_only`) | all `unclear`: the document addresses none of the 14 areas |
| `important_notes` | drafted | — | one process note |

## Decisions for the reviewer

1. **`optional_components`.** The gold (#27) says "None identified", a judgment call recorded under CD3. The
   1.0.0 contract adds the NSF backbone's "(if applicable)" items as `Sponsor standard` optional components, so
   the draft lists those four. Keep the backbone items, or follow the gold with `[]`?
2. **`formatting_requirements`.** The gold (#23) reads "Defers to PAPPG. Solicitation-specific: Collaborators &
   Other Affiliations Table 4 — list only the first three co-authors". Under the 1.0.0 placement contract, a
   per-component rule belongs on that component, which the draft does (COA `special_requirements`). Document-wide
   formatting then follows the precedence rule: the announcement states none, so the draft uses the NSF sponsor
   default. Accept this, or keep the gold text here?
3. **CRU "FAR-based or contract-type terms" = `no`.** The document states the award type as "Standard Grant or
   Continuing Grant", which the draft treats as affirmatively ruling out a contract. Under CD1 a silent document
   would be `unclear`. Is the award-type statement enough for `no`?
4. **CRU "Other unusual terms and conditions" = `unclear`.** The NASA MOU (NSF may share proposal information
   with NASA and invite NASA observers to panels) is listed in `special_requirements`, not as a CRU trigger.
   Should it be a `yes` here?
5. **`mandated_structure`.** Section II requires "a labeled section in the project description explaining why
   NASA data are required" for proposals with an extensive NASA-data effort. The draft records it as a
   conditional mandated section. The document does not name the section, so its `name` is descriptive, not
   verbatim. Keep it, or treat it only as part of the Project Description `description` and use `[]`?
6. **Not included, deliberately.** These are left out to stay within what the validated gold or the prompt
   supports:
   - "Posted: August 4, 2022" in `dates_and_deadlines` (not a deadline; the gold has one row);
   - the RUI institution category in `eligible_institutions` (it is mentioned only as a proposal type);
   - the "no limit on proposals per PI or co-PI" statement in `eligible_individuals` (it is in the Limited
     submission flag's `detail`).
