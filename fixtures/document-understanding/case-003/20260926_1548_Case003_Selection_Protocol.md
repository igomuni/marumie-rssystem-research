# case-003 Selection Protocol (Preregistration) — MIC (総務省) FY2024 Detailed Expenditure Request

Status: **frozen protocol. Row NOT yet selected. No Ground Truth. No benchmark engine run against MIC. No candidate row enumerated or inspected.**

Date: 2026-09-26 (Asia/Tokyo)

This document defines, in advance of examining any specific candidate row, how the case-003 target row will eventually be selected from the already-locked MIC source. It is committed before any row is identified so the choice cannot be influenced — consciously or not — by knowing how any engine performs, by any parser-failure pattern, or by convenience of transcription. Actual row selection is a **separate, later task** that applies this protocol; this task does not perform it.

## Purpose

> Before seeing candidate outcomes, what deterministic, source-appropriate procedure selects one benchmark row from MIC's large, internally segmented detailed request document?

This protocol freezes, in order: document identity → selection universe → allowed/excluded inspection → eligibility criteria → non-criteria → deterministic tie-break → locator convention → accidental-exposure policy → stop condition.

## Source identity (confirmed, unchanged)

- `sourceId`: `mic-fy2024-general-account-expenditure-request`
- Title: 令和6年度歳出予算概算要求書（一般会計）(FY2024 general-account expenditure request document), "20 総務省所管" cover
- URL: `https://www.soumu.go.jp/main_content/000901372.pdf`
- SHA-256 (verified against `sources/source-lock.json` immediately before writing this protocol, unchanged since the case-003 source survey): `cc54dbe5f689116619a1f8453747d47bca5b960137f90869ead26954d651703b`
- Size: 876,768 bytes; 454 pages; A4 landscape; Producer "List Creator"; not encrypted (per `pdfinfo`, recorded in the source survey)
- This protocol does not re-lock, re-acquire, or otherwise modify the source. Verified via `git diff` immediately before this task's first edit: `sources/source-lock.json` and `sources/raw/` are unchanged from the prior task's commit (`a12ce47`).
- Established source-of-truth for all structural facts below: `fixtures/document-understanding/case-003/20260926_1443_Case003_MIC_Source_Survey.md` (the source survey), specifically its table-of-contents transcription and page-10 generic-column-header observation. **No new PDF inspection was performed in this task** — every structural fact cited below was already established, and already committed, before this task began.

## Relationship to case-002 methodology

This protocol reuses `fixtures/document-understanding/case-002/20260926_0834_Case002_Selection_Protocol.md`'s overall shape (deterministic, document-family-independent eligibility criteria + explicit non-criteria + engine-blind visual enumeration + earliest-in-document-order tie-break), but does not mechanically copy it. Each element of case-002's E1–E5 was individually re-evaluated:

| case-002 concept | Classification for MIC | Disposition |
|---|---|---|
| E1 — row belongs to 明細表, not 総表 | Document-family-independent | **Retained**, reworded: MIC's own TOC explicitly distinguishes `令和6年度歳出概算要求額総表` (総表, page 1) from `令和6年度歳出概算要求額明細表` (明細表, page 5 onward) — the identical structural distinction, confirmed from MIC's own source, not assumed from case-002's precedent. |
| E2 — native expense-level code, not a bare subtotal/header row | Document-family-independent | **Retained** unchanged in substance. MIC's page-10 generic-column inspection (survey, already committed) showed native numeric code fields (e.g. `NN-NNNN`, `NNNNN-NNNN-NN-NNNN`-shaped codes) in the same column position as case-001/002's expense codes. |
| E3 — multi-line wrap required | Requires explicit re-justification (task's own caution) | **Retained, with justification below** — see "On retaining E3" below. Not mechanically copied without re-examination. |
| E4 — standard previous/current/delta amount triple | Document-family-independent | **Retained** unchanged in substance. MIC's page-10 inspection showed the same three-column relationship (前年度予算額 / 6年度概算要求額 / 対前年度比較増△減) as case-001/002's previousBudget/fy2024Request/delta triple. |
| E5 — sufficiency (not split across a page boundary) | Document-family-independent | **Retained** unchanged. |
| Non-criterion: `△` glyph presence/absence | Document-family-independent | **Retained.** No MIC row's sign has been observed; this remains a non-criterion for the same reason it was one for case-002 (a document-wide convention observed generically on page 10 — `△` glyphs are visible in that column — but which specific rows carry one is unknown and must stay unknown until Ground Truth). |
| Non-criterion: hierarchy ambiguity | Document-family-independent | **Retained.** Whether MIC exhibits the same `NNN <name>`-shaped multi-candidate ambiguity found in case-001/002 is completely unknown (no engine has run against MIC) and must not be engineered toward or away from. |
| Circularity-avoidance (visual-inspection-only enumeration, no compared engine) | Document-family-independent — the single most important methodological constraint, per case-002's own framing | **Retained in full**, extended below to explicitly cover the *universe decision itself*, not just the eventual row enumeration (see "Selection universe" below). |
| Tie-break: earliest eligible row in document order | Document-family-independent *concept*; MIC requires an explicit **selection-universe decision first** that case-002 never needed to make explicit | **Retained as the underlying philosophy**, but see "Selection universe" — MIC's internal organizational segmentation (absent, or at least never surfaced, in case-002's protocol) means "document order" must be scoped to a frozen universe before it is executable. |

