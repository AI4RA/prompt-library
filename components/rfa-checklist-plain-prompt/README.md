# RFA Checklist — Plain RA Prompt

A single natural-language prompt of the kind a research administrator might write when asking a general-purpose AI tool to turn a funding announcement into a pre-award checklist. It is the plain-prompt comparison condition for the governed [`rfa-checklist-extraction`](../../workflows/rfa-checklist-extraction/) workflow v3.1.0: same 11 checklist sections, none of the workflow's decomposition, schemas, or rendering rules.

**Current version:** 1.0.0
**Category:** extraction
**Domain:** research-administration
**Status:** experimental
**Manifestations:** prompt
**Output contract:** free-form checklist organized under the 11 named sections; no schema
**Contract scope:** repo-local

## Inputs

The full funding announcement (RFA / FOA / NOFO / program solicitation), attached the way a user of the tool would attach it, usually as the sponsor's PDF.

## Outputs

A checklist in whatever format the tool produces, organized under the 11 sections named in the prompt. The prompt asks for "Not stated" where the announcement is silent. There is no JSON contract, so outputs are not directly comparable field by field with the workflow's extraction fragments.

## Contract scope

Repo-local. The prompt names checklist sections that mirror the `rfa-checklist-extraction` workflow v3.1.0 Markdown deliverable, but it owns no structured output contract and does not align to shared AI4RA-UDM fields.

## Triad integration

- **Evaluation datasets:** none yet; no runs have been collected.
- **Harness notes:** none yet. The tools, models, input handling, replicates and scoring approach for this condition have not been decided.
- **Shared UDM relationship:** none.

## Manifestations

- [`prompt.md`](prompt.md) — canonical prompt

## Evals

No eval cases yet. See [`evals/`](evals/).

## Provenance

Drafted 2026-10-23 with Barrie Robison for the NCURA Region VI & VII RM2026 session "The Good, the Bad, and the Ungoverned," as the plain prompt most research administrators would write instead of a governed workflow. Adapted from the section list and section descriptions of the `rfa-checklist-extraction` workflow v3.1.0 (this repository, commit 9c0935e).
