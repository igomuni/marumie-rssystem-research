# Case-008 Ground Truth Evidence — Courts

Status: **Ground Truth evidence for the already frozen selected row.**

Date: 2026-09-28 19:54 (Asia/Tokyo)

## 1. Purpose

Record direct visual source transcription for Case-008's one already-selected standard-ledger row, then freeze the corresponding `ground-truth.json`. The source of truth in this task is the locked PDF render only.

## 2. Frozen selection reference

- Source Survey: `e10d56c529ce9c8197f71dd71df32297ea3675fb`
- Selection Protocol: `3cf4a4f23f036c96cae6852f97a8a17801725299`
- Selection Record: `0ccea62537dea8b97e2792a4ced1f70bd5f95f85`

The selection was not repeated. The frozen locator was re-verified before reading amounts.

## 3. Source SHA and integrity

`sha256sum` of `sources/raw/courts-fy2024-general-account-expenditure-request.pdf` returned:

`df43f2dc183da84fa9952ae4c5e17888177df186ad4c556ed1a519ba584e3c06`

This exactly matches the locked source ID `courts-fy2024-general-account-expenditure-request` (736,439 bytes). No source was downloaded, replaced, or relocked.

## 4. Fresh render method

Freshly rendered the physical PDF page 7 (`pdfPageIndex` 6) with:

`pdftoppm -f 7 -l 7 -r 400 -png -singlefile`

Source-preserving crops of the target row and unit area were then visually inspected. They were temporary files under `/private/tmp`, not repository artifacts. No OCR or text extraction was used to recognize target-row text or digits.

## 5. Locator re-verification before amount transcription

The fresh render visibly shows all of the following before the three amount values were transcribed:

| Field | Fresh visual source evidence |
|---|---|
| Physical locator | PDF page 7 / `pdfPageIndex` 6 / printed `裁（裁）3` |
| Standard-ledger grammar | title `令和6年度歳出概算要求額明細表` and standard request/事項/three-amount/remarks header |
| Organization | `010 裁判所` |
| Item | `010 最高裁判所` |
| Request number | `①` |
| Expense code | `01-95` |
| Section | standard ledger, not summary/staffing/policy-framework/local calculation box |

No locator or identity mismatch was found.

## 6. Identity transcription

- Organization raw/normalized: `010 裁判所` / `010 裁判所`
- Item raw/normalized: `010 最高裁判所` / `010 最高裁判所`
- Request number raw/normalized: `①` / `1`
- Expense code raw/normalized: `01-95` / `01-95`

## 7. Expense-name raw lines and normalization

- Raw line 1: `最高裁判所の事務処理に`
- Raw line 2: `必要な経費`
- Normalized: `最高裁判所の事務処理に必要な経費`

Normalization joins the visual wrap only. No source-absent whitespace, punctuation, or character correction was inserted.

## 8. Independent amount transcription: raw to normalized

The following entries were read independently from the selected physical row before arithmetic was performed.

| Field | Raw visual string | Normalization rule | Normalized integer |
|---|---|---|---:|
| previousBudget | `68,535,874` | remove comma grouping | 68535874 |
| fy2024Request | `80,989,261` | remove comma grouping | 80989261 |
| delta | `12,453,387` | remove comma grouping | 12453387 |

## 9. Delta glyph and sign evidence

The selected row's delta cell visibly reads `12,453,387` with **no `△` glyph or other negative marker**. Raw `deltaRaw` is therefore `12,453,387`; normalized delta is positive `12453387`. The sign was determined from the source glyph before arithmetic validation.

## 10. Unit evidence and scope

- Raw visual unit text: `（単位:千円）`
- Normalized unit: `千円`
- Evidence locator: selected page, `pdfPageIndex` 6, top-right standard-ledger header area
- Scope: standard `歳出概算要求額明細表` section

The same PDF's staffing-table 人 unit and other local non-ledger units do not govern this row.

## 11. Remarks evidence

The selected row's own remarks cell is visually **empty**. No neighboring-row remarks were inherited. `ground-truth.json` records this as the empty string (`""`), not an inferred description.

## 12. Arithmetic validation

Only after all three values and the source sign were independently transcribed, the validation calculation was made:

`80,989,261 - 68,535,874 = 12,453,387`

Result: **PASS**. This validates the independent transcription; it was not used to derive or alter any transcribed value.

## 13. Ambiguities

None. The 400dpi full-page render and source-preserving row crop made identity, each amount cell, sign state, unit, and empty remarks cell legible. No OCR or additional interpretation was needed.

## 14. Contamination audit

Before and during this freeze, this task did not read or use benchmark raw output, normalized extractor output, evaluator output, MOF/RS records, a prior expected value, or production logic. Arithmetic occurred only after independent visual transcription. No GT value was hard-coded into production code. Earlier selection-task amount exposure is disclosed by the Selection Record; it did not supply a saved amount transcription and was not used as GT evidence.

## 15. Multi-grammar provenance

This Ground Truth belongs to the same locked 127-page file as the staffing and policy-framework material, but specifically to its standard-ledger section at index 6. The standard-ledger title/header, hierarchy, and section-local 千円 declaration establish that provenance; file identity alone would not.

## 16. Explicit non-actions and next handoff

No benchmark engine, OCR system, parser/normalizer/evaluator change, MOF/RS linkage, or production adaptation was run or made. The next task is to run the existing, unmodified benchmark pipeline against this frozen Case-008 Ground Truth for the first time.

---

**Ground Truth was frozen from direct visual source evidence for the already-selected Case-008 standard-ledger row. No benchmark engine or OCR system was run before or during the freeze, and no frozen selection artifact was modified.**
