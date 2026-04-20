# OpenERA vs. Vandalizer — preliminary cross-system agreement

**Generated:** 2026-04-20T17:58:28Z  
**Vandalizer results loaded:** 15 distinct awards  
**Schema:** `/Users/barrierobison/Documents/Administration/AICoordination2026/AI4RAPromptLibrary/components/nsf-award-notice-extraction-udm/schema.json`

> **Not ground truth.** Vandalizer is a separate AI extraction system. Where the two systems agree we have high confidence the value is correct; where they disagree the document is ambiguous or one system is wrong. Treat this as a *second opinion*, not a truth signal.

## 1. Headline — overall scalar-field agreement

| run / mode | matched awards | scalar comparisons | overall agreement |
|---|---|---|---|
| `none` | 19 / 28 openera docs  (vandalizer covers 15) | 1492 | **97.3%** |
| `json_object` | 19 / 28 openera docs  (vandalizer covers 15) | 1528 | **98.0%** |
| `json_schema` | 19 / 28 openera docs  (vandalizer covers 15) | 1707 | **97.6%** |

## 2. Per-field agreement across modes

Scalar fields where both systems provided a value. Lower rows = more disagreement. Columns show **agree / compared** per mode.

| field | `none` | `json_object` | `json_schema` |
|---|---|---|---|
| `sponsor_award_number` | — | — | — |
| `award_status` | — | — | — |
| `proposal_number` | — | — | — |
| `amendment_type` | — | — | — |
| `amendment_date` | — | — | — |
| `amendment_description` | — | — | — |
| `award_received_date` | — | — | — |
| `start_date` | — | — | 100%  (18/18) |
| `end_date` | — | — | 100%  (18/18) |
| `total_intended_amount` | — | — | 100%  (88/88) |
| `expenditure_limitation` | — | — | — |
| `indirect_cost_base` | — | — | — |
| `fees` | — | 100%  (60/60) | 100%  (59/59) |
| `cfda_name` | 86%  (77/90) | 89%  (80/90) | 86%  (77/90) |
| `is_collaborative_research` | 88%  (84/95) | 90%  (85/95) | 88%  (84/95) |
| `cfda_number` | 91%  (82/90) | 94%  (85/90) | 93%  (84/90) |
| `award_title` | 94%  (85/90) | 94%  (85/90) | 90%  (85/94) |
| `funding_opportunity_number` | 97%  (87/90) | 99%  (89/90) | 98%  (88/90) |
| `award_id` | 100%  (95/95) | 100%  (95/95) | 100%  (95/95) |
| `award_number` | 100%  (95/95) | 100%  (95/95) | 100%  (95/95) |
| `sponsor_name` | 100%  (95/95) | 100%  (95/95) | 100%  (95/95) |
| `managing_division` | 100%  (95/95) | 100%  (95/95) | 100%  (95/95) |
| `award_instrument` | 100%  (95/95) | 100%  (95/95) | 100%  (95/95) |
| `is_research_and_development` | 100%  (90/90) | 100%  (90/90) | 100%  (90/90) |
| `funding_opportunity_title` | 100%  (90/90) | 100%  (90/90) | 100%  (90/90) |
| `amendment_number` | 100%  (95/95) | 100%  (95/95) | 100%  (95/95) |
| `award_date` | 100%  (73/73) | 100%  (64/64) | 100%  (65/65) |
| `amount_obligated_this_amendment` | 100%  (90/90) | 100%  (90/90) | 100%  (87/87) |
| `total_obligated_to_date` | 100%  (2/2) | 100%  (2/2) | 100%  (84/84) |
| `cost_share_approved_amount` | 100%  (87/87) | 100%  (72/72) | 100%  (45/45) |
| `indirect_cost_rate_percent` | 100%  (35/35) | 100%  (35/35) | 100%  (34/34) |

## 3. One-sided nulls (coverage asymmetry)

Cases where one system extracted a value and the other returned null. Useful to flag fields that one pipeline systematically skips.

