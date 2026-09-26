# case-005 — MLIT (国土交通省) FY2024 Source Survey

Status: **source survey only. No row selected. No selection protocol. No Ground Truth. No benchmark engine run.**

Date: 2026-09-27 (Asia/Tokyo)

Branch: `research/case-005-mlit-source-survey`, created from `origin/main` at `34c9424` (the merged case-004 checkpoint, PR #4).

This document uses the same evidence discipline as the case-002/003/004 surveys: **[FACT]** (independently verified against an official source or a locally-computed value), **[OBSERVATION]** (noticed, not yet interpreted), **[INTERPRETATION]** (a conclusion drawn from facts/observations), **[RECOMMENDATION]** (a proposal, never a frozen selection).

## Scope / non-goals

This task performs **source survey, source acquisition, and source characterization only**. It does **not**: select a case-005 target row; freeze a selection protocol; create Ground Truth; run any benchmark engine; adapt any existing production code; interpret `繰入`-shaped line items against MOF-CSV concepts; or reconstruct amounts via arithmetic. All of these are explicitly deferred to later, separately-scoped tasks.

## 1. Git baseline

- **[FACT]** `origin/main` freshly fetched at task start: `34c9424` (merge commit for PR #4, the case-004 research line). Working tree was clean before this task's first edit.
- **[FACT]** New branch `research/case-005-mlit-source-survey` created directly from `origin/main` (not from the case-004 branch), pre-task `HEAD` = `34c9424`.
- **[FACT]** No case-001–004 frozen artifact was touched in this task (confirmed by `git status`/`git diff` showing only new `case-005`-scoped files and the two shared `sources/*` registries).

## 2. Discovery provenance

- **[FACT]** Direct search to MLIT's own page `https://www.mlit.go.jp/page/kanbo05_hy_003158.html` (page title: "令和6年度概算要求書 - 国土交通省") lists six PDFs under distinct headings: 一般会計歳入 (`001630391.pdf`), **一般会計歳出 (`001630995.pdf`, the target)**, 自動車安全特別会計歳入/歳出 (`001630392.pdf`/`001630393.pdf`), and 東日本大震災復興特別会計歳入/歳出 (`001630394.pdf`/`001630395.pdf`). Only one PDF is linked under "一般会計歳出" — no separate 総表/明細表/定員表/表紙 links are shown on this landing page (contrast with case-004's four-file listing).
- **[FACT]** MOF's official FY2024 cross-ministry request-document link table (`https://www.mof.go.jp/policy/budget/budger_workflow/budget/fy2024/2024yokyuippan_link.html`, the same table already used for case-002/003/004) — the 国土交通省 row's **both** 歳入 and 歳出 columns link to the same `kanbo05_hy_003158.html` page found via direct search.
- **[INTERPRETATION]** Two independent routes converge on the identical landing page, corroborating it as the authoritative source for MLIT's FY2024 request-stage general-account materials — the same convergence pattern already established for case-002/003/004. The pre-survey candidate URL (`001630995.pdf`) is confirmed correct, not merely assumed.

## 3. Acquisition result

- **[FACT]** Plain, unauthenticated `curl`/`fetch()` succeeded on the first attempt (HTTP 200, `content-type: application/pdf`, served via CloudFront/S3) — **no WAF/JS challenge observed on `mlit.go.jp`**. Playwright/`browser-fetch` was therefore not used.
- **[FACT]** Downloaded bytes verified to start with the PDF magic number (`%PDF-1.3`) before locking.
- **[FACT]** Locked via the existing, unmodified shared `lock-policy.mjs` (the same immutable-lock module already used for case-003/004), through a small, uncommitted scratch script — not `scripts/source-acquisition/src/acquire.mjs` (still coupled to an unrelated request-ingestion manifest, per the same reasoning already documented in prior surveys) and not `browser-fetch.mjs` (no WAF encountered, so Playwright was unnecessary).
- **[FACT]** `sourceId`: `mlit-fy2024-general-account-expenditure-request`; locked successfully on the first attempt (`NEW`); **immutability re-verified** via an immediate second run, which correctly reported `IDENTICAL` with no lock/raw mutation.
- No acquisition failure occurred; there is no failure layer to report for this source.

## 4. Source identity / SHA-256

- Title: 令和6年度歳出概算要求書（一般会計）
- Official PDF: `https://www.mlit.go.jp/page/content/001630995.pdf`
- Local raw path: `sources/raw/mlit-fy2024-general-account-expenditure-request.pdf` (git-ignored, not committed)
- **SHA-256**: `4eebb84cec72a4b3b11a2b89c41093550bef5a07095d5c7b178e238406b08217` — independently recomputed via `shasum -a 256` and confirmed to match `sources/source-lock.json`'s own recorded value exactly.
- Byte size: 2,115,896 bytes.

## 5. PDF technical characteristics

- **[FACT]** (`pdfinfo`): 1,097 pages; A4 landscape (842×595 pts); PDF version 1.3; Producer "List Creator" (the same toolchain fingerprint already seen for METI/MIC/MEXT's own sibling cover/summary files); `CreationDate`: 2023-09-14 — **the identical calendar date already recorded for MEXT's own four sibling files**, consistent with a shared, government-wide PDF-generation batch for this fiscal year's request round, not evidence of any relationship beyond that.
- **[FACT]** **Not encrypted** (`Encrypted: no`) — a genuine, disclosed difference from case-004 (MEXT, permission-only AES-256) and a return to case-002/003's own unencrypted convention.
- **[OBSERVATION]** No custom metadata, no tagging, no JavaScript, no form fields — a plain, non-interactive document, consistent with every prior case's own source.

## 6. Packaging model

- **[FACT]** Unlike case-004 (MEXT's four separate sibling PDFs), MLIT's FY2024 general-account expenditure request is packaged as **one single combined PDF** containing the document-wide index (目次), the summary table (総表), and the detail table (明細表) together — structurally closer to case-002 (METI)/case-003 (MIC)'s own single-file model than to case-004's split model.
- **[FACT]** PDF page 1 (`pdfPageIndex` 0) is a blank-margin title page ("28　国土交通省所管 / 令和6年度歳出概算要求書") with no page number printed on it. PDF page 2 is blank.
- **[FACT]** PDF page 3 (`pdfPageIndex` 2), printed page "1", begins the document-wide **目次 (index)**: title "令和6年度歳出概算要求額目次", with columns 要求番号 | 区分 | ページ (repeated in two side-by-side blocks per physical page). Its own first entries list: `令和6年度歳出概算要求額総表` → page 1; `令和6年度歳出概算要求額明細表` → page 19; then `(組織) 010 国土交通本省` → page 19, `(項) 002 国土交通本省共通費` → page 19, request no. `①` code `05-95` `国土交通本省一般行政に必要な経費` → page 19, continuing with dozens of further expense-line entries (request numbers 2 through 36+ visible on this single TOC page alone) with individual page references reaching into the 100s–200s **on this first TOC page alone**.
- **[OBSERVATION]** This 目次 is **markedly more granular** than any prior case's own table of contents: it itemizes every individual expense-code line (not merely organization/item headers) with its own page reference, for the entire ~995-page detail table. This is a genuinely new packaging characteristic relative to case-001–004, whose TOCs were comparatively coarse (organization/item-level only).
- **[FACT]** Printed page label offset confirmed consistent at three independent sample points spanning the 総表→明細表 boundary: printed page 10 → `pdfPageIndex` 19 (PDF page 20); printed page 11 → `pdfPageIndex` 20 (PDF page 21); printed page 19 → `pdfPageIndex` 28 (PDF page 29) — a constant `pdfPageIndex = printedPage + 9` relationship across this range, distinct from the outer 目次's own page-3-equals-printed-page-1 numbering (i.e., the 目次 itself is *not* part of the same continuous printed-page count as 総表/明細表, occupying an un-integrated preamble of at least 8 physical pages before 総表's own printed page 1 begins).
- **[OBSERVATION]** Printed-label format differs between the two internal tables: 総表 pages carry a bare `"N　国"` label (e.g. `"10　国"`); 明細表 pages carry a ministry-headquarters-tagged `"国（本） N"` label (e.g. `"国（本） 19"`) — the same `(本)` suffix convention already established for case-002 (`経(本)`), case-003 (`総(本)`), and case-004 (`文（本）`).

## 7. Table/document structure

- **[FACT]** 明細表 (detail table) confirmed to begin at printed page 19 = `pdfPageIndex` 28 (PDF page 29), title "令和6年度歳出概算要求額明細表", sheet header "28　国土交通省所管", unit label **"(単位: 千円)"** printed once, directly beneath the table title, above the column headers — the same page-level unit-label position already established for case-002/003 (though whether this label repeats on every subsequent page, or only at this section's own start, was **not exhaustively checked** in this survey, consistent with case-004's own eventual finding that such labels are sometimes table-wide-once rather than page-repeated).
- **[FACT]** Column structure on this first 明細表 page: 要求番号 | 事項 (item, with codes) | 前年度予算額 | 6年度概算要求額 | 対前年度比較増△減 | 備考 — the same six-column structure already established for case-001–004.
- **[FACT]** First content rows, top to bottom: `010　国土交通本省` (組織-level aggregate, no code, delta `△530,617,743`) → `002　国土交通本省共通費` (項-level aggregate, no code, delta `18,734,083`) → request no. **`①`**, code **`05-95`**, label **`国土交通本省一般行政に必要な経費`** (delta `18,675,138`, positive, no `△`) — **[OBSERVATION]** this is the identical structural template already found as the deterministic first-eligible row in case-002 (METI, `①/01-95`), case-003 (MIC, `①/01-95`), and case-004 (MEXT, `①/01-95`), here appearing as `①/05-95` instead. **This is a source-survey observation only — no row-selection protocol exists yet, and this pattern must not be assumed as case-005's eventual target**, per this task's own explicit prohibition.
- **[FACT]** Beneath the `①05-95` row, the same deep nested numbered sub-breakdown convention already seen in every prior case: `001　大臣官房一般行政に必要な経費` → `006　既定定員に伴う経費` → `05　人件費` → individually numbered lines (`95016-2111-02-0000　職員基本給`, etc.), all still on the same or immediately following pages.
- **[FACT]** The document's own 目次 (index, §6) lists 12 internal organizations within this single file: `010 国土交通本省` (page 19), `035 国土技術政策総合研究所` (500), `045 国土地理院` (572), `048 海難審判所` (599), `050 地方整備局` (606), `060 北海道開発局` (694), `070 地方運輸局` (768), `080 地方航空局` (845), `095 観光庁` (859), `100 気象庁` (898), `105 運輸安全委員会` (975), `110 海上保安庁` (995) — **the widest internal-organization count and page span of any case surveyed so far** (12 organizations across ~995+ printed pages, vs. case-003/MIC's 5 organizations across 454 pages).

## 8. Representative page observations

- **[FACT]** 総表 (summary table), inspected at printed pages 10–11 (`pdfPageIndex` 19–20): **not** a coarse organization/item-level summary — it is itself already itemized down to individual expense-code rows (e.g. `01-41　治水事業調査諸費に必要な経費`, `35-43　空港整備事業の財源の自動車安全特別会計空港整備勘定へ繰入れに必要な経費`), each carrying **two** amount sub-columns per year (一般行政経費 / その他の経費, plus a computed 計 column) for both 前年度予算額 and 6年度概算要求額, a delta column, and a cross-reference **明細書頁数** (detail-book page number) column pointing directly into the corresponding 明細表 page. **[OBSERVATION]** This is a materially richer 総表 structure than any case-001–004 source is known to have — the summary table and the detail table are cross-linked by an explicit page-number column, a representation-linkage mechanism not previously documented in this research program.
- **[OBSERVATION]** Several 総表 rows in this same sampled region carry an explicit `一般行政経費`/`その他の経費` split for the *same* expense line, rather than case-001–004's single combined amount column — a genuinely different column convention worth flagging for any future comparison, not yet investigated further.

## 9. Comparison with cases 001–004

**Common structural elements** (confirmed present in MLIT, matching every prior case):
- 組織 (organization) → 項 (item) → 経費 (expense) hierarchy.
- 要求番号 (request number) column, using the same circled-numeral-then-plain-integer convention already seen across case-002/003/004.
- 経費コード (`NN-NN` format, e.g. `05-95`).
- 前年度予算額 / 6年度概算要求額 / 対前年度比較増△減 three-column amount structure, with the same `△` decrease-glyph convention.
- 備考 (remarks) column.
- 千円 (thousand-yen) unit convention.
- Deep nested numbered sub-line-item breakdowns beneath a selected expense row, using the same long dash-segmented code format (`95016-...`) already seen in every prior case.
- Producer "List Creator" toolchain fingerprint (shared with METI/MIC/MEXT's sibling files).
- The same `①/[code]/[ministry]一般行政に必要な経費` first-item-header template shape (observed only, not selected).

**Genuinely different from cases 001–004**:
- **Packaging**: single combined file (like case-002/003), but with an unusually long, granular, expense-line-level 目次 not seen in any prior case's coarser organization/item-level TOC.
- **総表 richness**: itemized down to individual expense codes with a two-part amount-column split and an explicit cross-reference page-number column into 明細表 — none of case-001–004's summary tables are known to have this level of granularity or an explicit page-number linkage column.
- **Encryption**: none (a return to case-002/003's convention, a difference from case-004's permission-only AES-256).
- **Scale**: 1,097 pages, 12 internal organizations — the largest organization count of any case surveyed, though a smaller total page count than case-004's 1,339 pages.
- **Printed-label format split**: 総表 pages use a bare `"N　国"` label; 明細表 pages use the ministry-tagged `"国（本）N"` label — a within-document label-format change tied to which internal table a page belongs to, not previously documented as varying *within* one file (case-004's own label-prefix variation, by contrast, was tied to *organization*, not to *table section*, within one file).

## 10. Potentially interesting structures (`繰入` etc.)

- **[FACT]** The literal string `繰入` (and the fuller phrases `...自動車安全特別会計へ繰入`, `...自動車安全特別会計空港整備勘定へ繰入れに必要な経費`) is **confirmed present**, verbatim, in the 総表 excerpt sampled in this survey (rows referencing 空港整備事業費, 航空機燃料税財源, at printed 総表 pages 10–11), with populated, non-zero amount values in at least one instance (e.g. `23,681,381`).
- **This is recorded as existence-only, per this task's explicit constraint**: no MOF-CSV correspondence is inferred; no relationship between this `繰入` line and any budget-lifecycle concept is asserted; no amount reconciliation was attempted; this is not used, and must not be used, as a selection or Ground Truth input. It is flagged here solely as a source observation with potential future research value, exactly as the originating task requested.

## 11. Accessibility/renderability observations

- **[FACT]** `pdftoppm` rendering succeeded on every page sampled in this survey (pages 1, 3, 20, 21, 29–31), with no error, warning, or degraded output — consistent with the source being unencrypted and posing no rendering obstacle.
- **[FACT]** `pdfinfo` metadata reading succeeded without any warning or error.
- No text-extraction, table-understanding, or engine-comparison work was performed in this survey — per the task's own explicit prohibition, no Docling/pdf.js/PyMuPDF ranking or comparison was started.

## 12. Source-safe facts vs. interpretation

Every finding above is tagged `[FACT]` (directly observed against the source or independently recomputed), `[OBSERVATION]` (noticed but not yet explained), or `[INTERPRETATION]` (a conclusion drawn from facts/observations, disclosed as such). No `[RECOMMENDATION]` in this report selects, implies, or hints at a specific target row — the `①/05-95` template match (§7) is recorded as an observation of structural similarity to prior cases, explicitly not as a selection input, per the task's own strict instruction.

## 13. Unknowns

- Whether the 明細表's own unit label (`(単位: 千円)`) repeats on every subsequent page or is stated once for the whole table (as case-004 ultimately found for MEXT) was **not** investigated in this survey.
- The exact page-count boundaries between each of the 12 internal organizations beyond their own 目次-listed starting pages were not independently re-verified page-by-page.
- Whether the 総表's own two-part amount-column split (一般行政経費/その他の経費) is a document-wide convention or varies by row/organization was not investigated beyond the one sampled region.
- Whether the `一般会計歳入`, `自動車安全特別会計`, or `東日本大震災復興特別会計` sibling PDFs (also linked from the same MLIT landing page) contain further relevant `繰入`/transfer structures was not investigated; only the target 一般会計歳出 PDF was acquired and locked.
- Whether encryption/rendering behavior holds uniformly across all 1,097 pages (only a small sample was checked) is not established.

## 14. Methodological risks

- The 目次's own page-number references (§6, §8) were read directly from the rendered TOC pages and cross-checked against the 明細表's own printed page label at one boundary point (page 19) — this is a reasonable but not exhaustive validation; a future selection-protocol task should independently re-verify any organization boundary it actually relies on, per the same discipline already established in case-002/003/004's own protocols.
- The 総表's richer, page-cross-referenced structure (§8) raises a genuine future design question — not resolved here — about whether a case-005 selection protocol should define its selection universe purely from 明細表 (as every prior case has done) or whether 総表's own explicit page-linkage could offer an alternative, more source-grounded universe-definition mechanism. This is recorded as an open methodological question for the next task, not decided here.

## 15. Suitability verdict for case-005

**SUITABLE**

Justification, based solely on source properties established in this survey: MLIT's FY2024 general-account expenditure request is authoritatively discovered via two independently converging routes; successfully acquired and immutably locked without any acquisition failure; unencrypted and fully renderable; confirmed via direct inspection (not assumed) to contain the same core row-level structure (組織/項/経費/要求番号/経費コード/amount-triple/備考) already validated across four prior cases; and offers genuinely new packaging and structural characteristics (a granular expense-level 目次, a richly cross-referenced 総表, the widest internal-organization count surveyed so far, and confirmed-present `繰入`-shaped structures) that would meaningfully extend this research program's corpus diversity, distinct from — not a repeat of — case-004's own new characteristics (standalone multi-file packaging, encryption).

This verdict does not authorize row selection, which remains a separate, later task.

## Files changed

- `fixtures/document-understanding/case-005/20260927_0806_Case005_MLIT_Source_Survey.md` (this file, new)
- `sources/source-lock.json` (one new entry: `mlit-fy2024-general-account-expenditure-request`)
- `sources/source-registry.csv` (one new row, same source)
- `sources/raw/mlit-fy2024-general-account-expenditure-request.pdf` (git-ignored, not committed)
- `state/CURRENT_STATE.json`, `state/TODO.md`, `state/CHANGELOG.md` (state updates)

No case-001–004 file, no selection protocol/record, no Ground Truth, no benchmark/adapter/normalizer/evaluator, and no source-acquisition code was modified.

## Recommended next step

Freeze a case-005 row-selection protocol for `mlit-fy2024-general-account-expenditure-request`, modeled on case-002/003/004's own methodology (critiquing, not copying, their eligibility criteria; explicitly deciding a selection universe from the document's own 12-organization structure, most likely starting with `010 国土交通本省`), before visually selecting any target row. **Not executed in this task.**
