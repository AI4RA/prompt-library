# Narrative to Budget Worksheet

Builds a first-draft proposal budget worksheet from a project narrative and/or a funding announcement. The component reads what the documents say (team, activities, trips, equipment; sponsor ceiling, caps, cost sharing), asks the user one question at a time for the numbers only the institution, the PI or the sponsor can supply (an empty reply or "skip" takes the stated estimate), estimates what is not supplied, and writes a worksheet in which every derived cell is a spreadsheet formula and every estimate is filled yellow. It is the estimation head of the budget pipeline: its summary block is laid out so that `nsf-budget-spreadsheet-ingest-udm` can read it and the justification drafters can follow.

**Current version:** 0.1.0
**Category:** drafting
**Domain:** research-administration
**Status:** experimental
**Manifestations:** prompt
**Output contract:** a worksheet (see "Outputs"); no JSON schema
**Contract scope:** repo-local

## Inputs

Any of, and at least one of the first two:

- A project narrative: proposal text, specific aims, or a summary. Supplies the team, activities, trips, participants, equipment and subawards.
- A funding announcement (RFA / NOFO / solicitation). Supplies the ceiling, project length, F&A and salary caps, cost sharing and allowed categories.
- A rates block from the institution: salaries, fringe by class, F&A rate and base, tuition, stipend, escalation, equipment threshold.
- PI decisions: effort in person-months, trips, participants, quantities, subaward totals.

With only an announcement the component proposes a minimal template team as estimates.

## Outputs

A new worksheet with six blocks: title and legend; inputs (value, origin, note) holding every rate and decision; personnel with per-year months, salary and fringe; detail blocks for equipment, travel, participant support and other direct costs; an A–H summary by year with total direct costs, MTDC base, indirect costs and total project cost; and checks against the sponsor's ceiling, per-year limit, salary cap, F&A cap and the NSF two-month rule. Derived cells are formulas referencing the inputs block; estimated inputs are filled yellow. Without a spreadsheet, the inputs and summary blocks are Markdown tables with estimates marked and formulas written in words.

## Contract scope

Repo-local. The worksheet is not a JSON contract. Its summary rows use the NSF category letters A–H and the same sub-lines as `#/$defs/input` in `../nsf-budget-justification-udm/schema.json`, so the sheet can be ingested by `nsf-budget-spreadsheet-ingest-udm` without a mapping step.

## Triad integration

- **Evaluation datasets:** none yet; repo-local evals only.
- **Harness notes:** the canonical manifestation is `prompt.md`. The component is conversational (it asks before it builds), so a harness case needs scripted replies to the Step 2 questions, one per turn. Scoring: structural (blocks present, every summary cell a formula, every estimate marked) is checkable from the sheet; the estimates themselves need a pre-award reviewer.
- **Shared UDM relationship:** none owned; summary rows align to ProposalBudget semantics by convention only.

## Manifestations

- [`prompt.md`](prompt.md) — canonical prompt

## Evals

See [`evals/`](evals/). None yet.

## Provenance

Authored 2026-09-14 by nlayman for the MindRouter Office add-in, where it runs as a skill in Excel: the model asks in the chat pane, then builds the sheet with the add-in's range, formula and format tools. It fills the gap that every other budget component in this library assumes away: a budget that already exists.
