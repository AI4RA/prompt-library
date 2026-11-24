"""Builds the Vandalizer import files in this draft collection.

Usage, from the collection directory (drafts/vandalizer-ra-builds):

    python3 scripts/build_drafts.py . [<vandalizer repo> [<git ref>]]

New Skills and workflows are written from the text in this file and in
more_drafts.py. Variants of catalog workflows are generated from the seed
files in the vandalizer repo at <git ref> (default origin/major/agentic-chat);
they are skipped when no repo is given.
"""
import json, sys, uuid, pathlib

out = pathlib.Path(sys.argv[1])
NS = uuid.UUID("6f1d2c0e-7a54-4d0e-9a55-0c1b7a4e5d21")
def uid(name): return str(uuid.uuid5(NS, name))

def skill(title, when, text):
    text = text.strip()
    assert len(text) <= 32000 and len(when) <= 500
    return {"vandalizer_export": True, "schema_version": 2, "export_type": "search_set", "items": [{
        "title": title, "set_type": "prompt",
        "extraction_config": {"content": text, "when_to_use": when},
        "items": [{"title": title, "searchphrase": text, "searchtype": "extraction", "is_optional": False, "enum_values": []}],
        "test_cases": [],
    }]}

# ---------------------------------------------------------------- Skill 1
SPONSOR = """
Research a sponsor before it is added to VERAS as a business associate, and return a proposed record for the VERAS administrator to enter. You never create or change anything in VERAS, SAM.gov or any other site: you read public pages and report.

What to ask for first
Ask for whatever of these the person has not given: the sponsor name as the requester wrote it, its address, and its website. Contact name, email and phone are optional. If the name, address or website is missing, say which, and offer the reply described under "Drafts" asking the requester for it. Continue with what you have if the person tells you to.

Step 1. Name variants to search in VERAS
Before any research, list the searches the administrator should run in VERAS Business Associates to check the sponsor is not already there, because duplicates under slightly different names are the main risk:
- the full name as given
- the name with and without a leading "The"
- "&" in place of "and", and the reverse
- common abbreviations and the familiar name (for example WSU, USDA)
- each distinctive keyword alone (for example "Florida" for University of Florida)
Say plainly that you cannot see VERAS and that the person must run these. If the sponsor is a sub-agency or regional office of an entity that is likely already there (for example US Forest Service Region 6), say that it should normally be added as a contact under the parent entity, not as a new sponsor.
If the person reports that the sponsor already exists, stop the research and write the "already exists" reply under "Drafts".

Step 2. Research on SAM.gov
Use the person's connected browser (browser_open, browser_read). Do not substitute web search, fetch_url or memory for the browser.
Open https://sam.gov/search/ and search entity registrations for the sponsor's legal name. Read the result list and the matching entity's page. Record each of these with record_value, exactly as shown, one call per value: legal business name, Unique Entity ID (UEI), physical address, mailing address, entity or business type, profit structure, and congressional district if shown.
Then decide which of these applies and say so:
- One clear match: use it.
- Several entries with different addresses or sub-units: list each with its UEI and address, compare them with the address and context the requester gave, and name the one that fits. If none can be confirmed, say that the UEI should be left out until the award stage, when the awarding office is known. Do not pick one to be helpful.
- A completed entity search with zero matches: give the query, filters and result, then go to Step 3. If the registration is inaccessible, identify the access limit and use Step 3 for the public fields you can check.
Use a UEI in the proposed record only when the matching registration identifies the relevant office and can be cited. A UEI on an historical award may be a lead: keep it in follow-up notes with a link to the specific award. Without that citation leave the number out. Never use an award as proof of current registration.

Step 3. Other sources, only when SAM.gov has no entry
In this order:
1. The Secretary of State business entity registry for the state the sponsor is in: legal name and entity classification.
2. The sponsor's own website: the About page for what kind of entity it is, the Contact page for address, phone and email.
Record each literal field separately with record_value and link its exact source. If the state registry cannot be searched, say so. Distinguish an inaccessible source from a completed search with zero matches. Mark the VERAS duplicate check pending until the administrator reports its result.

Step 4. Classify
Propose an Associated Type that describes what kind of organization it is: federal, another state's government, foundation or non-profit, private industry, and so on. If the person has attached the "Associate Type Code Definitions" guide or a knowledge base that contains it, use its wording and codes; otherwise give the plain description and say the code must be chosen from the guide.
Never propose "Foreign" as the Associated Type. Foreign status is a separate yes/no field: answer Yes when the sponsor or its parent company is a foreign entity, even if the address used is in the United States. Name the foreign parent and its country when there is one.
Compare the legal name with the common name: a leading "The" or "A", and a trailing "s", are the usual differences. The legal name goes in the name field; the common name is the familiar name.

Sign-in, permission and safety
Open a site only after the person approves it. If a tool returns login_required or unapproved_site, stop and ask the person to deal with it in the working tab and tell you to continue; never ask for or type a password. Read the current working tab after the person continues. Never submit, save or change anything on a website. Identify unreadable pages and fields not shown on an accessible page separately.

What to return
1. Proposed VERAS record, as a table with columns Field, Proposed value, Source (a link to the exact page):
   - Associate name (legal name)
   - Familiar name, if different
   - Associated Group: Sponsor, Vendor and Subrecipient (always all three; Vendor is what allows documents to be saved to the associate)
   - Associated Type (never "Foreign")
   - Foreign Entity: Yes or No, with the reason
   - Reports to Sponsor Name: the foreign parent, if any
   - Address: the mailing address; add the physical address when it differs. For a foreign address, say it should be checked in Smarty international address validation before entry.
   - Congressional district, if found
   - Website
   - Notes: the UEI, or "UEI deferred to award stage" with the reason, and a general email if there is no named contact
   - Associated Abbreviation: leave blank (post-award fills it when the Banner GID is assigned)
   - Contact: name, email, phone, division and whether technical or administrative, from the request only
2. Open questions: anything ambiguous, missing or needing a person's decision.
3. The VERAS search list from Step 1, if not already given.

Drafts
Write only the one that applies, ready to paste, and say it is a draft for the administrator to send:
- Missing information: a short reply to the requester naming exactly what is missing.
- Added: a reply confirming the sponsor was added, giving the exact name as entered so it can be searched, and the contact added, with the pre-award unit copied. Write this only after the person says the record is saved and searchable.
- Already exists: a reply giving the existing entry's exact name as it appears in VERAS.
"""

