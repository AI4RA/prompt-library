# OpenERA vs. Vandalizer — preliminary cross-system agreement

**Generated:** 2026-04-20T18:06:01Z  
**Vandalizer results loaded:** 20 distinct awards  
**Schema:** `/Users/barrierobison/Documents/Administration/AICoordination2026/AI4RAPromptLibrary/components/nsf-award-notice-extraction-udm/schema.json`

> **Not ground truth.** Vandalizer is a separate AI extraction system. Where the two systems agree we have high confidence the value is correct; where they disagree the document is ambiguous or one system is wrong. Treat this as a *second opinion*, not a truth signal.

## 1. Headline — overall scalar-field agreement

| run / mode | matched awards | scalar comparisons | overall agreement |
|---|---|---|---|
| `none` | 24 / 28 openera docs  (vandalizer covers 20) | 1900 | **97.3%** |
| `json_object` | 24 / 28 openera docs  (vandalizer covers 20) | 1952 | **98.2%** |
| `json_schema` | 24 / 28 openera docs  (vandalizer covers 20) | 2134 | **97.8%** |

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
| `start_date` | — | — | 100%  (19/19) |
| `end_date` | — | — | 100%  (19/19) |
| `total_intended_amount` | — | — | 100%  (111/111) |
| `expenditure_limitation` | — | — | — |
| `indirect_cost_base` | — | — | — |
| `fees` | — | 100%  (85/85) | 100%  (82/82) |
| `cfda_name` | 84%  (96/115) | 87%  (100/115) | 84%  (95/113) |
| `cfda_number` | 90%  (103/115) | 96%  (110/115) | 95%  (107/113) |
| `is_collaborative_research` | 91%  (109/120) | 92%  (110/120) | 91%  (107/118) |
| `award_title` | 96%  (110/115) | 96%  (110/115) | 92%  (108/117) |
| `funding_opportunity_number` | 96%  (110/115) | 99%  (114/115) | 98%  (111/113) |
| `award_id` | 100%  (120/120) | 100%  (120/120) | 100%  (118/118) |
| `award_number` | 100%  (120/120) | 100%  (120/120) | 100%  (118/118) |
| `sponsor_name` | 100%  (120/120) | 100%  (120/120) | 100%  (118/118) |
| `managing_division` | 100%  (120/120) | 100%  (120/120) | 100%  (118/118) |
| `award_instrument` | 100%  (120/120) | 100%  (120/120) | 100%  (118/118) |
| `is_research_and_development` | 100%  (115/115) | 100%  (115/115) | 100%  (113/113) |
| `funding_opportunity_title` | 100%  (115/115) | 100%  (115/115) | 100%  (113/113) |
| `amendment_number` | 100%  (120/120) | 100%  (120/120) | 100%  (118/118) |
| `award_date` | 100%  (92/92) | 100%  (77/77) | 100%  (81/81) |
| `amount_obligated_this_amendment` | 100%  (115/115) | 100%  (115/115) | 100%  (110/110) |
| `total_obligated_to_date` | 100%  (2/2) | 100%  (2/2) | 100%  (102/102) |
| `cost_share_approved_amount` | 100%  (106/106) | 100%  (88/88) | 100%  (52/52) |
| `indirect_cost_rate_percent` | 100%  (55/55) | 100%  (55/55) | 100%  (50/50) |

## 3. One-sided nulls (coverage asymmetry)

Cases where one system extracted a value and the other returned null. Useful to flag fields that one pipeline systematically skips.

| field | `none` OE-null / van-null | `json_object` OE-null / van-null | `json_schema` OE-null / van-null |
|---|---|---|---|
| `sponsor_award_number` | — | — | — |
| `award_status` | — | — | — |
| `proposal_number` | — | — | — |
| `amendment_type` | 0 / 120 | 0 / 120 | 0 / 118 |
| `amendment_date` | 0 / 20 | 0 / 9 | — |
| `amendment_description` | 0 / 120 | 0 / 120 | 0 / 118 |
| `award_received_date` | 0 / 20 | 0 / 20 | 0 / 20 |
| `start_date` | 120 / 0 | 120 / 0 | 99 / 0 |
| `end_date` | 120 / 0 | 120 / 0 | 99 / 0 |
| `total_intended_amount` | 115 / 0 | 115 / 0 | 2 / 5 |
| `expenditure_limitation` | — | — | 0 / 1 |
| `indirect_cost_base` | 0 / 114 | 0 / 113 | 0 / 103 |
| `fees` | 85 / 0 | 0 / 35 | 1 / 35 |
| `cfda_name` | 5 / 0 | 5 / 0 | 5 / 0 |
| `cfda_number` | 5 / 0 | 5 / 0 | 5 / 0 |
| `is_collaborative_research` | 0 / 0 | 0 / 0 | 0 / 0 |
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
| `award_date` | 28 / 0 | 43 / 0 | 37 / 0 |
| `amount_obligated_this_amendment` | 0 / 5 | 0 / 5 | 3 / 5 |
| `total_obligated_to_date` | 108 / 0 | 108 / 0 | 6 / 9 |
| `cost_share_approved_amount` | 4 / 10 | 22 / 7 | 56 / 8 |
| `indirect_cost_rate_percent` | 0 / 25 | 0 / 25 | 3 / 25 |

## 4. Disagreement examples — from best-agreeing run (`json_object`)

Up to 5 examples per field. When you see these, ask: was the document ambiguous, did Vandalizer extract the wrong thing, or did OpenERA?

