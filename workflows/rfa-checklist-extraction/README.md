# RFA Checklist Extraction

Uploads a federal funding announcement (RFA / FOA / NOFO / program solicitation) and returns a single **RA-friendly Markdown checklist** organized in the eight pre-award sections a sponsored-programs analyst uses when triaging an opportunity: Dates & Deadlines, Eligibility, Award Information, Application Components, Budget Requirements & Policies, Submission Details, Special Requirements, and Important Notes.

**Workflow version:** 0.3.0
**Vandalizer schema version:** 2
**Status:** experimental
**Components manifested:** `rfa-checklist-extraction-udm@0.1.0`
**Eval posture:** workflow-local — see [`evals/`](evals/)
**Output contract:** RA-friendly Markdown checklist (8 sections, placement-rule de-duplication)

## What this workflow does

The operator uploads a funding announcement (PDF) into Vandalizer. The workflow runs as two steps:

**Step 1 — Parallel Extraction (7 Prompt tasks):** each task receives the full uploaded document via `input_source: workflow_documents` and emits a **JSON fragment** for its block. (This is the Variant A handoff format. The side-by-side `rfa-checklist-extraction-md` workflow tests an alternative where each task emits a Markdown chunk instead.)

| Task | Block produced |
|---|---|
| `extract-opportunity-metadata` | Scalar fields: rfa_id, rfa_number, rfa_title, sponsor_name, program_code, announcement_url, opportunity_number, cfda_number |
| `extract-dates-and-deadlines` | Chronological array of `{item, date_time, notes}` |
| `extract-eligible-institutions` | Array of `{type, subcategory, examples, compliance_requirements}` |
| `extract-eligible-individuals` | Array of `{type, criteria, compliance_requirements, conditions}` |
| `extract-award-information` | `{award_duration, amount_per_award, number_of_awards, anticipated_award_date}` |
| `extract-application-components` | `{required_components, optional_components, submission_details, special_requirements}` |
| `extract-budget-requirements` | `{funding_limits, cost_sharing_status, cost_sharing_details, fa_policy, allowable_costs, unallowable_costs, personnel_effort, other_considerations}` |

**Step 2 — Consolidation (1 Prompt task, Markdown deliverable):** `rfa-checklist-consolidation` parses the seven JSON fragments and renders a single Markdown document with the eight sections in canonical order, enforcing the placement contract (award amount only in AWARD INFORMATION; detailed financial rules only in BUDGET REQUIREMENTS & POLICIES; per-component formatting rules on the individual component, not in SPECIAL REQUIREMENTS; submission mechanics only in SUBMISSION DETAILS) and synthesizing an IMPORTANT NOTES section from cross-fragment signals.

The runtime mirrors the source `ui-insight/ProcessMapping/workflows/rfa-checklist-extraction/` workflow's eight-section consolidated checklist conventions exactly.

## Architecture context

This workflow's **Markdown output is for end users (sponsored-programs analysts)**, not for the evaluation harness. The split:

- **Component** (`components/rfa-checklist-extraction-udm/`) — JSON-emitting, `schema.json`-backed, single-call canonical prompt. This is the evaluation-harness target.
- **Workflow** (this folder) — Markdown-emitting, Vandalizer-shaped pipeline. This is the RA-via-Vandalizer deliverable.

The two outputs serve different consumers without doubling maintenance.

## Components

- [`rfa-checklist-extraction-udm@0.1.0`](../../components/rfa-checklist-extraction-udm/) — the sole component. The component itself emits JSON for evaluation; this workflow's seven Extraction tasks carry focused `prompt_inline` bodies in [`manifest.yaml`](manifest.yaml) that emit JSON fragments for clean step-input handoff, and the Consolidation step renders the final Markdown.

## A/B test sibling

