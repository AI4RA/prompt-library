# Changelog

All notable changes to this workflow. Versions follow semver: MAJOR for step-structure changes, MINOR for additive changes (e.g., new search_set_items, validation checks), PATCH for display-name or wording edits.

## [1.1.0] — 2026-08-18

**MINOR — Tier 2 determinations now use University of Idaho's actual rubrics** (prompt-content only; topology unchanged). Michele Mattoon delivered the "Banner Help Tip" determination guides that were the Tier 2 open dependency flagged in v1.0.0, so the generic federal distinctions are replaced with UI's real decision logic. The 8 guides are committed under `Feedback Meetings/Export To Banner/Banner Help Tip Docs/`.

- **`extract-award-identification`:**
  - **Award Type** — replaced the generic FAR/2-CFR distinctions with UI's comparative-characteristics + 5-signal matrix (origination PI-vs-sponsor · involvement none/substantial/deliverables · payment lump-sum/cost-reimb-vs-milestone · purpose R&D-vs-procurement · reporting annual/minimal-vs-frequent), plus the rule "a PO that is part of a Grant award is treated as a Grant." Enum unchanged.
  - **Award Category** — replaced the free-text `award_category` + `funding_source_classification` with the UI 20-code single-letter tree (`F,5,D,E,K,C,W,B,H,A,Z,P,Q,I,S,J,T,U,O,R`), emitted as `award_category_code` + `award_category_label` + `award_category_rationale`.
  - **ALN/CFDA** — embedded the ALN decision tree (`NA.AAAA` / full `##.####` / `MULTIPLE` / `<2-digit agency>.RD` for Research or `<2-digit agency>.` otherwise / `FF.WAIT`) and the 2-digit agency table; added `cfda_rationale`.
- **`extract-budget-and-financial`:**
  - **`fa_rate_base`** enum corrected to UI basis codes: `MTDC-A` (default) / `PARSUP` / `SPEC-A` / `SPEC-R` / `SPEC-S`, with `MTDC-B` explicitly banned; MTDC exclusion list spelled out (incl. subaward portion over $25k).
  - New **`fa_rate_code`** — the Banner rate code from the Rate Codes table (e.g. `21ORO`), the sponsor's numeric rate when non-negotiated, or the waived-OH `W`-prefixed code (e.g. `W30B`); null when project type/location aren't in the inputs (Financial Unit derives it).
- **`extract-billing-and-payment`:** `billing_type` collapsed to UI's **three** setups — `Cost Reimbursement` / `Letter of Credit` / `Fixed` (dropped the spurious `Milestone`, which folds into `Fixed`) — with the Banner event mapping (BILL/MBIL/QBIL, LOC, LS%/UIBL) and the SF-270 → MBEV/QBEV/270B detail.
- **Consolidation:** SECTION 1 renders `award_category_label` + code + rationale; SECTION 4 renders the `fa_rate_code` when present. No fragment count or topology change.
- **One doc bug flagged to Michele:** Award Category code `H` (Private Business – Idaho) reads "Select when the sponsor is NOT based in Idaho" — a copy-paste typo; the prompt encodes the corrected logic (`H` = Idaho-based, `B` = non-Idaho).

**Status:** import-ready; in-Vandalizer re-test still pending. This closes the Tier 2 open dependency from v1.0.0.

## [1.0.0] — 2026-08-13

**MAJOR — step-structure change (3 steps → 2, KB step removed) bundled with additive fields, decision logic, and a new FOATEXT task**, implementing three tiers of RA feedback from Michele Mattoon's review of the v0.2.0 output (meeting transcript + `E2B Workflow Data Points.xlsx` + `FOATEXT Lines - Export To Banner Form.pdf`). No extraction task was collapsed.

