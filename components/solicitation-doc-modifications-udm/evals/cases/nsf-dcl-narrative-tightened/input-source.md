# Input source

The solicitation block in `input.md` is **synthetic**: a short Dear Colleague Letter-style supplement constructed specifically for this eval. It is not a real NSF DCL and the identifier "NSF DCL-SYN-01" is a placeholder.

The synthetic text was written to exercise two distinct modification shapes on a single sponsor default without introducing any net-new documents:

1. A **tightening** of a page limit: Project Description shortened from 15 pages (NSF default) to 10 pages.
2. An **expansion with added format spec**: Data Management Plan extended from 2 pages (NSF default) to 3 pages, with a new required subheading.

The sponsor-defaults JSON block in `input.md` is a copy of the `expected.json` from `sponsor-doc-defaults-udm`'s `nsf-full-proposal/` eval case, serving as the prior input to this component. Keeping the two in lockstep is intentional: the two components are evaluated as a pipeline.

No sensitive or identifying content is present.
