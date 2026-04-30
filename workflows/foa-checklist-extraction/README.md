# FOA Checklist Maker Extraction

Uploads a Federal Funding Opportunity Announcement (FOA) and returns a single structured JSON object covering the eight reference sections a federal-grants office uses for FOA review: FOA summary and key dates, funding and eligibility, evaluation criteria with weights, multi-stage review process, agency priorities and program goals, submission platform and forms, application components, and formatting requirements.

**Workflow version:** 0.1.0
**Vandalizer schema version:** 2
**Status:** experimental
**Components manifested:** `foa-checklist-extraction-udm@0.1.0`
**Eval posture:** workflow-local — see [`evals/`](evals/)

## What this workflow does

Two-step runtime mirroring the source `ui-insight/ProcessMapping/workflows/foa-checklist-extraction/` workflow:

**Step 1 — Parallel Extraction (6 Extraction tasks):**

| Task | Source counterpart | Schema target | SearchSet items |
|---|---|---|---|
| `extract-foa-identification-and-timeline` | TASK-01 | identification + timeline | `foa_number`, `cfda_number`, `federal_agency` (enum), `foa_title`, `total_funding`, `expected_awards`, `award_range`, `cost_sharing_required`, `critical_dates`, `performance_period`, `eligible_applicants` |
| `extract-evaluation-criteria` | TASK-02 | evaluation block | `total_points`, `evaluation_criteria`, `scoring_methodology`, `minimum_threshold` |
| `extract-review-process` | TASK-03 | review block | `review_stages`, `review_personnel`, `screening_criteria`, `review_timeline` |
| `extract-agency-priorities-and-goals` | TASK-04 | priorities block | `agency_mission`, `program_goals`, `priority_areas`, `expected_outcomes` |
| `extract-forms-and-submission-systems` | TASK-05 | submission block | `submission_platform`, `required_registrations`, `required_forms`, `application_components` |
| `extract-formatting-requirements` | TASK-06 | formatting block | `document_structure`, `page_limits`, `formatting_standards`, `file_requirements` |

**Step 2 — Consolidation (1 Prompt task):** `foa-checklist-consolidation` assembles the six fragments into a single 31-field schema-conformant object, normalizes the `federal_agency` enum, and verifies cross-field consistency (chronological `critical_dates`, `expected_awards * max(award_range) <= total_funding`).

## Components

- [`foa-checklist-extraction-udm@0.1.0`](../../components/foa-checklist-extraction-udm/) — the sole component.

## Validation plan

| Check | Type | Severity |
|---|---|---|
| `CHK-01` FOA number format | format | warning |
| `CHK-02` Date consistency | consistency | error |
| `CHK-03` Funding vs per-award amounts | arithmetic | warning |

## Eval posture

Workflow-local — see [`evals/`](evals/). The Consolidation Prompt assembles six fragments and enforces cross-field consistency rules — emergent behavior the component-level evals can't cover.

## Building

```bash
python3 scripts/build_vandalizer_workflows.py
```

## Sharing

The committed `foa-checklist-extraction.vandalizer.json` can be uploaded directly into Vandalizer via the workflow import UI.

## Triad integration

- **Evaluation datasets:** none yet — planned: cases at `components/foa-checklist-extraction-udm/evals/cases/`.
- **Shared UDM relationship:** inherits from the component's UDM alignment (RFA, Organization).
- **Sibling workflow:** `rfa-checklist-extraction` covers NSF/NIH solicitation triage; this workflow covers HHS/DOE/agency-issued FOAs with stronger emphasis on evaluation criteria, review process, and submission systems.

## Provenance

Authored 2026-04-30 alongside the initial `foa-checklist-extraction-udm` component.
