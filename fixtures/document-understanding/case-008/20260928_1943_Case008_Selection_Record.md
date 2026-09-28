# Case-008 Selection Record — Courts

Status: **one row selected under the frozen protocol. Ground Truth is not created in this task.**

Date: 2026-09-28 19:43 (Asia/Tokyo)

Branch: `research/case-008-courts-baseline`

Pre-task HEAD: `3cf4a4f23f036c96cae6852f97a8a17801725299`
Frozen protocol: `fixtures/document-understanding/case-008/20260928_1933_Case008_Selection_Protocol.md` at `3cf4a4f23f036c96cae6852f97a8a17801725299`

## 1. Protocol reference and freeze integrity

The frozen protocol was read in full before any candidate-row inspection. Its working-tree byte hash matched the artifact at commit `3cf4a4f`. No protocol text, criteria, universe, exclusion, tie-break, or context rule was modified.

## 2. Source identity and integrity

| Field | Value |
|---|---|
| Source ID | `courts-fy2024-general-account-expenditure-request` |
| Source SHA-256 | `df43f2dc183da84fa9952ae4c5e17888177df186ad4c556ed1a519ba584e3c06` |
| Lock result | local raw binary matched `sources/source-lock.json` exactly |
| File / section | one 127-page locked PDF / standard `歳出概算要求額明細表` ledger |

## 3. Frozen universe applied

The applied universe was unchanged from the protocol: top organization `010 裁判所`, standard-ledger grammar only, `pdfPageIndex` 6--110. The scan began at index 6. Cover/TOC, summary, blanks, staffing, policy-framework material, and nested non-target boxes remained excluded without re-evaluation.

## 4. Inspection method

One source-preserving, non-OCR visual rendering was made with `pdftoppm` at 300dpi for physical PDF page 7 (`pdfPageIndex` 6). Visual inspection, not OCR, text extraction, benchmark output, or Ground Truth, determined every criterion result. No later page was rendered or inspected after the winner was found.

## 5. Page and section identity

| Field | Evidence |
|---|---|
| `pdfPageIndex` / physical PDF page | 6 / 7 |
| Printed label | `裁（裁）3` |
| Section title | `令和6年度歳出概算要求額明細表` |
| Standard header | request number / 事項 / previous / FY2024 / delta / remarks columns visibly present |
| Organization anchor | `010 裁判所` on the same page |
| Unit evidence | `（単位：千円）` on the same standard-ledger opening page |
| Grammar verdict | P1 PASS: standard ledger, not an excluded grammar or local non-target box |

## 6. Rows evaluated before the winner

Exactly **three** top-to-bottom physical rows were evaluated on `pdfPageIndex` 6. No amount values are recorded here.

| Order | Row class / locator | C1 | C2--C4 | Result |
|---|---|---|---|---|
| 1 | organization aggregate `010 裁判所` | FAIL: no row-local request-number-plus-expense-code pair | not evaluated after C1 failure | rejected |
| 2 | internal aggregate `010 最高裁判所` | FAIL: no row-local request-number-plus-expense-code pair | not evaluated after C1 failure | rejected |
| 3 | request/expense physical row, selected below | PASS | PASS | first fully eligible row |

The first two rows are recorded only to show application of the frozen top-to-bottom tie-break; they are not amount-based rejections.

## 7. Selected row locator and identity

| Field | Selected source value |
|---|---|
| `pdfPageIndex` / printed label | 6 / `裁（裁）3` |
| Organization | `010 裁判所` |
| Item context | `010 最高裁判所` (same page, immediately preceding governing hierarchy) |
| Request number | `①` |
| Expense code | `01-95` |
| Expense label | `最高裁判所の事務処理に必要な経費` |
| Physical-row form | label visually wraps across two lines in its own cell |

## 8. Criterion application

| Criterion | Result | Source-safe reason |
|---|---|---|
| P1 correct section/grammar | PASS | index 6, standard-ledger title/header, 千円 unit, and ledger hierarchy all agree |
| P2 organization | PASS | same-page organization anchor resolves to `010 裁判所` |
| C1 native identifier | PASS | `①` and `01-95` are visibly printed on the selected physical row |
| C2 multi-line label | PASS | selected label visibly occupies two lines in its own cell |
| C3 row-local standard triple | PASS | all three standard amount cells are visibly present and associated with the selected physical row |
| C4 evidence sufficiency | PASS | row-local identity/triple, same-page item context, same-page organization, section identity, locked file identity, and same-page 千円 unit resolve without crossing a grammar boundary |

Amount values were visually exposed only to establish C3 presence. They are not transcribed, normalized, compared, or arithmetically checked in this record.

## 9. Context and unit resolution

The protocol's frozen order resolved all needed fields without ambiguity: row-local request/code/label/triple → same-page item `010 最高裁判所` → same-page organization `010 裁判所` → standard-ledger section → locked file identity. No context crossed a grammar boundary. The applicable unit is section-local **千円**, declared on the same page; staffing-table 人 and other local units were not considered.

## 10. Tie-break and stop condition

The selected row is the first fully eligible row under the frozen ordering: lowest `pdfPageIndex` in the universe (6), then third top-to-bottom evaluated row on that page after two C1-failing aggregates. The scan stopped immediately. No later row, page, grammar, or potential alternative was inspected or compared.

## 11. Prior exposure

The source survey had inspected the standard-ledger opening page for structural classification, so this result is not described as blind. Staffing and policy-framework spot-check exposure was outside this universe. Prior exposure neither changed the scan order nor influenced C1--C4 or the tie-break.

## 12. Ambiguities and unexpected observations

No unresolved ambiguity affected the selected row. The same-page visual evidence was legible at 300dpi; no higher-resolution render was required. No new grammar or structural condition requiring a protocol amendment was encountered.

## 13. Explicit non-actions

- No Ground Truth, amount transcription, normalized amount, delta transcription, or arithmetic check.
- No OCR, benchmark engine, `npm run docbench`, parser, normalizer, evaluator, MOF/RS, or production-code work.
- No protocol amendment, universe widening, excluded-grammar inspection, later-row comparison, or PR.

## 14. Next-task handoff

Freeze Ground Truth for this exactly one selected row in a separate task. That task must use this record and source evidence, preserve the selected locator/context/unit, and remain separate from any later benchmark run.

---

**Exactly one row was selected under the frozen Case-008 protocol. No Ground Truth or amount values were recorded, and no benchmark engine or OCR system was run.**
