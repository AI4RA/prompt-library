# Evals — rfa-checklist-extraction-udm

Each case lives under `cases/<case-slug>/` with at minimum:

- `metadata.yaml` — case identity plus **`validated_against_version`** (required): the component version at which the expected output was last human-validated
- `input-source.md` — where to obtain the source RFA (sponsor URL, PDF title, retrieval date)
- `expected.json` — the known-good extraction, validated against `../../schema.json` and reviewed by a sponsored-programs analyst
- `notes.md` — optional; qualitative observations from review

Run artifacts go under `runs/` (gitignored).

## Drafts

`drafts/<case-slug>/` holds cases that are complete and schema-valid but **not yet validated**. The lint and the
component catalog read only `cases/`, so a draft does not count as an evaluated case. Each draft's `notes.md` says
which fields restate validated gold and which were drafted, and lists the decisions a reviewer has to make. Once
a sponsored-programs reviewer has checked it, move the directory to `cases/` and fill in `validated_by`,
`validated_at` and `validated_against_version`.

- [`drafts/nsf22624/`](drafts/nsf22624/): NSF 22-624 (AAG). Cost sharing prohibited, NSF backbone merge, recurring
  submission window. It restates the Plan B gold where that exists (metadata, dates, eligibility, award, budget,
  the 5 escalation flags) and drafts the rest (the 12 CRU flags, the 14 compliance and international areas,
  mandated structure, special requirements, important notes).

## Planned cases

The first cases should exercise distinct structural features of the contract, not simply add volume:

- **Multi-round NSF solicitation** — exercises `dates_and_deadlines` round handling, LOI vs. full proposal placement, and round-specific notes.
- **Cost-sharing prohibition (NSF PAPPG-compliant)** — exercises `budget_requirements.cost_sharing_status: "Prohibited"` with a null `cost_sharing_details`.
- **NIH R01 or K-award** — exercises `eligible_individuals.criteria` with career-stage and citizenship rules, `budget_requirements.personnel_effort` with percent-effort minimums, and the NIH sponsor backbone.
- **Announcement with mandated Project Description sections and contract-review terms** — exercises `mandated_structure` (sections and sub-parts written out, never a pointer) and `risk_flags` CRU checks with grounded `detail`.
- **Announcement with explicit allowable/unallowable enumeration** — exercises both `allowable_costs` and `unallowable_costs` as non-empty arrays with sponsor-quoted language.
- **Rolling / open-ended announcement** — exercises `dates_and_deadlines` with `"Rolling"` `date_time` entries and no fixed deadline.

## `validated_against_version`

Every case must declare the component version that its `expected.json` was validated against. Re-running evals at a new component version: if the expected output did not change, bump only `validated_against_version`. If it did change, update `expected.json` and `validated_against_version` together.

## Triad alignment reminder

If this component gains a relationship to a dataset in `AI4RA/evaluation-data-sets` (e.g., a new `real.rfa_checklists` dataset), update `component_catalog_overrides.yaml` at the repo root in the same PR.
