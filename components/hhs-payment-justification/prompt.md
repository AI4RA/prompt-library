---
name: hhs-payment-justification
version: "0.4.1"
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
> **Expected input:** One JSON fragment: the draw's expense lines with the sheet's cells copied, each classified by cost type, personnel role, and timeframe, plus the PI's prior wording when available.
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

You receive ONE JSON fragment in your context, the **draw lines**:
`{grant_code, sponsor_award_id, columns, draw_header, lines:[{row,
cells, pms_code, acct_code, sponsor_account, acct_class, description,
amount, cost_type, role, period_start, period_end, timeframe_basis,
prior_wording, flags}], flags}`.

Use ONLY this fragment. Do not reference the original uploaded
documents directly, and do not invent costs, people, roles, dates,
research topics, or purposes that the fragment does not contain. It
may arrive minified, with null keys omitted, or truncated mid-string;
salvage every field you can read rather than discarding it.

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

Keep the language general: link every cost to "the research
activities supported by this award". Do NOT name the research topic,
aims, journals, or why an item was bought; the PI adds specifics if
they want them.

**Payroll lines with `prior_wording`** (salary, fringe): reuse the
PI's sentence word for word, replacing only its dates with this
line's `period_start` and `period_end`, but ONLY when all of these
hold:
- this line has both `period_start` and `period_end`;
- the prior sentence contains a "from <date> to <date>" range to
  replace;
- the prior sentence contains no person's name, account or object
  code, or payroll run label.
If any fails, write the line from the patterns below instead (keeping
the PI's role wording when it is a role, not a name). The rules on
missing pay periods, plain language, plain ASCII, and personal
information below always win over prior wording.

Otherwise write one sentence per line, in these patterns:

- Salary and fringe:
  `Payment for <cost> for <role> from <period_start> to <period_end> to conduct the research activities supported by this award.`
- Services (e.g., animal facility):
  `Payment for <cost> for <the month of Month YYYY | period>, to support the research activities supported by this award.`
- Publication costs:
  `Payment for publication costs incurred in <Month YYYY> for a paper reporting results of research supported by this award.`
- Supplies and other purchases:
  `Payment for <cost> purchased in <Month YYYY> for use in the research activities supported by this award.`
- Travel:
  `Payment for travel in <Month YYYY> to conduct or present the research activities supported by this award.`
- **Total / subtotal rows** (`cost_type` "total"): leave the
  justification "".

Do not claim a cost is in the approved budget, was prior-approved,
or is allowable: nothing in the fragment shows that. The PI may add
such wording ("as described in the approved budget") after checking.

- **<cost>**: from `cost_type` ("salary", "fringe benefits",
  "services provided by the Laboratory Animal Research Facility",
  "laboratory supplies"). Plain words, no account codes.
- **<role>**: from `role`, as a ROLE, never a person's name ("project
  graduate research assistants", "project staff").
- **Timeframe**: use `period_start`–`period_end` as dates in
  M/D/YYYY form; for a whole month write "the month of September
  2026"; for a single date write "in October 2026". Never invent a
  date range.
- **Payroll with no pay period** (`period_start` missing and
  `timeframe_basis` starts "pay date"): write "for the pay period paid
  on <M/D/YYYY>" in place of "from ... to ...". Never present the pay
  date as the dates worked.
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
   missing, use the key "ACTIVITY"), holding your justification
   sentence for that line ("" for a total row).

Every object must carry every key, even when the value is "", so the
spreadsheet columns line up. Do not add any other key: no row
numbers, notes, totals, or flags (the sheet goes back to OSP as is).
If `columns` is missing, or any line's `cells` is missing or has a
different length from `columns`, use this fixed header list for EVERY
row instead (OSP's standard report columns, in order): PMSCode,
GrantCode, FundCode, BillRunDate, TransDate, DocCode, AcctCode,
BillingStatus, BillInvoiceSeqNum, AcctClassCode, ItemNumber,
Description, SponsorAccount, Amount, then the justification key. Fill
PMSCode = pms_code, AcctCode = acct_code, AcctClassCode = acct_class,
Description = description, SponsorAccount = sponsor_account, Amount =
amount, GrantCode = grant_code, and "" for any other column. Every row
must have the same keys in the same order either way.

Shape (values illustrative; the keys come from the sheet):
[{"PMSCode":"V0000P","GrantCode":"XX0000","FundCode":"000000","BillRunDate":"","TransDate":"46472","DocCode":"F0000000","AcctCode":"E4109","BillingStatus":"U","BillInvoiceSeqNum":"","AcctClassCode":"D","ItemNumber":"0","Description":"HR Payroll 2027 UI 6 0","SponsorAccount":"10-SALARY","Amount":"1500","ACTIVITY 03/13-26/2027 PER PI/DGA":"Payment for salary for project graduate research assistants from 2/28/2027 to 3/13/2027 to conduct the research activities supported by this award."}]

Emit raw JSON only. Your reply must start with `[` and end with `]`:
no code fence, no heading, no notes before or after (anything else
stops the CSV download from splitting the columns). Minify it on
one line. Escape any double quote inside a value as \" or rephrase.
