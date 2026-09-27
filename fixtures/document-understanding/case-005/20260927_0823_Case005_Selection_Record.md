# case-005 Selection Record — MLIT (国土交通省) FY2024 General-Account Expenditure Request

Status: **row selected and frozen. No Ground Truth. No benchmark engine run against MLIT.**

Date: 2026-09-27 (Asia/Tokyo)

This record applies the already-frozen `fixtures/document-understanding/case-005/20260927_0815_Case005_Selection_Protocol.md` (commit `9b292c0`) exactly, through direct visual inspection only. It does not redesign, reinterpret, or weaken the protocol.

## 1. Purpose

Apply the frozen case-005 selection protocol via deterministic, document-order enumeration within the frozen universe, select exactly one eligible row, and stop before Ground Truth.

## 2. Frozen protocol identity / SHA

- Protocol file: `fixtures/document-understanding/case-005/20260927_0815_Case005_Selection_Protocol.md`
- Freeze commit: `9b292c0`
- Verified byte-identical to the frozen commit before this task's first edit (`git diff 9b292c0 -- <protocol path>` → empty).
- Criteria C1–C4, the frozen selection universe, the tie-break, and the ambiguity/continuation rules were applied exactly as written; none was modified.

## 3. Frozen source identity / SHA

- `sourceId`: `mlit-fy2024-general-account-expenditure-request`
- SHA-256: `4eebb84cec72a4b3b11a2b89c41093550bef5a07095d5c7b178e238406b08217` — re-verified against `sources/source-lock.json` and independently via `shasum -a 256` on the local raw file, both matching, unchanged.

## 4. Prior exposure disclosure

Per the protocol's own §3, the following was already visually exposed during the source survey, before this protocol existed: organization `010 国土交通本省`, item `002 国土交通本省共通費`, request no. `①`, expense code `05-95`, label `国土交通本省一般行政に必要な経費`. This exposure is disclosed again here, honestly, not concealed. **The winner recorded below (§8) is this same row** — this was not decided in advance; it is the deterministic, unavoidable result of applying C1–C4 in document order starting from the frozen universe's own first page, on which this is structurally the very first row that could possibly pass C1 at all (see §6). It was neither sought nor avoided, per the protocol's own explicit permission for this outcome.

## 5. Inspection method

Direct visual inspection only: `pdftoppm -png` rasterization of the locked PDF (poppler, not one of the three compared engines) at 200dpi for the full page and 400dpi for a targeted row-band crop, followed by direct human-style reading of the rendered images. No `pdfjs-baseline`, `pymupdf-baseline`, `docling`, MinerU, PaddleOCR, OCR, `npm run docbench`, or any benchmark-evidence reference was used at any point. No PDF utility's *output values* were used to determine any C1–C4 result — `pdftoppm`/`pdfinfo` were used solely as rendering/navigation tools, per the protocol's own permitted-tool list.

## 6. Enumeration in document order

