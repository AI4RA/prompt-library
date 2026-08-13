# Changelog — NOA Summary workflow

Versions follow semver and match `workflow_version` in `manifest.yaml`.

## 1.0.0 — 2026-08-13

**MAJOR — remove the KB lookup step (3 steps → 2).** The optional `KnowledgeBaseQuery` Step 0 was inert on a fresh import (Vandalizer blanks `kb_uuid` by design, so the operator always had to attach a KB manually) and confused operators comparing the imported workflow against their live Vandalizer copies. Mirrors `rfa-checklist-extraction` v1.0.0 (PR #50) and `export-to-banner-extraction` v1.0.0 (PR #52).

- The parallel extraction tasks now read `input_sources: [workflow_documents]` only; the vestigial `step_input` (which carried the removed KB step's output) is dropped. Consolidation is unchanged.
- No prompt-body or validation-plan changes. `vandalizer.json` rebuilt (export name now carries the version per the build-script convention).
- KBs will be reintroduced once the right approach is settled.

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
