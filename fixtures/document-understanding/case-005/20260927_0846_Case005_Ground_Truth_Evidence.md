# case-005 Ground Truth Evidence — MLIT (国土交通省) FY2024 General-Account Expenditure Request

Status: **Ground Truth frozen. No benchmark engine has been run.**

Date: 2026-09-27 (Asia/Tokyo)

## 1. Purpose / scope

This document is the provenance/evidence record for `fixtures/document-understanding/case-005/ground-truth.json`. It exists so a reviewer can independently verify every Ground Truth field against the source, without needing any benchmark-engine output — the same purpose case-001–004's own equivalent evidence documents serve. This task performs Ground Truth creation, evidence recording, and freeze **only** — no benchmark engine, OCR, or existing derived engine output was consulted at any point.

`ground-truth.json`'s `result` object uses the exact same field set as case-001–004's (`itemCode`, `itemName`, `requestNo`, `expenseCode`, `expenseName`, `previousBudget`, `fy2024Request`, `deltaRaw`, `delta`, `unit`, `page`), so the unchanged `evaluate.mjs` can score case-005 with no benchmark-code modification. No schema was invented or modified.

## 2. Source identity / SHA (re-verified in this task)

- `sourceId`: `mlit-fy2024-general-account-expenditure-request`
- Locked SHA-256 (`sources/source-lock.json`): `4eebb84cec72a4b3b11a2b89c41093550bef5a07095d5c7b178e238406b08217`
- Locally recomputed SHA-256 (`shasum -a 256 sources/raw/mlit-fy2024-general-account-expenditure-request.pdf`) in this task: `4eebb84cec72a4b3b11a2b89c41093550bef5a07095d5c7b178e238406b08217` — **exact match**

## 3. Selection freeze identity

- Selection protocol: `fixtures/document-understanding/case-005/20260927_0815_Case005_Selection_Protocol.md` (commit `9b292c0`) — re-verified byte-identical to the freeze commit before this task began.
- Selection record: `fixtures/document-understanding/case-005/20260927_0823_Case005_Selection_Record.md` (commit `bab422f`) — re-verified byte-identical to the freeze commit before this task began.
- This document and `ground-truth.json`: created after the above, still before any benchmark engine has been run against MLIT.

## 4. Locator re-verification

The selected row was re-verified by direct visual inspection **before** any transcription began, against the selection record's own stated locator:

| Field | Selection record | Re-verified against source | Match? |
|---|---|---|---|
| `pdfPageIndex` | 28 | 28 | Yes |
| 1-based PDF page | 29 | 29 | Yes |
| Printed page label | `国（本） 19` | `国（本） 19` | Yes |
| Organization | `010 国土交通本省` | `010 国土交通本省` | Yes |
| Item | `002 国土交通本省共通費` | `002 国土交通本省共通費` | Yes |
| Request no. (raw) | `①` | `①` | Yes |
| Expense code | `05-95` | `05-95` | Yes |
| Expense label | `国土交通本省一般行政に必要な経費`, wraps 2 lines | Confirmed: line 1 `国土交通本省一般行政に`, line 2 `必要な経費` | Yes |

**No discrepancy was found.** Row selection was not repeated or re-derived; this task proceeded directly to Ground Truth creation for the already-frozen row.

## 5. Inspection method

Direct visual inspection of the locked PDF, rendered with `pdftoppm` (poppler — a rasterizer with no text/layout reconstruction; not one of the three compared engines `pdfjs-dist`/`pymupdf`/`docling`). Renders used:

- 400 dpi full-page render of PDF page 29 (`pdfPageIndex` 28), viewed directly.
- A precise native crop of the target row's own band (`-x 0 -y 950 -W 4678 -H 250`) at 400 dpi, to confirm every character, digit, comma, and the absence of `△` at full legibility.
- A precise native crop of the unit-label region (captured incidentally within a wider top-of-page crop, `-x 0 -y 250 -W 4678 -H 250`) to confirm the unit text exactly.
- A precise native crop of the organization-aggregate row's own delta cell (`-x 0 -y 400 -W 4678 -H 200`) to corroborate the `△` glyph renders correctly elsewhere on this same page.

No OCR, LLM, or vision-model extraction was used at any point — every value below was read directly from the rendered page image by the same agent conducting this task, the same way a human reading the PDF in a viewer would. Docling, pdfjs-baseline, pymupdf-baseline, MinerU, PaddleOCR, `npm run docbench`, MOF CSV, and RS/marumie-rssystem data were not consulted at any point in this task.

## 6. Raw transcription table

