# case-005 Selection Protocol (Preregistration) — MLIT (国土交通省) FY2024 General-Account Expenditure Request

Status: **frozen protocol. Row NOT yet selected. No candidate row enumerated or inspected. No Ground Truth. No benchmark engine run against MLIT.**

Date: 2026-09-27 (Asia/Tokyo)

This document defines, in advance of examining any specific candidate row, how the case-005 target row will eventually be selected from the already-locked MLIT source. It is committed before any row is identified so the choice cannot be influenced — consciously or not — by knowledge of how any engine performs, by any parser-failure pattern, by desired difficulty, or by resemblance to case-002/003/004's own selected rows. Actual row selection is a **separate, later task** that applies this protocol; this task does not perform it.

## 1. Purpose

> Which row should become the single case-005 target, chosen from a source-defined MLIT universe without using Ground Truth, benchmark-engine behavior, known parser weaknesses, desired difficulty, or the specific values already incidentally observed during the source survey?

This protocol freezes, in order: frozen source identity → prior-exposure disclosure → critique of prior protocols → selection universe → source/table preconditions → eligibility criteria → PASS/FAIL determination rules → explicit non-criteria → deterministic tie-break → ambiguity/continuation handling → contamination controls → what was deliberately not inspected → freeze statement → next task.

## 2. Frozen source identity

- `sourceId`: `mlit-fy2024-general-account-expenditure-request`
- Title: 令和6年度歳出概算要求書（一般会計）
- Official PDF: `https://www.mlit.go.jp/page/content/001630995.pdf`
- SHA-256 (re-verified against `sources/source-lock.json` immediately before writing this protocol, and independently against the local raw file via `shasum -a 256`, both matching, unchanged since the case-005 source survey): `4eebb84cec72a4b3b11a2b89c41093550bef5a07095d5c7b178e238406b08217`
- Size: 2,115,896 bytes; 1,097 pages; A4 landscape; PDF 1.3; Producer "List Creator"; **not encrypted**.
- This protocol does not re-lock, re-acquire, or otherwise modify the source. Verified via `git status`/`git fetch` immediately before this task's first edit: branch `research/case-005-mlit-source-survey` at `314da39`, `origin/main` at `34c9424`, working tree clean; `sources/source-lock.json` and `sources/raw/` unchanged.
- Established source-of-truth for all structural facts below: `fixtures/document-understanding/case-005/20260927_0806_Case005_MLIT_Source_Survey.md` (the source survey). **No new PDF inspection was performed in this task** — every structural fact cited below was already established and already committed before this task began.

## 3. Prior-exposure disclosure

The source survey already, necessarily, visually exposed the following values while characterizing the document's packaging and table structure:

- Organization `010　国土交通本省` (組織-level aggregate row, no code).
- Item `002　国土交通本省共通費` (項-level aggregate row, no code).
- Request no. `①`, expense code `05-95`, label `国土交通本省一般行政に必要な経費` — the first coded expense row on 明細表's own first page.

**This disclosure is made honestly, not minimized.** This protocol does **not** claim the author approached MLIT with no memory of these values, nor does it claim a technical sandbox prevented seeing them — no such sandbox exists in this repository's toolset, exactly as already disclosed in case-004's own packaging review. The methodological control is instead that every criterion in §6 below is written in **abstract, source-structural terms** (native identifier presence, multi-line wrap, amount-triple presence, structural level, self-containment) that would produce the identical rule regardless of which specific row happens to satisfy them first — none references `①`, `05-95`, `一般行政に必要な経費`, `本省共通費`, or "the first row seen in the source survey" as a criterion, a tie-break input, or a justification for the universe. If the deterministic rule below happens to select this already-glimpsed row, that is disclosed as a known possibility, not concealed as a surprise — and it is neither sought nor avoided, exactly as case-004's own protocol treated its analogous situation.

