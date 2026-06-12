# Evals — compliance-personnel-verification (workflow-local)

This workflow carries its own cases under `cases/` because it is **not** a 1:1 repackaging of the `compliance-personnel-verification-udm` component's canonical prompt. Each Extraction task carries a focused `prompt_inline` body covering a different subset of the three input documents, and the Consolidation Prompt derives `non_compliant_personnel` and the five `verification_status` counts from the per-person SFI / RST status records. The workflow's behavior emerges from step interactions that no component-level eval can cover on its own.

Each case lives under `cases/<case-slug>/` with the same shape as component evals:

- `metadata.yaml` — case identity plus `validated_against_version` (the **workflow** version)
- `input-source.md` — where to obtain the three source documents (VERAS package, SFI records, RST spreadsheet) plus retrieval date
- `expected.json` — the known-good consolidated workflow output, validated by a compliance officer; conforms to [`components/compliance-personnel-verification-udm/schema.json`](https://github.com/AI4RA/prompt-library/blob/main/components/compliance-personnel-verification-udm/schema.json)
- `notes.md` — optional; qualitative observations from review

Run artifacts go under `runs/` (gitignored).

## What workflow-local cases need to exercise

The component contract (single-call extraction) is already covered by `components/compliance-personnel-verification-udm/evals/`. Workflow-local cases here should target behavior that only emerges from the three-task topology:

- **All-compliant federal research proposal** — `overall_status: "All Compliant"`, `non_compliant_personnel: []`, every per-person SFI status `"Valid"` and RST status `"Complete"`.
- **Mixed-compliance federal research proposal** — at least one SFI `"Expired"`, one SFI `"Not Found"`, and one RST `"Incomplete"`. Exercises the priority enum (`Critical` / `High` / `Medium`) and the cross-person `non_compliant_personnel` aggregation.
- **Non-federal sponsor or non-research proposal** — `sfi_rst_required: false`, `overall_status: "Not Applicable"`. Workflow must not fabricate compliance results; counts may be zero.
- **Missing RST spreadsheet** — only VERAS and SFI records uploaded. Workflow must emit per-person RST `"Incomplete"` records, set `rst_verification.spreadsheet_source: "Not provided"`, and capture the gap in `verification_status.notes`.
- **Ambiguous name match** — two `John Smith` entries cannot be disambiguated by department. Per-person status `"Review Required"` and `non_compliant_personnel` entry with priority `"Critical"`.
- **Section 6.6 / Section 2 mismatch** — at least one person in Section 2 but absent from Section 6.6 (or vice versa). Exercises the `personnel_discrepancies` derivation from source CFR-01.

## `validated_against_version`

Every case must declare the **workflow** version at which the expected output was last human-validated. This is distinct from the component's `validated_against_version`: when the workflow's step structure changes (MAJOR bump) or the consolidation prompt changes (MINOR bump), the expected output may need re-validation even though the underlying component is unchanged.

Capture the resolved component versions in `component_versions_at_validation` for reproducibility.

## Status

The initial scaffolded case (`federal-research-proposal-stub`) is a placeholder pending compliance-officer review against a synthetic federal research proposal with deliberately-mixed compliance fixtures. It should be replaced with the validated case before this workflow is promoted from `experimental` to `stable`.