| field | `none` OE-null / van-null | `json_object` OE-null / van-null | `json_schema` OE-null / van-null |
|---|---|---|---|
| `sponsor_award_number` | — | — | — |
| `award_status` | — | — | — |
| `proposal_number` | — | — | — |
| `amendment_type` | 0 / 95 | 0 / 95 | 0 / 95 |
| `amendment_date` | 0 / 20 | 0 / 6 | — |
| `amendment_description` | 0 / 95 | 0 / 95 | 0 / 95 |
| `award_received_date` | 0 / 20 | 0 / 20 | 0 / 20 |
| `start_date` | 95 / 0 | 95 / 0 | 77 / 0 |
| `end_date` | 95 / 0 | 95 / 0 | 77 / 0 |
| `total_intended_amount` | 90 / 0 | 90 / 0 | 2 / 5 |
| `expenditure_limitation` | — | — | — |
| `indirect_cost_base` | 0 / 89 | 0 / 89 | 0 / 82 |
| `fees` | 60 / 0 | 0 / 35 | 1 / 35 |
| `cfda_name` | 5 / 0 | 5 / 0 | 5 / 0 |
| `is_collaborative_research` | 0 / 0 | 0 / 0 | 0 / 0 |
| `cfda_number` | 5 / 0 | 5 / 0 | 5 / 0 |
| `award_title` | 5 / 0 | 5 / 0 | 1 / 0 |
| `funding_opportunity_number` | 5 / 0 | 5 / 0 | 5 / 0 |
| `award_id` | 0 / 0 | 0 / 0 | 0 / 0 |
| `award_number` | 0 / 0 | 0 / 0 | 0 / 0 |
| `sponsor_name` | 0 / 0 | 0 / 0 | 0 / 0 |
| `managing_division` | 0 / 0 | 0 / 0 | 0 / 0 |
| `award_instrument` | 0 / 0 | 0 / 0 | 0 / 0 |
| `is_research_and_development` | 5 / 0 | 5 / 0 | 5 / 0 |
| `funding_opportunity_title` | 5 / 0 | 5 / 0 | 5 / 0 |
| `amendment_number` | 0 / 0 | 0 / 0 | 0 / 0 |
| `award_date` | 22 / 0 | 31 / 0 | 30 / 0 |
| `amount_obligated_this_amendment` | 0 / 5 | 0 / 5 | 3 / 5 |
| `total_obligated_to_date` | 88 / 0 | 88 / 0 | 6 / 4 |
| `cost_share_approved_amount` | 3 / 5 | 18 / 3 | 45 / 5 |
| `indirect_cost_rate_percent` | 0 / 25 | 0 / 25 | 1 / 25 |

## 4. Disagreement examples — from best-agreeing run (`json_object`)

Up to 5 examples per field. When you see these, ask: was the document ambiguous, did Vandalizer extract the wrong thing, or did OpenERA?

### `cfda_name` — 89% agreement  (80/90)

