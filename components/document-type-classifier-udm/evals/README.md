# Evals — document-type-classifier-udm

## Structure

Each case lives under `cases/<case-slug>/` with:

- `metadata.yaml` — case identity, structural features exercised, and (required) `validated_against_version`
- `input.md` — the text sent to the classifier (typically the first N pages or the whole short body). Inline for compactness; this component's input is text, not PDF bytes.
- `input-source.md` — where the underlying source document originated (URL, sponsor, retrieval date)
- `expected.json` — the known-good classifier output, validated by a human reviewer and conforming to `../schema.json`
- `notes.md` — optional observations from validation

Run artifacts go under `runs/` (gitignored).

## Validating `expected.json`

```
check-jsonschema --schemafile components/document-type-classifier-udm/schema.json \
  components/document-type-classifier-udm/evals/cases/*/expected.json
```

## Case selection

Prefer cases that each exercise distinct structural features:

- **Vocabulary coverage** — at least one case per controlled code over time (the initial set does not aim for full coverage; it exercises the confidence bands and the sponsor-agnostic rule)
- **Sponsor diversity** — NSF, NIH, DoE, foundations; documents that look similar across sponsors
- **Initial vs. amendment** — award notices with amendment_number "000" vs. any other value
- **Self-identifying vs. structural-only** — documents that carry a canonical header label vs. documents classified from layout alone
- **Unambiguous vs. ambiguous** — top confidence above 0.8 (empty `secondary_candidates`) vs. below 0.8 (populated `secondary_candidates`)
- **`other` cases** — documents outside the vocabulary (emails, internal memos, unrelated correspondence) that should emit `document_type: "other"` with low confidence

## Current cases

- `nsf-pd-23-221y-solicitation/` — NSF program solicitation first-page text. Exercises the self-identifying-phrase rule, high confidence, empty secondary candidates.
- `nih-noa/` — NIH Notice of Award header block. Exercises the sponsor-agnostic rule (non-NSF award notice), high confidence, empty secondary candidates.
- `ambiguous-letter/` — a short letter that could read as either `letter_support` or `other`. Exercises the 0.5–0.7 confidence band and the `secondary_candidates` emit rule.
