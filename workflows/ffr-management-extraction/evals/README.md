# Evals — ffr-management-extraction (workflow-local)

This workflow carries its own cases under `cases/` because it is **not** a 1:1 repackaging of the `ffr-management-extraction-udm` component's canonical prompt. The Extraction task carries a focused `prompt_inline` body, and the Consolidation Prompt collapses the flat searchset outputs into the schema's nested objects (`submission_schedule`, `submission_system`, `compliance_consequences`) and normalizes the `submission_system.platform` enum, so the workflow's behavior emerges from step interactions that no component-level eval can cover on its own.

Each case lives under `cases/<case-slug>/` with the same shape as component evals:

- `metadata.yaml` — case identity plus `validated_against_version` (the **workflow** version)
- `input-source.md` — where to obtain the source input (sponsor URL, document version, date retrieved)
- `expected.json` — the known-good consolidated workflow output, validated by a sponsored-programs reviewer; conforms to [`components/ffr-management-extraction-udm/schema.json`](https://github.com/AI4RA/prompt-library/blob/main/components/ffr-management-extraction-udm/schema.json)
- `notes.md` — optional; qualitative observations from review

Run artifacts go under `runs/` (gitignored).

## What workflow-local cases need to exercise

The component contract (single-call extraction) is already covered by `components/ffr-management-extraction-udm/evals/`. Workflow-local cases here should target behavior that only emerges from the two-task topology:

- **Flat-to-nested collapse** — the four `submission_system_*` searchset items collapse into the nested `submission_system` object; the four `submission_schedule` items collapse into that nested object; the four `compliance_consequences` items collapse into that nested object.
- **Platform enum normalization** — the consolidator must map document phrasings (e.g., "PMS", "Payment Management System") to the enum value `"Payment Management System"` and only emit `"Other"` when the document names a platform outside the listed five.
- **Empty `preparation_timeline`** — when the document does not describe a countdown, the consolidator must return an empty array rather than synthesizing one from generic best practices.
- **Validation-plan checks** — date-format consistency (CHK-01) for day-counts, deadline consistency (CHK-02) between annual and final FFR cadences.

## `validated_against_version`

Every case must declare the **workflow** version at which the expected output was last human-validated. This is distinct from the component's `validated_against_version`: when the workflow's step structure changes (MAJOR bump) or the consolidation prompt changes (MINOR bump), the expected output may need re-validation even though the underlying component is unchanged.

Capture the resolved component versions in `component_versions_at_validation` for reproducibility.

## Status

The initial scaffolded case (`federal-award-pms-stub`) is a placeholder case-shell pending sponsored-programs review against an authorized, de-identified federal award notice. It should be replaced with the validated case before this workflow is promoted from `experimental` to `stable`.
