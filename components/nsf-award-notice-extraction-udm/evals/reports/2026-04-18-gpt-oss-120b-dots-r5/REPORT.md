# Evaluation run — `2026-04-18-gpt-oss-120b-dots-r5`

**Date:** 2026-04-18 22:31 UTC  
**Model:** `openai/gpt-oss-120b`  
**OCR:** `mindrouter` (Mindrouter `/v1/ocrmd`, dots.OCR backend)  
**Prompt:** `prompt.md` — sha256 `f828e83e0e8c`  
**Temperature:** 0.1  
**Replicates per doc:** 5  
**Documents:** 28

## 1. Run-level headline

- **Success rate:** 140/140 (100.0%) — 0 API errors, 0 JSON-parse errors.
- **OCR latency:** p50 19.1s, p95 22.6s (min 10.0s, max 29.3s).
- **Chat latency:** p50 66.9s, p95 89.1s (min 18.0s, max 126.6s).
- **Prompt tokens:** p50 5446, p95 6074 (min 4465, max 6994).
- **Completion tokens:** p50 7821, p95 9464, max **14073** (cap: 16384). 1 replicates over 80% of cap, 0 over 95%.

![completion tokens](charts/completion_tokens.png)

## 2. Structural validity (JSON Schema)

Validated every replicate against [`../../schema.json`](../../schema.json) with `jsonschema` (Draft 2020-12).

- **Strict pass rate:** 0/140 (0.0%)
- **Pass rate ignoring top-level extra keys:** 78/140 (55.7%) — this isolates structural/type errors from naming drift.

**Top-level naming drift — keys the model emits that the schema does not declare:**

| extra key emitted | occurrences | likely schema counterpart |
|---|---|---|
| `total_intended_award_amount` | 135 | `total_intended_amount` |
| `total_amount_obligated_to_date` | 126 | `total_obligated_to_date` |
| `total_approved_cost_share_or_matching_amount` | 113 | — |
| `period_of_performance_end` | 50 | — |
| `period_of_performance_start` | 50 | `start_date` |
| `award_period_end_date` | 35 | `end_date` |
| `award_period_start_date` | 35 | `start_date` |
| `award_period_end` | 29 | — |
| `award_period_start` | 29 | `start_date` |
| `period_of_performance_end_date` | 12 | `end_date` |
| `period_of_performance_start_date` | 12 | `start_date` |
| `award_period_of_performance_end_date` | 6 | `end_date` |
| `award_period_of_performance_start_date` | 6 | `start_date` |
| `award_period_of_performance_end` | 5 | — |
| `award_period_of_performance_start` | 5 | `start_date` |
| `total_award_amount` | 5 | — |
| `total_approved_cost_share` | 4 | — |
| `total_approved_cost_share_amount` | 4 | — |
| `award_end_date` | 2 | `end_date` |
| `award_start_date` | 2 | `start_date` |
| `total_cost_share_approved_amount` | 2 | `cost_share_approved_amount` |


**Required/declared top-level keys absent from outputs:**

| schema key missing | # replicates missing it (of 140) |
|---|---|
| `proposal_number` | 140 |
| `end_date` | 140 |
| `total_intended_amount` | 140 |
| `award_status` | 140 |
| `start_date` | 140 |
| `sponsor_award_number` | 140 |
| `total_obligated_to_date` | 133 |
| `amendment_date` | 115 |
| `award_date` | 32 |
| `expenditure_limitation` | 17 |
| `cost_share_approved_amount` | 5 |


**Top validation errors (error-key × occurrences):**

| rule @ pointer | count |
|---|---|
| `<root> :: additionalProperties` | 140 |
| `linked_awards/0 :: required` | 34 |
| `linked_awards/1 :: required` | 18 |
| `special_conditions/2/category :: enum` | 8 |
| `budget_categories/25/label :: minLength` | 8 |
| `budget_categories/26/label :: minLength` | 6 |
| `special_conditions/1/category :: enum` | 5 |
| `linked_awards/0 :: additionalProperties` | 5 |
| `linked_awards/1 :: additionalProperties` | 5 |
| `award_title :: type` | 5 |
| `current_budget_period/end_date :: type` | 5 |
| `current_budget_period/start_date :: type` | 5 |
| `expenditure_limitation :: type` | 5 |
| `special_conditions/4/category :: enum` | 4 |
| `special_conditions/5/category :: enum` | 2 |

**Documents with any schema-invalid replicate:**

| document | # invalid / 5 |
|---|---|
| award_01 | 5 |
| award_02 | 5 |
| award_03 | 5 |
| award_04 | 5 |
| award_05 | 5 |
| award_06 | 5 |
| award_07 | 5 |
| award_08 | 5 |
| award_09 | 5 |
| award_10 | 5 |
| award_11 | 5 |
| award_12 | 5 |
| award_13 | 5 |
| award_14 | 5 |
| award_15 | 5 |
| award_16 | 5 |
| award_17 | 5 |
| award_18 | 5 |
| award_19 | 5 |
| award_20 | 5 |
| award_21 | 5 |
| award_22 | 5 |
| award_23 | 5 |
| award_24 | 5 |
| award_25 | 5 |
| award_26 | 5 |
| award_27 | 5 |
| award_28 | 5 |

