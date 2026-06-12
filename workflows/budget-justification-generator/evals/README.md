# Evals — budget-justification-generator (workflow-local)

This workflow carries its own cases under `cases/` because it is **not** a 1:1 repackaging of the `budget-justification-generator-udm` component's canonical prompt. Each Extraction task does both data extraction AND narrative generation, and the Consolidation Prompt computes four arithmetic checks deterministically and renders the final Markdown document. The workflow's behavior emerges from step interactions that no component-level eval can cover on its own.

Each case lives under `cases/<case-slug>/` with the same shape as component evals:

- `metadata.yaml` — case identity plus `validated_against_version` (the **workflow** version)
- `input-source.md` — where to obtain the three source documents (budget form, project narrative, optional NOFO) plus retrieval date
- `expected.json` — the known-good consolidated workflow output, validated by a Pre-Award Analyst; conforms to [`components/budget-justification-generator-udm/schema.json`](https://github.com/AI4RA/prompt-library/blob/main/components/budget-justification-generator-udm/schema.json)
- `expected.md` — the expected `final_justification_document` Markdown string extracted for diff-based scoring (mirrors the JSON's `final_justification_document` field)
- `notes.md` — optional; qualitative observations from review

Run artifacts go under `runs/` (gitignored).

## What workflow-local cases need to exercise

The component contract (single-call generation) is already covered by `components/budget-justification-generator-udm/evals/`. Workflow-local cases here should target behavior that only emerges from the five-task topology:

- **Single-PI single-year R&R budget** — exercises the empty-section narrative defaults (`"No other personnel costs are requested..."`, `"No equipment costs are requested..."`, `"No foreign travel..."`), `is_multi_year_budget: false`, empty `budget_period_summary` array.
- **Multi-PI multi-year budget with cost share** — populated `budget_period_summary` table with multiple rows, populated `cost_share_*` fields, `year_over_year_*` narrative fields populated, `is_multi_year_budget: true`. Exercises the multi-year derivations.
- **Budget with arithmetic discrepancy** — line items deliberately do NOT sum to category totals. The workflow must emit `status: "FAIL"` entries in `cross_validation.arithmetic_checks` with populated expected / actual / discrepancy values WITHOUT altering the budget form's numbers.
- **NOFO with F&A cap and page limit** — `is_fa_rate_capped: true`, populated `fa_rate_cap_details`, populated `nofo_budget_rules` and `nofo_page_limit_for_justification`. Exercises the `FORMATTING ADVISORY` block emission at the top of `final_justification_document`.
- **Budget with PI clarification placeholders** — narrative contains `"clarification needed from PI"` strings. The workflow must preserve them in `final_justification_document` AND aggregate them in `cross_validation.items_requiring_clarification`.
- **Quoted-dollar-to-JSON-number conversion** — when extractor surfaces quoted-string monetary values in structured-data fields, the Consolidation Prompt must convert them to JSON numbers.

## `validated_against_version`

Every case must declare the **workflow** version at which the expected output was last human-validated. This is distinct from the component's `validated_against_version`: when the workflow's step structure changes (MAJOR bump) or the consolidation prompt changes (MINOR bump), the expected output may need re-validation even though the underlying component is unchanged.

Capture the resolved component versions in `component_versions_at_validation` for reproducibility.

## Status

The initial scaffolded case (`nsf-r-and-r-stub`) is a placeholder pending Pre-Award Analyst review against a synthetic NSF R&R Budget + project narrative exercise. It should be replaced with the validated case before this workflow is promoted from `experimental` to `stable`.
