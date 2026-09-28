# Case-006 Selection Record — 法務省 (Ministry of Justice) FY2024 General-Account Expenditure Request

Status: **selection executed under the already-frozen protocol. Row selected. No Ground Truth, no amount transcription, no benchmark engine or OCR run.**

Date: 2026-09-28 (Asia/Tokyo)

## 1. Purpose

This task applies the already-frozen Case-006 Selection Protocol (`fixtures/document-understanding/case-006/20260928_0711_Case006_Selection_Protocol.md`, commit `7ef2250`) via direct visual inspection only, to select exactly one row from organization `010 法務本省`'s own portion of MOJ's 明細表. The protocol itself is **not modified, re-derived, or reinterpreted** in this task — every rule applied below was frozen before this task began.

## 2. Frozen protocol reference

- Protocol document: `fixtures/document-understanding/case-006/20260928_0711_Case006_Selection_Protocol.md`
- Protocol freeze commit: `7ef2250`
- Pre-task branch HEAD (verified via `git fetch`/`git status` immediately before this task's first edit): `7ef2250`, branch `research/case-006-moj-source-survey`, working tree clean — matches the expected pre-task HEAD exactly.

## 3. Source identity / SHA

- `sourceId`: `moj-fy2024-general-account-expenditure-request`
- SHA-256 (re-verified via `shasum -a 256` against the local raw file, matching `sources/source-lock.json` exactly, unchanged since the protocol freeze): `bd5ce9c5dee48b03407e9a8d4050f3992c8a515f510c0339364316448dd9cf8c`

## 4. Universe (unchanged from the frozen protocol)

Organization `010 法務本省`, starting at `pdfPageIndex` 8 (PDF page 9, printed `法（本） 5`). Upper boundary: **unresolved**, per the protocol's own explicit disclosure — not investigated further in this task, since the winner was found before any need arose to determine it (§10 below).

## 5. Navigation method

Per the frozen protocol's own §11: cover-page TOC → organization locator → printed-to-PDF-page mapping (already established at the universe's own confirmed lower bound) → visual top-to-bottom rendering scan. Applied here via `pdftoppm` rendering (200 dpi) of `pdfPageIndex` 8 only — no text search was used or available (this source has zero extractable text), and no OCR was used at any point.

## 6. Rows actually evaluated

Scanning `pdfPageIndex` 8 from the top, immediately below the column-header row, in visual top-to-bottom order:

| Scan order | Locator | Structural role | C1 | C2 | C3 | C4 | Outcome |
|---|---|---|---|---|---|---|---|
| 1 | `pdfPageIndex` 8, topmost content row | Organization-level aggregate (`010 法務本省`) | **FAIL** — no native request number or expense code | not evaluated | not evaluated | not evaluated | **Rejected at C1** |
| 2 | `pdfPageIndex` 8, second content row | Item-level aggregate (`010 法務本省共通費`) | **FAIL** — no native request number or expense code | not evaluated | not evaluated | not evaluated | **Rejected at C1** |
| 3 | `pdfPageIndex` 8, third content row | Expense-level row | **PASS** — circled-numeral request number and expense code both present | **PASS** — label visually wraps across 2 printed lines | **PASS** — all three amount columns visually present and associated with this row | **PASS** — complete row visible within one coherent visual unit on this single page | **Accepted — WINNER** |

Per the frozen protocol's own rule, scanning stopped **immediately** upon Row 3 satisfying all four criteria. No row after Row 3 was viewed, compared, or considered. No page other than `pdfPageIndex` 8 was scanned for candidate rows.

## 7. Rejected rows and criterion failures

Two rows were rejected, both at C1, both for the identical reason: they are structural aggregate rows (organization-level and item-level respectively) carrying no native request-number or expense-level code — matching the same rejection pattern already documented in every prior case's own selection record (case-002 through case-005 each rejected an analogous organization-aggregate and item-aggregate pair immediately before their own selected row). No later criterion (C2–C4) was evaluated for either rejected row, per the protocol's own instruction not to force further evaluation once a row fails an earlier criterion.

## 8. Selected row locator

- `pdfPageIndex`: 8
- 1-based PDF page: 9
- Printed page label: `法（本） 5`
- Organization code/name: `010` / `法務本省`
- Item code/name: `010` / `法務本省共通費`
- Request number: `①` (circled numeral)
- Expense code: `01-95`
- Expense label (as visually read, for selection-identity purposes only — not a Ground Truth transcription): `法務本省一般行政に必要な経費`
- Visual wrap: 2 printed lines (`法務本省一般行政に必要` / `な経費`)

## 9. C1–C4 result for the selected row

