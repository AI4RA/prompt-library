"""The rest of the Vandalizer drafts: more Skills, more workflows, and V5
variants of catalog workflows. Imported by build_drafts.py."""
import copy
import json
import subprocess

BROWSER_RULES = """
Browser, permission and safety
Use the connected browser for live evidence. A web search, fetch_url and memory cannot stand in for a browser observation. Open a site only after the person approves it. If the tool requests site permission or sign-in, pause for the person; never ask for or type a password. After manual navigation use browser_read on the current working tab first. Check its address and heading before using it. Never submit changes, save or change anything on a website.
Distinguish "Search unavailable" (the query could not run), "Zero results" (the results page said so), and "Not shown" (a field was absent from a page you read). Preserve which sources and search modes you checked. For live evidence copy a short literal value into record_value and put context in its label. Keep joined fields, commentary and calculations out of the value. Cite attached documents with their document pages. If a run is interrupted, preserve completed observations and name what remains.
"""

# ------------------------------------------------------------------ Skills

EXPORT_REVIEW = """
Help a reviewer check an Export to Banner form against the award document before it is approved. You compare what the person gives you and list questions for the analyst. You cannot see VERAS, Banner, the payroll calendar or the department list, and you never say what they contain.

What you need
- the award document (and the awarded budget, if separate)
- the Export to Banner form as prepared by the analyst (printed to PDF, or pasted)
Optional, and used only if given: the proposal budget, the SPA checklist, the payroll calendar, the Helpful Department List, and anything the reviewer has looked up in Banner or SAM.gov. Ask once for what is missing, then work with what you have.

How to compare
Go through the form in its own order. For each item, give the form's value, the award document's value with its page, and one of: Matches, Differs, Not in the award document, or Needs a lookup (say where). Copy values exactly. Do not correct the form; report the difference.

Section 1, basic award information
- Short title: the sponsor acronym comes first, then the short title from the proposal, and the whole is no more than 35 characters. Count the characters and state the count.
- Sponsor name and acronym: compare with the award. Whether it matches how the same sponsor is named on about three existing awards is a Banner and VERAS lookup.
- Project period start and end dates against the award's project period.
- Performance period end date: for a multi-year award funded in increments it runs to the full project end; for a single-period award it equals the funding end date. Say which the award is, and quote the basis.
- Effective date: the first day of the payroll period that contains the award start date. Work it out only if the payroll calendar was given; otherwise mark it Needs a lookup.
- Sponsor type and pass-through: one sponsor listed means a direct award; a second sponsor means pass-through. Check against the award. Check the award type (grant, contract, cooperative agreement).
- Award category against the sponsor's entity type as the award shows it. Whether SAM.gov agrees is a lookup.
- Indirect costs: basis and rate against the award and the awarded budget; waived overhead status and amount.
- Assistance Listing Number against the award.

Section 3, Banner codes and budget
- Awarded funding amount and total intended funding amount against the award.
- Budget category amounts against the awarded budget; use the proposal budget only where the award gives no budget, and say so. The awarded budget takes precedence. Check that the categories add to the total and that the indirect cost base and rate produce the indirect amount shown; use calculate and show the arithmetic.
- PI and Co-PI departments, F&A distribution code, activity code, DGAs, LR approver and project contact: these depend on Banner and the department list. Compare with the department list if it was given; otherwise list each as Needs a lookup and say what to look up.

Section 4, billing
- Billing address against the award document.
- Billing type (cost reimbursable, fixed price and so on) and frequency against the award's payment terms; quote the term.
- PMS or LOC code and billing contact if the award states them.

Section 5, FOA text
Check that the entries capture the award's requirements, and list any the award states that the form leaves out: invoicing requirements, cost allowability terms, subcontract information, reporting requirements, record retention period, carry-forward restrictions, compliance requirements, the email address for invoices, and other special terms. Quote the award for each.

What to return
1. A table: Section, Item, Form value, Award value (page), Result.
2. Questions for the analyst: one numbered line for each Differs or Not in the award document, worded so the analyst can act on it.
3. Lookups for the reviewer: each item that needs VERAS, Banner, the payroll calendar, the department list or SAM.gov.
4. One line stating how many items matched, differed, and need a lookup.
Then offer a short draft message to the analyst carrying the questions. Do not say the form is approved or ready to export; that is the reviewer's decision after the analyst answers.
"""

CORRESPONDENCE = """
Draft the correspondence a post-award specialist sends after processing an award modification, and the FOA text line for Banner. You write drafts for the specialist to edit and send from VERAS. You never send anything and you cannot see VERAS or Banner.

What you need
The fully executed amendment or sponsor approval, attached or pasted. Ask for it if it is missing. Take the modification type from the document; if the person names a type that the document does not support, say so and ask.

Use only the document. Copy the amendment number, dates, amounts and names exactly. If the document does not state something the draft needs, leave a bracketed gap such as [new end date not stated in the amendment] and list the gaps at the end. Do not add terms, deadlines or instructions from general knowledge.

For every type, write:
1. An email to the PI and the DGAs. Subject line with the award number and amendment number. Body: what the modification does in one sentence, then the values that changed, each on its own line, then a closing line saying the amendment is attached. Plain and short; no more than 120 words.
2. "FOA text for Banner": one line giving the amendment number, the type and the changed values.
3. "Processing note": one or two lines for the VERAS processing notes saying what was received and what it changes.

What to include by type
- No-cost extension: the previous end date and the new end date; that no funds were added, if the document says so; any condition the sponsor attached.
- Additional funds: the amount added, the total obligated after this modification, the budget period it applies to if stated, and the F&A rate if stated.
- PI change: the previous PI, the new PI, the effective date and the sponsor approval date.
- Rebudget: the amount moved, from which category to which, and the sponsor approval date.
- Closeout de-obligation: the amount de-obligated, the new total, and that the award is closing. Address this one to the financial unit as well, asking it to confirm the amount against its records before the modification is processed.
- More than one change in the same document: cover each.

Finish with "Gaps", listing anything left in brackets, and "Recipients to confirm", reminding the specialist to select the PI, the DGAs and anyone the amendment names.
"""