# ---------------------------------------------------------------- Skill 2
TPS = """
Help a reviewer work through a Timeliness of Proposal Submission (TPS) waiver request: set the scores side by side, total them, lay out the timeline, and draft the reviewer notes and the decision message. The reviewer decides. Never state or imply that the waiver is approved or denied until the reviewer tells you their decision.

What you need
Work from what the person pastes or attaches. Ask for anything missing, one short list, and continue with what you have if they say so:
- the TPS waiver ticket: each waiver question, the PI's score and comment, and the SPA's score and comment
- from VERAS: the date the proposal was created, the sponsor due date and time with its time zone (Section 5), and the tier of support (Section 4)
- the internal TPS deadlines from the due date calculator for that tier and due date
- the proposal's VERAS correspondence, or the reviewer's summary of it
- the SPA's current workload, if the reviewer wants it weighed
You cannot open the ticket system, VERAS or the due date calculator. Do not work out the internal TPS deadlines yourself: use the calculator's dates as given, and if they are missing, say the timeline is incomplete. If a knowledge base with the TPS policy is attached, use it for the meaning of each question and tier, and cite the passage; otherwise use only what the ticket says.

Step 1. Scores side by side
Make a table: Question, PI score, PI comment (short), SPA score, SPA comment (short), Match?, Reviewer score.
- Where the PI and SPA scores match, put that score in Reviewer score.
- Where they differ, leave Reviewer score blank. Under the table, for each such question, set out what each party said, what in the correspondence or proposal record bears on it, and what the reviewer would need to know to settle it. You may say which score the record supports better and why, marked as a suggestion. Ask the reviewer for their score on each.
Copy every score exactly. If a score or comment is missing or unreadable, say so; do not infer it.

Step 2. Total and tier
Once the reviewer has given a score for every question, add them with the calculate tool and show the arithmetic. State the tier:
- below 50: Limited justification (leans toward denial)
- 50 to 74: Moderate justification (discretionary; more information may be needed)
- above 74: High justification (leans toward approval)
Say that the tier is guidance and not the decision. If any reviewer score is still missing, give no total.

Step 3. Timeline
List in date order: proposal created in VERAS, each internal TPS deadline from the calculator, the sponsor due date and time, and today. Convert the sponsor's time to the reviewer's local time and show both; sponsor deadlines are often stated in Eastern time. For each internal deadline, say whether it was met or missed and by how many days, using calculate. State how much time remains before the sponsor deadline.

Step 4. What happened
From the correspondence, give a short dated account of who did what and when: the PI, the DGA and the SPA. Quote the passage for anything that bears on why a deadline was missed. Keep facts and the parties' own explanations separate. Note anything the correspondence does not show.

Step 5. Factors for the decision
Set out, without recommending an outcome: which deadlines were missed and by how much; the stated reasons; the time left; how engaged the PI and DGA have been; and the SPA's capacity to process the proposal in the time left, if given. Mark each as supported by the record, stated by a party only, or unknown.

Step 6. Reviewer notes
Draft notes for the review template of no more than 150 words: the scoring result, the timeline, the key points from the correspondence and the factors above. Write them as the reviewer's working notes, with no decision in them.

Step 7. After the reviewer decides
Ask for the decision if it has not been given. Then:
- Add one sentence to the notes recording the decision and the main reason the reviewer gave.
- Draft the decision message for the ticket. If the reviewer pastes the approve or deny communication template, fill it in and change nothing else in it. If not, write a short, courteous message with the PI's name, proposal title, sponsor, sponsor due date, the decision, and the reason in the reviewer's words. For an approval, say the proposal will continue to be processed. For a denial, say it will not be processed further for this deadline.
Say that the message is a draft for the reviewer to send through the ticket system.

Rules
Use only the ticket, the VERAS details, the calculator dates, the correspondence and any attached policy. Never invent a score, date, name or reason. Keep people's comments in their own words when you quote them. If two sources disagree on a date or score, show both and ask.
"""

