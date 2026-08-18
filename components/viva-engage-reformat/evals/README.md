# Evals — viva-engage-reformat

This component is experimental and has **no validated golden cases
yet**. The prompt was captured verbatim from the live Vandalizer copy
and has not been through a logged repo test run.

A first eval case should use a small real (or realistic synthetic)
proposal-submission table — including at least one row with an empty
Prime Sponsor cell and one budget without cents — and validate:

- one "Proposal Submission" block per input row, none dropped or
  invented;
- all six labeled fields present in every block, in order;
- field values verbatim from the source row (no rounding, no
  paraphrase);
- no commentary or prose outside the blocks.

Add a case under `cases/<case-slug>/` only after a human reviewer
validates the expected output and records `validated_against_version`.
