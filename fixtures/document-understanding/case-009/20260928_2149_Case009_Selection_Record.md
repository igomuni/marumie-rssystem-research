# Case-009 Cabinet Office (CAO) Selection Record

Result: **exactly one row selected**

Created: 2026-09-28 21:49 Asia/Tokyo
Branch: `research/case-009-cao-source-survey`

## 1. Purpose

This record applies the already-frozen Case-009 Selection Protocol mechanically. It records one selected physical standard-ledger row and stops before Ground Truth. It does not amend the protocol, transcribe numeric amount values, create Ground Truth, run a benchmark, run OCR, or change source registration or production code.

## 2. Frozen protocol and source chain

| artifact | commit |
|---|---|
| Source Survey | `e640dc21c5bf536ab5ca40b20ed4b3ea8b2b3c11` |
| Selection Protocol | `d42b7b89f2671c8e9cad04b75116fbd7b64b7af6` |

The protocol was directly re-read and confirmed byte-identical to its freeze commit before inspection.

## 3. Canonical source identity and integrity

| field | value |
|---|---|
| package | CAO FY2024 official expenditure-request package |
| source ID | `cao-fy2024-general-account-expenditure-request-detail-01` |
| official filename / URL | `1.pdf` / `https://www.cao.go.jp/yosan/soshiki/r06/pdf/1.pdf` |
| SHA-256 | `7b5de5dbd397c7067cab4ea527ef02681e91265914057651ee5b886174de7f4e` |
| verification | local raw SHA-256 recomputed before inspection; matches the source lock |
| representation | native-text, A4 landscape, List Creator, permission-only AES encryption |

## 4. Frozen universe and inspection method

The frozen universe is the standard-ledger portion of locked `1.pdf`, `pdfPageIndex 0–2`, using the file-section-local unit `千円` and no cross-PDF context inheritance.

A fresh 400-dpi `pdftoppm` render of `pdfPageIndex 0` was inspected directly. No OCR, native text extraction, benchmark engine, MOF/RS data, arithmetic reconstruction, or amount-recognition automation was used for candidate eligibility. A full pass occurred on this first page, so `pdfPageIndex 1–2` were not inspected for selection eligibility under the stop rule.

## 5. Rows evaluated in document order

Three physical ledger/hierarchy rows were evaluated on `pdfPageIndex 0` before stopping. Header/title rows and nested remarks boxes were excluded by the frozen grammar rule and not counted as candidate-shaped physical rows.

| order | locator | row type | C1 | C2 | C3 | C4 | outcome / first reason |
|---:|---|---|---|---|---|---|---|
| 1 | page 0, top hierarchy | organization aggregate: `010 内閣本府` | FAIL | not evaluated | not evaluated | not evaluated | no row-local request number and expense code |
| 2 | page 0, below row 1 | item aggregate: `010 内閣本府共通費` | FAIL | not evaluated | not evaluated | not evaluated | no row-local request number and expense code |
| 3 | page 0, immediately below row 2 | request/expense standard-ledger row | PASS | PASS | PASS | PASS | **selected; first complete pass** |

## 6. Selected physical row

| field | source-visible value |
|---|---|
| PDF locator | `pdfPageIndex 0`; printed prefix `内（本）` |
| grammar | standard ledger: request-number, matter, previous/FY2024/delta, and remarks columns |
| file-opening division/organization scope | `19 内閣府所管（官房総務課（総務課））` |
| organization | `010 内閣本府` |
| item context | `010 内閣本府共通費` |
| request number | `①` |
| expense code | `01-95` |
| expense label, raw visual lines | `内閣本府一般行政に必要` / `な経費` |
| expense label, visual-wrap join | `内閣本府一般行政に必要な経費` |

The displayed label wraps visibly across two printed lines. Its row visibly carries its own three standard-ledger amount cells; their numeric values and delta representation are deliberately not transcribed here.

## 7. C1–C4 and context/unit evidence

- **C1 PASS:** `①` and `01-95` are visibly co-located on the selected physical row.
- **C2 PASS:** the selected label has the two visual lines recorded above.
- **C3 PASS:** each of the three standard-ledger amount columns visibly contains a cell associated with the selected row; no amount was inherited, inferred, or calculated.
- **C4 PASS:** row-local identifiers and label; same-page item context; the file-opening division/organization scope; standard-ledger grammar; canonical file identity; and the `（単位:千円）` file-section-opening declaration are source-visible on `pdfPageIndex 0`.

The unit is `千円`, scoped to this confirmed standard-ledger section only. The nested explanatory/breakdown material in the remarks region was excluded and supplied no identity, amount, item, organization, or unit evidence for selection.

## 8. File identity, tie-break, and stopping point

File identity is both mandatory provenance (`1.pdf`, source ID, official URL, SHA-256) and the bounded context-bearing division-scope partition. It is not used to replace visible organization/item context.

The selected row is the earliest fully eligible row at `pdfPageIndex 0` and the topmost complete pass on that page. Inspection stopped immediately after row 3; no later row on page 0 and no row on pages 1–2 was evaluated for eligibility.

## 9. Prior and incidental exposure

The Source Survey had already visually inspected `1.pdf` page 1; the protocol task structurally re-rendered all three pages. This task re-rendered page 0 fresh for direct visual selection. The selection is therefore not claimed to be blind. Prior familiarity was not a criterion or tie-break input.

Amount values were visually exposed while checking C3, but were not transcribed. Delta sign and remarks content were not used as criteria and were not recorded as Ground Truth.

## 10. Explicit non-actions and integrity

- Amount values recorded: **No**.
- Ground Truth created: **No**.
- Benchmark or OCR run: **No**.
- Protocol amendment: **No**.
- Source lock/registry mutation: **No**.
- Parser, normalizer, evaluator, or production adaptation: **No**.

The Source Survey report/evidence remains byte-identical to `e640dc21c5bf536ab5ca40b20ed4b3ea8b2b3c11`; the Selection Protocol remains byte-identical to `d42b7b89f2671c8e9cad04b75116fbd7b64b7af6`. The Case-006–010 Selection Freeze, Cases 001–008, `scripts/`, source lock/registry, parser/normalizer/evaluator, and production code were not changed.

## 11. Next task

**Case-009 Ground Truth Freeze**: independently re-render the already-selected row, directly transcribe its source evidence, and stop before any benchmark/OCR run.

**Exactly one row was selected under the frozen Case-009 protocol. No Ground Truth or amount values were recorded, and no benchmark engine or OCR system was run.**
