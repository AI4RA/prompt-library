# Evals — risk-domain-assessment-udm

Each case lives under `cases/<case-slug>/` with at minimum:

- `metadata.yaml` — case identity plus **`validated_against_version`** (required): the component version at which the expected output was last human-validated
- `input-source.md` — where to obtain the source documents (sponsor URL, document titles, retrieval date)
- `expected.json` — the known-good extraction, validated against `../../schema.json` and reviewed by a Research Security Officer and a Sponsored Programs Administrator together
- `notes.md` — optional; qualitative observations from review

Run artifacts go under `runs/` (gitignored).

## Planned cases

The first cases should exercise distinct structural features of the contract, not simply add volume:

- **Low-risk standard NIH R01** — most domains score 1–2, no high-risk domains. Exercises the baseline `overall_risk_level: "Low"`, empty `high_risk_domains` / `key_risk_findings` / `recommended_mitigations` arrays.
- **High research-security risk award** — Domain 4 (Research Security & Foreign Influence) scores 4 or 5 due to foreign-collaboration indicators. Exercises the `high_risk_domains` derivation, `key_risk_findings` evidence citation, and `recommended_mitigations` generation.
- **Multi-document award (NOA + RFA + proposal)** — risk scoring varies by document; the workflow must integrate evidence across all uploaded documents and cite the source document per finding.
- **Pass-through (subrecipient) award** — Domain 3 (Subrecipient Risk) score 3+, populated `subrecipient_details`, `foreign_partners_present` true / false, populated `subrecipient_risk_level` and `subrecipient_monitoring_requirements`.
- **Insufficient-evidence edge case** — at least one domain has insufficient document evidence to score reliably. The component must score conservatively (1 or 2) with justification beginning `"Insufficient document evidence: ..."`, NOT score 3 silently.
- **CFR-01 enforcement** — a domain with score ≥ 3 has a non-empty, evidence-cited justification. Verifies the prompt's evidence-citation rule fires.

## `validated_against_version`

Every case must declare the component version that its `expected.json` was validated against. Re-running evals at a new component version: if the expected output did not change, bump only `validated_against_version`. If it did change, update `expected.json` and `validated_against_version` together.

## Triad alignment reminder

If this component gains a relationship to a dataset in `AI4RA/evaluation-data-sets` (e.g., a new `synthetic.risk_assessments_14_domain` dataset with deliberately-mixed risk profiles), update `component_catalog_overrides.yaml` at the repo root in the same PR.
