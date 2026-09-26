# case-004 Ground Truth Evidence — MEXT (文部科学省) FY2024 Detailed Expenditure Request

Status: **Ground Truth frozen. No benchmark engine has been run.**

Date: 2026-09-26 (Asia/Tokyo)

This document is the provenance/evidence record for `fixtures/document-understanding/case-004/ground-truth.json`. It exists so a reviewer can independently verify every Ground Truth field against the source, without needing any benchmark-engine output — the same purpose case-001/002/003's equivalent evidence documents serve.

`ground-truth.json`'s `result` object uses the exact same field set as case-001/002/003's (`itemCode`, `itemName`, `requestNo`, `expenseCode`, `expenseName`, `previousBudget`, `fy2024Request`, `deltaRaw`, `delta`, `unit`, `page`), so the unchanged `evaluate.mjs` can score case-004 with no benchmark-code modification. No incompatibility with the existing schema was found.

## Provenance chain

- Source acquired/locked: `fixtures/document-understanding/case-004/20260926_2029_Case004_MEXT_Source_Survey.md`
- Selection protocol frozen: `fixtures/document-understanding/case-004/20260926_2045_Case004_Selection_Protocol.md` (commit `c2b2c28`)
- Target row selected/frozen: `fixtures/document-understanding/case-004/20260926_2101_Case004_Selection_Record.md` (commit `fa82c13`)
- This document and `ground-truth.json`: created after the above, still before any benchmark engine has been run against MEXT.

## Source and location (re-verified in this task)

- `sourceId`: `mext-fy2024-general-account-expenditure-request-detail`
- Locked SHA-256 (`sources/source-lock.json`): `6df221dfd22c48e0f32dd59bcf2dbcbaad19720083be43005ce700b984a6bf71`
- Locally recomputed SHA-256 (`shasum -a 256 sources/raw/mext-fy2024-general-account-expenditure-request-detail.pdf`) in this task: `6df221dfd22c48e0f32dd59bcf2dbcbaad19720083be43005ce700b984a6bf71` — **exact match**
- Page count re-verified via `pdfinfo`: 1,339 — unchanged.
- Selection protocol (`20260926_2045_Case004_Selection_Protocol.md`) re-verified byte-identical to `c2b2c28`; selection record (`20260926_2101_Case004_Selection_Record.md`) re-verified byte-identical to `fa82c13`.
- Selected row (re-verified visually against the source before transcription, matches the frozen locator exactly): PDF page 3 (1-based) / index 2 (0-based), printed page `文（本） 11`, organization `010 文部科学本省`, item `010 文部科学本省共通費`, request no. `①`, expense code `01-95`. **No discrepancy was found; the row identity was not changed.**

## Acquisition method

Direct visual inspection of the locked PDF, rendered with `pdftoppm` (poppler — a rasterizer with no text/layout reconstruction; not one of the three compared engines `pdfjs-dist`/`pymupdf`/`docling`). Renders used:

- 400 dpi full-page render of PDF page 3 (`pdfPageIndex` 2), viewed directly.
- A precise crop of the top band of the same page (`-x 0 -y 0 -W 4678 -H 350`) to confirm whether any unit label is present above the column headers (see "Unit evidence" below).
- A precise crop of the target row's own band (`-x 0 -y 120 -W 4678 -H 320`) at 400 dpi, to confirm every character, digit, comma, and the absence/presence of `△` at full legibility.
- The document's own page 1 (`pdfPageIndex` 0) and page 2 (`pdfPageIndex` 1), already rasterized during the case-004 selection task, were re-examined (not re-rendered) for corroborating unit-label and `△`-glyph evidence, per the permitted-corroboration rule below.

No OCR, LLM, or vision-model extraction was used at any point — every value below was read directly from the rendered page image by the same agent conducting this task, the same way a human reading the PDF in a viewer would. Docling, pdf.js-baseline, pymupdf-baseline, MinerU, PaddleOCR, and `npm run docbench` were not run against this source before or during this task, and no prior case-004 engine output exists to consult (confirmed absent in §1 of this task).

## Raw visual text vs. normalized Ground Truth value

