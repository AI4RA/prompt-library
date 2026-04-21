# [Component Name]

[One-paragraph summary of what the task is: input, output, and the problem it solves.]

**Current version:** 1.0.0
**Category:** [see `taxonomy.md`]
**Domain:** [see `taxonomy.md`]
**Status:** experimental
**Manifestations:** prompt
**Output contract:** [schema path or a short description of the canonical output surface]
**Contract scope:** [repo-local / UDM-aligned repo-local / delegated wrapper]

## Inputs

[Describe the expected input: format, required fields, typical size.]

## Outputs

[Describe the output contract: format, structure, guarantees.]

## Contract scope

[State clearly whether this component owns a repo-local contract, aligns to shared UDM semantics without owning the shared UDM, or delegates to another local schema.]

## Triad integration

- **Evaluation datasets:** [dataset IDs in `AI4RA/evaluation-data-sets`, or "none yet; repo-local evals only"]
- **Harness notes:** [canonical manifestation, validation surface, pinning expectations]
- **Shared UDM relationship:** [if applicable]

## Manifestations

- [`prompt.md`](prompt.md) — canonical prompt

## Evals

See [`evals/`](evals/) for reference inputs and known-good outputs.

## Provenance

[Who authored it, when, and what real task prompted its creation.]
