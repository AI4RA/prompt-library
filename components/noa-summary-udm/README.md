# noa-summary-udm

JSON extraction contract for a federal **Notice of Award (NoA)**. Extracts award
identification, key personnel and federal contacts, financial terms, periods of
performance, reporting deadlines, and compliance/administrative obligations into
a single structured JSON object (see [`schema.json`](schema.json)).

- **Input:** full text of a federal Notice of Award / agreement.
- **Output:** one JSON object conforming to `schema.json` (no prose).
- **Contract scope:** repo-local, UDM-aligned. Not the shared `ui-insight/AI4RA-UDM`
  contract.

The end-user-facing Markdown Grant Award Summary is produced by the
[`workflows/noa-summary`](../../workflows/noa-summary) Vandalizer workflow, which
reads the same source document. This component is the JSON-emitting contract for
tooling and evaluation.

See [`prompt.md`](prompt.md) for the extraction prompt and [`CHANGELOG.md`](CHANGELOG.md)
for version history.