| Field | Raw visual text (as printed) |
|---|---|
| Item code | `002` (label: `002　国土交通本省共通費`) |
| Item name | `国土交通本省共通費` (single printed line, does not wrap) |
| Request number | `①` (circled numeral one, U+2460) |
| Expense code | `05-95` |
| Expense name, line 1 | `国土交通本省一般行政に` |
| Expense name, line 2 | `必要な経費` |
| Previous budget | `118,052,728` |
| FY2024 request | `136,727,866` |
| Delta | `18,675,138` — **no `△` glyph precedes this value anywhere in the cell**, confirmed at 400 dpi in a dedicated full-width row-band crop |
| Unit label | `(単位：千円)`, printed once directly beneath the table title, above the column headers, on this same page |
| Printed page label | `国（本）　19` (top-right corner of the page) |

## 7. Raw → normalized mapping

| Field | Raw → Normalization operation | Normalized value | Confidence / ambiguity |
|---|---|---|---|
| itemCode | `002` → none | `"002"` | None — clearly printed |
| itemName | `国土交通本省共通費` → none | `"国土交通本省共通費"` | None |
| requestNo | `①` → circled-numeral-to-plain-digit-string, the same convention case-001–004 use | `"1"` | None |
| expenseCode | `05-95` → none | `"05-95"` | None |
| expenseName | Line-break join of `国土交通本省一般行政に` + `必要な経費`, no inserted space (CJK text does not use inter-word spaces, the same convention already documented for case-001–004) | `"国土交通本省一般行政に必要な経費"` | None — the line break falls at a natural word boundary with no ambiguity about join order (reading order confirmed top-to-bottom, single column, no interleaving with any other cell's text) |
| previousBudget | `118,052,728` → comma-group removed, parsed as integer | `118052728` | None |
| fy2024Request | `136,727,866` → comma-group removed, parsed as integer | `136727866` | None |
| delta | `18,675,138`, no glyph → comma-group removed; sign positive because no decrease glyph was observed — **not** inferred from `fy2024Request − previousBudget` | `deltaRaw: "18,675,138"`, `delta: 18675138` | None |
| unit | `(単位：千円)` → parenthetical/label wrapper removed, leaving the bare unit word | `"千円"` | None — confirmed directly on the target row's own page (see §11) |

No field required arithmetic backfill, cross-column completion, or inference from a prior case's own pattern; every value above was read directly from this specific source page.

## 8. Expense-name line-join evidence

The expense label visually occupies two printed lines within its own cell: `国土交通本省一般行政に` (line 1, sharing its printed line with the expense code `05-95`) and `必要な経費` (line 2, indented to align beneath the label's own start, with no code or amount printed on this line). Reading order is unambiguous — top-to-bottom, single column, no interleaving with the amount columns (which remain aligned with line 1 only) or with any neighboring row. This is a genuine layout-driven line break (the cell is visually narrower than the full label), not an intentional inter-word space or punctuation-driven break — the two fragments concatenate directly into one coherent phrase (`国土交通本省一般行政に` + `必要な経費` = `国土交通本省一般行政に必要な経費`, a complete and grammatical expense-name phrase) with no space needed at the join point, consistent with ordinary Japanese text wrapping. This determination was made by reading the rendered page directly, not by observing how any text-extraction engine reconstructed the line.

## 9. Amount evidence

- **Previous budget**: raw `118,052,728`, read directly from the row's own previous-budget column, independent of the FY2024 request and delta columns. Comma grouping confirmed unambiguous at 400 dpi (three-digit groups: `118` / `052` / `728`).
- **FY2024 request**: raw `136,727,866`, read directly and independently from the row's own current-year-request column. Comma grouping confirmed unambiguous (`136` / `727` / `866`).
- **Delta**: raw `18,675,138`, read directly and independently from the row's own delta column. Comma grouping confirmed unambiguous (`18` / `675` / `138`).
- No value was inferred from the other two; no value was completed from an adjacent row, the item-level aggregate above it, or any prior case's own pattern.

## 10. Delta-sign evidence

The delta cell was visually inspected specifically for the `△` glyph in a dedicated high-resolution crop of the full row band (§5); no glyph is present, and the digits read cleanly as `18,675,138` with no leading mark of any kind.

**Corroboration (document-level, not target-row evidence):** the same page's own `010　国土交通本省` organization-aggregate row visibly shows `△　530,617,743` in its own delta column, confirmed in a dedicated high-resolution crop. This confirms the `△` glyph renders correctly and is an actively-used convention on this exact page — not a font-rendering gap that could silently suppress a real negative sign. It was **not** used to infer the target row's own sign, which was determined solely from the absence of any mark in its own cell — this is glyph-rendering-mechanism corroboration only, per this task's own explicit constraint not to infer the target's sign from any other row.

The normalized `delta` is therefore recorded as **positive** (`18675138`) strictly because the source does not visually show a decrease indicator on this row — not because arithmetic suggested a sign either way (the arithmetic check in §12 was performed only after this determination was already made).

## 11. Unit evidence / scope

The unit label `(単位：千円)` is printed **once, directly on the same page as the target row** (`pdfPageIndex` 28), beneath the document-wide table title (`令和6年度歳出概算要求額明細表`) and the sheet header (`28　国土交通省所管`), above the column headers — the identical page-level position and scope already documented for case-002 and case-003's own target pages. This is a **genuinely different scope** from case-004 (MEXT), where the equivalent label was found only on the file's own first page, not repeated on the target row's own page, and was recorded there with an explicitly weaker table-wide scope. For case-005, the label is directly present on the target's own page, so `unit: "千円"` is recorded with a **page-level** scope, confirmed for this page only — not generalized to any other page of the 1,097-page document, including other pages within the same `010 国土交通本省` organization.

## 12. Hierarchy / item evidence

The selected expense row (`①`, `05-95`) sits beneath two aggregate rows on the same page, read in document order: `010　国土交通本省` (組織-level aggregate, its own amounts `5,439,976,254` / `4,909,358,511` / `△530,617,743`) and `002　国土交通本省共通費` (項-level aggregate, its own amounts `119,106,358` / `137,840,441` / `18,734,083`). **These aggregate amounts belong to the organization and item levels respectively, and are explicitly not transcribed as the selected expense row's own amounts** — `itemCode`/`itemName` in `ground-truth.json` record the item-level *identity* (`002`/`国土交通本省共通費`) as hierarchy context only, exactly matching the field's own established meaning in case-001–004's schema (the item the expense row falls under, not the item's own amount).

## 13. Arithmetic consistency check

```text
fy2024Request - previousBudget == delta
136,727,866   - 118,052,728    == 18,675,138
18,675,138                     == 18,675,138   -> PASS
```

This check was run **after** all three values were independently transcribed from the rendered image (§9) and after the delta's sign was already determined from glyph evidence alone (§10) — strictly as a post-hoc consistency check on the already-recorded transcription. No value was adjusted to make it pass, and none needed to be.

## 14. Ambiguities / incidental observations

- No field was genuinely ambiguous or illegible at 400 dpi. Nothing was marked unknown.
- **Incidental observation, not expanded into further investigation, per this task's own scope**: the item-level aggregate row (`002　国土交通本省共通費`) and the organization-level aggregate row (`010　国土交通本省`) both carry a lengthy free-text remarks block on this same page (visible in the full-page render, §4/§6) — this is not part of the GT schema and was not transcribed. Neither `繰入`-shaped expressions nor any other special structure was observed on this specific page; this observation is recorded only because the page was already being read for GT purposes, not from any additional or expanded inspection.

## 15. Contamination controls

- Docling: not run against this source.
- `pdfjs-baseline` (benchmark): not run.
- `pymupdf-baseline` (benchmark): not run.
- `npm run docbench` / document-understanding benchmark: not run.
- MinerU: not run.
- PaddleOCR / PP-Structure: not run.
- MOF CSV / RS (marumie-rssystem) data: not consulted.
- No prior or newly generated normalized engine output for MLIT was consulted (none exists).
- Ground Truth was derived solely from direct visual inspection of the rasterized source page, per the method in §5.
- Selection protocol (`9b292c0`) and selection record (`bab422f`) re-verified byte-identical to their freeze commits, both before this task began and again immediately before commit.
- No `result` value from this Ground Truth is hard-coded anywhere in production code or tests — confirmed by direct review of this task's own diff, which touches only the two new case-005 files and the three state files.

## 16. Ground Truth freeze statement

`fixtures/document-understanding/case-005/ground-truth.json` is frozen as of this task's own commit. Every value in its `result` object was determined solely from direct visual inspection of the locked MLIT source, independently transcribed, with the delta's sign determined from glyph evidence alone and the arithmetic check performed only afterward as validation. No benchmark engine, OCR tool, or `npm run docbench` was run against MLIT before or during this freeze. No case-001–004 file, selection protocol, selection record, evaluator, normalizer, adapter, or Case Package schema was modified.

## 17. Next step

Run the existing benchmark engines against case-005 for the first time using the frozen Ground Truth and unchanged benchmark semantics, preserving the first-run result before any adaptation. **Not executed in this task.**
