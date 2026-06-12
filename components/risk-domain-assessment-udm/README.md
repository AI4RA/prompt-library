# Risk Domain Assessment — UDM JSON

Evaluates one or more award documents (Notice of Award, FOA / NOFO / RFA, modification, proposal) across 14 institutional risk domains using a standardized 1–5 scoring rubric. Each domain captures a distinct dimension of risk — programmatic complexity, financial structure, subrecipient risk, research security, compliance burden, reporting burden, administrative burden, audit risk, strategic alignment, sustainability, sensitive data, IP / privacy, sponsor reliability, reputational risk — and produces an evidence-cited justification supporting an informed institutional risk-acceptance decision.

**Current version:** 0.1.0
**Category:** review
**Domain:** research-administration
**Status:** experimental
**Manifestations:** prompt
**Output contract:** [`schema.json`](schema.json)
**Contract scope:** repo-local, UDM-aligned

## Inputs

One or more award documents. The typical input set is:

- a **Notice of Award (NOA)** plus
- the originating **FOA / NOFO / RFA**, and
- optionally **modifications** and the **proposal / Statement of Work**.

Document complexity ranges from 10 to 150+ pages across the input set. All documents are uploaded as workflow documents to Vandalizer.

## Outputs

A single JSON object with three structured blocks:

- **`award_metadata`** — `award_number` (FAIN), `cfda_number`, `sponsor_name`, `pi_name`, `award_period_start`, `award_period_end`, `assessment_date`
- **`domain_scores`** — 14 typed domain blocks, each with a JSON integer `score` (1–5), an evidence-cited `justification`, and domain-specific evidence fields. Domain names: `domain_1_programmatic_complexity`, `domain_2_financial_budgetary_risk`, `domain_3_subrecipient_partner_risk`, `domain_4_research_security`, `domain_5_compliance_regulatory`, `domain_6_reporting_burden`, `domain_7_administrative_burden`, `domain_8_audit_risk`, `domain_9_strategic_alignment`, `domain_10_sustainability_closeout`, `domain_11_doj_bulk_data`, `domain_12_ip_privacy`, `domain_13_unusual_terms`, `domain_14_reputational_risk`
- **`aggregate_metrics`** — `total_risk_score` (integer 14–70), `average_risk_score` (number 1.0–5.0), `overall_risk_level` (four-value enum: `Low`, `Moderate`, `High`, `Very High`), `high_risk_domains[]` (names of domains with score ≥ 4), `key_risk_findings[]`, `recommended_mitigations[]`

See [`schema.json`](schema.json) for the authoritative definition and [`prompt.md`](prompt.md) for encoding rules (scores as JSON integers, JSON-number monetary evidence fields, evidence-cited justification rules, insufficient-evidence handling).

## Critical: scores are JSON integers, not enum strings

This component applies the boss's PR #33 number-vs-string review feedback to every scoring field. The source workflow types `Domain_X_Score` as `Integer`. The schema enforces this: every `score` is a JSON integer in `[1, 5]`. Quoted strings like `"3"` will fail validation. Mirrors the source workflow's `Field_Type: Integer`.

## Contract scope

Repo-local, UDM-aligned. Award metadata fields and select evidence fields resolve to UDM entities (`Award`, `Organization`, `Subaward`, `CostShare`, `IndirectRate`, `ComplianceRequirement`, `Terms`). The 14-domain rubric itself is repo-local — the AI4RA-UDM repository does not (yet) own a shared risk-rubric table.

## Relationship to other components

| Concern | Source of truth |
|---|---|
| 14-domain institutional risk profile | `risk-domain-assessment-udm` (this component) |
| Operational Banner ERP setup from a fully-executed award | [`export-to-banner-extraction-udm`](../export-to-banner-extraction-udm/) |
| Broader compliance monitoring (audit thresholds, deliverable schedules) | [`award-compliance-extraction-udm`](../award-compliance-extraction-udm/) |
| Prior-approval procedural mechanics per approval type | [`prior-approval-extraction-udm`](../prior-approval-extraction-udm/) |

The risk-domain-assessment is intended to run early in the post-award lifecycle (before signing or accepting) and again whenever a modification materially changes the risk profile. The other three components run continuously through the award lifecycle.

## Triad integration

- **Evaluation datasets:** none yet — planned: a multi-document fixture (NOA + RFA + proposal) that exercises diverse risk profiles across the 14 domains (e.g., low programmatic but high research-security; high IP and reputational concurrent).
- **Harness notes:** canonical manifestation is `prompt.md`. Validation surface is `schema.json`. The workflow runs across multiple uploaded documents.
- **Shared UDM relationship:** aligned, not owning. Leaf evidence fields bind to UDM entities; the 14-domain rubric and aggregate metrics are repo-local.

## Runtime topology — the Vandalizer workflow

The canonical runtime for this component is the [`risk-domain-assessment` workflow](https://github.com/AI4RA/prompt-library/tree/main/workflows/risk-domain-assessment) shipped at the top level of this repo. The single source of truth is [`workflows/risk-domain-assessment/manifest.yaml`](https://github.com/AI4RA/prompt-library/blob/main/workflows/risk-domain-assessment/manifest.yaml); the companion `.vandalizer.json` envelope is generated by [`scripts/build_vandalizer_workflows.py`](https://github.com/AI4RA/prompt-library/blob/main/scripts/build_vandalizer_workflows.py) and committed alongside. The runtime mirrors the source [`ui-insight/ProcessMapping/workflows/risk-domain-assessment/`](https://github.com/ui-insight/ProcessMapping/tree/main/workflows/risk-domain-assessment) workflow:

- **Step 1 (parallel Extraction)** — six Extraction tasks each cover 2–4 of the 14 domains. Task-1 = Domains 1+9 (Programmatic + Strategic). Task-2 = Domains 2+8 (Financial + Audit). Task-3 = Domains 3+13 (Subrecipient + Unusual Terms). Task-4 = Domains 4+5 (Research Security + Compliance). Task-5 = Domains 6+7 (Reporting + Administrative Burden). Task-6 = Domains 10+11+12+14 (Sustainability + DOJ Data + IP / Privacy + Reputational). The split mirrors the source workflow's `TASK-1-1` through `TASK-1-6` one-for-one.
- **Step 2 (Consolidation Prompt)** — assembles the six JSON fragments into the schema-conformant three-block object, computes `aggregate_metrics` (`total_risk_score` = sum of 14 scores, `average_risk_score` = total/14, `overall_risk_level` from the average), and derives `high_risk_domains` / `key_risk_findings` / `recommended_mitigations` from the per-domain scores and justifications.

Regenerate the workflow JSON whenever this component bumps MINOR or MAJOR (or whenever the workflow manifest changes); CI fails if the committed `.vandalizer.json` drifts from a fresh build.

## Manifestations

- [`prompt.md`](prompt.md) — canonical, LLM-agnostic prompt

## Evals

See [`evals/`](evals/) for reference inputs and known-good outputs. Initial case pending: a multi-document fixture (NOA + RFA + proposal) with deliberately mixed risk profile, validated by a Research Security Officer and a Sponsored Programs Administrator together.

## Provenance

Authored 2026-05-20 against the `risk-domain-assessment` (Workflow_ID: `WF-RISK-DOMAIN-ASSESSMENT`) process-mapping workflow in `ui-insight/ProcessMapping` at commit `2c1f47f46474130743af5aee44d074bcd21787e9`. The 14-domain rubric is the institutional risk-scoring framework adopted by the University of Idaho sponsored-programs office; this component makes the rubric a harness-evaluatable, versioned artifact rather than a manual scoring spreadsheet.
