# OCR Quality Signals

Uploads one PDF to Vandalizer and returns a schema-backed JSON record of OCR-text anomaly signals that can be joined to downstream workflow outcomes. It is a measurement workflow for calibration and review routing, not a claim that OCR quality can be known from text alone.

**Workflow version:** 0.1.0
**Vandalizer schema version:** 2
**Status:** experimental
**Components manifested:** `ocr-quality-signals@0.1.0`
**Eval posture:** inherited from `components/ocr-quality-signals/evals`

## What this workflow does

The operator uploads a PDF. Vandalizer performs its normal OCR, then the single Prompt task reads the resulting document text and emits:

- size and coverage estimates;
- 12 raw anomaly counts and rates with short verbatim examples;
- provisional threshold flags; and
- a transparent flag-density index plus review recommendation.

Run it before or beside a production extraction workflow. Persist its JSON output with the downstream result so analysis can test which individual signals correlate with missing, malformed, or incorrect fields.

## Important limitation

The workflow uses an LLM Prompt task because the current Vandalizer workflow schema has no deterministic code node. Counts are labeled `llm_estimate`. For calibration, run at least five replicates and use median signal rates. Do not use the provisional recommendation as an automatic rejection gate until it has been validated for the document family and downstream workflow in question.

## Component

- [`ocr-quality-signals@0.1.0`](../../components/ocr-quality-signals/) — owns the prompt, JSON schema, signal definitions, thresholds, and calibration plan.

## Eval posture

Evals inherit from [`components/ocr-quality-signals/evals`](../../components/ocr-quality-signals/evals/) because this is a 1:1 Vandalizer repackaging of the canonical prompt. No workflow-local prompt override or orchestration is added.

## Building

```bash
python3 scripts/build_vandalizer_workflows.py
```

Treat `manifest.yaml` as the source of truth and never hand-edit the generated export.

## Sharing

Upload `ocr-quality-signals.vandalizer.json` through Vandalizer's workflow import UI. The export's `x_ai4ra` block records the source manifest, workflow version, component version, and embedded-prompt hash.

## Triad integration

- **Evaluation datasets:** `synthetic.workshop_ocr` (ground-truth calibration) and `real.nsf_rfa_checklist_eval` (paired clean/OCR external check).
- **Harness notes:** the harness does not yet register this workflow. A future runner should store the 12 raw signal rates, the downstream field-level outcome, model/OCR provenance, and replicate number in the run artifact.
- **Shared UDM relationship:** none; the contract is repo-local.

## Provenance

Authored 2026-08-08 to make OCR quality an observable, testable input condition for Vandalizer workflows instead of an informal visual judgment.
