---
name: noa-summary-udm
version: "0.1.0"
category: extraction
domain: research-administration
status: experimental
tags: [noa, notice-of-award, grant-award-summary, post-award, compliance, financial, udm, structured-extraction, json]
audience: [sponsored-programs-staff, post-award-teams, ingest-pipelines]
owner: ui-insight
created: 2026-07-15
updated: 2026-07-15
---

# NOA Summary — UDM JSON

> **Purpose:** Extract award identification, key personnel and federal contacts, financial terms, periods of performance, reporting deadlines, and compliance/administrative obligations from a federal Notice of Award (NoA) into a single structured JSON object that downstream tooling can use to drive a post-award grant award summary.
> **Expected input:** Full text of a federal Notice of Award / agreement.
> **Expected output:** A single JSON object that validates against [`schema.json`](schema.json). No prose, no markdown outside the JSON.

## When to use this contract

Use this contract when a machine-readable extraction of a Notice of Award is
needed — e.g. to populate a post-award record, drive a reporting calendar, or
feed an evaluation harness. The end-user-facing Markdown deliverable is produced
by the `workflows/noa-summary` Vandalizer workflow, which reads the same source
document; this component is the JSON-emitting contract used by tooling.

## Rules

- Extract every fact from the NoA itself. Quote dollar amounts and dates
  verbatim. Never invent values, names, or phone numbers.
- The project lead may appear under any PI synonym (PI, Contact PI, Project
  Director, PD, Grantee Project Director, Recipient Project Manager, RPM).
- Use `null` for any field the document does not state.

## Output

Emit exactly one JSON object conforming to `schema.json`. No preamble, no
markdown fences.
