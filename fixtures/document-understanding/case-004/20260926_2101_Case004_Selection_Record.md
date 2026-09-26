# case-004 Selection Record — MEXT (文部科学省) FY2024 Detailed Expenditure Request

Status: **row selected and frozen. No Ground Truth. No benchmark engine run against MEXT.**

Date: 2026-09-26 (Asia/Tokyo)

This record applies the already-frozen `fixtures/document-understanding/case-004/20260926_2045_Case004_Selection_Protocol.md` (committed `c2b2c28`) exactly, through direct visual inspection only. It does not redesign, reinterpret, or weaken the protocol.

## Protocol identity and freeze commit

- Protocol file: `fixtures/document-understanding/case-004/20260926_2045_Case004_Selection_Protocol.md`
- Freeze commit: `c2b2c28`
- Verified byte-identical to the frozen commit before this task's first edit (`git diff c2b2c28 -- <protocol path>` → empty).

## Source ID and locked SHA-256

- `sourceId`: `mext-fy2024-general-account-expenditure-request-detail`
- SHA-256: `6df221dfd22c48e0f32dd59bcf2dbcbaad19720083be43005ce700b984a6bf71` — re-verified against `sources/source-lock.json` and independently via `shasum -a 256` on the local raw file, both matching, unchanged.

## Inspection method

Direct visual inspection only: `pdftoppm -png -r 200` rasterization of the locked PDF (poppler, not one of the three compared engines), followed by direct human-style reading of the rendered page images. No `pdfjs-baseline`, `pymupdf-baseline`, `docling`, MinerU, PaddleOCR, OCR, `npm run docbench`, or any prior engine-derived MEXT artifact was used at any point. `pdfinfo` was used only to confirm page count/encryption metadata (already known from the source survey, re-confirmed here). Rasterization succeeded despite the document's permission-only AES-256 encryption, consistent with the source survey's finding; encryption did not block or otherwise influence this inspection. Rendered PNGs were written to this session's scratch directory (outside the repository) and are not part of this commit.

## Frozen universe

Organization `010　文部科学本省`, per the protocol: approximately `pdfPageIndex` 0–894 (printed pages ~9–903), upper boundary against organization `020` recorded as approximate.

## Boundary clarification performed at selection time

**None was necessary and none was performed.** The first eligible row (below) was found at `pdfPageIndex` 2 — three pages into a universe whose approximate span is ~895 pages — far short of the uncertain `010`→`020` boundary. Resolving the exact boundary would have required additional structural navigation with no bearing on which row wins, so it was not performed, per the protocol's and this task's own explicit instruction not to scan pages merely to perfect unused metadata. The approximate TOC-derived boundary from the frozen protocol is preserved unchanged; this record does not retroactively edit it.

## Enumeration sequence (document order, `pdfPageIndex` ascending, top-to-bottom on each page)

| `pdfPageIndex` | Printed label | Row observed | MX1 (native code) | MX2 (multi-line wrap) | MX3 (amount triple) | MX4 (sufficiency) | Result |
|---|---|---|---|---|---|---|---|
| 0 | 文（本）9 | `010　文部科学本省` (組織-level total; the same row already incidentally disclosed in the source survey) | **FAIL** — no code in the code column; this is a bare organization-level aggregate | not evaluated | present, but on an ineligible row | not evaluated | **REJECTED (MX1 FAIL)** |
| 1 | 文（本）10 | `010　文部科学本省共通費` (項-level aggregate) | **FAIL** — no code in the code column; this is a bare item-level aggregate, structurally identical in kind to the ME2-failing candidates rejected at the equivalent stage in case-003's own selection record | not evaluated | present, but on an ineligible row | not evaluated | **REJECTED (MX1 FAIL)** |
| 2 | 文（本）11 | 要求番号 `①`, code `01-95`, `文部科学本省一般行政に必要な経費` | **PASS** | **PASS** | **PASS** | **PASS** | **SELECTED — first eligible row** |

Enumeration stopped immediately upon finding the first eligible row, per the protocol's tie-break and this task's own instruction not to enumerate farther or compare the winner against later rows. No page beyond `pdfPageIndex` 2 was inspected.

## Selected row locator

