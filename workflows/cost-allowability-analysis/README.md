# Federal Cost Allowability Analysis — Vandalizer Workflow

Three-step Vandalizer workflow that reviews a single federal-grant expense for cost allowability under the Uniform Guidance (2 CFR 200). It manifests thirteen prompt-library components as an uploadable `.vandalizer.json`.

**Workflow version:** 0.1.0
**Vandalizer schema version:** 2
**Status:** experimental
**Components manifested:** 13 (see [`manifest.yaml`](manifest.yaml))
**Eval posture:** workflow-local — see [`evals/`](evals/)

## What this workflow does

The operator uploads one expense plus its supporting evidence — the receipt or invoice, the federal award notice or terms, budget and policy documents, and any protocol-approval records — and the workflow returns a Markdown allowability determination.

### Step 1 — Normalize and classify

Three parallel tasks read the uploaded documents:

- `expense-transaction-extraction` — normalizes the expense into a structured transaction record.
- `award-allowability-terms-extraction` — extracts the award terms that govern allowability.
- `regulated-activity-classifier` — flags whether the expense implicates IRB-, IACUC-, or IBC-regulated activity.

### Step 2 — Run allowability checks

Nine parallel single-requirement checks, each anchored to a clause of the Uniform Guidance or to compliance-oversight authority:

| Check | Anchor |
| --- | --- |
| Period of performance | 2 CFR 200.403(h), 200.309 |
| Reasonableness | 2 CFR 200.404 |
| Allocability | 2 CFR 200.405 |
| Consistent treatment | 2 CFR 200.403(d), 200.405(c) |
| Award terms conformance | 2 CFR 200.403(b) |
| Federal prior approval | 2 CFR 200.407 |
| Documentation | 2 CFR 200.403(g) |
| Selected items of cost | 2 CFR 200.421-200.476 |
| Protocol approval | 45 CFR 46; PHS Policy / 9 CFR; NIH rDNA Guidelines / 42 CFR 73 |

Each check emits the shared structured finding object. The protocol-approval check returns `not_applicable` unless the classifier flagged a regulated activity.

### Step 3 — Synthesize determination

`cost-allowability-determination` aggregates the nine findings into one Markdown determination — Allowable, Potential issue, Missing info, or Not allowable — applying the conservative rule that any single `not_allowable` finding forces an overall Not allowable.

## Eval posture

Workflow-local. See [`evals/`](evals/). Component-level evals live with each component under `components/<slug>/evals/`.

## Building

```bash
python3 scripts/build_vandalizer_workflows.py
```

CI fails if the committed `cost-allowability-analysis.vandalizer.json` differs from a fresh build.

## Sharing

Upload the committed `cost-allowability-analysis.vandalizer.json` into Vandalizer. Its `x_ai4ra` block records the workflow source path, pinned component versions, and the SHA256 of each embedded prompt body.

## Scope

Decision support for post-award expense review under the Uniform Guidance. It is federal-generic (2 CFR 200), not sponsor-specific, and does not replace institutional approval, sponsor prior approval, or final accounting authority.

## Provenance

Created 2026-05-21 as the runtime for the federal cost-allowability analysis component set.
