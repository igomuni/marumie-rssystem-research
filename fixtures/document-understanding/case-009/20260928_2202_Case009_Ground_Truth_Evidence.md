# Case-009 Cabinet Office (CAO) Ground Truth Evidence

Status: **FROZEN from direct visual source evidence**

Created: 2026-09-28 22:02 Asia/Tokyo
Branch: `research/case-009-cao-source-survey`

## 1. Purpose and frozen selection reference

This document independently transcribes Ground Truth for the one physical row already frozen in `20260928_2149_Case009_Selection_Record.md` at commit `985f77ed1ffa3cd29ae9e5b90f2b5de8fa74b969`. Selection was not repeated or changed.

Freeze chain: Source Survey `e640dc21c5bf536ab5ca40b20ed4b3ea8b2b3c11` → Selection Protocol `d42b7b89f2671c8e9cad04b75116fbd7b64b7af6` → Selection Record `985f77ed1ffa3cd29ae9e5b90f2b5de8fa74b969`.

## 2. Canonical source identity and inspection method

| field | value |
|---|---|
| source ID | `cao-fy2024-general-account-expenditure-request-detail-01` |
| official file / URL | `1.pdf` / `https://www.cao.go.jp/yosan/soshiki/r06/pdf/1.pdf` |
| SHA-256 | `7b5de5dbd397c7067cab4ea527ef02681e91265914057651ee5b886174de7f4e` |
| integrity | recomputed from the locked raw PDF before rendering; matches source lock and registry |
| render | fresh `pdftoppm` page 1 (`pdfPageIndex 0`) at 600 dpi |

All character and numeric transcription below was read from that fresh render. No OCR, text extraction, PDF text/object inspection as a recognition substitute, benchmark output, MOF/RS data, production data, or expected arithmetic result was used.

## 3. Locator and identity re-verification

Before reading amounts, the fresh render matched the frozen Selection Record on all of: `pdfPageIndex 0`; printed prefix `内（本）`; division scope `19 内閣府所管（官房総務課（総務課））`; organization `010 内閣本府`; item `010 内閣本府共通費`; request number `①`; expense code `01-95`; and the two-line expense label below. The row is in the standard-ledger grammar and the non-target explanatory/breakdown material in the remarks region was not used.

## 4. Expense name: raw visual lines → normalized

| representation | value |
|---|---|
| raw line 1 | `内閣本府一般行政に必要` |
| raw line 2 | `な経費` |
| normalized | `内閣本府一般行政に必要な経費` |

Normalization removes the visual line wrap only; no space or other character was inserted.

## 5. Independent amount transcription

The three cells were read independently in this order, before any arithmetic operation.

| field | raw visual string | normalized integer |
|---|---|---:|
| previous budget | `79,533` | 79533 |
| FY2024 request | `84,991` | 84991 |
| delta | `5,458` | 5458 |

## 6. Delta sign evidence

The selected-row delta cell visibly contains `5,458` with no preceding `△`, minus, or other negative marker. Its normalized signed value is therefore positive `5458`. This sign determination preceded arithmetic validation.

## 7. Unit evidence and scope

| representation | value |
|---|---|
| raw source text | `（単位:千円）` |
| normalized unit | `千円` |
| locator | `pdfPageIndex 0`, top-right file-section opening |
| scope | the standard-ledger section of locked `1.pdf`; not package-global and not inherited by embedded explanatory/breakdown material |

## 8. Remarks state

The selected row's own remarks cell is visually empty. Explanatory/breakdown text lower in the remarks region belongs to nested non-target material and was not assigned to the selected row. Ground Truth remarks is therefore the empty string.

## 9. Arithmetic validation

Only after independent transcription of all three amount fields and the sign:

`84991 - 79533 = 5458`

Result: **PASS**. The calculation confirmed the independently read values; it did not supply or modify any transcription.

## 10. Ambiguities and remediation

No character, digit, or sign ambiguity remained at the 600-dpi render. No crop, OCR, extraction tool, or arithmetic-led correction was needed.

## 11. Contamination audit and provenance

- Benchmark raw/normalized/evaluation output consulted: **No**.
- Extractor or OCR output used as a reading aid: **No**.
- MOF/RS or production data consulted: **No**.
- Arithmetic used before transcription: **No**.
- Frozen Selection Record or Protocol changed: **No**.
- Prior exposure: the row had been visualized during source survey/protocol/selection work; this GT was nevertheless transcribed afresh from the locked source and does not claim blind transcription.

`ground-truth.json` follows the existing case schema. It retains normalized semantic fields; this evidence document preserves the raw visual forms and the source-to-normalized distinction.

## 12. Frozen-artifact integrity, validation, and next task

Source Survey/evidence, Selection Protocol, and Selection Record remain byte-identical to their respective freeze commits. The Case-006–010 Selection Freeze, Cases 001–008, `scripts/`, source lock/registry, parser/normalizer/evaluator, and production code were not changed. Temporary render files are not committed.

Validation includes strict JSON parsing/type checks, repository validation, source-acquisition tests, and `git diff --check`. No benchmark or OCR system was run.

Recommended next task: **Case-009 First Frozen Benchmark** using the existing, unmodified pipeline against this frozen Ground Truth.

**Ground Truth was frozen from direct visual evidence for the already-selected Case-009 row. All amount fields and the delta sign were transcribed independently before arithmetic validation. No benchmark engine or OCR system was run before or during the freeze, and no frozen selection artifact was modified.**
