# RFA Checklist Extraction

Uploads a federal funding announcement (RFA / FOA / NOFO / program solicitation) and returns a single **RA-friendly Markdown checklist** organized in the pre-award sections a sponsored-programs analyst uses when triaging an opportunity, led by a **Red Flags** banner that surfaces escalation triggers first: Red Flags, Dates & Deadlines, Eligibility, Award Information, Budget Requirements & Policies, Submission Details, Application Components, Special Requirements, and Important Notes.

**Workflow version:** 0.7.0
**Vandalizer schema version:** 2
**Status:** experimental
**Components manifested:** `rfa-checklist-extraction-udm@0.1.0`
**Eval posture:** workflow-local — see [`evals/`](evals/)
**Output contract:** RA-friendly Markdown checklist (11 sections, Red-Flags-led, sponsor-backbone-merged components, placement-rule de-duplication)

## What this workflow does

The operator uploads a funding announcement (PDF) into Vandalizer. The workflow runs as two steps (parallel extraction and consolidation):

**Step 1 — Parallel Extraction (10 Prompt tasks):** each task receives the full uploaded document via `input_sources: [workflow_documents]` and emits a **JSON fragment** for its block. (This is the Variant A handoff format. The side-by-side `rfa-checklist-extraction-md` workflow tests an alternative where each task emits a Markdown chunk instead.) Every task carries explicit anti-hallucination guards — ground each value in the document, use "unclear"/null rather than guessing, never infer a typical federal value.

| Task | Block produced |
|---|---|
| `extract-opportunity-metadata` | Scalar fields: rfa_id, rfa_number, rfa_title, sponsor_name, program_code, announcement_url, opportunity_number, cfda_number, **funding_instrument_type** |
| `extract-risk-flags` | `{risk_flags: [{check, category, status, detail}]}` — **expanded** to 5 escalation flags + the Contract-Review-Unit trigger set (indemnification, IP/data ownership, publication restrictions, insurance, NDA, FAR/contract terms, governing law of another state, acceptance of T&C on submission, restricted country / foreign ownership, JPL/INL, CUI/classified); `category` = escalation \| cru |
| `extract-dates-and-deadlines` | Chronological array of `{item, date_time, notes}` — resolves recurring/relative deadline rules to concrete dates, rule text kept in `notes` |
| `extract-eligible-institutions` | Array of `{type, subcategory, examples, compliance_requirements}` — incl. institution-level limited-submission caps, required certifications, **subrecipient eligibility** |
| `extract-eligible-individuals` | Array of `{type, criteria, compliance_requirements, conditions}` — incl. per-individual submission caps + **limited-submission mechanics/nomination**, citizenship, career stage, required credentials |
| `extract-award-information` | `{award_duration, amount_per_award, number_of_awards, anticipated_award_date}` |
| `extract-application-components` | `{submission_details, formatting_requirements, special_requirements, required_components, optional_components}` — **sponsor-backbone-merged** (NSF/NIH/USDA-NIFA/DOE/NASA); each component carries a `source`; pure "Sponsor standard" components arrive as `{name, source}` stubs; `submission_details` names the specific portal; `formatting_requirements` uses the announcement's rules if stated, else the sponsor default |
| `extract-mandated-structure` | `{mandated_structure: [{component, mandated_sections}]}` — internal sections the announcement mandates for a component (names verbatim, sub-parts/table columns/milestones spelled out — never a pointer like "see Section V.A"); empty array when the announcement prescribes no internal structure |
| `extract-budget-requirements` | `{funding_limits, cost_sharing_status, cost_sharing_details, fa_policy, allowable_costs, unallowable_costs, personnel_effort, other_considerations}` — explicitly hunts salary/tuition/equipment/participant/travel/food/incentive/publication rules |
| `extract-compliance-flags` | `{compliance_risks: [{area, status, detail}], international_components: [{area, status, detail}]}` — human subjects, animals, biosafety, export control, select agents, CUI, data security, national security; foreign collaborators/subawards/travel, talent-program certs, international data sharing, country restrictions |

**Step 2 — Consolidation (1 Prompt task, Markdown deliverable):** `rfa-checklist-consolidation` parses the ten JSON fragments and renders a single Markdown document with the eleven sections in canonical order (Red Flags first), enforcing the placement contract (award amount only in AWARD INFORMATION; detailed financial rules only in BUDGET REQUIREMENTS & POLICIES; per-component formatting rules on the individual component, not in SPECIAL REQUIREMENTS; submission mechanics only in SUBMISSION DETAILS — with the Red Flags banner allowed to carry short *pointers* to those triggers; mandated-section enumerations only in the Announcement-Mandated Structure block) and synthesizing an IMPORTANT NOTES section from cross-fragment signals. When any CRU trigger fires, Red Flags adds the "route to the Contract Review Unit via VERAS" action. For each entry in the mandated-structure fragment, a **"📋 Required structure: \<Component\>"** block renders after the Required Components table enumerating every mandated section and sub-part, with the component's Special Requirements cell pointing to it.

The runtime extends the source `ui-insight/ProcessMapping/workflows/rfa-checklist-extraction/` workflow's consolidated checklist conventions with the 2026-08 pre-award RA feedback (Red Flags banner + expanded Contract-Review trigger set, section reorder, recurring date resolution, richer eligibility, sponsor backbone, Compliance Risks + Foreign Influence sections).

## Sponsor backbone (v0.6.0)