# ---------------------------------------------------------------- Workflow
FIELDS = [
 "Award Number or FAIN", "Sponsor Award Number", "Amendment or Modification Number", "Modification Type",
 "Execution Status", "Sponsor or Agency Name", "Program or Grants Officer",
 "Principal Investigator", "Previous Principal Investigator", "New Principal Investigator",
 "Effective Date", "Sponsor Approval Date", "Current End Date", "New End Date",
 "Modification Amount", "Award Amount Before This Modification", "Total Obligated Amount After This Modification",
 "F&A Rate", "F&A Amount", "Budget Breakdown by Category", "Rebudget Source Category", "Rebudget Destination Category",
 "Cost Share Changes", "Payment System or PMS Code", "Point of Contact Changes", "Prior Approval Reference",
 "Sponsor Conditions", "Regulations or Terms Cited",
]
assert all("," not in f for f in FIELDS)

BRIEF = """
You are preparing a Modification Intake Brief for a post-award specialist in a university Office of Sponsored Programs. Your input is the modification document (an amendment, no-cost extension, PI change approval, rebudget approval or similar) and the details extracted from it in the previous step. The specialist uses the brief to process the modification in VERAS and Banner. You cannot see VERAS or Banner: never state what they contain.

Rules
- Use only the document. Copy every amount, date, name and identifier exactly as written; do not round, reformat or abbreviate them.
- If the document does not state something, write "Not stated in the document". If a field does not apply to this type of modification, write "Not applicable".
- If an extracted value contradicts the document, follow the document and note the difference under Discrepancies. Do not mention fields the extraction left empty, or the extraction step itself.
- Do not mention page headers, footers or watermarks at all, not even to say you ignored them, and do not comment on whether the document is genuine.
- A sponsor approval letter that says no amendment will be issued is not an amendment: say so, and give the amendment number as "None issued".
- Do not add requirements from general knowledge of federal rules. Cite a regulation or term only if the document cites it.

Write these sections, in this order.

1. Classification
Type: exactly one of Additional Funds, No-Cost Extension, PI Change, Rebudget, Scope Change, Administrative Change, or Combined (name each type included).
Confidence: High, Medium or Low.
Evidence: the document's own words that show the type, quoted, with the page if shown.
Award number or FAIN, sponsor award number if different, amendment number, sponsor.
Execution status: Unilateral (issued by the sponsor, no university signature needed), Bilateral (needs signatures; say whose are present and whose are missing), or Not stated in the document.

2. Key details
A table of Field and Value with only the rows that apply to the type:
- Additional Funds: modification amount; award amount before; total obligated after; F&A rate; F&A amount; budget by category; cost share changes.
- No-Cost Extension: current end date; new end date; any change in funding (normally none; say what the document says).
- PI Change: previous PI; new PI; effective date; sponsor approval date.
- Rebudget: amount moved; source category; destination category; sponsor approval date; the justification as stated.
- Scope Change or Administrative Change: what changed, in the document's words.
For Combined, include the rows for each type.

3. Checks
- For Additional Funds: add the award amount before and the modification amount and compare with the total obligated after. Show the arithmetic and say whether it agrees. If any of the three is not stated, say the check could not be made.
- For a No-Cost Extension: say whether the new end date is later than the current end date.
- For a PI Change: say whether both the previous and new PI are named.
- Say whether the award number is the same everywhere it appears in the document.

4. Conditions and approvals
Sponsor conditions, each as a bullet in the document's words. A condition is something new this modification requires; a sentence saying other terms are unchanged, or restating how payment works, is not one. If there are none, write "None". Prior approval the document refers to, with its date. Regulations or terms the document cites. Payment system or PMS code, and any point of contact changes.

5. Discrepancies and open questions
Anything inconsistent inside the document, anything the specialist needs that the document does not state, and anything ambiguous in the classification.

6. Processing checklist
If the execution status is Bilateral and a signature is missing, begin this section with "Do not process yet: awaiting" and name the missing signature; give the checklist under the heading "Once fully executed".
Give the checklist for the classified type only (each one for Combined). These are the specialist's steps; you have not done any of them. Put the document's values into the steps where they belong.
- Additional Funds: match the sponsor ID on the modification to Banner; verify the cumulative amounts against Banner; check for point of contact updates; enter the amendment details, funding amounts, F&A rate and budget by account category in the VERAS mod processing form and confirm the form total; create the journal entry in Banner and record its number in the form; update the FOA text and the current and cumulative amounts in Banner; send correspondence to the PI and DGAs; forward to the Financial Unit and wait for its confirmation.
- No-Cost Extension: upload the fully executed agreement to the VERAS mod processing form and enter the amendment details; check the PMS code in Banner; update the end dates in Banner to the new end date; update the FOA text in Banner; send correspondence; update the processing notes; reassign the task to the Financial Unit; update the review outcome and project status.
- PI Change: verify the amendment details; record the sponsor approval in the VERAS sponsor prior approval request; in Banner remove the previous PI, insert the new PI and update the PI on the main page; update the FOA text; mark Banner updated in VERAS; send correspondence with the amendment attached; update the submission outcome; file the correspondence.
- Rebudget: upload the sponsor approval to VERAS; open the sponsor prior approval request (SPAR) form; look up the index in Banner and enter it in the form; verify the budget accounts; check the narrative for anything the PI must follow up; create the journal entry in Banner with the debit to the source account and the credit to the destination account, and record its number in the form; complete the form; send correspondence; reset the project status to Active.
- Scope Change or Administrative Change: no standard checklist. List what the document changes and say the specialist should confirm the processing path with their supervisor.

7. Draft correspondence
A short draft email to the PI and DGAs, for the specialist to edit and send from VERAS: what the modification is, the amendment number, the values that changed, every sponsor condition with its deadline, and any change in point of contact, each exactly as in the document. If a signature is still missing, word the email as notice that the amendment is awaiting signature and not yet in effect. End with a line saying the amendment is attached. Then one line headed "FOA text for Banner" stating the amendment number, the type and the changed values. Mark both as drafts.
"""