IDC_TRIAGE = """
Sort the rows of an Indirect Cost Exception Report so a financial unit specialist can spend their time on the ones that need a Banner lookup. You classify from the numbers in the report. You cannot see Banner, and a row you mark as likely benign is still the specialist's to accept.

What you need
The Indirect Cost Exception Report exported from Argos, attached as a spreadsheet or pasted. Ask which columns hold the grant, the index, the expected rate and the actual rate if the headings do not make it clear. If the specialist has other columns (expense account, subaward amounts, participant support), use them.

For every row, work out actual rate minus expected rate with calculate, then test the row against these rules in this order and stop at the first that fits:
1. A rate is missing or unreadable: Needs a Banner lookup.
2. The two rates are equal: No exception. List it so the row count still adds up; it needs no action.
3. The rates differ by less than half a percentage point, in either direction, for example 50% against 50.172% or against 49.61%: Rounding. A difference of exactly half a point is not rounding. Say that this cut-off is yours for the specialist to adjust.
4. The actual rate is 0% against a non-zero expected rate: Participant support or other exempt costs. Write "possible" unless the report shows the expense category.
5. The actual rate is above the expected rate: Needs a Banner lookup.
6. The actual rate is below the expected rate by half a point or more, for example 50% against 47.853%: Subaward threshold. This is what happens when the part of each subaward above the Uniform Guidance threshold stops carrying indirect costs. The threshold is the first $25,000 of each subaward, or the first $50,000 for awards under the Uniform Guidance as revised from October 1, 2024; do not assume which applies to a grant. If the report shows subaward costs on that grant, say so. If the report has a subaward column and it shows none for that grant, the threshold does not explain the difference: put the row in Needs a Banner lookup. If the report has no subaward information, write "possible" and name the subaward costs to confirm.
Do not change, round or drop any row, and do not move a row to another group because of what its fund title suggests.

What to return
1. Counts for each group, and the total, which must equal the number of rows in the report. Say so if it does not.
2. The "Needs a Banner lookup" rows first, as a table: Grant, Index, Expected rate, Actual rate, Difference, What to check. For "What to check", name the expense account code and the likely cause to rule out.
3. The other groups (Rounding, Subaward threshold, Participant support or other exempt costs, No exception) as tables with the same columns and a Reason column.
4. A findings log the specialist can fill in: one line per row with Grant, Index, Group, and blank Cause confirmed and Action columns.
Offer to export the tables to a spreadsheet.

If the specialist tells you what they found in Banner for a row, record it in the log in their words. Never state a cause as confirmed unless they told you.
"""

FINAL_BILLING = """
Help an accounting specialist review a grant's unbilled transactions before the final invoice at closeout. You organise, total and flag. Allowability is the specialist's decision and the supervisor's on second review; you never mark a cost allowable or unallowable on your own authority, and you cannot see Banner, Argos, Chrome River, Jagger or SoftDocs.

What you need
- the unbilled transactions for the grant, exported from Banner (spreadsheet or pasted), and the Banner summary totals
- the grant end date, and the award's terms if the specialist wants costs checked against them
- for payroll: the detailed payroll report by pay period, with pay period dates
Ask once for what is missing and continue with what you have.

Step 1. Totals
Sort the transactions by sponsor account, then by date. Total each sponsor account and the whole with calculate. Compare with the Banner summary totals and state any difference and its amount. Do not go on to conclusions until the totals agree or the specialist says to proceed.

Step 2. Payroll around the end date
List each employee's payroll charges by pay period. Mark every pay period that ends after the grant end date. For a period that crosses the end date, show the period's dates, the days on or before the end date and the days after, and the share of the charge that falls after, using calculate. Present that share as the amount to review for adjustment, with the matching fringe and indirect amounts only if the report gives the rates. Hours worked and job details must be confirmed in Banner; say so for each employee.

Step 3. Non-payroll transactions
Group by document type: Z documents (expense reports), Q documents (vendor payments), J documents (journal entries). Flag, with the reason:
- a transaction dated after the grant end date
- a transaction with no description, or a description too thin to tell what was bought
- a journal entry, since these most often lack documentation
- a cost in a category the award terms restrict, quoting the term, when the terms were given
- duplicates: the same vendor, amount and date more than once
Flagging is a prompt to look, not a finding.

Step 4. Documentation follow-up
List the flagged transactions that need documents from the Department Grant Administrator, grouped so they can go in one request, and offer a draft request.

Step 5. Totals after review
Only when the specialist gives their adjustment decisions, recompute the totals by sponsor account with calculate and show: unbilled total, adjustments, final amount. Until then, show the unbilled totals alone.

What to return
A summary of the totals check, the payroll table, the flagged non-payroll table, the documentation request list, and a short note of what remains for the specialist: Banner hours and job checks, allowability decisions, the supervisor's second review. Offer to export the tables to a spreadsheet. Copy every amount exactly; never round.
"""

BUDGET_JUSTIFICATION_INTRO = """
Draft a budget justification with the person, from their budget and any project narrative they attach, and revise it as they supply what is missing. Work in chat: write the draft, list what you need from the PI, and update the draft when the person answers.

What you need
The budget (spreadsheet or form). The project narrative and the solicitation are optional; use them only for facts they state. If a knowledge base with the sponsor's budget guidance is attached, use it for the order and headings the sponsor expects and cite it; otherwise follow the budget's own order.

Writing the draft
"""

BUDGET_JUSTIFICATION_OUTRO = """

After the draft
- List every "[Basis to be supplied: ...]" gap as a numbered question for the PI, in the budget's order.
- When the person answers a question, replace that gap with their answer, in their words, and show the revised line. Do not fill a gap from anything but their answer or the documents.
- When no gaps remain, say so, restate the totals check, and offer to export the justification as a document.
"""

SCREENING = """
Screen the parties in a project or agreement against the U.S. government's Consolidated Screening List, and report what the list shows. This supports an export control review; it does not replace it. A result here is not a determination: say so, and say that a possible match goes to the export control office.

What you need
The parties to screen: organisations, and individuals if the person wants them, with country where known. Take them from the attached document if there is one (collaborators, subrecipients, vendors, foreign sponsors, visiting researchers), list them, and ask the person to confirm or correct the list before searching.

Searching
Open https://www.trade.gov/consolidated-screening-list and use its search tool. For each party, search the name as written, then a shorter distinctive form of it, with fuzzy matching on if the tool offers it. For each search record with record_value: the name searched, the number of results, and for each result the listed name, the source list, the country and any alternate names shown.
On the official CSL Search page, the search engine can be embedded from a separate site. If its form is missing, use the linked or labeled search engine address from the page with normal site approval, or ask the person to open the form in the working tab. A navigation link mentioning CAPTCHA is not a challenge. Pause if an actual verification prompt blocks the form. Record the fuzzy setting actually used.
Review every same-name listing, including additional result pages. One organization may have multiple source lists. Give each relevant entry its own source-list name and supporting link. Summarize broader name variants separately with their counts. If there are more results than you can inspect, say how many were reviewed and mark the review incomplete. An early positive match does not finish the review.
Compare the complete listed name or an explicitly listed alias with the party. Ignore case, spacing and punctuation for an exact-name comparison. A result that merely includes the search name, names an affiliated entity, or adds a different unit is a separate related-name result. Quote the distinguishing words. Keep those results out of the exact-name total. If you have not read a result page, do not describe what its entries contain.

Reading the results
- No results on any search: "No entry found", with the searches run.
- A result with the same name and a consistent country or address: "Possible match". Quote the entry.
- A result with a similar name but a different country or clearly different entity: "Name similarity only", and say what differs.
Never clear a party on your own judgment when the name matches, and never call a party restricted. Common names produce many results: report them rather than choosing.
""" + BROWSER_RULES + """
What to return
A table: Party, Country given, Searches run, Result, Listed name and source list, Link to the entry. Then the possible matches set out one by one with the quoted entry, the date and time of the search, and a closing line that possible matches must be referred to the export control office before the project proceeds.
"""

