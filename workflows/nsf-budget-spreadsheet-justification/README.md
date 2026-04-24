# NSF Budget Spreadsheet Justification — Vandalizer Workflow

Single-step Vandalizer workflow that delivers the [nsf-budget-spreadsheet-justification-udm](../../components/nsf-budget-spreadsheet-justification-udm/) component as an uploadable `.vandalizer.json`. The workflow reads an NSF-style proposal budget workbook (or extracted workbook evidence) supplied as the step input and emits the eight-section NSF budget-justification JSON array that validates against [components/nsf-budget-justification-udm/schema.json](../../components/nsf-budget-justification-udm/schema.json) at `#/$defs/output`.

**Workflow version:** 1.0.0
**Vandalizer schema version:** 2
**Status:** experimental
**Components manifested:** nsf-budget-spreadsheet-justification-udm@1.0.0
**Eval posture:** inherited from [components/nsf-budget-spreadsheet-justification-udm/evals](../../components/nsf-budget-spreadsheet-justification-udm/evals/)

## What this workflow does

The operator uploads a workbook or pastes workbook-derived evidence as the workflow input. The single step drafts all eight NSF sections (A–H) in one pass, matching the component's canonical contract. There is no multi-step orchestration — every section is produced by the single underlying prompt.

## Eval posture

Evals inherit from the component because this workflow is a 1:1 repackaging of the canonical prompt: one step, one task, `prompt_ref` pointing at the component's `## Prompt` section with no override. Any change that would require workflow-local cases (adding steps, parameterizing input, inlining a variant prompt) must also flip `evals.inherits_from` to `evals.workflow_local` and bump the workflow MAJOR.

## Building

```bash
python3 scripts/build_vandalizer_workflows.py
```

CI fails if the committed `nsf-budget-spreadsheet-justification.vandalizer.json` differs from a fresh build.

## Sharing

Upload the committed `nsf-budget-spreadsheet-justification.vandalizer.json` into Vandalizer. Its `x_ai4ra` block records the workflow source path, pinned component version, and the SHA256 of the embedded prompt body — so a downloaded export can be traced back to a specific prompt-library commit.

## Provenance

Built from the prose NSF budget-spreadsheet-to-justification prompt committed in cd3fd68 (2026-04-24). The first uploadable export (`NSF Budget Spreadsheet Justification.vandalizer.json`) was produced ad hoc for operator use; this directory is the durable, versioned, rebuildable source of that export.
