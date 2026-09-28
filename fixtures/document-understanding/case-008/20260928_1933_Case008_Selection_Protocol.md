# Case-008 Selection Protocol — Courts

Status: **FROZEN before candidate-row enumeration.**

Date: 2026-09-28 19:33 (Asia/Tokyo)

Branch: `research/case-008-courts-baseline`
Pre-task HEAD: `e10d56c529ce9c8197f71dd71df32297ea3675fb`

## 1. Purpose

Freeze the selection universe, grammar exclusions, eligibility rules, context resolution, unit evidence, tie-break, ambiguity handling, and prior-exposure disclosure for Case-008. This protocol does not enumerate or choose a row, create Ground Truth, or run a benchmark/OCR experiment.

## 2. Frozen source identity

| Field | Frozen value |
|---|---|
| Source ID | `courts-fy2024-general-account-expenditure-request` |
| Authority / FY / stage | 裁判所 / FY2024 (令和6年度) / general-account request |
| PDF URL | `https://www.courts.go.jp/vc-files/courts/2023/R06saisyutsu_gaisanyoukyusyo_720kb.pdf` |
| SHA-256 | `df43f2dc183da84fa9952ae4c5e17888177df186ad4c556ed1a519ba584e3c06` |
| Size / pages | 736,439 bytes / 127 physical PDF pages |
| Representation | A4 landscape, text layer, unencrypted, Producer `JUST PDF 3` |

The local raw binary matched the lock in the preceding source survey. No acquisition or lock change is authorized by this protocol.

## 3. Source-survey dependency

This protocol depends on `reports/document-understanding/20260928_1911_Case008_Courts_Source_Survey.md`, frozen in commit `e10d56c`. That survey established that one physical file contains multiple document grammars and concluded **SUITABLE WITH CAVEATS**. The source survey is an immutable input to this task and is not modified.

## 4. Selection unit

The selection unit is **one physical row in the standard `歳出概算要求額明細表` ledger body**. Its provenance is not file identity alone; it is the tuple:

`locked source file + standard-ledger section/grammar + pdfPageIndex + printed page label + organization/item context + row-local native identifier`.

No semantic-parent/child amount model is authorized. A row with blank own amount cells cannot inherit or reconstruct amounts from a subordinate row.

## 5. Frozen standard-ledger universe

The universe is the locked source's standard-ledger section only:

| Constraint | Frozen value / source-side locator |
|---|---|
| `pdfPageIndex` | 6--110 inclusive |
| Printed labels | `裁（裁）3` through `裁（裁）107` |
| Opening locator | title `令和6年度歳出概算要求額明細表`, `03 裁判所所管`, organization `010 裁判所`, standard header |
| Required page grammar | `要求番号 / 事項 / 前年度予算額 / 6年度概算要求額 / 対前年度比較増△減 / 備考` |
| Section unit | 千円, declared at the opening page |

This range is a provenance locator, not the sole proof of grammar. A future selection record must confirm both the range and the standard-ledger source cues in §12 before treating a row as in-universe.

## 6. Explicit grammar exclusions

The following are never eligible, even where a visual token resembles an identifier or amount triple:

| Excluded area | Locator | Why it is a different grammar |
|---|---|---|
| Cover / TOC | indices 0--3 | document navigation, not ledger-row semantics |
| Leading `歳出概算要求額総表` | index 4 | split general/other/total columns and `明細書頁数` cross-reference grammar |
| Blank separators | indices 1, 3, 5, 111, 113 | source blank pages, not missing ledger data |
| Staffing (`定員表`) | indices 112, 114 | 人 unit; staffing/change/transfer/personnel-detail columns, not request/expense ledger semantics |
| `重要政策推進枠要望額総表` | index 115 | policy-framework hierarchy and its own cross-reference-summary grammar |
| `重要政策推進枠要望額明細表` | indices 116--126 | policy-framework hierarchy and fresh local page series, not the standard request-number ledger |
| Nested non-target calculation boxes in a ledger page | wherever present | a local title/header or a local unit such as 百万円 denotes a subordinate grammar, not a standard-ledger row |

The exclusions are semantic/source-structure rules; page ranges only locate them. A row is not admitted merely because it is in the same PDF as the ledger.

## 7. Organization universe

The standard ledger's source-defined top organization is `010 裁判所`, declared at the section opening. The universe is not narrowed below it: the survey's TOC and opening locator establish one top-level Courts organization for the entire frozen ledger range, with internal `項`/request hierarchy rather than later independent organization sections.

This decision is source-safe and deterministic. It does not use amount, candidate shape, engine behavior, or perceived interest. If a future scan finds an apparently new top-level organization declaration within indices 6--110, it is an ambiguity under §14, not authority to widen or redefine this protocol.

