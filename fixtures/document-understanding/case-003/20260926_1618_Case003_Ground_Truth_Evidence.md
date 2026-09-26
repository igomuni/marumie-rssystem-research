# case-003 Ground Truth Evidence — MIC (総務省) FY2024 Detailed Expenditure Request

Status: **Ground Truth frozen. No benchmark engine has been run.**

Date: 2026-09-26 (Asia/Tokyo)

This document is the provenance/evidence record for `fixtures/document-understanding/case-003/ground-truth.json`. It exists so a reviewer can independently verify every Ground Truth field against the source, without needing any benchmark-engine output — the same purpose case-001's and case-002's equivalent evidence documents serve.

`ground-truth.json`'s `result` object uses the exact same field set as case-001/case-002's (`itemCode`, `itemName`, `requestNo`, `expenseCode`, `expenseName`, `previousBudget`, `fy2024Request`, `deltaRaw`, `delta`, `unit`, `page`), so the unchanged `evaluate.mjs` can score case-003 with no benchmark-code modification.

## Provenance chain

- Source acquired/locked: `fixtures/document-understanding/case-003/20260926_1443_Case003_MIC_Source_Survey.md`
- Selection protocol frozen: `fixtures/document-understanding/case-003/20260926_1548_Case003_Selection_Protocol.md` (commit `8b65364`)
- Target row selected/frozen: `fixtures/document-understanding/case-003/20260926_1603_Case003_Selection_Record.md` (commit `31c4626`)
- This document and `ground-truth.json`: created after the above, still before any benchmark engine has been run against MIC.

## Source and location (re-verified in this task)

- `sourceId`: `mic-fy2024-general-account-expenditure-request`
- Locked SHA-256 (`sources/source-lock.json`): `cc54dbe5f689116619a1f8453747d47bca5b960137f90869ead26954d651703b`
- Locally recomputed SHA-256 (`shasum -a 256 sources/raw/mic-fy2024-general-account-expenditure-request.pdf`) in this task: `cc54dbe5f689116619a1f8453747d47bca5b960137f90869ead26954d651703b` — **exact match**
- Selected row: PDF page 9 (1-based) / index 8 (0-based), printed page `総(本) 5` — per the already-frozen selection record. The row identity was not changed.

## Acquisition method

Direct visual inspection of the locked PDF, rendered with `pdftoppm` (poppler — a rasterizer with no text/layout reconstruction; not one of the three compared engines `pdfjs-dist`/`pymupdf`/`docling`). Renders used:

- 400 dpi full-page render of PDF page 9, viewed directly.
- A precise native crop of the target-row band (`pdftoppm -x 0 -y 650 -W 4678 -H 200 ... -r 400`) to confirm every character, digit, comma, and the absence/presence of `△` at full legibility.
- A precise native crop of the unit-label region (`pdftoppm -x 3900 -y 350 -W 778 -H 100 ... -r 400`) to confirm the unit text exactly.

No OCR, LLM, or vision-model extraction was used at any point — every value below was read directly from the rendered page image by the same agent conducting this task, the same way a human reading the PDF in a viewer would. Docling, pdf.js-baseline, pymupdf-baseline, MinerU, PaddleOCR, and `npm run docbench` were not run against this source before or during this task.

## Raw visual text vs. normalized Ground Truth value

