# Case-007 Selection Record — 内閣官房 (Cabinet Secretariat, CAS), `detail-01`

Status: **NULL RESULT. No row was selected. No Ground Truth was created. No benchmark engine or OCR was run.** This record documents an exhaustive, unmodified application of the frozen Case-007 Selection Protocol to its own frozen universe, which found **zero rows satisfying all criteria (C1–C4) together.** This is preserved as a genuine research outcome, not concealed or worked around, per this program's own established precedent of preserving null/failure results as-is (see the Case-006 first-frozen-benchmark run).

Date: 2026-09-28 (Asia/Tokyo)

## 1. Purpose

Apply the frozen Case-007 Selection Protocol (`2cc0821`) without modification to its own frozen universe (`cas-fy2024-general-account-expenditure-request-detail-01`) to select exactly one row. This record documents that enumeration and its outcome.

## 2. Frozen protocol reference / SHA

- Protocol: `fixtures/document-understanding/case-007/20260928_1207_Case007_Selection_Protocol.md`, commit `2cc0821`.
- Re-verified byte-identical to `2cc0821` immediately before this task's first edit.
- No criterion, universe, tie-break, or context-resolution rule was modified in this task.

## 3. Source/package/file identity

- Package: CAS FY2024 general-account expenditure request.
- Frozen target file (`sourceId`): `cas-fy2024-general-account-expenditure-request-detail-01`.
- Official URL: `https://www.cas.go.jp/jp/yosan/pdf/r6_02.pdf` (re-confirmed in this task from `sources/source-lock.json` — the file's own URL filename is `r6_02.pdf`, since `r6_01.pdf` is the already-excluded `cover` file; this confirms `detail-01` genuinely is the first detail-ledger file in official numbering order, consistent with §4 of the protocol).
- Page count: 2 (re-confirmed via `pdfinfo` in this task).
- Bureau label (page-1 header): `05 内閣所管(総務官室（総務課）)`.

## 4. Source SHA verification

- `sources/source-lock.json` entry SHA-256: `37c5d82cb7fc835ab16d7f85c113f646d712c34315cf45fce556846f0419d5c0`.
- Local raw file SHA-256 (`shasum -a 256`): `37c5d82cb7fc835ab16d7f85c113f646d712c34315cf45fce556846f0419d5c0`. **Match confirmed.** No drift, no re-acquisition.

## 5. Frozen universe

The entire 2-page file (`pdfPageIndex` 0–1), per protocol §5. No sub-range within the file; no other CAS file consulted or scanned.

## 6. Context anchor verification

Organization anchor `010 内閣官房` confirmed present at the top of the file's own page 1 (rendered at 200dpi, viewed directly), immediately above the standard column-header row (`要求番号 / 事項 / 前年度予算額 / 6年度概算要求額 / 対前年度比較増△減 / 備考`). Per the protocol's own file-scoped organization rule (§8.2/§9), this anchor is resolved once for the entire file and is not required to be re-printed on any individual row's own page.

## 7. Enumeration procedure

Rendered both pages of `detail-01` at 200dpi via `pdftoppm` (non-OCR, visual/image inspection only). Scanned top-to-bottom on page 1 first; page 2 only consulted because page 1 yielded no fully eligible row (per the protocol's own stop-rule discipline). No page outside this 2-page universe was rendered or consulted.

## 8. Rows evaluated in order

| # | Page | Row (as printed) | C1 | C2 | C3 | C4 | Outcome |
|---|---|---|---|---|---|---|---|
| 1 | 1 | `010 内閣官房` (organization aggregate) | FAIL | — | — | — | Rejected at C1 |
| 2 | 1 | `010 内閣官房共通費` (item aggregate) | FAIL | — | — | — | Rejected at C1 |
| 3 | 1 | `① / 01-95 内閣官房一般行政に必要な経費` | PASS | PASS | **FAIL** | not reached | Rejected at C3 |
| 4 | 1 | `011 経常事務費` (project-level breakdown, no request no.) | FAIL | — | — | — | Rejected at C1 |
| 5 | 1 | `006 内閣総務官室一般事務費` (further breakdown, no request no.) | FAIL | — | — | — | Rejected at C1 |
| 6 | 1 | `95016-2111-05-0710 非常勤職員手当` (object-code line, no request no.) | FAIL | — | — | — | Rejected at C1 |
| 7 | 1 | `95016-2129-06-0110 諸謝金` (object-code line, no request no.) | FAIL | — | — | — | Rejected at C1 |
| 8 | 1 | `95016-2122-08-2010 職員旅費` (object-code line, no request no.) | FAIL | — | — | — | Rejected at C1 |
| 9 | 1 | `95016-2122-08-3010 赴任旅費` (object-code line, no request no.) | FAIL | — | — | — | Rejected at C1 |
| 10 | 1 | `95016-2123-09-1010 庁費` (object-code line, no request no.) | FAIL | — | — | — | Rejected at C1 |
| 11 | 1 | `2 / 06-95 情報の収集及び分析その他の調査に必要な経費` | PASS | PASS | **FAIL** | not reached | Rejected at C3 |
| 12 | 1 | `011 内閣総務官室システム関係経費` (project-level breakdown, no request no.) | FAIL | — | — | — | Rejected at C1 |
| 13 | 2 | `95016-2111-05-0710 非常勤職員手当` (continuation, no request no.) | FAIL | — | — | — | Rejected at C1 |
| 14 | 2 | `95016-2123-09-1040 情報処理業務庁費` (continuation, no request no.) | FAIL | — | — | — | Rejected at C1 |

**Every row in the frozen 2-page universe was evaluated.** No row satisfies C1–C4 jointly.

## 9. Rejected candidates + exact criterion/reason

- **Organization/item aggregate rows** (`#1`, `#2`): rejected at C1, per the protocol's own explicit exclusion of "a bare organizational- or item-level aggregate/header row with no such identifier" — no request number, no expense-level code.
- **The two request/expense-code-bearing rows** (`#3`: `①/01-95`; `#11`: `2/06-95`): both PASS C1 (native request number + expense-level `NN-NN` code) and C2 (confirmed 2-line visual wrap on both). Both **FAIL C3**: their own printed line(s) show **visually blank cells in all three amount columns** (previous-year budget / FY2024 request / delta) — the amount figures corresponding to each item instead appear one or more structural levels deeper (project-level and/or object-code-level rows below), not on the identifier-bearing row itself. This was confirmed by direct, tightly-cropped visual inspection at 2x zoom of both candidates (§16), not inferred. Per C3's own text ("associated with this specific row... FAIL: one or more is visually absent or unassociated with this specific row"), this is an unambiguous FAIL, not an insufficient-evidence case.
- **Project-level breakdown rows** (`#4`, `#5`, `#12`, e.g. `011 経常事務費`, `006 内閣総務官室一般事務費`, `011 内閣総務官室システム関係経費`): rejected at C1. These rows carry a native numeric code (e.g. `011`, `006`) but **no entry in the 要求番号 (request-number) column**, and their code format (bare 3-digit) differs from the `NN-NN` expense-level format the protocol's own C1 text and every prior case's own selected-row convention (case-002 through case-006) associates with the "request/expense-level identifier." They are interpreted as sub-breakdown rows belonging to whichever request-numbered row governs them, not as independent eligible row candidates in the same schema sense (`requestNo` + `expenseCode` together identifying one row, matching every prior case's `ground-truth.json` schema).
- **Object-code lines** (`#6`–`#10`, `#13`, `#14`, e.g. `95016-2111-05-0710 非常勤職員手当`): rejected at C1 for the same reason — no request-number entry, and a deeper `NNNNN-NNNN-NN-NNNN` object-code format, one or more levels below the expense-level code.

## 10. Selected row locator

**None.** No row satisfies C1–C4 jointly within the frozen universe. No locator is recorded.

## 11. C1...Cn result

See §8 table. Two candidates reached C3 (both PASS C1, PASS C2); both FAILED C3; C4 was never reached for any row, since no row passed C1–C3 together.

## 12. Context resolution evidence

Not applicable to a null outcome at the row level, but the context-resolution mechanics themselves were exercised and confirmed working as designed during enumeration:

- **File-scoped organization anchor** (`010 内閣官房`): confirmed present once, at page 1's own top, per §6 — consistent with the protocol's own C4 redefinition (this anchor is never required to reprint on any candidate row's own page).
- **Item context persistence across a page boundary**: directly observed in this file (not merely cited from the protocol's own prior observation) — item `2 / 06-95`'s own project-level breakdown (`011 内閣総務官室システム関係経費`) begins on page 1 and its own object-code sub-rows (`95016-2111-05-0710`, `95016-2123-09-1040`) continue onto page 2 without any item-header re-declaration, confirming the "nearest preceding item header, same file" resolution rule (protocol §9) is both necessary and sufficient here.

## 13. Tie-break application

Not reached — no tie exists among zero eligible rows.

## 14. Cross-file splitting handling

Not exercised in this task. Per the frozen protocol (§7), the single-file universe (`detail-01` only) was designed specifically so this question never needs adjudication during row enumeration — and since no row was even found eligible within `detail-01` itself, no cross-file question arose at all. No other CAS file was consulted, compared, or referenced at any point in this task.

## 15. Prior exposure

`detail-01`'s own page-1 and page-2 content — including the same amount values now confirmed structurally unassociated with either C1-passing candidate (`132,904`/`153,320` at the item level; `107,902`/`128,304` at the `006` level; `25,002`/`25,016` at the `011` level under item 2; `3,754`/`3,754` and `21,248`/`21,262` on page 2) — was already read during the Case-007 source survey and again during the Selection Protocol Freeze task, both times for precondition-confirmation purposes, not row selection. This task's own enumeration (§7–§9) is a fresh, exhaustive, criterion-by-criterion pass over every row in the universe, not a re-application of prior conclusions. **No "blind selection" is claimed.** The outcome (zero eligible rows) was not anticipated, predicted, or hinted at in either the source survey or the protocol — both prior tasks' own inspection focused on the item/organization-level anchors and the cross-file item-splitting pattern, not on whether the request/expense-code row itself carried its own amount triple. This specific structural mismatch was discovered fresh, during this task's own criterion-by-criterion enumeration.

## 16. Incidental amount exposure

C3 evaluation for both candidate rows (`#3`, `#11`) necessarily required visually inspecting the amount-column cells directly beside and below each candidate, at 2x zoom, to determine presence/absence and association. **No amount value is transcribed as a Ground Truth candidate anywhere in this record.** Specific figures are named in §9/§12 above only to explain *which row* each amount is structurally associated with (a source-safe structural fact, not a value transcription) — consistent with the protocol's own instruction that incidental exposure during C3 confirmation is permitted and must be disclosed, not concealed.

## 17. Inspection tools

- `pdftoppm -png -r 200` (visual rendering, non-OCR).
- Direct visual reading of the rendered PNG images, including Python/Pillow-based cropping and 2x resizing for close-up confirmation of ambiguous cell boundaries (no OCR, no text extraction of any kind used to read or confirm any value).
- `pdfinfo` (page count).
- `shasum -a 256` / Python `hashlib` (source integrity only).
- **No `pdftotext` or any other text-extraction tool was used to read or confirm any candidate row's content in this task** — all row content was read directly from the rendered images, per the tool restrictions in the originating instructions.
- No compared benchmark engine (`pdfjs-baseline`/`pymupdf-baseline`/`docling`), no `docbench`, no MOF/RS data was consulted.

## 18. Ambiguities / unexpected observations

**Major unexpected finding**: CAS's own `detail-01` ledger uses a **deeper hierarchy than every prior case (002–006)** — organization (組織) → item (項) → **request/expense-code row (要求番号+経費, e.g. `①/01-95`) → project-level breakdown (目, e.g. `011`) → further breakdown (細, e.g. `006`) → object-code line (`95016-xxxx-xx-xxxx`)** — where the amount triple is associated with the **project-level or deeper** rows, not with the request/expense-code row itself. In every prior case (002–006), the request/expense-code row was itself the amount-bearing row, with no intervening project-level layer of this kind observed between it and the amount. This is a genuinely new structural pattern for this research program, discovered through exhaustive, literal application of the frozen protocol's own criteria — not an ambiguity requiring guesswork, since the visual evidence for blank-vs-populated amount cells was unambiguous at 2x zoom. This finding was reported to, and confirmed for continued documentation (rather than protocol amendment or a rescue reinterpretation) by, the requesting user during this task.

No other ambiguity was encountered: every row's C1/C2/C3 status was visually clear.

## 19. Stop confirmation

Enumeration was exhaustive across the entire 2-page frozen universe (§8 lists all 14 rows). No row outside `detail-01` was scanned, rendered, or consulted. No criterion was modified, relaxed, or reinterpreted mid-enumeration to produce a selection. This record was written, and the task stopped, upon confirming the null outcome with the requesting user.

## 20. Ground Truth handoff

**No Ground Truth can be created from this outcome as-is.** The immediate blocker for any future task is that the frozen Selection Protocol's own C3 criterion, as written, has no satisfiable candidate in `detail-01`'s own confirmed hierarchy. Recommended next step (not performed in this task, requires a separate, explicitly-scoped decision): a **Case-007 Selection Protocol Amendment** task must decide, before any further enumeration, one of:

1. Redefine C3/C1 to recognize the project-level or deeper breakdown row (e.g. `006 内閣総務官室一般事務費`, or the object-code line) — rather than the request/expense-code row — as the eligible unit for CAS's own multi-level hierarchy, with its own explicit provenance chain back to the governing request number and expense code (via the context-resolution order already frozen in §9 of the protocol).
2. Re-open the file-universe choice (§4–§5 of the protocol) to test whether other CAS detail files share this same amount-placement convention, or whether some files place the amount triple directly on the request/expense-code row (matching case-002–006's convention) — which would itself be a new, disclosable finding about within-package convention variability.
3. Accept this null result as Case-007's own first-frozen outcome for the `detail-01` universe specifically (analogous to Case-006's own null benchmark preservation), and select a different universe for the row that actually becomes Case-007's target.

None of these three options was decided or acted upon in this task.

---

**Exactly zero rows in the frozen Case-007 universe (`detail-01`) satisfy the frozen protocol's own C1–C4 jointly. No row was selected. No Ground Truth or amount values were recorded. No cross-file adjudication was performed. No benchmark engine or OCR system was run.**
