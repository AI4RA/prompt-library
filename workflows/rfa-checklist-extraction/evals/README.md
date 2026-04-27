# Evals — rfa-checklist-extraction (workflow-local)

This workflow carries its own cases under `cases/` because it is **not** a 1:1 repackaging of the `rfa-checklist-extraction-udm` component's canonical prompt. The runtime is a seven-task parallel-Extraction-plus-Consolidation pipeline (each Extraction task runs a focused per-section `prompt_inline` body, not the full single-call component prompt), so the workflow's behavior emerges from step interactions that no component-level eval can cover on its own.

Each case lives under `cases/<case-slug>/` with the same shape as component evals:

- `metadata.yaml` — case identity plus `validated_against_version` (the **workflow** version)
- `input-source.md` — where to obtain the source input (URL, document version, date retrieved)
- `expected.json` — the known-good consolidated workflow output, validated by a sponsored-programs reviewer; conforms to [`components/rfa-checklist-extraction-udm/schema.json`](https://github.com/AI4RA/prompt-library/blob/main/components/rfa-checklist-extraction-udm/schema.json)
- `notes.md` — optional; qualitative observations from review

Run artifacts go under `runs/` (gitignored).

## What workflow-local cases need to exercise

The component contract (single-call extraction) is already covered by `components/rfa-checklist-extraction-udm/evals/`. Workflow-local cases here should target behavior that only emerges from the seven-task topology:

- **Cross-task de-duplication** — award amount appearing in `amount_per_award` extraction but not bleeding into `funding_limits`; cost-sharing details staying inside `budget_requirements` rather than being repeated in `special_requirements`.
- **`cost_sharing` rebuild** — the consolidator rebuilds the nested `cost_sharing: {status, details}` object from the flat `cost_sharing_status` (4-value enum) and `cost_sharing_details` extraction outputs; `details` must be `null` when status is `Prohibited` or `Not Specified`.
- **`important_notes` synthesis** — the consolidator produces 0–5 entries from cross-section signals (coordinator deadlines, one-nomination-per-institution rules, mandatory cost-sharing warnings); a section-only signal like an explicit page-limit is **not** the right hit.
- **Empty/optional fields** — an announcement with no optional components, no cost-sharing language, or a missing CFDA number should not produce hallucinated fields.
- **Validation-plan checks** — date-format consistency (CHK-01), monetary-amount validation (CHK-02), eligibility completeness (CHK-03), de-duplication (CHK-04) all surface against realistic announcement text.

## `validated_against_version`

Every case must declare the **workflow** version at which the expected output was last human-validated. This is distinct from the component's `validated_against_version`: when the workflow's step structure changes (MAJOR bump) or the consolidation prompt changes (MINOR bump), the expected output may need re-validation even though the underlying component is unchanged.

Capture the resolved component versions in `component_versions_at_validation` for reproducibility. When you re-run evals at a new workflow version:

- If the expected output did not need to change, update only `validated_against_version` and `validated_at`.
- If the expected output changed, update the output file **and** `validated_against_version`, and refresh `component_versions_at_validation`.

## Status

The initial scaffolded case (`nsf-multi-round-solicitation-stub`) is a placeholder case-shell pending sponsored-programs review against an authorized, de-identified NSF multi-round solicitation. It should be replaced with the validated case before this workflow is promoted from `experimental` to `stable`. See [`AI4RA/evaluation-data-sets`](https://github.com/AI4RA/evaluation-data-sets) for the canonical input source.
