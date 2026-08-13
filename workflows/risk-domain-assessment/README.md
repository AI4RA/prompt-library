# Risk Domain Assessment

Uploads one or more award documents (Notice of Award, FOA / NOFO / RFA, modification, proposal) and returns a single structured JSON object scoring 14 institutional risk domains on a 1–5 rubric with evidence-cited justifications, plus aggregate metrics (total / average risk scores, overall risk level enum, high-risk-domain list, key findings, recommended mitigations).

**Workflow version:** 1.0.0
**Vandalizer schema version:** 2
**Status:** experimental
**Components manifested:** `risk-domain-assessment-udm@0.1.0`
**Eval posture:** workflow-local — see [`evals/`](evals/)

> **v1.0.0 (KB step removed):** the optional Knowledge Base lookup step was removed (MAJOR, 3 steps → 2) — it was inert on import (Vandalizer blanks `kb_uuid`). Extraction tasks now read the uploaded documents directly. Mirrors `rfa-checklist-extraction` v1.0.0. See the [CHANGELOG](CHANGELOG.md).

## What this workflow does

The operator uploads one or more award documents into Vandalizer (typically NOA + RFA + proposal). The workflow runs as two steps:

**Step 1 — Parallel Extraction (6 Extraction tasks):**

| Task | Domains scored | Highlights |
|---|---|---|
| `extract-programmatic-strategic` | 1 + 9 | Programmatic Complexity + Strategic Alignment |
| `extract-financial-audit` | 2 + 8 | Financial / Budgetary + Audit Risk; monetary evidence fields as JSON numbers |
| `extract-subrecipient-sponsor` | 3 + 13 | Subrecipient + Unusual Terms / Sponsor Reliability |
| `extract-security-compliance` | 4 + 5 | Research Security + Compliance / Regulatory |
| `extract-reporting-administrative` | 6 + 7 | Reporting Burden + Administrative Burden |
| `extract-data-sustainability-reputational` | 10 + 11 + 12 + 14 | Sustainability + DOJ Bulk Data + IP / Privacy + Reputational Risk |

**Step 2 — Consolidation (1 Prompt task):** `risk-domain-assessment-consolidation` assembles the six JSON fragments into the schema-conformant three-block object, computes the `aggregate_metrics` deterministically (`total_risk_score` = sum of 14 scores; `average_risk_score` = total / 14; `overall_risk_level` enum from the average), and derives `high_risk_domains` / `key_risk_findings` / `recommended_mitigations` from the per-domain scores and justifications.

The runtime mirrors the source `ui-insight/ProcessMapping/workflows/risk-domain-assessment/` workflow one-for-one (the source's TASK-1-1 through TASK-1-6 + Consolidation).

## Components

- [`risk-domain-assessment-udm@0.1.0`](../../components/risk-domain-assessment-udm/) — the sole component. The six Extraction tasks carry focused `prompt_inline` bodies in [`manifest.yaml`](manifest.yaml); the canonical full-document prompt at [`components/risk-domain-assessment-udm/prompt.md`](../../components/risk-domain-assessment-udm/prompt.md) remains the single-call reference for harness invocations.

## Scoring as JSON integers (boss requirement)

All 14 domain scores and `aggregate_metrics.total_risk_score` are emitted as **JSON integers**, never quoted strings or enum entries. This is the boss's PR #33 number-vs-string requirement applied to scoring fields. The source workflow declares `Field_Type: Integer` on the score fields; the schema and prompts enforce JSON integer encoding throughout.

## Validation plan

Carried into the Vandalizer export at the workflow level (mirrors the source ProcessMapping `Validation_Plan`):

| Check | Type | Severity |
|---|---|---|
| `CHK-01` Score range validation | range | error |
| `CHK-02` Justification completeness | completeness | error |
| `CHK-03` Aggregate score consistency | arithmetic | warning |

CFR-01 from the source workflow (`justification not empty when score >= 3`) is enforced by `minLength: 1` on every domain block's `justification` plus the Consolidation Prompt's FLAG path for generic justifications on high-score domains.

## Eval posture

Workflow-local — see [`evals/`](evals/). The workflow is **not** a 1:1 repackaging of the canonical component prompt: each Extraction task carries a focused `prompt_inline` body covering 2–4 of the 14 domains, and the Consolidation Prompt computes `aggregate_metrics` deterministically and derives the three flag arrays from the per-domain scores. The workflow's behavior emerges from step interactions that no component-level eval can cover on its own.

Workflow-local cases should target the four `overall_risk_level` enum coverages (`Low`, `Moderate`, `High`, `Very High`), the `high_risk_domains` derivation, the insufficient-evidence path (conservative 1–2 scores with `"Insufficient document evidence: ..."` justifications), and the CHK-03 arithmetic consistency check (total = sum; average = total / 14).

## Building

Re-generate the Vandalizer export from `manifest.yaml`:

```bash
python3 scripts/build_vandalizer_workflows.py
```

CI fails when the committed `risk-domain-assessment.vandalizer.json` differs from a fresh build.

## Sharing

The committed `risk-domain-assessment.vandalizer.json` can be uploaded directly into Vandalizer via the workflow import UI. Its `x_ai4ra` block traces it back to this manifest, the pinned component version, and the content hash of the embedded prompt bodies.

## Triad integration

- **Evaluation datasets:** none yet — planned: a multi-document fixture (NOA + RFA + proposal) with deliberately-varied risk profiles across the 14 domains.
- **Harness notes:** the seven-task runtime is not identical to running the canonical full-document prompt in one shot. Harness campaigns that score the component prompt directly are still the primary signal for the contract, but workflow-level scoring (post-consolidation JSON) is the right signal for the v0.1.0 runtime — record both when both are available.
- **Shared UDM relationship:** inherits from the `risk-domain-assessment-udm` component's UDM alignment (broad bindings to Award, Organization, Subaward, CostShare, IndirectRate, ComplianceRequirement, Terms via leaf evidence fields; the 14-domain rubric and aggregate metrics are repo-local).

## Provenance

Authored 2026-05-20 alongside the initial `risk-domain-assessment-udm` component, against `ui-insight/ProcessMapping` at commit `2c1f47f46474130743af5aee44d074bcd21787e9`. The 14-domain rubric is the institutional risk-scoring framework adopted by the University of Idaho sponsored-programs office.