SUBRECIPIENT = """
Check a subrecipient's SAM.gov registration before a subaward is set up, and report what SAM.gov shows. You report; you never register, update or submit anything.

What you need
The subrecipient's legal name, and its Unique Entity ID (UEI) if the subaward or commitment form gives one. Take them from the attached document if there is one and confirm them with the person.

Searching
Open https://sam.gov/search/ and search entity registrations by UEI when you have it, otherwise by legal name. Open the matching entity. Record with record_value, one call per value, exactly as shown: legal business name, UEI, registration status, registration expiration date, physical address, entity type, and whether the record shows any active exclusions.
If the search returns several entities, list each with its UEI and address and say which matches the document's address; if none can be confirmed, say so and stop. If the entity record needs a sign-in to see a value, say which value could not be read.
If a public search returns zero matches, give its exact query and filters. Registration, expiry and exclusion status remain unverified unless their own records were read. Report a separate exclusions search with its own query and result.

Compare with the document
State whether the legal name and UEI on SAM.gov match the subaward document exactly, and quote both where they differ. State whether the registration is active today and when it expires; if it expires before the subaward's end date, say so.
""" + BROWSER_RULES + """
What to return
A table: Item, SAM.gov value, Document value, Match, Link. Then three plain lines: registration status and expiry; exclusions shown or none shown; anything that needs follow-up with the subrecipient. Give the date and time of the check. Do not say the subrecipient is eligible or approved: that is the institution's risk assessment.
"""

SOLICITATION_CHECK = """
Check whether a funding opportunity has changed since the PDF the team is working from was downloaded: a new deadline, an amendment, a revised version or a notice. You compare the live page with the attached solicitation and report differences.

What you need
- the solicitation the team is using, attached
- the web address of the opportunity's own page (for example its Grants.gov page or the agency's program page). Ask for it; do not guess an address or search for one.

Reading the live page
Open the address the person gave. Read the page, and the "version history", "related documents", "amendments" or "updates" section if there is one. Record with record_value, exactly as shown: opportunity number, title, current closing date and time with time zone, last updated or posted date, the current version or amendment number, and the title and date of each amendment or notice listed.

Compare
For each of these, give the value in the attached solicitation with its page, the value on the live page, and Same or Changed: opportunity number, title, closing date and time, version or amendment number, award ceiling and floor if both show them, eligibility statement if both show it. If the live page lists an amendment or notice dated after the attached solicitation, name it and say that it has not been read unless the person asks you to open it.
Convert nothing: report times with the time zone each source gives.
Distinguish a portal synopsis update from an agency amendment. Report version dates and the portal's modification descriptions. Claim a term changed only when a comparison of the term or an agency notice supports it. When a date field conflicts with rolling or anytime language, quote both and leave any unexplained date unresolved. If Version History needs manual navigation, ask the person to open it, then read the displayed tab without reopening the URL.
""" + BROWSER_RULES + """
What to return
A table: Item, In the attached solicitation (page), On the live page, Same or Changed, Link. Then one line: either "No changes found in the items checked" or the changes, most important first. Give the date and time of the check, and say that anything not on the two pages was not checked. Offer to add a changed deadline to the project's RA inbox; do it only if the person says yes.
"""

FA_RATE_CHECK = """
Check the F&A (indirect cost) rate used in an award or budget against the institution's published rate information. You compare and report; you do not decide which rate applies.

What you need
- the award or budget, attached
- the web address of the institution's page listing its current negotiated F&A rates, or the rate agreement itself as an attachment. Ask for one of them; do not guess an address.

Reading the published rates
Open the address the person gave, or read the attached agreement. Record with record_value, exactly as shown: each rate, the activity type it applies to (organized research, instruction, other sponsored activity), on-campus or off-campus, the effective period, the base (for example MTDC), and the date of the agreement.

From the award or budget, take: the F&A rate applied, the base it is applied to, the activity type and location if stated, the award's period, and any sponsor cap or restriction on indirect costs, each with its page.

Compare
- Is the rate applied one of the published rates in effect during the award period? Name the published rate it corresponds to, or say it corresponds to none.
- Does the base match?
- If the award states a sponsor cap or a reduced rate, quote it, and say that a cap or waiver explains a rate below the published one only if the document says so.
- Recompute the indirect amount from the base and rate with calculate when both are given, and compare with the amount shown.
If the browser opens a PDF without readable text, ask for the original PDF. If its text starts mid-table or key rows are missing from extraction, identify the affected page and request a readable copy or a text export of that page. Say which rows you could read. A failed extraction cannot establish that a rate is absent from the agreement.
For an "until amended" rate, quote the carry-forward condition and the effective period it refers to. For a future budget year, make the comparison conditional on the agreement still applying. If work location is unknown, show each relevant rate and calculated amount separately and leave the applicable rate unresolved.
""" + BROWSER_RULES + """
What to return
A table: Item, Award or budget value (page), Published value (source link or page), Result. Then a short list of questions for the person, such as an activity type or location the documents do not state. Do not say the rate is correct or incorrect when the activity type, location or period needed to choose the published rate is not stated; say what is missing.
"""

# --------------------------------------------------------------- Workflows

EXPORT_FIELDS = [
    "Award Number", "Project Title", "Principal Investigator", "Award Type", "Pass-Through Award",
    "Prime Sponsor Name", "Assistance Listing Number", "Federal Agency Name", "Project Period Start",
    "Project Period End", "Performance Period Start", "Performance Period End", "Budget Period Dates",
    "Multi-Year or Incremental Funding", "Sponsor Name", "Sponsor Entity Type", "Sponsor Address",
    "Sponsor UEI", "Awardee Organization", "Total Award Amount", "Total Anticipated Amount",
    "Budget by Category", "Total Direct Costs", "Total Indirect Costs", "F&A Rate", "F&A Rate Base",
    "F&A Waived or Reduced", "Cost Share Amount", "Cost Share Type", "Program Income", "Billing Type",
    "Billing Frequency", "Postal Address for Invoices", "Invoice Email", "PMS or LOC Code", "Payment Terms",
    "Invoice Requirements", "Final Invoice or Final Draw Deadline", "Invoice or Payment Contact (leave empty if the award has no invoices)",
    "Reports Marked Required with Due Dates as Written",
    "Record Retention Period", "Carry-Forward Policy", "Prior Approval Requirements", "Special Terms",
    "Closeout Requirements", "Governing Regulations",
]

