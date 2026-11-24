# Vandalizer drafts for RA review

**Status:** draft · **Kind:** draft collection · **Items:** 11 Skills, 14 workflows · **Status as of:** 2026-11-23

Draft Vandalizer items built from recorded research-administration process walkthroughs and from Vandalizer's catalog. **Nothing here is published, and no catalog item is changed.** Each JSON file is a Vandalizer import file: loading it creates a private item under **Library → Mine** for the person who imports it, named "… (Imported)".

[`drafts.json`](drafts.json) is the machine-readable index: one entry per file with its kind, group, SHA256, related workflows in this repository, test fixtures and evaluation outcome. See [`../README.md`](../README.md) for the draft kinds and the index contract.

- `new/`: Skills and workflows that are not in the catalog.
- `companion/`: browser Skills to use beside an existing catalog workflow.
- `variants/`: copies of catalog workflows with V5 steps added, named "… (V5 draft)". The catalog originals are untouched; run the two side by side to compare.

## new/

| File | Kind | Built from | What it does |
|---|---|---|---|
| `award-modification-intake.workflow` | Workflow | more money, NCE, PI change, rebudget processes | Classifies an amendment and writes an intake brief: key details, checks, conditions, the processing checklist for that type, draft correspondence. |
| `modification-correspondence.skill` | Skill | same four processes, closeout de-obligation | PI/DGA email, Banner FOA text line and processing note from the executed amendment. |
| `export-to-banner-worksheet.workflow` | Workflow | financial-unit-account-setup, export-to-banner-review | Lays out an award's values in the order of the Export to Banner form, with pages, and lists what the award does not state. |
| `export-to-banner-form-review.skill` | Skill | export-to-banner-review | Compares a prepared form with the award and lists differences as questions for the analyst, plus the lookups the reviewer still has to do. |
| `add-sponsor-research.skill` | Skill, browser | adding-sponsor-to-veras | VERAS search variants, SAM.gov research, proposed business associate record with a source per value. |
| `tps-waiver-review.skill` | Skill | tps-waiver-review | PI and SPA scores side by side, tier, timeline, reviewer notes, decision message. The reviewer decides. |
| `section2-personnel-eligibility.workflow` | Workflow | spa-section2-review | PI/Co-PI eligibility against APM 45.22 and required DGAs against Section 2. |
| `sfi-rst-personnel-check.workflow` | Workflow | sfi-rst-compliance-check | Compliance matrix: who must comply, SFI disclosure dates and when they lapse, RST completion. |
| `near-final-document-completeness.workflow` | Workflow | near-final-doc-review | Required documents, the four senior/key documents per person, conditional documents, subaward documents, and a draft note to the PI. |
| `idc-exception-triage.skill` | Skill | indirect-cost-exception-review | Sorts exception report rows into rounding, possible subaward threshold, possible exempt costs, and rows that need a Banner lookup. |
| `final-billing-review.skill` | Skill | final-billing | Totals check, payroll around the end date, flagged transactions, documentation request. Allowability stays with the specialist. |
| `budget-justification.skill` | Skill | catalog "Budget Generator" | The same rules as a chat Skill, so the RA can answer the "[Basis to be supplied]" gaps and get a revised draft. |

## companion/

| File | Use beside | What it does |
|---|---|---|
| `screening-list-lookup.skill` | Export Control Screening | Looks parties up on the Consolidated Screening List (trade.gov) and reports entries found. |
| `subrecipient-sam-check.skill` | Subaward Extraction, New Subaward Intake | SAM.gov registration, UEI, expiry and exclusions, compared with the subaward. |
| `live-solicitation-check.skill` | FOA Checklist, RFA Checklist, Sponsor Compliance Checker | Compares the solicitation PDF with the opportunity's live page for a changed deadline or new amendment. |
| `fa-rate-agreement-check.skill` | F&A Rate Validator | Compares the rate and base in an award with the institution's published rate page. |

For reading figures from sponsor portals or Banner under the RA's sign-in, Vandalizer's built-in "Collect figures from websites" Skill starter already fits; no draft was made.

## variants/

