# AI4RA Prompt Library Agent Guide

This repository is the prompt-library leg of the AI4RA triad. It owns prompts, skills, agents, schemas, and component contracts.

## Read order

1. `README.md`
2. `TRIAD.md`
3. `triad.workspace.yaml`
4. `component_catalog.json`
5. `component_catalog_overrides.yaml`
6. `docs/contracts.md` and `docs/ecosystem.md`
7. the specific `components/<slug>/` directory you are changing

## Default scope

- Start in this repository first.
- Do not read all triad repos by default.
- Open sibling repos when the task touches dataset expectations, harness vendoring or discovery, shared UDM scope, or observed upstream refs.

## Contract boundaries

- `component_catalog.json` is the repo-level machine discovery surface.
- `component_catalog_overrides.yaml` is the editable source for repo-level triad metadata and observed upstream refs.
- `components/<slug>/schema.json` is authoritative for that component's structured output contract when present.
- `workflows/<wf-slug>/manifest.yaml` is the authored source for a Vandalizer-workflow manifestation; the sibling `<wf-slug>.vandalizer.json` is generated and must not be hand-edited.
- A `-udm` suffix in a component slug does not automatically mean the checked-in schema is the shared UDM contract from `ui-insight/AI4RA-UDM`.
- Record contract scope explicitly as repo-local, UDM-aligned repo-local, delegated wrapper, or shared UDM backed.

## Cross-repo triggers

Open `AI4RA/evaluation-data-sets` when:

- a component contract change affects expected outputs, golden cases, or dataset-side validation language
- a dataset relationship or scoring reference described in this repo changed
- observed dataset refs need to be refreshed

Open `AI4RA/evaluation-harness` when:

- vendored prompt snapshots, harness discovery, or runnable dataset registration needs to reflect a new component state
- harness-local scoring surfaces or catalog notes mention a changed component contract
- observed harness refs need to be refreshed

Open `ui-insight/AI4RA-UDM` when:

- the change depends on a shared UDM field definition or contract boundary
- you need to prove a schema is shared UDM rather than only UDM-aligned repo-local

## Validation

Run the commands that match your change:

```bash
python3 scripts/build_component_catalog.py
python3 scripts/build_vandalizer_workflows.py
python3 .github/scripts/lint_components.py
python3 scripts/build_docs.py
python3 -m mkdocs build --strict
```

## Editing rules

- Keep human-facing docs, component manifests, and `component_catalog.json` aligned in the same change.
- Prefer pinning observed upstream SHAs over floating branch names.
- When a change is repo-local only, say that clearly instead of implying wider harness, dataset, or UDM support.

## Workflow testing log (v0.2.0 → PR baseline)

This log tracks per-workflow version changes since the v0.2.0 Variant A
rollout. Each entry captures what changed in each bump, what surfaced
the change (test artifact + bug observed), and the current test status
against a real input document. The eventual PR description should
summarize these notes at submission time.

**Maintenance protocol** — when a workflow's manifest version is
bumped, append a `#### vX.Y.Z → vA.B.C` subsection under that
workflow's heading capturing: (1) the input document the test was run
against, (2) the exact bug or symptom observed, (3) the prompt /
manifest changes applied. Keep it specific — the goal is that a fresh
session can reconstruct *why* every change happened without re-running
the experiments.

**Branch**: `claude/nifty-heyrovsky-3cef48`. Local commits only — no
push without explicit user approval.

**KB attached for all tested workflows**: OMB Uniform Guidance (2 CFR
200). Cost Accounting Standards (CAS) considered but skipped — only
relevant for CAS-covered institutions with >$50M in federal R&D
awards and complex cost-allocation triggers, which none of the test
packages exercise.

### `workflows/ffr-management-extraction`

**Status**: ✅ Confirmed working end-to-end on BLM Rominger NoA.

#### v0.2.0 → v0.3.0 (2026-05-27)

**Test input**: `NoA - Rominger - BLM (2)_FLAT.pdf` (32 pages, DOI/BLM
Notice of Award L24AC00293 with explicit Federal Financial Report
Cycle and Performance Progress Report Cycle tables).

