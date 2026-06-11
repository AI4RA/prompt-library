# NSFAwardExtract — Vandalizer search set

**Status:** experimental · **Kind:** Vandalizer search set (single-pass extraction) ·
**Captured:** 2026-06-11 from a `vandalizer.validation-setup.v1` export

A 92-field Vandalizer extraction task over NSF Award Notices, used by University of
Idaho sponsored-programs staff. This directory registers the task definition so that
ground truth curated against it (see `AI4RA/evaluation-data-sets`,
`field_validations[].task_search_set_uuid`) has a pinned, reviewable provenance target.

## Contents

| File | Role |
|---|---|
| `nsf-award-extract.searchset.json` | The search-set definition verbatim (uuid `8d32c4a3-…`, 92 items with searchphrases, extraction config) |
| `fieldmap.yaml` | Mapping from the 92 Vandalizer field titles to `nsf-award-notice-extraction-udm` v1.1.0 schema paths, with normalization rules (currency, US dates, percents, N/A sentinels) |

## Relationship to existing components

- The **task** overlaps `nsf-award-notice-extraction-udm` (same documents, UDM target)
  but is a distinct manifestation: a Vandalizer search set rather than a prompt, with
  its own field vocabulary. It covers ~61 of the component schema's ~77 content fields
  (notably absent: sponsor identity, current_budget_period, subawards,
  terms_and_conditions); two of its totals have no UDM target (see `fieldmap.yaml`).
- The **fieldmap** is the successor to the `vandalizer-to-udm-translation` component's
  mapping for this newer search-set shape (which now captures recipient
  address/UEI/email and budget counts/person-months that the old flat shape lacked).
  Unlike that component, the mapping here is intended for deterministic code, not LLM
  translation — the AI4RA Evaluation Explorer implements it in
  `backend/app/ingest/vandalizer.py` and uses it to emit field-scoped ground truth.

## Open questions for maintainers

- Should search sets become a first-class manifestation type alongside
  prompts/skills/agents/workflows in `component_catalog.json`?
- `searchsets/` is a new top-level directory; it is intentionally not wired into the
  workflow build/lint scripts yet.
