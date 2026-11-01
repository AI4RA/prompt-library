# RFA Checklist Field Mapper

Sorts the text of a free-form RFA checklist into the 28 fields of the RFA Plan B human gold, by copying passages only. It lets a checklist that has no JSON contract, such as the output of [`rfa-checklist-plain-prompt`](../rfa-checklist-plain-prompt/), be scored with the CLEF judge field by field, like the `rfa-checklist-extraction` workflow v3.1.0 field output.

**Current version:** 1.0.0
**Category:** extraction
**Domain:** research-administration
**Status:** experimental
**Manifestations:** prompt
**Output contract:** [`schema.json`](schema.json)
**Contract scope:** repo-local

## Inputs

One checklist as plain text or Markdown, inserted at `{{CHECKLIST}}`. The model sees nothing else: not the announcement, not the gold, not other runs.

## Outputs

One JSON object with the 28 field names as keys. Each value is a list of passages copied from the checklist; an empty list means the checklist gives nothing for that field. The caller checks every passage in code and drops any that is not a verbatim substring of the checklist, so the field values contain only the checklist's own text.

## Contract scope

Repo-local. The field names and descriptions are copied unchanged from [`rfa-checklist-extraction-udm`](../rfa-checklist-extraction-udm/) `schema.json` v1.0.0 (commit 098ab80), limited to the 28 fields the Plan B gold scores. The output shape (lists of passages) is this component's own.

## Triad integration

- **Evaluation datasets:** `evaluation_results/rfa-checklist-extraction/arms/plain-prompt/field-mapping/` in AI4RA/evaluation-data-sets; its `MAPPING_PLAN.md` (approved by Barrie Robison 2026-10-29) sets the model, the quote check and how field values are built.
- **Harness notes:** run by `runners/rfa-checklist-vandalizer/scripts/run_field_mapper.py` in AI4RA/evaluation-harness.
- **Shared UDM relationship:** none.

## Manifestations

- [`prompt.md`](prompt.md) — canonical prompt

## Evals

No eval cases. See [`evals/`](evals/).

## Provenance

Drafted 2026-10-29 with Barrie Robison, as the field-mapping step of the plan to score plain-prompt checklists with CLEF.
