# Case-010 MHLW Row Selection Record

## 1. Purpose

Apply the frozen Case-010 Selection Protocol exactly once, in document order, to select the first physical main-standard-ledger row that passes C1--C4. This record is not Ground Truth and does not transcribe amount values.

## 2. Frozen protocol and source-survey references

- Selection Protocol: `fixtures/document-understanding/case-010/20260929_0647_Case010_Selection_Protocol.md`, frozen at `2f910f218a35a776d57d32c30f10322b0b945209`.
- Source Survey: `reports/document-understanding/20260929_0625_Case010_MHLW_Source_Survey.md`, frozen at `cc5115b80076159dc58570fb9fa4e7d7267a14f5`.
- Survey evidence: `evidence/document-understanding/case-010-source-survey.json`, frozen with the Source Survey.

Neither frozen artifact was changed by this task.

## 3. Canonical source identity and integrity

- Source ID: `mhlw-fy2024-general-account-expenditure-request-summary-detail`
- Official URL: `https://www.mhlw.go.jp/wp/yosan/yosan/24syokan/dl/05-1b-01.pdf`
- Local locked source: `sources/raw/mhlw-fy2024-general-account-expenditure-request-summary-detail.pdf`
- SHA-256 re-verification: `09d26048b20d1b1dac7aab236ab6da452e482a12f4d97a8f6c28ec7c420eb192` — PASS
- Package model: one 1,723-page PDF

The source lock and registry were not changed.

## 4. Frozen selection universe

The frozen universe is the main standard-ledger grammar for organization `010 厚生労働本省`, `pdfPageIndex 20–1226`, inclusive. Cover/TOC, separators, cross-reference summary, aggregate-only rows, embedded remarks-side structures, other non-main grammars, and ambiguous grammar are excluded.

## 5. Inspection method and order

Selection used a fresh direct visual render of physical PDF page 21 (`pdfPageIndex 20`) at 400 dpi. Inspection began at the top of the frozen universe and proceeded top-to-bottom. No OCR, text-extraction search, benchmark engine, arithmetic reconstruction, or automated amount recognition was used.

The first full pass occurred on this first inspected page; therefore, no later physical row and no later page was inspected.

## 6. Rows actually evaluated before the stop condition

| Order | Locator | Source-visible row type | C1 | Result and reason |
| --- | --- | --- | --- | --- |
| 1 | `pdfPageIndex 20`, top main grid | Organization aggregate: `010 厚生労働本省` | FAIL | No row-local request number and expense code pair. C2–C4 were not evaluated. |
| 2 | `pdfPageIndex 20`, below organization aggregate | Item aggregate: `001 厚生労働本省共通費` | FAIL | No row-local request number and expense code pair. C2–C4 were not evaluated. |
| 3 | `pdfPageIndex 20`, immediately below item aggregate | Physical main-ledger request/expense row | PASS | C1–C4 all PASS; selected and inspection stopped. |

Rows evaluated: 3.

## 7. Selected row locator and identity

- `pdfPageIndex`: 20
- Printed page: `厚（本） 13`
- Grammar: main standard ledger
- Organization: `010 厚生労働本省`
- Item context: `001 厚生労働本省共通費`
- Request number: `①`
- Expense code: `05-95`
- Expense label, raw visual lines:
  1. `厚生労働本省一般行政に`
  2. `必要な経費`

## 8. Frozen criteria application

- **C1 — PASS.** The selected physical main row visibly carries its own request number `①` and expense code `05-95`.
- **C2 — PASS.** The selected row’s expense label visibly wraps across the two raw lines recorded above.
- **C3 — PASS.** Three standard amount cells are visibly aligned with and associated with this same physical main-ledger row. Their digits and sign were not transcribed or otherwise recorded.
- **C4 — PASS.** The row has source-visible row identity, same-page main-ledger item context, the frozen organization anchor, main-detail section/file provenance, and the applicable unit evidence. No cross-page lookup was used.

## 9. Context, unit, and grammar determination

Context followed the frozen order: row-local identifier and label, then the same-page main-ledger item context, then the frozen organization anchor, then the main-detail section/file identity. Context was not inherited from another page or from an embedded remarks-side structure.

The applicable unit is the main-detail section’s `千円`, declared on this section-opening page. It is section-scoped for confirmed main-ledger rows. No local unit from the remarks-side embedded material was used.

The selected row is in the continuous main grid, aligned to the main request-number, expense-code, and three amount columns. It is not contained in the remarks-side nested material; the latter remains excluded from the universe.

## 10. Tie-break and stop condition

The selected row is the earliest fully eligible row under the frozen document-order rule: earliest `pdfPageIndex`, then topmost eligible physical row. It followed two C1-failing aggregate rows on the first page of the frozen universe. Selection stopped immediately after its C1–C4 full pass. No later row or page was compared or inspected.

## 11. Prior and incidental exposure

The Source Survey had already visually sampled representative MHLW content; this selection is not claimed to be blind or sandboxed. The fresh visual inspection necessarily exposed amount glyphs while confirming C3, but no amount value or delta sign was transcribed, recorded, normalized, or used as a selection input. Prior or incidental exposure did not affect the frozen criteria, document order, or tie-break.

## 12. Explicit non-actions

No Selection Protocol or Source Survey change was made. No Ground Truth, amount transcription, arithmetic validation, benchmark run, separate OCR experiment, parser/normalizer/evaluator change, source-lock/registry change, MOF linkage, or production adaptation was performed.

## 13. Frozen-artifact integrity

Before selection, the Selection Protocol was byte-identical to `2f910f218a35a776d57d32c30f10322b0b945209`; the Source Survey report and evidence were byte-identical to `cc5115b80076159dc58570fb9fa4e7d7267a14f5`. The Case-006–010 Selection Freeze, Cases 001–009 artifacts, scripts, source lock/registry, parser/normalizer/evaluator, OCR configuration, and production code remain outside this task’s changes.

## 14. Next task

Case-010 Ground Truth Freeze: independently re-verify this already-selected locator using fresh direct visual source evidence, transcribe the selected row’s values only then, and stop before benchmark execution.

**Exactly one row was selected under the frozen Case-010 protocol. Inspection stopped at the first C1--C4 full pass. No Ground Truth or amount values were recorded, and no benchmark engine or OCR system was run.**
