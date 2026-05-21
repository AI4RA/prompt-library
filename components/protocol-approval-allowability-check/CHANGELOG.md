# Changelog

All notable changes to this component. Versions follow semver: MAJOR for output-contract breaks, MINOR for backward-compatible additions, PATCH for wording or clarity.

## [0.1.0] — 2026-05-21

- Initial experimental release.
- Single-requirement check covering institutional IRB (45 CFR 46), IACUC (PHS Policy / 9 CFR), and IBC (NIH Guidelines for Recombinant or Synthetic Nucleic Acid Molecules / 42 CFR 73) protocol-approval coverage.
- Emits the shared cost-allowability finding object (`status`, `summary`, `rationale`, `evidence`, `follow_up_actions`, `confidence`) with `check_id` "protocol-approval-allowability".
- Applicability is gated by the regulated-activity-classifier output; an unflagged expense returns `not_applicable`.
- A flagged expense with no protocol evidence returns `needs_info` to route it for human verification, rather than disallowing the cost on absence of evidence alone.
- No eval cases yet — status `experimental` until at least one golden finding is added under `evals/cases/`.
