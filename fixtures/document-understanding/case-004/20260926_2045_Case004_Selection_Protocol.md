# case-004 Selection Protocol (Preregistration) — MEXT (文部科学省) FY2024 Detailed Expenditure Request

Status: **frozen protocol. Row NOT yet selected. No Ground Truth. No benchmark engine run against MEXT. No candidate row enumerated or inspected.**

Date: 2026-09-26 (Asia/Tokyo)

This document defines, in advance of examining any specific candidate row, how the case-004 target row will eventually be selected from the already-locked MEXT detail-table source. It is committed before any row is identified so the choice cannot be influenced — consciously or not — by knowledge of how any engine performs, by any parser-failure pattern, by desired difficulty, or by similarity/difference to case-002/case-003. Actual row selection is a **separate, later task** that applies this protocol; this task does not perform it.

## 1. Purpose and freeze statement

> Which row should become the single case-004 target, chosen from a source-defined MEXT universe without using Ground Truth, benchmark-engine behavior, known parser weaknesses, or desired difficulty?

This protocol freezes, in order: source identity → relationship to the source survey → critique of prior criteria → selection universe → standalone-detail packaging treatment → eligibility criteria → non-criteria → deterministic tie-break → continuation/page-boundary handling → contamination controls → permitted inspection method → accidental-exposure disclosure → unresolved questions → stop condition.

Similarity to case-002/case-003's own first-eligible row (`①01-95 [ministry]一般行政に必要な経費`) is explicitly **not a disqualifier**. If the deterministic rule below naturally selects such a row, that is acceptable; it was neither sought nor avoided in writing this protocol.

## 2. Source identity and locked SHA-256

- `sourceId`: `mext-fy2024-general-account-expenditure-request-detail`
- Title: 第2表　概算要求額明細表（令和6年度歳出予算概算要求書）(FY2024 general-account expenditure request, detail table)
- Official PDF: `https://www.mext.go.jp/content/20230914-mxt_kaikesou01-000031817_03.pdf`
- SHA-256 (re-verified against `sources/source-lock.json` immediately before writing this protocol, and independently against the local raw file via `shasum -a 256`, both matching, unchanged since the case-004 source survey): `6df221dfd22c48e0f32dd59bcf2dbcbaad19720083be43005ce700b984a6bf71`
- Size: 2,665,714 bytes; 1,339 pages; A4 landscape (842×595pt); encrypted (owner-password, permission-only, AES-256, print:yes copy:yes change:no addNotes:no — confirmed not to block `pdftoppm`/`pdfinfo`); no recorded PDF `Producer` field.
- This protocol does not re-lock, re-acquire, or otherwise modify the source. Verified via `git status`/`git diff` immediately before this task's first edit: the working tree was clean at `d4449dd`, `sources/source-lock.json` and `sources/raw/` unchanged.

## 3. Relationship to the source survey

Established source-of-truth for all structural facts below: `fixtures/document-understanding/case-004/20260926_2029_Case004_MEXT_Source_Survey.md` (the source survey), specifically its packaging inventory, its transcription of `_01.pdf`'s (cover/TOC file) own table of contents, and its page-1 rasterization of `_03.pdf` (the target detail file). **No new PDF inspection was performed in this task** — every structural fact cited below was already established and already committed before this task began.

## 4. Critique of case-002/case-003 criteria

Starting from case-002's E1–E5 (`fixtures/document-understanding/case-002/20260926_0834_Case002_Selection_Protocol.md`) and case-003's ME1–ME5 (`fixtures/document-understanding/case-003/20260926_1548_Case003_Selection_Protocol.md`) as precedents, each is re-evaluated individually for MEXT:

