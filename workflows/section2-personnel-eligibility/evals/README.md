# Evals — section2-personnel-eligibility (workflow-local)

This workflow carries its own cases under `cases/` because it is **not** a 1:1 repackaging of the `section2-personnel-eligibility-udm` component's canonical prompt. Each Extraction task carries a focused `prompt_inline` body covering a different subset of the three input documents, and the Consolidation Prompt derives the seven `verification_summary` counts and four flag arrays from the per-person / per-org-code / per-DGA records. The workflow's behavior emerges from step interactions that no component-level eval can cover on its own.

Each case lives under `cases/<case-slug>/` with the same shape as component evals:

- `metadata.yaml` — case identity plus `validated_against_version` (the **workflow** version)
- `input-source.md` — where to obtain the three source documents (VERAS package, Banner NBAJOBS extract, Department List) plus retrieval date
- `expected.json` — the known-good consolidated workflow output, validated by a Sponsored Programs Administrator; conforms to [`components/section2-personnel-eligibility-udm/schema.json`](https://github.com/AI4RA/prompt-library/blob/main/components/section2-personnel-eligibility-udm/schema.json)
- `notes.md` — optional; qualitative observations from review

Run artifacts go under `runs/` (gitignored).

## What workflow-local cases need to exercise

The component contract (single-call extraction) is already covered by `components/section2-personnel-eligibility-udm/evals/`. Workflow-local cases here should target behavior that only emerges from the three-task topology:

- **All-eligible PI with mapped DGA** — `eligibility_status: "Eligible"` for every PI / Co-PI, `action_needed: "No action needed"` for every DGA, empty `missing_dgas` and `unmapped_org_codes`. Exercises the baseline derivation of `verification_summary` counts.
- **Mixed-eligibility proposal** — one Professor (Eligible), one Lecturer (Not Eligible), one Clinical Assistant Professor (Review Required). Exercises all three `eligibility_status` enum values and the `pi_copis_not_eligible` / `pi_copis_review_required` flag arrays.
- **Missing DGA path** — org-code mapping pulls a DGA whose name is NOT in Section 2. Exercises `action_needed: "FLAG — Must be added to Section 2"`, populates `missing_dgas`, and demonstrates the cross-reference derivation.
- **Unmapped org code path** — at least one Banner timesheet org code is absent from the Department List. Exercises `dga_mapping[].department_name: null`, empty `dga_names`, and the `unmapped_org_codes` summary flag.
- **Missing Banner extract path** — VERAS + Department List uploaded but Banner not provided. Per-person `found_in_banner: false`, every PI / Co-PI `eligibility_status: "Review Required"` with the standard evidence string, and a `verification_summary.notes` gap-flag.
- **Senior / Key Personnel exclusion** — a proposal with Section 2.2A populated. Senior / Key Personnel must appear in `personnel_extraction.section_22_personnel` and `personnel_verification` but NOT in `eligibility_check` (only PI / Co-PI need APM 45.22 verification per the source workflow's task instructions).

## `validated_against_version`

Every case must declare the **workflow** version at which the expected output was last human-validated. This is distinct from the component's `validated_against_version`: when the workflow's step structure changes (MAJOR bump) or the consolidation prompt changes (MINOR bump), the expected output may need re-validation even though the underlying component is unchanged.

Capture the resolved component versions in `component_versions_at_validation` for reproducibility.

## Status

The initial scaffolded case (`uidaho-section2-stub`) is a placeholder pending SPA review against a synthetic UI proposal with mixed-eligibility personnel and missing-DGA fixtures. It should be replaced with the validated case before this workflow is promoted from `experimental` to `stable`.