- `pdfPageIndex`: 2
- `pdfPageNumber` (1-based): 3
- Printed page label: `文（本） 11`
- Organization: `010　文部科学本省`
- Item (項): `010　文部科学本省共通費` (per the immediately preceding page's own item-level header, `pdfPageIndex` 1 — the item this row's own code falls under)
- Request number (要求番号): `①` (circled numeral, printed in the leftmost column, aligned with this row's first line)
- Expense code (事項 code): `01-95`
- Expense label as visually printed, literal line wrapping: line 1 `文部科学本省一般行政に` / line 2 `必要な経費` (two printed lines within the same cell)
- Expense label, human-readable joined form used only as a locator (not benchmark-normalized Ground Truth): `文部科学本省一般行政に必要な経費`

No ambiguity was observed in this locator; the printed text is clear and unbroken across its two visual lines.

## MX1–MX4 result for the selected row

- **MX1 — native code: PASS.** `01-95` is printed in the row's own code column, next to the label, in the same format already named in the sibling TOC file.
- **MX2 — multi-line wrap: PASS.** The label visually occupies two printed lines within its own cell (see literal wrapping above).
- **MX3 — standard amount triple: PASS.** The row's own three amount columns (前年度予算額 / 6年度概算要求額 / 対前年度比較増△減) are all visually present and directly associated with this row on the same page. Per this task's own instruction (§8), the specific numeric values were necessarily visible while confirming this and are **not transcribed here** — see "Ground Truth separation" below.
- **MX4 — sufficiency: PASS.** The row's code, label, and complete amount triple are all visually present on one page (`pdfPageIndex` 2); nothing required to populate the case-001/002/003-schema fields is split across a page boundary.

## Deterministic tie-break

Not needed to break a tie among multiple simultaneously-eligible rows — no other row on `pdfPageIndex` 0, 1, or 2 satisfied MX1–MX4 before this one, so the "first eligible row in document order" rule (lowest `pdfPageIndex`, then topmost position on that page) selected this row directly, with no competing candidate at the same rank.

## Confirmation: explicit non-criteria played no role

None of the following influenced this selection, though some were incidentally visible while reading the rendered pages:

- The selected row's delta (`478,589`) is **positive, no `△` glyph** — this was seen while confirming MX3, but was not a selection input in either direction (a negative/`△`-marked delta would have been equally acceptable).
- No hierarchy-ambiguity check was performed or needed; the selected row was the first, and only, coded row encountered.
- The 備考 (remarks) column is visually empty for this row and for both preceding aggregate rows — observed, not used to select for or against.
- No engine (pdf.js/PyMuPDF/Docling) was run or consulted; no expectation about any engine's behavior on this row influenced the choice.
- The document's permission-only AES-256 encryption did not block rasterization and was not tested against any engine; it played no role in row choice.
- The row's structural similarity to case-002's and case-003's own selected rows (`①01-95 [ministry]一般行政に必要な経費`) was neither sought nor avoided — it is a consequence of applying the same deterministic rule to a document that happens to share the same first-item-header convention, exactly as the task anticipated could happen.
- Perceived difficulty, convenience, novelty, and whether this row would confirm or falsify any prior hypothesis played no role.

## Contamination controls

- Enumeration proceeded strictly in document order from `pdfPageIndex` 0, using only direct visual inspection of `pdftoppm`-rendered pages.
- No prior-case Ground Truth, selection record, or benchmark output was consulted to locate or recognize this row; the resemblance to case-002/003's own selected row was recognized only after arriving at it in strict document order, not used to search for it.
- No compared engine (pdf.js, PyMuPDF, Docling), OCR tool, or `npm run docbench` was run against any MEXT page at any point in this task.
- The frozen protocol's MX1–MX4, non-criteria list, universe, and tie-break were applied unmodified; none was adjusted after viewing any row.

## Ground Truth separation

Explicitly confirmed: this task did **not** transcribe the previous-budget, current-request, or delta amounts into this record; did not normalize any amount; did not determine a signed delta value; did not perform any arithmetic consistency check; did not normalize the item/expense name into a Ground-Truth-shaped field (the "human-readable joined form" above is recorded solely as a locator, explicitly labeled as such, not as a normalized value); and did not create `ground-truth.json`. Only source-observable locator/structural information is recorded above.

## Incidental/accidental exposure disclosure

- Carried forward from the source survey (not re-obtained in this task): the `010　文部科学本省` organization-total row's own amounts (`5,149,805,046` / `4,884,776,863` / `△265,028,183`), visible again on `pdfPageIndex` 0 during this task's own enumeration. This is an aggregate row that fails MX1 outright and was never a selection candidate; it is not reframed as Ground Truth contamination, consistent with the originating task's own instruction.
- New in this task: the `010　文部科学本省共通費` item-aggregate row's own amounts (`95,994,472` / `96,240,784` / `246,312`, no `△`), visible on `pdfPageIndex` 1 while confirming it fails MX1 (no code). This, too, is an aggregate row, not a selection candidate, and is disclosed here rather than silently omitted.
- The selected row's own amount triple (previous budget, current request, and delta figures) was necessarily visible while confirming MX3, as anticipated and explicitly permitted by the originating task's §8. These values are disclosed as *having been seen* here, but are deliberately **not transcribed** into this record, per that same instruction.
- One additional structural observation, incidental to reading `pdfPageIndex` 2: beneath the selected row's own header line, the same page (and, visibly, continuing beyond it) contains an extensive breakdown of numbered sub-line-items (e.g. `95016-2111-02-0000　職員基本給`, `95016-2111-03-0000　職員諸手当`, and many further `NN-NNNN`-coded lines with a `令和5年度` staffing-count annotation block), a level of internal detail not previously observed at this position in case-001/002/003's own selected rows. This is recorded as an observation for a future task, not evaluated against MX1–MX4 and not used to reconsider the selection.

## Unresolved observations

- Whether the sub-line-item breakdown observed beneath the selected row (see above) is unique to MEXT's own `01-95` item or a general convention throughout organization `010` is unknown — not investigated, since it plays no role in this row's own eligibility (which was already established from the row's own header line, before any sub-line-item detail was visible).
- The exact `010`→`020` organization boundary remains unresolved, as explicitly permitted (see "Boundary clarification" above); it was not operationally needed to determine the winner.
- Whether the printed-page-label convention (`文（本） N`) remains stable throughout organization `010` beyond the three pages inspected here is still unknown.

## Stopping condition

This task stops here, having selected exactly one row (`pdfPageIndex` 2, request no. `①`, code `01-95`, `文部科学本省一般行政に必要な経費`) and frozen it in this record. No `ground-truth.json` was created. No benchmark engine, OCR tool, or `npm run docbench` was run against MEXT. The next task must create and freeze Ground Truth for this already-selected row through direct visual source inspection, still without running any benchmark engine.
