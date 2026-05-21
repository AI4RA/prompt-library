---
name: risk-domain-assessment-udm
version: 0.1.0
category: review
domain: research-administration
status: experimental
tags: [risk-assessment, risk-scoring, 14-domain-rubric, post-award, pre-award, compliance, research-security, audit, sustainability, intellectual-property, reputational-risk, udm, structured-extraction, json]
audience: [sponsored-programs-staff, post-award-teams, research-security-officers, audit-and-compliance, institutional-leadership]
owner: ui-insight
created: 2026-05-20
updated: 2026-05-20
---

# Risk Domain Assessment — UDM JSON

> **Purpose:** Evaluate an award document (Notice of Award, FOA / NOFO / RFA, modification, or proposal) across 14 institutional risk domains using a standardized 1–5 scoring rubric. Each domain captures a distinct dimension of risk — from programmatic complexity and financial structure to research security, compliance burden, intellectual property, and reputational exposure — producing a comprehensive evidence-backed risk profile that supports informed award-acceptance and post-award management decisions.
> **Expected input:** One or more award documents — typically a Notice of Award plus the FOA / NOFO / RFA and any modifications. Optional but useful: the proposal and Statement of Work. Document complexity ranges from 10 to 150+ pages.
> **Expected output:** A single JSON object that validates against [`schema.json`](schema.json). No prose, no markdown outside the JSON.

## When to use this contract

This component is the **risk-profile** cut of an award document, distinct from the operational cuts (Banner setup, FFR cadence, compliance framework). It is intended to:

- support the institutional risk-acceptance decision before signing or accepting an award;
- inform post-award management priorities (which domains need monitoring or mitigation);
- give research security, audit, and compliance officers a consistent evidence-backed scoring across awards rather than ad-hoc narrative reviews.

The 14 domains are mapped 1-for-1 to the source ProcessMapping workflow's domain rubric. Each domain produces an integer score (1–5) and an **evidence-based justification** that cites specific document sections rather than inferring from general practice. The contract enforces:

- Scores are **JSON integers** (1–5), not enum strings — this is the boss's number-vs-string requirement applied to scoring fields.
- Every score has a non-empty justification.
- When the document does not contain sufficient information to assess a domain, the score is conservative (typically 1–2) and the justification says `"Insufficient document evidence: ..."`.
- The consolidator derives aggregate metrics (`total_risk_score` 14–70 integer; `average_risk_score` 1.0–5.0 number; `overall_risk_level` four-value enum; `high_risk_domains` array of domain names with score ≥ 4).

This component does **not** cover Banner setup — that lives in `export-to-banner-extraction-udm`. It does not cover modification-intake routing — that lives in `award-modification-intake-udm`.

---

## Prompt

You are evaluating one or more award documents (Notice of Award, FOA / NOFO / RFA, modification, proposal) against a 14-domain institutional risk rubric. Your output is a single JSON object conforming to `schema.json`.

**Evidence-based scoring only.** Every score must cite specific document sections or provisions. When the document does not contain sufficient information to assess a domain, score conservatively (1 or 2) and write `"Insufficient document evidence: <what was missing>"` as the justification. **Never infer or assume information not present in the documents.**

Search the entire input across all uploaded documents. Each domain has its own search-section hints (see below). Keywords cluster around the domain — follow them.

Return a single JSON object that validates against [`schema.json`](schema.json) with these top-level keys:

- `award_metadata` — object with `award_number`, `cfda_number`, `sponsor_name`, `pi_name`, `award_period_start`, `award_period_end`, `assessment_date`.
- `domain_scores` — object with 14 typed domain blocks (one per domain), each containing the domain's score (integer), justification (string), and any domain-specific evidence fields.
- `aggregate_metrics` — object with `total_risk_score`, `average_risk_score`, `overall_risk_level`, `high_risk_domains`, `key_risk_findings`, `recommended_mitigations`.

### Critical: scores are JSON integers

Every `*_score` field below is a JSON integer 1–5 inclusive. Not a quoted string `"3"`. Not an enum entry. **A JSON integer.** Mirrors the source workflow's `Field_Type: Integer`.

`average_risk_score` is a JSON number (decimal allowed, e.g., `3.4`). `total_risk_score` is a JSON integer (sum of the 14 domain scores; range 14–70).

### The 14 domains

Each domain produces a `{score, justification, ...evidence}` block. Score 1 = minimal risk; 5 = maximum risk. Justifications must cite document sections.

#### Domain 1 — Programmatic Complexity

Search: *Project Narrative, Project Summary / Abstract, Statement of Work, Award Face Sheet, Program Description*.

Evidence fields: `project_title`, `project_description_summary`, `number_of_project_components` (integer or null), `partnership_requirements` (string or null), `technical_sophistication_indicators` (array of strings).

#### Domain 2 — Financial & Budgetary Risk

Search: *Award Face Sheet, Budget, Funding Information, Cost Sharing or Matching, Funding Restrictions, Award Provisions*.

Evidence fields: `total_federal_funding` (JSON number), `total_anticipated_funding` (JSON number or null), `cost_share_required` (boolean), `cost_share_amount` (JSON number or null), `idc_rate_restriction` (string), `budget_flexibility_restrictions` (array), `multiple_funding_streams` (boolean or null).

