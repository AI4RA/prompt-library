# Funding Opportunity Finder

Turns a project idea, topic, sponsor or opportunity number into a short ranked list of current federal funding opportunities on grants.gov, each as a clickable link, and hands the chosen one on: a summary of the record with its attachment links, the full announcement read in pages, or the budget worksheet component. It is a chat-first component that also works as a step for another task, where it returns the best three hits in the shortest form.

**Current version:** 0.1.0
**Category:** research
**Domain:** research-administration
**Status:** experimental
**Manifestations:** prompt
**Output contract:** a Markdown list and summary block (see "Outputs"); no JSON schema
**Contract scope:** repo-local

## Inputs

A few words to a paragraph describing the research idea, field, target sponsor or program, or an opportunity number or title; optional constraints on sponsor, deadline, award size or eligibility. The component needs two tools at run time: one that searches grants.gov (keyword, status, agency and category filters, paging) and one that fetches a document by link and returns a grants.gov opportunity record or a page or PDF as text. The MindRouter add-in supplies both through the AI4RA eCFR MCP server.

## Outputs

A numbered list of at most ten opportunities ordered by fit, each with the title as a link to its grants.gov page, the number, agency, status, close date and one line on fit; the searches run with their hit counts; and a one-line offer of next steps. When the user picks one: a summary block of purpose, ceiling, floor, expected awards, close date, cost sharing, eligibility and attachment links, keeping the page link. When called by another task: the best three hits with links and the searches used.

## Contract scope

Repo-local. No schema; the output is prose for a person, with a compact form for an orchestrating task.

## Triad integration

- **Evaluation datasets:** none yet; repo-local evals only.
- **Harness notes:** live grants.gov results change daily, so cases pin the tool responses (recorded search and fetch results) and score presentation: every entry linked, no invented fields, forecast labelled, at most ten.
- **Shared UDM relationship:** none.

## Manifestations

- [`prompt.md`](prompt.md) — canonical prompt

## Evals

See [`evals/`](evals/). None yet.

## Provenance

Authored 2026-09-14 by nlayman for the MindRouter Office add-in, as the front end of the pre-award chain: find the announcement, read it, then build the budget with `narrative-to-budget-worksheet`.
