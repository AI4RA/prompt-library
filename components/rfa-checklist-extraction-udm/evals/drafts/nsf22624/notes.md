# Draft case nsf22624: provenance and open decisions

**Status: DRAFT, not validated.** This case lives in `evals/drafts/`, which the lint and the component catalog
do not read, so it does not count as an evaluated case. A sponsored-programs reviewer has to check every field
marked *drafted* or *decision* below against the source, then move the directory to `evals/cases/` and fill in
`validated_by`, `validated_at` and `validated_against_version` in `metadata.yaml`.

**Input for this case:** the clean web text `real/nsf_rfa_checklist_eval/corpus/webtext_md/nsf22624.md` in
`AI4RA/evaluation-data-sets`, the text the Plan B gold was drafted from (see `input-source.md`). Expected values
are what a correct run on *that* text should produce.

## Where each field comes from

**Gold** means the value restates a Plan B gold row in `evaluation_results/rfa-checklist-extraction/plan-b/answer_key_v3.1.0.jsonl`.
Those rows were verified or corrected against the source text on 2026-09-17, except where noted (row `#` given).
**Drafted** means the value was written from the source for this case and has no validated gold.

| field | provenance | gold row(s) | how the gold was mapped |
|---|---|---|---|
| `rfa_id` | drafted | — | `"<SPONSOR_CODE>-<OPPORTUNITY_NUMBER>"` rule |
| `rfa_number` | gold | #1 | gold `NSF 22-624` without the agency prefix, as the prompt asks |
| `rfa_title`, `sponsor_name`, `cfda_number` | gold | #2, #3, #7 | verbatim |
| `program_code` | gold (corrected) | #4 | verbatim |
| `announcement_url` | **decision** | #5 | `null`: see decision 1 |
| `opportunity_number` | gold | #6 | "Not specified in the document" → `null` |
| `funding_instrument_type` | gold | #8 | verbatim (`Grant`; the document says "Standard Grant or Continuing Grant") |
| `risk_flags`, 5 escalation checks | gold | #37–#41 | statuses verbatim; `detail` written from the gold notes |
| `risk_flags`, 12 CRU checks | drafted | (#42–#53 are `ra_pending`) | see decisions 4 and 5 |
| `dates_and_deadlines` | gold | #10 | one row, as in the gold; label as stated ("Submission Window Date(s)"), time in `date_time` |
| `eligible_institutions` | gold | #11, #12 | the two gold elements as two entries |
| `eligible_individuals` | gold | #13 | the gold element as `conditions` |
| `award_information` | gold | #14–#17 | "Not specified" → the prompt's string or `null`; `number_of_awards` as the gold text, worded as in the source |
| `required_components` | gold (corrected) + sponsor backbone | #26 | gold's three RFA-explicit components as `Announcement + sponsor standard`, then the NSF backbone stubs; the NASA-data section is in `mandated_structure`, not repeated here |
| `optional_components` | **decision** | #27 | see decision 2 |
| `submission_details` | gold + document | #22 | gold text plus the collaborative-proposal rule the gold notes mention |
| `formatting_requirements` | **decision** | #23 | see decision 3 |
| `special_requirements` | drafted | (#24–#25 are `descoped`) | three solicitation-specific rules from Section II |
| `mandated_structure` | drafted | (#28 is `deferred`) | see decision 6 |
| `budget_requirements` | gold | #29–#36 | verbatim; "Not specified" → `null`; "None enumerated" → `[]` |
| `compliance_risks`, `international_components` | drafted | (#54–#61 `descoped`, #62–#67 `faithfulness_only`) | all `unclear`: the document addresses none of the 14 areas |
| `important_notes` | drafted | — | one process note |

## Decisions for the reviewer

1. **`announcement_url` = `null`.** The web text links to this solicitation only through relative paths
   (`/funding/opportunities/aag-…`), with no absolute URL for it, and the prompt says null when the document does not state a value. Gold #5 holds
   `https://www.nsf.gov/funding/opportunities/aag-astronomy-astrophysics-research-grants/nsf22-624/solicitation`.
   It was re-derived on 2026-10-02 from the corpus anchor index (`corpus/rfa_index.csv`) under rubric v1.1 C1, not
   from the text; the PDF's print footer carries the URL. Keep `null` for the web-text input, or switch the case
   input to the PDF (`corpus/pdfs/nsf22624.pdf`) and use the gold URL?
2. **`optional_components`.** The gold (#27) says "None identified", a judgment call recorded under CD3. The
   1.0.0 contract adds the NSF backbone's "(if applicable)" items as `Sponsor standard` optional components, so
   the draft lists those four. Keep the backbone items, or follow the gold with `[]`?
3. **`formatting_requirements`.** The gold (#23) reads "Defers to PAPPG. Solicitation-specific: Collaborators &
   Other Affiliations Table 4 — list only the first three co-authors". Under the 1.0.0 placement contract, the
   Table 4 rule is per-component, so the draft puts it on the COA component. The announcement's document-wide rule
   ("prepare your proposal according to Chapter II.D.2 of the PAPPG … in effect on your proposal's due date")
   goes first here, and the NSF sponsor default fills the rest, following the prompt's "some rules but not
   others" branch. Accept, or keep the gold text here?
4. **CRU "FAR-based or contract-type terms" = `no`.** The document states the award type as "Standard Grant or
   Continuing Grant", which the draft treats as affirmatively ruling out a contract. Under CD1 a silent document
   would be `unclear`. Is the award-type statement enough for `no`?
5. **CRU "Other unusual terms and conditions" = `unclear`.** The NASA MOU (NSF may share proposal information
   with NASA and invite NASA observers to panels) is listed in `special_requirements`, not as a CRU trigger.
   Should it be a `yes` here?
6. **`mandated_structure`.** Section II requires "a labeled section in the project description explaining why
   NASA data are required" for proposals with an extensive NASA-data effort. The draft records it as a
   conditional mandated section (only there; the Project Description `description` no longer repeats it). The
   document does not name the section, so its `name` is descriptive, not verbatim. Keep the entry, or drop it
   and use `[]`?
7. **Supplemental-funding deadline.** Section II says a supplemental funding request to an existing award "should
   be submitted by April 1 in the year for which the supplemental funds are requested". Conference proposals
   should be submitted "at least 12 months before the anticipated conference". The solicitation itself does
   not apply to supplements or conferences, and the gold (#10) has only the submission window, so the draft
   leaves both out of `dates_and_deadlines`. The prompt asks for every date-bound event. Include the April 1
   deadline?

### Left out deliberately, or noted

- "Posted: August 4, 2022" is not in `dates_and_deadlines`: it is not a deadline, and the gold has one row.
- The RUI institution category is not in `eligible_institutions`: the document mentions RUI only as a proposal
  type the program accepts.
- The "no limit on proposals per PI or co-PI" statement is not in `eligible_individuals`: it is in the Limited
  submission flag's `detail`.
- The "Anticipated Funding Amount: $50,000,000" has no slot in the contract (gold #20 is retired), so it appears
  nowhere. `amount_per_award` stays "Not specified in the document", because the prompt forbids deriving a
  per-award figure.
- "Other Budgetary Limitations: Not Applicable" appears in both `funding_limits` and `other_considerations`,
  as in gold #29 and #34.
- The CDS&E rule ("address the CDS&E program goals within the 15-page Project Description") is in
  `special_requirements`, not on the Project Description component, because it applies only to CDS&E proposals.
- The Subaward Documents component carries a `description` even though its source is `Sponsor standard`, as the
  prompt's backbone rule 3 asks; the schema allows it.
