# Changelog — rfp-extraction

All notable changes to this component. Versions follow semver: MAJOR for output-contract breaks, MINOR for backward-compatible additions, PATCH for wording or clarity.

## [1.1.0] — 2026-04-18

- Add agent manifestation (`agent/AGENT.md`, name `rfp-extractor`, tools: Read/WebFetch/Glob/Grep/Write). Resolves file paths, URLs, or pasted text; optionally writes the checklist to a file; reports a one-line summary of the most consequential constraint.
- Lockstep version bump on `prompt.md` and `skill/SKILL.md` (no content change in those manifestations).

## [1.0.0] — 2026-04-18

- Initial version.
- Canonical prompt (`prompt.md`) authored 2026-04-17 during NSF 26-508 submission prep.
- Claude Skill manifestation (`skill/SKILL.md`) added with description tuned for skill-router matching.
- First golden eval case: NSF 26-508 (TechAccess) — a multi-round solicitation with LOI requirements and several PAPPG deviations.