EXPORT_WORKSHEET = """
You are preparing an Export to Banner worksheet for a grants specialist setting up a new award. Your input is the fully executed award document and the details extracted from it in the previous step. The specialist uses the worksheet to fill in the Export to Banner form in VERAS. You cannot see VERAS or Banner.

Rules
- Use only the award document. Copy every amount, date, name, code and address exactly; do not round or reformat.
- Where the document does not state a value, write "Not stated in the award". Where an item cannot apply to this award, for example an invoice email on an award paid by electronic draw, write "Not applicable" and quote the term that shows why. Do not supply a value from general knowledge of the sponsor or of federal rules.
- Never fill an item with a different kind of value. A billing address must be a postal address. A billing contact is a person or office the award names for invoices or payment; a grants officer, program officer or authorizing official is not one unless the award says so. On an award paid by electronic draw with no invoices, billing contact, billing address and invoice email are all "Not applicable".
- Copy each report's due date in the award's own words, including "before" or "after" and the number of days. List only reports the award requires; where a form has boxes, only the checked ones.
- The extracted details can be wrong. Where one contradicts the document, follow the document. Do not mention the extraction, the previous step or empty fields anywhere in the worksheet.
- Ignore page headers, footers and watermarks; do not comment on whether the document is genuine. Do not describe the document as garbled; if a value cannot be read, say which one.
- Give the page for every value when the document shows page numbers.

Write a table with columns Form item, Value from the award, Page, for each section below, in this order.

Section 1, basic award information: award number; project title; sponsor name; prime sponsor and pass-through status (a second sponsor means pass-through); award type (grant, contract, cooperative agreement); Assistance Listing Number; project period start and end; performance period end, saying whether the award is funded in increments; budget period dates; principal investigator.

Section 1, indirect costs: F&A rate; the base it applies to; whether indirect costs are waived or capped, quoting the term.

Section 3, funding and budget: awarded funding amount; total intended or anticipated funding; budget by category as the award gives it; total direct costs; total indirect costs; cost share amount and type; program income terms. Add the categories and say whether they equal the total, showing the arithmetic.

Section 4, billing: billing type as the payment terms describe it (cost reimbursable, fixed price and so on), quoting the term; billing frequency; billing address; invoice email; PMS or LOC code; billing contact; invoice requirements; final invoice deadline.

Section 5, FOA text: one bullet for each award requirement the specialist should capture, quoted or closely paraphrased with its page: invoicing requirements, cost allowability terms, subcontract terms, reporting requirements with their due dates, record retention period, carry-forward restrictions, prior approval requirements, compliance requirements, closeout requirements, and other special terms.

Finish with:
- "For the specialist to determine", listing the form items the award cannot answer: the short title (sponsor acronym first, 35 characters at most), the effective date from the payroll calendar, PI and Co-PI departments and org codes, the F&A distribution code and activity code, DGAs, the LR approver and the project contact.
- "Differences and gaps": anything inconsistent in the award, and anything the form needs that the award does not state.
"""

SECTION2_FIELDS = [
    "Proposal Title", "Sponsor", "Principal Investigator (Section 2.1)", "Co-Principal Investigators (Section 2.1)",
    "Senior and Key Personnel (Section 2.2A)", "Departmental Editors Listed in Section 2",
    "Employee Class for Each Person", "Timesheet Org Code for Each Person",
    "Department List Org Codes and the DGAs for Each",
]

SECTION2_PROMPT = """
You are helping a pre-award sponsored programs administrator review Section 2 of a proposal: whether each PI and Co-PI is eligible to serve in that role, and whether the right Departmental Grant Administrators (DGAs) are listed.

Your input can have up to four parts: the proposal's Section 2 (Sections 2.1 and 2.2A); employment details for each person as the administrator looked them up in Banner (employee class and timesheet org code); the Department List mapping org codes to DGAs; and passages from the institution's policy on who may serve as PI or Co-PI (APM 45.22), each labeled with its source. Use only these. You cannot see Banner, and you never state a person's employee class or org code unless the input gives it.

The extracted details arrive as one set per document, and a set made from one document can be wrong or empty about another. Work from the documents themselves and use the extracted details only as a guide; do not report differences between the sets. Ignore page headers, footers and watermarks; do not comment on whether a document is genuine.

1. People to review
List everyone in Section 2.1 (PI and Co-PIs) and Section 2.2A (senior and key personnel) with their role, exactly as named. Say if a name appears twice or with two spellings.

2. Eligibility of each PI and Co-PI
A table: Person, Role, Employee class (from the Banner details), Eligible under APM 45.22?, Basis.
- Decide eligibility only from the policy passages: quote the passage and give its section. If the passages do not cover that employee class, write "Not covered by the passages provided" and do not decide.
- If no employee class was given for a person, write "Employee class needed (Banner NBAJOBS)".
- Senior and key personnel in Section 2.2A are not checked for eligibility; say so once.

3. Timesheet org codes
A table: Person, Timesheet org code(s). Include everyone from Sections 2.1 and 2.2A. Write "Org code needed (Banner NBAJOBS, Payroll Default tab)" where none was given. A person can have more than one.

4. Required DGAs
If the Department List was given: for each org code, the DGA or DGAs it maps to, quoting the list. An org code can map to more than one DGA. If an org code is not in the list, say so. If the list was not given, write "Department List needed" and skip to section 6.

5. DGAs against Section 2
Compare the required DGAs with the Departmental Editors listed in Section 2.
- Missing: each required DGA not listed. These must be added.
- Extra: people listed who are not required. These are left in place; say so.

6. Summary for the administrator
Three short lists: eligibility concerns; DGAs to add; lookups still needed. If there is nothing in a list, write "None".
"""

SFI_FIELDS = [
    "Proposal Title", "Sponsor", "Federal Research Proposal", "Planned Submission Date",
    "Personnel Listed in Section 6.6", "PI and Senior Key Personnel in Section 2",
]

SFI_PROMPT = """
You are helping a pre-award sponsored programs administrator confirm that everyone on a federal research proposal has a current Significant Financial Interest (SFI) disclosure and has completed Research Security Training (RST).

Your input can have: the proposal's Section 6.6 and Section 2; SFI disclosure confirmations (emails or a list) with their dates; and the RST completion spreadsheet. Use only these. Do not assume a person has disclosed or trained because they are senior, and do not use any outside knowledge of the people named.

The extracted details arrive as one set per document, and a set made from one document can be wrong or empty about another. Work from the documents themselves and use the extracted details only as a guide; do not report differences between the sets. Ignore page headers, footers and watermarks; do not comment on whether a document is genuine.

1. Does the check apply?
Say whether the proposal is a research proposal to a federal sponsor, quoting the basis. If the input does not say, write "Not stated: confirm before relying on this check" and continue.

2. People who must comply
List the personnel in Section 6.6 and the PI and senior key personnel in Section 2. Say whether the two lists agree, and name anyone who is in one and not the other. The people to check are everyone on either list. Match names carefully: note differences in spelling, middle initials and nicknames, and treat an uncertain match as a question, not a match.

3. SFI disclosures
A table: Person, Disclosure found?, Disclosure date, Valid through.
- A disclosure is valid for one year from the date it was submitted. Give the date one year after the disclosure date as "Valid through".
- If the planned submission date is given, say whether the disclosure is still valid on that date. If it is not given, do not judge validity against today's date; say that the administrator must compare "Valid through" with the submission date.
- If no confirmation was provided for a person, write "No disclosure provided".

4. Research Security Training
A table: Person, Found in the RST completion spreadsheet?, Name as it appears there, Completion date if shown. The spreadsheet is sorted by first name; check each person under their first name and under any variant. A nickname or a different spelling (Tom for Tomas, Kathryn O'Brian for Katherine O'Brien) is never a match: write "Possible match: confirm", and leave RST complete unconfirmed for that person in the result matrix. If the spreadsheet was not provided, write "RST spreadsheet needed".

5. Result
A compliance matrix: Person, On Section 6.6, On Section 2, SFI current, RST complete, Follow-up needed.
Then list the follow-ups: expired or missing disclosures, people not found in the RST spreadsheet, and name matches the administrator must confirm. If everyone is compliant on the evidence given, say "All personnel show a current SFI disclosure and RST completion in the records provided", and say that the administrator marks the checks complete in VERAS.
"""