| Concept (case-002 E# / case-003 ME#) | Classification for MEXT | Disposition |
|---|---|---|
| E1/ME1 — row belongs to 明細表, not 総表/定員表 | Was a row-level eligibility test for METI/MIC, because their 明細表 is embedded mid-document, after 総表, within one combined file | **Reclassified from row-level eligibility to a source/universe precondition.** MEXT's locked source (`..._03.pdf`) *is already*, in its entirety, `第2表　概算要求額明細表` — confirmed structurally by the source survey (its own page 1 begins immediately with 明細表 content; no 総表 or cover material exists inside this specific file). There is no row within this file that could fail this test; testing it per-row would be vacuous. See §6 below for the explicit reasoning. |
| E2/ME2 — native item/expense-level code, not a bare subtotal/header row | Document-family-independent | **Retained** unchanged in substance. The survey's page-1 rasterization already showed the same column position and the same convention (a `組織`-level total row, `010 文部科学本省`, itself lacking a code) as case-002/003's own organization/item-aggregate rows that were rejected at the same stage; the sibling TOC's `①01-95` listing corroborates the same `NN-NN`-style code format exists somewhere within organization `010`. |
| E3/ME3 — multi-line wrap required | Requires explicit re-justification per the task's own caution | **Retained, same justification as case-003's ME3**: no engine has been run against MEXT, so there is no known MEXT-specific failure mode this could be selecting for or against. Its function remains capability-comparability (testing the same deterministic multi-line label-reconstruction capability already exercised in case-001/002/003), not difficulty-engineering. If no row in the frozen universe satisfies it, that must be reported honestly, not quietly dropped. |
| E4/ME4 — standard amount triple | Document-family-independent | **Retained** unchanged. The survey's page-1 rasterization already confirmed the identical three-column relationship (前年度予算額 / 6年度概算要求額 / 対前年度比較増△減) in the same column positions as case-001/002/003. |
| E5/ME5 — sufficiency (not split across a page boundary) | Document-family-independent | **Retained** unchanged. |
| Non-criterion: `△` glyph presence/absence | Document-family-independent | **Retained.** The survey's incidental page-1 exposure (an organization-aggregate row, `△265,028,183`) already confirms the glyph convention exists somewhere in this document, but says nothing about any future candidate row's own sign — that remains unknown by design and must stay unknown until Ground Truth. |
| Non-criterion: hierarchy ambiguity | Document-family-independent | **Retained.** Unknown for MEXT; must not be engineered toward or away from. |
| Circularity-avoidance (visual-inspection-only enumeration, no compared engine) | Document-family-independent — the single most important constraint, per both prior protocols' own framing | **Retained in full**, and, per case-003's extension, applied to the universe decision itself (§5), not just the eventual row enumeration. |
| Tie-break: earliest eligible row in document order | Document-family-independent *concept*; case-003 needed an explicit universe decision first because of MIC's internal segmentation | **Retained as the underlying philosophy**; MEXT also needs an explicit universe decision (§5), for the same reason as MIC — internal `組織` segmentation exists and spans a range at least as large. |

**No concept was rejected outright.** One (E1/ME1) is reclassified in scope — from a row-level test to a source-level precondition — because MEXT's packaging makes it structurally impossible for any row inside this specific locked file to fail it; the substance of the distinction (明細表 vs. 総表/定員表) is preserved, just moved to where it is actually decided (source/file selection, already made in the survey) rather than re-tested per row.

## 5. Frozen selection universe

MEXT's locked file is 1,339 pages and, per its sibling `_01.pdf`'s own table of contents (already transcribed in the source survey, not re-inspected in this task), is itself subdivided by internal organization (`組織`), of which at least two are known:

| 組織 code | Organization | Printed page (per `_01.pdf`'s TOC) | Approx. `pdfPageIndex` within `_03.pdf` (0-based; printed page 9 = `pdfPageIndex` 0) |
|---|---|---|---|
| 010 | 文部科学本省 (MEXT's own ministry headquarters) | starts at 9 | starts at 0 |
| 020 | 文部科学本省所轄機関 (affiliated institutions) | starts around 904–905 (survey records this as approximate, not pinned to a single page) | starts around 895–896 |

**Three candidate universes were compared before any row was inspected:**

- **(A) Entire 1,339-page detail PDF.** Strongest document-wide determinism (a single "earliest eligible row" rule over the whole file, no organization-choice judgment call). **Rejected**, for the same reason case-003 rejected its analogous option A: organization `020` (文部科学本省所轄機関, affiliated institutions) and any further organizations beyond it are structurally distinct bodies from the ministry's own headquarters, and nothing is currently known about whether their internal budget-line conventions, code formats, or table layout match `010`'s. Selecting from across the whole file without first confirming layout homogeneity risks silently mixing document sub-families under one case (the same ADR-010 layer-conflation concern already raised for case-003).
- **(B) First source-defined organizational section: `010 文部科学本省`.** **Selected.** Justification, from source structure alone: (1) it is explicitly demarcated by the sibling file's own table of contents — not a convenience boundary invented for this protocol; (2) it is the first organizational section in document order, consistent with the "earliest in document order" philosophy that already governs the tie-break within a page; (3) it is the ministry's own headquarters operating-budget section, the structurally closest analog to case-002's `010 経済産業本省` and case-003's `010 総務本省` — both of which were themselves the *first* organization in their own documents' internal segmentation, kept as the case's universe over any external-bureau/affiliated-institution section. Restricting MEXT's universe to its own `010` keeps the cross-case comparison "ministry headquarters vs. ministry headquarters, vs. ministry headquarters," not diluted by a fourth, structurally different comparison point.
- **(C) Another source-defined universe (e.g. organization `020` or later).** Not adopted: nothing in the TOC or generic page structure singles out any later organization as more appropriate than the first, and no TOC/structural justification stronger than (B) exists for any alternative.

**Frozen selection universe: organization `010　文部科学本省`, `_03.pdf`'s own PDF pages 1 through the page immediately preceding organization `020`'s start** — approximately `pdfPageIndex` 0–894 (printed pages 9–903), per the source survey's own TOC transcription.

The exact upper boundary is recorded as **approximate** here, matching the source survey's own hedge ("around printed page 904/905," not pinned to a single page). Per this task's own instructions (§4/point 4 of the originating task), pinning the exact last page of organization `010` — by reading the section-heading text on the one or two candidate boundary pages, not any row's content — is explicitly permitted as **necessary structural navigation** for the future task that applies this protocol, and is deferred to that task rather than performed here (this task performs no new PDF inspection at all, per §3).

If no row within organization `010` satisfies every eligibility criterion below (considered unlikely given ~895 pages of ledger content, but not ruled out), the correct response in the future selection task is to report that honestly and treat widening the universe as a new, separately justified decision — not an automatic fallback to organization `020` or beyond.

## 6. Standalone-detail packaging treatment

MEXT's locked source is **not** packaged the same way as METI's or MIC's. Both prior cases locked one combined PDF containing 総表, 明細表, and 定員表 together, so "is this row inside 明細表, not 総表/定員表" was a genuine, non-trivial row-level (or at least page-range-level) eligibility test (case-002's E1, case-003's ME1). MEXT's locked source is already, and only, `第2表　概算要求額明細表` — a standalone file. 総表 and 定員表 exist as separate sibling files (`_02.pdf`, `_04.pdf`) that were never locked as this case's source and are irrelevant to it.

Consequently: **"correct table" is not retained as a row-level eligibility criterion for case-004.** It is instead already satisfied, permanently and for the entire locked file, by the source-selection decision itself — made in the source survey (choosing `_03.pdf` over its siblings) — and is recorded here as a **frozen source/universe precondition**, not re-tested per candidate row. Every row anywhere in the frozen universe (§5) automatically satisfies this precondition; none needs to be individually checked against it.

This is recorded because it may later become a source-safe Document Profile feature (e.g. "detail table packaged as a standalone file vs. embedded in a combined document"), consistent with the observation already logged in the source survey's "Representation observations" section. No Document Profile schema change is made in this task.

## 7. Final eligibility criteria

A row is **eligible** for case-004 if and only if all of the following hold, evaluated purely from the page's own visual structure within the frozen universe (organization `010　文部科学本省`, §5):

- **MX1 — Native item/expense-level code.** The row carries an explicit item or expense-level code in the document's own numbering scheme (structurally analogous to case-001/002/003's `NNN`/`NN-NN`-shaped codes, or the `01-95`-style format already named in the sibling TOC), not a bare organizational/item-level subtotal or a header-only row with no code.
  - *PASS*: a code in this format is visually printed in the row's own code column.
  - *FAIL*: the row is an organization-level (`組織`) or item-level (`項`) aggregate/header row with no such code — e.g. the `010 文部科学本省` row already incidentally seen on page 1, which the source survey confirms carries no code.
  - *Visual determination*: read the printed code text in the row's code column directly from the rendered page.
  - *Continuation rows*: a row whose code is printed once but whose label/amount visually continues onto a later line remains one MX1-eligible row (its code does not need to repeat on every wrapped line).
- **MX2 — Multi-line wrap.** The row's item name and/or expense name visually wraps across two or more printed lines, exercising the same multi-line cell-reconstruction capability tested in case-001/002/003 (kept for capability-comparability, per §4's re-justification, not difficulty-engineering).
  - *PASS*: the label visually occupies two or more printed lines within the row's own cell.
  - *FAIL*: the label fits on a single printed line.
  - *Visual determination*: count printed lines occupied by the label text in the rendered page.
- **MX3 — Standard amount triple.** The row carries the document's standard three-column previous-budget / current-year-request / delta relationship in its native layout, structurally analogous to case-001/002/003, so the same benchmark fields remain meaningful and comparable.
  - *PASS*: all three amount columns (前年度予算額 / 6年度概算要求額 / 対前年度比較増△減) are visually present and associated with this row.
  - *FAIL*: one or more of the three is visually absent or unassociated with this specific row.
  - *Visual determination*: read the three amount columns in the rendered page directly.
- **MX4 — Sufficiency.** The row is complete enough to populate every case-001/002/003-schema field expected to be recoverable from the page itself — i.e. not a row whose amount triple is split across a page boundary or otherwise physically unrecoverable from a single page.
  - *PASS*: the complete row (code, label, all three amounts) is visually present on one page (or, for a continuation label per MX2, wholly resolvable from the label's own start page plus its immediate visual continuation, without needing a different row's data).
  - *FAIL*: any required field is printed only on a different, non-continuation page.
  - *Visual determination*: confirm all required fields appear within one coherent visual unit (a single page, or a label's own wrap onto the immediately following printed line within the same physical row block).
  - *Continuation/page-spanning handling*: if a row's amount triple is visually split across a page boundary (e.g. code+label on one page, amounts starting the next), the row FAILS MX4 and is excluded from the tie-break entirely — not selected and then patched from an adjacent page.

MX1/MX2/MX3/MX4 correspond respectively to case-003's ME2/ME3/ME4/ME5 (case-003's ME1, "correct table," is the one criterion removed here per §6, since it is already a source-level precondition for this file, not a row-level test).

## 8. Explicit non-criteria

The following must **not** influence eligibility, tie-break, or universe selection, now or in the future selection task:

- Presence or absence of the `△` (decrease) glyph on the specific candidate row's own delta.
- Whether the candidate row's delta is positive or negative.
- Whether the row's page also exhibits header-row hierarchy ambiguity (multiple structurally-similar candidate rows).
- Placement or population of the 備考 (remarks/annotation) column relative to the amount triple — the same feature that broke `common.mjs`'s trailing-triple regex on case-002; selecting for or against it on MEXT would make case-004 a targeted regression test rather than a genuine out-of-sample generalization test.
- Any prediction, expectation, or hope about how `pdfjs-baseline`, `pymupdf-baseline`, or `docling` will perform on the row.
- Docling's table-grid density/geometry on the candidate page.
- Compatibility of the row's page with any engine given the document's permission-only AES-256 encryption. Encryption is a document/source property, established once for the entire locked file, not a row property, and must not be probed per-candidate or per-page by running any engine before the row is frozen (see §9).
- The row's PDF `Producer`/toolchain metadata (already known to be absent for this specific file, document-wide, per the survey — not a per-row fact and not a selection input regardless).
- Similarity or difference to case-002's or case-003's own selected row (explicitly permitted either way, per §1).
- Expected benchmark score, perceived difficulty, or convenience of transcription.
- Whether a candidate row would confirm or falsify any hypothesis formed from case-001/002/003 (e.g. whether the CJK-spacing strategy, the annotation-contamination issue, or Docling's grid-misalignment pattern would recur) — those remain observations to make *after* the row is frozen and Ground Truth exists, never selection inputs.
- Proximity to the universe's page-range boundary beyond what the deterministic tie-break itself produces.

## 9. Deterministic tie-break

If more than one row within the frozen universe (organization `010　文部科学本省`, §5) satisfies MX1–MX4, the tie-break is:

> **The earliest eligible row in document order within the frozen universe** — lowest `pdfPageIndex` (0-based, this repository's authoritative convention) within `_03.pdf`, then topmost eligible row position on that page (top-to-bottom reading order).

Explicit handling:

- **PDF index vs. printed page number**: `pdfPageIndex` (0-based) is the authoritative ordering key, not the document's own printed page label (`文（本） N`). This mirrors case-002/003's own convention. It is not currently known whether MEXT's printed-label convention is stable throughout organization `010`'s ~895 pages (only page 1, printed "9", has been observed) — this is not needed to make `pdfPageIndex` ordering executable.
- **Repeated headers / organization- or item-level aggregate rows**: excluded from eligibility entirely by MX1 (no code), so they cannot participate in the tie-break regardless of position — this is exactly what already happened, incidentally, to the one row already visually exposed (§12).
- **Rows beginning on a prior page / continuing onto a later page**: per MX4, a row whose amount triple is split across a page boundary FAILS and is excluded from the tie-break. A row whose label (not its amount triple) wraps onto an immediately-following printed line within the same visual row block is not "page-spanning" in this sense — it is the MX2 multi-line-wrap case, anchored at its first identifying line, per the same convention already used in case-001/002/003.
- **Multiple qualifying rows on one page**: resolved by top-to-bottom reading order on that page, matching case-002/003's convention exactly.

## 10. Contamination controls

The workspace, and this task, retain full knowledge of case-001/002/003's prior findings (parser failure modes, glyph conventions, hierarchy ambiguity, etc.). No unrealistic claim is made that this memory has been erased. The methodological control is instead:

- These rules (§7–§9) are frozen **before** any candidate row within organization `010` is inspected.
- The universe (§5) is defined from source-provided TOC boundaries, not from any row's content.
- No benchmark output or engine behavior for MEXT is consulted (none exists — confirmed in §1 of this task's own verification, see final report).
- No Ground Truth for MEXT exists or is consulted.
- No criterion is chosen because it is known, from case-001/002/003, to produce or avoid a specific failure mode on MEXT specifically — MX1–MX4 test the same document-understanding capabilities case-001/002/003 tested, not MEXT-specific known weaknesses (none are known, since no engine has run against MEXT).
- Provenance and chronology (this protocol's own commit, preceding any future selection-record commit) are preserved as the audit trail proving the freeze order.

Prior-case experience informs *what the protocol checks* (the same categories of criteria and non-criteria already validated as meaningful across two prior ministries), exactly as an experienced analyst accumulates methodology from a real workspace. It does not determine *which value* the future selection produces.

## 11. Permitted inspection method for the future selection task

Once this protocol is applied, eligible-row enumeration within organization `010` must be performed by **direct visual inspection of the rendered PDF pages** (viewing rasterized pages as a human would), not by running any text-extraction or document-understanding tool — the same method already used for case-001/002/003's own selections. `pdfinfo`/`pdftoppm` (poppler) remain acceptable for narrow structural purposes (page count, boundary-page heading text, confirming the document renders despite encryption) precisely because they perform no text/layout reconstruction and are not one of the three compared engines. Running `pdfjs-baseline`, `pymupdf-baseline`, `docling`, `npm run docbench`, MinerU, PaddleOCR, or any OCR/LLM/vision-based extraction against any candidate row before the row is frozen constitutes a protocol violation, for the same circularity reason already established in case-002/003's protocols.

Direct rasterization of pages for the future visual-selection task is expected and permitted; this task itself performs none.

## 12. Accidental-exposure disclosure

The source survey (`fixtures/document-understanding/case-004/20260926_2029_Case004_MEXT_Source_Survey.md`) already disclosed one such exposure, carried forward here for completeness: rasterizing `_03.pdf`'s own page 1 (a necessary structural check — the file's own first page, not chosen for row-eligibility reasons) incidentally showed the `010 文部科学本省` organization-total row's own amounts (`5,149,805,046` / `4,884,776,863` / `△265,028,183`). This is an **organization-level aggregate row**, which fails MX1 outright (no expense-level code) and is therefore ineligible regardless; it was not, and must not be, used to influence universe selection, MX1–MX4, the non-criteria, or the tie-break. **No exposure of any eligible (coded) candidate row occurred in this task or in the prior survey.**

No new PDF inspection was performed in this task (per §3); accordingly, no new exposure occurred here.

## 13. Unresolved questions

- The exact `pdfPageIndex`/printed-page boundary where organization `010` ends and `020` begins is known only approximately (survey: "around printed page 904/905"). Pinning it exactly requires reading the section-heading text on one or two boundary pages — permitted, per §5, as necessary structural navigation in the future selection task, not performed here.
- Whether MEXT's printed-page-label convention (`文（本） N`) remains stable throughout organization `010`'s ~895 pages is unknown (only page 1 has been observed); this does not block the tie-break, which uses `pdfPageIndex`, not the printed label.
- Whether the native `NN-NN`-style expense-code convention named in the sibling TOC (`01-95`) is used uniformly throughout organization `010`, or varies internally, is unknown beyond that one TOC-listed example.
- Whether the document's permission-only AES-256 encryption affects rasterization uniformly across all ~895 pages of organization `010` (only page 1 has been rendered and confirmed unaffected) is unknown; if a future page fails to rasterize for reasons connected to encryption, that must be reported as a blocking source-access issue, per the originating task's own instruction, rather than silently changing the universe.

## 14. Stop condition

This task stops here. It does not enumerate candidate rows, does not select a row, does not create `ground-truth.json`, and does not run any document-understanding engine, OCR tool, or `npm run docbench` against MEXT. The next task that applies this protocol must perform eligible-row enumeration within organization `010` (§5) by direct visual inspection only (§11), record the selected row and any accidental exposure in a new selection-record artifact, and stop **before Ground Truth** — exactly mirroring case-002/003's own two-step selection-then-Ground-Truth sequencing.
