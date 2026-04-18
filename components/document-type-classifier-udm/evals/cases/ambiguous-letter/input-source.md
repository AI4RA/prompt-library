# Input source

The text in `input.md` is a synthetic short letter drafted specifically to exercise the confidence band 0.5–0.7 and the `secondary_candidates` emit rule. It mimics the surface features of a letter of support — institutional letterhead, date, salutation, reference to a specific proposal, signature block — but contains no concrete commitment (no resources offered, no collaborative role stated, no subrecipient role, no personnel hours pledged).

The case exists to verify that the classifier does not reflexively assign high confidence to any letter-shaped document that names a proposal. Calibrated classification should lean toward `letter_support` but emit a populated `secondary_candidates` array because the top confidence falls below 0.8.

No sensitive or identifying content is present. All names are fictional.
