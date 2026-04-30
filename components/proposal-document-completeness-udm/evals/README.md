# Evals — proposal-document-completeness-udm

Each case lives under `cases/<case-slug>/` with at minimum `metadata.yaml`, `input-source.md`, `expected.json`, and optional `notes.md`. Run artifacts go under `runs/` (gitignored).

## Planned cases

- **NSF TTP-P track proposal** — exercises `proposal_track_type: "TTP-P"` triggering the letter-of-collaboration conditional requirement.
- **NIH proposal with postdocs** — exercises `has_postdocs_or_grad_students: true` triggering the mentoring plan conditional requirement.
- **Proposal with subawards** — exercises `has_subawards: true`, `subaward_documents` populated per subawardee, and `subaward_required_documents`.
- **Proposal with name mismatches** — exercises `personnel_discrepancies` with a budget-vs-Section-2 name-mismatch case.
- **Proposal with all docs present** — exercises `prioritized_missing: []` and confirms no false positives.

## `validated_against_version`

Every case must declare the component version that its `expected.json` was validated against.

## Triad alignment reminder

If this component gains a relationship to a dataset in `AI4RA/evaluation-data-sets`, update `component_catalog_overrides.yaml` at the repo root in the same PR.
