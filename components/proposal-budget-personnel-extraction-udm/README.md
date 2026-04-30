# Proposal Budget Personnel & Compliance Triggers — UDM JSON

Extracts personnel information and compliance-requirement triggers from a proposal budget document into a structured JSON object. Identifies senior key personnel, postdocs, graduate students (RA / TA), undergraduates, and other personnel; the budget category structure; subaward recipients, equipment over $5,000, travel summary, F&A rate and base, cost sharing, and total costs. The output drives the downstream `proposal-document-completeness-udm` gap analysis.

**Current version:** 0.1.0
**Category:** extraction
**Domain:** research-administration
**Status:** experimental
**Manifestations:** prompt
**Output contract:** [`schema.json`](schema.json)
**Contract scope:** repo-local, UDM-aligned

## Inputs

A proposal budget document (NSF-style budget tables / NIH PHS 398 / agency budget form), optionally with a budget justification.

## Outputs

A single JSON object with personnel listings (senior key personnel, postdocs, graduate students, undergraduates, other personnel), derivable boolean triggers (`has_postdocs_or_grad_students`, `mentoring_plan_required`, `has_subawards`, `has_equipment_over_5k`), the budget structure (budget categories, subaward recipients, equipment items, travel summary, F&A rate and base, cost sharing, total costs), and per-period budgets.

See [`schema.json`](schema.json) for the authoritative definition and [`prompt.md`](prompt.md) for the encoding rules (booleans must be derived from list lengths; equipment threshold is $5,000; F&A rate and base split into a `{rate, base}` object; total-costs reconciliation rule).

## Contract scope

Repo-local, UDM-aligned. `senior_key_personnel` rows resolve to `Personnel`; `fa_rate_and_base` resolves to `IndirectRate`; `cost_sharing` resolves to `CostShare`. The structured shape mirrors the deliverable produced by the [`proposal-budget-personnel-extraction` Vandalizer workflow](https://github.com/ui-insight/ProcessMapping/tree/main/workflows/proposal-budget-personnel-extraction) in the ui-insight/ProcessMapping process-mapping corpus.

## Relationship to sibling components

| Concern | This component | Related |
| --- | --- | --- |
| Personnel + compliance-trigger booleans from proposal budget | `proposal-budget-personnel-extraction-udm` | — |
| Document-completeness gap analysis (consumes booleans here) | — | `proposal-document-completeness-udm` |
| Post-award budget structure | — | `award-compliance-extraction-udm.financial_management` |
| Solicitation requirements | — | `rfa-checklist-extraction-udm` / `foa-checklist-extraction-udm` |

## Triad integration

- **Evaluation datasets:** none yet — planned: NSF proposal with postdocs and graduate students (mentoring plan trigger); NSF proposal with subaward and equipment > $5K; NIH proposal with cost-share commitment.
- **Harness notes:** canonical manifestation is `prompt.md`. Validation surface is `schema.json`. The companion top-level `workflows/proposal-budget-personnel-extraction` Vandalizer workflow at v0.1.0 implements the contract as two parallel Extraction tasks (personnel identification + budget structure) plus a Consolidation Prompt that derives the boolean triggers.

## Runtime topology — the Vandalizer workflow

The canonical runtime is the [`proposal-budget-personnel-extraction` workflow](https://github.com/AI4RA/prompt-library/tree/main/workflows/proposal-budget-personnel-extraction) shipped at the top level of this repo.

- **Step 1 (parallel Extraction)** — two Extraction tasks. `extract-personnel-identification` captures personnel; `extract-budget-structure-and-compliance-triggers` captures the budget structure.
- **Step 2 (Consolidation Prompt)** — assembles the two fragments and **derives** the four boolean triggers from list lengths.

## Manifestations

- [`prompt.md`](prompt.md) — canonical, LLM-agnostic prompt

## Evals

See [`evals/`](evals/) for reference inputs and known-good outputs.

## Provenance

Authored 2026-04-30 against the `proposal-budget-personnel-extraction` (Workflow_ID: `WF-PROPOSAL-BUDGET-PERSONNEL-EXTRACTION`) process-mapping workflow in `ui-insight/ProcessMapping`.
