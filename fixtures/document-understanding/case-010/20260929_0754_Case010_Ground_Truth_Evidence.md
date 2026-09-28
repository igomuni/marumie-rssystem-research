# Case-010 MHLW Ground Truth Evidence

Status: **FROZEN from fresh direct visual source evidence**

Created: 2026-09-29 07:54 Asia/Tokyo
Branch: `research/case-010-mhlw-source-survey`

## 1. Purpose and frozen selection reference

This document independently transcribes Ground Truth for the one physical row already frozen in `20260929_0711_Case010_Selection_Record.md` at commit `4b98acea75c4abad9b4086ecd76a3c3261b1bab5`. Selection was not repeated or changed.

Freeze chain: Source Survey `cc5115b80076159dc58570fb9fa4e7d7267a14f5` → Selection Protocol `2f910f218a35a776d57d32c30f10322b0b945209` → Selection Record `4b98acea75c4abad9b4086ecd76a3c3261b1bab5`.

## 2. Canonical source identity and fresh-render method

| field | value |
| --- | --- |
| source ID | `mhlw-fy2024-general-account-expenditure-request-summary-detail` |
| official URL | `https://www.mhlw.go.jp/wp/yosan/yosan/24syokan/dl/05-1b-01.pdf` |
| SHA-256 | `09d26048b20d1b1dac7aab236ab6da452e482a12f4d97a8f6c28ec7c420eb192` |
| integrity | recomputed against the locked raw PDF before rendering; matches source lock and registry |
| render | fresh `pdftoppm` physical PDF page 21 (`pdfPageIndex 20`) at 600 dpi |

All character and numeric transcription below was read directly from that fresh render. No OCR, text extraction, PDF text/object inspection as a reading substitute, benchmark output, MOF/RS data, production data, or expected arithmetic result was used.

## 3. Locator re-verification before amount transcription

Before reading the amount cells, the fresh render matched the frozen Selection Record on: `pdfPageIndex 20`; printed page `厚（本） 13`; organization `010 厚生労働本省`; item `001 厚生労働本省共通費`; request number `①`; expense code `05-95`; and the two-line label below. The row is in the continuous main standard-ledger grid, aligned to the request-number, expense-code, and amount columns. It is not the embedded remarks-side material.

## 4. Identity and expense name: raw visual forms → normalized

| field | raw visual form | normalized form |
| --- | --- | --- |
| organization | `010 厚生労働本省` | `010 厚生労働本省` |
| item | `001 厚生労働本省共通費` | `001 厚生労働本省共通費` |
| request number | `①` | `1` |
| expense code | `05-95` | `05-95` |
| expense label line 1 | `厚生労働本省一般行政に` | — |
| expense label line 2 | `必要な経費` | — |
| expense label | — | `厚生労働本省一般行政に必要な経費` |

Label normalization removes the visual line wrap only; it inserts no space or other character.

## 5. Independent amount transcription

The three main-ledger amount cells were transcribed independently, in the listed order, before arithmetic validation.

| field | raw visual string | normalized integer |
| --- | --- | ---: |
| previous budget | `95,219,981` | 95219981 |
| FY2024 request | `107,468,512` | 107468512 |
| delta | `12,248,531` | 12248531 |

## 6. Delta sign evidence

The selected-row delta cell visibly shows `12,248,531` without a preceding `△`, minus, or other negative marker. The normalized signed delta is therefore positive `12248531`. This glyph-based sign determination was made before arithmetic validation.

## 7. Unit evidence and scope

| field | value |
| --- | --- |
| raw source text | `（単位:千円）` |
| normalized unit | `千円` |
| locator | `pdfPageIndex 20`, top-right main-detail section opening |
| scope | confirmed main standard-ledger rows in the detail section; not a unit inherited from the embedded remarks-side material |

## 8. Remarks state

The selected row's own remarks cell is visually empty at the selected main-row height. The populated explanatory/breakdown material lower in the remarks region belongs to a deeper, non-target embedded structure and was not assigned to the selected row. Ground Truth remarks is therefore the empty string.

## 9. Arithmetic validation

Only after independently transcribing all three amount fields and the delta sign:

`107468512 - 95219981 = 12248531`

Result: **PASS**. This calculation validated the already transcribed fields; it supplied or altered none of them.

## 10. Ambiguities and embedded-structure separation

No character, digit, or sign ambiguity remained at 600 dpi. No crop, OCR, text extraction, or arithmetic-led correction was needed. The selected row was confirmed as a main-grid row; no number, unit, or remarks content was borrowed from the remarks-side embedded structure.

## 11. Transcription independence and contamination audit

- Text extraction used to determine Ground Truth: **No**.
- OCR or image-recognition system used: **No**.
- Benchmark raw, normalized, or evaluation output consulted: **No**.
- MOF/RS or production data consulted: **No**.
- Arithmetic used before transcription or sign determination: **No**.
- Frozen Selection Record or Protocol changed: **No**.
- Prior exposure: source survey and row selection had exposed the page previously; this task nevertheless used a fresh 600-dpi render and does not claim blind transcription.

`ground-truth.json` retains existing normalized fixture fields; this evidence document preserves the raw visual forms and transcription provenance.

## 12. Integrity, explicit non-actions, and next task

The Selection Record, Protocol, Source Survey, and survey evidence remain byte-identical to their respective freeze commits. The Case-006–010 Selection Freeze, Cases 001–009, `scripts/`, source lock/registry, parser/normalizer/evaluator, OCR configuration, and production code were not changed. Temporary render files are not committed.

No benchmark engine, extraction command, separate OCR experiment, parser/normalizer/evaluator change, source-lock/registry change, MOF linkage, production adaptation, or row reselection was performed.

Recommended next task: **Case-010 First Frozen Benchmark** using the existing, unmodified pipeline against this frozen Ground Truth.

**Ground Truth was frozen from fresh direct visual source evidence for the already-selected Case-010 row. All amount fields and the delta sign were transcribed independently before arithmetic validation. No text-extraction output, benchmark engine, or OCR system was used to determine Ground Truth, and no frozen selection artifact was modified.**
