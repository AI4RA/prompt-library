# [Workflow Name]

[One-paragraph summary: what a Vandalizer operator gets from this workflow, the input they supply, the output they receive, and which component(s) this workflow manifests.]

**Workflow version:** 1.0.0
**Vandalizer schema version:** 2
**Status:** experimental
**Components manifested:** [slug@version, ...]
**Eval posture:** [inherited from <slug> | workflow-local]

## What this workflow does

[Describe the operator-facing experience: what they supply as input in Vandalizer, what steps run, what deliverable they get back, and the problem this solves.]

## Components

- [slug@version](../../../components/<slug>/) — [role this component plays in the workflow]

For multi-component workflows, list every component the workflow manifests and describe how the steps compose them.

## Eval posture

**If inherited:** "Evals inherit from [components/<slug>/evals](../../../components/<slug>/evals/) because this workflow is a 1:1 repackaging of that component's canonical prompt. No workflow-local cases are required."

**If workflow-local:** "This workflow defines its own eval cases under [evals/](evals/) because [reason: multi-step orchestration, parameterization, or prompt override]. Cases validate the workflow as a whole, not the underlying component prompt."

## Building

Re-generate the Vandalizer export from `manifest.yaml`:

```bash
python3 scripts/build_vandalizer_workflows.py
```

CI fails when the committed `<workflow-name>.vandalizer.json` differs from a fresh build, so treat `manifest.yaml` as the source of truth and never hand-edit the generated JSON.

## Sharing

The committed `<workflow-name>.vandalizer.json` can be uploaded directly into Vandalizer. Its `x_ai4ra` block traces it back to this manifest, the pinned component versions, and the content hash of each embedded prompt body — so anyone with the exported JSON can locate the exact prompt-library commit it was built from.

## Triad integration

- **Evaluation datasets:** [dataset IDs in `AI4RA/evaluation-data-sets`, or "none yet; repo-local evals only"]
- **Harness notes:** [whether the harness treats this workflow as a runnable target, and how it pairs with the underlying component(s)]
- **Shared UDM relationship:** [inherit from the referenced components; restate only if the workflow adds its own UDM-facing surface]

## Provenance

[Who authored this workflow, when, and what real operator task prompted its creation.]
