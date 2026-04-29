# NSF Expense Allowability Check - Vandalizer Workflow

Single-step Vandalizer workflow that delivers the [nsf-expense-allowability-check](../../components/nsf-expense-allowability-check/) component as an uploadable `.vandalizer.json`. The operator supplies one expense plus award, budget, policy, and documentation evidence; the workflow emits a concise chat-ready allowability assessment.

**Workflow version:** 1.0.0
**Vandalizer schema version:** 2
**Status:** experimental
**Components manifested:** nsf-expense-allowability-check@1.0.0
**Eval posture:** inherited from [components/nsf-expense-allowability-check/evals](../../components/nsf-expense-allowability-check/evals/)

## What this workflow does

The operator uploads or pastes a single expense snapshot and supporting evidence. The workflow checks award period, budget category, budget alignment, documentation, participant-support treatment, travel or equipment constraints, indirect-cost treatment, and prohibited or restricted costs when those checks are applicable.

## Eval posture

Evals inherit from the component because this workflow is a 1:1 repackaging of the canonical prompt: one step, one task, `prompt_ref` pointing at the component's `## Prompt` section with no override.

## Building

```bash
python3 scripts/build_vandalizer_workflows.py
```

CI fails if the committed `nsf-expense-allowability-check.vandalizer.json` differs from a fresh build.

## Sharing

Upload the committed `nsf-expense-allowability-check.vandalizer.json` into Vandalizer. Its `x_ai4ra` block records the workflow source path, pinned component version, and the SHA256 of the embedded prompt body.

## Provenance

Created 2026-04-29 from an operator-authored Vandalizer checklist titled "Expense-Allowability Check."
