# Evals — section2-personnel-eligibility-udm

Each case lives under `cases/<case-slug>/` with at minimum:

- `metadata.yaml` — case identity plus **`validated_against_version`** (required): the component version at which the expected output was last human-validated
- `input-source.md` — where to obtain the three source documents (VERAS package, Banner NBAJOBS extract, Department List) plus retrieval date
- `expected.json` — the known-good extraction, validated against `../../schema.json` and reviewed by a Sponsored Programs Administrator
- `notes.md` — optional; qualitative observations from review

Run artifacts go under `runs/` (gitignored).

## Planned cases

The first cases should exercise distinct structural features of the contract, not simply add volume:

- **Single-PI Professor proposal** — one PI with an explicitly-eligible APM 45.22 job title, single org code mapping to a DGA already in Section 2. Exercises the `pi_copis_eligible_count: 1` baseline and `missing_dgas: []`.
- **Mixed-eligibility proposal** — one Professor (`Eligible`), one Lecturer (`Not Eligible`), one Clinical Assistant Professor (`Review Required`). Exercises all three `eligibility_status` enum values and the `pi_copis_not_eligible` / `pi_copis_review_required` flag arrays.
- **Missing DGA proposal** — org-code mapping pulls a DGA whose name is NOT in Section 2. Exercises `action_needed: "FLAG — Must be added to Section 2"`, populates `missing_dgas`, and demonstrates the cross-reference derivation.
- **Unmapped org code** — at least one Banner timesheet org code is absent from the Department List. Exercises `dga_mapping[].department_name: null`, empty `dga_names`, and the `unmapped_org_codes` summary flag.
- **Missing Banner extract** — VERAS + Department List uploaded but Banner NBAJOBS not provided. Per-person `found_in_banner: false`, every PI / Co-PI `eligibility_status: "Review Required"` with evidence "Banner record not found", and a `verification_summary.notes` gap-flag.

## `validated_against_version`

Every case must declare the component version that its `expected.json` was validated against. Re-running evals at a new component version: if the expected output did not change, bump only `validated_against_version`. If it did change, update `expected.json` and `validated_against_version` together.

## Triad alignment reminder

If this component gains a relationship to a dataset in `AI4RA/evaluation-data-sets` (e.g., a new `synthetic.section2_personnel_matrix` dataset with mixed-eligibility profiles and missing-DGA scenarios), update `component_catalog_overrides.yaml` at the repo root in the same PR.
