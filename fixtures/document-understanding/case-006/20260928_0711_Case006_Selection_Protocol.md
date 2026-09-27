# Case-006 Selection Protocol (Preregistration) — 法務省 (Ministry of Justice) FY2024 General-Account Expenditure Request

Status: **frozen protocol. Row NOT yet selected. No candidate row enumerated or inspected in this task. No Ground Truth. No benchmark engine or OCR run against MOJ.**

Date: 2026-09-28 (Asia/Tokyo)

This document defines, in advance of examining any specific candidate row, how the Case-006 target row will eventually be selected from the already-locked MOJ source. It is committed before any row is identified so the choice cannot be influenced — consciously or not — by knowledge of how any engine performs (none has run, and none can meaningfully run against this raster-only source), by the expected null benchmark result, by vector-path complexity, or by resemblance to case-001–005's own selected rows. Actual row selection is a **separate, later task** that applies this protocol; this task does not perform it.

## 1. Purpose

> Which row should become the single Case-006 target, chosen from a source-defined MOJ universe using only source-visible structure — never OCR output, benchmark behavior, the expected null-extraction result, or vector-path/object characteristics — so that the eventual Ground Truth exercises the same document-understanding capabilities already tested in case-001–005, on a source whose *representation* (not layout) is the axis under study?

This protocol freezes, in order: frozen source identity → Case-006's own representation context → critique/comparison against prior protocols → selection universe → universe evidence → source/multi-grammar preconditions → eligibility criteria → criterion-by-criterion rationale → explicit non-criteria → deterministic tie-break → ambiguity/continuation handling → navigation method for a textless source → prior-exposure disclosure → contamination controls → what was/was not inspected → freeze statement → next task.

## 2. Frozen source identity

- `sourceId`: `moj-fy2024-general-account-expenditure-request`
- Title (from the document's own cover page): `令和6年度歳出概算要求書`, `21 法務省所管`
- Official PDF: `https://www.moj.go.jp/content/001402818.pdf`
- SHA-256 (re-verified against `sources/source-lock.json` and independently against the local raw file via `shasum -a 256`, both matching, unchanged since the Case-006 source survey): `bd5ce9c5dee48b03407e9a8d4050f3992c8a515f510c0339364316448dd9cf8c`
- Size: 147,742,864 bytes; 737 pages; A4 (page objects portrait-dimensioned, rotated 90° for landscape display); PDF 1.5; Producer "JUST PDF 5"; **not encrypted**.
- This protocol does not re-lock, re-acquire, or otherwise modify the source. Verified via `git fetch`/`git status` immediately before this task's first edit: branch `research/case-006-moj-source-survey` at `b4a9cd2`, working tree clean; `sources/source-lock.json` and `sources/raw/` unchanged.
- Established source-of-truth for all structural facts below: `reports/document-understanding/20260928_0703_Case006_MOJ_Source_Survey.md` and `evidence/document-understanding/case-006-source-representation.json` (the source survey and its companion diagnostic). **No new PDF inspection beyond re-confirming the exact detail-table opening page (§5) was performed in this task.**

## 3. Case-006's own representation context (not a selection input)

Per the Case-006–010 Selection Freeze (`654e3c5`), Case-006's own primary research axis is **source representation** (vector-outlined content with zero extractable text, zero font/image resources — refined from a simple "rasterized" label in the source survey's own §7) — the layout/ledger grammar itself is already known to be identical to case-002–005's own standard grammar. This protocol treats that representation fact as **context for why this case exists**, never as an eligibility criterion, a tie-break input, or a justification for widening or narrowing the universe. A row is not more or less eligible because of how "hard" the representation makes it for any engine; eligibility is judged purely on the same source-visible structural properties every prior case's protocol has used.

## 4. Critique of prior protocols (case-002 E1–E5 / case-003 ME1–ME5 / case-004 MX1–MX4 / case-005 C1–C4)

