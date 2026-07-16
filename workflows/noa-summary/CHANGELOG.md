# Changelog — NOA Summary workflow

Versions follow semver and match `workflow_version` in `manifest.yaml`.

## 0.2.0 — 2026-07-15

- Added the contact anti-hallucination guard to both extraction prompts and
  consolidation Part 1 (never invent a contact name / title / email / phone;
  absent → "Not specified in the document"), after a validation run occasionally
  fabricated a press contact. No structural change.

## 0.1.0 — 2026-07-15

- Initial AI4RA rebuild of the public NOA Summary workflow. Variant A + KB
  injection topology (KB Context Lookup → two parallel extraction prompts →
  five-part Markdown consolidation), an always-render anti-leak consolidation,
  and a runtime-schema validation plan (structure, core fields, monetary/date
  fidelity, placeholder discipline). Validated end-to-end in Vandalizer against
  an NIH R25 Notice of Award.
