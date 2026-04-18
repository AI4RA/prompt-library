# Evals — rfp-extraction

## Structure

Each case lives under `cases/<case-slug>/` with:

- `metadata.yaml` — solicitation identifier, source URL, notes on why this case is interesting (edge cases exercised, parent-guide deviations, structural complexity)
- `input-source.md` — where to obtain the source announcement (URL, document version, date retrieved). Full source text is not committed when it is long or hosted elsewhere; `input-source.md` must contain enough information to reproduce.
- `input.md` — the full source text when it is short enough or cannot be reliably re-fetched. Optional when `input-source.md` points to a stable URL.
- `expected.md` — the known-good checklist output, validated by a human reviewer.
- `notes.md` — optional; qualitative observations from review (what the reviewer caught, what the prompt missed, what edge cases surfaced).

Run outputs go under `runs/` (gitignored). Commit only `expected.md` and metadata.

## Case selection

Pick cases that exercise distinct structural features:

- Single vs. multi-round deadlines
- LOI / preliminary proposal / white paper pre-submission steps
- Per-institution and per-PI proposal limits
- Cost-sharing required / prohibited / optional
- Significant deviations from the parent guide (PAPPG, SF424 Guide, etc.)
- Non-standard required or prohibited supplements
- Award conditions that affect proposal content (e.g., mandatory collaboration)

## Current cases

- `NSF_26-508/` — TechAccess: AI-Ready America. Multi-round (3 rounds), LOI required, per-organization limit of one proposal per round, PAPPG-based, several deviations.
