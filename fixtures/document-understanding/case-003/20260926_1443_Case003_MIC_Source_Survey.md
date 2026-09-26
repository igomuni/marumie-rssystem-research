# case-003 — MIC (総務省) FY2024 Source Survey and Acquisition Preregistration

Status: **source survey only. No row selected. No Ground Truth. No benchmark engine run against MIC.**

Date: 2026-09-26 (Asia/Tokyo)

Branch: `research/case-003-mic-preregistration`, created from `main` at `f8e32ef` (the merged case-002/Case Package checkpoint, PR #2).

This document distinguishes four kinds of statement throughout: **[FACT]** (independently verified against an official source or a locally-computed value), **[OBSERVATION]** (something noticed during the survey, not yet interpreted), **[INTERPRETATION]** (a conclusion drawn from facts/observations), and **[RECOMMENDATION]** (a proposal for future work — never a frozen selection).

## Research question

> What official MIC FY2024 budget-request documents exist, what purpose does each document serve, and which source — if any — is structurally suitable as a future case-003 comparable to case-001/case-002?

## Survey method

- Started from official MIC and MOF sites only, per the task's discovery-hints-are-not-facts instruction. Third-party pages were not used.
- MIC's own budget navigation was crawled by direct HTTP fetch of HTML pages (`curl`, no browser/Playwright — no bot-challenge was ever observed on `soumu.go.jp`), extracting `<a href>` targets and their surrounding section headings (`<h1>`/`<h2>`) to attribute each linked document to a specific fiscal year and document category.
- MOF's official cross-ministry link tables were located via `WebSearch` (query restricted to `site:mof.go.jp`) and then fetched directly to read the actual table row for 総務省.
- Basic document identification used only `curl` (HTTP status/headers), PDF magic-byte inspection, `shasum -a 256`, `pdfinfo` (poppler — no text/layout reconstruction), and `pdftoppm` rasterization of two pages (page 1 and one arbitrary interior page) purely to confirm document purpose/layout at a high level. No pdf.js/PyMuPDF/Docling/MinerU/PaddleOCR/document-understanding-benchmark engine was run. No Ground Truth was created or consulted (none exists for case-003).

## Official MIC landing pages found

- **[FACT]** `https://www.soumu.go.jp/menu_yosan/yosan.html` — MIC's top "予算" (Budget) page. Lists budget-related documents for every fiscal year back to 平成23年度, each under its own `<h2>` heading (`id="r6"` for 令和6年度/FY2024, etc.). This single page mixes multiple lifecycle stages (request, enacted/original budget, supplementary budget, reserve-fund-use requests, execution status) under one fiscal-year heading — see "Lifecycle-stage mixing" below.
- **[FACT]** `https://www.soumu.go.jp/menu_yosan/yosan_R06.html` — a dedicated FY2024 sub-page titled "令和6年度概算要求書及び政策評価調書" (FY2024 budget request documents and policy evaluation reports), linked from the `r6` section of `yosan.html`. This page's own breadcrumb and `<h1>` confirm its scope: request-stage documents only, for FY2024 only.

## Official MOF cross-reference

- **[FACT]** MOF's official FY2024 cross-ministry budget-request page: `https://www.mof.go.jp/policy/budget/budger_workflow/budget/fy2024/fy2024.html`, which links to `https://www.mof.go.jp/policy/budget/budger_workflow/budget/fy2024/2024yokyuippan_link.html` — a table titled "概算要求書" (Budget Request Document) with 歳入 (revenue) / 歳出 (expenditure) columns per ministry, plus a `<要望一覧>` (priority-policy list) column.
- **[FACT]** In that table, the 総務省 (MIC) row's **歳入 and 歳出 columns both link to `https://www.soumu.go.jp/menu_yosan/yosan_R06.html`** — independently corroborating the page found via MIC's own navigation.
- **[OBSERVATION]** The same table's `<要望一覧>` column for MIC, and a separate MOF summary-document cross-reference table (`2024gaisangaiyo_link.html`), both link to `https://www.soumu.go.jp/menu_yosan/yosan.html#r5` — the `#r5` anchor corresponds to `令和5年度` (FY2023) on MIC's page, not `#r6`/FY2024. **[INTERPRETATION]** This looks like a stale/uncorrected anchor on MOF's side (an off-by-one-fiscal-year link), not a claim about which document is authoritative — it does not affect the 歳入/歳出 request-document links, which correctly point to the FY2024 page. Not corrected in this task; noted only as an anomaly for a future task to be aware of if it ever relies on that specific link.
- Role in provenance: MOF's page independently confirms MIC's own navigation path is the government's own designated cross-reference for FY2024 budget-request materials — this is corroborating evidence, not a replacement for the MIC-hosted source itself, per the task's instruction.

## Discovered document inventory

All titles/URLs below are transcribed exactly as they appear in each official page's HTML; classifications marked [FACT] were established from the page's own section headings (fiscal year, document category) or from `pdfinfo`, not inferred.

| # | Title (as linked) | URL | Landing page | Purpose/type | PDF/HTML | Page count | Account scope | Comparable to case-001/002? | Evidence |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 令和6年度歳出予算概算要求書（一般会計） | `https://www.soumu.go.jp/main_content/000901372.pdf` | `yosan_R06.html` | **Detailed request-stage document**: 総表 (summary table) + 明細表 (item/expense detail table) + 定員表 (staffing table) | PDF | **454** [FACT, pdfinfo] | 一般会計 (general account) | **Yes — primary candidate** | MIC nav + MOF cross-ref (both agree); pdfinfo; page-1/page-10 rasterization |
| 2 | 令和6年度歳入予算概算見積書（一般会計） | `https://www.soumu.go.jp/main_content/000901924.pdf` | `yosan_R06.html` | Revenue-side request estimate, general account | PDF | not verified (not downloaded/pdfinfo'd) | 一般会計 | Unclear — revenue-side, not the expenditure/expense-row structure case-001/002 test | MIC nav (link text + HTTP 200/size only) |
| 3 | 令和6年度歳入予算概算見積書（特別会計） | `https://www.soumu.go.jp/main_content/000901373.pdf` | `yosan_R06.html` | Revenue-side request estimate, special account | PDF | not verified | 特別会計 (special account) | Unclear | MIC nav (HTTP 200/size only, 14,121 bytes — very small) |
| 4 | 令和6年度歳出予算概算要求書（特別会計） | `https://www.soumu.go.jp/main_content/000901375.pdf` | `yosan_R06.html` | Expenditure request, special account | PDF | not verified | 特別会計 | Possibly, but not investigated further this task | MIC nav (HTTP 200/size only, 30,240 bytes — much smaller than #1) |
| 5 | 令和6年度歳出予算概算要求書（東日本大震災復興特別会計） | `https://www.soumu.go.jp/main_content/000901376.pdf` | `yosan_R06.html` | Expenditure request, earthquake-reconstruction special account | PDF | not verified | 特別会計 | Possibly, but not investigated further this task | MIC nav (HTTP 200/size only, 11,636 bytes) |
| 6 | 総務省所管予算概算要求の概要 | `https://www.soumu.go.jp/main_content/000898534.pdf` (byte-identical to `000897932.pdf`, see below) | `yosan.html` (r6 section) | **Summary/overview only** — request-stage | PDF | **38** [FACT, pdfinfo] | n/a (narrative overview) | **No — confirmed summary, not row-level** | pdfinfo; page size/orientation; Adobe Acrobat Pro producer (typical of a designed overview document, not a generated ledger) |
| 7 | 令和6年度概算要求書及び政策評価調書 (index page, not a PDF itself) | `https://www.soumu.go.jp/menu_yosan/yosan_R06.html` | `yosan.html` | Index/landing page for #1–5 plus policy-evaluation materials | HTML | n/a | n/a | n/a (navigation only) | Direct fetch |
| 8 | 政策評価体系図 / 個別票 (policy evaluation framework diagram / individual sheets) | `000907322.pdf`, `000906095.pdf`, `000906096.pdf`, `000906098.pdf`, `000906100.pdf` | `yosan_R06.html` | Policy evaluation materials, not budget-request line items | PDF | not verified | n/a | No — different document purpose entirely | MIC nav |
| 9 | 一般会計歳出予算各目明細書 (enacted-budget item-detail statement) | `https://www.soumu.go.jp/main_content/000926587.pdf` | `yosan.html` (r6 section, listed alongside but distinct from the request-stage materials) | **Enacted-budget** (not request-stage) detailed item statement | PDF | **[FACT, pdfinfo]** — not fully read this task, but confirmed distinct from #1 by title, URL, and file size (196,089 bytes vs. #1's 876,768 bytes) | 一般会計 | **Explicitly a different lifecycle stage — not case-003 material** (see below) | MIC nav; per-lifecycle-stage `<h2>`/document-list grouping on `yosan.html` |
| 10 | 総務省所管予算の概要 (enacted-budget summary, distinct from #6's request-stage summary) | `https://www.soumu.go.jp/main_content/000938395.pdf` | `yosan.html` (r6 section) | Enacted-budget summary | PDF | not verified | n/a | No | MIC nav |

**[OBSERVATION] Lifecycle-stage mixing on `yosan.html`:** MIC's top budget page lists, under one `令和6年度` heading, at least four distinct budget-lifecycle stages side by side: the original request (`概算要求書`, item #1 above), the enacted/original budget's own item-detail statement (`各目明細書`, item #9), supplementary-budget item-detail statements (`一般会計歳出予算補正（第1号）各目明細書`), and ad hoc reserve-fund-use requests (`一般会計予備費使用要求書`, dated per cabinet decision). **[INTERPRETATION]** This is a direct, concrete illustration of exactly the hazard `protocol/RESEARCH_PROTOCOL.md`'s budget-lifecycle invariant warns about (`request != enacted_budget != settlement`): a careless survey could easily conflate the FY2024 **request**-stage detail document (item #1, the one comparable to case-001/002) with the FY2024 **enacted-budget** detail document (item #9), since both are titled similarly (both contain "各目"-shaped or "明細"-shaped table language) and both are FY2024. This survey did not open item #9's content and makes no claim about its internal structure — it is recorded here only to be correctly excluded from consideration as a request-stage comparandum, not evaluated as a possible future case for a different research question (enacted-budget detail recovery).

## Critical question: summary vs. detailed source

- **[FACT]** The task's lead URL, `https://www.soumu.go.jp/main_content/000897932.pdf`, returns HTTP 200 and is a valid PDF.
- **[FACT]** Its SHA-256 (`7370d245d6ea38733edc99ec345ea01a3cd763411522a30619c8a6e90ecfe4b3`) is **byte-identical** to `https://www.soumu.go.jp/main_content/000898534.pdf`, the summary document actually linked from MIC's own FY2024 navigation. **[OBSERVATION]** These are two different content-management IDs on `soumu.go.jp` serving the exact same binary — the task's lead URL was not independently found via current MIC navigation, but does resolve to the same content as a URL that is.
- **[FACT]** `pdfinfo` on this document: 38 pages, A4 **portrait** (595×842 pt), Producer "Adobe Acrobat Pro (32-bit)", Creator "Adobe Acrobat Pro", tagged/AcroForm present.
- **[FACT]** `pdfinfo` on `000901372.pdf` (the candidate detailed document): 454 pages, A4 **landscape** (842×595 pt), Producer "**List Creator**", not tagged, no AcroForm — the same producer and orientation pattern independently recorded for case-002's METI source (`sources/source-registry.csv`: "A4 landscape, Producer 'List Creator'").
- **[FACT]** Rasterizing `000901372.pdf` page 1 (table of contents) shows: "20 総務省所管 / 令和6年度歳出概算要求書", with an explicit table of contents listing "1. 令和6年度歳出概算要求額総表" (summary table, page 1), "2. 令和6年度歳出概算要求額明細表" (**detail table**, page 5, with sub-sections per internal organization: 010 総務本省 p.5, 040 管区行政評価局 p.246, 050 総合通信局 p.264, 070 公害等調整委員会 p.280, 080 消防庁 p.291), and "3. 令和6年度概算要求定員表" (staffing table, page 451).
- **[FACT]** Rasterizing page 10 (an arbitrary page within the 明細表 section, not chosen for row eligibility) shows a table with columns 要求番号 (request number) | 事項 (item, with numeric codes like `95016-2111-04-0100` and `03-1200`) | 前年度予算額 (previous-year budget) | 6年度概算要求額 (FY2024 request) | 対前年度比較増△減 (delta vs. previous year, using the `△` glyph for decreases) | 備考 (remarks/annotation column) — structurally the same column set, code format, multi-line-wrapped labels, and `△`-glyph delta convention as case-001's and case-002's target tables.
- **[INTERPRETATION]** `000897932.pdf`/`000898534.pdf` is **confirmed to be summary-only** (38 pages, narrative/overview layout, Adobe-authored, no per-row ledger structure observed). `000901372.pdf` **contains the detailed, row-level 明細表 structure** the benchmark needs, and its table structure, code conventions, and government-toolchain fingerprint (`List Creator`, A4 landscape) closely parallel case-002's METI source. **A more detailed official MIC document than the summary lead does exist, and this survey did not stop at the easier-to-discover summary.**

## Acquisition

- **[FACT]** `000901372.pdf`, `000897932.pdf`, and `000898534.pdf` were each fetched with a plain, unauthenticated `curl` request (`User-Agent: Mozilla/5.0`, no cookies/session state) and each returned HTTP 200 with `content-type: application/pdf` on the first attempt — **no WAF/JS challenge was observed on `soumu.go.jp`**, unlike METI's `meti.go.jp`. Per the task's explicit instruction, Playwright/`scripts/source-acquisition/browser-fetch` was therefore **not used** for MIC.
- **[FACT]** The repository's manifest-driven `scripts/source-acquisition/src/acquire.mjs` was reviewed but not used to perform this lock: its `lock` command reads exclusively from `scripts/request-ingestion/source_manifest.json`, a file coupled to the existing request-ingestion PoC's own two Digital Agency sources, not a generic single-URL entry point. Using it would have required editing that shared manifest for an unrelated subsystem, which this task's scope discipline (no repository reorganization, no unrelated changes) argues against. **[OBSERVATION]** `acquire.mjs`'s `lockCommand()` also still contains the same unconditional lock-overwrite pattern (`lock.sources[existingIndex] = record`) that was fixed in `browser-fetch.mjs` after the PR #2 review — this is a real, pre-existing inconsistency between the two acquisition tools, not fixed in this task (out of scope; recorded under Unresolved issues below).
- **[FACT]** Acquisition and locking were instead performed with a small, uncommitted scratch script (`plain-lock-mic.mjs`, not added to the repository) that does a plain `fetch()` and then calls the already-committed, already-reviewed `applyAcquisition()`/`decideLockAction()` functions exported from `scripts/source-acquisition/browser-fetch/src/browser-fetch.mjs` — reusing the exact immutable-lock policy fixed after PR #2, without duplicating or bypassing it, and without invoking Playwright.
- **[FACT]** `mic-fy2024-general-account-expenditure-request` (`000901372.pdf`) was locked: SHA-256 `cc54dbe5f689116619a1f8453747d47bca5b960137f90869ead26954d651703b`, 876,768 bytes, `acquisitionMethod: "plain-fetch"`. Immutability was verified by re-running the same acquisition immediately afterward: result `IDENTICAL`, with the lock entry and raw file confirmed byte-for-byte unchanged.
- **[FACT]** The summary document (`000897932.pdf`/`000898534.pdf`) and the four smaller request-family PDFs (items #2–5 in the inventory table) were **not locked** — downloaded only to a temporary, non-repository location for hashing/`pdfinfo`, per the task's instruction not to mass-acquire unrelated materials. Their SHA-256/page-count facts recorded above were established this way but are not persisted in `sources/source-lock.json`.
- `sources/source-registry.csv` was updated with one new row for the locked source, following the exact column convention of the existing three rows, with full provenance (both discovery routes, acquisition method, `pdfinfo` facts, and an explicit note that no row has been selected).

## Suitability assessment

**[RECOMMENDATION]** MIC (総務省) remains a good case-003 candidate. The recommended future benchmark source is `mic-fy2024-general-account-expenditure-request` (`https://www.soumu.go.jp/main_content/000901372.pdf`, locked at SHA-256 `cc54dbe5f689116619a1f8453747d47bca5b960137f90869ead26954d651703b`), specifically its `令和6年度歳出概算要求額明細表` section (pages 5–245, per its own table of contents, before the `管区行政評価局` sub-organization begins at page 246). This is a recommendation for a future task to evaluate against a properly frozen selection protocol — **it is not a frozen selection**, and no specific row, page, or organization sub-section has been chosen.

## Freeze confirmation

- No target row has been selected for case-003.
- No `ground-truth.json` exists for case-003.
- No engine (pdf.js/PyMuPDF/Docling/MinerU/PaddleOCR, or `npm run docbench`) has been run against any MIC document.
- No benchmark/evaluator semantics were changed.
- No Case Package (`document-profile.json`/`research-history.jsonl`) was created for case-003 in this task (per the task's instruction not to backfill prematurely).
- `△` presence/absence, expected engine difficulty, or known-parser-failure patterns were not used as a basis for anything in this survey — the page-10 rasterization was chosen arbitrarily (the tenth page of the PDF) purely to confirm table-column structure at a high level, not to identify or evaluate a candidate row.

## Representation observations (prospective, unconfirmed, not acted on)

- **[OBSERVATION]** The existing `document-profile.json` schema's `sourceSafeProfile` includes a `pageLevelUnitLabelPresentOnTargetPage` feature keyed to a single target page. MIC's document has multiple internal organization sub-sections (総務本省, 管区行政評価局, 総合通信局, 公害等調整委員会, 消防庁) each potentially starting a new page range — if a future MIC case's target row falls in a sub-section whose unit-label placement differs from `010 総務本省`'s, the current schema has no field distinguishing "page-level" from "sub-organization-level" unit-label scope. Flagged as a possible future schema gap, not fixed here, and not yet confirmed to actually occur (no page beyond page 10 was inspected).
- **[OBSERVATION]** `acquire.mjs`'s manifest-only design means the existing "generic source acquisition" story in this repository is really two separate tools (`acquire.mjs` for the two original Digital Agency sources via a coupled manifest, `browser-fetch.mjs` for anything else via direct CLI args) rather than one consistent path. This was already implicitly true before this task, but locking a third, unrelated ministry's source made the seam more visible. Not resolved here.

## Files changed

- `fixtures/document-understanding/case-003/20260926_1443_Case003_MIC_Source_Survey.md` (this file, new)
- `sources/source-lock.json` (one new entry: `mic-fy2024-general-account-expenditure-request`)
- `sources/source-registry.csv` (one new row, same source)
- `sources/raw/mic-fy2024-general-account-expenditure-request.pdf` (git-ignored, not committed)
- `state/CURRENT_STATE.json`, `state/TODO.md`, `state/CHANGELOG.md` (state updates)

No case-001/case-002 file, no adapter/normalizer/evaluator, no Ground Truth, and no Case Package schema was modified.

## Validation

```bash
npm run validate      # PASS
git diff --check       # clean
```

Source verification: the newly-locked source's SHA-256 was independently reproduced twice (once during the initial lock, once during the immutability re-run) and matches; both are local, filesystem-level verifications (`shasum -a 256` equivalent inside `applyAcquisition()`), not a network-level WAF/JS-challenge verification, since no such challenge exists for `soumu.go.jp` to distinguish from. `npm run docbench` was not run, per the task's explicit instruction.

## Unresolved issues

- `acquire.mjs` still has the pre-PR-#2-review unconditional lock-overwrite behavior that `browser-fetch.mjs` no longer has — a real inconsistency between the repository's two acquisition tools, not fixed in this task.
- Page counts/content structure for the four smaller MIC PDFs (items #2–5 in the inventory table) were not independently verified beyond HTTP size — their suitability, if any, as supplementary case-003 material is unknown.
- MOF's `<要望一覧>`/summary-table links for MIC point to a `#r5` (FY2023) anchor rather than `#r6` — unclear whether this is a stale link on MOF's side or intentional; not investigated further.
- Whether MIC's document exhibits the same annotation-placement, CJK-wrap-spacing, or table-grid-density issues found in case-001/case-002 is completely unknown — no engine has been run, by design.
- Total page count and structural content of `000901372.pdf`'s later organizational sections (管区行政評価局, 総合通信局, 公害等調整委員会, 消防庁, pages 246–450) were not inspected — only the table of contents and one arbitrary early page were viewed.

## Recommended next step

Freeze a case-003 row-selection protocol for `mic-fy2024-general-account-expenditure-request` (specifically its `令和6年度歳出概算要求額明細表` section, pages 5–245, the `010 総務本省` organizational range), modeled on `fixtures/document-understanding/case-002/20260926_0834_Case002_Selection_Protocol.md`'s E1–E5 eligibility-criteria and engine-blind-enumeration discipline, **before** visually selecting any row. Not executed in this task.