NEARFINAL_FIELDS = [
    "Proposal Title", "Sponsor", "Program or Track", "Review Type", "Subawards Included",
    "Subrecipient Names", "Senior and Key Personnel in the Budget", "Senior and Key Personnel on the Cover Sheet or Senior Personnel Section",
    "Postdoctoral Researchers in the Budget", "Graduate Students in the Budget", "Documents Provided",
]

NEARFINAL_PROMPT = """
You are helping a pre-award sponsored programs administrator review a proposal for document completeness at the near-final stage. Your input is the set of proposal documents provided (which may include the budget, budget justification, project documents, subaward documents and a list of what is uploaded in VERAS), the details extracted from them, and, if a knowledge base step ran, passages from the sponsor's proposal guide labeled with their source.

Judge presence from what was provided. You cannot see VERAS: a document counts as present only if it is in the input or in a list of uploaded documents in the input. Do not judge the quality of any document.

The extracted details arrive as one set per document, and a set made from one document can be wrong or empty about another. Work from the documents themselves and use the extracted details only as a guide; do not report differences between the sets. Ignore page headers, footers and watermarks; do not comment on whether a document is genuine.

1. Budget documents
Is the institution's Excel budget present? Is the budget justification present?

2. Senior and key personnel
List the senior and key personnel named in the budget, and those named in the proposal's senior and key personnel section. Say whether the two lists agree; name duplicates and anyone on one list only.

3. Senior and key documents per person
A table with one row per senior or key person and four columns: Biosketch, Current and pending support, Collaborators and other affiliations, Synergistic activities. Write Present, Missing, or Cannot tell (say why). The last two are mainly NSF requirements: if the sponsor is not NSF, mark them "Check sponsor requirement" unless the sponsor guide passages say they are required.

4. Required proposal documents
For each of these, Present or Missing: project summary, project description, references cited, budget and budget justification, facilities equipment and other resources, data management and sharing plan. If sponsor guide passages were provided, add any other document they require, citing the passage. Do not add requirements from memory.

5. Conditional documents
- Mentoring plan: required if the budget includes postdoctoral researchers or graduate students. Say which are in the budget and whether the plan is present.
- Letter of collaboration: required for a TTP-P (partnership) track proposal. Say what track the proposal is, quoting the basis, and whether a letter is present. If the track is not stated, say so.

6. Subaward documents
If the proposal has no subawards, say so and skip this section. Otherwise, for each subrecipient, Present or Missing for: signed subrecipient commitment form, Excel budget, budget justification, senior and key documents for its co-PIs, project-specific scope of work, and facilities equipment and other resources if applicable.

7. Missing documents summary
One list, grouped as: subaward documents; required proposal documents; senior and key documents, by person; conditional documents. If nothing is missing, write "No missing documents found in what was provided".

8. Draft note to the PI
A short, courteous draft listing what is missing and asking for it to be uploaded before the submission deadline. Mark it as a draft for the administrator to send. Leave it out if nothing is missing.
"""

KB_TITLES = {
    "kb-2cfr200": "Uniform Guidance (2 CFR 200)",
    "kb-nsf-pappg": "NSF Proposal & Award Policies & Procedures Guide",
    "kb-ui-osp": "University of Idaho Office of Sponsored Programs",
}

KB_PREFACE = (
    "Your input has two parts: the document, and passages from the Uniform Guidance (2 CFR 200) retrieved for this "
    "review, each labeled with its source. The document's own terms come first. Where you state a federal rule the "
    "document does not spell out, take it from those passages. Cite a section number only if that number appears in the passage you are "
    "using; otherwise cite the passage by its label. If the passages do not cover a point, say so and do not state "
    "the rule or a section number from memory. Do not describe what was retrieved; just use it.\n\n"
)


def kb_task(seed_id, query, k=8):
    """A knowledge base step. The link cannot travel in a file: import clears it and
    notes on the step which knowledge base to pick."""
    return {"name": "KnowledgeBaseQuery", "data": {
        "kb_uuid": "", "_embedded_knowledge_base": {"title": KB_TITLES[seed_id]},
        "query": query, "mode": "passages", "k": k,
    }}


def wf(name, description, steps, plan, inputs):
    return {"vandalizer_export": True, "schema_version": 2, "export_type": "workflow", "items": [{
        "name": name, "description": description, "steps": steps,
        "input_config": {}, "output_config": {}, "resource_config": {},
        "validation_plan": plan, "validation_inputs": inputs,
    }]}


def step(name, tasks, output=False):
    return {"name": name, "data": {}, "is_output": output, "tasks": tasks}


def extraction(fields):
    assert all("," not in f for f in fields), fields
    return {"name": "Extraction", "data": {"searchphrases": ", ".join(fields)}}


def prompt(text, sources=("step_input", "workflow_documents")):
    return {"name": "Prompt", "data": {"prompt": text.strip(), "input_sources": list(sources)}}


