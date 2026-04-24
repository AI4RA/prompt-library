# Evals — nsf-budget-justification-multistep

Workflow-local evals for the four-step NSF budget-justification pipeline. A case validates the pipeline end to end: a workbook (or workbook-derived evidence) goes in, a Word-pasteable `{ markdown, html }` object comes out.

Each case lives under `cases/<case-slug>/` with at minimum:

- `metadata.yaml` — case identity plus `validated_against_version` (the **workflow version**, not a component version) and `component_versions_at_validation` (the pinned component versions resolved at validation time).
- `input-source.md` — where to obtain the workbook (URL, version, date retrieved).
- `expected.json` — the known-good rendered object, validating against `../../../components/nsf-budget-justification-render-udm/schema.json`.
- `notes.md` — optional; qualitative observations.
- Optional intermediate snapshots (`step1-structured-budget.json`, `step2-draft.json`, `step3-reviewed.json`) when a case is specifically exercising how an intermediate shape affects downstream output.

Run artifacts go under `runs/` (gitignored).

## Why workflow-local rather than inherited

The pipeline's behavior emerges from step interactions: a plausible-looking step 1 output can produce an inconsistent step 2 draft, step 3 can mask or amplify step-2 errors, and step 4's rendering only ever reflects what the upstream review allowed through. No single component's evals cover this composed behavior. Workflow-local cases exercise:

- End-to-end fidelity: the same workbook always produces the same rendered object at a fixed workflow version.
- Intermediate-shape sensitivity: how a plausible-looking structured budget with subtle flaws flows through drafting, review, and rendering.
- Review-rubric hits: cases deliberately crafted so the review step should catch and fix a specific problem (misplaced tuition, missing participant-support disclosure, fabricated figure, zero-section invention) before the renderer freezes the prose into Word-pasteable form.
- Render fidelity: the deterministic renderer should not paraphrase or "improve" content; cases pairing a fixed reviewed array with the expected render verify the structural-only translation.

## Triad alignment reminder

If this workflow starts interacting with `AI4RA/evaluation-data-sets` or the evaluation harness as a runnable target, add a corresponding `workflows:` entry to `component_catalog_overrides.yaml` (top-level `workflows:` block) in the same PR so the human docs and the machine-readable catalog stay aligned.
