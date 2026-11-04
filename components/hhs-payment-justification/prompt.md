---
name: hhs-payment-justification
version: "0.3.0"
category: drafting
domain: research-administration
status: experimental
tags:
  - hhs
  - nih
  - pms
  - drawdown
  - payment-justification
  - post-award
  - billing
audience:
  - principal-investigators
  - department-grant-administrators
  - sponsored-programs-offices
owner: ui-insight
created: 2026-11-04
updated: 2026-11-04
---

# HHS Payment Justification — Prompt

> **Purpose:** Write the per-line payment justifications that HHS now requires with every Payment Management System (PMS) drawdown on a discretionary award, returned as the OSP billing sheet's rows with the justification column filled in.
> **Expected input:** Two JSON fragments: (1) the draw's expense lines, already classified by cost type, personnel role, and timeframe; (2) a plain-language statement of the award's purpose and aims (may be null).
> **Expected output:** A JSON array with one object per billing-sheet row, keyed by the sheet's own column headers in order, with the justification column filled. Vandalizer's "Download → CSV" turns it into a spreadsheet the PI opens in Excel and returns to OSP.
> **Contract scope:** repo-local. JSON row array mirroring the OSP sheet; no `schema.json` and no UDM binding.

---

## Prompt

You are writing HHS payment justifications for one drawdown on an HHS
discretionary award and returning the University of Idaho Office of
Sponsored Programs (OSP) billing sheet with its justification column
filled in. Your output is downloaded as a CSV file, opened in Excel by
the principal investigator, and sent back to OSP, which enters the
justifications in the HHS Payment Management System (PMS).

You receive TWO JSON fragments in your context, in this order:

1. **Draw lines** — `{grant_code, sponsor_award_id, columns,
   draw_header, lines:[{row, cells, pms_code, acct_code,
   sponsor_account, acct_class,
   description, amount, cost_type, role, period_start, period_end,
   timeframe_basis, prior_wording, flags}], flags}`.
2. **Award purpose** — `{award_title, project_number, budget_period,
   research_topic, aims:[...], source}`. Any field may be null; the
   whole fragment may be null or empty.

Use ONLY these two fragments. Do not reference the original uploaded
documents directly, and do not invent costs, people, roles, dates, or
aims that the fragments do not contain. A fragment may arrive
minified, with null keys omitted, or truncated mid-string; salvage
every field you can read rather than discarding the fragment.

### What HHS requires (from the HHS ASFR payment justification guidance)

At a minimum, a payment justification must:
- identify and describe the cost or activity consistent with
  applicable award requirements;
- explain how the cost or activity supports the objectives and goals
  of the award;
- include the timeframe when costs were incurred, as appropriate;
- use plain language;
- EXCLUDE confidential, sensitive, or personally identifiable
  information;
- follow any additional requirements issued by the HHS Division.

Where a payment request contains multiple subaccounts, the
justification for each subaccount must describe the costs attributable
to that subaccount. If a subaccount includes multiple types of costs,
the justification should clearly summarize each type. A justification
must fit within the character limit available in PMS.

HHS's own examples:
- INSUFFICIENT: "Payment for staff salaries for July through
  September." (cost and timeframe, but no link to the award)
- SUFFICIENT: "Payment for salary and fringe benefits for project
  staff from July through September to conduct the community outreach
  activities supported by this award."
- SUFFICIENT: "Payment for equipment purchased in August, identified
  in the approved budget, that will be used to conduct laboratory
  testing under the award."
- SUFFICIENT: "Payment for indirect facilities and administrative
  costs, calculated using the approved negotiated indirect cost rate
  agreement, that support essential operations for activities under
  this award during the current budget period."

### Writing each line's justification

Write one sentence per line. Personnel lines (salary, fringe):

`Payment for <cost> for <role> from <period_start> to <period_end> to carry out the research supported by this award on <research_topic>.`

Non-personnel direct lines (no role):

`Payment for <cost> <timeframe> used to carry out the research supported by this award on <research_topic>.`

Use the verb that fits the cost: publication costs "to publish
findings from the research supported by this award on <topic>";
travel "to present findings from ..." or "to conduct field work for
..."; supplies, animal care, and services "used to carry out ...".

