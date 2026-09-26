# Case-002 Ground Truth Evidence

Status: **Ground Truth frozen. No benchmark engine has been run.**

Date: 2026-09-26 (Asia/Tokyo)

This document is the provenance/evidence record for `fixtures/document-understanding/case-002/ground-truth.json`. It exists so a reviewer can independently verify every Ground Truth field against the source, without needing any benchmark-engine output — the same purpose `fixtures/document-understanding/case-001/README.md` serves for `case-001`.

`ground-truth.json`'s `result` object intentionally uses the exact same field set as `case-001`'s (`itemCode`, `itemName`, `requestNo`, `expenseCode`, `expenseName`, `previousBudget`, `fy2024Request`, `deltaRaw`, `delta`, `unit`, `page`) so that the unchanged `evaluate.mjs` can score `case-002` with no benchmark-code modification. That schema stores only normalized values; this document is where the raw/visual evidence and normalization decisions live, exactly mirroring how `case-001`'s own README already documents its raw wrapped-line structure alongside its Ground Truth.

## Source and location (re-verified in this task)

- sourceId: `meti-fy2024-general-account-request`
- Locked SHA-256 (`sources/source-lock.json`): `ba64c25df327161a33c293374a7255c203cc9a527130ece848574badefbf909a`
- Locally recomputed SHA-256 (`shasum -a 256 sources/raw/meti-fy2024-general-account-request.pdf`) in this task: `ba64c25df327161a33c293374a7255c203cc9a527130ece848574badefbf909a` — **exact match**
- Selected row: PDF page 9 (1-based) / index 8 (0-based), printed page `経(本) 5` — per the already-frozen `20260926_0852_Case002_Selection_Record.md`. The row identity was not changed.

## Acquisition method

Direct visual inspection of the locked PDF, rendered with `pdftoppm` (poppler — a rasterizer with no text/layout reconstruction; not one of the three compared engines `pdfjs-dist`/`pymupdf`/`docling`). Renders used:

- 400 dpi full-page render of PDF page 9 (`pdftoppm -png -r 400 -f 9 -l 9`), viewed directly.
- A precise native crop of the target-row band (`pdftoppm -x 0 -y 650 -W 4678 -H 250 ... -r 400`, i.e. `pdftoppm`'s own pixel-accurate crop options rather than post-hoc image cropping) to confirm every character, digit, comma, and the absence/presence of `△` at full legibility.
- A precise native crop of the unit-label region (`pdftoppm -x 3800 -y 350 -W 878 -H 150 ... -r 400`) to confirm the unit text exactly.

No OCR, LLM, or vision-model extraction was used at any point — every value below was read directly from the rendered page image by the same agent conducting this task, the same way a human reading the PDF in a viewer would.

## Raw visual text vs. normalized Ground Truth value

| Field | Raw visual text (as printed) | Normalization applied | Normalized value (in `ground-truth.json`) |
|---|---|---|---|
| Item code | `010` (label: `010 経済産業本省共通費`) | none | `"010"` |
| Item name | `経済産業本省共通費` (single printed line, does not wrap) | none | `"経済産業本省共通費"` |
| Request number | `①` (circled numeral one, U+2460) | circled-numeral → plain digit string, the same convention `case-001` uses for its own plain digit request numbers (e.g. `"4"`) | `"1"` |
| Expense code | `01-95` | none | `"01-95"` |
| Expense name | Wraps across two printed lines: line 1 `経済産業本省一般行政に`, line 2 `必要な経費` | Line-break join with no inserted space — CJK text does not use inter-word spaces, the same convention already documented for `case-001`'s wrapped item/expense names | `"経済産業本省一般行政に必要な経費"` |
| Previous budget | `42,331,005` | Comma-group removed, parsed as integer | `42331005` |
| FY2024 request | `46,887,829` | Comma-group removed, parsed as integer | `46887829` |
| Delta | `4,556,824` — **no `△` glyph precedes this value anywhere in the cell** (directly compared against multiple neighboring rows on the same page that do visibly carry `△`, e.g. `△6,745`, `△2,839`, `△32`, `△2,570`, `△7,485`, `△32,402` — the visual contrast confirms this is a genuine absence, not a misread) | Comma-group removed; sign is positive because no decrease glyph was observed — **not** inferred from `fy2024Request − previousBudget` | `deltaRaw: "4,556,824"`, `delta: 4556824` |
| Unit | `(単位: 千円)`, printed once directly below the table title, above the column headers, applying to the whole page's table | Parenthetical/label wrapper removed, leaving the bare unit word — same normalization as `case-001`'s `"千円"` | `"千円"` |
| Printed page label | `経(本)　5` (top-right corner of the page) | none | `"経(本) 5"` |

No field was ambiguous or illegible at 400 dpi. Nothing was marked unknown.

## Sign handling

The delta cell was visually inspected specifically for the `△` glyph and compared side-by-side against six other rows on the same page that do carry it, to rule out a rendering artifact suppressing a faint glyph. No glyph is present. The normalized `delta` is therefore recorded as **positive** (`4556824`) strictly because the source does not visually show a decrease indicator — not because arithmetic or `case-001`'s (negative, `△`-marked) delta suggested a sign either way. This is a deliberate out-of-sample difference from `case-001` and is itself a valid test of the same sign-handling code path (see `common.mjs`'s `parseAmountToken` and `normalize-docling.mjs`'s `reconstructNumericToken`, both already tested for "no glyph anywhere means never signed negative").

## Arithmetic consistency check

```text
fy2024Request - previousBudget == delta
46,887,829    - 42,331,005     == 4,556,824
4,556,824                      == 4,556,824   -> PASS
```

This check was run **after** all three values were independently transcribed from the rendered image, strictly as a consistency check on the already-recorded transcription — no value was adjusted to make it pass, and none needed to be.

## Unit handling (re-verified, not assumed from the prior selection record)

The selection record noted incidentally that this page carries a `千円` unit label, unlike `case-001`'s target page. This was independently re-verified in this task via a dedicated high-resolution crop of the unit-label region: the exact printed text is `(単位: 千円)`, appearing once at the top of the 明細表 table (applies to the whole page), normalized to `"千円"`. This remains an observed structural difference between the two documents, not a criterion that influenced row selection (selection was already frozen before this task began).

## Contamination controls

- Docling: not run against this source.
- `pdfjs-baseline` (benchmark): not run.
- `pymupdf-baseline` (benchmark): not run.
- `npm run docbench` / document-understanding benchmark: not run.
- MinerU: not run.
- PaddleOCR / PP-Structure: not run.
- No prior or newly generated normalized engine output for METI was consulted.
- Ground Truth was derived solely from direct visual inspection of the rasterized source page, per the method above.

## What this task did not do

This task did not modify `case-001`'s Ground Truth, evidence, or results; the Docling normalizer; the numeric-token reversal rule; the CJK wrap-space-closing rule; `evaluate.mjs`; any engine adapter; or any benchmark scoring/check definition. `ground-truth.json`'s `result` schema is identical in shape to `case-001`'s, so no benchmark-code change was needed to accommodate `case-002`.
