# Evals — proposal-document-completeness (workflow-local)

This workflow carries its own cases under `cases/` because the Consolidation & Gap Analysis Prompt does substantial work — it joins the as-found inventory with the sponsor requirements, derives `present` and `triggered` booleans, computes per-person and per-subawardee `missing` lists, and ranks `prioritized_missing` — so the workflow's behavior emerges from step interactions that no component-level eval can cover on its own.

## What workflow-local cases need to exercise

- **Join correctness** — every `senior_key_personnel` row produces exactly one `per_person_document_matrix` row; every subawardee in the inventory produces exactly one `subaward_documents` row.
- **`present` derivation** — the consolidator marks documents present iff they appear in `uploaded_documents` matching the right name.
- **Conditional triggers** — `conditional_requirements.triggered` correctly fires when `has_postdocs_or_grad_students` (mentoring plan) or when `proposal_track_type` contains "TTP" (letter of collaboration).
- **`missing` list derivation** — the per-person and per-subawardee `missing` arrays equal the false-valued document booleans for that row.
- **`prioritized_missing` ranking** — compliance-critical first, then per-person required documents, then conditional documents whose condition is triggered, then optional improvements; present documents do not appear.
- **Validation-plan checks** — personnel list completeness (CHK-01), required documents coverage (CHK-02), per-person document verification (CHK-03).

## Status

The initial scaffolded case (`nsf-ttp-p-with-postdocs-stub`) is a placeholder pending sponsored-programs review against an authorized, de-identified NSF TTP-P-track proposal that includes postdocs (so it exercises both conditional-requirement triggers).