**Bug surfaced**: FFR cadence fields (`annual_ffr_due`,
`final_ffr_due`, `pi_name`) returned "Not specified" even though the
document contained the data — the v0.2.0 extraction prompt anchored
the LLM to relative-day-count policy language ("90 days after period
end") and didn't recognize the explicit FFR Cycle table format.
`pi_name` failed because the NoA uses "Grantee Project Director"
rather than "PI".

**Changes**:
- Extraction prompt now recognizes BOTH cadence formats: (A) relative
  day-count policy language and (B) explicit FFR Cycle TABLE
  (BLM/DOI/USDA/DOE format).
- New `ffr_schedule_table` JSON array captures the explicit table
  verbatim. `annual_ffr_due` and `final_ffr_due` derive from this
  table when relative language is absent.
- `pi_name` recognizes "Grantee Project Director", "Project
  Director", "PD", "Recipient Project Manager", "RPM" as PI synonyms.
- `submission_system_platform` enum extended with "GrantSolutions"
  and "ezFedGrants" (DOI / USDA portals).
- Consolidation prompt adds an `## FFR REPORTING CYCLE` table section
  that renders `ffr_schedule_table` when present and is omitted
  entirely when empty.
- Final row of the FFR Cycle table is bolded.

### `workflows/rfa-checklist-extraction`

**Status**: ✅ v2.0.x CONFIRMED end-to-end on THREE documents:
BLM Idaho Wildlife FOA L24AS00123 (v0.2.0 baseline), NSF 22-603
Mid-Career Advancement (v2.0.0, simple mandated structure — 3
flat sections), and NSF 25-541 PCL Test Bed (v2.0.0, complex
mandated structure — 8 sections, 5 nested sub-parts, 6-milestone
timeline; the document that drove the v0.8.0→v2.0.1 arc). The
PCL confirmation run (2026-08-13, after the operator raised model
token limits): all 10 fragments valid minified JSON, zero salvage
needed, backbone stubs rendered, full award amount preserved,
placement contract enforced, deliverable complete with clean
ending. Historically also used as the reference architecture for
the FOA Checklist v0.3.0 consolidation rewrite.

**Test input**:
`C:\Users\lehsan\Documents\Sample_FOAs\BLM\1_Foa_Content_of_L24AS00123.pdf`
(24-page BLM Idaho Wildlife Program NOFO L24AS00123).

**Confirmed output shape**: Full eight-section Markdown checklist
deliverable (Dates & Deadlines, Eligibility with both Institutions
and Individuals subsections, Award Information, Application
Components with required + optional sub-tables, Budget Requirements
& Policies, Submission Details, Special Requirements, Important
Notes). All 12 eligible-applicant institution types rendered as
bulleted entries with compliance sub-bullets. Final section's
Important Notes synthesized critical reviewer warnings from across
the seven fragments.

#### v0.7.0 → v0.8.0 (2026-08-13)

**Test input**: NSF 25-541 "Test Bed: Toward a Network of
Programmable Cloud Laboratories (PCL-Test Bed)" solicitation PDF
(26 pages), run on the v0.7.0-equivalent Vandalizer copy ("RFA
Checklist Extraction New (Copy)").

**Bug surfaced**: The solicitation's Section V.A supplements the
PAPPG with ten named Project Description sections (Science drivers;
Node capabilities with five numbered sub-parts incl. the Instrument
Inventory Table and its three required columns; Cross-Node
Collaborations; Training and education; Broadening access; Metrics;
Management Plan with a six-milestone Implementation Timeline; Plan
for Post-Award Continued Operation). The extraction compressed all
of it into one run-on `description` sentence plus the pointer
"Must include all specified subsections listed in Section V.A" —
the schema had no field to hold the enumeration, so the checklist
never surfaced the RFA-unique required sections.

**Changes**:
- `extract-application-components`: component objects gain
  `mandated_sections` ({name, requirements, subsections}) with
  enumeration rules (announcement order, names verbatim, sub-parts
  / table columns / milestones spelled out), an explicit ban on
  pointer-only phrasing, and a WRONG vs CORRECT worked example
  where the WRONG side is the literal failing NSF 25-541 output
  and the CORRECT side enumerates all ten sections.
- `rfa-checklist-consolidation`: renders a "📋 Required structure:
  <Component>" block after the Required Components table for each
  component carrying `mandated_sections`; the component's Special
  Requirements cell appends "See required structure below.";
  placement contract rule 6 keeps the enumeration out of top-level
  SPECIAL REQUIREMENTS. Block omitted entirely when no component
  has mandated structure.
- `validation_plan`: new CHK-07 (mandated structure enumerated;
  FAIL on pointer substitution).
- Re-test pending: re-import v0.8.0 JSON, re-run on NSF 25-541,
  verify all ten sections render; also spot-check a
  structure-free RFA to confirm the model doesn't invent
  structure from the sponsor backbone (rule: mandated_sections
  null unless the announcement prescribes it).

#### v0.8.0 → v1.0.0 (2026-08-13)

**Not a test-surfaced bug — user decision.** MAJOR bump: removed
the optional Knowledge Base lookup Step 0 (added v0.4.0). The RA's
live Vandalizer copy never carried it, KBs are never auto-wired on
import anyway (Vandalizer blanks kb_uuid by design, so the step was
inert until an operator manually attached a KB), and the extra step
confused comparison between the repo-built JSON and the live copy.
Extraction tasks now read input_sources: [workflow_documents] only
(vestigial step_input removed); consolidation unchanged; no prompt
changes; validation_plan unchanged. Operators can still add a
KnowledgeBaseQuery step manually post-import, per the README's
Recommended knowledge bases section. The pending v0.8.0 NSF 25-541
re-test should be run against this v1.0.0 JSON instead.

#### v1.0.0 → v1.1.0 (2026-08-13)

**Test input**: NSF 25-541 (PCL Test Bed) solicitation PDF, two
in-Vandalizer runs of the v1.0.0-equivalent workflow.

**Bug surfaced**: hard output-token caps in Vandalizer (operator
cannot raise them) truncated LLM output mid-string in both runs,
at different pipeline stages depending on model assignment:
- Run 1: extraction complete (~11K-char components fragment), but
  the consolidation deliverable cut at ~9.3K chars — mid-sentence
  inside the Required-structure block; everything downstream
  (mandated sections 3–8, Optional Components, Formatting,
  Compliance, Foreign Influence, Special Requirements, Important
  Notes) missing.
- Run 2 (user changed model assignment): consolidation completed,
  but the extract-application-components fragment itself cut at
  ~4.9K chars mid-way through the Implementation Timeline string —
  unparseable JSON; the deliverable lost the backbone components
  (1-row Required Components table), submission_details,
  formatting_requirements, and the last two milestones. The
  consolidation LLM salvaged the parseable prefix gracefully.
  Separate model-quality note: run 2's model found BABA + CHIPS
  §10636 CRU triggers (better than run 1) but returned empty
  allowable_costs (worse than run 1).

**Changes** (output-token economy, since caps are not adjustable):
- All 9 extraction tasks: "Output compactness (CRITICAL)" block —
  minified single-line JSON (run-2's pretty-printed fragment spent
  ~35% of its budget on indentation); in-prompt examples flagged
  as indented-for-readability-only.
- extract-application-components: scalar keys emitted first, then
  Announcement-sourced components (with mandated_sections) before
  backbone rows, so any future cap-hit clips low-value tail
  content; null component keys omitted; backbone descriptions
  ≤12 words; mandated_sections requirements ≤~30 words with the
  hard rule "compress wording, never drop an enumerated item".
- Consolidation: told fragments arrive minified / reordered /
  null-keys-omitted, and to salvage truncated or malformed
  fragments field-by-field rather than discarding.
- Re-test pending: re-import v1.1.0, re-run NSF 25-541 under the
  run-2 model assignment; verify the components fragment parses,
  the Required Components table has all backbone rows, and all
  six Implementation Timeline milestones survive.

#### v1.1.0 → v1.2.0 (2026-08-13)

**Test input**: NSF 25-541, in-Vandalizer run of imported v1.1.0
(run 3).

**Bugs surfaced**: v1.1.0's minification WORKED (components
fragment parsed at 4,851 chars minified; scalar-first ordering
held; all 8 mandated sections, 5 subsections, and all 6
Implementation Timeline milestones survived; Submission Details
and Formatting Requirements populated). But the compactness block
itself caused two regressions:
1. extract-risk-flags returned conversational PROSE ("Since no
   specific question or JSON schema was provided... I'm ready to
   format or extract exactly what you need") — the block was
   appended AFTER the ## Output schema, became the final
   instruction, and the weak model lost the schema entirely. The
   deliverable rendered the false empty-state "✅ No red flags
   identified", hiding the real limited-submission and AOR flags
   as clear. Worst failure mode of the three runs.
2. Backbone dropped: required_components contained ONLY Project
   Description (10 standard components + 4 optional missing);
   the "spend budget on announcement-specific content" framing
   over-steered. Also award task over-compressed content ("Up to
   $5M/year for 4 years" → "$20M per PCL Node").
3. Consolidation clipped its final Important Notes line at the
   output cap (~10.5K chars) even without backbone rows.

**Changes**:
- All 9 tasks: compactness block relocated BEFORE ## Output (the
  schema is always the final instruction); every prompt now ends
  with an anti-chat anchor ("Begin your reply with `{` ... no
  questions, no offers to help, no commentary").
- Generic block gains "minify the SYNTAX only — never shorten,
  summarize, or drop content values" with the observed award-
  amount over-compression as the example.
- Components task: backbone components emitted as STUBS
  ({name, source} only, ~60 chars) with a NEVER-drop rule and
  run-3's backbone-less output as the WRONG example; description
  field spec updated (required only for Announcement-sourced
  components).
- Consolidation: stub rows render with "—" cells (no invented
  descriptions, no dropped rows); Important Notes 0–5 → 0–3.
- Re-test: verify RED FLAGS shows limited-submission + AOR +
  PI-meeting flags again, Required Components has all 11 rows
  (announcement + backbone stubs), and the deliverable reaches
  its final line without truncation.

#### v1.2.0 → v2.0.0 (2026-08-13)

**Bug surfaced**: importing/running v1.2.0 failed with "Model
token limit (8192) exceeded before any response was generated" —
no output at all. Arithmetic identified the culprit:
extract-application-components had accreted to ~20.8K chars
(~5.2K tokens) of prompt across the v0.8→v1.2 fix iterations;
prompt + attached document slice + reserved output budget
exceeded the extraction model's total 8192-token window, so the
call was rejected upfront. The consolidation is NOT affected —
it consumed ~7.5K input tokens and produced ~2.6K output tokens
in runs 3–4, so it runs on a larger-context assignment.

**Changes** (MAJOR — parallel tasks 9 → 10):
- New task extract-mandated-structure owns the
  announcement-mandated internal structure extraction
  ({mandated_structure:[{component, mandated_sections}]}, empty
  array when none) with the v0.8.0 enumeration rules + pointer
  ban + a compact worked example (~4.5K chars).
- extract-application-components rewritten without the
  mandated-sections content: backbone merge + stubs +
  compactness only, 20.8K → 9.5K chars (~2.4K tokens).
- Consolidation reads TEN fragments; the Required-structure
  block + table pointer source from fragment 10 (matched on
  component name).
- Deliverable and validation_plan unchanged.
- Lesson recorded: with an 8192-token extraction model, keep
  every extraction prompt ≤ ~2.5K tokens (~10K chars) — the
  document slice + output reservation consume the rest. Check
  prompt sizes BEFORE import when iterating.
- Re-test pending: same NSF 25-541 checklist as v1.2.0 (real
  red flags, 11-row components table, full award amount, clean
  ending) plus: mandated-structure fragment populates with all
  ten sections and the components fragment carries the backbone
  stubs.

#### v2.0.0 → v2.0.1 (2026-08-13)

**Test input**: NSF 22-603 Mid-Career Advancement (MCA)
solicitation — a NEW test document (generalization test), run
after the operator (John) raised the model token limits.

**Result: first fully clean end-to-end run.** All ten fragments
emitted minified (no chatting, no truncation, no token errors);
backbone stubs rendered as "—" rows with announcement-modified
components first; mandated-structure fragment captured the three
MCA-mandated Project Description sections (Candidate's Past
Research; Research Advancement and Training Plan; Long-Term
Career Plans); red flags correct (commitment letter + AOR
flagged, limited submission clear); consolidation enforced the
placement contract unprompted (dropped the cost-sharing item
from Special Requirements because Budget owns it); deliverable
ended cleanly.

**One residual defect → v2.0.1**: extract-mandated-structure
quoted announcement text with unescaped double quotes
("mutual benefits/\"added value\" of collaboration"),
invalidating its fragment's JSON. The consolidation's salvage
rule recovered every section, so the deliverable was unaffected
— but the fragment should parse. PATCH: all ten extraction
prompts now carry an explicit escape-or-rephrase rule for double
quotes inside JSON string values. No other changes.

#### v2.0.0 PCL confirmation run (2026-08-13)

**Test input**: NSF 25-541 PCL Test Bed — the complex-structure
document that drove the entire v0.8.0→v2.0.1 arc — re-run on the
v2.0.0 import under the raised token limits.

**Result: clean pass, workflow confirmed.** All 10 fragments
valid minified JSON (0 invalid, no quote-escaping issues even
without the v2.0.1 rule); mandated_structure carried all 8
sections + Node capabilities' 5 sub-parts + the 6-milestone
Implementation Timeline; Required Components table = 2
announcement-modified rows first + 9 backbone stubs; Optional
Components = Letters of Collaboration (with the
Letters-of-Support prohibition) + 3 stubs; award amount preserved
in full ("Up to $5M/year for 4 years... $20M"); placement
contract enforced (cost-sharing item dropped from Special
Requirements, carried in Budget); deliverable ends cleanly at
3 Important Notes. Run-to-run variance note: this run's
risk-flags returned "unclear" for AOR/signature (a prior run said
"yes"); the grounding rule correctly kept it un-flagged rather
than guessing — acceptable behavior, not a defect.

#### v2.0.1 → v3.0.0 (2026-08-13)

**Not a test-surfaced bug — operator feature request.** Two asks,
both verified feasible against the ui-insight/vandalizer backend
source (schemas/workflows.py, services/export_import_service.py,
services/workflow_engine.py) before implementing:
1. Parallel Extraction step now sets is_output: true → the raw
   JSON fragments surface as a workflow deliverable alongside
   the Markdown checklist. Vandalizer supports multiple output
   steps (import preserves per-step is_output;
   output_step_names is a list); the "at most one output step"
   constraint was our build script's, now relaxed to "at least
   one".
2. New workflow-level manifest key default_task_model:
   VandalStrong → build script emits "model": "VandalStrong"
   into every task's data. Engine precedence is
   task_data["model"] or run_model (task wins), so the pin
   overrides the run dialog's picker. Name must EXACTLY match a
   server available_models[].name entry; per-task model: can
   override the default; Vandalizer's optimizer per-step
   overrides can still swap models after the pin.
MAJOR per this workflow's semver (is_output change). No prompt
changes — re-test only needs to confirm both steps appear as
deliverables and runs use VandalStrong regardless of the model
picked in the run dialog.

#### v3.0.0 → v3.1.0 (2026-08-18)

**Not a test-surfaced bug — feature rollback.** The
default_task_model: VandalStrong pin (v3.0.0 ask 2) was removed:
John could not confirm how to pin the model / what the real
server available_models[].name entry is, and an unmatched name
would point every task at a nonexistent model on import. Tasks
once again use the model chosen in Vandalizer's run dialog. The
dual-deliverable is_output change (v3.0.0 ask 1) is retained.
MINOR: manifest-key removal only — no step-structure, prompt, or
is_output changes. The build script keeps generic
default_task_model support for future use. Re-test only needs to
confirm both steps still appear as deliverables.

### `workflows/foa-checklist-extraction`

**Status**: ⚠️ v0.3.0 import-ready but not yet re-tested by user.

#### v0.2.0 → v0.3.0 (2026-05-27)

**Test input**: `1_Foa_Content_of_L24AS00123.pdf` (24-page BLM Idaho
Wildlife Program NOFO L24AS00123).

**Bug surfaced**: Full workflow runs failed at Step 3/3 Consolidation
with a Vandalizer "Connection error" while individual Step-2 Test
Step extractions and the consolidation Test Step both succeeded. The
sibling RFA Checklist workflow (which has *more* parallel tasks — 7
vs FOA's 6 — ruling out concurrency) ran end-to-end on the same input
PDF without issue. Consolidation Test Step output exhibited fidelity
bugs: dropped populated fields and verbatim PDF text appearing in
sections that had no corresponding JSON field, indicating the LLM was
losing track of what it was supposed to consume.

**Changes**: Consolidation prompt rewritten to mirror the working RFA
Checklist consolidation structure exactly.
- Enumerates all six JSON fragments and their fields up front (lines
  5–20 of the new prompt).
- Replaces terse "Bulleted list from X" instructions with explicit
  field-by-field templates per section.
- Adds a placement contract block routing each fact to exactly one
  section (funding only in Funding Information, eligibility only in
  Eligibility, etc.).
- Adds explicit anti-leakage anchor: "Use ONLY the six JSON fragments
  above. Do NOT reference the original uploaded document directly."
- Drops the static Table of Contents (markdown viewers render TOC
  automatically; static block consumed output tokens for no end-user
  benefit).
- Empty-state language tightened for every section.

### `workflows/budget-justification-generator`

**Status**: ✅ v0.5.0 confirmed working end-to-end on the **full
four-document HUD test package** (HUD RFP + HUD project narrative +
HUD-424-CBW XLS + Appendix E budget narrative). Earlier v0.4.1
"passing" tests used only three of the four documents (project
narrative was unchecked); those runs got every number right but
Section A descriptions were generic-academic because the LLM had no
project-narrative context. The four-document run produces Section A
prose that ties each investigator's effort to actual research
elements ("economic development theory and quality control" for
Stokan, "program-evaluation experience" for Ellison, "GIS and
data-management support... extensive spatial datasets" for Godfrey)
while preserving all numerical accuracy.

**Confirmed-passing baseline** (use this as the reference for all
four-document runs):
- All 4 personnel with effort hours + computed salary + per-person
  fringe in Personnel Summary Table.
- Section A narrative ties personnel roles to actual research
  topics drawn from the project narrative.
- Section G.1 Materials $207.20, G.5 Subawards $38,257.60 (with
  under/over $25K MTDC split), ODC Summary Total $38,464.80.
- Section H Indirect $74,230.57 (prime-only, no double-count).
- Total Direct $169,532.49, Total Project $243,763.06 with cents.
- All four Cross-Validation arithmetic checks PASS.

Minor cosmetic notes (not bugs):
- Budget Summary prose mentions "24-month period with two 12-month
  phases" but the table correctly renders as single-year Year 1
  with consolidated totals. The narrative's framing is awkward but
  the dollar amounts are right.
- Project Title: "Not specified in the document" — genuine
  document limitation; App E is "Appendix E: Budget Narrative,"
  HUD narrative just says "Grant Narrative," HUD RFP gives the
  program title not the applicant's project title.

#### v0.4.1 → v0.5.0 (2026-05-27)

**Generalization** (not a bug fix): User requested both budget
workflows be agency-agnostic. v0.4.x had "HUD-424-CBW" as the only
example of numbered-section budget format, making the workflows
feel HUD-specific even though most non-NSF / non-NIH federal grant
agencies use similar 10-section budget worksheets.

**Changes**:
- All four budget extraction tasks now reframe the format
  taxonomy with four explicit families:
  - (A) SF-424 R&R Budget (Detailed) — NIH, NSF, DOE-research,
    DOD-research, EPA-research; A-K letter-coded.
  - (B) SF-424A Budget Information (Non-Construction) — most
    non-research federal assistance.
  - (C) Numbered-section budget worksheets — HUD-424-CBW is one
    example; DOI, USDA, ED, EPA, HHS, DOE non-research, DOD
    non-research, cooperative-agreement variants all share the
    10-section structure.
  - (D) Narrative-only budgets.
- "For HUD-424-CBW specifically:" subsection headers replaced
  with "For numbered-section format specifically (HUD-424-CBW,
  DOI, USDA, ED, EPA, HHS, DOE non-research, DOD non-research,
  and cooperative-agreement variants):".
- Worked-example labels like "HUD-424-CBW four-investigator
  proposal" replaced with format-agnostic "numbered-section
  budget worksheet with hourly-rate personnel" framing.
- Worked-example dollar amounts and the University of Idaho /
  Towson University illustrative institutions kept — they're
  realistic universities, not HUD-specific.
- The has_subawards detection rule now reads "numbered-section
  format Section 7 (Contracts and Sub-Grantees) / SF-424 R&R
  line G.5 Subawards / NIH consortium line".
- YAML topology comments retained as historical documentation
  of which test surfaced which bug — internal record only,
  not in prompts.

**No behavioral change expected on the HUD test package** — the
LLM still sees the same content with the same logical structure;
just framed as one example among many rather than the primary
anchor.

**Four-document re-test (2026-05-27)**: confirmed v0.5.0 produces
identical numerical output to the three-document v0.4.1 baseline
when the project narrative is attached, AND produces richer
Section A prose tied to actual research topics from the narrative.
Two minor cosmetic-tier observations (not bugs):
1. Personnel Summary Table totals row showed grand total only
   ("TOTAL — — — — $131,067.69") in the four-doc run, vs. per-
   column subtotals ("Totals — — $104,104.60 $26,963.09
   $131,067.69") in the three-doc run. The consolidation prompt's
   totals instruction is ambiguous between these interpretations.
   Both are functionally correct.
2. FORMATTING ADVISORY admin cost cap rendered as "15% for the
   first $1 million" (truncated) vs. the more complete "15% of the
   first $1M and 10% above" in earlier runs. NOFO text in the
   FORMATTING ADVISORY block is paraphrased from the NOFO, so
   minor variance run-to-run is expected.

**Test input**: Same HUD test package as
`proposal-budget-personnel-extraction`
(`C:\Users\lehsan\Documents\Budget Generated Test Documents\` — HUD
RFP + HUD project narrative + HUD-424-CBW XLS + Appendix E budget
narrative).

#### v0.2.0 → v0.3.0 (2026-05-27)

**Bug surfaced**: Full workflow run produced:
- Sections A/B/C entirely blank ("Not specified in the document"),
  personnel summary table empty, project_title and pi_name missing
  from the header — Task 1 returned null for senior_key_personnel
  because the schema required `person_months` (NSF/NIH concept) and
  the HUD-424-CBW format uses hours.
- Section G.5 Subawards showed "$0" / "No costs are requested"
  despite the $38,257.60 Towson subcontract.
- Section G.1 Materials & Supplies showed "$0" despite the
  $207.20 Dallas appraisal data line item.
- Section H Indirect Costs: $86,274.65 (double-counted Towson's
  $12,143.20 sub-indirect into the prime's Section H) instead of
  the correct $74,230.57 (UI 47.5% on $156,274.89 MTDC base, prime
  ONLY).
- MTDC base used $156,067.69 (missing $207.20 supplies) instead
  of $156,274.89.
- Cascade: $157,389.29 direct (should be $169,532.49),
  $86,274.65 indirect (should be $74,230.57),
  $243,663.94 total (should be $243,763.06).
- Cross-Validation Notes section correctly caught three of these
  as FAIL (the workflow's self-check feature is working).

**Changes** (port of the v0.4.1 patterns from
`proposal-budget-personnel-extraction`, adapted to the 4-task
generator topology):

- `extract-personnel-and-fringe`: schema now accepts EITHER
  `person_months` OR `effort_hours` (HUD-424-CBW hourly-rate
  format), with explicit `hours * hourly_rate` computation rule
  and the worked example. PI synonym list added for `pi_name`.
  Subaward classification rules: Co-PIs at subawardee institutions
  LISTED in `senior_key_personnel[]` but EXCLUDED from
  `total_senior_personnel_cost` and `total_fringe_benefits` (their
  costs flow through G.5). Anti-double-count rules with
  CORRECT/WRONG worked examples ($104,104.60 prime personnel
  correct vs $128,284.60 with Stokan double-counted wrong).
- `extract-equipment-and-travel`: HUD-424-CBW Section 4
  (Equipment) and Section 3 (Travel) anchors. Zero-defaults for
  empty categories.
- `extract-participant-support-and-odc`: HUD-424-CBW Section 5
  (Supplies) → `materials_and_supplies` ($207.20 Dallas appraisal
  data line picked up). Section 7 (Contracts and Sub-Grantees) →
  `subaward_details` with per-institution aggregation. Subaward
  total formula: salary + fringe + sub-indirect = $38,257.60 for
  Towson. New `under_25k_mtdc` / `over_25k_mtdc` split fields
  passed to the indirect task for MTDC base computation. WRONG
  worked example showing $75,132.60 (the v0.2.0 pattern of
  including $25K threshold + prime's $11,875 indirect as subaward
  cost components) labeled wrong.
- `extract-indirect-and-summary`: Section H is PRIME indirect
  ONLY. Subawardee sub-indirect is part of the subaward total
  ($38,257.60 in G.5), NOT added to Section H. `prime_MTDC_base`
  FORMULA explicitly includes prime personnel + fringe + supplies
  + first $25K of each subaward (via `under_25k_mtdc` from task
  3). WRONG worked example showing the exact $86,274.65 pattern
  observed (UI indirect with missing supplies + Towson sub-indirect
  added). CORRECT example shows $74,230.57 prime-only derivation.
- `budget-justification-consolidation`: placement contract added
  (subaward costs ONLY in G.5; Section H ONLY prime indirect;
  equipment ONLY in D; travel ONLY in E). Anti-leakage anchor:
  "Use ONLY the four JSON fragments above. Do NOT reference the
  original uploaded documents directly."

#### v0.3.0 → v0.4.0 (2026-05-27)

**Bug surfaced**: v0.3.0 fixed personnel extraction, Section H
indirect math, and Budget Summary totals — all correct. Three
polish bugs remained:
- Personnel Summary Table tagged all four investigators as
  "Senior Personnel" instead of Overton=PI, Stokan=Co-PI;
  `pi_name` returned null. The prompt listed allowed roles but
  didn't tell the LLM how to pick when the document lacks
  explicit "PI" labels.
- Section G.1 Materials and G.5 Subawards both rendered "$0 / No
  costs are requested" despite the $207.20 supplies and
  $38,257.60 Towson subaward. Task 3 emitted empty arrays for
  `materials_and_supplies` and `subaward_details`, while Task 4
  correctly referenced both in its Section H narrative — the
  documents were visible to Task 4 but Task 3 didn't extract
  into its structured fields.
- Cross-Validation arithmetic check rendered as "Personnel &
  Fringe subtotal: FAIL ($104,104.60 + Not specified in the
  document + $26,963.09 = Not computable)" — the null
  `total_other_personnel_cost` cascaded into the check as text
  instead of being treated as $0.

**Changes**:
- Task 1 `extract-personnel-and-fringe`: explicit role-assignment
  heuristics added — PI = first-listed prime investigator OR
  named lead; Co-PI = lead at subawardee institution; Sub-PI =
  Co-PI variant; Senior Personnel = other prime contributors;
  Key Personnel = synonym. Worked HUD-424-CBW example tags
  Overton=PI, Stokan=Co-PI, Ellison=Senior Personnel, Godfrey=
  Senior Personnel.
- Task 3 `extract-participant-support-and-odc`: Section 5 and
  Section 7 recognition strengthened with explicit worked
  examples on the HUD test case data. The $207.20 example shows
  exact materials_and_supplies array contents. The $38,257.60
  Towson example shows the full subaward_details object with
  under_25k_mtdc / over_25k_mtdc split. WRONG examples show
  empty-array emissions that would cause G.1 / G.5 narratives
  to say "No costs are requested" when sections in fact have
  non-zero rows.
- Consolidation: null-handling rule for arithmetic checks.
  total_other_personnel_cost = null is treated as $0 for
  PASS/FAIL math. CORRECT vs WRONG examples show the
  $0-substitution producing PASS vs the "Not specified"
  rendering producing "Not computable".

#### v0.4.0 → v0.4.1 (2026-05-27)

**Bugs surfaced (two re-tests showed non-deterministic behavior
across runs)**:
- **Run 1**: Section H correct ($74,230.57); Section F and G
  narratives null → "Not specified"; Other Direct Costs Summary
  all $0; Personnel Summary Table Fringe column inconsistent.
- **Run 2**: Section F and G narratives correct; G.1 $207.20 and
  G.5 $38,257.60 populated; Section H REGRESSED to v0.2.0
  double-count pattern — used $128,284.60 personnel + $28,897.49
  fringe in MTDC base (= all 4 investigators + all fringe), MTDC
  base $182,389.29 instead of correct $156,274.89, yielding
  $86,634.91 indirect and $282,281.80 total project cost.
- **Both runs**: Cross-Validation "Total Direct Costs" check
  formula was wrong — compared Personnel+Fringe-only against the
  stated total direct cost rather than (Personnel+Fringe +
  Non-personnel direct). Personnel Summary Table Fringe column
  emitted "—" for some/all people instead of computed per-person
  fringe values.

**Changes**:
- Task 4 `extract-indirect-and-summary`: ported the anti-
  double-count anchor from `proposal-budget-personnel-extraction`
  v0.4.1. Three explicit rules: (a) MTDC base personnel is PRIME
  ONLY, exclude subawardee Sub-PI / Co-PI salaries; (b) MTDC base
  fringe is PRIME ONLY; (c) self-check that no subawardee
  salary/fringe is in your MTDC base. WRONG worked example uses
  the exact Run 2 cascade ($128,284.60 / $28,897.49 / $182,389.29
  / $86,634.91) labeled wrong. CORRECT example shows
  $104,104.60 / $26,963.09 / $156,274.89 / $74,230.57.
- Task 3 `extract-participant-support-and-odc`:
  section_f_narrative and section_g_narrative are now declared
  NEVER null with explicit default templates. The G.1-G.9 default
  template is written out verbatim in the prompt so the LLM
  copy-pastes when categories are empty, eliminating Run 1's
  null-narrative failure mode.
- Consolidation: Total Direct Costs cross-validation formula
  fixed. Was: "P = total_direct_costs" (wrong — P is Personnel &
  Fringe only). Now: "P + N = total_direct_costs" where
  P = Personnel & Fringe and N = Non-personnel direct (equipment
  + travel + participant + ODC). Explicit Fringe-column rendering
  rule added: derive per-person fringe by matching the person's
  institution to fringe_benefit_rates[] entries. Worked example
  shows Stokan at Towson 8% on $24,180 = $1,934.40; Overton at UI
  25.9% on $52,947 = $13,713.27.

**Note on non-determinism**: the in-house model is producing
different outputs on the same prompt + same inputs across runs.
v0.4.1 reduces the surface area for this by adding stronger
anchors at the specific points where the LLM diverges. The same
pattern (worked CORRECT + WRONG example for the precise
mistake observed) that resolved double-counting in
`proposal-budget-personnel-extraction` is what we're applying
here.

### `workflows/proposal-budget-personnel-extraction`

**Status**: ✅ Confirmed working end-to-end on HUD test package
(every field correct after 3 iterations).

**Test input**: HUD test package at
`C:\Users\lehsan\Documents\Budget Generated Test Documents\`:
- `HUD RFP (2).pdf` (47-page HUD NOFO FR-6100-N-29, sponsor RFA)
- `HUD narrative Final (2).pdf` (25-page Grant Narrative on CDBG)
- `HUD Budget Final (2).xls` (HUD-424-CBW Detailed Budget Worksheet,
  246 rows, $243,763.06 total)
- `App E (1).pdf` (1-page Appendix E budget narrative)

**Proposal characteristics**: 4 senior key personnel (Overton PI,
Ellison + Godfrey Senior Personnel at U of Idaho; Stokan Co-PI at
Towson via subcontract). UI direct + fringe = $131,067.69. Towson
subaward = $38,257.60 (Stokan salary $24,180 + 8% fringe $1,934.40 +
46.5% Towson indirect on $26,114.40 = $12,143.20). UI 47.5% MTDC
indirect on $156,274.89 base ($131,067.69 personnel + $207.20
supplies + first $25K of $38,257.60 subaward) = $74,230.57. Total
$243,763.06. No trainees, no equipment ≥ $5K, no foreign travel, no
cost share. Single-year.

#### v0.2.0 → v0.3.0 (2026-05-27)

**Bug surfaced**: First test run returned multiple errors —
salary/effort columns empty, Stokan misclassified as "Key Personnel"
with no institution, Subaward Commitment Forms flag ❌ No, missing
all budget totals, "Multi-year (2 periods)" hallucinated on a
single-year HUD-424-CBW form, `undergraduates` returned null instead
of 0.

**Changes**:
- `extract-personnel-identification` now handles both budget formats
  explicitly: (A) FTE/months-of-effort (NSF/NIH) and (B)
  hours-times-hourly-rate (HUD-424-CBW, DOI/BLM, USDA) with explicit
  `hours * hourly_rate` computation rule and worked example.
- Adds subaward / subcontract classification rules with three
  signals: HUD-424-CBW Section 7 line, narrative "subcontract with
  X" language, different institution + different fringe/indirect
  rate.
- Subaward Co-PIs / Sub-PIs go in `senior_key_personnel[]` with
  their **subawardee** institution AND their cost goes in
  `subawards[]`.
- `undergraduates` defaults to integer `0`, never null.
- `extract-budget-structure-and-triggers` anchors HUD-424-CBW format
  with all 10 numbered sections, "Subtotal of Direct Costs" /
  "Total Indirect Costs" / "Total Estimated Costs" totals line
  recognition.
- Zero-default rules ("$0" not null when category has no line
  items).
- Single-year default when budget periods are ambiguous.
- Consolidation prompt: RFA-style structural improvements (fragment
  enumeration, placement contract, anti-leakage, "$0" defaults for
  empty category totals).

#### v0.3.0 → v0.4.0 (2026-05-27)

**Bug surfaced**: Re-test showed personnel/subaward classification
fixed (Stokan now Sub-PI at Towson, subaward flag ✅), but budget
totals still wrong:
- `total_personnel_cost` = $104,104.60 (Direct Labor only) instead
  of $131,067.69 (Direct Labor + Fringe).
- `subaward_costs_total` = $75,132.60. The LLM misread the
  narrative phrase "first $25,000 of our subcontract" as a separate
  subaward cost line AND rolled UI's 47.5% indirect on that $25K
  into the subaward. Correct value: $38,257.60.
- `total_direct_costs` and `total_indirect_costs` returned null —
  prompt named the totals lines but didn't tell the LLM what to do
  if they weren't visible in extracted text.

**Changes**: `extract-budget-structure-and-triggers` adds five
explicit FORMULA sections with worked-arithmetic examples:
- `total_personnel_cost`: Direct Labor + Fringe formula with worked
  example ($104,104.60 + $26,963.09 = $131,067.69).
- `subaward_costs_total` with explicit `$25K threshold`
  disambiguation: narrative "first $25,000 of the subcontract"
  describes the PRIME's MTDC base for ITS OWN indirect calculation,
  not a subaward cost line. Worked example for Towson = $38,257.60.
- `total_direct_costs`: priority order — read totals line if
  present, otherwise compute formula, NEVER emit null.
- `total_indirect_costs`: same priority pattern with MTDC base
  exclusion rules (subaward amounts BEYOND first $25K excluded from
  prime base).
- `total_project_cost`: priority pattern with cents preserved.

#### v0.4.0 → v0.4.1 (2026-05-27)

**Bug surfaced**: Third re-test fixed the subaward total
($38,257.60 ✓) but introduced a cascading double-count. The LLM
included Stokan's salary+fringe ($26,114.40) in BOTH
`total_personnel_cost` (with UI personnel) AND in the
`subawards[].amount`. Cascade produced:
- `total_personnel_cost` = $157,182.09 (= correct $131,067.69 +
  $26,114.40 Stokan double-count)
- `total_direct_costs` = $195,646.89 (formula correct, inputs wrong)
- `total_indirect_costs` = $86,634.91 (MTDC base inflated by
  Stokan)
- `total_project_cost` = $282,281.80

**Changes**: `total_personnel_cost FORMULA` section expanded with
three explicit anti-double-count rules:
- (a) Add Direct Labor AND Fringe, not Direct Labor alone.
- (b) EXCLUDE compensation for any person classified as Sub-PI /
  Co-PI at a SUBAWARDEE institution. Their salary, fringe, and
  sub-indirect are already captured in `subawards[]` /
  `subaward_costs_total`. Including them in
  `total_personnel_cost` would double-count.
- (c) Self-check: "if any subaward person's salary or derived
  fringe is also represented inside your total_personnel_cost,
  you have double-counted. Subtract them out."

Side-by-side WRONG and CORRECT worked examples added so the LLM can
pattern-match its own potential failure before emitting it. The
WRONG example uses the exact $157,182.09 number from the
v0.4.0 failure, annotated with why it's wrong.

**Methodology note**: Showing the LLM the exact wrong answer it
produced (labeled "WRONG", with arithmetic), alongside the correct
derivation (labeled "CORRECT"), was the technique that resolved
this. Telling it "don't double-count" in the abstract wasn't enough.

#### v0.4.1 → v0.5.0 (2026-05-27)

**Generalization** (not a bug fix): same agency-generalization
patch as `budget-justification-generator` v0.5.0 — see that entry
for the four-family format taxonomy expansion. Applied to both
extraction tasks (`extract-personnel-identification` and
`extract-budget-structure-and-triggers`) plus the consolidation.
Worked-example dollar amounts and institutional names (University
of Idaho, Towson University) kept; "HUD-424-CBW" references
reframed as one example within a numbered-section format family
that includes DOI/BLM, USDA, ED, EPA, HHS, DOE non-research, DOD
non-research, and cooperative-agreement variants. NSF-specific
budget workflows (workflows/nsf-budget-*) remain the dedicated
path for NSF proposals. No behavioral change expected on the HUD
test package.

### `workflows/risk-domain-assessment`

**Status**: ⚠️ v0.3.0 import-ready, awaiting re-test on the HUD
test package. v0.2.0 was tested on the 4-document HUD package and
produced four contradictions against the workflow's own
verification.html spec; v0.3.0 patches all four.

**Test input**: HUD 4-document package (HUD RFP + HUD project
narrative + HUD-424-CBW XLS + Appendix E).

**Reference spec**:
`C:\Users\lehsan\Documents\Process_Mapping_Claude_Git\workflows\risk-domain-assessment\verification.html`
— this is the source of truth for the 14 domain rubrics, the
output structure, and the consolidation instructions. v0.3.0
prompts were brought into alignment with this spec.

#### v0.2.0 → v0.3.0 (2026-05-27)

**Bugs surfaced (test against 4-document HUD package)**:

1. **Award metadata all "Not specified"**: Award, Sponsor, PI,
   Period (Start/End) all returned "Not specified in the document"
   even though documents clearly contained them (HUD sponsor in
   RFP; Dr. Michael Overton named as PI in budget + narrative; the
   verification.html spec marks these REQUIRED outputs at lines
   374-380). Same PI synonym issue we fixed in
   proposal-budget-personnel-extraction v0.3.0.
2. **Domain 9 polarity INVERTED**: LLM scored "Directly supports
   HUD's CDBG impact evaluation goals, strong mission fit" as
   5/5 — but the rubric (verification.html line 475-481) says
   5 = "Clear misalignment; significant mission conflict". Strong
   fit → score 1. Root cause: v0.2.0 prompt didn't include the
   rubric table, LLM defaulted to "higher = better" training
   prior. This is the most user-visible contradiction in the
   output (a perfectly mission-aligned project tagged as the
   maximum-risk-of-misalignment).
3. **Funding amount $950,000 vs proposal $243,763.06**: LLM
   grabbed program-wide RFP total ("$950,000 in program-wide
   funding for two awards") instead of the proposal-specific
   budget ($243,763.06 from HUD-424-CBW).
4. **Domain 14 missing from DETAILED EVIDENCE section**: Domain
   14 score (3/5) appeared in the score table but had no detail
   block. Output stopped at Domain 13. Verification spec line
   1213-1215 requires all 14 in detail.

Additional contradiction with verification.html: v0.2.0 prompts
said "score conservatively (1 or 2)" when evidence is weak, but
verification.html line 511 says "lean toward the middle of the
scale rather than guessing". The previous default undershoots
risk; the new default matches the verification's intent of
conservative-toward-moderate when evidence is weak.

**Changes**:

- **All 6 extraction prompts** now include the full rubric table
  (1-5 score levels with criteria) inline, pulled verbatim from
  verification.html. The LLM no longer has to guess any rubric.
- **Task 1 (extract-programmatic-strategic)** adds an explicit
  "POLARITY REVERSED" warning before the Domain 9 rubric plus a
  WRONG/CORRECT worked example: "strong mission fit → score 1,
  NOT score 5". Also adds the PI synonym list ("Principal
  Investigator", "PI", "Project Director", "PD", "Lead
  Investigator", "Grantee Project Director", "Grantee Project
  Manager", "Recipient Project Manager", "RPM") and a
  proposal-only-context fallback (when no explicit PI label,
  designate first-listed prime investigator).
- **Task 2 (extract-financial-audit)** adds a funding-amount
  disambiguation section with the exact $950K-vs-$243K HUD test
  example labeled CORRECT vs WRONG.
- **Task 3 (extract-subrecipient-sponsor)** adds a note that ANY
  subaward (e.g., a single domestic university subcontract) is
  at least score 2, not 1.
- **Task 4 (extract-security-compliance)** clarifies that standard
  cross-cutting federal requirements alone don't elevate
  Domain 5 above 2.
- **Task 6 (extract-data-sustainability-reputational)** adds a
  CRITICAL anchor: ALL FOUR domains (10, 11, 12, 14) MUST be
  populated. Domain 14 is the final required domain.
- **Consolidation** adds award-metadata-fallback logic for
  proposal-only contexts (Award = "Pending (FAIN not yet
  assigned; proposed under <RFP/FOA number>)", PI from Task 1's
  pi_name with synonym handling, Sponsor from RFP) plus an
  explicit "ALL 14 domains MUST appear in DETAILED EVIDENCE"
  rule with an emit-default for missing Domain 14 ("Score: ?/5
  / Insufficient evidence").
- **"Score conservatively (1 or 2)" default** replaced with
  "lean toward the middle (3)" to match verification.html line
  511.

**Expected output on re-test** (HUD 4-doc package):
- Award: "Pending (FAIN not yet assigned; proposed under HUD
  FR-6100-N-29)"
- Sponsor: "U.S. Department of Housing and Urban Development"
  (or "HUD")
- PI: "Dr. Michael Overton"
- Funding: "$243,763.06" (not $950,000)
- Domain 3 (Subrecipient): score 2 (one Towson subaward), not 1
- Domain 9 (Strategic Alignment): score 1 (strong fit; HUD-funded
  project supporting HUD's CDBG impact evaluation mission)
- Domain 14 (Reputational): present in DETAILED EVIDENCE with
  score + justification
- All other domain scores preserved (no behavioral changes
  expected for domains 4, 6, 8, 10, 11, 13 — those already had
  evidence-based scoring)

### `workflows/award-compliance-extraction`

**Status**: ✅ Output confirmed working on BLM `BLM_Award.pdf`
(L24AC00293). ⚠️ v0.2.1 validation-plan rework import-ready but the
in-Vandalizer **Validate** re-test is still pending.

**UDM conformance (verified 2026-06-05)**: component
`award-compliance-extraction-udm` declares contract scope
**"repo-local, UDM-aligned"** (NOT shared-UDM-backed). Every UDM
binding in its `schema.json` was checked against the live
`ui-insight/AI4RA-UDM` data dictionary (40 tables) and all exist:
`Award.Federal_Award_ID`, `Award.Current_Total_Funded`,
`Terms.{Reporting_Requirements, Property_Requirements,
Special_Conditions, Record_Retention_Years}`, `AwardBudget`,
`AwardBudgetPeriod`, `AwardDeliverable`, `CostShare.Committed_Amount`,
`IndirectRate.{Rate_Percentage, Base_Type}`,
`Modification.Requires_Prior_Approval`. Conformance is accurate.

#### v0.2.1 → v0.2.2 (2026-06-06) — validation-check recalibration

**Surfaced by a real in-Vandalizer Validate run** (BLM `BLM_Award.pdf`,
single-doc, with the Vandalizer judge-source-grounding fix
[ui-insight/Vandalizer PR #487] live locally). Two checks failed not
because the output was wrong but because they demanded exact placeholder
strings the deliverable does not use: `ac-header-financial-fields` and
`ac-placeholder-discipline` required the literal "Not specified in the
document" / "Not required", but the consolidation prompt legitimately
renders "Not specified" (FINANCIAL SUMMARY table cells) and
"Not required (—)" (Cost Share row). Recalibrated both checks to accept
ANY equivalent placeholder variant ("Not specified", "Not specified in
the document", "Not required", "Not required (—)", "—") and fail only on
blank/dropped fields. After this, the single-doc BLM run grades Good
(83%); the only remaining FAIL on the stale 4-doc run is a *correct*
cross-document-contamination catch (run one award per run). No change to
runnable steps or output.

#### v0.2.0 → v0.2.1 (2026-06-05) — validation plan

**How Vandalizer validation actually works** (researched against
`ui-insight/Vandalizer` `origin/main`; the editor "Validation Plan"
panel is `workflow_service.py`, distinct from the A–F
`workflow_validator.py` quality/cert engine):
- A workflow stores `validation_plan` = list of checks
  `{id, name, description, category}`, category ∈ {completeness,
  accuracy, content, formatting} (scored ×1.5/×1.3/×1.0/×0.7).
- "Regenerate" → `generate_validation_plan()` LLM-generates 4–8
  workflow-specific checks (sees step names, extraction fields, and
  the **first 2000 chars** of each Prompt only). Non-deterministic.
- "Validate" → `validate_workflow()` takes the last ≤3 completed runs
  and LLM-judges the final output + source doc (≤15k) + intermediate
  step outputs (≤20k) → PASS/FAIL/WARN per check.

**Bug surfaced**: the manifest's `validation_plan` used schema
`{check_id, check_name, check_type, check_description, severity,
target_fields}`, but Vandalizer's evaluator reads `c["id"]`,
`c["name"]`, `c["description"]`, `c["category"]`
(`workflow_service.py` `_evaluate_checks_against_output`). Import
copies the plan verbatim, so clicking **Validate** on an imported
manifest plan would **KeyError on `c["id"]`**. The 3 old checks were
effectively inert; the category-based plan seen in the editor was an
LLM "Regenerate", not the manifest's.

**Changes**:
- Rewrote `validation_plan` as a hand-authored **core-contract** plan
  in the Vandalizer **runtime schema** (`id/name/description/
  category`), 6 checks: `ac-sections-complete` (completeness),
  `ac-header-financial-fields` (completeness),
  `ac-monetary-fain-fidelity` (accuracy),
  `ac-admin-requirements-coverage` (completeness),
  `ac-markdown-formatting` (formatting),
  `ac-placeholder-discipline` (content). Each references the actual
  deliverable sections/fields so it imports cleanly and runs.
- No change to runnable steps or output. Build/catalog/lint green.
- The build script passes `validation_plan` through verbatim (only
  asserts it's a list); lint/docs don't consume it — so authoring the
  runtime schema directly in the manifest is safe.

**Companion Vandalizer fix** (separate repo, branch
`fix/validation-plan-schema-tolerance` off `origin/main`, NOT pushed
pending approval): added `_normalize_validation_plan()` in
`workflow_service.py`, applied in `validate_workflow` and
`get_validation_plan`, that coerces either schema (`id`|`check_id`,
`name`|`check_name`, `description`|`check_description`,
`category`|`check_type` with an alias map format→formatting,
arithmetic/consistency/correctness/presence/constraints/hallucination
→ accuracy/completeness) into the canonical shape and never raises on
a malformed check. +6 unit tests in `test_workflow_service.py`. This
makes any mismatched plan validate instead of crashing — defense in
depth so the repo plans work even on an unpatched Vandalizer.

**Pattern to roll out**: author every other workflow's
`validation_plan` in this runtime schema (core-contract depth) the
same way, then re-import + Validate each.

### `workflows/export-to-banner-extraction`

**Status**: ⚠️ v1.0.0 import-ready from a live RA feedback session;
in-Vandalizer re-test still pending. First workflow reworked from
*direct RA feedback on real output* rather than an internal test run.

#### v0.2.0 → v1.0.0 (2026-08-13) — RA feedback (Michele Mattoon) + KB removal

**How the change was surfaced**: Michele Mattoon (pre-award reviewer)
reviewed the v0.2.0 Markdown output and returned a 23-min meeting
transcript + a post-meeting email with two attachments:
`E2B Workflow Data Points.xlsx` (a prioritized 22-item data-point spec
+ FOATEXT lines 100–114, each annotated with whether the v0.2.0 output
had it) and `FOATEXT Lines - Export To Banner Form.pdf` (the actual
Export to Banner form + the full FOATEXT line catalog 100–230). The
feedback package lives at `Feedback Meetings/Export To Banner/`.

**Gaps identified** (from the xlsx "Did your Workflow Results have
these data points?" column + transcript): no Award Category; no
Subrecipients Y/N; no Co-PI / Co-I / Co-PD or Senior/Key Personnel;
Program Income not split Y/N + amount; no SF-270; no cost-share detail;
Award Type came off the literal word (RA wants it *determined* from
attributes via UI rubric docs — sponsors mislabel); Award Type enum
wrong (had "Subcontract"; missing Letter Award / Gift Funding /
Purchase Order); dates/sponsors/amounts collapsed to one value; no
provenance; no award-over-T&C precedence; the ~130-line FOATEXT manual
scan was not automated.

**Changes applied** — Tier 1 additive fields; Tier 2 rubric-driven
determinations + enum fix + precedence rule; Tier 3 new
`extract-foatext-lines` scanner over the full 100–230 catalog. Bundled
with **KB-step removal** (see below). Bumped **0.2.0 → 1.0.0** (MAJOR:
step structure 3 → 2). Validation plan rewritten to 8 core-contract
`etb-*` checks in the Vandalizer runtime schema. See the workflow
CHANGELOG `[1.0.0]` entry for the field-by-field list.

**KB removal**: mirrors `rfa-checklist-extraction` v1.0.0 (PR #50) —
the inert `KnowledgeBaseQuery` Step 0 is removed, extraction tasks read
`input_sources: [workflow_documents]` only, prompts no longer reference
"KB chunks", and "UI" is spelled out as "University of Idaho" in prose
(the FOATEXT line-154 form literal "UI $" is kept). Sponsor T&Cs / the
UI determination guides are honored when uploaded as documents; the
award-over-T&C precedence rule is retained as a latent rule.

**Open dependency**: Michele's exact UI determination guides (award
type / category / indirect basis / billing type) were NOT yet in hand.
The Tier 2 prompts encode the standard federal distinctions AND
instruct the model to apply the UI guide verbatim when uploaded as a
document — refine the rationale blocks once the guides arrive. Also
pending: her promised field-by-field comparison of the v0.2.0 output
against a real E2B review.

### Batch: KB-step removal across remaining Variant-A workflows (v1.0.0, 2026-08-13)

PR #2 (branch `remove-kb-step-remaining-workflows`) removes the inert
`KnowledgeBaseQuery` Step 0 from the **14** remaining KB-carrying
workflows, each bumped to **v1.0.0** (MAJOR, 3 steps → 2), mirroring
`rfa-checklist-extraction` v1.0.0 (#50) and `export-to-banner-extraction`
v1.0.0 (#52). The 14: `award-compliance-extraction`,
`award-modification-intake`, `budget-justification-generator`,
`compliance-personnel-verification`, `effort-reporting-extraction`,
`ffr-management-extraction`, `foa-checklist-extraction`, `noa-summary`,
`prior-approval-extraction`, `proposal-budget-personnel-extraction`,
`proposal-document-completeness`, `risk-domain-assessment`,
`section2-personnel-eligibility`, `subaward-extraction`. Surgical change
(mirrors #50): extraction tasks now read `input_sources:
[workflow_documents]` only; consolidation unchanged; **no** prompt-body
or validation-plan edits. Two READMEs had KB-specific topology prose
cleaned (noa-summary flow line; section2 APM-45.22 KB input-model note).
KBs will be reintroduced once the right approach is settled.

### Workflows not yet tested

The following workflows have not been tested against a representative
input document yet. The KB-carrying ones among them were bumped to
**v1.0.0** by the KB-removal batch above; the `nsf-*` entries never
carried a KB step and keep their prior versions:

- `award-modification-intake`
- `budget-justification-generator`
- `compliance-personnel-verification`
- `effort-reporting-extraction`
- `nsf-budget-justification-multistep`
- `nsf-budget-spreadsheet-justification`
- `nsf-expense-allowability-check`
- `prior-approval-extraction`
- `proposal-document-completeness`
- `section2-personnel-eligibility`
- `subaward-extraction`

The compliance-personnel / section2-personnel pair is the
highest-priority remaining cluster to test — they work on the same
federal NoA / proposal document shape that surfaced the PI synonym and
subaward classification bugs in
`proposal-budget-personnel-extraction`, so they may benefit from
preemptive porting of the v0.3.0+ patches. (`export-to-banner` has
since moved to its own v1.0.0 entry above following the RA feedback
session.)

### Test input documents catalog

| Document path | Type | Used to test |
|---|---|---|
| `C:\Users\lehsan\Downloads\NoA - Rominger - BLM (2)_FLAT.pdf` (and non-FLAT) | 32-page DOI/BLM NoA L24AC00293 | `ffr-management-extraction` |
| `C:\Users\lehsan\Downloads\Documents\BLM_Award.pdf` | 20-page BLM NoA L24AC00293-00 | `award-compliance-extraction` |
| `C:\Users\lehsan\Documents\Sample_FOAs\BLM\1_Foa_Content_of_L24AS00123.pdf` | 24-page BLM Idaho NOFO L24AS00123 | `foa-checklist-extraction` (failing → v0.3.0); `rfa-checklist-extraction` (passing) |
| `C:\Users\lehsan\Documents\Budget Generated Test Documents\` (4 files) | HUD RFP + narrative + HUD-424-CBW XLS + Appendix E | `proposal-budget-personnel-extraction` |

### Debugging methodology that's been working

When a workflow produces wrong output, the iteration loop that has
landed fixes consistently:

1. **Reverse-engineer the wrong number / wrong classification.** If
   the LLM emits $75,132.60 for a subaward, decompose it back to
   component terms to identify what was incorrectly added.
2. **Locate the prompt section that should have prevented the
   error.** Read the existing instruction; identify why it's
   ambiguous or insufficient.
3. **Add an explicit anchor with a worked example.** When the bug
   is numeric, include the wrong number in the prompt itself
   labeled "WRONG" alongside the correct derivation labeled
   "CORRECT". The LLM pattern-matches against its own potential
   failure.
4. **Bump workflow_version (patch for clarifications, minor for
   structural changes), update topology comment, sync JSON via
   `python scripts/build_vandalizer_workflows.py`.**
5. **Run `--check` against the build script and component catalog
   to verify manifest ↔ JSON in sync.**
6. **User re-imports the regenerated JSON into Vandalizer, attaches
   the same KB, runs on the same test document, reports output.**
7. **Compare every field of the new output to the expected
   reference. Pin remaining bugs precisely.**