| Field | Raw visual text (as printed) | Normalization applied | Normalized value (in `ground-truth.json`) |
|---|---|---|---|
| Item code | `010` (label, on the immediately preceding page, `pdfPageIndex` 1: `010　文部科学本省共通費`) | none | `"010"` |
| Item name | `文部科学本省共通費` (single printed line, does not wrap, read from `pdfPageIndex` 1's own item-header row — this is the item the selected row's own code falls under, not the selected row's own line) | none | `"文部科学本省共通費"` |
| Request number | `①` (circled numeral one, U+2460) | circled-numeral → plain digit string, the same convention case-001/002/003 use | `"1"` |
| Expense code | `01-95` | none | `"01-95"` |
| Expense name | Wraps across two printed lines: line 1 `01-95　文部科学本省一般行政に`, line 2 `必要な経費` (the code and the first part of the label share the wrapped line; the label itself is what wraps — the same joint-line convention already documented for case-003) | Line-break join with no inserted space — CJK text does not use inter-word spaces, the same convention already documented for case-001/002/003 | `"文部科学本省一般行政に必要な経費"` |
| Previous budget | `95,208,241` | Comma-group removed, parsed as integer | `95208241` |
| FY2024 request | `95,686,830` | Comma-group removed, parsed as integer | `95686830` |
| Delta | `478,589` — **no `△` glyph precedes this value anywhere in the cell**, confirmed at 400 dpi in a dedicated full-width row-band crop | Comma-group removed; sign is positive because no decrease glyph was observed — **not** inferred from `fy2024Request − previousBudget` | `deltaRaw: "478,589"`, `delta: 478589` |
| Unit | **Not present on the selected row's own page** (`pdfPageIndex` 2); see "Unit evidence and scope" below for the full disclosure | Parenthetical/label wrapper removed from the document-level source text, same normalization as case-001/002/003's `"千円"` | `"千円"` (document/table-level scope, not page-level — see below) |
| Printed page label | `文（本）　11` (top-right corner of the page) | none | `"文（本） 11"` |

No field was ambiguous or illegible at 400 dpi. Nothing was marked unknown.

## Delta glyph/sign evidence

The delta cell was visually inspected specifically for the `△` glyph in a dedicated high-resolution crop of the full row band; no glyph is present, and the digits read cleanly as `478,589` with no leading mark of any kind — the raw cell text is exactly `478,589`.

**Corroboration (document-level, not target-row evidence):** the selected row's own page (`pdfPageIndex` 2) carries no `△`-marked row to cross-check against. Per this task's own permitted-corroboration rule, another already-accessible page within the same locked source was used solely to confirm that `△` is a genuinely rendered, active convention in this document (not a font/rendering artifact that could silently suppress a real negative sign): `pdfPageIndex` 0 (the organization-level `010 文部科学本省` aggregate row, already visually inspected during the prior selection task) visibly shows `△　265,028,183`. This confirms the glyph renders correctly elsewhere in the same document and is not a font-rendering gap. It was **not** used to infer the target row's own sign — the target row's sign was determined solely from the absence of any `△` mark in its own cell, exactly as required.

The normalized `delta` is therefore recorded as **positive** (`478589`) strictly because the source does not visually show a decrease indicator on this row — not because arithmetic suggested a sign either way.

## Unit evidence and scope

**Raw observation, disclosed exactly as found:** no unit text of any kind is visually present on the selected row's own page (`pdfPageIndex` 2, printed `文（本） 11`) — confirmed via a dedicated high-resolution crop of the full top band of that page, which shows only the page's printed-label corner and the column-header row, with nothing above it. The immediately preceding page (`pdfPageIndex` 1, printed `文（本） 10`) similarly carries no unit text — only a page-corner label and the column headers.

The unit label `(単位：千円)` is printed exactly once in the entire visually-inspected range: on `pdfPageIndex` 0 (printed `文（本） 9`), the document's own first page, directly beneath the document-wide table title (`令和6年度歳出概算要求額明細表`) and the sheet header (`24　文部科学省所管`), above that same page's own column headers.

**This is a genuine, disclosed difference from case-002/003**, both of whose target pages carried the unit label directly, in the page-level scope already documented for those cases. For MEXT, the label is not repeated per page; it is stated once, at the start of the entire detail table, and — per ordinary convention for this kind of ledger document, and absent any contradicting unit text anywhere in the pages actually inspected (`pdfPageIndex` 0–2) — applies to the whole table that follows, not solely to the one page it happens to be printed on.

**Normalized value and scope, stated honestly:** `unit: "千円"` is recorded, but its scope is **table-level, established from the document's own first page (`pdfPageIndex` 0), not independently confirmed on the target row's own page** — a materially weaker basis than case-002/003's direct same-page confirmation. This scope distinction is recorded here, in `ground-truth.json`'s own `notes` field, and in the comparison section below, specifically so a future reviewer does not mistake this for the same page-level guarantee case-002/003 had. It is **not** generalized beyond the actually-inspected pages (`pdfPageIndex` 0–2) to the remaining ~1,336 pages of the file.

## Arithmetic consistency check

```text
fy2024Request - previousBudget == delta
95,686,830    - 95,208,241     == 478,589
478,589                        == 478,589   -> PASS
```

This check was run **after** all three values were independently transcribed from the rendered image, strictly as a consistency check on the already-recorded transcription — no value was adjusted to make it pass, and none needed to be.

## Subordinate-breakdown delimitation

The selected row's own page (`pdfPageIndex` 2) begins with the target row's own header line (`①　01-95　文部科学本省一般行政に必要な経費`, previous budget `95,208,241`, FY2024 request `95,686,830`, delta `478,589`), immediately followed — still on the same page, and continuing beyond it — by an extensive breakdown of numbered sub-line-items (`001　既定定員に伴う経費` → `001　人件費` → individually numbered allowance lines such as `95016-2111-02-0000　職員基本給`, each carrying its own previous/current/delta triple). **No ambiguity existed**: the target row's own amount triple is printed directly beside its own header line, at the top of the page, structurally distinguishable from every subordinate line by (a) position — it is the first, unindented row on the page, directly under the column headers, while every subordinate line is progressively indented beneath it, and (b) content — only the header line carries the row's own request number (`①`) and expense code (`01-95`); no subordinate line carries either. The subordinate lines were not aggregated, not used to double-check or replace the target's own amount triple, and are not represented as separate Ground Truth targets or additional schema fields.

## Comparison with prior cases (research context, not new Ground Truth evidence)

This section captures useful observations from treating case-004 as a continuation of the same research program, not as fields that feed into `ground-truth.json` or that change any benchmark logic. No case-002/003 numeric or string value was copied or substituted for any case-004 value at any point; the comparisons below informed *what to look for*, never *what value to write down*.

**Similar (actually observed, not assumed):**
- The selected row is, structurally, the same kind of row as case-002's and case-003's: the first `①`-numbered, expense-coded (`NN-NN` format) row under the ministry's own headquarters common-expense item header (`010 [ministry]共通費`), titled `[ministry]一般行政に必要な経費`. This is the deterministic first-eligible row under near-identical eligibility criteria applied independently to a third ministry's document, not a copied choice.
- The expense-name label wraps across exactly two printed lines with no inter-word space at the join point, and the code shares its first line with the label's own start — the same convention already documented for case-003.
- The document producer/toolchain fingerprint for the sibling cover/TOC files (`List Creator`, A4 landscape) resembles case-002/003's METI/MIC sources, already noted in the source survey (though the target file itself, uniquely among the three cases, has no recorded `Producer`).

**Different (genuine source differences, actually observed):**
- **Unit-label placement**: unlike case-002/003, whose target page directly carried `(単位：千円)`, MEXT's unit label is stated once on the document's own first page and not repeated on the target's own page — a genuinely weaker same-page confirmation basis, fully disclosed above.
- **Subordinate breakdown**: the selected row is followed by an unusually extensive, deeply-nested numbered sub-line-item breakdown (already flagged in the selection record) — deeper and more extensive than case-001/002's target rows, and structurally similar in *kind* (though not depth) to case-003's own single extra intermediate level.
- **Remarks column**: visually empty for the target row (no annotation text), the same as case-003's target row — unlike case-002's same-line annotation contamination.
- **Packaging/encryption**: the source itself is a standalone 明細表-only file, encrypted (permission-only AES-256) — both already established in the source survey and selection protocol, not new findings of this task, but relevant context for why the unit-label placement differs (a combined file's 明細表 section, as in case-002/003, apparently repeats or is entered close enough to its own section start that the label lands on the target page; a document that is itself only the 明細表, starting exactly at its own title page, apparently states the label once at that title and does not repeat it a few pages later).

**New (genuinely new observation, not previously seen in case-001/002/003):**
- The document-wide unit-declaration-once-per-table convention (rather than a per-page repetition) had not been previously distinguished from a per-page convention in this research program, because case-001/002/003's target pages all happened to carry the label directly. This is recorded as a new, source-grounded observation about how unit scope should be represented and evidenced for future cases — not a Ground Truth field, and not a reason to change `evaluate.mjs`'s existing unit-check semantics in this task.

**Whether a prior known issue appears potentially relevant:** Unknown, and not testable in this task by design — whether `common.mjs`'s trailing-triple regex, the CJK-wrap-space-closing gap, or Docling's grid-density behavior will reproduce, differ, or not apply at all on case-004 is exactly what the first case-004 benchmark run (not part of this task) will reveal.

## Ambiguity assessment

No field was genuinely ambiguous or illegible. The one substantive judgment call made explicit in this document is the unit-scope disclosure above (table-level vs. page-level), which is a documented scope distinction, not an unresolved value — the unit text itself (`千円`) was read unambiguously from `pdfPageIndex` 0.

## Contamination controls

- Docling: not run against this source.
- `pdfjs-baseline` (benchmark): not run.
- `pymupdf-baseline` (benchmark): not run.
- `npm run docbench` / document-understanding benchmark: not run.
- MinerU: not run.
- PaddleOCR / PP-Structure: not run.
- No prior or newly generated normalized engine output for MEXT was consulted (none exists).
- Ground Truth was derived solely from direct visual inspection of the rasterized source pages, per the method above.

## What this task did not do

This task did not modify case-001/002/003's Ground Truth, evidence, or results; the selection protocol or selection record (both re-verified byte-identical to their freeze commits before this task began); any benchmark evaluator, normalizer, adapter, or check definition; the Case Package schema; or the source lock/raw binary (re-verified unchanged). `ground-truth.json`'s `result` schema is identical in shape to case-001/002/003's, so no benchmark-code change was needed to accommodate case-004. No benchmark engine, OCR tool, or `npm run docbench` was run against MEXT before this Ground Truth freeze commit.