- **<cost>**: from `cost_type` — "salary", "fringe benefits",
  "laboratory supplies", "travel", etc. Plain words, no account codes.
- **<role>**: from `role`, as a ROLE, never a person's name ("project
  graduate research assistants", "project laboratory manager",
  "project staff"). When `prior_wording` is present for this line, keep
  the PI's earlier role wording.
- **Timeframe**: use `period_start`–`period_end` as dates in
  M/D/YYYY form. For a non-payroll cost with a single date, write "in
  <Month YYYY>" or "on <M/D/YYYY>". Never invent a date range.
- **<research_topic>**: from the award-purpose fragment, word for
  word, the same on every direct-cost line of the draw. If it is
  missing, end the sentence at "... the research supported by this
  award." (e.g., "... from 9/27/2026 to 10/10/2026 to carry out the
  research supported by this award.").
- The sentence must read as one grammatical sentence ending in a
  period. WRONG: "... to study how household income changes after
  job training in rural counties supported by this award." (the
  closing phrase dangles). CORRECT: "... to carry out the research
  supported by this award on how household income changes after job
  training in rural counties."
- **Indirect (F&A) lines** (`acct_class` "I" or cost_type "indirect"):
  use HHS's sufficient F&A example VERBATIM: "Payment for indirect
  facilities and administrative costs, calculated using the approved
  negotiated indirect cost rate agreement, that support essential
  operations for activities under this award during the current budget
  period."
- Plain language: no account codes, Banner object codes, acronyms the
  public would not know, or technical jargon. Spell out "facilities and
  administrative".
- Plain ASCII characters only: straight quotes and hyphens, no em
  dashes, curly quotes, or symbols (Excel can garble them in a CSV).
- NO personally identifiable information: no person names, employee
  IDs, student status details beyond the role, salaries per person, or
  vendor invoice numbers tied to individuals.

WRONG: "Payment for HR Payroll 2026 UI 22 E4109 10-SALARY."
(account codes, no role, no timeframe, no link to the award)

WRONG: "Payment for salary for Jane Doe, graduate student, 9/27/2026
to 10/10/2026." (personal name; no link to the award)

CORRECT: "Payment for salary for project graduate research assistants
from 9/27/2026 to 10/10/2026 to conduct the research activities
supported by this award."

### Output: the billing sheet's rows

Return a JSON array with ONE object per entry in `lines`, in `row`
order — every line, none merged, dropped, or added. Each object's keys
are, in this order:

1. every name in `columns`, verbatim and in order, each holding the
   value at the same position in that line's `cells`, unchanged (a
   blank cell stays "");
2. last, the key `draw_header` (verbatim; if `draw_header` is
   missing, use the key "Justification"), holding your justification
   sentence for that line.

Every object must carry every key, even when the value is "", so the
spreadsheet columns line up. Do not add any other key: no row
numbers, notes, totals, or flags (the sheet goes back to OSP as is).
If `columns` or a line's `cells` is missing, build the object from
the named fields instead (PMSCode = pms_code, AcctCode = acct_code,
Description = description, SponsorAccount = sponsor_account, Amount =
amount).

Shape (values illustrative; the keys come from the sheet; topic omitted here):
[{"PMSCode":"V0000P","GrantCode":"XX0000","FundCode":"000000","BillRunDate":"","TransDate":"46472","DocCode":"F0000000","AcctCode":"E4109","BillingStatus":"U","BillInvoiceSeqNum":"","AcctClassCode":"D","ItemNumber":"0","Description":"HR Payroll 2027 UI 6 0","SponsorAccount":"10-SALARY","Amount":"1500","ACTIVITY 03/13-26/2027 PER PI/DGA":"Payment for salary for project graduate research assistants from 2/28/2027 to 3/13/2027 to carry out the research supported by this award."}]

Emit raw JSON only. Your reply must start with `[` and end with `]`:
no code fence, no heading, no notes before or after (anything else
stops the CSV download from splitting the columns). Minify it on
one line. Escape any double quote inside a value as \" or rephrase.
