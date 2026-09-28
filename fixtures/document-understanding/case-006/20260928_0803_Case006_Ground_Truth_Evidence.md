# Case-006 Ground Truth Evidence — 法務省 (Ministry of Justice) FY2024 General-Account Expenditure Request

Status: **Ground Truth frozen from direct visual source evidence only. No benchmark engine or OCR system was used before or during this freeze.**

Date: 2026-09-28 (Asia/Tokyo)

## 1. Purpose

This document records the raw visual transcription, normalization, delta-sign determination, unit evidence/scope, and post-hoc arithmetic consistency check underlying `fixtures/document-understanding/case-006/ground-truth.json`, for the single row already selected and frozen in `fixtures/document-understanding/case-006/20260928_0742_Case006_Selection_Record.md`. This task creates Ground Truth for that already-selected row only — it does not re-select, re-consider, or re-open the selection itself.

## 2. Frozen selection reference

- Selection Protocol: `fixtures/document-understanding/case-006/20260928_0711_Case006_Selection_Protocol.md` (freeze commit `7ef2250`)
- Selection Record: `fixtures/document-understanding/case-006/20260928_0742_Case006_Selection_Record.md` (freeze commit `e2253ee`)
- Pre-task branch HEAD (verified via `git fetch`/`git status` immediately before this task's first edit): `e2253ee`, branch `research/case-006-moj-source-survey`, working tree clean — matches the expected pre-task HEAD exactly.

## 3. Source identity / SHA

- `sourceId`: `moj-fy2024-general-account-expenditure-request`
- SHA-256 (re-verified via `shasum -a 256` against the local raw file, matching `sources/source-lock.json` exactly, unchanged since the selection freeze): `bd5ce9c5dee48b03407e9a8d4050f3992c8a515f510c0339364316448dd9cf8c`

## 4. Selected locator verification

The frozen locator (`pdfPageIndex` 8, PDF page 9, printed `法（本） 5`, organization `010 法務本省`, item `010 法務本省共通費`, request no. `①`, expense code `01-95`) was re-verified against a fresh 400 dpi render of `pdfPageIndex` 8 in this task. **No mismatch was found** — the rendered page shows the identical structure already documented in the Selection Record, at the identical position (third content row, immediately below the two rejected aggregate rows).

## 5. Inspection method

- `pdftoppm -png -f 9 -l 9 -r 400` (and, for close reading of specific columns, cropped/zoomed regions of that same 400 dpi render via direct image cropping — no image processing that performs character recognition).
- No OCR, no Tesseract, no cloud/vision OCR, no LLM image-to-text extraction, no `pdftotext`, no `pypdf` object inspection was used in this task. Every value below was read directly from the rendered image by a human.
- No benchmark engine (`pdf.js`, `PyMuPDF`, `Docling`) was run.
- No MOF or RS/marumie-rssystem data was consulted.

## 6. Raw visual transcription

Directly read from the 400 dpi render, top-to-bottom within the target row's own visual block:

- Organization: `010 法務本省`
- Item: `010 法務本省共通費`
- Request number (circled numeral): `①`
- Expense code: `01-95`
- Expense name, raw printed lines:
  - Line 1: `法務本省一般行政に必要`
  - Line 2: `な経費`
- Previous-year-budget column: `112,183,723`
- FY2024-request column: `131,650,389`
- Delta column: `19,466,666` (no `△` glyph immediately preceding or attached to this value — confirmed via a zoomed crop of the delta column alone, see §9)
- Remarks (備考) column, at this row's own height: **empty** — confirmed via a zoomed crop of the full-width remarks column area spanning all three visible rows (organization aggregate, item aggregate, target row); populated remarks content exists further down the page, associated with a different, deeper sub-item row, not this target row.

## 7. Expense-name wrap/join

Per the frozen protocol's own C2 criterion, the label visually wraps across exactly 2 printed lines. Raw lines (§6) are joined directly, with **no space inserted** between them, consistent with this being a layout-driven wrap (the line break falls mid-word, between `必要` and `な経費`, not at a natural word boundary) rather than two semantically separate phrases:

- Normalized `expenseName`: `法務本省一般行政に必要な経費`

## 8. Amount raw → normalized

| Field | Raw (as printed) | Normalized (integer) |
|---|---|---|
| `previousBudget` | `112,183,723` | `112183723` |
| `fy2024Request` | `131,650,389` | `131650389` |
| `delta` | `19,466,666` | `19466666` |

Comma separators are the only difference between raw and normalized forms; no other transformation was applied.

## 9. Delta sign evidence

The delta column for the target row was examined at 2x zoom, isolated from the surrounding two rows (organization and item aggregates, both also confirmed to show no `△` glyph on their own delta values: `16,664,187` and `19,241,291` respectively). **No `△` (decrease) glyph is present immediately before or attached to `19,466,666`.** Per this program's own established convention (no glyph = positive), the delta is recorded as **positive**: `delta: 19466666`, `deltaRaw: "19,466,666"`. This determination was made **before** any arithmetic check (§13), from glyph evidence alone.

## 10. Unit evidence and scope

`[FACT]` The target page itself (`pdfPageIndex` 8, PDF page 9) carries its own unit declaration: `(単位:千円)`, printed directly below the `21 法務省所管` heading and above the column headers, on the **same page** as the target row itself — confirmed via a cropped, zoomed view of the page's own top region.

- Raw unit text: `(単位:千円)`
- Normalized unit: `千円`
- Evidence locator: `pdfPageIndex` 8, same page as the target row (not a remote/table-wide declaration from a different page)
- Scope interpretation: **page-level** — the unit is declared directly on the target row's own page, matching case-002/003/005's own same-page convention. This is a genuine, disclosed **difference from case-004/MEXT**, whose own unit was established once, remotely, on the document's first page, absent from the target row's own page. This scope was determined by direct inspection of the target page itself in this task, not assumed by analogy to any prior case or to the source survey's own earlier (different-page) unit observation.

## 11. Hierarchy evidence

- `itemCode`: `010` (from the item-level aggregate row `010 法務本省共通費` immediately preceding the target row)
- `itemName`: `法務本省共通費`
- Organization (`010 法務本省`) is recorded in this evidence document as hierarchy context but is not itself a `ground-truth.json` field, consistent with case-002–005's own schema, which records `itemCode`/`itemName` but not a separate organization field.

## 12. Remarks state

Per §6, the target row's own 備考 cell is **empty** (confirmed via direct visual inspection of the full-width remarks column at this row's own height). No remarks content is recorded in `ground-truth.json`, consistent with the existing schema's own convention (case-005's own schema likewise has no dedicated remarks field; remarks state is recorded here in evidence only, not elevated to a new GT field).

