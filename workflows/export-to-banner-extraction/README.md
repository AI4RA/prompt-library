# Export to Banner Award Extraction

Uploads a fully-executed award document (optionally alongside the sponsor's general terms & conditions and the University of Idaho determination guides as additional documents) and returns an **RA-friendly Markdown Export to Banner Reference Summary** — the prioritized data points a University of Idaho sponsored-programs analyst needs to populate the VERAS Export to Banner form.

**Workflow version:** 1.0.0
**Vandalizer schema version:** 2
**Status:** experimental
**Components manifested:** `export-to-banner-extraction-udm@0.1.0`
**Eval posture:** workflow-local — see [`evals/`](evals/)

## What this workflow does

The operator uploads a fully-executed award document (notice of award, cooperative agreement, contract, or modification) into Vandalizer. The workflow runs as two steps. (There is **no** knowledge-base step as of v1.0.0 — see the note below; sponsor terms & conditions or the University of Idaho determination guides can be uploaded as additional documents when available.)

**Step 1 — Parallel Extraction (7 `Prompt` tasks):**

| Task | Covers | Highlights |
|---|---|---|
| `extract-award-identification` | Identification & classification | `award_type` + `award_category` **determinations** (rubric-driven, not copied labels), Co-PI/key personnel, subrecipients Y/N, prime sponsor award ID, CFDA |
| `extract-dates-and-performance` | Dates | `all_date_ranges` (captures **every** range), budget periods, multi-year/incremental flags |
| `extract-sponsor-and-entity` | Sponsor(s) | `all_sponsors` (captures **every** sponsor), entity type, UEIs, officers |
| `extract-budget-and-financial` | Budget & financial | `all_award_amounts` (captures **every** amount), indirect-basis determination, cost-share detail table, program income Y/N + amount |
| `extract-billing-and-payment` | Billing & payment | billing-type determination, `minimum_billing` + frequency logic mapped to Banner form 4.3–4.5, SF-270 Y/N |
| `extract-reporting-and-special` | Reporting & special | report table, retention, carry-forward, prior approvals, governing regs |
| `extract-foatext-lines` | **FOATEXT scanner** | scans the award against the full FOATEXT line catalog (lines 100–230, §5.2–5.8) and emits **only present lines** with line #, Banner-ready text, and source |

**Step 2 — Consolidation (1 `Prompt` task):** `export-to-banner-consolidation` assembles the seven JSON fragments into the RA-friendly Markdown deliverable (eight sections + verification checklist), rendering provenance for the determination fields, funding amounts, and FOATEXT table; flagging cross-task contradictions with `[DISCREPANCY - ...]`; and honoring the **award-over-T&C precedence** rule.

Every extracted value cites where in the input documents it was found (an RA Output Note), and the deliverable follows the RA's prioritized data-point order.

## Design provenance — RA feedback (2026-08-13)

v1.0.0 implements three tiers of feedback from Michele Mattoon's review of the v0.2.0 output (transcript + `E2B Workflow Data Points.xlsx` + the `FOATEXT Lines - Export To Banner Form.pdf`), bundled with removal of the inert KB step:

- **Tier 1 — additive fields:** award category, subrecipients Y/N, Co-PI/key personnel, program income amount, SF-270, cost-share detail, "capture all variants" for dates/sponsors/amounts, provenance, output reordering.
- **Tier 2 — decision logic:** Award Type / Category / Indirect Basis / Billing Type reframed as rubric-driven determinations; Award Type enum corrected to the University of Idaho Banner set (Grant, Cooperative Agreement, Contract, Letter Award, Gift Funding, Purchase Order); explicit award-over-T&C precedence.
- **Tier 3 — FOATEXT engine:** the `extract-foatext-lines` scanner.
- **KB step removed (MAJOR, 3 steps → 2):** the optional `KnowledgeBaseQuery` Step 0 was inert on import (Vandalizer blanks `kb_uuid`, so a KB always had to be attached manually) and confused operators comparing against their live copies. Mirrors `rfa-checklist-extraction` v1.0.0. Extraction tasks now read `input_sources: [workflow_documents]` only. KBs will be reintroduced once the right approach is settled.

> **Open dependency:** Michele's exact University of Idaho determination guides for award type / category / indirect basis / billing type were not in hand at authoring time. The Tier 2 prompts encode the standard federal distinctions **and** instruct the model to apply the University of Idaho guide verbatim when it is uploaded as a workflow document. Refine the rationale blocks once the guides arrive.

## Components

- [`export-to-banner-extraction-udm@0.1.0`](../../components/export-to-banner-extraction-udm/) — the pinned component. Its JSON `schema.json` / `prompt.md` remain the **single-call harness reference** (a six-block JSON contract). This WORKFLOW intentionally diverges from that shape: it is the end-user Vandalizer **Markdown deliverable**, and since v1.0.0 it is a superset (personnel, FOATEXT, determinations, provenance) driven by RA feedback. The seven Extraction tasks carry focused `prompt_inline` bodies in [`manifest.yaml`](manifest.yaml).

## Validation plan

Authored in the Vandalizer runtime schema (`id` / `name` / `description` / `category`) and carried into the export verbatim:

| Check | Category |
|---|---|
| `etb-sections-complete` — all deliverable sections rendered | completeness |
| `etb-award-type-determination` — Award Type is a determination, not a copied label | accuracy |
| `etb-award-precedence` — award-over-T&C precedence honored | content |
| `etb-all-variants-captured` — all date / sponsor / amount variants captured | completeness |
| `etb-foatext-line-mapping` — FOATEXT rows map to the catalog with source | content |
| `etb-provenance-present` — extracted values cite their source | content |
| `etb-monetary-fidelity` — monetary amounts verbatim | accuracy |
| `etb-flags-and-personnel-present` — personnel + Y/N flags present | completeness |

## Eval posture

Workflow-local — see [`evals/`](evals/). Per [`docs/contracts.md`](../../docs/contracts.md), workflow-local cases are required because behavior emerges from the eight-task topology rather than a single component prompt. Cases should target: the four rubric-driven determinations (award type / category / indirect basis / billing type), the "capture all variants" arrays, the FOATEXT scan (present-line detection + line-number fidelity + omission of absent terms), the award-over-T&C precedence path, and provenance rendering.

## Building

Re-generate the Vandalizer export from `manifest.yaml`:

```bash
python3 scripts/build_vandalizer_workflows.py
```

CI fails when the committed `export-to-banner-extraction.vandalizer.json` differs from a fresh build, so treat `manifest.yaml` as the source of truth and never hand-edit the generated JSON.

## Sharing

The committed `export-to-banner-extraction.vandalizer.json` can be uploaded directly into Vandalizer via the workflow import UI. Its `x_ai4ra` block traces it back to this manifest, the pinned component version, and the content hash of the embedded prompt bodies.

## Triad integration

- **Evaluation datasets:** none yet — planned: an authorized, de-identified award (with sponsor T&Cs) exercising a mislabeled instrument (Tier 2 determination), multiple date ranges/amounts, and several present FOATEXT lines.
- **Harness notes:** the eight-task runtime is not identical to running the canonical component prompt in one shot, and since v1.0.0 the workflow deliverable is a superset of the component's six-block JSON. Harness campaigns that score the component prompt directly remain the primary signal for the component contract; workflow-level scoring (the post-consolidation Markdown) is the right signal for this RA-facing runtime.
- **Shared UDM relationship:** inherits from the `export-to-banner-extraction-udm` component's UDM alignment (broad bindings to `Award`, `Personnel`, `Organization`, `AwardBudget`, `AwardBudgetPeriod`, `IndirectRate`, `CostShare`, `ContactDetails`, `Terms`).

## Provenance

Authored 2026-05-20 alongside the initial `export-to-banner-extraction-udm` component, against `ui-insight/ProcessMapping` at commit `2c1f47f46474130743af5aee44d074bcd21787e9`. v1.0.0 (2026-08-13) reworks the workflow against Michele Mattoon's RA feedback and removes the inert KB step (see the workflow [`CHANGELOG`](CHANGELOG.md) and the prompt-library `CLAUDE.md` workflow testing log).