Starting at `pdfPageIndex` 28 (the frozen universe's own confirmed lower bound, printed page 19), all rows on this single page were evaluated top to bottom, in document order:

| # | `pdfPageIndex` | Row (locator only, no amounts) | C1 | C2 | C3 | C4 | Result |
|---|---|---|---|---|---|---|---|
| 1 | 28 | `010　国土交通本省` (組織-level aggregate; no request no., no expense code) | **FAIL** | not evaluated after C1 failure | not evaluated | not evaluated | Rejected |
| 2 | 28 | `002　国土交通本省共通費` (項-level aggregate; no request no., no expense code) | **FAIL** | not evaluated after C1 failure | not evaluated | not evaluated | Rejected |
| 3 | 28 | request no. `①`, expense code `05-95`, label wrapping across two lines | **PASS** | **PASS** | **PASS** | **PASS** | **SELECTED — first eligible row** |

Enumeration stopped immediately upon finding this eligible row, per the protocol's tie-break and this task's own explicit instruction not to look at any subsequent candidate for comparison. No page beyond `pdfPageIndex` 28 was inspected, and no row after the winner on this same page was inspected either.

## 7. Candidate rejection reasons

- **Candidate 1** (`010　国土交通本省`): fails C1 outright — this is a bare organization-level aggregate row with no request number or expense-level code printed in its own identifier position. Per the protocol's own early-rejection allowance, C2–C4 were not evaluated.
- **Candidate 2** (`002　国土交通本省共通費`): fails C1 for the identical reason — a bare item-level aggregate row with no native identifier. C2–C4 not evaluated.

## 8. Selected row locator

- `pdfPageIndex`: 28
- 1-based PDF page: 29
- Printed page label: `国（本） 19`
- Organization: `010　国土交通本省`
- Item (項): `002　国土交通本省共通費` (the item this row's own code falls under, per the immediately preceding aggregate line on the same page)
- Request number, raw visual representation: `①` (circled numeral one, printed in the leftmost column, aligned with this row's own first line)
- Expense code: `05-95`
- Expense label, literal line wrapping as printed: line 1 `国土交通本省一般行政に` / line 2 `必要な経費` (the code `05-95` shares the first printed line with the start of the label)
- Expense label, human-readable joined form used only as a locator (not benchmark-normalized Ground Truth): `国土交通本省一般行政に必要な経費`

No ambiguity was observed in this locator; the printed text is clear and unbroken across its two visual lines, confirmed at 400dpi.

## 9. C1–C4 evidence for the winner

- **C1 — Native request/expense-level identifier: PASS.** Both a request number (`①`) and an expense-level code (`05-95`) are printed in the row's own identifier columns.
- **C2 — Multi-line wrap: PASS.** The expense label visually occupies two printed lines within its own cell (`国土交通本省一般行政に` / `必要な経費`), confirmed at 400dpi — not inferred from any text-extraction representation.
- **C3 — Standard amount triple: PASS.** All three amount columns (前年度予算額 / 6年度概算要求額 / 対前年度比較増△減) are visually present and directly associated with this row's own first printed line, in the document's native layout. **Only structural presence and association are confirmed here — the values themselves are not recorded as Ground Truth (see §13).**
- **C4 — Self-contained sufficiency: PASS.** The row's identifier, label, and complete amount triple are all visually present within one coherent visual unit on `pdfPageIndex` 28 (the label's own two-line wrap is the ordinary C2 case, not page-spanning); no page-spanning amount triple, no blank inline triple, no value relocated to a separate embedded-matrix-like region, and no dependency on any neighboring unusual representation was observed for this row.

## 10. Tie-break application

Not needed to break a tie among multiple simultaneously-eligible rows — no other row on `pdfPageIndex` 28 satisfied C1–C4 before this one (candidates 1 and 2 both failed C1), so the "first eligible row in document order" rule selected this row directly, with no competing candidate at the same rank. The frozen universe's own upper-boundary uncertainty (~`pdfPageIndex` 509, extrapolated and unverified per the protocol's own §5) was **not** resolved in this task, since the winner was found on the universe's own very first page — far short of that boundary, so pinning it was unnecessary, consistent with the originating task's own §7 instruction.

## 11. Incidental exposure disclosure

While confirming C3 (amount-triple presence and association), the three amount values for the selected row, and for both rejected aggregate rows, were necessarily visible on the rendered page. **These values are disclosed here as having been seen, but are deliberately not transcribed as Ground Truth**, per this task's own explicit instruction: only their structural presence and row-association were used as evidence (§9); no previous-budget, current-request, or delta figure for any row is recorded as a value anywhere in this document. No `△` glyph was observed on the selected row's own delta (observed incidentally, not used as a selection input — see §12). No other unusual structure, embedded matrix, or special representation was encountered on `pdfPageIndex` 28 during this enumeration.

## 12. Non-criteria confirmation

None of the following influenced this selection, though some were incidentally observable while reading the rendered page:

- The selected row's delta was incidentally seen to carry no `△` glyph (positive) — observed, not used as a selection input in either direction.
- Remarks-column content/population on this or the rejected rows was not used as a selection input.
- Amount magnitude and any arithmetic relationship among the three visually-present values were not computed, checked, or used.
- No engine (pdf.js/PyMuPDF/Docling) was run or consulted; no expectation about any engine's behavior on this row influenced the choice.
- The document's Producer metadata ("List Creator") and its unencrypted status played no role.
- This row's structural resemblance to case-002's, case-003's, and case-004's own selected rows (`①/[code]/[ministry]一般行政に必要な経費`) was neither sought nor avoided — it is the deterministic consequence of applying C1–C4 to the universe's own first page, exactly as the protocol anticipated could happen (§1/§3 of the protocol).
- The `繰入` (transfer-into) expressions already known to exist elsewhere in this document's 総表 (source survey §10) played no role — this row is not, and was not evaluated as, a `繰入`-shaped row.
- No correspondence to any MOF-CSV concept was considered.
- The fact that this exact row was already incidentally visible during the source survey did not qualify or disqualify it — it was evaluated identically to the two rejected candidates, using only C1–C4.
- Perceived difficulty, unusualness, or "interestingness" played no role.
- The web/chat-level pre-survey textual rendering of the request number as plain `1` (vs. the confirmed source visual fact `①`) was not used as a locator or selection input — only the directly-rendered source page was used.

## 13. Ground Truth separation confirmation

Explicitly confirmed: this task did **not** create `ground-truth.json`; did **not** transcribe the previous-budget, current-request, or delta amounts as truth values; did **not** perform comma removal, circled-numeral normalization, line-join normalization, or any other Ground-Truth-shaping transformation; did **not** determine or record a signed delta; did **not** perform any arithmetic consistency check; and did **not** confirm or record a unit scope beyond what selection itself required (none was required — unit was not a C1–C4 input). The "human-readable joined form" in §8 is recorded solely as a locator, explicitly labeled as such, not as a normalized Ground Truth value.

## 14. Stop condition confirmation

This task stops here, having selected exactly one row (`pdfPageIndex` 28, request no. `①`, expense code `05-95`, `国土交通本省一般行政に必要な経費`) and frozen it in this record. No `ground-truth.json` was created. No benchmark engine, OCR tool, or `npm run docbench` was run against MLIT. No context diagnostic, anomaly survey, or MOF reverse-linkage investigation was started. The next task must create and freeze Ground Truth for this already-selected row through direct visual source inspection, still without running any benchmark engine.

## 15. Recommended next step

Create and freeze Ground Truth for the already-selected case-005 row through direct visual source inspection, without running any benchmark engine. **Not executed in this task.**