| Concept | Classification pattern across case-002–005 | Re-evaluation for MOJ |
|---|---|---|
| "Correct table" (明細表, not 総表/定員表) | Row-level criterion in case-002/003 (single combined file, 明細表 embedded mid-document); reclassified to a source/universe precondition in case-004 (standalone 明細表-only file) and case-005 (combined file, but with an exact TOC-confirmed 明細表 boundary). | MOJ's locked source is a **single combined file containing three distinct sections** (総表, 明細表, 定員表) — structurally like case-005/MLIT, not like case-004/MEXT's standalone file. Like case-005, MOJ's own cover-page TOC gives an **exact, page-referenced boundary** for 明細表's own start (printed page 5) independently re-confirmed by rendering that exact page (§5). This protocol therefore treats "correct table" as a **source/universe precondition** (§6.1), following case-005's own reasoning, not case-002/003's row-level treatment — an independently re-derived choice for MOJ's own document structure, not a copy. **Additionally, and newly for this program**: MOJ's own file contains a *third* grammar (定員表, staffing table, unit 人) that no prior case's protocol needed to exclude explicitly, since no prior case's own locked file combined three distinct grammars in one document. This protocol elevates multi-grammar exclusion to its own explicit precondition (§6.1, P2) rather than folding it into the "correct table" language alone. |
| Native item/expense-level code | Document-family-independent; retained unchanged across case-002–005. | **Retained.** MOJ's own 明細表 opening page already shows the same `NN-NN`/`NNNNN-NNNN-NN-NNNN` code-column convention in the same position as every prior case. |
| Multi-line wrap | Retained in all four, each time re-justified as a capability test, not a difficulty-engineering choice. | **Retained, with an explicit re-justification specific to Case-006's own axis**: since no compared engine can currently extract *any* text from this source, this criterion's *immediate* payoff (testing a future engine's deterministic multi-line reconstruction) is deferred rather than realized in Case-006's own first frozen benchmark run. It is retained anyway, for two source-grounded reasons: (1) the eventual Ground Truth is still created by direct human visual transcription, for which multi-line-wrap self-containment remains a meaningful, source-visible property to test; (2) retaining the identical criterion semantics preserves comparability with case-001–005 for any future non-text-based recovery method (e.g., a future OCR or vision-based experiment, explicitly not run in this task) that might one day be evaluated against this same Ground Truth. |
| Standard amount triple | Document-family-independent; retained unchanged across case-002–005. | **Retained.** Confirmed present in the same three-column position on MOJ's own 明細表 opening page (visually, not via any text extraction). |
| Sufficiency / self-containment | Retained in all four, with case-004/005 each extending it to pre-decide page-spanning/blank-triple/embedded-relocation handling. | **Retained, with the same extensions as case-005**, since MOJ's own document is known (§12, Case-006's own source survey) to contain embedded-substructure patterns (a 総表 with its own cross-reference mechanism, a 定員表) analogous to patterns already documented elsewhere in this research program. |
| Correct structural level (row vs. aggregate) | Present in every prior protocol folded into the native-identifier criterion. | **Retained**, folded into C1 as before. |
| Tie-break (earliest `pdfPageIndex`, then topmost row) | Document-family-independent in all four. | **Retained unchanged.** No MOJ-specific reason was found to deviate. |
| Circularity-avoidance (visual-inspection-only enumeration) | The single most important constraint in every prior protocol. | **Retained in full, and structurally reinforced**: since this source has zero extractable text, visual-inspection-only enumeration is not merely a discipline choice here — it is the **only physically possible method** (§13). |

**No concept was rejected outright.** "Correct table" is reclassified to a universe precondition on source-grounded reasoning specific to MOJ's own TOC precision (following case-005's own precedent, independently re-derived for MOJ's own document); a new multi-grammar exclusion precondition is added, reflecting a genuinely new structural fact (three grammars in one file) that no prior case's own protocol needed to address in this explicit form.

## 5. Frozen selection universe

MOJ's locked file is 737 pages and, per its own cover-page TOC (already transcribed in the source survey, re-confirmed via direct rendering of the referenced pages in this task — see below), is subdivided into 8 internal organizations within the 明細表 section:

