# Viva Engage

Single-step Vandalizer workflow that reformats a table of
proposal-submission information (e.g. rows from an Excel export) into
per-proposal "Proposal Submission" announcement blocks — proposal
number, title, sponsor, prime sponsor, principal investigator, and
budget total — suitable for pasting into Microsoft Teams / Viva Engage.

## Topology

| Step | Task | Input | Output |
|---|---|---|---|
| 1. Reformatting Prompt (output step) | `viva-engage-reformat` (Prompt) | `step_input` (pasted / step-provided table text) | One fixed-format "Proposal Submission" block per input row |

The prompt body lives in `components/viva-engage-reformat/prompt.md`
and is inlined into the generated JSON at build time.

## Import

Import `viva-engage.vandalizer.json` into Vandalizer. No knowledge
base and no model pin: the run dialog's model selection applies.

## Provenance

Captured 2026-08-18 from the University of Idaho RA team's live
Vandalizer workflow of the same name (exported by
brobison@uidaho.edu). Two deliberate deltas from the live export:

1. The live task referenced its prompt by `saved_prompt_uuid`; the
   repo version inlines the prompt text so the generated JSON is
   self-contained on import.
2. The live task pinned `model: qwen/qwen3.6-27b`. The repo version
   drops the pin (consistent with `rfa-checklist-extraction` v3.1.0);
   that string is a known-valid `available_models[].name` on the
   server if a pin is ever wanted again.

## Status

Experimental — not yet re-tested from a repo-built import. First
re-test: import the generated JSON, paste a real proposal-submission
table, and check the four `VE-*` validation-plan items (one block per
row, all six labels, verbatim values, no surrounding prose).
