# NSF Budget Justification (Multi-step) — Vandalizer Workflow

Four-step Vandalizer workflow that produces a Word-pasteable NSF budget justification from an NSF-style proposal budget workbook. Each step pins its own prompt-library component, so each phase of the pipeline can be versioned, prompted, and evaluated independently.

**Workflow version:** 2.0.0
**Vandalizer schema version:** 2
**Status:** experimental
**Components manifested:**

- [nsf-budget-spreadsheet-ingest-udm@1.0.0](../../components/nsf-budget-spreadsheet-ingest-udm/) — step 1
- [nsf-budget-justification-udm@1.0.0](../../components/nsf-budget-justification-udm/) — step 2
- [nsf-budget-justification-review-udm@1.0.0](../../components/nsf-budget-justification-review-udm/) — step 3
- [nsf-budget-justification-render-udm@1.0.0](../../components/nsf-budget-justification-render-udm/) — step 4

**Eval posture:** workflow-local — the pipeline's behavior emerges from step interactions and cannot be covered by any single component's evals.

## What this workflow does

| Step | Component | Input | Output |
| --- | --- | --- | --- |
| 1. Ingest | `nsf-budget-spreadsheet-ingest-udm` | Workbook attachment or extracted workbook evidence | Structured budget JSON (`#/$defs/input` of `nsf-budget-justification-udm/schema.json`) |
| 2. Draft | `nsf-budget-justification-udm` | Structured budget JSON from step 1 | Eight-section narrative JSON array (`#/$defs/output`) |
| 3. Review | `nsf-budget-justification-review-udm` | Drafted array from step 2 | Revised eight-section JSON array (same contract) |
| 4. Render | `nsf-budget-justification-render-udm` | Reviewed array from step 3 | JSON object `{ "markdown": "...", "html": "..." }` validating against `nsf-budget-justification-render-udm/schema.json` |

Step 4 is marked `is_output: true` in the manifest; the rendered object is the deliverable. Operators paste the `markdown` field into Word as plain text (markdown symbols visible) or paste the `html` field via *Paste Special → HTML* to preserve heading and paragraph hierarchy automatically.

The earlier intermediate artifacts remain available as step results for inspection or downstream tooling: the structured budget after step 1, the raw draft array after step 2, and the reviewed array after step 3.

This workflow is a **multi-step alternative** to the [`nsf-budget-spreadsheet-justification`](../../components/nsf-budget-spreadsheet-justification-udm/workflows/nsf-budget-spreadsheet-justification/) single-step workflow. Both are supported:

- **Single-step** is cheaper (one round-trip, one prompt) and works well when the operator trusts the one-shot prompt to handle ingestion, drafting, and polish together. Its deliverable is the eight-section array; rendering to Word is left to the operator.
- **Multi-step** surfaces intermediate artifacts (structured budget, raw draft, reviewed draft) and concludes with a Word-ready paste artifact. Each phase can be versioned and evaluated separately.

## Eval posture

`workflow_local: true`. Cases under [`evals/`](evals/) validate the pipeline as a whole: workbook in, rendered Markdown/HTML object out. Each case should record the resolved component versions at validation time in `component_versions_at_validation` so a future re-run can rebuild the exact prompts that were evaluated.

## Building

```bash
python3 scripts/build_vandalizer_workflows.py
```

CI fails if the committed `nsf-budget-justification-multistep.vandalizer.json` differs from a fresh build.

## Sharing

Upload the committed `nsf-budget-justification-multistep.vandalizer.json` into Vandalizer. The `x_ai4ra` block records the workflow source path, all four pinned component versions, and the SHA256 of each embedded prompt body — so a downloaded export can be traced back to a specific prompt-library commit.

## Provenance

Created 2026-04-24 as the first multi-component orchestration in the prompt-library and as the validation pass for the top-level `workflows/` location in the repo conventions. The fourth (render) step was added in the 2.0.0 bump after operators reported needing a Word-pasteable artifact at the end of the pipeline; the structured array remains available as an intermediate step result for evals and downstream tooling.
