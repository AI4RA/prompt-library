# Evals — subaward-extraction-udm

Each case lives under `cases/<case-slug>/` with at minimum `metadata.yaml`, `input-source.md`, `expected.json`, and optional `notes.md`. Run artifacts go under `runs/` (gitignored).

## Planned cases

- **PTE → academic-subrecipient subaward** with full Attachment A and Attachment 4 — exercises every contact field plus typed reporting arrays.
- **Subaward with cost-share commitment** — exercises `cost_sharing_required: true`.
- **Subaward with non-default invoicing cadence** — exercises `invoicing_frequency: "Quarterly"` or `"Semi-Annual"`.
- **Subaward with explicit COI flow-down language** — exercises `coi_policy` populated.
- **Subaward with no required reports** — exercises empty arrays for `technical_reports` / `financial_reports` (strict-inclusion rule).

## `validated_against_version`

Every case must declare the component version that its `expected.json` was validated against.