## 3. Within-doc consistency (5 replicates per doc)

![consistency heatmap](charts/consistency_heatmap.png)

![per-field agreement](charts/field_agreement.png)

### 3a. Per-field agreement rollup (top 15 worst)

| field | docs probed | % full agreement | 2 distinct | ≥3 distinct |
|---|---|---|---|---|
| `expenditure_limitation` | 28 | **36%** | 18 | 0 |
| `amendment_date` | 28 | **46%** | 15 | 0 |
| `award_date` | 28 | **50%** | 14 | 0 |
| `cfda_name` | 28 | **82%** | 1 | 4 |
| `indirect_cost_base` | 28 | **82%** | 4 | 1 |
| `cfda_number` | 28 | **82%** | 5 | 0 |
| `cost_share_approved_amount` | 28 | **82%** | 5 | 0 |
| `funding_opportunity_number` | 28 | **89%** | 3 | 0 |
| `total_obligated_to_date` | 28 | **89%** | 3 | 0 |
| `is_collaborative_research` | 28 | **93%** | 2 | 0 |
| `indirect_cost_rate_percent` | 28 | **96%** | 1 | 0 |
| `award_id` | 28 | **100%** | 0 | 0 |
| `award_number` | 28 | **100%** | 0 | 0 |
| `sponsor_award_number` | 28 | **100%** | 0 | 0 |
| `award_title` | 28 | **100%** | 0 | 0 |

### 3b. Worst docs (most fields disagreeing)

| document | disagreeing / probed | % |
|---|---|---|
| award_19 | 6 / 40 | 15% |
| award_02 | 5 / 40 | 12% |
| award_06 | 4 / 40 | 10% |
| award_10 | 4 / 40 | 10% |
| award_16 | 4 / 40 | 10% |
| award_18 | 4 / 40 | 10% |
| award_23 | 4 / 40 | 10% |
| award_05 | 3 / 40 | 8% |
| award_09 | 3 / 40 | 8% |
| award_11 | 3 / 40 | 8% |

### 3c. Array-length stability across replicates

| array | mean CV | max CV | % docs stable (CV=0) | worst docs |
|---|---|---|---|---|
| `special_conditions` | 0.181 | 1.225 | 25% | award_27 ([1, 0, 0, 0, 1]); award_19 ([0, 3, 3, 3, 3]); award_06 ([2, 1, 2, 3, 3]) |
| `terms_and_conditions` | 0.140 | 0.298 | 11% | award_21 ([2, 4, 2, 3, 4]); award_10 ([2, 2, 3, 4, 3]); award_20 ([3, 3, 3, 4, 2]) |
| `budget_categories` | 0.137 | 0.243 | 7% | award_07 ([48, 30, 30, 29, 48]); award_05 ([27, 48, 48, 31, 48]); award_02 ([30, 48, 48, 48, 30]) |
| `linked_awards` | 0.054 | 0.500 | 89% | award_09 ([0, 1, 1, 1, 1]); award_12 ([0, 1, 1, 1, 1]); award_18 ([0, 1, 1, 1, 1]) |
| `project_personnel` | 0.000 | 0.000 | 100% | — |
| `sponsor_contacts` | 0.000 | 0.000 | 100% | — |
| `subawards` | 0.000 | 0.000 | 100% | — |

## 4. Field coverage

![coverage bar chart](charts/coverage.png)

### 4a. Scalar fields — least-populated first

| field | % non-null | n / total |
|---|---|---|
| `sponsor_award_number` | 0% | 0 / 140 |
| `award_status` | 0% | 0 / 140 |
| `proposal_number` | 0% | 0 / 140 |
| `start_date` | 0% | 0 / 140 |
| `end_date` | 0% | 0 / 140 |
| `total_intended_amount` | 0% | 0 / 140 |
| `total_obligated_to_date` | 5% | 7 / 140 |
| `award_received_date` | 14% | 20 / 140 |
| `amendment_date` | 18% | 25 / 140 |
| `expenditure_limitation` | 54% | 75 / 140 |
| `indirect_cost_rate_percent` | 62% | 87 / 140 |
| `award_date` | 77% | 108 / 140 |
| `indirect_cost_base` | 92% | 129 / 140 |
| `award_title` | 96% | 135 / 140 |
| `is_research_and_development` | 96% | 135 / 140 |

### 4b. Array fields — least-populated first

| array | % non-empty | n / total |
|---|---|---|
| `subawards` | 4% | 5 / 140 |
| `linked_awards` | 26% | 37 / 140 |
| `special_conditions` | 94% | 131 / 140 |
| `budget_categories` | 96% | 135 / 140 |
| `project_personnel` | 100% | 140 / 140 |
| `sponsor_contacts` | 100% | 140 / 140 |
| `terms_and_conditions` | 100% | 140 / 140 |

## Reproduction

```bash
python scripts/extract_only.py \
  --pdf-dir <local-pdf-dir> \
  --prompt components/nsf-award-notice-extraction-udm/prompt.md \
  --model openai/gpt-oss-120b \
  --ocr mindrouter \
  --replicates 5 \
  --max-tokens 16384 \
  --run-name 2026-04-18-gpt-oss-120b-dots-r5
```
