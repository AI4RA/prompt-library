# Evals — risk-domain-assessment (workflow-local)

This workflow carries its own cases under `cases/` because it is **not** a 1:1 repackaging of the `risk-domain-assessment-udm` component's canonical prompt. Each Extraction task carries a focused `prompt_inline` body covering 2–4 of the 14 risk domains, and the Consolidation Prompt computes `aggregate_metrics` deterministically from the 14 per-domain integer scores and derives the three flag arrays. The workflow's behavior emerges from step interactions that no component-level eval can cover on its own.

Each case lives under `cases/<case-slug>/` with the same shape as component evals:

- `metadata.yaml` — case identity plus `validated_against_version` (the **workflow** version)
- `input-source.md` — where to obtain the source documents (sponsor URL, document titles, retrieval date)
- `expected.json` — the known-good consolidated workflow output, validated by a Research Security Officer and a Sponsored Programs Administrator together; conforms to [`components/risk-domain-assessment-udm/schema.json`](https://github.com/AI4RA/prompt-library/blob/main/components/risk-domain-assessment-udm/schema.json)
- `notes.md` — optional; qualitative observations from review

Run artifacts go under `runs/` (gitignored).

## What workflow-local cases need to exercise

The component contract (single-call extraction) is already covered by `components/risk-domain-assessment-udm/evals/`. Workflow-local cases here should target behavior that only emerges from the seven-task topology:

- **Low-risk standard award** — all domain scores 1–2, `overall_risk_level: "Low"`, empty `high_risk_domains` / `key_risk_findings` / `recommended_mitigations` arrays. Exercises the baseline `aggregate_metrics` derivation.
- **High research-security risk award** — Domain 4 scores 4 or 5; `high_risk_domains` contains `"Domain 4 — Research Security & Foreign Influence"`; populated `key_risk_findings` with evidence citations from the Domain 4 task output; populated `recommended_mitigations` tied to the Domain 4 score.
- **Multi-document award** — input is NOA + RFA + proposal. The workflow integrates evidence across documents; the per-domain justifications cite specific source documents.
- **Score-as-integer conformance** — every score in the output is a JSON integer (verify with `jq 'type' .domain_scores.domain_1_programmatic_complexity.score == "number"`). No quoted strings appear in any score field.
- **CHK-03 arithmetic consistency** — `total_risk_score` equals the arithmetic sum of the 14 domain scores; `average_risk_score` equals `total_risk_score / 14` rounded to one decimal place.
- **Insufficient-evidence edge case** — at least one domain has insufficient document evidence. The component scores conservatively (1 or 2) with `"Insufficient document evidence: ..."` justification. The consolidator must NOT flag this as missing or fabricate evidence.

## `validated_against_version`

Every case must declare the **workflow** version at which the expected output was last human-validated. This is distinct from the component's `validated_against_version`: when the workflow's step structure changes (MAJOR bump) or the consolidation prompt changes (MINOR bump), the expected output may need re-validation even though the underlying component is unchanged.

Capture the resolved component versions in `component_versions_at_validation` for reproducibility.

## Status

The initial scaffolded case (`federal-multi-domain-stub`) is a placeholder pending joint Research Security Officer + Sponsored Programs Administrator review against a multi-document award fixture. It should be replaced with the validated case before this workflow is promoted from `experimental` to `stable`.