- **C1 (native identifier)**: PASS — both a circled-numeral request number (`①`) and an expense-level code (`01-95`) are visually present in the row's own identifier columns.
- **C2 (multi-line wrap)**: PASS — the expense label visually occupies 2 printed lines within its own cell.
- **C3 (standard amount triple)**: PASS — all three amount columns (前年度予算額 / 6年度概算要求額 / 対前年度比較増△減) are visually present and associated with this specific row. **No value from any of the three columns is transcribed in this record.**
- **C4 (self-contained sufficiency)**: PASS — the complete row (identifier, label, all three amounts) is visually present within one coherent visual unit on this single page; no page-spanning, no blank inline triple, no relocation to a separate embedded region was observed for this row.

## 10. Tie-break application

No tie-break was needed: exactly one row satisfying all four criteria was found before any second candidate could be evaluated (per the protocol's own "stop immediately" rule, scanning ended at the first fully-passing row). The tie-break rule (earliest `pdfPageIndex`, then topmost row) is trivially satisfied by construction, since the winner is the first eligible row encountered in document order.

**Universe upper boundary**: the winner was found on `pdfPageIndex` 8, the universe's own very first page — far short of any need to determine organization `020`'s own start. Per the protocol's own §10 instruction, the upper boundary is **not investigated in this task** and remains recorded as `unresolved and unnecessary for the observed outcome`.

## 11. Prior-exposure disclosure

**This is the same row already disclosed as prior exposure in both the Case-006 source survey (`20260928_0703_Case006_MOJ_Source_Survey.md`, §16) and the Case-006 selection protocol (`20260928_0711_Case006_Selection_Protocol.md`, §12).** This is disclosed honestly, not minimized: this task does not claim a blind selection, and no technical sandbox prevented this row from being seen before this task began. The methodological control remains, as stated in the protocol itself, that every criterion (C1–C4) was frozen in abstract, source-structural terms **before** this task's own visual scan began, and would have produced the identical rule and the identical rejection of the two preceding aggregate rows regardless of which specific expense row happened to satisfy them first. This row is recorded as the deterministic output of applying the already-frozen protocol to the universe's own first page — it was neither sought nor avoided because of its prior familiarity.

## 12. Incidental visual exposure

While confirming C3 (standard amount triple) for the winning row, the three amount values (前年度予算額, 6年度概算要求額, 対前年度比較増△減, including its own delta sign) were necessarily visible in the rendered page image, as was the fully populated 備考 column content to the right of the ledger (organization-wide staffing-count figures, not associated with this specific row's own identifier). **None of these values is transcribed anywhere in this record.** This is disclosed as unavoidable incidental exposure inherent to visual-only inspection (the only method available for this raster/vector-outline source), not as a Ground Truth transcription.

## 13. Ground Truth separation

This task explicitly did **not**: transcribe any amount value (previous budget, request amount, or delta); determine or record the delta's sign; perform any arithmetic validation; establish or freeze a unit for this target row; transcribe any 備考 content; or produce a normalized version of the expense label. The expense label recorded in §8 is a **selection-identity locator**, not a Ground Truth transcription — it is recorded in the same un-normalized, directly-observed form used by every prior case's own selection record for the identical purpose, and is understood to require independent re-verification (not mere reuse) if and when a future, separate Ground Truth task is performed.

## 14. Tools used

`pdftoppm` (PNG render, 200 dpi, `pdfPageIndex` 8 only) for visual inspection. No text extraction tool (`pdftotext`, `pdffonts`) was used for row discovery in this task (consistent with the protocol's own explicit prohibition, and moot regardless since this source has no extractable text). No OCR tool of any kind was used. No PDF object-inspection tool (`pypdf`) was used in this task — that method was reserved for the source survey's own representation diagnostic, not row selection.

## 15. What was not done

- No row beyond the three evaluated (§6) was viewed, rendered, or considered.
- No page other than `pdfPageIndex` 8 was rendered or scanned.
- The universe's own upper boundary was not investigated (§10).
- No amount value, delta sign, or 備考 content was transcribed.
- No Ground Truth was created.
- No benchmark engine (`pdf.js`, `PyMuPDF`, `Docling`) was run.
- No OCR, vision-based extraction, or LLM image-to-text transcription was performed.
- No parser, normalizer, or evaluator was modified.

## 16. Freeze semantics

This selection record is frozen as of this task's own commit. Exactly one row has been selected from organization `010 法務本省`'s own portion of MOJ's 明細表, under the already-frozen protocol, applied without modification. No Ground Truth exists for Case-006. The next task must create Ground Truth for this specific row via direct visual transcription (amounts, delta sign from glyph evidence, unit, hierarchy), following the same methodology already established in case-001–005, and must stop before any benchmark engine or OCR run — consistent with the Case-006–010 Selection Freeze's own binding methodology note that any future first-frozen benchmark run must use the existing, unmodified three-engine pipeline and preserve a null/empty result as-is.

## 17. Recommended next task

Create Ground Truth for the selected row (§8) via direct visual transcription, by the same methodology already established in case-001–005, and stop before any benchmark engine or OCR run. **Not executed in this task.**

---

**Exactly one row was selected under the frozen protocol. No Ground Truth or amount values were recorded, and no benchmark engine or OCR system was run.**