### `cfda_name` — 87% agreement  (100/115)

| award | vandalizer | openera | vandalizer raw | openera raw |
|---|---|---|---|---|
| 2514552 | `geosciences (predominant source of funding for sefa reporting), 47.076 education and human resources` | `geosciences (predominant source of funding for sefa reporting)` | Geosciences (Predominant source of funding for SEFA reportin | Geosciences (Predominant source of funding for SEFA reportin |
| 2514552 | `geosciences (predominant source of funding for sefa reporting), 47.076 education and human resources` | `geosciences (predominant source of funding for sefa reporting)` | Geosciences (Predominant source of funding for SEFA reportin | Geosciences (Predominant source of funding for SEFA reportin |
| 2514552 | `geosciences (predominant source of funding for sefa reporting), 47.076 education and human resources` | `geosciences (predominant source of funding for sefa reporting); education and human resources` | Geosciences (Predominant source of funding for SEFA reportin | Geosciences (Predominant source of funding for SEFA reportin |
| 2514552 | `geosciences (predominant source of funding for sefa reporting), 47.076 education and human resources` | `geosciences (predominant source of funding for sefa reporting)` | Geosciences (Predominant source of funding for SEFA reportin | Geosciences (Predominant source of funding for SEFA reportin |
| 2514552 | `geosciences (predominant source of funding for sefa reporting), 47.076 education and human resources` | `geosciences (predominant source of funding for sefa reporting)` | Geosciences (Predominant source of funding for SEFA reportin | Geosciences (Predominant source of funding for SEFA reportin |

### `is_collaborative_research` — 92% agreement  (110/120)

| award | vandalizer | openera | vandalizer raw | openera raw |
|---|---|---|---|---|
| 2531886 | `False` | `True` | False | True |
| 2531886 | `False` | `True` | False | True |
| 2531886 | `False` | `True` | False | True |
| 2531886 | `False` | `True` | False | True |
| 2531886 | `False` | `True` | False | True |

### `award_title` — 96% agreement  (110/115)

| award | vandalizer | openera | vandalizer raw | openera raw |
|---|---|---|---|---|
| 2511003 | `equipment: mri: track 1 acquisition of element aviti system to enable multi-omics research and research training.` | `equipment: mri: track 1 acquisition of element a viti system to enable multi-omics research and research training` | Equipment: MRI: Track 1 Acquisition of Element AVITI System  | Equipment: MRI: Track 1 Acquisition of Element A VITI System |
| 2511003 | `equipment: mri: track 1 acquisition of element aviti system to enable multi-omics research and research training.` | `equipment: mri: track 1 acquisition of element a viti system to enable multi-omics research and research training` | Equipment: MRI: Track 1 Acquisition of Element AVITI System  | Equipment: MRI: Track 1 Acquisition of Element A VITI System |
| 2511003 | `equipment: mri: track 1 acquisition of element aviti system to enable multi-omics research and research training.` | `equipment: mri: track 1 acquisition of element a viti system to enable multi-omics research and research training` | Equipment: MRI: Track 1 Acquisition of Element AVITI System  | Equipment: MRI: Track 1 Acquisition of Element A VITI System |
| 2511003 | `equipment: mri: track 1 acquisition of element aviti system to enable multi-omics research and research training.` | `equipment: mri: track 1 acquisition of element a viti system to enable multi-omics research and research training` | Equipment: MRI: Track 1 Acquisition of Element AVITI System  | Equipment: MRI: Track 1 Acquisition of Element A VITI System |
| 2511003 | `equipment: mri: track 1 acquisition of element aviti system to enable multi-omics research and research training.` | `equipment: mri: track 1 acquisition of element a viti system to enable multi-omics research and research training` | Equipment: MRI: Track 1 Acquisition of Element AVITI System  | Equipment: MRI: Track 1 Acquisition of Element A VITI System |

### `cfda_number` — 96% agreement  (110/115)

| award | vandalizer | openera | vandalizer raw | openera raw |
|---|---|---|---|---|
| 2514552 | `47.050` | `47.050; 47.076` | 47.050 | 47.050; 47.076 |
| 2514552 | `47.050` | `47.050, 47.076` | 47.050 | 47.050, 47.076 |
| 2514552 | `47.050` | `47.050; 47.076` | 47.050 | 47.050; 47.076 |
| 2514552 | `47.050` | `47.050; 47.076` | 47.050 | 47.050; 47.076 |
| 2314616 | `47.074` | `47.074, 47.049, 47.083` | 47.074 | 47.074, 47.049, 47.083 |

## Methodology

- **Matching.** OpenERA PDFs are matched to Vandalizer results by the tuple `(award_number, amendment_number)`, majority-voted across replicates. This matters for amendment series: three PDFs may share an award_number but represent the base award, Mod 1, and Mod 2 respectively; matching on award_number alone would falsely align all three to one Vandalizer extraction.
- **Scope.** Top-level scalar fields only. Nested objects (`recipient_organization`, `current_budget_period`) and arrays (`project_personnel`, `budget_categories`, etc.) are out of scope for this pass.
- **Normalization.** Currency (`$584,845` → `584845`), percentages (`50.0000%` → `50.0`), US dates (`08/18/2025` → `2025-08-18`) are coerced. `"N/A"`, `""`, and `null` are all treated as null.
- **Denominator.** Each field's `agreement_pct` uses only replicates where *both* systems produced a non-null value — one-sided nulls are surfaced separately in §3 rather than penalizing agreement.

**Script:** `scripts/compare_to_vandalizer.py`