| File | What was added to the catalog workflow |
|---|---|
| `ffr-management`, `prior-approval-tracking` | Uniform Guidance knowledge base step; then approval → create project → add deadlines to the RA inbox. |
| `award-compliance-analysis`, `noa-summary` | The same, plus an award snapshot Page. |
| `effort-reporting-compliance` | Uniform Guidance knowledge base step only. |
| `post-award-closeout-checklist` | Approval → create project → add deadlines to the RA inbox. |
| `foa-checklist`, `rfa-checklist` | A structured "Key fields" step first; then approval → create project → add deadlines to the RA inbox. |
| `subaward-extraction` | A structured "Key fields" step first. (Project and inbox setup already exists as the catalog's New Subaward Intake.) |

The original prompts are unchanged except that a knowledge base variant's first prompt gets a paragraph telling it to cite the retrieved passages. The catalog's validation plans and test inputs are carried over.

## Relationship to `workflows/`

Several drafts cover a task that already has a manifest-built workflow in this repository. The drafts were written independently from the same process walkthroughs or from Vandalizer's catalog seeds, so neither is derived from the other. `drafts.json` lists the overlap per item under `related_workflows`.

| Draft | Existing workflow |
|---|---|
| `award-modification-intake`, `modification-correspondence` | `award-modification-intake` |
| `export-to-banner-worksheet`, `export-to-banner-form-review` | `export-to-banner-extraction` |
| `section2-personnel-eligibility` | `section2-personnel-eligibility` |
| `sfi-rst-personnel-check` | `compliance-personnel-verification` |
| `near-final-document-completeness` | `proposal-document-completeness` |
| `budget-justification` | `budget-justification-generator` |
| `subrecipient-sam-check`, `subaward-extraction` variant | `subaward-extraction` |
| `live-solicitation-check`, `foa-checklist` and `rfa-checklist` variants | `foa-checklist-extraction`, `rfa-checklist-extraction` |
| `ffr-management`, `prior-approval-tracking`, `award-compliance-analysis`, `noa-summary`, `effort-reporting-compliance` variants | `ffr-management-extraction`, `prior-approval-extraction`, `award-compliance-extraction`, `noa-summary`, `effort-reporting-extraction` |

## Loading them

- **Skills:** Library → import, choose the `.skill.vandalizer.json` file, then select the Skill in chat.
- **Workflows:** the workflow editor's import, choose the `.workflow.vandalizer.json` file.

## After import: pick the knowledge base

A file cannot carry a link to a knowledge base. These workflows import with their knowledge base step empty and a note on the step naming the one to pick. **They stop at that step until one is selected.**

| Workflow | Knowledge base to pick |
|---|---|
| The five `variants/` with a "Regulation passages" step | Uniform Guidance (2 CFR 200) |
| `section2-personnel-eligibility` | University of Idaho Office of Sponsored Programs (APM 45) |

`near-final-document-completeness` has no knowledge base step; to check against the NSF PAPPG, add a Knowledge Base Query task to its first step. `award-modification-intake` also has none; it uses only the document.

## What each needs from the RA

- **Browser Skills** (`add-sponsor-research`, all of `companion/`): the browser extension connected and the site allowed. They only read. `live-solicitation-check` and `fa-rate-agreement-check` ask for the page address; they do not guess one.
- **Section 2 check:** the proposal's Section 2, the employee class and timesheet org code for each person as looked up in Banner, and the Department List, as files or pasted text. The workflow cannot look anything up in Banner.
- **SFI/RST check:** Sections 2 and 6.6, the SFI confirmations with dates, and the RST completion spreadsheet.
- **TPS waiver review:** the ticket, the VERAS dates and tier, and the due date calculator's output. The Skill does not compute the internal deadlines.
- **Variants with setup steps:** approving the gate creates a real project and real inbox items. In a validation run or step test those steps only describe what they would do.

## Things for RAs to check

- Each processing checklist and rule comes from one recorded walkthrough. Are the steps, order and thresholds right? In particular: the TPS tiers (below 50, 50–74, above 74); the sponsor record's "always Sponsor, Vendor and Subrecipient" setting; SFI disclosures valid one year; the 35-character short title rule.
- `idc-exception-triage` treats a difference under half a percentage point as rounding. That cut-off is a guess to be confirmed.
- The TPS waiver questions and the due date calculator's rules are not in the process map.
- `add-sponsor-research` here leaves out one institution-specific sentence from Step 4 of the source draft: an instruction to stop and consult before creating a record for a sponsor with a particular country of ownership. Reviewers working from the source version will see it; decide whether a general form of that rule belongs in the Skill.

## Test documents and results

The triad's other two repositories hold the evaluation material:

- **Fixtures:** [`AI4RA/evaluation-data-sets` `synthetic/ra_process_test_documents/`](https://github.com/AI4RA/evaluation-data-sets/tree/main/synthetic/ra_process_test_documents) has synthetic documents for trying every workflow and Skill, with planted traps, and answer keys saying which files go with which item and what a correct result contains. Everything in them is invented.
- **Run outputs:** [`AI4RA/evaluation-data-sets` `evaluation_results/vandalizer-ra-drafts/`](https://github.com/AI4RA/evaluation-data-sets/tree/main/evaluation_results/vandalizer-ra-drafts) has the saved workflow results and Skill transcripts.
- **Runner:** [`AI4RA/evaluation-harness` `runners/vandalizer-ra-drafts/`](https://github.com/AI4RA/evaluation-harness/tree/main/runners/vandalizer-ra-drafts) imports these files into a Vandalizer site and runs them against the fixtures.

## Evaluation status · November 23, 2026

All 25 drafts were attempted on a Vandalizer development site. Thirteen workflows and six chat Skills produced output from the synthetic corpus. All five browser Skills were exercised in a signed-in browser. Four paired a synthetic input with live sources, and Live Solicitation Check used a real NSF opportunity. Section 2 Personnel Eligibility stopped before producing a report because the OSP policy knowledge base was unconfigured. Workflow tests with a setup approval stopped at that gate.

- Export to Banner Form Review found all six planted discrepancies. Award Modification Intake flagged the missing countersignature, Near-Final Document Completeness found the missing mentoring plan, and Final Billing Review stopped at a $125 reconciliation difference.
- Repeat runs of Award Compliance Analysis still included unsupported regulation numbers. Prior Approval Tracking contradicted its own equipment threshold in one run.
- All five browser Skills had their instructions revised after their first live run, and the files here are the revised versions. Screening received two live retests and identified both federal source lists. Later result pages and a parenthetical name variant still need review. The other four await a live rerun with the revised instructions. No browser Skill output was saved.
- Time saved on real cases and reviewer preference over the published workflows remain open.

These outcomes record what a run produced. They are not accuracy scores, and no draft has been reviewed by an RA yet.

## Editing

The text lives in `scripts/build_drafts.py` and `scripts/more_drafts.py`. From this directory, regenerate with:

```
python3 scripts/build_drafts.py . /path/to/vandalizer
```

The second argument is a clone of the vandalizer repo; the variants and `budget-justification` are generated from its seed files at `origin/major/agentic-chat`. Without it only the other drafts are written. The checked-in files were built from seed commit `1453fc46ea022b9e2e9d6a783a3c86731485437d`; pass that as a third argument to reproduce them byte for byte.

After regenerating, update each changed file's `sha256` in `drafts.json` and run `python3 .github/scripts/lint_components.py` from the repository root.