Federal sponsors often omit standardized required components from an individual announcement (they live in the sponsor's proposal guide, e.g., the NSF PAPPG). The `extract-application-components` task carries a **baked-in reference** of each sponsor's standard required components and standard formatting for **NSF, NIH, USDA-NIFA, DOE, and NASA**, sourced from the RA-provided `Required document components and formatting NSF_NIH_USDA_NIFA_DOE_NASA.pdf`. At runtime it:

- **detects the sponsor** from the document and **merges** the standard components into the output even when the announcement does not list them — no operator action, no second upload;
- tags every component with a **`source`** (Announcement / Sponsor standard / Announcement + sponsor standard) so the reviewer can verify provenance and see where the RFA modifies a standard component;
- fills **`formatting_requirements`** by precedence: the announcement's stated formatting if present, otherwise the sponsor default (prefixed `Sponsor default (<SPONSOR>):`);
- applies **no backbone to non-federal sponsors** (state agencies, foundations) — those reflect only what the announcement states.

Some backbone items are University-of-Idaho-specific (e.g., the AOR-signed Letter of Commitment / FDP-list / UI subrecipient Commitment form language), carried verbatim from the reference PDF.

## Architecture context

This workflow's **Markdown output is for end users (sponsored-programs analysts)**, not for the evaluation harness. The split:

- **Component** (`components/rfa-checklist-extraction-udm/`) — JSON-emitting, `schema.json`-backed, single-call canonical prompt. This is the evaluation-harness target.
- **Workflow** (this folder) — Markdown-emitting, Vandalizer-shaped pipeline. This is the RA-via-Vandalizer deliverable.

The two outputs serve different consumers without doubling maintenance.

## Components

- [`rfa-checklist-extraction-udm@0.1.0`](../../components/rfa-checklist-extraction-udm/) — the sole component. The component itself emits JSON for evaluation; this workflow's eight parallel Prompt tasks carry focused `prompt_inline` bodies in [`manifest.yaml`](manifest.yaml) that emit JSON fragments for clean step-input handoff, and the Consolidation step renders the final Markdown. **Note (v0.5.0):** the workflow prompts have moved ahead of the component (Red Flags task, recurring-date resolution, richer eligibility); the component `prompt.md` / `schema.json` are a pending sync — see CHANGELOG.

## A/B test sibling

- [`rfa-checklist-extraction-md`](../rfa-checklist-extraction-md/) — same final Markdown deliverable, but the parallel tasks emit Markdown chunks (already wearing their target section's heading) and the Consolidation step glues them rather than parsing JSON. Comparing the two workflows' outputs against the same RFA tells us which mid-pipeline format produces more reliable deliverables.

## Validation plan

Carried into the Vandalizer export at the workflow level (re-targeted for the Markdown deliverable):

| Check | Type | Severity |
|---|---|---|
| `CHK-01` Eleven sections present | completeness | error |
| `CHK-02` Placement contract enforcement (incl. Red-Flags pointer exception) | consistency | warning |
| `CHK-03` Monetary amount preservation | format | error |
| `CHK-04` Eligibility completeness | completeness | warning |
| `CHK-05` Red Flags section grounded (escalation + CRU triggers; VERAS action) | accuracy | warning |
| `CHK-06` Compliance & International sections grounded | accuracy | warning |

## Eval posture

Workflow-local — see [`evals/`](evals/). The workflow's deliverable is Markdown, so workflow-local cases use `expected.md` rather than `expected.json`. The component-level evals at [`components/rfa-checklist-extraction-udm/evals/`](../../components/rfa-checklist-extraction-udm/evals/) remain the JSON-against-schema test for the harness.

Workflow-local cases should target the nine-section presence (Red Flags first), the placement contract enforcement during consolidation (any cost-sharing inadvertently mentioned by extract-award-information should be moved to BUDGET REQUIREMENTS & POLICIES; per-component formatting in SPECIAL REQUIREMENTS should be moved onto the matching component row), monetary preservation, and IMPORTANT NOTES synthesis.

## Recommended knowledge bases

The workflow ships without a Knowledge Base step (removed in v1.0.0 — it was inert on import because Vandalizer blanks `kb_uuid` by design). When adding a `KnowledgeBaseQuery` step manually in Vandalizer (post-import), the following institutional knowledge bases provide useful context:

- **Primary:** OMB Uniform Guidance (2 CFR 200)
- **Agency-specific (attach the one(s) that match the RFA's sponsor):** NSF PAPPG Reference, NIH Grants Policy Statement, DOE Financial Assistance Rules, DOD Research Funding & DFARS
- **When proposal has human subjects:** Human Subjects Protection (Common Rule)
- **When research-security-relevant:** Export Control (EAR & ITAR)


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

## Evaluation (Plan A / B)

This workflow is evaluated under two complementary plans; evidence lives in [`AI4RA/evaluation-data-sets`](https://github.com/AI4RA/evaluation-data-sets/tree/main/evaluation_results/rfa-checklist-extraction):
- **Plan A** — large-scale, silver-referenced study of the extraction tasks (135 RFAs × v2/v3 OCR representations × 10 reps) via the evaluation-harness.
- **Plan B** — human-gold, end-to-end evaluation of the shipped workflow on 20 curated RFAs (paired **v0.4.0 → v3.1.0**), scored per field against a hand-authored answer key → `evaluation_results/rfa-checklist-extraction/plan-b/` (gold currently DRAFT / pre-verification).
