# FOA Checklist Extraction — UDM JSON

Extracts a Federal Funding Opportunity Announcement (FOA) into a structured JSON object covering the eight reference sections a federal-grants office uses for FOA review: FOA summary, key dates, funding information, eligibility, application components, evaluation process, program priorities, and special requirements. Stronger emphasis than its sibling `rfa-checklist-extraction-udm` on the **evaluation criteria**, **review process**, and **submission system** fields.

**Current version:** 0.1.0
**Category:** extraction
**Domain:** research-administration
**Status:** experimental
**Manifestations:** prompt
**Output contract:** [`schema.json`](schema.json)
**Contract scope:** repo-local, UDM-aligned

## Inputs

Full text of an FOA (HHS / NIH / DOE / DOD / agency-issued funding opportunity announcement) — pasted text, attached PDF/DOCX/HTML, or URL.

## Outputs

A single JSON object covering 31 schema fields organized around the eight FOA reference sections (see [`prompt.md`](prompt.md) for the full breakdown). Headline blocks: `evaluation_criteria` (with weights), `review_stages` (sequential), `program_goals` (table), `required_registrations` (SAM/UEI/eRA Commons/Grants.gov), `required_forms`, `application_components`, `page_limits` (with `what_counts` rules).

See [`schema.json`](schema.json) for the authoritative definition.

## Contract scope

Repo-local, UDM-aligned. UDM bindings: `foa_number` → `RFA.Opportunity_Number`; `cfda_number` → `RFA.CFDA_Number`; `federal_agency` → `Organization.Organization_Name`; `foa_title` → `RFA.RFA_Title`. The structured shape mirrors the deliverable produced by the [`foa-checklist-extraction` Vandalizer workflow](https://github.com/ui-insight/ProcessMapping/tree/main/workflows/foa-checklist-extraction) in the ui-insight/ProcessMapping process-mapping corpus.

## Relationship to `rfa-checklist-extraction-udm`

| Concern | `rfa-checklist-extraction-udm` | `foa-checklist-extraction-udm` (this) |
| --- | --- | --- |
| Emphasis | NSF/NIH solicitation triage; placement-rule de-duplication | FOA review with strong evaluation-criteria, review-process, and submission-system focus |
| Output sections | 8 (dates, institutions, individuals, award, components, budget, submission, special, notes) | 8 (FOA summary, key dates, funding, eligibility, application components, evaluation process, program priorities, special requirements) |
| Distinct fields | `cost_sharing.status` enum; `important_notes` synthesis | `evaluation_criteria` table with weights; `review_stages` sequential list; `program_goals` table |

A single announcement can be extracted through both contracts when the downstream consumer needs both cuts.

## Triad integration

- **Evaluation datasets:** none yet — planned: NIH PA/PAR/RFA with multi-stage review (LOI → full → panel → council); DOE FOA with explicit point-weighted evaluation criteria; HHS NOFO with required pre-application registrations (SAM, UEI, eRA Commons).
- **Harness notes:** canonical manifestation is `prompt.md`. The companion top-level `workflows/foa-checklist-extraction` Vandalizer workflow at v0.1.0 implements the contract as six parallel Extraction tasks plus a Consolidation Prompt.

## Runtime topology — the Vandalizer workflow

The canonical runtime is the [`foa-checklist-extraction` workflow](https://github.com/AI4RA/prompt-library/tree/main/workflows/foa-checklist-extraction).

- **Step 1 (parallel Extraction)** — six Extraction tasks mirroring the source ProcessMapping workflow one-for-one (FOA Identification & Timeline, Evaluation Criteria, Review Process, Agency Priorities & Goals, Forms & Submission Systems, Formatting Requirements).
- **Step 2 (Consolidation Prompt)** — assembles the six fragments into a single schema-conformant object and enforces the cross-field reconciliation between `expected_awards`, `award_range`, and `total_funding`.

## Manifestations

- [`prompt.md`](prompt.md) — canonical, LLM-agnostic prompt

## Evals

See [`evals/`](evals/) for reference inputs and known-good outputs.

## Provenance

Authored 2026-04-30 against the `foa-checklist-extraction` (Workflow_ID: `WF-FOA-CHECKLIST-EXTRACTION`) process-mapping workflow in `ui-insight/ProcessMapping` at commit `b7176b0c913833a205efdb5e4ba00c17ff88af0f`.
