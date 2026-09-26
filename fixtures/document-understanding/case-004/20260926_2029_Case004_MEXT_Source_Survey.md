# case-004 — MEXT (文部科学省) FY2024 Source Survey and Acquisition

Status: **source survey only. No row selected. No Ground Truth. No benchmark engine run against MEXT.**

Date: 2026-09-26 (Asia/Tokyo)

Branch: `research/case-004-mext-preregistration`, created from `main` at `3b29ebd` (the merged case-003/CJK-normalization checkpoint, PR #3).

This document uses the same evidence discipline as the case-003 survey: **[FACT]** (independently verified against an official source or a locally-computed value), **[OBSERVATION]** (noticed, not yet interpreted), **[INTERPRETATION]** (a conclusion drawn from facts/observations), **[RECOMMENDATION]** (a proposal, never a frozen selection).

## Research question

> What is the authoritative MEXT FY2024 general-account expenditure budget-request source suitable for row-level document-understanding research, and how is it packaged relative to case-002 (METI) and case-003 (MIC)?

The preliminary hypothesis — that MEXT publishes its detailed 第2表 概算要求額明細表 as a separate PDF rather than as part of one combined document — is treated as a hypothesis to verify, not a fact to copy blindly.

## Official MEXT landing page

- **[FACT]** `https://www.mext.go.jp/a_menu/yosan/r01/1420955_00005.htm` — page title "令和6年度　概算要求書" (confirmed via `<title>` and `<h1>`). Structured under two top-level headings, `[一般会計]` (general account) and `[特別会計]` (special accounts).
- **[FACT]** Under `[一般会計]`, the sub-heading "令和6年度　歳出予算概算要求書" (FY2024 expenditure budget request document) lists **four separate PDF files**, not one combined document:

| File | Title (as linked) | Size |
|---|---|---|
| `..._01.pdf` | 表紙・目次 (cover/table of contents) | 15KB |
| `..._02.pdf` | 第1表　概算要求額総表 (summary table) | 44KB |
| `..._03.pdf` | 第2表　概算要求額明細表 (**detail table**) | 2,604KB |
| `..._04.pdf` | 第3表　概算要求定員表 (staffing table) | 147KB |

A separate sub-heading, "令和6年度　一般会計歳入予算概算見積書" (revenue-side estimate), similarly splits into 4 files (`_05`–`_07`, `_10`). Under `[特別会計]`, エネルギー対策特別会計 (Energy Measures Special Account) has its own combined, much smaller 歳出概算要求書 (`_08.pdf`, 58KB) and 歳入概算見積書 (`_09.pdf`, 14KB).

**This confirms the preliminary hypothesis precisely**: MEXT's general-account expenditure request is packaged as four independent PDFs by table type, unlike METI/MIC's single combined document containing 総表+明細表+定員表 together.

## MOF cross-reference

- **[FACT]** MOF's official FY2024 general-account request link table (`https://www.mof.go.jp/policy/budget/budger_workflow/budget/fy2024/2024yokyuippan_link.html`, the same table already used for the case-002/case-003 surveys): the 文部科学省 row's 歳入/歳出 columns both link to `https://www.mext.go.jp/a_menu/yosan/r01/1420672_00009.htm`.
- **[FACT]** That page (MEXT's own "令和6年度予算" top page) mixes, under one page, multiple budget-lifecycle stages exactly as MIC's own top page did: 補正予算 (supplementary budget), 予備費 (reserve fund use), 予算 (enacted budget, with its own 各局課別/各目明細書 sub-links), and a "概算要求" (budget request) section that itself links to `https://www.mext.go.jp/a_menu/yosan/r01/1420955_00005.htm` — the exact same page found via direct search.
- **[INTERPRETATION]** Two independent routes (direct MEXT search, and MOF → MEXT's budget top page → MEXT's request page) converge on the identical `1420955_00005.htm` page, corroborating it as the authoritative source for FY2024 request-stage materials. **[OBSERVATION]** This is the second ministry (after MIC) whose own top budget page mixes request-stage and enacted-budget-stage materials under one heading — reinforcing that this is a general cross-ministry hazard, not MIC-specific, consistent with `protocol/RESEARCH_PROTOCOL.md`'s lifecycle-separation invariant.

## Official source inventory

| # | Title | URL | Stage | Role | Size | Acquired |
|---|---|---|---|---|---|---|
| 1 | 表紙・目次 | `..._01.pdf` | request | Cover/TOC for the 4-file expenditure-request set | 15,427B (independently confirmed) | Hashed only, not locked |
| 2 | 第1表 概算要求額総表 | `..._02.pdf` | request | Summary/total table | 44,755B | Hashed only, not locked |
| 3 | **第2表 概算要求額明細表** | `..._03.pdf` | request | **Detail table — selected source** | 2,665,714B | **Locked** |
| 4 | 第3表 概算要求定員表 | `..._04.pdf` | request | Staffing table | 149,937B | Hashed only, not locked |
| 5 | 令和6年度一般会計歳入予算概算見積書 (4 files, `_05`/`_06`/`_07`/`_10`) | — | request | Revenue-side estimate, general account | not individually verified | Not acquired |
| 6 | エネルギー対策特別会計 歳出概算要求書/歳入概算見積書 (`_08`/`_09`) | — | request | Special account | not individually verified | Not acquired |

Consistent with the case-003 survey's discipline, only the detailed candidate was locked; the sibling files were downloaded to a temporary, non-repository location purely for hashing/`pdfinfo` comparison, not committed as locked sources, per the instruction not to mass-acquire unrelated materials.

## Summary-vs-detail classification

- **[FACT]** `pdfinfo` on `_02.pdf` (総表): not deeply inspected beyond file size (44,755 bytes — far smaller than `_03.pdf`'s 2.6MB), consistent with a page-count-limited summary table (per the TOC, 総表 spans printed pages 1–8, matching case-003's own 総表 page-count pattern).
- **[FACT]** `pdfinfo` on `_03.pdf` (明細表): **1,339 pages**, A4 landscape (842×595pt), `Encrypted: yes (print:yes copy:yes change:no addNotes:no, algorithm:AES-256)`, no `Producer` field recorded, `Form: AcroForm`.
- **[FACT]** Rasterizing `_03.pdf` page 1 (400dpi-equivalent, `pdftoppm`) shows: printed label "文（本） 9", title "令和6年度歳出概算要求額明細表", organization header "24 文部科学省所管", and the full column-header row: 要求番号 (request number) | 事項 (item, with codes) | 前年度予算額 (previous budget) | 6年度概算要求額 (FY2024 request) | 対前前年度比較増△減 (delta, `△` glyph visible in the one row shown) | 備考 (remarks) — the identical column set already established for case-001/002/003. The first content row visible is `010 文部科学本省` (組織-level total), with delta shown as `△265,028,183` (a genuine `△`-marked decrease, at the aggregate level — not a target-row observation).
- **[FACT]** `_03.pdf`'s own PDF page 1 begins **immediately** with 明細表 content — no cover page, no embedded TOC, no 総表 within this file. This confirms the packaging split is genuine and structural, not merely a naming convenience: the front matter and summary table that METI/MIC embed as the first several pages of one combined file are, for MEXT, entirely contained in the separate `_01.pdf`/`_02.pdf` files.
- **[FACT]** `_01.pdf` (cover/TOC, 6 pages) contains the document-wide coarse TOC (page 3 of that file, printed page "1"): `令和6年度歳出概算要求額総表` → page 1; `令和6年度歳出概算要求額明細表` → page 9; `(組織) 010 文部科学本省` → page 9; `(項) 010 文部科学本省共通費` → page 10; `①01-95 文部科学本省一般行政に必要な経費` → page 11; further items continuing (`②11-95 審議会等に必要な経費` → page 63; `③16-95 国際会議に必要な経費` → page 126; ...). A later detailed-TOC page (page 4 of `_01.pdf`) shows organization `(組織) 020 文部科学本省所轄機関` beginning around printed page 904/905 — confirming multiple internal `組織` sections exist, similar in kind to MIC's structure, spanning a page range at least as large (1,339 total pages vs. MIC's 454).
- **[INTERPRETATION]** `_03.pdf` is confirmed to be the genuine, row-level detail table (明細表), not a summary — its own first page already shows the full standard column structure, and the TOC (in the sibling file) confirms the same `①01-95 [ministry]一般行政に必要な経費`-shaped first expense row under organization `010`'s first item header, structurally identical in template position to case-002's and case-003's own target rows.

## Selected source for future case-004 work

- **sourceId**: `mext-fy2024-general-account-expenditure-request-detail`
- **Title**: 第2表　概算要求額明細表 (part of 令和6年度歳出予算概算要求書)
- **Official landing page**: `https://www.mext.go.jp/a_menu/yosan/r01/1420955_00005.htm`
- **Official PDF URL**: `https://www.mext.go.jp/content/20230914-mxt_kaikesou01-000031817_03.pdf`
- **Lifecycle/account/type**: request-stage, general account, expenditure detail table
- **Local raw path**: `sources/raw/mext-fy2024-general-account-expenditure-request-detail.pdf` (git-ignored, not committed)
- **Byte size**: 2,665,714 bytes
- **SHA-256**: `6df221dfd22c48e0f32dd59bcf2dbcbaad19720083be43005ce700b984a6bf71`
- **Page count**: 1,339

## Acquisition

- **[FACT]** Plain, unauthenticated `curl`/`fetch()` succeeded on the first attempt for all four `_01`–`_04` files (HTTP 200, `content-type: application/pdf`) — **no WAF/JS challenge observed on `mext.go.jp`**. Per the task's instruction, Playwright/`scripts/source-acquisition/browser-fetch` was therefore **not used**.
- **[FACT]** `scripts/source-acquisition/src/acquire.mjs` was not used to perform this lock, for the same reason documented in the case-003 survey: its `lock` command is coupled to `scripts/request-ingestion/source_manifest.json`, a manifest belonging to an unrelated subsystem, not a generic single-URL entry point.
- **[FACT]** Acquisition and locking were performed with a small, uncommitted scratch script that does a plain `fetch()` and then calls the shared, already-reviewed `applyAcquisition()`/`decideLockAction()` functions exported from `scripts/source-acquisition/src/lock-policy.mjs` — the same shared immutable-lock module both `acquire.mjs` and `browser-fetch.mjs` now use, reusing it exactly rather than duplicating or bypassing it.
- **[FACT]** `mext-fy2024-general-account-expenditure-request-detail` was locked (SHA-256 above, `acquisitionMethod: "plain-fetch"`). **Immutability re-verified**: re-running the identical acquisition immediately afterward returned `IDENTICAL`, with the lock entry and raw file confirmed unchanged.
- **[FACT]** The other three general-account files (`_01`, `_02`, `_04`) and the special-account/revenue-side files were downloaded only to a temporary, non-repository location for hashing/`pdfinfo`, per the instruction not to mass-acquire unrelated materials — not persisted in `sources/source-lock.json`.
- `sources/source-registry.csv` was updated with one new row for the locked source, following the exact column convention of the existing four rows.

## Source-safe structural observations

- **[FACT]** The detail table begins **immediately** at PDF page 1 of `_03.pdf` — there is no front matter to skip within this specific file (unlike METI/MIC, where the combined file's 明細表 starts several pages after a cover/TOC/総表 preamble). The equivalent front matter (cover, TOC, 総表) exists but lives entirely in the separate `_01.pdf`/`_02.pdf` files.
- **[FACT]** Major organization boundaries, per the sibling TOC file: `(組織) 010 文部科学本省` starts at printed page 9 (= `_03.pdf`'s own PDF page 1); a second organization, `(組織) 020 文部科学本省所轄機関`, begins around printed page 904/905 — meaning organization `010` alone spans roughly 895 pages within this 1,339-page file, with further organizations beyond `020` not yet enumerated.
- **[FACT]** Page orientation: A4 landscape (842×595pt), matching case-002/003.
- **[FACT]** A page-level unit label, `(単位: 千円)`, is visibly part of the table format on the one page inspected (page 1) — consistent with case-002/003's convention, though (per the same protocol already applied to those cases) this is confirmed only for this specific page, not generalized to the other 1,338 pages.
- **[FACT]** Major column headers, visible on page 1: 要求番号 (request number) | 事項 (item, with native codes) | 前年度予算額 (previous budget) | 6年度概算要求額 (FY2024 request) | 対前年度比較増△減 (delta, `△` convention confirmed present on this page's aggregate row) | 備考 (remarks) — request-number, item-code, and previous/current/delta numeric columns are all confirmed to exist structurally, matching case-001/002/003.
- **[FACT]** Whether a native `目`-level expense code column (analogous to case-002/003's `NN-NN` format) exists cannot be confirmed from page 1 alone, since the only row visible there is the `組織`-level aggregate (`010 文部科学本省`), which — consistent with case-002/003's own pattern — carries no expense code. The sibling TOC file's own listing (`①01-95 文部科学本省一般行政に必要な経費`) strongly suggests the same `01-95`-style expense-code convention is used, but this was read from the **TOC**, not from inspecting the target page's own row content, and is recorded here as a document-wide-convention indicator, not as row-level candidate inspection.
- **[FACT]** A `備考` (remarks) column header exists in the table format (visible on page 1), but whether it is populated, and for which rows, was not inspected beyond the one aggregate row on page 1 (which shows no remarks text).
- **[OBSERVATION]** `_03.pdf` (明細表) shows no `Producer` field in its PDF metadata, while sibling files `_01.pdf`/`_02.pdf` (cover/TOC, 総表) show `Producer: List Creator`, and `_04.pdf` (staffing table) shows an entirely different toolchain (`Producer: Acrobat Distiller 22.0 (Windows)`, `Creator: PScript5.dll Version 5.2.2`, achieving its landscape appearance via a `Page rot: 90` flag rather than native landscape page dimensions). **[INTERPRETATION]** MEXT's four-file packaging is **not** uniformly produced by a single toolchain, unlike METI/MIC's single combined file (uniformly "List Creator" throughout) — a genuinely new packaging-heterogeneity finding.
- **[OBSERVATION]** All four general-account expenditure-request files are encrypted with owner-password permission restrictions (`print:yes copy:yes change:no addNotes:no`, AES-256). This did not impede `pdftoppm` rendering or `pdfinfo` metadata reading (permissions restrict editing, not viewing/printing/copying) and is not expected to impede any of the three benchmark engines, but is a genuinely new characteristic — case-001/002/003's sources were all unencrypted.

## Packaging comparison with METI (case-002) / MIC (case-003)

| Property | METI (case-002) | MIC (case-003) | MEXT (case-004 candidate) |
|---|---|---|---|
| Packaging | One combined PDF (総表+明細表+定員表) | One combined PDF (総表+明細表+定員表) | **Four separate PDFs**, one per table |
| 明細表 file's own page 1 | Mid-document (after cover/TOC/総表) | Mid-document (after cover/TOC/総表) | **The file's own PDF page 1** (front matter lives in sibling files) |
| Toolchain uniformity | Uniform ("List Creator" throughout) | Uniform ("List Creator" throughout) | **Heterogeneous** (明細表 has no recorded Producer; staffing table uses a different toolchain entirely) |
| Encryption | Not encrypted | Not encrypted | **Encrypted** (permission-only; viewing/printing/extraction unaffected) |
| Multiple internal `組織` sections | Not confirmed (not investigated beyond the target organization) | Confirmed (5 organizations, 454 total pages) | Confirmed (at least 2 organizations found so far; 1,339 total pages, larger than MIC) |
| Page-level unit label | Present on target page | Present on target page | Present on the one page inspected |
| First-row-under-first-item template pattern (`①01-95 [ministry]一般行政に必要な経費`) | Present | Present | **Present** (per TOC; not yet confirmed via direct row inspection) |

**[INTERPRETATION]** MEXT adds a genuine, useful new packaging variation: splitting one logical document into multiple files by table type. This has direct implications for a future selection protocol's "selection universe" framing (the protocol will need to define the universe in terms of `_03.pdf`'s own page range, without needing to first skip past an embedded 総表/TOC as case-002/003's protocols did) and for a future Document Profile representation (a "single PDF" assumption implicit in the current Case Package schema's `sourceSha256`/`pdfPageIndex` fields would need a documented convention for referring to "which of several sibling files" — not changed in this task, only noted). This is not evidence that MEXT is harder or easier to extract from — packaging and extraction difficulty are explicitly not conflated here, per the task's instruction.

## Suitability assessment

**[RECOMMENDATION]** MEXT is a good case-004 candidate. It provides: an authoritative official source (confirmed via two independently converging routes); genuine request-stage row-level detail (confirmed via TOC and direct page-1 inspection, not assumed); sufficient provenance (title, author, per-file producer/toolchain metadata, page counts, official URLs, SHA-256); and a **meaningful new addition to the corpus** — the first case where the detailed table is packaged as an independently-published file rather than embedded in a larger combined document, with document-wide encryption and toolchain heterogeneity as additional new characteristics. No benchmark semantics need to change before preregistration; the existing Case Package schema and selection-protocol methodology (per case-002/003's precedent) both apply, with the packaging difference noted as a representation observation for a future task, not requiring an immediate schema change. This is a recommendation only — no row, page, or organization sub-section has been chosen.

## Freeze confirmation

- No target row has been selected for case-004.
- No candidate rows were enumerated for eligibility — the `①01-95 文部科学本省一般行政に必要な経費` reference above came from reading the sibling TOC file's own printed listing (a structural/navigational fact, exactly analogous to how case-002/003's own TOCs were read during their surveys), not from inspecting or evaluating the target page's row content for eligibility.
- No `ground-truth.json` exists for case-004.
- No engine (pdf.js/PyMuPDF/Docling/MinerU/PaddleOCR, or `npm run docbench`) has been run against any MEXT document.
- No benchmark/evaluator/normalization semantics were changed.
- No Case Package (`document-profile.json`/`research-history.jsonl`) was created for case-004.
- **Accidental exposure disclosure**: rasterizing `_03.pdf`'s page 1 (a necessary, arbitrary structural page — the file's own first page, not chosen for any row-eligibility reason) incidentally showed the `010 文部科学本省` organization-total row's own amounts (`5,149,805,046` / `4,884,776,863` / `△265,028,183`). This is an **organization-level aggregate**, not any specific future candidate row, and is disclosed here exactly as seen, per the task's instruction to disclose rather than conceal incidental exposure. It was not used to influence source selection (already established from packaging/TOC facts, not from this row's values) and must not be used to influence any future row-selection protocol or tie-break.

## Representation observations (prospective, unconfirmed, not acted on)

- **[OBSERVATION]** The current Case Package schema's `sourceId`/`sourceSha256` fields implicitly assume one case maps to one PDF file. MEXT's genuinely separate-file packaging (明細表 in one file, 総表/TOC/定員表 in siblings) means a future case-004 selection protocol will need an explicit convention for referencing "this specific sibling file" without ambiguity — most likely already satisfied by choosing a sufficiently specific `sourceId` (as done here: `...-detail`, distinguishing it from a hypothetical `...-summary` or `...-staffing` source), but worth flagging as a schema assumption that held only by convention, not by an explicit multi-file-package field, until now.
- **[OBSERVATION]** MEXT's document-wide PDF encryption (permission-restricted, not password-protected) is a genuinely new source characteristic. If any future engine or tool in this pipeline were to rely on document *editing* rather than reading/printing/extracting text, this could matter; for the three currently-compared engines (pdf.js, PyMuPDF, Docling), all of which only read/extract, no impact is expected, but this was not exhaustively tested against all three in this survey (no benchmark engine was run, per the freeze).
- **[OBSERVATION]** Toolchain heterogeneity *within* what MEXT presents as one logical document (four files, at least two different producers) is a new packaging-heterogeneity dimension not previously represented in the Case Package concept, which currently characterizes "the document's producer" as if it were a single fact per case.

## Files changed

- `fixtures/document-understanding/case-004/20260926_2029_Case004_MEXT_Source_Survey.md` (this file, new)
- `sources/source-lock.json` (one new entry: `mext-fy2024-general-account-expenditure-request-detail`)
- `sources/source-registry.csv` (one new row, same source)
- `sources/raw/mext-fy2024-general-account-expenditure-request-detail.pdf` (git-ignored, not committed)
- `state/CURRENT_STATE.json`, `state/TODO.md`, `state/CHANGELOG.md` (state updates)

No case-001/002/003 file, no adapter/normalizer/evaluator, no Ground Truth, and no Case Package schema was modified. No source-acquisition code was modified (no blocking defect was discovered; the existing shared `lock-policy.mjs` worked exactly as intended).

## Validation

```bash
npm run validate      # PASS
npm run sources:test  # PASS (8/8)
git diff --check      # clean
```

Local SHA-256 for the newly-locked MEXT source was independently reproduced twice (once during the initial lock, once during the immutability re-run) and matches the value independently computed via `shasum -a 256` on the temporary comparison copy before locking. `npm run sources:verify` (live network) was not run for this survey task, consistent with the case-003 survey's precedent (not needed to establish local integrity); if run in a future task, METI's known AWS WAF remote-verification limitation should continue to be reported separately from local source integrity, per existing practice.

## Unresolved issues

- Whether MEXT's detail table (`_03.pdf`) is genuinely encryption-unaffected for all three benchmark engines (pdf.js, PyMuPDF, Docling) was not tested — no benchmark engine was run, by design. `pdftoppm`/`pdfinfo` compatibility is confirmed; engine-level compatibility is not.
- The full internal organization list beyond `010 文部科学本省` and `020 文部科学本省所轄機関` was not enumerated — only the first two organization boundaries were read from the sibling TOC file.
- The four revenue-side files (`_05`/`_06`/`_07`/`_10`) and the two special-account files (`_08`/`_09`) were not independently verified beyond their listed sizes on MEXT's landing page.
- Whether a native `目`-level expense-code convention identical to case-002/003's `NN-NN` format is used throughout, or varies by organization, is unknown beyond the single TOC-listed example (`01-95`).
- Whether the `備考` (remarks) column is ever populated with same-line annotation content analogous to case-002's `（要求要旨）` contamination pattern is completely unknown — not investigated, by design (would require row-level inspection).

## Recommended next step

Freeze a case-004 row-selection protocol for `mext-fy2024-general-account-expenditure-request-detail`, modeled on `fixtures/document-understanding/case-003/20260926_1548_Case003_Selection_Protocol.md`'s methodology (critiquing, not copying, its ME1–ME5 criteria; explicitly deciding a selection universe — here, likely `010 文部科学本省`, this file's own pages 1 through the point where `020 文部科学本省所轄機関` begins), before visually selecting any row. Not executed in this task.
