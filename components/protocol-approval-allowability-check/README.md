# Protocol Approval Allowability Check

Checks whether an expense tied to a regulated activity is backed by a current, in-scope institutional protocol approval — IRB (human subjects), IACUC (animals), or IBC (biosafety). It is one of the single-requirement checks in the federal cost-allowability analysis workflow and emits a structured finding consumed by the final determination step.

**Current version:** 0.1.0
**Category:** review
**Domain:** research-administration
**Status:** experimental
**Manifestations:** prompt
**Output contract:** [`schema.json`](schema.json)
**Contract scope:** repo-local

## Inputs

A normalized expense record, extracted award terms, a regulated-activity classification, and any protocol-approval evidence the reviewer supplied, from the [`cost-allowability-analysis`](https://github.com/AI4RA/prompt-library/tree/main/workflows/cost-allowability-analysis) workflow. The classification (see [`regulated-activity-classifier`](../regulated-activity-classifier/)) determines which oversight regimes this check verifies.

## Outputs

A single structured finding — see [`schema.json`](schema.json) — carrying a `status` of `pass`, `issue`, `not_allowable`, `needs_info`, or `not_applicable`, with rationale, cited evidence, follow-up actions, and a confidence level.

## The check

For each oversight regime the classifier flagged, verifies that the supplied protocol-approval evidence shows an approval that exists, is active, has effective dates covering the expense date, and has an approved scope covering the activity. It applies the Common Rule (45 CFR 46), PHS Policy and the Animal Welfare Act regulations (9 CFR), and the NIH Guidelines for recombinant or synthetic nucleic acids (with 42 CFR 73 for select agents).

When a regime is flagged but no protocol records are attached, the check returns `needs_info` — its purpose is to route the expense to a human for verification against the institutional IRB / IACUC / IBC system of record, not to disallow the cost on absence of evidence alone. When no regime is flagged, it returns `not_applicable`.

## Contract scope

Repo-local. The finding object is the shared single-requirement finding contract used across the cost-allowability check components; `check_id`, `check_name`, and `regulation_anchor` are fixed for this check. It is not a shared AI4RA-UDM schema.

## Triad integration

- **Evaluation datasets:** none yet — repo-local synthetic coverage planned.
- **Harness notes:** canonical manifestation is `prompt.md`; validation surface is `schema.json`. Invoked as a Step 2 task of the `cost-allowability-analysis` workflow; its applicability is gated by the `regulated-activity-classifier` output.
- **Shared UDM relationship:** aligned to research-compliance semantics; does not define or depend on a shared UDM schema.

## Manifestations

- [`prompt.md`](prompt.md) — canonical, LLM-agnostic prompt

## Related components

- [`regulated-activity-classifier`](../regulated-activity-classifier/) — produces the regime flags that gate this check.
- [`cost-prior-approval-check`](../cost-prior-approval-check/) — the companion check for federal sponsor prior approval, a distinct regulatory regime from institutional protocol approval.

## Evals

See [`evals/`](evals/).

## Provenance

Created 2026-05-21 as the compliance-oversight check in the federal cost-allowability analysis component set, to catch costs tied to IRB-, IACUC-, and IBC-regulated activities that lack a current, in-scope protocol approval.
