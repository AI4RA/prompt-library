# Proposal Document Completeness — UDM JSON

Automates the near-final document-completeness review of a proposal package: identifies all senior key personnel, the four required documents per person (biosketch, current & pending, collaboration & affiliation, synergistic activities), subaward documents, and conditional-requirement triggers. Produces a single gap-analysis JSON for sponsored-programs analysts to use when sending a "missing documents" message back to the PI.

**Current version:** 0.1.0
**Category:** extraction
**Domain:** research-administration
**Status:** experimental
**Manifestations:** prompt
**Output contract:** [`schema.json`](schema.json)
**Contract scope:** repo-local, UDM-aligned

## Inputs

A proposal package — VERAS upload bundle, NSF/NIH proposal in PDF/DOCX form, plus the relevant solicitation (RFA / FOA / NOFO).

## Outputs

A single JSON object with three logical layers:

- **As-found inventory** — `sponsor_name`, `rfa_foa_number`, `proposal_track_type`, `review_type`, `senior_key_personnel`, `budget_personnel`, `has_postdocs_or_grad_students`, `has_subawards`, `uploaded_documents`
- **Sponsor requirements** — `required_documents_checklist`, `conditional_requirements`, `per_person_required_documents`, `subaward_required_documents`
- **Gap analysis** — `per_person_document_matrix` (one row per person × four required documents with a `missing` list), `subaward_documents` (one row per subawardee × six required documents), `personnel_discrepancies`, `prioritized_missing`

See [`schema.json`](schema.json) for the authoritative definition and [`prompt.md`](prompt.md) for the encoding rules (booleans must be derived from observable signals; the matrix is keyed on `senior_key_personnel`; `prioritized_missing` ranks compliance-critical gaps first).

## Contract scope

Repo-local, UDM-aligned. `sponsor_name` resolves to UDM `Sponsor_Organization`; `senior_key_personnel` rows resolve to `Personnel`; `has_subawards: true` triggers `Subaward` presence; the proposal record itself resolves to `Proposal`. The structured shape does not duplicate any shared UDM schema — it mirrors the deliverable produced by the [`proposal-document-completeness` Vandalizer workflow](https://github.com/ui-insight/ProcessMapping/tree/main/workflows/proposal-document-completeness) in the ui-insight/ProcessMapping process-mapping corpus.

## Triad integration

- **Evaluation datasets:** none yet — planned: NSF proposal with TTP-P track triggering letter-of-collaboration; NIH proposal with postdocs triggering mentoring plan; proposal with subawards exercising the subaward matrix; proposal with name mismatches between budget and Section 2.
- **Harness notes:** canonical manifestation is `prompt.md`. Validation surface is `schema.json`. The companion top-level `workflows/proposal-document-completeness` Vandalizer workflow at v0.1.0 implements the contract as two parallel Extraction tasks (proposal components + sponsor requirements) plus a Consolidation Prompt; record both single-call and post-consolidation signals when both are available.
- **Shared UDM relationship:** aligned, not owning.

## Runtime topology — the Vandalizer workflow

The canonical runtime is the [`proposal-document-completeness` workflow](https://github.com/AI4RA/prompt-library/tree/main/workflows/proposal-document-completeness) shipped at the top level of this repo.

- **Step 1 (parallel Extraction)** — two Extraction tasks. `extract-proposal-components` captures what's *in* the package (senior key personnel, budget personnel, subaward presence, the per-person matrix). `extract-sponsor-requirements` captures what *should* be there per the solicitation (required documents checklist, conditional requirements, per-person and per-subawardee required documents).
- **Step 2 (Consolidation Prompt)** — joins the as-found inventory with the sponsor requirements, derives the `missing` lists per person and per subawardee, computes the conditional triggers, surfaces personnel discrepancies, and ranks `prioritized_missing`.

## Manifestations

- [`prompt.md`](prompt.md) — canonical, LLM-agnostic prompt

## Evals

See [`evals/`](evals/) for reference inputs and known-good outputs.

## Provenance

Authored 2026-04-30 against the `proposal-document-completeness` (Workflow_ID: `WF-PROPOSAL-DOC-COMPLETENESS`) process-mapping workflow in `ui-insight/ProcessMapping` at commit `b7176b0c913833a205efdb5e4ba00c17ff88af0f`, which was built from walkthrough transcripts of the near-final-doc-review process (13-step process). Created to make that workflow a harness-evaluatable, versioned artifact.