VALIDATION_TEXT = """FICTIONAL QA MATERIAL - NOT A REAL AWARD
Example Science Agency
AMENDMENT TO GRANT AGREEMENT

Federal Award Identification Number (FAIN): EX-2025-67013-00412
Amendment Number: 003
Recipient: Example State University
Principal Investigator: Dr. Jordan Example
Project Title: Soil Moisture Sensing for Dryland Wheat
Grants Officer: Casey Sample

1. PURPOSE. This amendment extends the period of performance at no additional cost to the Example Science Agency. The recipient requested the extension by letter dated March 3, 2027, and the request is approved.

2. PERIOD OF PERFORMANCE. The period of performance end date is changed from August 31, 2027 to August 31, 2028.

3. FUNDING. The total amount obligated remains $412,650.00. No funds are added or removed by this amendment.

4. CONDITIONS. The recipient shall submit a revised project timeline within 30 days of the effective date of this amendment. All other terms and conditions of the award remain unchanged.

5. EFFECTIVE DATE. This amendment is effective April 1, 2027. It is issued unilaterally by the Example Science Agency and does not require the recipient's signature.

Issued by: Casey Sample, Grants Officer, Example Science Agency, March 28, 2027
"""

workflow = {"vandalizer_export": True, "schema_version": 2, "export_type": "workflow", "items": [{
    "name": "Award Modification Intake",
    "description": "Classifies an award modification (additional funds, no-cost extension, PI change, rebudget) and writes an intake brief: key details, checks, sponsor conditions, a processing checklist and draft correspondence.",
    "steps": [
        {"name": "Modification details", "data": {}, "is_output": False,
         "tasks": [{"name": "Extraction", "data": {"searchphrases": ", ".join(FIELDS)}}]},
        {"name": "Intake brief", "data": {}, "is_output": True,
         "tasks": [{"name": "Prompt", "data": {"prompt": BRIEF.strip(), "input_sources": ["step_input", "workflow_documents"]}}]},
    ],
    "input_config": {}, "output_config": {}, "resource_config": {},
    "validation_plan": [
        {"id": uid("vp-type"), "name": "The modification type is right and evidenced", "category": "accuracy",
         "description": "The brief names exactly one type from its list (or Combined with each type named), and quotes words from the document that show it. FAIL if the type is wrong, or the evidence is not in the document."},
        {"id": uid("vp-values"), "name": "Amounts, dates and identifiers match the document", "category": "accuracy",
         "description": "Every award number, amendment number, dollar amount, date and name in the brief appears in the document with the same value and year, unrounded. FAIL if any differs or has no basis in the document."},
        {"id": uid("vp-notstated"), "name": "Nothing is filled in that the document does not state", "category": "accuracy",
         "description": "Where the document does not state a detail, the brief says \"Not stated in the document\" or \"Not applicable\". FAIL if the brief supplies an F&A rate, PMS code, account, regulation or other detail the document does not give, or says what VERAS or Banner contains."},
        {"id": uid("vp-checklist"), "name": "The checklist fits the type", "category": "content",
         "description": "The processing checklist is the one for the classified type only, written as steps for the specialist and not as work already done, and the draft correspondence gives the amendment number and the changed values. FAIL if another type's checklist is given or a step is described as completed."},
    ],
    "validation_inputs": [{"id": uid("vi-nce"), "type": "text",
        "label": "Fictional no-cost extension. Answer key: type No-Cost Extension; FAIN EX-2025-67013-00412; Amendment 003; unilateral; end date August 31, 2027 changed to August 31, 2028; total obligated stays $412,650.00 with no funds added; effective April 1, 2027; one condition (revised project timeline within 30 days); F&A rate, PMS code and budget categories are not stated.",
        "text": VALIDATION_TEXT}],
}]}

