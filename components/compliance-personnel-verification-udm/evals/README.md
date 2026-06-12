# Evals — compliance-personnel-verification-udm

Each case lives under `cases/<case-slug>/` with at minimum:

- `metadata.yaml` — case identity plus **`validated_against_version`** (required): the component version at which the expected output was last human-validated
- `input-source.md` — where to obtain the three source documents (VERAS package, SFI records, RST spreadsheet) plus retrieval date
- `expected.json` — the known-good extraction, validated against `../../schema.json` and reviewed by a compliance officer
- `notes.md` — optional; qualitative observations from review

Run artifacts go under `runs/` (gitignored).

## Planned cases

The first cases should exercise distinct structural features of the contract, not simply add volume:

- **Federal research proposal, full compliance** — every person on the consolidated list has a current SFI disclosure and a complete RST record. Exercises the `overall_status: "All Compliant"` path and confirms `non_compliant_personnel` is `[]`.
- **Federal research proposal, mixed compliance** — at least one SFI expired, one SFI not found, and one RST incomplete. Exercises the `Critical` / `High` / `Medium` priority assignments and the cross-person `non_compliant_personnel` aggregation.
- **Non-federal research proposal** — `sfi_rst_required: false`, `overall_status: "Not Applicable"`. Verifies the contract correctly skips the verification work without fabricating compliance status.
- **Missing source document** — VERAS uploaded without RST spreadsheet. Exercises the `verification_status.notes` gap-flagging path; per-person RST `status` defaults must NOT silently become `"Complete"`.
- **Ambiguous name match** — two people share a last name and the SFI records do not disambiguate by department. Exercises the `status: "Review Required"` path and confirms the contract does not guess.

## `validated_against_version`

Every case must declare the component version that its `expected.json` was validated against. Re-running evals at a new component version: if the expected output did not change, bump only `validated_against_version`. If it did change, update `expected.json` and `validated_against_version` together.

## Triad alignment reminder

If this component gains a relationship to a dataset in `AI4RA/evaluation-data-sets` (e.g., a new `synthetic.compliance_personnel_matrix` dataset with deliberately-mixed compliance profiles), update `component_catalog_overrides.yaml` at the repo root in the same PR.
