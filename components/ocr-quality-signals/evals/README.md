# Evals — ocr-quality-signals

This component is experimental and has **no validated golden cases yet**. That is intentional: the provisional thresholds must not be promoted to ground truth before they are tested against downstream extraction outcomes.

The first evaluation campaign should use `AI4RA/evaluation-data-sets` dataset `synthetic.workshop_ocr`:

- run all three document types across clean and tiers 1–4 through the production-equivalent Vandalizer OCR path;
- collect at least five component replicates per OCR text and aggregate each raw signal by median;
- score the downstream extractor against `ground_truth.json` for all fields and separately for numeric fields; and
- test raw-signal correlations before revising thresholds or the composite index.

Run artifacts belong in `AI4RA/evaluation-data-sets/evaluation_results/`, not here. Add a case under `cases/<case-slug>/` only after a human reviewer validates the expected output and records `validated_against_version`.