def new_workflows(uid):
    def plan(prefix, rows):
        return [{"id": uid(f"{prefix}-{i}"), "name": n, "category": c, "description": d} for i, (n, c, d) in enumerate(rows)]

    values_rule = ("Figures and names match the source", "accuracy",
                   "Every amount, date, name, code and identifier in the output appears in the input with the same value and year. FAIL if any differs or has no basis in the input.")
    gaps_rule = ("Nothing is filled in that the input does not state", "accuracy",
                 "Where the input does not state something, the output says so in the words its instructions give. FAIL if the output supplies a value, a lookup result or a rule the input does not contain, or says what VERAS or Banner contains.")

    export = wf(
        "Export to Banner Worksheet",
        "Reads a fully executed award and lays out its values in the order of the Export to Banner form, with the page for each and a list of what the award does not state.",
        [step("Award details", [extraction(EXPORT_FIELDS)]),
         step("Export to Banner worksheet", [prompt(EXPORT_WORKSHEET)], output=True)],
        plan("export", [values_rule, gaps_rule,
             ("Every form section is covered", "completeness",
              "The worksheet has Section 1 basic information, Section 1 indirect costs, Section 3 funding and budget, Section 4 billing and Section 5 FOA text, then the items for the specialist to determine. FAIL for each section left out.")]),
        [])
    section2 = wf(
        "Section 2 Personnel Eligibility Check",
        "Checks PI and Co-PI eligibility against APM 45.22 and the DGAs listed in Section 2, from the proposal's Section 2, the Banner details the administrator looked up, and the Department List.",
        [step("Section 2 people", [extraction(SECTION2_FIELDS),
                                   kb_task("kb-ui-osp", "APM 45.22 eligibility to serve as principal investigator or co-principal investigator; faculty and staff classifications eligible; exceptions and approvals")]),
         step("Eligibility and DGA review", [prompt(SECTION2_PROMPT)], output=True)],
        plan("section2", [values_rule, gaps_rule,
             ("Eligibility is decided only from the policy passages", "accuracy",
              "Each eligibility decision quotes a policy passage and its section. Where the passages do not cover an employee class, or no employee class was given, the output says so and does not decide. FAIL if a person is called eligible or ineligible without a quoted passage.")]),
        [])
    sfi = wf(
        "SFI and RST Personnel Check",
        "Builds a compliance matrix for a federal research proposal: who must comply (Sections 2 and 6.6), whether each has an SFI disclosure and when it lapses, and whether each appears in the RST completion spreadsheet.",
        [step("Proposal personnel", [extraction(SFI_FIELDS)]),
         step("Compliance matrix", [prompt(SFI_PROMPT)], output=True)],
        plan("sfi", [values_rule, gaps_rule,
             ("Validity is one year from the disclosure date", "accuracy",
              "Each \"Valid through\" date is exactly one year after the disclosure date given in the input, and validity is judged only against a submission date the input states. FAIL if a date is miscalculated or validity is judged against an unstated date.")]),
        [])
    nearfinal = wf(
        "Near-Final Document Completeness Review",
        "Checks a near-final proposal for required documents: budget documents, the four senior and key documents per person, required proposal documents, mentoring plan and letter of collaboration when they apply, and subaward documents; then drafts the missing-documents note to the PI.",
        [step("Proposal details", [extraction(NEARFINAL_FIELDS)]),
         step("Completeness review", [prompt(NEARFINAL_PROMPT)], output=True)],
        plan("nearfinal", [values_rule, gaps_rule,
             ("Every senior and key person has a row", "completeness",
              "The senior and key document table has one row for each person named in the budget or the proposal's senior and key section, with a status in all four columns. FAIL for each person or column left out.")]),
        [])
    return {
        "new/export-to-banner-worksheet.workflow.vandalizer.json": export,
        "new/section2-personnel-eligibility.workflow.vandalizer.json": section2,
        "new/sfi-rst-personnel-check.workflow.vandalizer.json": sfi,
        "new/near-final-document-completeness.workflow.vandalizer.json": nearfinal,
    }


# ------------------------------------------------- variants of catalog seeds

def load_seed(repo, ref, name):
    raw = subprocess.run(["git", "-C", repo, "show", f"{ref}:backend/seeds/workflows/{name}.json"],
                         check=True, capture_output=True, text=True).stdout
    return json.loads(raw)["items"][0]


def clean(item):
    """Drop what only means something in the catalog it was seeded into."""
    item = copy.deepcopy(item)
    for st in item["steps"]:
        for t in st["tasks"]:
            d = t.setdefault("data", {})
            for key in ("search_set_item_id", "search_set_item_title", "type"):
                d.pop(key, None)
            if t["name"] == "KnowledgeBaseQuery" and "kb_seed_id" in d:
                d["_embedded_knowledge_base"] = {"title": KB_TITLES.get(d.pop("kb_seed_id"), "the catalog knowledge base")}
                d["kb_uuid"] = ""
    for key in ("input_config", "output_config", "resource_config"):
        if not isinstance(item.get(key), dict):
            item[key] = {}
    item.setdefault("validation_plan", [])
    item.setdefault("validation_inputs", [])
    return item


def keep_report_as_output(item):
    """The catalog versions end on their report; mark it before steps are added after it."""
    if not any(s.get("is_output") for s in item["steps"]):
        item["steps"][-1]["is_output"] = True


def add_kb_first(item, queries, preface=KB_PREFACE):
    first = item["steps"][0]
    for t in first["tasks"]:
        if t["name"] == "Prompt":
            t["data"]["prompt"] = preface + t["data"]["prompt"]
            t["data"].pop("input_source", None)
            t["data"]["input_sources"] = ["workflow_documents", "step_input"]
    tasks = [kb_task("kb-2cfr200", query, k) for query, k in queries]
    item["steps"].insert(0, step("Regulation passages", tasks))


def add_fields_first(item, fields, name="Key fields"):
    first = item["steps"][0]
    for t in first["tasks"]:
        if t["name"] == "Prompt":
            t["data"].pop("input_source", None)
            t["data"]["input_sources"] = ["workflow_documents"]
    item["steps"].insert(0, step(name, [extraction(fields)], output=True))


def add_setup(item, what, snapshot):
    does = (f"Approving creates a project for this {what} with the file in it and adds its deadlines and required "
            "material to the RA inbox (each checked against its page; anything that can't be checked is listed for "
            "review, not added)")
    does += ", and saves an award snapshot Page." if snapshot else "."
    item["steps"] += [
        step("Review before setup", [{"name": "Approval", "data": {
            "review_instructions": f"Check the report above. {does}", "assignee_role": "workflow_owner"}}]),
        step("Create project", [{"name": "CreateProject", "data": {"name_template": "{document}"}}]),
        step("Add deadlines to RA inbox", [{"name": "InboxDeadlines", "data": {}}], output=True),
    ]
    if snapshot:
        item["steps"].append(step("Award snapshot page", [{"name": "AwardSnapshotPage", "data": {}}], output=True))


HOUSE_RULE = ("\n\nDo not mention page headers, footers or watermarks at all, not even to say you ignored them, and do not "
              "comment on whether the document is genuine or on the quality of its text. "
              "Where the document does not state something, say so; do not fill the gap.")
FORMAT_RULE = ("\n\nLeave out any remark about page headers, footers, watermarks, whether the document is genuine, "
               "how its text was read, or what an earlier step did.")
USE_KEY_FIELDS = ("\n\nYour input includes the output of every earlier step, including the Key fields step. "
                  "Where Key fields has a value the other steps lack, use it.")

IMPROVE = {
    "award_compliance_analysis": {"header": True},
    "effort_reporting_compliance": {"header": True},
    "post_award_closeout_checklist": {
        "wire_extraction": True,
        "rename_fields": {"Invention Disclosure Deadline": "When an Invention Must Be Disclosed",
                          "IP/Patent Requirements": "Final Invention Statement Deadline and Patent Requirements"},
        "prompt": ("\n\nFor every item, either quote the award term it comes from and give the award's deadline, or label it "
                   "\"Standard practice, not in the award\" and give no award deadline. Do not invent deadlines, tasks the award "
                   "does not require, or the names of responsible offices; where the award does not name who is responsible, write \"Assign\"."),
        "format": "\n\nList each item once. If you include a timeline table, do not repeat its items in a second list.",
    },
    "foa_checklist": {
        "use_key_fields": True,
        "format": ("\n\nName each deadline as the document names it and say whether the document makes it required or optional; "
                   "never call a required item optional. Give an award date only if the document states one."
                   "\n\nInclude a line \"Application limits\" with any limit on the number of applications per institution or per person, "
                   "and a line \"Sponsor contact\" with the contact the document gives; write \"Not stated\" for either if the document "
                   "gives none. Describe each evaluation criterion in the document's own words; if it gives only a name and points, give only those."),
    },
    "rfa_checklist": {
        "use_key_fields": True,
        "format": ("\n\nInclude a line \"Application limits\" with any limit on the number of applications per institution or per person, "
                   "and a line \"Sponsor contact\" with the contact the document gives; write \"Not stated\" for either if the document gives none."),
    },
    "subaward_extraction": {
        "use_key_fields": True,
        "replace": {"Prime Award Period Start/End (if specified)": "Estimated Project Period Start/End of the subaward (if specified)",
                    "- Prime Award Period: [start] - [end] (if specified)": "- Estimated Project Period: [start] - [end] (if specified)"},
        "format": ("\n\nList only the reports the document marks as required, each with its due date in the document's own words; "
                   "do not add report types the document does not list. Label the subaward's own estimated project period as "
                   "\"Estimated project period\", and give a prime award period only if the document states one."),
    },
}