## 8. Eligibility criteria

A row is eligible only if it satisfies **all** C1--C4, after P1--P2 are satisfied by source evidence.

### P1 — Correct section and grammar

The row lies in the frozen range and is part of the standard-ledger body under the title/header/unit cues in §§5 and 12, not an excluded grammar in §6.

### P2 — Correct organization universe

The governing source hierarchy resolves to `010 裁判所` within the standard-ledger section. P2 is a universe precondition, not an inherited file-level assertion.

### C1 — Native identifier on the physical row

The physical row itself visibly prints both a native request number and an expense-level `NN-NN` code in its own identifier fields.

- PASS: both identifiers are printed on the same physical row as its label.
- FAIL: organization/item aggregates, headers, object-code/subordinate rows without the request-number-plus-expense-code pair, or a row relying on an identifier only inherited from another row.
- A wrapped label remains one physical row; its identifier need not repeat on its continuation line.

### C2 — Multi-line expense-label wrap

The row's expense label visibly occupies two or more printed lines in its own cell.

- PASS: visual line count is at least two within one physical row block.
- FAIL: label is one printed line, or the apparent continuation is a different row.

### C3 — Standard amount triple on the same physical row

The row itself visibly carries the standard previous-budget / FY2024-request / delta triple in the three ledger amount columns.

- PASS: all three cells are present and associated with that same physical row.
- FAIL: any cell is blank, absent, ambiguous, located in a different row/box/page, or would require arithmetic reconstruction or semantic inheritance.

### C4 — Evidence sufficiency

The row has a source-safe, self-contained provenance chain: row-local C1/C3 evidence; resolvable item and organization context within the standard-ledger section; standard-ledger section identity; and section-appropriate unit evidence.

- PASS: all required evidence resolves using §10--§12 without crossing a grammar boundary.
- FAIL: amount data are page-split or relocated; required context is ambiguous; the row is part of a nested non-target box; or any field is only inferable from an excluded grammar.
- A label wrapping inside the same visual row block is permitted under C2 and is not, by itself, a page-spanning failure.

## 9. Criteria rationale and critique

| Criterion | Case-008 decision | Rationale |
|---|---|---|
| Native identifier | Retain as C1, row-local | Preserves prior-case comparability and excludes aggregate/subordinate rows without importing a CAS-style semantic-parent model. |
| Multi-line wrap | Retain as C2 | Retains the cross-case layout-reconstruction challenge. The source survey's visual opening-ledger inspection established that the `事項` layout can wrap; this was a structural observation, not candidate selection. |
| Standard triple | Retain as C3, row-local | Preserves the three-field benchmark target and directly guards against Case-007's blank-parent/descendant-amount failure mode. |
| Self-contained evidence | Retain as C4, expanded | Case-008 requires explicit section/grammar and local-unit checks because one file contains multiple grammars. This makes the source boundary visible rather than flattening it for comparability. |

The Case-008 primary axis is embedded multi-grammar structure. These criteria test a standard-ledger row without using that axis to seek a novelty-maximizing row.

## 10. Context-resolution order

Resolve context only in this order:

1. row-local request number, expense code, label, and amount cells;
2. same-page governing item hierarchy in the standard-ledger body;
3. nearest preceding valid governing item header **within indices 6--110 and the same standard-ledger section**, stopping at a new item or any section/grammar boundary;
4. section-scoped organization `010 裁判所`, as printed at the ledger opening and by any later direct source declaration;
5. standard-ledger section identity;
6. locked file identity and SHA-256.

No context may cross into the leading summary, a blank page, staffing, policy-framework material, or a nested non-target box. If two governing contexts remain plausible, C4 fails as insufficient evidence; do not choose by amount, arithmetic, or engine output.

## 11. Unit evidence

The target unit is **千円**, established by `（単位：千円）` at standard-ledger index 6. Its scope is the standard-ledger section, not the physical file. The record must cite that section-opening locator and must not substitute staffing's 人 unit, policy-section unit, or a local nested-box unit (including 百万円).

If a candidate's own page does not repeat the unit, the section-opening declaration is the permitted evidence source only while P1/§12 still establish uninterrupted standard-ledger membership. A local non-千円 declaration is evidence of a boundary/non-target box and causes P1/C4 failure unless direct visual inspection resolves it as unrelated to the physical row.

## 12. Section-identity rule

A candidate is standard-ledger material only when all applicable source cues agree:

- index is 6--110;
- the governing section begins with the standard ledger title and `010 裁判所` anchor;
- its repeated column grammar is request number / 事項 / previous / FY2024 / delta / remarks;
- its governing unit is 千円; and
- the row follows the ledger's organization/item/request/expense hierarchy, not a staffing, policy-framework, summary, or local calculation-box schema.

