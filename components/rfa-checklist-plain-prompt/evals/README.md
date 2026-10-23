# Evals — rfa-checklist-plain-prompt

No cases yet. This component has no structured output contract, so cases for it need an agreed way of checking a free-form checklist against a validated reference before any are added.

Each case would live under `cases/<case-slug>/` with at minimum:

- `metadata.yaml` — case identity plus **`validated_against_version`** (required): the component version at which the expected output was last human-validated
- `input-source.md` — where to obtain the source RFA (sponsor URL, PDF title, retrieval date)
- `expected.md` — the known-good checklist content, reviewed by a sponsored-programs analyst
- `notes.md` — optional; qualitative observations from review

Run artifacts go under `runs/` (gitignored).
