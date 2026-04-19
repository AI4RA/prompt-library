# Input source

The solicitation block in `input.md` is **synthetic**: a short excerpt of an Engineering Research Center-style NSF solicitation constructed specifically for this eval. It is not a real NSF ERC solicitation and the identifier "NSF 99-SYN-ERC" is a placeholder.

The synthetic text introduces two documents that are not part of the standard PAPPG default set: a Strategic Plan and a Knowledge Transfer Plan. Both are emitted in `expected.json` with code `other` and a distinctive `label`, exercising the controlled-vocabulary fallback.

The text is intentionally narrow: it does not mention or modify any PAPPG default document, so `expected.json` contains exactly two entries, both net-new.

The sponsor-defaults JSON block in `input.md` is the same NSF full-proposal defaults used in the `nsf-dcl-narrative-tightened` case, for consistency across the modify-only and net-new-only evaluations.

No sensitive or identifying content is present.
