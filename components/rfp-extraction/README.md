# RFP Extraction

Extracts a comprehensive submission and eligibility checklist from any federal funding announcement — RFP, RFA, FOA, NOFO, BAA, Dear Colleague Letter, or program solicitation. Output is a single markdown document with GFM checkboxes that PIs can use for proposal development and OSP staff can use for pre-submission compliance review.

**Current version:** 1.1.0
**Last fully evaluated:** 1.0.0 — agent manifestation added in 1.1.0 without re-running evals
**Category:** extraction
**Domain:** research-administration
**Status:** stable
**Manifestations:** prompt, skill, agent
**Output contract:** `prompt.md` plus `evals/cases/*/expected.md` golden outputs

## Inputs

Full text of a funding announcement — pasted text, attached document, or URL.

## Outputs

A single markdown document containing a structured checklist:

- Header block (solicitation metadata)
- Key dates
- Eligibility requirements (organizational, PI, cost sharing)
- Pre-submission requirements (if applicable)
- Full-proposal general requirements (logistics, page limits, standard documents)
- Project description / narrative required sections
- Supplemental materials (required and prohibited)
- Budgetary requirements
- Merit review criteria
- Special award conditions and post-award requirements
- Deviations from parent guide / standard procedures
- Contacts and resources

Every actionable item is expressed as a `- [ ]` checkbox so the output functions directly as a tracking document.

## Manifestations

- [`prompt.md`](prompt.md) — canonical, LLM-agnostic prompt
- [`skill/SKILL.md`](skill/SKILL.md) — Claude Skill form for use with Claude Code / Agent SDK
- [`agent/AGENT.md`](agent/AGENT.md) — subagent form (`rfp-extractor`) that resolves file/URL/text inputs, writes output, and reports a one-line summary

## Evals

See [`evals/`](evals/) for reference inputs and known-good outputs. The initial golden case is NSF 26-508 (TechAccess), a multi-round solicitation with LOI requirements and several deviations from PAPPG defaults.

## Provenance

Original prompt authored 2026-04-17 during preparation of the NSF 26-508 submission checklist. First validated output is the NSF 26-508 case under `evals/cases/`.