**Methodological note on representation fidelity**: earlier, informal web/chat-level pre-survey observation described the request number as plain `1`; direct visual inspection of the source in the committed survey confirmed it is actually printed as the circled numeral `①`. This is recorded as a concrete instance of a general rule this protocol adopts explicitly: **a web page's or chat transcript's textual rendering of a source value is never treated as a substitute for the source's own visual fact.** Every value this protocol or any future case-005 task relies on must trace to direct inspection of the locked PDF itself.

## 4. Critique of prior protocols (case-002 E1–E5 / case-003 ME1–ME5 / case-004 MX1–MX4)

| Concept | Classification pattern across case-002/003/004 | Re-evaluation for MLIT |
|---|---|---|
| "Correct table" (明細表, not 総表/目次/定員表) | **Row-level eligibility criterion** in case-002 (E1) and case-003 (ME1), because both lock one combined PDF where 明細表 is embedded mid-document after 総表. **Reclassified to a source/universe precondition** in case-004 (MX-series dropped it entirely), because MEXT's locked file is *already*, in its entirety, a standalone 明細表-only PDF — no row inside it could ever fail the test. | MLIT's locked source is a **single combined PDF** containing 目次 + 総表 + 明細表 together — structurally like METI/MIC (case-002/003), not like MEXT (case-004). However, unlike case-002/003 (where the exact 明細表-start page was established but not treated as a hard universe boundary), MLIT's own document-wide 目次 gives an **exact, source-stated page number** for 明細表's own start (printed page 19), independently cross-confirmed in the survey by directly rendering that exact page and finding the 明細表 title and column headers there. Given this precise, doubly-confirmed boundary exists, this protocol treats "correct table" as a **source/universe precondition** (like case-004), not a per-row criterion (like case-002/003) — the universe's own lower bound (§5) is fixed at the confirmed 明細表 start, so no row within the frozen universe could ever be a 総表/目次 row. This is a deliberate, source-grounded departure from case-002/003's choice, not a copy of either precedent. |
| Native item/expense-level code | Document-family-independent; retained unchanged across all three prior protocols. | **Retained.** MLIT's own 明細表 first page already shows the same code-column convention (`NN-NN`-shaped codes) in the same position as every prior case. |
| Multi-line wrap | Retained in all three, each time with an explicit re-justification that it tests a capability, not a known failure mode, since no engine had run against that case yet. | **Retained, same re-justification.** No engine has run against MLIT; this remains a capability-comparability criterion (deterministic multi-line label reconstruction), not a difficulty-engineering choice. |
| Standard amount triple | Document-family-independent; retained unchanged across all three. | **Retained.** Confirmed present in the same three-column position on MLIT's own 明細表 first page. |
| Sufficiency / self-containment | Retained unchanged in case-002/003; in case-004, additionally had to confront a newly-observed "blank inline triple, real values in a nested sub-line" pattern (found only *after* selection, in a different organization sampled during later diagnostic work, not built into MX4 itself). | **Retained, and explicitly extended** (§6, criterion C4) to pre-decide how to handle page-spanning values, blank inline triples, and any value apparently relocated into a separate matrix-like region — patterns already documented as real possibilities in this research program (case-004's own selection record and later anomaly surveys), even though none has yet been observed on MLIT's own 明細表 pages. |
| Correct structural level (row vs. aggregate) | Present in every prior protocol as part of the "native code" criterion (an aggregate row has no code). | **Retained**, folded into the native-identifier criterion (§6, C1) exactly as before — not elevated to a separate named criterion, since no MLIT-specific reason was found to treat it differently. |
| Tie-break (earliest `pdfPageIndex`, then topmost row) | Document-family-independent concept in all three; case-003/004 additionally needed an explicit selection-universe decision first because of internal organizational segmentation. | **Retained unchanged.** MLIT also has internal organizational segmentation (12 organizations, §5), so the same universe-then-tie-break sequencing already established for case-003/004 applies; no MLIT-specific reason was found to deviate from lowest-`pdfPageIndex`-then-topmost-row. |
| Circularity-avoidance (visual-inspection-only enumeration) | The single most important constraint in every prior protocol, always retained in full. | **Retained in full**, extended to the universe decision itself, exactly as case-003/004 already established. |

**No concept was rejected outright.** One ("correct table") is reclassified from a row-level test to a universe precondition, on source-grounded reasoning specific to MLIT's own TOC precision — not copied from case-002/003's row-level treatment nor from case-004's precondition treatment, but independently re-derived.

## 5. Frozen selection universe

MLIT's locked file is 1,097 pages and, per its own document-wide 目次 (already transcribed in the source survey, not re-inspected in this task), is subdivided into 12 internal organizations:

| 組織 code | Organization | Printed page (per the document's own 目次) |
|---|---|---|
| 010 | 国土交通本省 (MLIT's own ministry headquarters) | starts at 19 |
| 035 | 国土技術政策総合研究所 | starts at 500 |
| 045 | 国土地理院 | starts at 572 |
| 048 | 海難審判所 | starts at 599 |
| 050 | 地方整備局 | starts at 606 |
| 060 | 北海道開発局 | starts at 694 |
| 070 | 地方運輸局 | starts at 768 |
| 080 | 地方航空局 | starts at 845 |
| 095 | 観光庁 | starts at 859 |
| 100 | 気象庁 | starts at 898 |
| 105 | 運輸安全委員会 | starts at 975 |
| 110 | 海上保安庁 | starts at 995 |

**Three candidate universes were compared before any row was inspected:**

- **(A) Entire 明細表 (all 12 organizations, printed pages 19–~1097).** Strongest document-wide determinism. **Rejected**, for the same reason every prior case rejected its own analogous option: organizations beyond `010` (国土技術政策総合研究所, 国土地理院, 地方整備局, 北海道開発局, etc.) are structurally distinct bodies — regional bureaus, research institutes, and quasi-independent agencies — and nothing is currently known about whether their internal budget-line conventions match `010`'s own. Selecting across all 12 without first confirming layout homogeneity risks silently mixing document sub-families under one case (the same ADR-010 layer-conflation concern already raised for case-003/004).
- **(B) First source-defined organizational section: `010　国土交通本省`.** **Selected.** Justification, from source structure alone: (1) it is explicitly demarcated by the document's own 目次, not a convenience boundary invented for this protocol; (2) it is the first organizational section in document order, consistent with the "earliest in document order" philosophy already governing the tie-break; (3) it is the ministry's own headquarters operating-budget section, the structurally closest analog to case-002's `010 経済産業本省`, case-003's `010 総務本省`, and case-004's `010 文部科学本省` — every one of which was itself the *first* organization in its own document's internal segmentation, kept as that case's universe over any external-bureau/affiliated-institution section. Restricting MLIT's universe to its own `010` keeps the cross-case comparison "ministry headquarters vs. ministry headquarters," not diluted by a fifth, structurally different comparison point.
- **(C) Another source-defined universe.** Not adopted: nothing in the 目次 or generic page structure singles out any later organization as more appropriate than the first, and no TOC/structural justification stronger than (B) exists for any alternative.

**Frozen selection universe: organization `010　国土交通本省`, printed pages 19 through the page immediately preceding organization `035`'s start (printed page 500).**

**Page-bounds locator convention**: `pdfPageIndex` (0-based) is the authoritative ordering/locator key, matching this repository's established convention; the printed page label is recorded for human cross-reference only. The lower bound is **confirmed exact**: printed page 19 = `pdfPageIndex` 28 (PDF page 29), independently verified in the source survey by rendering that exact page and finding the 明細表 title, sheet header, and column headers there. The upper bound is **not independently re-verified** in this task: it is derived by extrapolating the `pdfPageIndex = printedPage + 9` offset the survey confirmed at three sample points spanning printed pages 10–19 (i.e., `pdfPageIndex` 19–28) forward to printed page 500 (`pdfPageIndex` ≈509) — an extrapolation across roughly 480 further pages that was **not** independently checked at that specific boundary. This uncertainty is disclosed explicitly, not hidden: if the offset drifts anywhere in that span (e.g., due to inserted blank pages, a differently-paginated sub-section, or any other structural irregularity not yet observed), the true `pdfPageIndex` for organization `035`'s own start could differ from 509. Per the same discipline already established in case-004's own protocol, **pinning this boundary exactly — by reading the section-heading text on the one or two candidate boundary pages, not any row's content — is explicitly permitted as necessary structural navigation for the future task that applies this protocol**, and is deferred to that task rather than performed here (this task performs no new PDF inspection at all, per §2).

If no row within organization `010` satisfies every eligibility criterion below (considered unlikely given ~480 pages of ledger content, but not ruled out), the correct response in the future selection task is to report that honestly and treat widening the universe as a new, separately justified decision — not an automatic fallback to organization `035` or beyond.

## 6. Source/table preconditions and eligibility criteria

### 6.1 Source/universe precondition (not a per-row check)

- **P1 — Correct table.** Every row considered must lie within the frozen universe's page range (§5), which is itself defined to start exactly at 明細表's own confirmed first page. This precondition is satisfied automatically, for every row in the universe, by the universe definition itself — it is not re-tested per candidate row (see §4's critique for why this differs from case-002/003's row-level treatment of the analogous concept).

### 6.2 Row-level eligibility criteria

A row is **eligible** for case-005 if and only if all of the following hold, evaluated purely from the page's own visual structure within the frozen universe:

- **C1 — Native request/expense-level identifier.** The row carries an explicit request-number and/or expense-level code in the document's own numbering scheme (structurally analogous to every prior case's `NNN`/`NN-NN`-shaped codes), not a bare organizational- or item-level aggregate/header row with no such identifier.
  - *PASS*: an identifier in this format is visually printed in the row's own identifier column(s).
  - *FAIL*: the row is an organization-level (`組織`) or item-level (`項`) aggregate/header row with no such identifier.
  - *Visual determination*: read the printed identifier text directly from the rendered page.
- **C2 — Multi-line wrap.** The row's expense-name label visually wraps across two or more printed lines, exercising the same deterministic multi-line cell-reconstruction capability tested in every prior case (kept for capability-comparability, per §4, not difficulty-engineering).
  - *PASS*: the label visually occupies two or more printed lines within its own cell.
  - *FAIL*: the label fits on a single printed line.
  - *Visual determination*: count printed lines occupied by the label text in the rendered page.
- **C3 — Standard amount triple.** The row carries the document's standard three-column previous-budget / current-year-request / delta relationship, associated with this specific row, in its native layout.
  - *PASS*: all three amount columns are visually present and associated with this row.
  - *FAIL*: one or more is visually absent or unassociated with this specific row.
  - *Visual determination*: read the three amount columns directly from the rendered page.
- **C4 — Self-contained sufficiency.** The row is complete enough to populate every prior-case-schema field expected to be recoverable from the page itself, with the following pre-decided handling of known-possible complications (none yet observed on MLIT's own 明細表 pages, but explicitly pre-decided per this task's own instruction, not left to be improvised later):
  - A row whose amount triple is visually split across a page boundary **FAILS** C4 and is excluded from the tie-break entirely — not selected and then patched from an adjacent page.
  - A row whose own inline amount-triple cells are visually blank, with the row's real amounts apparently relocated into a separate, differently-shaped region of the page (e.g., an embedded matrix or cross-referenced sub-table, a pattern already documented elsewhere in this research program) **FAILS** C4 — the row's own native layout must carry its own triple directly, not by reference to another region.
  - A row whose label wraps onto an immediately-following printed line within the same visual row block (the ordinary C2 case) is **not** treated as page-spanning under this criterion.
  - *PASS*: the complete row (identifier, label, all three amounts) is visually present within one coherent visual unit, as described above.
  - *FAIL*: any required field is only recoverable from a different, non-continuation page or a different structural region.
  - *Visual determination*: confirm all required fields appear within one coherent visual unit on the rendered page(s).

C1–C4 are new labels for this case, deliberately not literally copied from case-004's `MX1`–`MX4` naming, though they test the same underlying document-understanding capabilities already validated across three prior cases: native identifier recognition, multi-line reconstruction, amount-triple association, and page/region self-containment.

## 7. Explicit non-criteria

The following must **not** influence eligibility, universe selection, or the tie-break, now or in the future selection task:

- Presence or absence of the `△` (decrease) glyph on the specific candidate row's own delta, or whether the delta is positive or negative.
- Content or population of the 備考 (remarks) column.
- Docling's table-grid geometry on the candidate page.
- Any prediction, expectation, or hope about how `pdfjs-baseline`, `pymupdf-baseline`, or `docling` will perform on the row.
- Expected benchmark score, perceived difficulty, or convenience of transcription.
- CJK-spacing artifacts of the kind already documented and normalized elsewhere in this benchmark (`closeCjkWrapSpaces`).
- The document's PDF `Producer` metadata ("List Creator" — a document-wide fact, not a per-row property, and not a selection input regardless).
- Encryption compatibility — moot for this specific source (confirmed unencrypted in the survey), but stated for completeness and consistency with every prior protocol's own non-criteria list.
- Similarity or difference to case-002/003/004's own selected rows (explicitly permitted either way, per §1/§3).
- Whether the row's page, or nearby pages, contain a `繰入` (transfer-into)-shaped expression — already confirmed present elsewhere in this document's 総表 (source survey §10), but explicitly **not** a selection input: this protocol does not seek, avoid, or otherwise weight candidacy based on `繰入` presence. Any future research interest in `繰入`-shaped rows is a **separate, later research question**, not resolved or advanced by this protocol.
- Any inferred or asserted correspondence between MLIT's `繰入`-shaped expressions and MOF-CSV concepts (`繰入`, `移替`, or any other budget-lifecycle category) — no such correspondence is asserted, assumed, or investigated by this protocol.
- Whether a candidate row would confirm or falsify any hypothesis formed from case-001–004 (CJK-spacing strategy, annotation-contamination, Docling grid-misalignment, pagination-context loss, structural-anomaly-signal findings, etc.) — those remain observations to make *after* the row is frozen and Ground Truth exists, never selection inputs.
- Amount magnitude or any arithmetic relationship between a candidate row's own previous/current/delta values.
- Whether a candidate row is the same one already incidentally observed during the source survey (§3) — its prior visibility neither qualifies nor disqualifies it.
- Proximity to the universe's page-range boundary beyond what the deterministic tie-break itself produces.

No item was removed from this list relative to the categories the originating task itself enumerated; each is retained because no MLIT-specific source property was found that would justify treating it as relevant to selection.

## 8. Deterministic tie-break

If more than one row within the frozen universe (organization `010　国土交通本省`, §5) satisfies C1–C4, the tie-break is:

> **The earliest eligible row in document order within the frozen universe** — lowest `pdfPageIndex` (0-based), then topmost eligible row position on that page (top-to-bottom reading order).

No MLIT-specific source property was found in the survey that would justify a different tie-break; this matches every prior case's own convention exactly, retained on that basis, not copied without consideration.

## 9. Ambiguity / continuation-handling rules

Explicit handling, decided before any candidate is inspected:

- **`pdfPageIndex` vs. printed page number**: `pdfPageIndex` is the authoritative ordering key throughout, per §5. It is not currently known whether MLIT's printed-label convention (bare `"N　国"` on 総表 pages vs. `"国（本） N"` on 明細表 pages, per the source survey) is stable throughout organization `010`'s own ~480 pages — this does not block the tie-break, which does not depend on the printed label's own stability.
- **Repeated headers / organization- or item-level aggregate rows**: excluded from eligibility entirely by C1 (no native identifier), so they cannot participate in the tie-break regardless of position.
- **Rows beginning on a prior page / continuing onto a later page**: per C4, a row whose amount triple is split across a page boundary FAILS and is excluded from the tie-break entirely.
- **A row's label wrapping onto an immediately-following printed line within the same visual block**: this is the ordinary C2 case, not page-spanning, anchored at the row's own first identifying line.
- **A row whose value appears relocated into a separate embedded-matrix-like region**: FAILS C4 per §6.2's explicit pre-decision, excluded from the tie-break.
- **Multiple qualifying rows on one page**: resolved by top-to-bottom reading order on that page.
- **Insufficient visual evidence to determine PASS/FAIL for a given criterion on a given row** (e.g., illegible text, ambiguous line-wrap boundary): the row is treated as **not yet eligible** — continue scanning to the next candidate in document order, and record the ambiguous row's own locator and the specific reason for the ambiguity in the future selection record, rather than silently resolving the ambiguity in either direction.
- **A row that is structurally coded (passes C1) but embedded within, or immediately adjacent to, an unusual/special representation** (e.g., a page containing both an ordinary row and a differently-shaped matrix region, per the general pattern already documented in case-004's own anomaly research): the row's own eligibility is judged solely on C1–C4 applied to that row's own visual presentation; the mere presence of an unusual neighboring representation on the same page is **not**, by itself, a reason to exclude or prefer the row (see §7's non-criteria list).

None of these rules is applied to any actual candidate in this task; they are recorded here so the future selection task can apply them consistently and reproducibly.

## 10. Contamination controls

- These rules (§5–§9) are frozen **before** any candidate row within organization `010` is inspected.
- The universe (§5) is defined from the document's own 目次 page-number references, not from any row's content.
- No benchmark output or engine behavior for MLIT is consulted (none exists).
- No Ground Truth for MLIT exists or is consulted.
- No criterion is chosen because it is known, from case-001–004, to produce or avoid a specific failure mode on MLIT specifically — C1–C4 test the same document-understanding capabilities every prior case tested, not MLIT-specific known weaknesses (none are known, since no engine has run against MLIT).
- The already-disclosed prior exposure (§3) is not used to shape any criterion's substance toward matching the already-seen row; each criterion was written to be satisfiable by many different possible rows, not tailored to the one already glimpsed.
- Provenance and chronology (this protocol's own commit, preceding any future selection-record commit) are preserved as the audit trail proving the freeze order.

## 11. What was deliberately not inspected

Per §2/§5, this task performed **no new PDF inspection** — every structural fact used here was already established and committed in the source survey. In particular, this task did **not**:

- Render or read any page within organization `010`'s own 明細表 range beyond what the source survey already rendered (its own first page).
- Enumerate, compare, or rank any candidate row.
- Pin the exact `035`-organization boundary (left as an extrapolated, explicitly-flagged-uncertain estimate, §5).
- Investigate the 総表's own `繰入`-shaped rows any further than the source survey's own existence-only confirmation.
- Consult any sibling special-account or revenue-side PDF also linked from MLIT's landing page.

## 12. Freeze statement

This protocol is frozen as of this task's own commit. No candidate row within organization `010　国土交通本省` has been enumerated, compared, or selected. No Ground Truth exists for case-005. No benchmark engine, OCR tool, or `npm run docbench` has been run against MLIT at any point in this research program. The next task that applies this protocol must perform eligible-row enumeration by direct visual inspection only (rendering pages within the frozen universe and reading them as a human would, per the same method already established in case-002/003/004), record the selected row and any accidental exposure in a new selection-record artifact, and stop **before Ground Truth** — mirroring every prior case's own two-step selection-then-Ground-Truth sequencing.

## 13. Next task

Apply this frozen protocol via direct visual inspection to select exactly one row from organization `010`'s own portion of MLIT's 明細表, create a selection record, and stop before Ground Truth. **Not executed in this task.**
