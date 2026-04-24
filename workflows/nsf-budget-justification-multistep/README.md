# NSF Budget Justification (Multi-step) — Vandalizer Workflow

Three-step Vandalizer workflow that produces an NSF budget justification from an NSF-style proposal budget workbook. Each step pins its own prompt-library component, so each phase of the pipeline can be versioned, prompted, and evaluated independently.

**Workflow version:** 1.0.0
**Vandalizer schema version:** 2
**Status:** experimental
**Components manifested:**

- [nsf-budget-spreadsheet-ingest-udm@1.0.0](../../components/nsf-budget-spreadsheet-ingest-udm/) — step 1
- [nsf-budget-justification-udm@1.0.0](../../components/nsf-budget-justification-udm/) — step 2
- [nsf-budget-justification-review-udm@1.0.0](../../components/nsf-budget-justification-review-udm/) — step 3

**Eval posture:** workflow-local — the pipeline's behavior emerges from step interactions and cannot be covered by any single component's evals.

## What this workflow does

| Step | Component | Input | Output |
| --- | --- | --- | --- |
| 1. Ingest | `nsf-budget-spreadsheet-ingest-udm` | Workbook attachment or extracted workbook evidence | Structured budget JSON (`#/$defs/input` of `nsf-budget-justification-udm/schema.json`) |
| 2. Draft | `nsf-budget-justification-udm` | Structured budget JSON from step 1 | Eight-section narrative JSON array (`#/$defs/output`) |
| 3. Review | `nsf-budget-justification-review-udm` | Drafted array from step 2 | Revised eight-section JSON array (same contract) |

Step 3 is marked `is_output: true` in the manifest; the revised array is the deliverable.

This workflow is a **multi-step alternative** to the [`nsf-budget-spreadsheet-justification`](../../components/nsf-budget-spreadsheet-justification-udm/workflows/nsf-budget-spreadsheet-justification/) single-step workflow. Both are supported:

- **Single-step** is cheaper (one round-trip, one prompt) and works well when the operator trusts the one-shot prompt to handle ingestion, drafting, and polish together.
- **Multi-step** surfaces intermediate artifacts (the structured budget after step 1, the raw draft after step 2) and lets the review rubric be versioned separately from the drafting prompt.

## Eval posture

`workflow_local: true`. Cases under [`evals/`](evals/) validate the pipeline as a whole: workbook in, revised eight-section array out. Each case should record the resolved component versions at validation time in `component_versions_at_validation` so a future re-run can rebuild the exact prompts that were evaluated.

## Building

```bash
python3 scripts/build_vandalizer_workflows.py
```

CI fails if the committed `nsf-budget-justification-multistep.vandalizer.json` differs from a fresh build.

## Sharing

Upload the committed `nsf-budget-justification-multistep.vandalizer.json` into Vandalizer. The `x_ai4ra` block records the workflow source path, all three pinned component versions, and the SHA256 of each embedded prompt body — so a downloaded export can be traced back to a specific prompt-library commit.

## Provenance

Created 2026-04-24 as the first multi-component orchestration in the prompt-library and as the validation pass for the top-level `workflows/` location in the repo conventions.