| award | vandalizer | openera | vandalizer raw | openera raw |
|---|---|---|---|---|
| 2514552 | `geosciences (predominant source of funding for sefa reporting), 47.076 education and human resources` | `geosciences (predominant source of funding for sefa reporting)` | Geosciences (Predominant source of funding for SEFA reportin | Geosciences (Predominant source of funding for SEFA reportin |
| 2514552 | `geosciences (predominant source of funding for sefa reporting), 47.076 education and human resources` | `geosciences (predominant source of funding for sefa reporting)` | Geosciences (Predominant source of funding for SEFA reportin | Geosciences (Predominant source of funding for SEFA reportin |
| 2514552 | `geosciences (predominant source of funding for sefa reporting), 47.076 education and human resources` | `geosciences (predominant source of funding for sefa reporting); education and human resources` | Geosciences (Predominant source of funding for SEFA reportin | Geosciences (Predominant source of funding for SEFA reportin |
| 2514552 | `geosciences (predominant source of funding for sefa reporting), 47.076 education and human resources` | `geosciences (predominant source of funding for sefa reporting)` | Geosciences (Predominant source of funding for SEFA reportin | Geosciences (Predominant source of funding for SEFA reportin |
| 2514552 | `geosciences (predominant source of funding for sefa reporting), 47.076 education and human resources` | `geosciences (predominant source of funding for sefa reporting)` | Geosciences (Predominant source of funding for SEFA reportin | Geosciences (Predominant source of funding for SEFA reportin |

### `is_collaborative_research` — 90% agreement  (85/95)

| award | vandalizer | openera | vandalizer raw | openera raw |
|---|---|---|---|---|
| 2531886 | `False` | `True` | False | True |
| 2531886 | `False` | `True` | False | True |
| 2531886 | `False` | `True` | False | True |
| 2531886 | `False` | `True` | False | True |
| 2531886 | `False` | `True` | False | True |

### `award_title` — 94% agreement  (85/90)

| award | vandalizer | openera | vandalizer raw | openera raw |
|---|---|---|---|---|
| 2511003 | `equipment: mri: track 1 acquisition of element aviti system to enable multi-omics research and research training.` | `equipment: mri: track 1 acquisition of element a viti system to enable multi-omics research and research training` | Equipment: MRI: Track 1 Acquisition of Element AVITI System  | Equipment: MRI: Track 1 Acquisition of Element A VITI System |
| 2511003 | `equipment: mri: track 1 acquisition of element aviti system to enable multi-omics research and research training.` | `equipment: mri: track 1 acquisition of element a viti system to enable multi-omics research and research training` | Equipment: MRI: Track 1 Acquisition of Element AVITI System  | Equipment: MRI: Track 1 Acquisition of Element A VITI System |
| 2511003 | `equipment: mri: track 1 acquisition of element aviti system to enable multi-omics research and research training.` | `equipment: mri: track 1 acquisition of element a viti system to enable multi-omics research and research training` | Equipment: MRI: Track 1 Acquisition of Element AVITI System  | Equipment: MRI: Track 1 Acquisition of Element A VITI System |
| 2511003 | `equipment: mri: track 1 acquisition of element aviti system to enable multi-omics research and research training.` | `equipment: mri: track 1 acquisition of element a viti system to enable multi-omics research and research training` | Equipment: MRI: Track 1 Acquisition of Element AVITI System  | Equipment: MRI: Track 1 Acquisition of Element A VITI System |
| 2511003 | `equipment: mri: track 1 acquisition of element aviti system to enable multi-omics research and research training.` | `equipment: mri: track 1 acquisition of element a viti system to enable multi-omics research and research training` | Equipment: MRI: Track 1 Acquisition of Element AVITI System  | Equipment: MRI: Track 1 Acquisition of Element A VITI System |

### `cfda_number` — 94% agreement  (85/90)

| award | vandalizer | openera | vandalizer raw | openera raw |
|---|---|---|---|---|
| 2514552 | `47.050` | `47.050; 47.076` | 47.050 | 47.050; 47.076 |
| 2514552 | `47.050` | `47.050, 47.076` | 47.050 | 47.050, 47.076 |
| 2514552 | `47.050` | `47.050; 47.076` | 47.050 | 47.050; 47.076 |
| 2514552 | `47.050` | `47.050; 47.076` | 47.050 | 47.050; 47.076 |
| 2314616 | `47.074` | `47.074, 47.049, 47.083` | 47.074 | 47.074, 47.049, 47.083 |

### `funding_opportunity_number` — 99% agreement  (89/90)

| award | vandalizer | openera | vandalizer raw | openera raw |
|---|---|---|---|---|
| 2527135 | `nsf 25-509` | `25-509` | NSF 25-509 | 25-509 |

## Methodology

- **Matching.** OpenERA PDFs are matched to Vandalizer results by the tuple `(award_number, amendment_number)`, majority-voted across replicates. This matters for amendment series: three PDFs may share an award_number but represent the base award, Mod 1, and Mod 2 respectively; matching on award_number alone would falsely align all three to one Vandalizer extraction.
- **Scope.** Top-level scalar fields only. Nested objects (`recipient_organization`, `current_budget_period`) and arrays (`project_personnel`, `budget_categories`, etc.) are out of scope for this pass.
- **Normalization.** Currency (`$584,845` → `584845`), percentages (`50.0000%` → `50.0`), US dates (`08/18/2025` → `2025-08-18`) are coerced. `"N/A"`, `""`, and `null` are all treated as null.
- **Denominator.** Each field's `agreement_pct` uses only replicates where *both* systems produced a non-null value — one-sided nulls are surfaced separately in §3 rather than penalizing agreement.

**Script:** `scripts/compare_to_vandalizer.py`