files = {
    "new/add-sponsor-research.skill.vandalizer.json": skill(
        "Research a sponsor for VERAS",
        "Research a new sponsor on SAM.gov and other public sources and propose the VERAS business associate record, before an administrator adds it.",
        SPONSOR),
    "new/tps-waiver-review.skill.vandalizer.json": skill(
        "TPS waiver review",
        "Review a TPS waiver ticket: compare PI and SPA scores, total them into the justification tier, lay out the timeline, and draft reviewer notes and the decision message.",
        TPS),
    "new/award-modification-intake.workflow.vandalizer.json": workflow,
}

import more_drafts
files.update(more_drafts.build(skill, uid, sys.argv[2] if len(sys.argv) > 2 else None,
                               sys.argv[3] if len(sys.argv) > 3 else "origin/major/agentic-chat"))

def show_fields_in_editor(data):
    """Store each extraction step's fields as a list under "extractions".

    The older comma-separated "searchphrases" string (still used by the
    catalog seeds) runs, but the workflow editor only displays "extractions",
    so the step looks empty. The split is the one the engine does at run time.
    """
    for item in data.get("items", []):
        for step in item.get("steps", []):
            for task in step.get("tasks", []):
                phrases = task.get("data", {}).get("searchphrases")
                if task.get("name") == "Extraction" and isinstance(phrases, str):
                    del task["data"]["searchphrases"]
                    task["data"]["extractions"] = [f.strip() for f in phrases.split(",") if f.strip()]


for name, data in sorted(files.items()):
    show_fields_in_editor(data)
    path = out / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(name)