**On retaining E3 (multi-line wrap):** the task's instructions specifically warn that requiring multi-line wrapping (or `△`, delta sign, annotation placement, hierarchy ambiguity, or any other known-parser-challenging feature) risks becoming an outcome-selection criterion. This risk applies most directly to a criterion chosen *because* it is known to break a specific engine. That is not the situation here: **no engine has been run against MIC**, so there is no known MIC-specific failure mode E3 could be selecting for or against. E3's actual function is to ensure the selected row exercises the same document-understanding *capability* (deterministic multi-line label reconstruction) that case-001 and case-002 both exercised — this is a capability-comparability decision (keeping what is measured consistent across cases), not a difficulty-engineering decision. It is retained on that basis, with the explicit caveat that if it turns out no row in the frozen universe satisfies E3, the correct response is to report that honestly (and reconsider E3, or the universe, in a future task) — not to quietly drop E3 after seeing which rows would otherwise qualify.

**No case-002 concept was rejected outright** — every one was either retained unchanged, retained with MIC-specific rewording, or retained with additional justification. None was found to be METI-specific or inapplicable to MIC's document family (both are 歳出概算要求書-titled, ledger-style, `List Creator`-produced documents with visually confirmed matching column structure).

## Selection universe (the key decision)

MIC's document is 454 pages and, per its own table of contents (already transcribed in the source survey, not re-inspected in this task), its `令和6年度歳出概算要求額明細表` (detail table) spans pages 5–450 and is itself subdivided by **internal organization** (`組織`):

