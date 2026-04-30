# Evals — ffr-management-extraction-udm

Each case lives under `cases/<case-slug>/` with at minimum:

- `metadata.yaml` — case identity plus **`validated_against_version`** (required): the component version at which the expected output was last human-validated
- `input-source.md` — where to obtain the source award notice (sponsor URL, FAIN, retrieval date)
- `expected.json` — the known-good extraction, validated against `../../schema.json` and reviewed by a sponsored-programs analyst
- `notes.md` — optional; qualitative observations from review

Run artifacts go under `runs/` (gitignored).

## Planned cases

The first cases should exercise distinct structural features of the contract, not simply add volume:

- **NIH R01 with eRA Commons + PMS** — exercises `submission_system.era_commons_integration` and the `Payment Management System` platform enum.
- **NSF standard award** — exercises `submission_system.platform: "ACH"` and a 120-day annual cadence.
- **HHS award with explicit late-submission penalties** — exercises the full `compliance_consequences` block including `account_restrictions` language.
- **Award with documented preparation timeline** — exercises a non-empty `preparation_timeline` populated only from document-stated milestones.
- **Award with no PMS / interim reporting language** — exercises `null` propagation across the contract.

## `validated_against_version`

Every case must declare the component version that its `expected.json` was validated against. Re-running evals at a new component version: if the expected output did not change, bump only `validated_against_version`. If it did change, update `expected.json` and `validated_against_version` together.

## Triad alignment reminder

If this component gains a relationship to a dataset in `AI4RA/evaluation-data-sets`, update `component_catalog_overrides.yaml` at the repo root in the same PR.