**KB step removal (mirrors `rfa-checklist-extraction` v1.0.0 / PR #50):**

- The optional `KnowledgeBaseQuery` Step 0 is **removed**. It was inert on a fresh import (Vandalizer blanks `kb_uuid` by design, so the operator always had to attach a KB manually) and confused operators comparing the imported workflow to their live copies. KBs will be reintroduced once the right approach is settled.
- The seven parallel extraction tasks now read `input_sources: [workflow_documents]` only — the vestigial `step_input` (which fed the now-removed KB step's output) is dropped. Consolidation is unchanged (`input_source: step_input`, i.e. the extraction fragments).
- Prompts no longer claim to receive "KB chunks." Sponsor terms & conditions and the University of Idaho determination guides are honored **when uploaded as workflow documents**; the award-over-T&C precedence rule is retained as a latent rule for that case.
- Prompt prose spells out "UI" as "University of Idaho" (the one exception is the literal Banner FOATEXT line-154 label "Cost share: UI $", kept verbatim as it mirrors the form).

**Tier 1 — additive fields (low risk):**

- **Award Category** + `funding_source_classification` added to `extract-award-identification` (NEW — the v0.2.0 output had no category).
- **Subrecipients** present Y/N + list added (RA data point 8, previously missing).
- **Co-PI / Co-I / Co-PD names** and **Senior/Key Personnel names** added (RA data points 18–19, previously missing).
- **Program Income** split into a present Y/N flag plus `program_income_amount`.
- **SF-270 Required** Y/N added to `extract-billing-and-payment` (RA data point 24).
- **Cost-share category detail** table added to `extract-budget-and-financial` (conditional, mirrors the budget table).
- **"Capture ALL variants"** arrays added — `all_date_ranges`, `all_sponsors`, `all_award_amounts` — because an award commonly states more than one of each and the RA wants them all, not a collapsed single value.
- **Provenance:** every extraction task now emits a `provenance` array, and the consolidation renders sources for the determination fields, funding amounts, and FOATEXT/Reporting tables (RA Output Note: "provide where in the input documents the information was extracted from").
- Deliverable **reordered** to follow the RA's prioritized data-point list.

**Tier 2 — decision logic (rubric-driven determinations):**

- **Award Type**, **Award Category**, **Indirect Cost Basis**, and **Billing Type** are now DETERMINED from project attributes + UI determination rubrics, NOT copied from the literal word the sponsor used — the RA's central point (sponsors mislabel documents; a doc titled "Contract" is often a Cooperative Agreement). Each carries a `*_rationale` field.
- **Award Type enum corrected** to the UI Banner set: `Grant`, `Cooperative Agreement`, `Contract`, `Letter Award`, `Gift Funding`, `Purchase Order` (dropped `Subcontract`; subawards are captured via the new subrecipients fields).
- **Billing determination** encodes the Banner form's own logic (§4.3–4.5): minimum billing $0 (LOC / fixed) vs. $500 (non-LOC cost-reimbursable, unless lower or award ≤ $1,000); frequency tied to billing type but overridable by the award.
- **Indirect basis** encodes the waived-OH → MTDC-A rule from Banner form §2.2/2.5.
- **Award-over-T&C precedence** rule added explicitly to every task and the consolidation (RA + xlsx cell A1).
- ⚠️ Michele's exact UI determination guides were not yet in hand; prompts encode the standard federal distinctions and instruct the model to apply the UI guide verbatim when attached as KB context. Rationale blocks should be refined when the guides arrive.

**Tier 3 — FOATEXT engine (highest value):**

- NEW parallel task **`extract-foatext-lines`** scans the award (+ T&Cs) against the full Export to Banner FOATEXT line catalog (lines 100–230, §5.2–5.8) and emits ONLY the present/applicable lines with line number, standard term, Banner-ready award-specific text (placeholders filled from the award), source location, and evidence snippet. Absent terms are omitted. Rendered as SECTION 7 of the deliverable. This automates the analyst's most labor-intensive manual step.

**Validation plan:** replaced the four `CHK-0x` format/consistency checks with eight core-contract checks in the Vandalizer runtime schema (`etb-sections-complete`, `etb-award-type-determination`, `etb-award-precedence`, `etb-all-variants-captured`, `etb-foatext-line-mapping`, `etb-provenance-present`, `etb-monetary-fidelity`, `etb-flags-and-personnel-present`).

**Docs:** README brought current (it had lagged at v0.1.0) and updated to the two-step, KB-free topology. Component `harness_notes` in `component_catalog_overrides.yaml` refreshed.

**Status:** import-ready; in-Vandalizer re-test on a real award still pending.

## [0.2.0] — 2026-05-22

- **MAJOR step-structure change + output-contract change** for end-user Vandalizer use.
- Parallel "Extraction" tasks converted from Vandalizer Extraction (SearchSet keyword retrieval) to Vandalizer Prompt tasks (full-document LLM reading via `input_sources: [step_input, workflow_documents]`). Grant documents don't use the literal field labels SearchSet retrieval expects, so the SearchSet path returned empty fragments and the Consolidation step had nothing to assemble. Prompt tasks pass the full OCR'd document into the LLM, which then reads with NLU.
- Output contract changed from JSON-against-schema to RA-friendly Markdown deliverable, mirroring the source `ui-insight/ProcessMapping` workflow's `consolidation.md` (or `formatting.md`) conventions. The paired `*-udm` COMPONENT remains JSON-emitting and is the evaluation-harness target via its `prompt.md`; this WORKFLOW is the Vandalizer end-user (sponsored-programs analyst) deliverable.
- Step 0 `KnowledgeBaseQuery` placeholder added — `kb_uuid` blanked by Vandalizer's importer; the embedded `knowledge_base_hint.title` becomes an `_import_note` telling the operator which KB title to select in Vandalizer's UI. Downstream Prompt tasks read `input_sources: [step_input, workflow_documents]` so the KB chunks (when attached) plus the uploaded PDF reach the LLM context together. Returns empty output gracefully when no KB is attached — the workflow runs end-to-end either way.
- Extraction prompts tightened with explicit "flat strings, not nested objects" discipline for descriptive fields, plus a worked WRONG/CORRECT example, after the v0.1.0 → v0.2.0 dry run on real RFA documents showed nested JSON leaking into the Markdown deliverable.
- Consolidation prompts updated to skip empty sub-bullets (no "Field: —" placeholder lines when a field is null) and to rewrite any nested JSON arriving from upstream into Markdown prose rather than passing through `{...}` literals.

## [0.1.0] — 2026-05-20

- Initial experimental release.
- Two-step runtime mirroring the source `export-to-banner-extraction` v2 workflow in `ui-insight/ProcessMapping`: six parallel Extraction tasks (award-identification, dates-and-performance, sponsor-and-entity, budget-and-financial, billing-and-payment, reporting-and-special) with embedded SearchSets, plus a Consolidation Prompt that assembles the six JSON fragments into a single schema-conformant object, converts quoted-dollar strings to JSON numbers, normalizes the four enums, and enforces the two source cross-field rules as flag emissions on `reporting_special.special_terms`.
- Four enums match the source workflow exactly: `award_type` (Grant, Cooperative Agreement, Contract, Subcontract); `sponsor_entity_type` (Federal, State Government, Non-Profit, Private Industry, Foundation, University, Other); `fa_rate_base` (MTDC, TDC, Salary & Wages, Other); `billing_type` (Cost Reimbursement, Fixed Price, Letter of Credit, Milestone).
- Monetary fields explicitly typed and prompted as JSON numbers, not quoted strings — applies CFR-04-style number-vs-string handling from the boss's PR #33 review feedback to every monetary leaf in the schema.
- Validation plan carries CHK-01..CHK-04 — matches the source `Validation_Plan` with field-target paths updated to reflect the schema's six-block shape.
- Source `Cross_Field_Rules` (CFR-01 `award_start < award_end`; CFR-02 `performance_period_start <= award_start_date`) enforced by the Consolidation Prompt at runtime as flag strings on `reporting_special.special_terms` rather than altering the dates.
- Pins `export-to-banner-extraction-udm@0.1.0`.