| 組織 code | Organization | Page range (from the document's own TOC) |
|---|---|---|
| 010 | 総務本省 (MIC's own ministry headquarters) | 5–245 (241 pages) |
| 040 | 管区行政評価局 (regional administrative evaluation bureaus) | 246–263 (18 pages) |
| 050 | 総合通信局 (regional telecommunications bureaus) | 264–279 (16 pages) |
| 070 | 公害等調整委員会 (Environmental Dispute Coordination Commission) | 280–290 (11 pages) |
| 080 | 消防庁 (Fire and Disaster Management Agency) | 291–450 (160 pages) |

This segmentation has no analog that was ever made explicit in case-002's protocol or selection record — case-002's document either does not have comparably-sized, separately-headed external-bureau sections, or case-002 simply never needed to notice them, because its selected row happened to fall within the ministry's own headquarters section (`経済産業本省`) regardless. MIC's document forces this decision to be made explicitly and in advance.

**Three candidate universes were compared before any row was inspected:**

- **(A) Entire 明細表 (pages 5–450, all five organizations).** Strongest document-wide determinism (a single "earliest eligible row" rule over the whole detail table, no organization-choice judgment call needed). **Rejected**: 040/050/070/080 are structurally distinct organizational bodies — regional bureaus and a quasi-independent commission/external agency, not the ministry's own headquarters — and nothing is currently known about whether their internal budget-line conventions, code formats, or table layout match 010's (or each other's). Selecting from across all five without first confirming layout homogeneity risks silently mixing document sub-families under one case, which is exactly the kind of layer-conflation this repository's architecture work (`protocol/DECISIONS.md` ADR-010) argues against.
- **(B) First source-defined organizational section: 010 総務本省 (pages 5–245).** **Selected.** Justification, from source structure alone: (1) it is explicitly, unambiguously demarcated by the document's own table of contents — not a convenience boundary invented for this protocol; (2) it is the first organizational section in document order, consistent with the same "earliest in document order" philosophy that already governs the tie-break within a page; (3) it is the ministry's own headquarters operating-budget section, structurally the closest analog to what case-001 (Digital Agency, a single-ministry-body document) and case-002 (経済産業本省, METI's own ministry headquarters, not an external bureau) already tested — case-002's actual selected row was under `010 経済産業本省` specifically, not any external-bureau equivalent, so restricting MIC's universe to its own `010` organization keeps the cross-case comparison to "ministry headquarters vs. ministry headquarters," not "ministry headquarters vs. external regional bureau." This inference about case-002 is stated cautiously: case-002's protocol never explicitly excluded external-bureau sections because it apparently never needed to (no such sections were mentioned in its selection record); it is not confirmed here that METI's document lacks such sections entirely.
- **(C) Another source-defined universe (e.g. a specific later organization).** Not adopted: nothing in the TOC or generic page structure singles out any other organization as more appropriate than the first, and the task requires clear TOC/structural justification for any universe other than A or B, which is not available here.

**Frozen selection universe: 010 総務本省, PDF pages 5–245 inclusive** (per the document's own table of contents), within `令和6年度歳出概算要求額明細表`.

If no row in this universe satisfies every eligibility criterion below (an edge case considered unlikely given 241 pages of ledger content, but not ruled out), the correct response in the future selection task is to report that honestly and treat widening the universe as a new, separately justified decision — not an automatic fallback to organization 040 or beyond.

## Allowed structural inspection (already performed, in the prior survey task)

Limited to: table of contents; section/organization headings and their page ranges; generic column headers (request number / item+code / previous budget / current request / delta / remarks); the general presence of the `△` glyph *as a document-wide legend/convention*, not tied to any specific row; page orientation/size. All of this was established in `20260926_1443_Case003_MIC_Source_Survey.md` before this task began; no new rasterization was performed to write this protocol.

## Excluded information (not inspected, and not to be inspected before this protocol's future selection task freezes a row)

Individual candidate row names, item/expense codes, amounts, signs, wrapping behavior, or annotation placement anywhere within pages 5–245. No candidate row has been enumerated. No page within the universe (other than page 10, inspected during the *prior* source-survey task purely for generic column-header identification, not for row eligibility, and not re-inspected here) has been viewed.

## Eligibility criteria (numbered, source-observable, visually decidable)

A row is **eligible** for case-003 if and only if all of the following hold, evaluated purely from the page's own visual structure within the frozen universe (010 総務本省, pages 5–245):

- **ME1 — Correct table.** The row belongs to `令和6年度歳出概算要求額明細表` (the detail table), not `総表` (page 1) or `定員表` (page 451 onward, outside the frozen universe regardless).
- **ME2 — Native item/expense-level code.** The row carries an explicit item or expense-level code in the document's own numbering scheme (structurally analogous to case-001/002's `NNN`/`NN-NN`-shaped codes, or MIC's own longer numeric code format observed generically on page 10), not a bare organizational/item-level subtotal or a header-only row with no code.
- **ME3 — Multi-line wrap.** The row's item name and/or expense name visually wraps across two or more printed lines, exercising the same multi-line cell-reconstruction capability tested in case-001 and case-002 (see justification above; not adopted as a difficulty-engineering criterion).
- **ME4 — Standard amount triple.** The row carries the document's standard three-column previous-budget / current-year-request / delta relationship in its native layout, structurally analogous to case-001/002, so the same benchmark fields remain meaningful and comparable.
- **ME5 — Sufficiency.** The row is complete enough to populate every case-001/002-schema field expected to be recoverable from the page itself — i.e. not a row whose amount triple is split across a page boundary or otherwise physically unrecoverable from a single page.

## Explicit non-criteria

The following must **not** influence eligibility, tie-break, or universe selection, now or in the future selection task:

- Presence or absence of the `△` (decrease) glyph on the specific candidate row's own delta.
- Whether the row's page also exhibits header-row hierarchy ambiguity (multiple `NNN <name>`-shaped candidate rows).
- Placement of the 備考 (remarks/annotation) column relative to the amount triple (same-line vs. continuation-line) — this was the specific structural feature that broke `common.mjs`'s trailing-triple regex on case-002; selecting for or against its presence on MIC would make case-003 a targeted regression test rather than a genuine out-of-sample generalization test.
- Any prediction, expectation, or hope about how any of the three benchmark engines (pdfjs-baseline, pymupdf-baseline, docling) will perform on the row.
- Convenience of transcription, "representativeness," typicality, or any other subjective quality judgment.
- Proximity to the universe's page-range boundary (page 5 vs. page 245) beyond what the deterministic tie-break itself produces.

## Deterministic tie-break

If more than one row within the frozen universe (010 総務本省, pages 5–245) satisfies ME1–ME5, the tie-break is:

> **The earliest eligible row in document order within the frozen universe** — lowest PDF page index (0-based, matching this repository's `pdfPageIndex` convention), then topmost eligible row position on that page (top-to-bottom reading order).

Explicit handling:

- **PDF index vs. printed page number**: PDF page index (0-based) is the authoritative ordering key, not the document's own printed page label. This is a deliberate departure from stating printed-label ordering as primary, because it is currently **unknown** whether MIC's printed page numbering resets or changes convention at any point within pages 5–245 (case-002's document used a `経(本) N` printed-label convention specific to its own 経済産業本省 section; whether MIC's `010 総務本省` section uses an analogous or different convention has not been checked, and is not needed to make PDF-index ordering executable).
- **Continuation rows**: if a row's amount triple visually continues onto a subsequent printed line that is not itself a new structural row (i.e. still part of the same wrapped label per ME3), it is treated as one row anchored at its first identifying line, per the same convention already used for case-001/002.
- **Repeated headers / organizational or item-level subtotal lines**: excluded from eligibility entirely by ME2 (no expense-level code), so they cannot participate in the tie-break regardless of position.
- **Page-spanning semantic rows**: excluded from eligibility entirely by ME5, not selected and then patched from an adjacent page.
- **Positional ordering for ties on the same page**: top-to-bottom reading order, matching case-002's convention exactly.

## Future page/row locator convention

Once a row is selected in a future task, it must be recorded using the same convention as case-001/case-002's `ground-truth.json`/selection records: `pdfPageIndex` (0-based, authoritative), `pdfPageNumber` (1-based, for human reference), `printedPageLabel` (the document's own printed label, recorded but not used for ordering, per the unknown noted above), plus the row's own item/expense code as the minimum unique identifier — mirroring `fixtures/document-understanding/case-002/20260926_0852_Case002_Selection_Record.md`'s "Selected location" section shape.

## Accidental-exposure policy

If, during the future task that applies this protocol, a candidate row's specific value (name, code, amount, sign, or annotation content) is observed incidentally before eligibility/tie-break determination is complete, that exposure must be recorded explicitly in that task's own selection record (what was seen, when, and why it was unavoidable), and **must not** be used to alter ME1–ME5, the non-criteria list, or the tie-break rule after the fact. No such exposure occurred in this task: no candidate row within pages 5–245 was inspected.

## Stop condition

This task stops here. It does not enumerate candidate rows, does not select a row, does not create `ground-truth.json`, and does not run any document-understanding engine or `npm run docbench` against MIC. The next task that applies this protocol must perform eligible-row enumeration by direct visual inspection only (rendering pages 5–245 and reading them as a human would), exactly as case-002's protocol required for METI, and must record the same contamination controls (no `pdfjs-baseline`/`pymupdf-baseline`/`docling`/MinerU/PaddleOCR/`npm run docbench` run before the row is frozen).