| Field | Raw visual text (as printed) | Normalization applied | Normalized value (in `ground-truth.json`) |
|---|---|---|---|
| Item code | `010` (label: `010 総務本省共通費`) | none | `"010"` |
| Item name | `総務本省共通費` (single printed line, does not wrap) | none | `"総務本省共通費"` |
| Request number | `①` (circled numeral one, U+2460) | circled-numeral → plain digit string, the same convention case-001/case-002 use (e.g. case-002's own `"1"` for its own `①`) | `"1"` |
| Expense code | `01-95` | none | `"01-95"` |
| Expense name | Wraps across two printed lines: line 1 `01-95　総務本省一般行政に必要`, line 2 `な経費` (the code and the first part of the label share the wrapped line; the label itself is what wraps) | Line-break join with no inserted space — CJK text does not use inter-word spaces, the same convention already documented for case-001/case-002 | `"総務本省一般行政に必要な経費"` |
| Previous budget | `38,472,070` | Comma-group removed, parsed as integer | `38472070` |
| FY2024 request | `41,763,907` | Comma-group removed, parsed as integer | `41763907` |
| Delta | `3,291,837` — **no `△` glyph precedes this value anywhere in the cell**, confirmed at 400 dpi in a dedicated full-width row-band crop | Comma-group removed; sign is positive because no decrease glyph was observed — **not** inferred from `fy2024Request − previousBudget` | `deltaRaw: "3,291,837"`, `delta: 3291837` |
| Unit | `(単位: 千円)`, printed once directly below the table title, above the column headers, applying to the whole page's table | Parenthetical/label wrapper removed, leaving the bare unit word — same normalization as case-001/case-002's `"千円"` | `"千円"` |
| Printed page label | `総(本)　5` (top-right corner of the page) | none | `"総(本) 5"` |

No field was ambiguous or illegible at 400 dpi. Nothing was marked unknown.

## Sign handling

The delta cell was visually inspected specifically for the `△` glyph in a dedicated high-resolution crop of the full row band; no glyph is present, and the digits read cleanly as `3,291,837` with no leading mark of any kind. Unlike case-002 (which cross-checked against six neighboring rows on the *same page* that visibly carry `△`), **no row on page 9 itself carries a `△` glyph** — every delta visible on this specific page (organization/item/expense totals down to the individual allowance line items) is positive. This is recorded as an honest limitation of same-page cross-validation, not glossed over. However, the `△` glyph convention is independently confirmed to be a real, actively rendered feature of this same document and organization: PDF page 10 (within the same `010 総務本省` universe, previously rasterized during the case-003 source survey for a general structural-layout purpose, not for row selection or Ground Truth) visibly shows multiple `△`-marked decreases (e.g. `95016-2111-05-1300 国際機関等派遣職員給与` and `95016-2151-05-1400 公務災害補償費`, both with a visible `△` before their delta figures). This rules out the absence on page 9 being a font-rendering or extraction-tooling artifact — the glyph is genuinely used elsewhere in this exact document, and its absence on the target row's own line is a genuine positive delta, not a suppressed or unrendered negative one.

The normalized `delta` is therefore recorded as **positive** (`3291837`) strictly because the source does not visually show a decrease indicator on this row — not because arithmetic suggested a sign either way.

## Arithmetic consistency check

```text
fy2024Request - previousBudget == delta
41,763,907    - 38,472,070     == 3,291,837
3,291,837                      == 3,291,837   -> PASS
```

This check was run **after** all three values were independently transcribed from the rendered image, strictly as a consistency check on the already-recorded transcription — no value was adjusted to make it pass, and none needed to be.

## Unit handling

The unit label `(単位: 千円)` is printed once at the top of the `明細表` table on this page, directly beneath the table title (`令和6年度歳出概算要求額明細表`) and above the column headers — applying to the entire page's table, the same page-level scope already documented for case-002's target page. It was independently re-verified via a dedicated high-resolution crop of the unit-label region. This confirmation is scoped to **this page only** — it is not generalized to any other page of the 454-page document, including other pages within the same `010 総務本省` organization, per the frozen protocol's instruction not to infer unconfirmed structural facts.

## Comparison with prior cases (research context, not new Ground Truth evidence)

This section captures useful observations from treating case-003 as a continuation of the same research program, not as fields that feed into `ground-truth.json` or that change any benchmark logic.

**Materially similar to case-002:**
- The selected row is, structurally, the same kind of row as case-002's: the first `①`-numbered, expense-coded (`NN-NN` format) row under the ministry's own headquarters common-expense item header (`010 [ministry]共通費`), titled `[ministry]一般行政に必要な経費`. This did not happen by copying case-002's row — it is the deterministic first-eligible row under both cases' independently-applied, near-identical eligibility criteria, applied to two different ministries' documents. That the same template position produces the same *kind* of row in both cases is itself a useful structural observation about how these government budget-request documents are conventionally organized (first item under the first organization is almost always the ministry's own general-administration line), not a coincidence requiring explanation.
- Both target pages carry a page-level `(単位: 千円)` unit label in the same position (top of the table, above the column headers) — this matches case-002's page (which had the label) rather than case-001's page (which lacked it), consistent with case-002's own H4 finding that unit-label presence is page-context-dependent rather than a fixed per-document property.
- Both rows' expense-name labels wrap across exactly two printed lines with no inter-word space at the join point (a general CJK-text convention, not ministry-specific).
- The document producer/toolchain fingerprint (`List Creator`, A4 landscape) matches case-002's METI source exactly, already noted in the source survey.

