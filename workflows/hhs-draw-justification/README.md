# HHS Draw Justification

Drafts the payment justifications HHS now requires with every Payment
Management System (PMS) drawdown on a discretionary award. Upload the
OSP "Billed-Unbilled Detail by PMS Code" spreadsheet (and, ideally, the
PI's last completed sheet); the workflow returns the same sheet with the justification column filled in, one justification per
expense line, as a CSV file the PI opens in Excel and sends back to
OSP.

## Why it exists

HHS changed its payment-justification requirements for discretionary
awards in October 2026, effective immediately. At the University of
Idaho, OSP's Financial Unit sends each affected PI and DGA the expense
lines for the draw on the Tuesday of every draw week. The PI must return
a compliant justification for each line to `osp-billing@uidaho.edu` by
close of business Wednesday so OSP can submit the draw on Thursday
morning. 19 UI grants were affected at rollout. Each justification
must:

- identify and describe the cost;
- explain how it supports the award's objectives;
- give the timeframe the cost was incurred;
- use plain language;
- exclude confidential, sensitive, or personally identifiable
  information;
- for multiple cost types in a subaccount, summarize each type;
- fit the PMS character limit.

## Topology

| Step | Task | Input | Output |
|---|---|---|---|
| 1. Extraction | `extract-draw-lines` (Prompt) | `workflow_documents` | Minified JSON: every billing-sheet row with cost type, role (never a name), and timeframe resolved |
| 2. Consolidation (output) | `hhs-payment-justification` (Prompt) | `step_input` | Raw JSON array: one object per sheet row, keyed by the sheet's own headers, justification column filled |

## How to run

1. Import `hhs-draw-justification.vandalizer.json` into Vandalizer.
2. Upload the current OSP billing spreadsheet. If you have it, also
   upload the PI's last completed sheet: payroll lines then reuse the
   PI's own sentences for the same account codes, with the dates
   updated.
3. Run, then download the result with **CSV** format (not Word or
   JSON). Open it in Excel and read every justification; the
   Extraction step's output lists any flags (an unrecognized account
   code, a pay date outside the table).
4. Save it as .xlsx if OSP prefers, and email it to
   `osp-billing@uidaho.edu`.

### Why CSV works

Vandalizer's run download, in CSV format, parses a step's JSON string
output and writes a list of objects as real columns, with the object
keys as the header row. The consolidation therefore emits raw JSON
(no code fence or commentary, which would defeat the parse) with the
sheet's own headers as keys. A **Data Export** step would not help: it
only tabulates structured output, and a Prompt step's output is text,
so it would produce a .txt file. Excel may display TransDate as a
number (Excel's date serial) if that is how the sheet was read; the
values themselves are unchanged.

## How the timeframe is set

Payroll lines (Description "HR Payroll …") carry the **pay date** as
TransDate, not the period worked. The extraction prompt holds a lookup
table of UI biweekly pay dates (9/25/2026 through 6/18/2027) and the
pay period each one covers (pay date minus 26 days through pay date
minus 13 days). This comes from one confirmed example: the CB7897
sheet's 10/23/2026 payroll was justified as 9/27/2026–10/10/2026.
**Confirm with OSP or Payroll before relying on it**, and extend the
table before 6/18/2027. Pay dates not in the table are flagged rather
than guessed.

The draw-window dates in the justification column header (for example
"ACTIVITY 10/10-23/2026") are not used as the work period.

## Wording

The language is deliberately general, per the PI's review: every cost
is linked to "the research activities supported by this award", and
the workflow never names the research topic, a journal, or why an item
was bought. Sentence patterns follow the justifications the PI
submitted for the 11/06/2026 draw:

- Payroll: "Payment for salary for project graduate research
  assistants from 10/11/2026 to 10/24/2026 to conduct the research
  activities supported by this award."
- Services: "Payment for services provided by the Laboratory Animal
  Research Facility, as described in the approved budget, for the
  month of September 2026, to support the research activities
  supported by this award."
- Publication: "Payment for publication costs, as described in the
  approved budget, for a paper reporting results of research supported
  by this award."
- Indirect: HHS's own sufficient F&A sentence, word for word.

The PI can add specifics (the journal, what the supplies were for)
before sending the sheet.

## Open questions

- **PMS character limit.** The HHS guidance says justifications must
  fit "the character limit available in PMS" but the limit was not in
  the material we had (the HHS PDF blocks automated download). Line
  justifications run one sentence (roughly 30-50 words); confirm they
  fit once OSP knows the limit.
- **Per line or per subaccount?** OSP's sheet asks for one
  justification per line, so that is what the workflow fills. If OSP
  also wants a combined per-subaccount paragraph for PMS, that would be
  a separate output (v0.1.0 had one).
- **Account-code roles.** E4106 / E4109 / E4135 / E4281 / E4282 role
  mappings were inferred from the CB7897 example. Other personnel codes
  fall back to "project personnel" with a reviewer flag.
- **Who runs it.** OSP already pulls every affected grant's lines each
  Tuesday; running the workflow there and sending PIs a draft to
  approve would shorten the one-day turnaround.

## Status

Experimental. v0.1.0 ran once in Vandalizer on Deborah Stenkamp's
CB7897 sheet for the 10/23/2026 draw: content correct (10 lines,
$8,470.30, 9/27–10/10 pay period), but a Markdown report rather than
the sheet. v0.2.0 ran on the real 11/06/2026 CB7897 sheet (16 lines)
and downloaded as a clean 16 × 15 CSV. The PI reviewed it ("Not bad!
... would lean toward using less specific language") and returned the
sheet she submitted; v0.4.0 adopts her wording and drops the
award-document step. v0.4.0 is not yet run: re-run the 11/06 sheet
(with the 10/23 completed sheet as the prior sheet) and compare
column O with what she submitted.
