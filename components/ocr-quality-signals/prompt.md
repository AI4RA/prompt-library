---
name: ocr-quality-signals
version: "0.1.0"
category: review
domain: general
status: experimental
tags:
  - ocr
  - document-quality
  - anomaly-detection
  - quantitative-signals
  - workflow-gating
audience:
  - document-intelligence-teams
  - workflow-designers
  - evaluation-engineers
owner: ui-insight
created: 2026-08-08
updated: 2026-08-08
---

# OCR Quality Signals — Prompt

> **Purpose:** Measure observable properties of OCR-derived text that may correlate with downstream extraction failures.
> **Expected input:** OCR markdown or plain text from one document.
> **Expected output:** One schema-conformant JSON object containing raw signal estimates, provisional flags, and an explicitly non-validated risk index.

---

## Prompt

You are auditing OCR-DERIVED TEXT, not the original PDF image. Produce
quantitative, reproducible-as-possible signals that can later be tested for
correlation with downstream workflow errors. Do not repair the text, infer
missing source content, or call this an OCR accuracy score.

All measurements are LLM estimates. Analyze all input available in context. If
the context may be truncated, say so in `coverage_assessment`. Use the counting
rules below consistently:

- `character_count_estimate`: non-whitespace Unicode code points.
- `word_count_estimate`: whitespace-delimited tokens after ignoring standalone
  Markdown markers.
- `nonempty_line_count_estimate`: trimmed lines containing visible content.
- `numeric_token_count_estimate`: word tokens containing at least one digit.
- `explicit_page_count`: pages only when the text has explicit page boundaries
  or unambiguous page-number sequences; otherwise null.

Emit exactly these 12 signals, in this order. For every signal, report the
observed count, denominator count, rate (`observed_count / denominator_count`),
the fixed provisional threshold below, whether the threshold is met or
exceeded, measurement confidence, up to three short VERBATIM examples, and a
short note when interpretation needs care.

1. `replacement_or_mojibake_character_rate` — U+FFFD replacement characters or
   recognizable encoding damage such as `â€™`, `â€“`, or `Ã©`; denominator:
   characters; threshold 0.0005.
2. `suspicious_glyph_character_rate` — isolated glyphs apparently substituted
   for letters or punctuation; exclude legitimate math, currency, scientific,
   and non-English characters; denominator: characters; threshold 0.002.
3. `single_character_alpha_token_rate` — isolated one-letter alphabetic tokens;
   exclude legitimate `a`/`I`, initials, outline labels, variables, and table
   column labels; denominator: words; threshold 0.02.
4. `implausible_mixed_alphanumeric_token_rate` — word-like tokens with unlikely
   letter/digit mixing; exclude identifiers, award numbers, dates, URLs, emails,
   chemical notation, and valid codes; denominator: words; threshold 0.01.
5. `broken_word_line_end_rate` — words split unnaturally across line boundaries;
   exclude ordinary end-of-line hyphenation when the parts form a clear word;
   denominator: words; threshold 0.005.
6. `garbled_word_token_rate` — uninterpretable word-like tokens that are not
   names, acronyms, codes, formulas, or non-English terms; denominator: words;
   threshold 0.01.
7. `malformed_numeric_token_rate` — digit-bearing tokens with suspicious OCR
   substitutions, spacing, decimal/grouping punctuation, or lost signs; exclude
   valid dates, IDs, telephone numbers, citations, and ranges; denominator:
   numeric tokens; threshold 0.03.
8. `very_short_nonempty_line_rate` — nonempty lines with three or fewer visible
   characters after Markdown markers; denominator: nonempty lines; threshold
   0.20.
9. `duplicate_nonempty_line_rate` — repeated normalized header, footer, or body
   lines after the first occurrence; denominator: nonempty lines; threshold
   0.08.
10. `table_row_irregularity_rate` — candidate table rows whose apparent column
    count or alignment is inconsistent with neighboring rows; denominator:
    candidate table rows; threshold 0.15.
11. `low_text_page_rate` — explicit pages with fewer than 50 word tokens;
    denominator: explicit pages; threshold 0.10.
12. `heading_sequence_anomaly_rate` — Markdown headings or recognizable numbered
    section headings that skip levels, appear out of order, or merge with body
    text; denominator: observed headings; threshold 0.10.

Set `applicable` false, `denominator_count` to 0, `rate` to null, and `flagged`
false when a denominator cannot be observed reliably. Exclude non-applicable
signals from the summary calculation. Otherwise round each rate to six decimal
places and make `flagged` exactly equal to `rate >= provisional_threshold`.

Compute:

- `applicable_signal_count`: count of signals where `applicable` is true.
- `flagged_signal_count`: count of applicable signals where `flagged` is true.
- `risk_index`: `round(100 * flagged_signal_count / applicable_signal_count)`;
  use 0 only when no signal is applicable.
- `risk_band`: `low` for 0–19, `watch` for 20–39, `elevated` for 40–59,
  and `high` for 60–100.
- `review_recommendation`: `proceed_with_spot_check` for low,
  `spot_check_critical_fields` for watch, `rerun_ocr_or_human_review` for
  elevated, and `block_automation_pending_review` for high.
- `dominant_signals`: up to five flagged signal IDs, highest rate-to-threshold
  multiple first.

The `risk_index` is provisional flag density, not a probability, confidence,
OCR accuracy, or validated pass/fail threshold. Always include caveats covering
LLM counting error, lack of access to the source image, and possible false
positives from legitimate tables, identifiers, math, multilingual text, or
repeated page furniture.

Emit exactly one JSON object conforming to `schema.json`. No preamble, Markdown
fences, or closing commentary.

---

## Quality Standards

- Preserve evidence examples verbatim; never silently correct suspected OCR.
- Keep raw counts and denominators so later analysis can ignore the provisional index.
- Make every rate and summary value arithmetically coherent with its reported inputs.
- Mark unobservable page, table, or heading signals non-applicable instead of guessing.
- Never describe the heuristic as accuracy, confidence, or a validated production gate.