#### Domain 3 — Subrecipient / Partner Risk

Search: *Subaward Information, Consortium Agreements, Award Terms and Conditions, Special Conditions*.

Evidence fields: `number_of_subrecipients` (integer), `subrecipient_details` (array of strings), `foreign_partners_present` (boolean or null), `subrecipient_risk_level` (string or null), `subrecipient_monitoring_requirements` (string or null).

#### Domain 4 — Research Security & Foreign Influence

Search: *Award Terms and Conditions, Ethical Conduct, Research Security, Certifications and Assurances*.

Evidence fields: `foreign_collaboration_indicators` (array), `export_control_concerns` (boolean or null), `nspm33_chips_applicability` (string or null).

#### Domain 5 — Compliance & Regulatory Requirements

Search: *Compliance Requirements, Cross-cutting Requirements, Certifications and Assurances*.

Evidence fields: `compliance_requirements_identified` (array), `compliance_requirement_type` (string or null), `compliance_risk_level` (string or null), `cross_cutting_federal_requirements` (array).

#### Domain 6 — Performance Measurement & Reporting Burden

Search: *Reporting Requirements, Performance Metrics, Deliverables*.

Evidence fields: `reporting_frequency` (string), `reporting_requirements_detail` (string), `performance_metrics_complexity` (string or null), `evaluator_required` (boolean or null), `data_use_agreements_required` (boolean or null).

#### Domain 7 — Administrative / Operational Burden

Search: *Award Administration, Prior Approval Matrix, Personnel*.

Evidence fields: `prior_approval_requirements` (array), `administrative_complexity_indicators` (array), `pi_capacity_considerations` (string or null).

#### Domain 8 — Audit Risk

Same search corpus as Domain 2 plus audit-specific keywords.

Evidence fields: `pass_through_indicator` (boolean or null), `audit_exposure_indicators` (array).

#### Domain 9 — Strategic / Mission Alignment

Same search corpus as Domain 1.

Evidence fields: `institutional_mission_fit` (string or null), `institutional_resource_requirements` (array).

#### Domain 10 — Sustainability & Closeout Risk

Search: *Closeout Requirements, Property Requirements, Terms and Conditions, Sustainment*.

Evidence fields: `post_award_obligations` (array), `closeout_requirements` (string or null), `property_equipment_obligations` (string or null).

#### Domain 11 — DOJ Bulk Data & Sensitive Information

Search: *Data Management Plan, Privacy, Confidentiality, Sensitive Data*.

Evidence fields: `sensitive_data_requirements` (string or null), `data_security_standards` (array).

#### Domain 12 — Intellectual Property, Data Rights & Privacy

Search: *Intellectual Property, Data Rights, Publication Requirements, Confidentiality*.

Evidence fields: `ip_ownership_terms` (string or null), `data_sharing_requirements` (string or null), `publication_requirements` (string or null), `privacy_risk_indicators` (array).

#### Domain 13 — Unusual Terms and Conditions / Sponsor Reliability

Search: *Award Terms and Conditions, Special Conditions, Provisions*.

Evidence fields: `non_standard_terms` (array), `special_conditions` (array).

#### Domain 14 — Institutional / Reputational Risk

Search: *Award Terms and Conditions, Special Terms, Publication Requirements*.

Evidence fields: `reputational_risk_indicators` (array).

### aggregate_metrics

- `total_risk_score` — JSON integer in `[14, 70]`. Sum of the 14 domain scores. The consolidator computes this; the schema validates it.
- `average_risk_score` — JSON number with one decimal place in `[1.0, 5.0]`. `total_risk_score / 14`.
- `overall_risk_level` — one of `"Low"` (average 1.0–1.9), `"Moderate"` (2.0–2.9), `"High"` (3.0–3.9), `"Very High"` (4.0–5.0).
- `high_risk_domains` — array of strings (domain names with `score >= 4`). E.g., `["Domain 4 — Research Security & Foreign Influence", "Domain 11 — DOJ Bulk Data & Sensitive Information"]`. Empty array when no domain scores 4 or 5.
- `key_risk_findings` — array of strings (top evidence-cited findings across high-risk domains). Empty array when overall risk is Low.
- `recommended_mitigations` — array of strings (mitigation strategies for high-risk domains). Empty array when overall risk is Low.

### Cross-field rules

1. Every domain score is a JSON integer in `[1, 5]`.
2. Every domain score has a non-empty justification.
3. When `score >= 3`, the justification MUST cite specific document evidence (mirrors source workflow's CFR-01).
4. `total_risk_score` equals the sum of the 14 individual `*_score` integers (mirrors source workflow's CHK-03).
5. `average_risk_score` equals `total_risk_score / 14` (rounded to one decimal place).

### Encoding rules

1. **Scores are JSON integers**, never quoted strings or enum entries.
2. **Boolean evidence fields are JSON booleans**, not `"Yes"` / `"No"`.
3. **Monetary evidence fields are JSON numbers** (`total_federal_funding`, `total_anticipated_funding`, `cost_share_amount`).
4. **Justifications must be evidence-based**, never inferred from general practice.
5. **Insufficient evidence is scored conservatively (1 or 2)** with `"Insufficient document evidence: ..."` justification, never silently scored 3.

### Output

A single JSON object. No surrounding markdown.
