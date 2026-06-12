# Changelog

All notable changes to this component. Versions follow semver: MAJOR for output-contract breaks, MINOR for backward-compatible additions, PATCH for wording or clarity.

## [0.1.0] — 2026-05-21

- Initial experimental release.
- Per-regime classification (human subjects / animal / biosafety), each with `triggered`, `rationale`, and `trigger_signals`, plus an `any_regime_triggered` roll-up.
- Inclusive flagging posture: a plausible expense-level signal sets `triggered: true` so the expense is surfaced for reviewer verification.
- No eval cases yet — status `experimental` until at least one golden classification is added under `evals/cases/`.
