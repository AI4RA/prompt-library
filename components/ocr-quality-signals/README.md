# OCR Quality Signals

Audits OCR markdown or plain text and returns a stable JSON record of observable anomaly rates: encoding damage, suspicious glyphs, implausible tokens, broken words, numeric corruption, line fragmentation, repeated page furniture, table irregularity, sparse pages, and heading-order problems. The output is designed for correlation studies and workflow gating experiments, not as ground-truth OCR accuracy.

**Current version:** 0.1.0
**Category:** review
**Domain:** general
**Status:** experimental
**Manifestations:** prompt
**Output contract:** [`schema.json`](schema.json)
**Contract scope:** repo-local OCR diagnostic contract

## Inputs

One document's OCR-derived Markdown or plain text. In Vandalizer, the companion workflow receives the text produced by the platform's normal PDF OCR path. The component does not inspect pixels, OCR-engine confidence values, bounding boxes, or the original PDF.

## Outputs

One JSON object with:

- input-size estimates and a context-coverage assessment;
- 12 signal records containing raw counts, denominators, rates, provisional thresholds, flags, confidence, and verbatim evidence examples; and
- a provisional risk index equal to the percentage of applicable signals that crossed their threshold.

`risk_index` is deliberately simple and inspectable. It is **not** a probability of failure, OCR accuracy, or a validated production gate. Raw signal rates are the primary analytical surface.

## Measurement limitations

Vandalizer's current workflow format exposes Prompt, Extraction, and Knowledge Base Query tasks, not a deterministic code node. Counts from this component are therefore labeled `llm_estimate`. A production gate should eventually replace or corroborate character/token counts with a deterministic analyzer while retaining this JSON contract.

The component can only see OCR text. It cannot detect visual blur, skew, rotation, clipped margins, or a missing page when those failures leave no textual trace. Legitimate tables, identifiers, math, multilingual text, and repeated headers can also resemble OCR corruption.

## Calibration plan

Use [`synthetic.workshop_ocr`](https://github.com/AI4RA/evaluation-data-sets/tree/main/synthetic/workshop_ocr) as the first calibration ladder:

1. Run all 15 PDFs (3 document types × clean plus 4 degradation tiers) through the same Vandalizer OCR path.
2. Run this component at least five times per OCR text and retain the median rate for every signal because the measurements are model-estimated.
3. Run the downstream extraction workflow and score field accuracy, numeric-field accuracy, missing-field rate, and hallucinated-field rate against `ground_truth.json`.
4. Measure Spearman correlation between each raw signal and each downstream error endpoint. Predefine a practical bad-run endpoint, such as field accuracy below 0.90, before examining threshold performance.
5. Report threshold precision/recall and uncertainty. With only 15 PDFs, treat results as calibration evidence, not general validation.
6. Externally check useful signals on `real.nsf_rfa_checklist_eval`, using paired clean-text versus dots.OCR extraction deltas and anchored-field accuracy. That corpus has no complete human ground truth, so describe non-anchored results as agreement or robustness, not accuracy.

## Contract scope

This is a prompt-library repo-local diagnostic schema. It does not extend or claim alignment to the shared AI4RA UDM.

## Triad integration

- **Evaluation datasets:** `synthetic.workshop_ocr` for ground-truth calibration; `real.nsf_rfa_checklist_eval` for paired external robustness checks.
- **Harness notes:** validate output against `schema.json`; store raw signal records alongside downstream extraction outcomes; use repeated measurements and median aggregation until deterministic counting is available.
- **Shared UDM relationship:** none.

## Manifestations

- [`prompt.md`](prompt.md) — canonical prompt.
- [`workflows/ocr-quality-signals`](https://github.com/AI4RA/prompt-library/tree/main/workflows/ocr-quality-signals) — uploadable Vandalizer manifestation.

## Evals

See [`evals/`](evals/) for the current calibration posture. No case is marked validated yet.

## Provenance

Authored 2026-08-08 after OCR quality emerged as a major determinant of downstream Vandalizer workflow quality. The design keeps measured signals separate from the downstream outcome so correlations can be tested rather than assumed.
