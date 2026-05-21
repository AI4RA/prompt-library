# Evals — award-modification-intake (workflow-local)

This workflow carries its own cases under `cases/` because it is **not** a 1:1 repackaging of the `award-modification-intake-udm` component's canonical prompt. Each Extraction task carries a focused `prompt_inline` body covering a single block, and the Consolidation Prompt assembles the three fragments and enforces four cross-field rules (CFR-01..CFR-04) as flag emissions on `compliance.sponsor_conditions`. The workflow's behavior emerges from step interactions that no component-level eval can cover on its own.

Each case lives under `cases/<case-slug>/` with the same shape as component evals:

- `metadata.yaml` — case identity plus `validated_against_version` (the **workflow** version)
- `input-source.md` — where to obtain the source modification document (sponsor URL, document version, date retrieved)
- `expected.json` — the known-good consolidated workflow output, validated by a Post-Award Specialist; conforms to [`components/award-modification-intake-udm/schema.json`](https://github.com/AI4RA/prompt-library/blob/main/components/award-modification-intake-udm/schema.json)
- `notes.md` — optional; qualitative observations from review

Run artifacts go under `runs/` (gitignored).

## What workflow-local cases need to exercise

The component contract (single-call extraction) is already covered by `components/award-modification-intake-udm/evals/`. Workflow-local cases here should target behavior that only emerges from the four-task topology:

- **Modification-type enum coverage** — at least one case per major enum value (`Additional Funds`, `No-Cost Extension`, `PI Change`, `Rebudget`) to exercise the consolidator's classification handoff and conditional population rules.
- **Conditional `old_pi` / `new_pi`** — populated only for `PI Change` / `Combined`; the consolidator must emit `null` for non-PI-change modifications even if the extractor surfaced names from elsewhere in the document.
- **Conditional `new_end_date`** — populated only for `No-Cost Extension` / `Combined`; same enforcement.
- **CFR-01 / CFR-02 / CFR-03 flag emission** — when the source document is internally inconsistent (e.g., NCE without a new end date, additional-funds with no positive amount), the consolidator must append a `"FLAG: ..."` entry to `compliance.sponsor_conditions` without altering the document's stated values.
- **CFR-04 totals reconciliation** — for additional-funds modifications where all three of `current_award_amount`, `modification_amount`, `total_obligated_amount` are present, the consolidator must verify the additive identity and flag any deviation.
- **Quoted-dollar-to-JSON-number conversion** — when extractor output includes quoted strings like `"$1,234,567.89"`, the consolidator must convert them to JSON numbers.

## `validated_against_version`

Every case must declare the **workflow** version at which the expected output was last human-validated. This is distinct from the component's `validated_against_version`: when the workflow's step structure changes (MAJOR bump) or the consolidation prompt changes (MINOR bump), the expected output may need re-validation even though the underlying component is unchanged.

Capture the resolved component versions in `component_versions_at_validation` for reproducibility.

## Status

The initial scaffolded case (`nih-supplemental-award-stub`) is a placeholder pending Post-Award Specialist review against an authorized, de-identified federal modification. It should be replaced with the validated case before this workflow is promoted from `experimental` to `stable`.