**Structurally similar but different in actual content:**
- Case-002's expense-name line wrapped with an annotation column (`（要求要旨）`) visible on the *same reconstructed line* as the amount triple in flat-text extraction — this was the specific structural feature that broke `common.mjs`'s trailing-triple regex. On case-003's target row, the equivalent 備考 (remarks) column is **empty** for this specific row (no annotation text is visible in that column for row ①) — visually, nothing analogous to case-002's same-line annotation contamination risk is present *for this row*. Whether this holds for other rows in the same document is unknown and was not investigated (per the protocol's non-criteria list, annotation placement was correctly not used to select this row).
- Case-002's page had **no** `△`-marked rows visible during its own Ground Truth creation cross-check being needed for a genuinely glyph-free delta; case-003's target page (page 9) also shows no `△`-marked rows, but for a different underlying reason worth distinguishing: case-002 checked six *other* rows on its own page and found them `△`-marked (contrasting with its own glyph-free target), whereas case-003's entire page 9 is uniformly positive, and the `△` convention only became independently verifiable by reference to a *different* page (page 10) within the same organization. This is a weaker same-page cross-validation than case-002's, honestly disclosed above.

**Whether a prior known issue appears potentially relevant:** Unknown, and not testable in this task by design — whether `common.mjs`'s trailing-triple regex, the CJK-wrap-space-closing gap, or Docling's grid-density behavior will reproduce, differ, or not apply at all on case-003 is exactly what the first case-003 benchmark run (not part of this task) will reveal.

**Genuinely new observation:** MIC's document nests an additional intermediate breakdown level not seen in case-001/case-002's target rows — beneath the selected row (`①01-95`), the document further breaks the same expense down into `001 既定定員に伴う経費` → `001 人件費` → individual numbered allowance lines (`95016-2111-02-0000 職員基本給`, etc.), all still on the same page. Case-001/case-002's selected rows did not visibly nest this deeply on their own target pages. This is recorded as an observation for future reference (e.g. for understanding hierarchy-ambiguity candidate sets on this document), not as a Ground Truth field, and does not affect any value in `ground-truth.json` above.

**Confirmation:** every value in `ground-truth.json` was determined solely from direct visual inspection of the locked MIC source; the comparisons in this section informed *what to look for and what to note*, not *what value to write down*. No case-002 value was copied or substituted for a case-003 value at any point.

## Contamination controls

- Docling: not run against this source.
- `pdfjs-baseline` (benchmark): not run.
- `pymupdf-baseline` (benchmark): not run.
- `npm run docbench` / document-understanding benchmark: not run.
- MinerU: not run.
- PaddleOCR / PP-Structure: not run.
- No prior or newly generated normalized engine output for MIC was consulted.
- Ground Truth was derived solely from direct visual inspection of the rasterized source page, per the method above.

## What this task did not do

This task did not modify case-001's or case-002's Ground Truth, evidence, or results; the selection protocol or selection record (both re-verified byte-identical to their freeze commits before this task began); any benchmark evaluator, normalizer, adapter, or check definition; or the Case Package schema. `ground-truth.json`'s `result` schema is identical in shape to case-001/case-002's, so no benchmark-code change was needed to accommodate case-003.