- [`rfa-checklist-extraction-md`](../rfa-checklist-extraction-md/) — same final Markdown deliverable, but the parallel tasks emit Markdown chunks (already wearing their target section's heading) and the Consolidation step glues them rather than parsing JSON. Comparing the two workflows' outputs against the same RFA tells us which mid-pipeline format produces more reliable deliverables.

## Validation plan

Carried into the Vandalizer export at the workflow level (re-targeted for the Markdown deliverable):

| Check | Type | Severity |
|---|---|---|
| `CHK-01` Eight sections present | completeness | error |
| `CHK-02` Placement contract enforcement | consistency | warning |
| `CHK-03` Monetary amount preservation | format | error |
| `CHK-04` Eligibility completeness | completeness | warning |

## Eval posture

Workflow-local — see [`evals/`](evals/). The workflow's deliverable is Markdown, so workflow-local cases use `expected.md` rather than `expected.json`. The component-level evals at [`components/rfa-checklist-extraction-udm/evals/`](../../components/rfa-checklist-extraction-udm/evals/) remain the JSON-against-schema test for the harness.

Workflow-local cases should target the eight-section presence, the placement contract enforcement during consolidation (any cost-sharing inadvertently mentioned by extract-award-information should be moved to BUDGET REQUIREMENTS & POLICIES; per-component formatting in SPECIAL REQUIREMENTS should be moved onto the matching component row), monetary preservation, and IMPORTANT NOTES synthesis.

## Recommended knowledge bases

When attaching a `KnowledgeBaseQuery` step manually in Vandalizer (post-import), the following institutional knowledge bases provide useful context:

- **Primary:** OMB Uniform Guidance (2 CFR 200)
- **Agency-specific (attach the one(s) that match the RFA's sponsor):** NSF PAPPG Reference, NIH Grants Policy Statement, DOE Financial Assistance Rules, DOD Research Funding & DFARS
- **When proposal has human subjects:** Human Subjects Protection (Common Rule)
- **When research-security-relevant:** Export Control (EAR & ITAR)

KBs are not auto-wired by the workflow import — Vandalizer's importer blanks `kb_uuid` references by design. Attach them by adding a `KnowledgeBaseQuery` step manually in the Vandalizer UI after import.

## Building

Re-generate the Vandalizer export from `manifest.yaml`:

```bash
python3 scripts/build_vandalizer_workflows.py
```

CI fails when the committed `rfa-checklist-extraction.vandalizer.json` differs from a fresh build, so treat `manifest.yaml` as the source of truth and never hand-edit the generated JSON.

## Sharing

The committed `rfa-checklist-extraction.vandalizer.json` can be uploaded directly into Vandalizer via the workflow import UI. Its `x_ai4ra` block traces it back to this manifest, the pinned component version, and the content hash of the embedded prompt bodies.

## Triad integration

- **Evaluation datasets:** none yet — planned: add an RFA case to `real.nsf_awards` or a new `real.rfa_checklists` dataset with `expected.md` produced from a sponsored-programs-reviewed Markdown deliverable.
- **Harness notes:** the harness's primary RFA-checklist evaluation target is the JSON-emitting `rfa-checklist-extraction-udm` component via `prompt.md`. This workflow's Markdown output is a secondary signal; pair workflow-level Markdown-diff scoring (against `expected.md`) with component-level JSON-against-schema scoring when both are available.
- **Shared UDM relationship:** inherits from the `rfa-checklist-extraction-udm` component's UDM alignment (`rfa_id`, `sponsor_name` resolve to UDM `RFA` and `Sponsor_Organization`; `cost_sharing` to `CostShare`; `fa_policy` to `IndirectRate`; `personnel_effort` to `Effort`).

## Provenance

Authored 2026-04-24 alongside the initial `rfa-checklist-extraction-udm` component. Upgraded to v0.3.0 on 2026-05-22 with two changes: (1) parallel tasks converted from Vandalizer Extraction (SearchSet) to Vandalizer Prompt (full-document NLU) — necessary because grant documents in practice don't use the literal field labels SearchSet keyword retrieval expects; (2) output contract switched from JSON-against-schema to RA-friendly Markdown deliverable, with the harness target remaining the JSON-emitting component. Against `ui-insight/ProcessMapping` at commit `2c1f47f46474130743af5aee44d074bcd21787e9`; the eight-section structure follows the source `consolidation.md` conventions verbatim.
