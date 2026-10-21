# NSFAwardExtract — Vandalizer search set

**Status:** experimental · **Kind:** Vandalizer search set (single-pass extraction) ·
**Latest search-set version:** 0.2.0 (2026-10-21) · **Baseline captured:** 2026-06-11

A versioned Vandalizer extraction task (92 fields in v0.1.0; 96 fields in v0.2.0) over NSF Award Notices, used by University of
Idaho sponsored-programs staff. This directory registers the task definition so that
ground truth curated against it (see `AI4RA/evaluation-data-sets`,
`field_validations[].task_search_set_uuid`) has a pinned, reviewable provenance target.

## Contents

| File | Role |
|---|---|
| `versions.json` | Version index with artifact paths, SHA256 hashes, model configuration, and mapping/evaluation scope |
| `versions/0.2.0/nsf-award-extract.vandalizer.json` | Byte-for-byte original October 21 export; uploadable Vandalizer schema v2 search set, 96 fields |
| `CHANGELOG.md` | Search-set release history and changes |
| `nsf-award-extract.searchset.json` | The search-set definition verbatim (uuid `8d32c4a3-…`, 92 items with searchphrases, extraction config) |
| `fieldmap.yaml` | Mapping from the 92 Vandalizer field titles to `nsf-award-notice-extraction-udm` v1.1.0 schema paths, with normalization rules (currency, US dates, percents, N/A sentinels) |

## Versioning and use

Search-set versions are independent of the Vandalizer export's `schema_version: 2`,
the UDM component version, and `fieldmap.yaml`'s mapping version. The June capture
is retrospectively labeled **0.1.0**; its bytes and original path are preserved.
The October export is **0.2.0**, an experimental pre-1.0 revision adding four
required extraction fields and recording `moonshotai/kimi-k3` as its model.
All 92 existing field definitions and their relative order are unchanged.

The four additions are **ORCID Number**, **Graduate Student Full Name**, **PI SSN**,
and **University Mascot**. Their purpose and expected missing-value behavior have
not been established by this export. They have no declared UDM mapping here.
The baseline fieldmap remains v0.1.0 and applies only to its original field set.
Consumers that require an exact field list need to account for the additions.

The October export records no search-set UUID and contains no test cases.
It establishes a task definition and recorded configuration, with no new validation
or performance claim. Pin the prompt-library commit plus the version, path, and
SHA256 from `versions.json` when recording evaluations. Preserve versioned exports
verbatim; record future revisions at new version paths and update the index and
changelog together. The model recorded in the export is configuration evidence,
not proof of which model executed an evaluation.

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
