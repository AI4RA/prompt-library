# Input source

The text in `input.md` is a synthetic reconstruction of the NIH Notice of Award (HHS-3734) header block. All names, amounts, and identifiers are fictional; the structure (Notice of Award header, FAIN, institute code, action code, project period, total award amount, PI line, recipient organization) mirrors the public NIH NoA template.

The purpose of this case is to exercise the classifier's sponsor-agnostic rule: a non-NSF award document with a canonical "Notice of Award" header must classify as `award_notice` at high confidence, with no initial-vs-amendment ambiguity because no amendment or modification marker is present.

No sensitive or identifying content is present.
