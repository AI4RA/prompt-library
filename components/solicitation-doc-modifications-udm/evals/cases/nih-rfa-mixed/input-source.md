# Input source

The solicitation block in `input.md` is **synthetic**: a short NIH-style Request for Applications excerpt constructed specifically for this eval. It is not a real NIH RFA and the identifier "RFA-XX-25-SYN" is a placeholder.

The synthetic text exercises two shapes in a single solicitation:

1. A **modification** to a default: the RFA tightens the NIH Research Strategy (`proposal_narrative`) from the R01 default of 12 pages to 6 pages.
2. A **net-new** document: the RFA adds a "Milestones and Timeline" supplement that has no counterpart in the NIH R01 default set.

The sponsor-defaults JSON block in `input.md` is a condensed NIH R01 defaults object aligned with the shape produced by `sponsor-doc-defaults-udm`'s `nih-r01/` case. It includes only the fields relevant to exercising the modification (a `proposal_narrative` entry with `page_limit: 12`) and enough surrounding defaults to keep the prior realistic.

No sensitive or identifying content is present.
