# Regulated Activity Classifier

Flags whether an expense implicates an activity that requires institutional compliance oversight — human subjects (IRB), animals (IACUC), or biosafety (IBC) — based on expense-level signals such as the description, vendor, and account coding. It is the detection layer of the federal cost-allowability analysis workflow.

**Current version:** 0.1.0
**Category:** classification
**Domain:** research-administration
**Status:** experimental
**Manifestations:** prompt
**Output contract:** [`schema.json`](schema.json)
**Contract scope:** repo-local

## Inputs

A normalized expense record (see [`expense-transaction-extraction`](../expense-transaction-extraction/)), optionally with award context. The component works from expense-level signals, not from the general nature of the project.

## Outputs

A single JSON object — see [`schema.json`](schema.json) — with a per-regime decision (`triggered`, `rationale`, `trigger_signals`) for human subjects, animals, and biosafety, plus an `any_regime_triggered` roll-up and a one-sentence `summary`.

The classifier is deliberately inclusive: a plausible signal is enough to flag a regime. Its purpose is to surface expenses for a reviewer to verify against the protocol-approval system, not to make a final determination.

## Contract scope

Repo-local. The classification record is a prompt-library detection contract that routes the downstream `protocol-approval-allowability-check`. It is not a shared AI4RA-UDM schema.

## Triad integration

- **Evaluation datasets:** none yet — repo-local synthetic coverage planned.
- **Harness notes:** canonical manifestation is `prompt.md`; validation surface is `schema.json`. Invoked as a Step 1 task of the [`cost-allowability-analysis`](https://github.com/AI4RA/prompt-library/tree/main/workflows/cost-allowability-analysis) workflow; its output routes the protocol-approval check in Step 2.
- **Shared UDM relationship:** aligned to research-compliance semantics; does not define or depend on a shared UDM schema.

## Manifestations

- [`prompt.md`](prompt.md) — canonical, LLM-agnostic prompt

## Related components

- [`protocol-approval-allowability-check`](../protocol-approval-allowability-check/) — consumes the regime flags and verifies that a current, in-scope protocol approval covers the expense.

## Evals

See [`evals/`](evals/).

## Provenance

Created 2026-05-21 as the detection layer of the federal cost-allowability analysis component set, to catch expenses tied to IRB-, IACUC-, and IBC-regulated activities.