Page index alone is insufficient. If cues conflict, use a higher-resolution source render; unresolved conflict means the row is outside the eligible universe.

## 13. Deterministic tie-break

Among rows that fully pass P1, P2, and C1--C4:

1. lowest `pdfPageIndex` (zero-based) within the frozen standard-ledger universe;
2. then topmost eligible physical row on that page, in visual reading order.

Printed page labels are recorded for human cross-reference but do not override `pdfPageIndex`. No later-row comparison, ranking, or search for a more interesting candidate is permitted after the first full pass.

## 14. Ambiguity and continuation rules

- **Ambiguous grammar/section:** re-render source page(s) at higher resolution and compare title/header/unit/row semantics; unresolved means outside the universe.
- **Ambiguous organization or item context:** apply §10 only; unresolved means C4 fails (`insufficient evidence`).
- **Row continuation:** a label continuing immediately within the same visual row block is C2-compatible. A row with identifier, triple, or required evidence split to another page/row fails C4.
- **Multiple identifiers visually spanning rows:** require the C1 pair on the physical row. If association is not visually unique, fail C1/C4.
- **Blank or ambiguously associated amount cells:** fail C3/C4. No child-row inheritance, arithmetic reconstruction, or semantic-parent model.
- **Ambiguous unit:** use only standard-ledger section evidence. If a local unit could govern the physical row and cannot be resolved visually, fail P1/C4.
- **Insufficient legibility:** non-OCR higher-resolution rendering is permitted. If still insufficient, record the locator and reason as `insufficient evidence`, continue, and do not infer a pass.

## 15. Explicit non-criteria

The following must not influence universe definition, eligibility, context resolution, or tie-break:

- amount magnitude, similarity, or arithmetic relationship;
- delta sign or the `△` glyph;
- remarks content;
- expected benchmark score or engine behavior (pdf.js, PyMuPDF, Docling, or any other engine);
- MOF/RS correspondence;
- visual familiarity, prior exposure, or inspection depth;
- whether a row feels “interesting” or emphasizes embedded-substructure novelty;
- desired benchmark success/failure;
- downstream implementation convenience;
- PDF producer, encryption, fonts, images, or other document-wide representation metadata;
- similarity/difference to a selected row from Cases 002--006.

## 16. Prior exposure

Prior repository artifacts exposed the staffing region (physical PDF page 113 / index 112) and the policy-framework region (physical pages 116--117 / indices 115--116); both are outside this frozen universe. The source survey also directly inspected the standard-ledger opening page (index 6) for structural classification, so no claim of blind selection is made. That inspection exposed standard-ledger hierarchy and layout, and may have incidentally made row-shaped material visible, but did not apply eligibility criteria, enumerate rows, transcribe candidate amounts, or determine a winner.

Prior exposure is a disclosure only and is an explicit non-criterion (§15).

## 17. Permitted inspection method for the next task

The future selection task may use direct visual inspection of non-OCR `pdftoppm` renderings, `pdfinfo`, and narrow page/header/unit/boundary checks. It may render at higher resolution when required by §14. It must not run text-extraction/document-understanding engines, OCR, LLM/vision extraction, `npm run docbench`, or any benchmark before selection is frozen.

Candidate enumeration begins only in that next task, from index 6 in top-to-bottom order. Amounts may be visually checked for C3 presence but must not be transcribed as Ground Truth there.

## 18. Stop rule

The next task must stop immediately at the first row that fully passes P1, P2, and C1--C4 under §13; write a Selection Record and stop before Ground Truth. If no eligible row exists in the frozen universe, record a NULL result and stop. It must not widen the universe, change exclusions/criteria, or inspect excluded grammars to rescue a selection.

## 19. Frozen facts and unresolved questions

**Frozen:** source identity; single-file/multi-grammar model; standard-ledger range; exclusions; top organization; C1--C4; section-aware context and unit scope; tie-break; ambiguity treatment.

**Unresolved and intentionally deferred:** which physical row, if any, passes all criteria; exact item-context lookback required for any future candidate; full population of embedded local boxes; whether a NULL result will occur. These are not inputs to this freeze.

## 20. Next-task handoff

Apply this protocol to select exactly one row if one exists, write `Case008_Selection_Record`, and stop before Ground Truth. Required record locators include source ID/SHA, `pdfPageIndex`, printed label, section/grammar, organization, resolved item context, native request number, expense code, and the criterion-by-criterion decision.

---

**The Case-008 selection universe, grammar exclusions, eligibility criteria, context rules, unit scope, and tie-break were frozen before candidate-row enumeration. No row was selected, no Ground Truth was created, and no benchmark or OCR experiment was run.**