def _text_key(data):
    return next((k for k in ("prompt", "format_template", "formatting_prompt", "template", "instructions") if k in data), None)


HEADER = ("\n\nBegin your output with four lines copied exactly from the document: award number, project title, "
          "principal investigator, and project period.")

AWARD_LOOKUPS = [
    ("Financial management, payment and federal financial reporting by recipients", 2),
    ("Performance reporting and closeout deadlines for recipient final reports", 2),
    ("Retention period for recipient records and exceptions to record retention", 2),
    ("Recipient procurement standards and pass-through entity monitoring of subrecipients", 2),
    ("Single audit applicability and responsibilities of the auditee", 2),
]

PASSAGE_EVIDENCE = (
    "Read the award and the retrieved Uniform Guidance excerpts separately. Attribute each award term to the award. "
    "For a rule added from an excerpt, give the source title and a short verbatim quote supporting the rule. "
    "Use a section identifier for that rule only when its heading appears in the same excerpt and the quoted text "
    "belongs to that heading. When an excerpt starts midway through a section, the title and quote are the citation. "
    "Report gaps when the excerpts do not support an answer.\n\n"
)

PRIOR_APPROVAL_FORMAT = (
    "Format the Extraction report with bold category labels and preserve its five sections. Use a Markdown table "
    "for approval procedures with columns for approval type, trigger, required documentation, authority, timeline "
    "and consequences. Keep the award terms separate from supplemental federal guidance. Verify every supplemental "
    "rule against the original Regulation passages. Retain the source title and a short exact quote. Remove any "
    "section or subsection locator the quoted excerpt does not establish. Retain award citations found in the award. "
    "Preserve thresholds, dates, responsible parties and missing-information statements."
)

AWARD_FORMAT = (
    "Merge the compliance and financial extractions. Use the award face sheet to verify the header. Begin with "
    "Award Compliance & Financial Overview and give the project title, legal awardee organization, awarding agency, "
    "FAIN, principal investigator and period of performance. Use the agency and regulations named in this award. "
    "Distinguish the awardee institution from the investigator and the federal sponsor.\n\n"
    "Use a two-column Financial Summary table for total, obligations, annual breakdown if stated, federal and "
    "nonfederal shares, cost sharing, indirect rate and base, and performance dates. Follow with Approved Budget "
    "& Restrictions, retaining category amounts and restrictions. Use the five compliance sections from the "
    "extraction, including a Compliance Calendar covering every report and deadline. Keep exceptions, thresholds, "
    "agencies, systems, and due dates as given. Mark missing information explicitly. Attribute award requirements "
    "to the award. For supplemental rules retain the supporting excerpt title and exact quote, checking both "
    "against the Regulation passages. Omit a rule when the cited excerpt does not support it."
)


def improve(item, seed):
    """Changes the test runs showed were needed. The catalog originals are untouched."""
    spec = IMPROVE.get(seed, {})
    last_text_task = None
    first_prompt = True
    for i, st in enumerate(item["steps"]):
        for t in st["tasks"]:
            d = t["data"]
            key = _text_key(d)
            if t["name"] == "Extraction" and spec.get("rename_fields") and isinstance(d.get("searchphrases"), str):
                for old, new in spec["rename_fields"].items():
                    assert old in d["searchphrases"], old
                    d["searchphrases"] = d["searchphrases"].replace(old, new)
            if key:
                for old, new in spec.get("replace", {}).items():
                    d[key] = d[key].replace(old, new)
            if t["name"] == "Prompt":
                # The catalog's later prompts say they use the previous step's output but were wired to the document only.
                if spec.get("wire_extraction") and i > 0 and d.get("input_source") == "workflow_documents":
                    d.pop("input_source")
                    d["input_sources"] = ["step_input", "workflow_documents"]
                if spec.get("prompt") and i > 0 and st is not item["steps"][-1]:
                    d["prompt"] = d["prompt"].rstrip() + spec["prompt"]
                if spec.get("header") and first_prompt:
                    d["prompt"] = d["prompt"].rstrip() + HEADER
                first_prompt = False
                d["prompt"] = d["prompt"].rstrip() + HOUSE_RULE
            if t["name"] in ("Prompt", "Formatter") and st.get("is_output"):
                last_text_task = t
    for old in spec.get("replace", {}):
        assert old not in json.dumps(item), old
    if last_text_task is not None:
        key = _text_key(last_text_task["data"])
        assert key, (seed, sorted(last_text_task["data"]))
        extra = spec.get("format", "") + FORMAT_RULE
        if spec.get("use_key_fields"):
            # The report step only saw the step before it, so values found only in Key fields were lost.
            last_text_task["data"].pop("input_source", None)
            last_text_task["data"]["input_sources"] = ["earlier_steps"]
            extra += USE_KEY_FIELDS
        last_text_task["data"][key] = last_text_task["data"][key].rstrip() + extra


def spaced(names):
    return [n.replace("_", " ").replace("FA ", "F&A ").replace("PTE", "Pass-Through Entity") for n in names]


RFA_FIELDS = spaced(["Dates_Table", "Eligible_Institutions", "Eligible_Individuals", "Award_Duration", "Amount_Per_Award",
                     "Number_Of_Awards", "Anticipated_Award_Date", "Required_Components", "Optional_Components",
                     "Submission_Details", "Sponsor_Contact", "Special_Requirements", "Funding_Limits", "Cost_Sharing", "FA_Policy",
                     "Allowable_Costs", "Unallowable_Costs", "Personnel_Effort"])
FOA_FIELDS = spaced(["FOA_Number", "Assistance_Listing_Number", "Federal_Agency", "FOA_Title", "Total_Funding",
                     "Expected_Awards", "Award_Range", "Cost_Sharing_Required", "Critical_Dates", "Performance_Period",
                     "Eligible_Applicants", "Total_Points", "Evaluation_Criteria", "Minimum_Threshold", "Application_Limits_per_Institution_or_Person",
                     "Submission_Platform", "Required_Registrations", "Required_Forms", "Application_Components",
                     "Page_Limits", "Formatting_Standards"])
