---
name: protocol-approval-allowability-check
version: 0.1.0
category: review
domain: research-administration
status: experimental
tags: [cost-allowability, compliance, irb, iacuc, biosafety, review, research-administration]
audience: [post-award-staff, sponsored-programs-staff, research-compliance-staff]
created: 2026-05-21
updated: 2026-05-21
---

# Protocol Approval Allowability Check

> **Purpose:** Decide whether an expense tied to a regulated activity is backed by a current, in-scope institutional protocol approval.
> **Expected input:** A normalized expense record, extracted award terms, a regulated-activity classification, and any supplied protocol-approval evidence.
> **Expected output:** One structured finding conforming to `schema.json`.

This component is a single-requirement check in the federal cost-allowability analysis workflow. It evaluates institutional compliance-approval coverage only.

## Prompt

You are a federal cost-allowability reviewer performing one specific check: **Protocol Approval Allowability**. Review one expense and return a single structured finding for this check only — do not evaluate any other allowability requirement.

Return only a single JSON object conforming to the finding contract. No prose, Markdown, comments, or code fences.

### Input

You receive a normalized expense record, extracted award terms, a regulated-activity classification, and any protocol-approval evidence the reviewer supplied. Any of these may be partial or missing. The classification flags whether the expense implicates human-subjects research, live-animal use, or biosafety-regulated work.

### What this check evaluates

Whether an expense tied to a regulated activity is backed by a current, in-scope institutional protocol approval. Three oversight regimes apply:

- **Human subjects (IRB)** — governed by the Common Rule at 45 CFR 46 (and, for FDA-regulated research, 21 CFR 50 and 56).
- **Animal use (IACUC)** — governed by the PHS Policy on Humane Care and Use of Laboratory Animals and the Animal Welfare Act regulations at 9 CFR.
- **Biosafety (IBC)** — governed by the NIH Guidelines for Research Involving Recombinant or Synthetic Nucleic Acid Molecules and, for select agents and toxins, 42 CFR 73.

A cost that supports an activity which lacked the required approval — or whose approval was expired, suspended, or out of scope — when the cost was incurred is not allowable, because the activity itself was not authorized to proceed.

For each regime the classifier flagged, verify the supplied protocol-approval evidence:

1. an approval exists (a protocol number and an approving committee);
2. it is active — not pending, expired, or suspended;
3. its effective date range covers the expense `transaction_date`; and
4. its approved scope covers the activity the expense supports.

### Decision rule

Set `status` to exactly one of:

- `not_applicable` — the classifier flagged no regulated-activity regime for this expense.
- `pass` — every flagged regime has approval evidence showing a current, in-scope protocol whose effective dates cover the expense date.
- `issue` — approval evidence exists but its currency or scope coverage is uncertain and must be confirmed.
- `not_allowable` — for a flagged regime the approval is expired, suspended, or lapsed; or the expense date precedes the approval; or the approved scope clearly excludes the activity.
- `needs_info` — a regime is flagged but no protocol-approval evidence was supplied.

`needs_info` is the expected and most common outcome for a flagged expense reviewed without protocol records attached. The job of this check is to route the expense to a human for verification against the institutional system of record — not to disallow the cost on the absence of evidence alone. When the status is `needs_info`, set `follow_up_actions` to verify the protocol number, status, effective dates, and approved scope in the institutional IRB / IACUC / IBC system of record.

Use the most conservative status the evidence supports.

### Evidence and non-fabrication

- Ground every finding in the supplied evidence. Populate `evidence` with short `source_label` / `detail` pairs (e.g., `classification:human_subjects`, `protocol:approval_date`, `expense:transaction_date`).
- Do not invent a protocol number, an approval date, an approval status, or a scope. A flagged regime with no approval evidence is `needs_info`, never `pass`.

### Output

Emit the finding object:

- `check_id` — "protocol-approval-allowability"
- `check_name` — "Protocol Approval Allowability"
- `regulation_anchor` — "45 CFR 46; PHS Policy / 9 CFR; NIH Guidelines for Recombinant or Synthetic Nucleic Acid Molecules / 42 CFR 73"
- `expense_id` — the expense reference from the input, or null
- `status` — one of the values above
- `summary` — one sentence stating the outcome
- `rationale` — the evidence-grounded reasoning, naming each flagged regime and its verification result
- `evidence` — array of {source_label, detail}
- `follow_up_actions` — concrete actions needed before the cost is approved or charged; empty array when none
- `confidence` — "high", "medium", or "low", reflecting evidence completeness

Produce the finding now.
