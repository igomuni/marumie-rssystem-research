# Case-002 Selection Record

Status: **row frozen. Ground Truth NOT yet created. No benchmark engine run.**

Date: 2026-09-26 (Asia/Tokyo)

This record applies the already-committed, unmodified selection protocol (`fixtures/document-understanding/case-002/20260926_0834_Case002_Selection_Protocol.md`) to the locked METI source and freezes the exact target row. It does not create Ground Truth and does not run any benchmark engine.

## Source

- sourceId: `meti-fy2024-general-account-request`
- Source SHA-256 (from `sources/source-lock.json`, independently re-verified against the local `sources/raw/meti-fy2024-general-account-request.pdf` in this task via `shasum -a 256`): `ba64c25df327161a33c293374a7255c203cc9a527130ece848574badefbf909a`
- Official document: 令和6年度歳出概算要求書（一般会計）, 経済産業省 (METI FY2024 general-account expenditure request), 106 pages

## Frozen protocol

- Protocol path: `fixtures/document-understanding/case-002/20260926_0834_Case002_Selection_Protocol.md`
- Protocol commit: `4432492` (branch `research/case-002-meti-preregistration`), unmodified since
- Confirmation: E1–E5, the `△`/hierarchy-ambiguity non-requirements, and the tie-break rule were applied exactly as committed. No wording was changed before or after inspection.

## Inspection method

Direct visual inspection only. The locked PDF was rasterized page-by-page with `pdftoppm` (poppler) — a rasterizer with no text/layout reconstruction, not one of the three compared engines (`pdfjs-dist`, `pymupdf`, `docling`) — and the resulting page images were viewed directly, the same way a human would view the PDF in a viewer. No text-extraction or document-understanding tool was run.

Inspection trail (for reproducibility):
1. Rendered pages 1–6 to locate the document's own table of contents (目次). Page 3 (PDF page index 2) is the 目次 for 27 経済産業省所管, listing "令和6年度歳出概算要求額総表" at printed page 1 and "令和6年度歳出概算要求額明細表" (the detail table, item E1 requires) starting at printed page 5.
2. Rendered pages 7–10 to locate printed page "5". PDF pages 5–8 (printed 経1–経4) are the summary table (総表) — excluded by E1. PDF page 9 (1-based; 0-based index 8) is printed page "経(本) 5" — the first page of 令和6年度歳出概算要求額明細表, confirming the 目次's page reference.
3. On PDF page 9, the visible row order from the top is: `010 経済産業本省` (organization-level total, no expense code) → `010 経済産業本省共通費` (項/item-level total, no expense code) → `① 01-95 経済産業本省一般行政に必要な経費` (the first row anywhere in 明細表 carrying an explicit 目-level expense code). No row satisfying E2 appears earlier than this one, on this page or any preceding page (pages 1–8 are cover/blank/TOC/summary-table pages, none of which contain an expense-code-level row under E1's detail-table requirement).
4. Re-rendered PDF page 9 at higher resolution (300 dpi) and visually confirmed the row's structure directly (see Eligibility below).

## Selected location

- PDF page (1-based): 9
- PDF page (0-based index, matching this repository's `pdfPageIndex` convention): 8
- Printed page label: `経(本) 5`
- Row locator: the first (topmost) 目-level expense row in 令和6年度歳出概算要求額明細表, immediately under item header `010 経済産業本省共通費`
- Minimum identifying information: 要求番号 (request number) `①`, 事項 code `01-95`

Raw visible label text, recorded here **only to make the row locator unique and reproducible** — this is not a Ground Truth transcription and is not the curated/normalized expense name that a later Ground Truth phase will independently produce:

> `01-95　経済産業本省一般行政に必要な経費` — wraps across two printed lines (`経済産業本省一般行政に` / `必要な経費`) in the source.

## Eligibility (E1–E5)

- **E1 — Correct table: PASS.** The row is on PDF page 9, printed page `経(本) 5`, the first page of 令和6年度歳出概算要求額明細表 (the detail table), confirmed both by the document's own 目次 (page 3) and by the page's own title text ("令和6年度歳出概算要求額明細表"). It is not on the preceding summary table (総表, printed 経1–経4).
- **E2 — Native expense code: PASS.** The row carries the document's own expense code `01-95` in the 事項 column, in the same `NN-NN` format as case-001's `01-95`.
- **E3 — Multi-line wrap: PASS.** The row's label visibly wraps across two printed lines within the 事項 column (confirmed at 300 dpi).
- **E4 — Standard amount triple: PASS.** The row carries the document's standard three-column relationship (前年度予算額 / 6年度概算要求額 / 対前年度比較増△減) in its native layout, structurally analogous to case-001's previous/current/delta triple. (Values themselves are not transcribed here — see "Do not create Ground Truth" below.)
- **E5 — Sufficiency: PASS.** All of the row's identifying and amount-triple information is visible on this single page; nothing is split across a page boundary. The page additionally displays a "(単位:千円)" unit label directly beneath the table title — unlike case-001's target page, where the unit label was only present on an earlier summary page. This is a genuine structural difference between the two documents, noted here as an observation (relevant to hypothesis 4-adjacent questions about unit-label recovery), not something that affected eligibility.

## Tie-break

No earlier eligible row exists. This row is the first row anywhere in the entire 明細表 section (PDF pages 9 onward) to carry an explicit 目-level expense code (E2); every row before it (pages 1–8, and the two header rows immediately preceding this one on page 9 itself) is either front matter, the excluded summary table, or an organization/item-level total row with no expense code. The earliest-eligible-row-in-document-order tie-break therefore selects this row without ambiguity — no comparison between multiple eligible candidates was needed.

## Contamination controls

- Docling: not run against this source.
- `pdfjs-baseline` (benchmark): not run against this source.
- `pymupdf-baseline` (benchmark): not run against this source.
- `npm run docbench` / document-understanding benchmark: not run against this source.
- MinerU: not run.
- PaddleOCR / PP-Structure: not run.
- OCR or LLM/vision extraction intended to identify candidate values: none used. Page images were viewed directly by the same agent conducting this task, exactly as a human would view a rendered PDF page — no automated content-extraction step was interposed between the rasterized image and the eligibility decision.
- Ground Truth: does not exist yet (`fixtures/document-understanding/case-002/ground-truth.json` was not created); not consulted.
- No selection criterion (E1–E5, the tie-break, or the `△`/hierarchy-ambiguity non-requirements) was changed at any point during or after this inspection.

## Ground Truth

Not created in this task. `previousBudget`, `fy2024Request`, `deltaRaw`, `delta`, `unit`, and the normalized/curated `itemName`/`expenseName` fields were intentionally not transcribed here, even though some were visible during inspection, per the protocol's phase separation (selection freeze, then a separate Ground Truth creation task).
