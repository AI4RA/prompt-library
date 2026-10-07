# Changelog

All notable changes to this component. Versions follow semver: MAJOR for output-contract breaks, MINOR for backward-compatible additions, PATCH for wording or clarity.

## [1.0.0] — 2026-10-06

- **MAJOR — synced to the `rfa-checklist-extraction` workflow v3.1.0.** The 0.1.0 contract predated the workflow's 2026-08 changes, so the workflow prompts had moved ahead of `prompt.md` / `schema.json`. The contract is now the union of the workflow's ten extraction fragments, field for field:
  - **New fields:** `funding_instrument_type`, `risk_flags` (17 fixed checks: 5 escalation + 12 Contract Review Unit), `formatting_requirements`, `mandated_structure`, `compliance_risks` (8 fixed areas), `international_components` (6 fixed areas).
  - **Components** gain a required `source` (`Announcement` / `Sponsor standard` / `Announcement + sponsor standard`) and the sponsor backbone (NSF, NIH, USDA-NIFA, DOE, NASA). A pure "Sponsor standard" component is a `{name, source}` stub; every other component needs a `description`. A component's `special_requirements` may be omitted or null.
  - **`budget_requirements`:** `cost_sharing: {status, details}` becomes the workflow's flat `cost_sharing_status` / `cost_sharing_details` (same enum).
  - **`award_information.number_of_awards`** may be text, an integer or null.
  - **Every top-level key is now required**, including the metadata scalars (null when not stated).
  - `important_notes` stays (0–3 items, synthesized like the workflow's consolidation step).
- **Prompt:** the ten task prompts' rules are merged into one single-call prompt (fixed labels, backbone lists and formatting defaults verbatim), including recurring-deadline resolution, limited-submission capture and the formatting precedence rule.
- **Checked against real outputs:** across the evaluation harness's v3.1.0 replays (2,900 runs), a merged set of the ten fragments plus `important_notes` validates against this schema exactly when every fragment passes the harness's v3.1.0 fragment schemas (0 disagreements).
- The workflow keeps its 0.1.0 pin; its manifest now records the lag with `pinned_version_sha`.

## [0.1.0] — 2026-04-24

- Initial experimental release.
- Schema derived from the `rfa-checklist-extraction` v2 Vandalizer workflow in `ui-insight/ProcessMapping` (six parallel extraction tasks + consolidation, 17 source fields).
- Scalar metadata (`rfa_id`, `rfa_number`, `rfa_title`, `sponsor_name`, `program_code`, `announcement_url`, `opportunity_number`, `cfda_number`) aligned with standard opportunity-metadata conventions.
- Eight structured sections each given a distinct shape to enforce the de-duplication / placement contract at schema level.
- `cost_sharing.status` enum matches the Cost_Sharing Enum_Values from the source workflow (`Required`, `Voluntary`, `Prohibited`, `Not Specified`).
- UDM column bindings preserved: `cost_sharing` → `CostShare`, `fa_policy` → `IndirectRate`, `personnel_effort` → `Effort`.
- No eval cases yet — status `experimental` until at least one golden extraction is added under `evals/cases/`.