## 13. Arithmetic validation

Performed **only after** independent raw transcription (§6) and delta-sign determination (§9), as a post-hoc consistency check, never used to derive or adjust any transcribed value:

`131,650,389 − 112,183,723 = 19,466,666`

Computed directly: `131650389 − 112183723 = 19466666`. **Matches the transcribed and glyph-confirmed delta exactly.** No discrepancy was found; no re-transcription was triggered.

## 14. Vector-outline provenance note (Case-006-specific)

Per this task's own explicit requirement, the following is recorded as **provenance/context**, not as a Ground Truth value itself:

- The source page's own visual content is fully human-readable when rendered (confirmed throughout §5–§12 above).
- This source has **no extractable text layer** — confirmed exhaustively across all 737 pages in the Case-006 source survey (`reports/document-understanding/20260928_0703_Case006_MOJ_Source_Survey.md`).
- Every value in this Ground Truth was transcribed by direct human visual inspection of a rendered page image. **No OCR of any kind was used.**
- The PDF's own internal vector-path/object geometry (moveto/curveto/lineto operator counts, content-stream byte sizes, etc., as characterized in the source survey) was **not** used, referenced, or consulted to estimate, infer, or cross-check any character value in this Ground Truth — it is a document-level representation fact, entirely separate from the row-level transcription performed here.

## 15. Ambiguities

None encountered. Every digit, glyph, and line-break in the target row's own visual block was legible without ambiguity at 400 dpi (with 2x-zoomed crops used for close confirmation of the delta glyph and amount digits specifically). No `insufficient evidence` condition arose.

## 16. Contamination audit

- `ground-truth.json` and this evidence document are the only files containing the transcribed values; no value from this row was written into any production, benchmark, or evaluator logic.
- `scripts/` was not modified.
- No evaluator, normalizer, or extraction logic was modified.
- The Selection Protocol and Selection Record were not modified (byte-identical verification below).
- No MOF or RS/marumie-rssystem data was referenced at any point.
- No benchmark output was generated or consulted.

## 17. Freeze semantics

This Ground Truth is frozen as of this task's own commit. It exists for exactly the one row already selected and frozen in the Selection Record (§2) — no other row's Ground Truth exists or is implied. No benchmark engine has been run against this Ground Truth. Per the Case-006–010 Selection Freeze's own binding methodology note, the next task that runs a first frozen benchmark against this Ground Truth must use the existing, unmodified three-engine pipeline (`pdf.js`, `PyMuPDF`, `Docling`), and must preserve a null/empty result as-is, analyzing any such result as a pipeline-applicability-boundary finding rather than an ordinary document-understanding failure — not deviate from that methodology in response to seeing this specific Ground Truth.

## 18. Recommended next task

Run the existing, unmodified benchmark pipeline against this Ground Truth for the first time (Case-006's own first frozen benchmark run), preserving whatever result (including a null/empty one) occurs, per the Case-006–010 Selection Freeze's own frozen methodology note. **Not executed in this task.**

---

**Ground Truth was frozen from direct visual source evidence only. No benchmark engine or OCR system was run before or during the freeze.**