SUBAWARD_FIELDS = spaced(["PTE_Name", "Subrecipient_Name", "Federal_Award_Number", "Subaward_Number", "Project_Title",
                          "Federal_Awarding_Agency", "PTE_PI", "Subrecipient_PI", "Budget_Period_Start",
                          "Budget_Period_End", "Amount_Funded", "Total_Direct_Costs", "Total_Indirect_Costs",
                          "Cost_Type", "Invoicing_Frequency", "Final_Invoice_Due", "FA_Rate", "FA_Base",
                          "Cost_Sharing_Required", "Carryforward_Policy", "Reports_Marked_Required_with_Due_Dates_as_Written",
                          "Reports_Listed_but_Not_Marked_Required", "Estimated_Project_Period", "Record_Retention"])

VARIANTS = [
    # seed file, what changes, kb query, key fields, setup noun, snapshot
    ("ffr_management", "federal financial report (SF-425) requirements; financial reporting frequency and due dates; closeout financial reports; cash management and payment", None, "award", False),
    ("prior_approval_tracking", "prior approval requirements; revision of budget and program plans; changes requiring prior written approval; no-cost extension; change in key person; equipment and subawards", None, "award", False),
    ("award_compliance_analysis", AWARD_LOOKUPS, None, "award", True),
    ("noa_summary", "period of performance; allowable costs; indirect cost rates; reporting requirements; prior approval requirements; record retention; closeout", None, "award", True),
    ("effort_reporting_compliance", "compensation for personal services; standards for documentation of personnel expenses; institutional base salary; cost sharing of effort", None, None, False),
    ("post_award_closeout_checklist", None, None, "award", False),
    ("foa_checklist", None, FOA_FIELDS, "funding opportunity", False),
    ("rfa_checklist", None, RFA_FIELDS, "funding opportunity", False),
    ("subaward_extraction", None, SUBAWARD_FIELDS, None, False),
]


def variants(repo, ref, uid):
    out = {}
    for seed, kb_query, fields, setup, snapshot in VARIANTS:
        item = clean(load_seed(repo, ref, seed))
        changes = []
        keep_report_as_output(item)
        improve(item, seed)
        if seed in IMPROVE:
            changes.append("tightens the report rules after test runs")
        if kb_query:
            queries = [(kb_query, 8)] if isinstance(kb_query, str) else kb_query
            reviewed = seed in ("prior_approval_tracking", "award_compliance_analysis")
            add_kb_first(item, queries, PASSAGE_EVIDENCE if reviewed else KB_PREFACE)
            if reviewed:
                # The formatter previously saw only an extraction, so it repeated unsupported citations and gaps.
                report = item["steps"][-1]["tasks"][0]
                assert report["name"] == "Formatter"
                report["data"]["input_sources"] = ["workflow_documents", "earlier_steps"]
                if seed == "award_compliance_analysis":
                    report["data"]["prompt"] = AWARD_FORMAT + FORMAT_RULE
                    for rule in item["validation_plan"]:
                        if rule["name"] == "Header Fields Presence":
                            rule["description"] = (
                                "The report identifies the project title, legal awardee, awarding agency, FAIN, "
                                "principal investigator and project period as given on the award face sheet. "
                                "Fail if the report omits a supplied value or substitutes a person for the awardee."
                            )
                else:
                    report["data"]["prompt"] = PRIOR_APPROVAL_FORMAT + FORMAT_RULE
                item["validation_plan"].append({
                    "id": uid(f"{seed}-passage-citations"),
                    "name": "Supplemental rules can be traced to their passages",
                    "category": "accuracy",
                    "description": (
                        "For each supplemental rule, find its source title and quoted words in the retrieved "
                        "passages. The quote must support the claim. Fail if a section locator is attributed "
                        "to an excerpt that lacks its heading or if an award term is attributed to another source."
                    ),
                })
            changes.append("cites Uniform Guidance from a knowledge base step")
        if fields:
            add_fields_first(item, fields)
            changes.append("adds a structured key-fields step that can be checked field by field and exported")
        if setup:
            add_setup(item, setup, snapshot)
            changes.append("after one approval, creates the project and adds deadlines to the RA inbox"
                           + (" and saves an award snapshot Page" if snapshot else ""))
        item["description"] = ((item.get("description") or "").rstrip(". ") + ". V5 draft: " + "; ".join(changes) + ".").strip()
        item["name"] = item["name"] + " (V5 draft)"
        out[f"variants/{seed.replace('_', '-')}.v5-draft.workflow.vandalizer.json"] = {
            "vandalizer_export": True, "schema_version": 2, "export_type": "workflow", "items": [item]}
    return out


def budget_skill(skill, repo, ref):
    base = load_seed(repo, ref, "budget_generator")["steps"][0]["tasks"][0]["data"]["prompt"].strip()
    lines = [ln for ln in base.splitlines() if ln.strip().startswith("- ")]
    text = BUDGET_JUSTIFICATION_INTRO.strip() + "\n" + "\n".join(lines) + BUDGET_JUSTIFICATION_OUTRO
    return skill(
        "Budget justification with the PI's answers",
        "Draft a line-by-line budget justification from a budget, list what the PI must supply, and revise the draft as the answers come in.",
        text)


def build(skill, uid, repo, ref):
    files = {
        "new/export-to-banner-form-review.skill.vandalizer.json": skill(
            "Export to Banner form review",
            "Compare a prepared Export to Banner form with the award document and list the differences as questions for the analyst.",
            EXPORT_REVIEW),
        "new/modification-correspondence.skill.vandalizer.json": skill(
            "Modification correspondence",
            "Draft the PI and DGA email, the Banner FOA text line and the processing note for an award modification, from the executed amendment.",
            CORRESPONDENCE),
        "new/idc-exception-triage.skill.vandalizer.json": skill(
            "Indirect cost exception triage",
            "Sort the rows of an Indirect Cost Exception Report into rounding, likely subaward threshold, likely exempt costs, and rows that need a Banner lookup.",
            IDC_TRIAGE),
        "new/final-billing-review.skill.vandalizer.json": skill(
            "Final billing review helper",
            "Organise a grant's unbilled transactions for closeout: check totals, lay out payroll around the end date, and flag transactions to review before the final invoice.",
            FINAL_BILLING),
        "companion/screening-list-lookup.skill.vandalizer.json": skill(
            "Screening list lookup",
            "Look up the parties in a project or agreement on the Consolidated Screening List in the browser and report what the list shows. Use alongside Export Control Screening.",
            SCREENING),
        "companion/subrecipient-sam-check.skill.vandalizer.json": skill(
            "Subrecipient SAM.gov check",
            "Check a subrecipient's SAM.gov registration, UEI, expiry and exclusions in the browser and compare them with the subaward document.",
            SUBRECIPIENT),
        "companion/live-solicitation-check.skill.vandalizer.json": skill(
            "Live solicitation check",
            "Compare the solicitation PDF the team is using with the opportunity's live page, to catch a changed deadline or a new amendment.",
            SOLICITATION_CHECK),
        "companion/fa-rate-agreement-check.skill.vandalizer.json": skill(
            "F&A rate agreement check",
            "Compare the F&A rate and base in an award or budget with the institution's published rate agreement page.",
            FA_RATE_CHECK),
    }
    files.update(new_workflows(uid))
    if repo:
        files.update(variants(repo, ref, uid))
        files["new/budget-justification.skill.vandalizer.json"] = budget_skill(skill, repo, ref)
    return files
