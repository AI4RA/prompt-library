# Evals — foa-checklist-extraction-udm

Each case lives under `cases/<case-slug>/` with at minimum `metadata.yaml`, `input-source.md`, `expected.json`, and optional `notes.md`. Run artifacts go under `runs/` (gitignored).

## Planned cases

- **NIH PA/PAR/RFA with multi-stage review** — exercises `review_stages` with LOI → full → panel → council sequence.
- **DOE FOA with point-weighted evaluation criteria** — exercises `evaluation_criteria` with explicit per-criterion `weight` and `total_points`.
- **HHS NOFO with prerequisite registrations** — exercises `required_registrations` (SAM, UEI, eRA Commons).
- **FOA with strict page limits** — exercises `page_limits` rows with `what_counts` rules and `consequences`.

## Relationship to `rfa-checklist-extraction-udm`

These two components are siblings — both are pre-award checklist extractions for federal funding announcements. Cases that are well-aligned to one sibling do not have to be duplicated under the other; harness campaigns can run both contracts on the same source document.

## `validated_against_version`

Every case must declare the component version that its `expected.json` was validated against.
