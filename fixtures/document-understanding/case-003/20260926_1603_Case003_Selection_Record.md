# case-003 Selection Record — MIC (総務省) FY2024 Detailed Expenditure Request

Status: **row frozen. Ground Truth NOT created. No benchmark engine run.**

Date: 2026-09-26 (Asia/Tokyo)

This record applies the already-committed, unmodified selection protocol to the already-locked MIC source and freezes the exact target row. It does not create Ground Truth and does not run any benchmark engine.

## Protocol reference

- Protocol path: `fixtures/document-understanding/case-003/20260926_1548_Case003_Selection_Protocol.md`
- Freeze commit: `8b65364`
- Confirmed byte-identical to that commit immediately before this task began (`git diff 8b65364 -- <protocol path>` = empty). No criterion, non-criterion, universe, or tie-break rule was changed at any point during this task.

## Source identity

- `sourceId`: `mic-fy2024-general-account-expenditure-request`
- SHA-256 (re-verified against `sources/source-lock.json` and against `shasum -a 256` of the local raw file immediately before and after inspection): `cc54dbe5f689116619a1f8453747d47bca5b960137f90869ead26954d651703b` — unchanged throughout this task.
- Frozen universe (per the protocol, unmodified): organization `010 総務本省`, within `令和6年度歳出概算要求額明細表`, printed pages 5–245.

## Inspection method

Direct visual inspection only. The locked PDF was rasterized page-by-page with `pdftoppm` (poppler — a rasterizer with no text/layout reconstruction, not one of the three compared engines) at 80–400 dpi, and the resulting page images were viewed directly, the same way a human would view the PDF in a viewer. No text-extraction, OCR, or document-understanding tool was run. No `pdfjs-baseline`/`pymupdf-baseline`/`docling`/MinerU/PaddleOCR/`npm run docbench` was used. No Ground Truth was consulted (none exists for case-003).

**Necessary pre-enumeration navigation:** the frozen protocol had explicitly left the PDF-page-index-to-printed-page-label mapping as an unresolved unknown (needed because printed labels are not the authoritative ordering key). Resolving this required paging through the document's front matter — the cover/coarse TOC (PDF page 1), the detailed TOC (PDF pages 3–4), and the summary table `総表` (PDF pages 5–8, printed `総1`–`総4`) — before reaching the actual start of `明細表` for organization `010` at PDF page 9 (printed `総(本) 5`). This is source-native TOC/pagination navigation, explicitly allowed by the protocol, not row-level candidate inspection of any organization's detail table.

## Enumeration

Starting point: the first page of `令和6年度歳出概算要求額明細表` for organization `010 総務本省` — PDF page 9 (1-based), `pdfPageIndex` 8 (0-based), printed label `総(本) 5`. Ordering followed: top-to-bottom reading order on this page, per the frozen tie-break.

Three potential semantic rows were encountered, in this order, before enumeration stopped:

| # | Row (locator only) | ME1 | First failing criterion | Disposition |
|---|---|---|---|---|
| 1 | `010 総務本省` (組織-level aggregate line) | PASS (within 明細表) | **ME2** — no request number or expense-level code; a pure organization-level aggregate with no code beyond the organization number itself | Rejected |
| 2 | `010 総務省共通費` (項-level aggregate line, directly beneath #1) | PASS (within 明細表) | **ME2** — carries only an item(項)-level code (`010`), no expense(目)-level code; a bare aggregate/header row | Rejected |
| 3 | `① 01-95 総務本省一般行政に必要な経費` (directly beneath #2) | PASS | — (all five passed) | **Selected — first eligible row** |

No row beyond #3 was inspected. Enumeration stopped at the first row passing all five criteria, per the protocol's explicit instruction not to continue searching for a "better" candidate.

## Selected row locator

- `pdfPageIndex`: 8 (0-based; authoritative ordering key, per the frozen protocol)
- `pdfPageNumber`: 9 (1-based)
- `printedPageLabel`: `総(本) 5`
- Organization (`組織`): `010 総務本省`
- Item header (`項`): `010 総務省共通費`
- Request number (`要求番号`): `①`
- Expense code (`事項`): `01-95`
- Expense name: `総務本省一般行政に必要な経費`

This is the minimum locator sufficient for a later, independent Ground Truth task to find the exact row without consulting any engine output.

## Eligibility (ME1–ME5)

- **ME1 — Correct table: PASS.** The row is on PDF page 9, printed page `総(本) 5`, the page header itself reads "令和6年度歳出概算要求額明細表" (the detail table) — confirmed not to be on `総表` (printed `総1`–`総4`, PDF pages 5–8) or `定員表` (printed page 451 onward, well outside both the row's location and the frozen universe).
- **ME2 — Native item/expense-level code: PASS.** The row carries an explicit expense-level code (`01-95`) together with a request number (`①`), in the same `NN-NN` + circled-numeral format already used by case-001/case-002 — visibly distinct from the two rejected rows above it, which carry only organization- or item-level codes with no expense code.
- **ME3 — Multi-line wrap: PASS.** Confirmed at 400 dpi: the expense-name label visibly wraps across two printed lines within its column (`01-95　総務本省一般行政に必要` / `な経費`).
- **ME4 — Standard amount triple: PASS.** The row visibly carries the document's standard three-column relationship (前年度予算額 / 6年度概算要求額 / 対前年度比較増△減) in its native layout, structurally analogous to case-001/002's previous/current/delta triple. (Values themselves are not transcribed here — see "Ground Truth freeze" below.)
- **ME5 — Sufficiency: PASS.** All three amount-triple columns are visible together on this single page; nothing is split across a page boundary.

## Non-criteria confirmation

The following were **not** used to prefer, reject, or rank this row, or any of the two rejected candidates: presence/absence of `△`; sign of the delta; hierarchy ambiguity on this or any other page; placement of the 備考 (remarks) column relative to the amount triple; any expectation about Docling/pdf.js-baseline/pymupdf-baseline behavior; apparent difficulty or ease; similarity to case-001/case-002; policy importance; the specific magnitude of any amount; representativeness; or proximity to the universe's page-range boundary. Rows #1 and #2 were rejected solely because they failed ME2 (no expense-level code) — a criterion frozen before this task began — not for any of the reasons above.

## Incidental observations (recorded, not used to influence selection)

- While paging through `総表` (PDF pages 5–8) purely to resolve the PDF-index-to-printed-page mapping, organization-level aggregate totals for all five organizations (010, 040, 050, 070, 080) were incidentally visible, since `総表` is a whole-ministry summary table. This was unavoidable given that the only way to reach the start of organization 010's `明細表` was to page past the preceding summary table. No row-level detail content for organizations 040/050/070/080 was viewed (only their aggregate totals, in `総表`, which is itself excluded from `明細表` eligibility by ME1 regardless of organization), and this observation did not influence the choice of universe (already frozen in the prior task) or the selection within it.
- The selected row's own amount-triple values and delta sign were visible during ME4 verification (necessarily, since ME4 requires confirming the triple's presence). Per this task's instructions, they are deliberately **not transcribed** into this record beyond the qualitative structural confirmation above (see "Ground Truth freeze").
- The two rejected candidate rows' own aggregate totals were also visible during ME2 evaluation; likewise not transcribed, since they are not needed to establish the first-failing-criterion determination already recorded above.

## Ground Truth freeze

**No Ground Truth was created in this task.** `previousBudget`, `fy2024Request`, `deltaRaw`, `delta`, `unit`, and the normalized/curated item/expense names were **not** fully transcribed, **not** normalized, and **no arithmetic consistency check** was performed, even though the amount triple was visually confirmed present (ME4) and therefore partially observed. `fixtures/document-understanding/case-003/ground-truth.json` does not exist. Ground Truth creation is explicitly deferred to a separate, later task, per the stop condition in the frozen protocol.

## Contamination controls

- Docling: not run against this source.
- `pdfjs-baseline` / `pymupdf-baseline` (benchmark): not run.
- `npm run docbench` / document-understanding benchmark: not run.
- MinerU: not run.
- PaddleOCR / PP-Structure: not run.
- OCR or LLM/vision extraction intended to identify or rank candidate rows: none used. Page images were viewed directly by the same agent conducting this task, exactly as a human would view a rendered PDF page.
- Ground Truth: does not exist; not consulted.
- No selection criterion (ME1–ME5), non-criterion, universe, or tie-break was changed at any point during or after this inspection.
- Rendered page images and crops produced during this task are scratch artifacts under `/tmp` (outside the repository) and were not committed.

## Stop condition

Selection is frozen by this commit. The next task is Ground Truth creation for the row identified above, through direct visual source inspection, still before any benchmark engine is run against it — mirroring `fixtures/document-understanding/case-002/20260926_0908_Case002_Ground_Truth_Evidence.md`'s method for case-002.