| 組織 code | Organization | Printed page (per the document's own cover-page TOC) |
|---|---|---|
| 010 | 法務本省 (MOJ's own ministry headquarters) | starts at 5 |
| 020 | 法務総合研究所 | starts at 153 |
| 040 | 検察庁 | starts at 176 |
| 050 | 矯正官署 | starts at 222 |
| 060 | 更生保護官署 | starts at 464 |
| 065 | 法務局 | starts at 537 |
| 075 | 出入国在留管理庁 | starts at 625 |
| 080 | 公安審査委員会 | starts at 705 |
| 090 | 公安調査庁 | starts at 708 |

**Three candidate universes were compared before any expense row was inspected:**

- **(A) Entire 明細表 (all 8 organizations, printed pages 5–~728).** Rejected, for the same reason every prior case rejected its own analogous option: organizations beyond `010` (法務総合研究所, 検察庁, 矯正官署, etc.) are structurally distinct bodies (a research institute, prosecutorial offices, correctional facilities, an immigration agency, quasi-independent commissions) whose own internal budget-line conventions are not yet confirmed to match `010`'s own. Mixing them under one case without confirming layout homogeneity risks the same document-sub-family conflation already avoided in case-003/004/005.
- **(B) First source-defined organizational section: `010 法務本省`.** **Selected.** Justification, from source structure alone: (1) explicitly demarcated by the document's own cover-page TOC, not a convenience boundary; (2) the first organizational section in document order, consistent with the tie-break's own "earliest in document order" philosophy; (3) the ministry's own headquarters section, the structurally closest analog to every prior case's own selected universe (case-002's `010 経済産業本省`, case-003's `010 総務本省`, case-004's `010 文部科学本省`, case-005's `010 国土交通本省`) — each itself the first organization in its own document's internal segmentation. Restricting MOJ's universe to its own `010` keeps the cross-case comparison "ministry headquarters vs. ministry headquarters."
- **(C) Another source-defined universe.** Not adopted: nothing in the TOC or generic page structure singles out any later organization as more appropriate than the first.

**Frozen selection universe: organization `010 法務本省`, printed pages 5 through the page immediately preceding organization `020`'s start (printed page 153).**

**Page-bounds locator convention**: `pdfPageIndex` (0-based) is the authoritative ordering/locator key. The lower bound is **confirmed exact, re-verified in this task**: printed page 5 = PDF page 9 (`pdfPageIndex` 8) — re-rendered directly in this task (not merely re-cited from the source survey) and confirmed to show the 明細表's own title, sheet header (`法（本） 5`), and the `010 法務本省 / 010 法務本省共通費` organization/item-aggregate opening. The upper bound is **not independently re-verified at the boundary page itself**: it is derived from the same +4-page offset observed at the universe's own confirmed start (printed page 5 = PDF page 9) applied forward to printed page 153 (implying `pdfPageIndex` ≈156), but this offset was **not** checked to hold constant across the intervening ~144 pages, and — per this program's own established discipline (case-004's own blank-separator-page finding; case-005's own analogous disclosed uncertainty) — is **not extrapolated with confidence**. This uncertainty is disclosed explicitly: if any blank separator page, embedded sub-table, or other structural irregularity (patterns already confirmed elsewhere in this census, including within MOJ's own document per the source survey's own §12) falls within this range, the true `pdfPageIndex` for organization `020`'s own start could differ from the ≈156 estimate.

**Upper boundary status: unresolved (approximate only), per explicit instruction not to extrapolate with confidence.** Pinning it exactly — by reading the section-heading text on the one or two candidate boundary pages, not any expense row's content — is explicitly permitted as necessary structural navigation for the future task that applies this protocol, and is deferred to that task. Given a deterministic top-to-bottom scan from the universe's own confirmed opening (`pdfPageIndex` 8) is expected to find an eligible row within the first few pages (consistent with every prior case's own experience), the exact upper boundary is not expected to matter for finding the winner — it is recorded as unresolved for completeness and honesty, not because it is expected to change the eventual selection.

## 6. Source/multi-grammar preconditions and eligibility criteria

### 6.1 Source/universe preconditions (not per-row checks)

- **P1 — Correct table.** Every row considered must lie within the frozen universe's page range (§5), itself defined to start exactly at 明細表's own confirmed first page. Satisfied automatically by the universe definition; not re-tested per candidate row.
- **P2 — Correct grammar (multi-grammar exclusion), newly explicit for Case-006.** MOJ's own single combined file contains three distinct document sections with three distinct grammars: 総表 (cross-reference-summary grammar, split 一般行政経費/その他の経費/計 subcolumns, printed pages 1–4), 明細表 (the standard grammar this protocol targets, printed pages 5–728), and 定員表 (staffing/personnel grammar, unit 人, printed page 729 onward). **Only rows within the 明細表 section, as bounded by P1, are eligible.** A row from the 総表 or 定員表 sections — even one that superficially shows request-number-like or code-like tokens — is never eligible under this protocol, regardless of any other property. This precondition is stated explicitly, separate from P1, because MOJ is the first Case-006–010 candidate whose own document mixes three grammars in one file in a way no prior protocol needed to address this explicitly (case-005's own P1 addressed a two-grammar concern — 総表 vs. 明細表 — not three).

### 6.2 Row-level eligibility criteria

A row is **eligible** for Case-006 if and only if all of the following hold, evaluated purely from the page's own visual structure within the frozen universe (P1 and P2 already satisfied):

- **C1 — Native request/expense-level identifier.** The row carries an explicit request-number and/or expense-level code in the document's own numbering scheme, not a bare organizational- or item-level aggregate/header row with no such identifier.
  - *PASS*: an identifier in this format is visually printed in the row's own identifier column(s).
  - *FAIL*: the row is an organization-level (`組織`) or item-level (`項`) aggregate/header row with no such identifier.
  - *Visual determination*: read the printed identifier text directly from the rendered page. **No OCR, no text extraction of any kind** — this source has none.
- **C2 — Multi-line wrap.** The row's expense-name label visually wraps across two or more printed lines.
  - *PASS*: the label visually occupies two or more printed lines within its own cell.
  - *FAIL*: the label fits on a single printed line.
  - *Visual determination*: count printed lines occupied by the label text in the rendered page.
- **C3 — Standard amount triple.** The row carries the document's standard three-column previous-budget / current-year-request / delta relationship, associated with this specific row, in its native layout.
  - *PASS*: all three amount columns are visually present and associated with this row.
  - *FAIL*: one or more is visually absent or unassociated with this specific row.
  - *Visual determination*: read the three amount columns directly from the rendered page.
- **C4 — Self-contained sufficiency.** The row is complete enough to populate every prior-case-schema field expected to be recoverable from the page itself, with the following pre-decided handling of known-possible complications:
  - A row whose amount triple is visually split across a page boundary **FAILS** C4.
  - A row whose own inline amount-triple cells are visually blank, with real amounts apparently relocated into a separate, differently-shaped region (e.g., an embedded matrix, a pattern already documented elsewhere in this research program and structurally analogous to what MOJ's own 総表 section demonstrates for a *different* section of this same file) **FAILS** C4.
  - A row whose label wraps onto an immediately-following printed line within the same visual row block (the ordinary C2 case) is **not** treated as page-spanning under this criterion.
  - *PASS*: the complete row (identifier, label, all three amounts) is visually present within one coherent visual unit.
  - *FAIL*: any required field is only recoverable from a different, non-continuation page or a different structural region.
  - *Visual determination*: confirm all required fields appear within one coherent visual unit on the rendered page(s). **Rendering at higher resolution is permitted if legibility is initially insufficient; OCR is never permitted, at any resolution.**

C1–C4 are new labels for this case, testing the same underlying document-understanding capabilities already validated across case-002–005: native identifier recognition, multi-line reconstruction, amount-triple association, and page/region self-containment.

## 7. Explicit non-criteria

The following must **not** influence eligibility, universe selection, or the tie-break, now or in the future selection task:

- Presence or absence of the `△` (decrease) glyph, or whether the delta is positive or negative.
- Content or population of the 備考 (remarks) column.
- Any prediction, expectation, or hope about how `pdfjs-baseline`, `pymupdf-baseline`, or `docling` will perform on the row — **including the already-known expectation that all three will return a null/empty result**, which must not be used to justify, avoid, or otherwise weight any candidate.
- **Vector path/object count, complexity, or any other property of the PDF's own internal content-stream representation** (e.g., number of `m`/`c`/`l` operators on a given page) — this is Case-006's own research subject at the *document* level, never a per-row selection input.
- The document's PDF `Producer` metadata ("JUST PDF 5") or encryption status (not encrypted) — document-wide facts, not per-row properties, and not selection inputs regardless.
- Similarity or difference to case-001–005's own selected rows (explicitly permitted either way).
- Whether OCR, a future vision-based method, or any alternative-extraction technique would plausibly succeed or fail on the row — no such method is run, evaluated, or anticipated as a selection input in this protocol.
- Any embedded-substructure novelty (e.g., the 総表's own cross-reference mechanism, the 定員表's own existence) beyond what P2 already requires (exclusion from the 明細表 universe) — the mere fact that this document is structurally rich is not a reason to prefer or avoid any particular row within the frozen 明細表 universe.
- Any inferred or asserted correspondence between MOJ's own budget-line items and MOF-CSV or RS/marumie-rssystem concepts — no such correspondence is asserted, assumed, or investigated by this protocol.
- Whether a candidate row is the same one already incidentally observed during the source survey (§13) — its prior visibility neither qualifies nor disqualifies it.
- Amount magnitude or any arithmetic relationship between a candidate row's own previous/current/delta values.
- Proximity to the universe's page-range boundary beyond what the deterministic tie-break itself produces.

## 8. Deterministic tie-break

If more than one row within the frozen universe (organization `010 法務本省`, §5) satisfies C1–C4 (and P1/P2), the tie-break is:

> **The earliest eligible row in document order within the frozen universe** — lowest `pdfPageIndex` (0-based), then topmost eligible row position on that page (top-to-bottom reading order).

No MOJ-specific source property was found that would justify a different tie-break; this matches every prior case's own convention, retained on that basis.

## 9. Ambiguity / continuation-handling rules

Explicit handling, decided before any candidate is inspected:

- **`pdfPageIndex` vs. printed page number**: `pdfPageIndex` is the authoritative ordering key throughout, per §5.
- **Repeated headers / organization- or item-level aggregate rows**: excluded from eligibility entirely by C1, so they cannot participate in the tie-break.
- **Rows beginning on a prior page / continuing onto a later page**: per C4, a row whose amount triple is split across a page boundary FAILS and is excluded from the tie-break entirely.
- **A row's label wrapping onto an immediately-following printed line within the same visual block**: the ordinary C2 case, not page-spanning.
- **A row whose value appears relocated into a separate embedded-region-like structure**: FAILS C4 per §6.2's explicit pre-decision.
- **Multiple qualifying rows on one page**: resolved by top-to-bottom reading order on that page.
- **Insufficient visual evidence to determine PASS/FAIL for a given criterion** (e.g., a rendering artifact obscuring legibility): the row is treated as **not yet eligible**; a higher-resolution re-render (source-preserving, non-OCR) is the only permitted remediation. If still insufficient, record the row's own locator and the specific reason as `insufficient evidence` in the future selection record, and continue scanning — never resolve via OCR.
- **A row that passes C1 but is embedded within, or immediately adjacent to, an unusual/special representation** (analogous to case-004's own anomaly-research findings, or to MOJ's own 総表/定員表 sections if a boundary page happens to show transitional content): the row's own eligibility is judged solely on C1–C4/P1–P2 applied to that row's own visual presentation; the mere presence of an unusual neighboring representation is **not**, by itself, a reason to exclude or prefer the row.
- **Locator mismatch between printed page label and PDF page index**: recorded honestly if found; does not itself affect eligibility.

None of these rules is applied to any actual candidate in this task; they are recorded here so the future selection task can apply them consistently and reproducibly.

## 10. Multi-grammar exclusions (elaboration of P2)

To remove any ambiguity for the future selection task:

- **総表 rows are never eligible**, regardless of whether they show a request-number-like token, an expense-code-like token, or an amount-triple-like structure — the 総表's own grammar (split subcolumns, `明細書頁数` cross-reference) is visually distinguishable from 明細表's own grammar at a glance, and this protocol relies on that visual distinguishability, not on any mechanical check (none is possible for this source).
- **定員表 rows are never eligible** — distinguishable by its own unit (人, not 千円) and its own distinct column set (already confirmed via the document's own cover-page TOC reference, though the 定員表 section itself was not directly rendered in the source survey or in this task).
- If the future selection task encounters a page whose grammar is ambiguous between 明細表 and either excluded grammar, it must treat that page as **outside the universe** (not merely low-confidence) until the ambiguity is resolved by direct visual comparison against a page unambiguously confirmed to belong to each candidate grammar.

## 11. Navigation method for a textless, vector-outline source

Because this source has zero extractable text (confirmed exhaustively in the source survey), the future selection task **cannot** use any text-search-based navigation aid, even as a convenience — a constraint no prior case's own protocol needed to state, since case-001–005 all retained at least the theoretical possibility of text-based page-finding even when not actually used. The frozen navigation method is:

> **Cover-page TOC → organization locator (printed page reference) → printed-page-to-PDF-page mapping (established once, at the universe's own confirmed lower bound, §5) → visual top-to-bottom rendering scan within the frozen universe.**

Locators must be recorded with all of the following kept distinct, per this program's own established convention:

- `pdfPageIndex` (0-based, authoritative)
- 1-based PDF page number
- printed page label (where legible)
- organization code/name
- section (総表 / 明細表 / 定員表)

Where the printed-page-to-PDF-page mapping is uncertain (as it is for the universe's own upper bound, §5), this must be recorded as uncertain, not silently resolved by assumption. The actual visual scan itself is **not performed in this task** — it is deferred to the future selection task, per §9 of the originating instructions.

## 12. Prior-exposure disclosure

The source survey already, necessarily, visually exposed the following while confirming the 明細表's own opening page (§5, PDF page 9):

- Organization `010 法務本省` (組織-level aggregate row, no code).
- Item `010 法務本省共通費` (項-level aggregate row, no code).
- A request-numbered, expense-coded row (`①` / `01-95`) with the label `法務本省一般行政に必要な経費` — structurally the same first-eligible-row-shaped template already seen at the start of every one of case-002 through case-005's own selected rows.

**This disclosure is made honestly, not minimized.** This protocol does **not** claim the author approached MOJ's own document with no memory of this template, nor does it claim a technical sandbox prevented seeing it — no such sandbox exists in this repository's toolset, exactly as already disclosed in every prior case's own protocol. The methodological control is instead that every criterion in §6 is written in abstract, source-structural terms (native identifier presence, multi-line wrap, amount-triple presence, self-containment) that would produce the identical rule regardless of which specific row happens to satisfy them first — none references `①`, `01-95`, `法務本省一般行政に必要な経費`, `本省共通費`, or "the row already seen in the source survey" as a criterion, a tie-break input, or a justification for the universe. If the deterministic rule below happens to select this already-glimpsed row, that is disclosed as a known possibility, not concealed as a surprise — and it is neither sought nor avoided. **No amount value from this row was, or is here, transcribed.**

## 13. Contamination controls

- These rules (§5–§11) are frozen **before** any candidate row within organization `010` is inspected.
- The universe (§5) is defined from the document's own cover-page TOC references, not from any expense row's content.
- No benchmark output or engine behavior for MOJ is consulted (none exists, and none is expected to exist meaningfully given the confirmed representation).
- No Ground Truth for MOJ exists or is consulted.
- No criterion is chosen because it is known to produce or avoid a specific engine-failure mode on MOJ specifically — C1–C4 test the same document-understanding capabilities every prior case tested, independent of this source's own representation.
- The already-disclosed prior exposure (§12) is not used to shape any criterion's substance toward matching the already-seen row.
- Provenance and chronology (this protocol's own commit, preceding any future selection-record commit) are preserved as the audit trail proving the freeze order.

## 14. What was inspected in this task

- Re-verified the source's own SHA-256 against `sources/source-lock.json` and the local raw file.
- Re-rendered PDF page 9 (`pdfPageIndex` 8) to directly re-confirm the 明細表's own opening page and its printed label (`法（本） 5`), rather than merely re-citing the source survey's own prior finding.
- Read the source survey's own already-committed cover-page TOC transcription for organization boundaries (not re-rendered independently in this task, since it was already directly rendered and transcribed in the source survey itself).
- Read case-005's own selection protocol in full, for comparison and methodological continuity (§4).

## 15. What was deliberately not inspected

- No candidate expense row within organization `010` was enumerated, viewed, compared, or ranked.
- The exact PDF-page equivalent of organization `020`'s own start (printed page 153) was not rendered or confirmed — left explicitly unresolved (§5).
- The 定員表 section (printed page 729 onward) was not rendered in this task, consistent with the source survey's own disclosed limitation.
- No sibling special-account or revenue-side document (if any exists for MOJ) was consulted.

## 16. Freeze semantics

This protocol is frozen as of this task's own commit. No candidate row within organization `010 法務本省` has been enumerated, compared, or selected. No Ground Truth exists for Case-006. No benchmark engine, OCR tool, or `npm run docbench` has been run against MOJ at any point in this research program. The next task that applies this protocol must perform eligible-row enumeration by direct visual inspection only (rendering pages within the frozen universe and reading them as a human would), record the selected row and any accidental exposure in a new selection-record artifact, and stop **before Ground Truth** — mirroring every prior case's own two-step selection-then-Ground-Truth sequencing. Per the Case-006–010 Selection Freeze's own binding methodology note, any future first-frozen benchmark run for Case-006 must use the existing, unmodified three-engine pipeline and preserve a null/empty result as-is; that step is not reached by this protocol or its immediate successor task.

## 17. Recommended next task

Apply this frozen protocol via direct visual inspection to select exactly one row from organization `010`'s own portion of MOJ's 明細表, create a selection record, and stop before Ground Truth. **Not executed in this task.**

---

**No candidate rows were enumerated or selected. No Ground Truth was created. No benchmark engine or OCR system was run.**
