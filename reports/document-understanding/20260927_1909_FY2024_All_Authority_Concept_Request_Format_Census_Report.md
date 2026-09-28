# FY2024 All-Authority 概算要求 PDF Format Census — Report

Status: **Seventh pass. All 33 originally-frozen population authorities now have a closed status: 31 acquired/inspected in scope, 1 precisely confirmed absent from its own live page. A 34th candidate authority (復興庁) has been investigated and found categorically out of scope (special-account-only budgeting). Provisional format families, not finalized. No row selection, no Ground Truth, no benchmark engine run, no schema/production change.**

Date: 2026-09-27 (Asia/Tokyo)

Branch: `research/fy2024-all-authority-format-census`, from `main@fc7c0ea`.

## 10.1 Population

`[FACT]` MOF's official FY2024 cross-authority index (`2024yokyuippan_link.html`) lists **33 authorities** (frozen in `20260927_1909_FY2024_Population_Freeze.md`, commit `558f7fb`). See §10.2e for a 34th candidate (復興庁) discovered via a *different* MOF index page in this pass, not yet added to the frozen population.

- Acquired and in-scope: **31** (5 reused from case-001–005's own already-committed evidence; 26 newly acquired this task)
- Precisely confirmed absent from the authority's own current live page (request-stage retention window has elapsed; the final-budget-stage document for the same year is still retained): **1** (国立国会図書館/NDL)
- Direct-PDF-vs-landing-page ratio: most authorities required a landing-page hop; several (防衛省, 会計検査院, 裁判官弾劾裁判所, 参議院) required bypassing a blocked or unhelpful general landing page in favor of a year-specific direct URL found via web search.
- Single-file vs. split-package ratio among the 30 acquired: **at least 21 single/combined**, **≥7 split** (文部科学省=4 files, 内閣官房=17 files (exhaustively confirmed), 金融庁=12 files, 内閣本府=~50 files, MHLW's narrative package=10+ files across 3 sub-pages, coexisting with its own single-file 1,723-page 総表+明細表 document).

## 10.2g Seventh-pass: 裁判官訴追委員会 fully resolved; 復興庁 categorically out of scope

`[FACT]` **裁判官訴追委員会 (Sotsui) — RESOLVED.** The user identified the exact URL: `https://www.sotsui.go.jp/budget/images/r6budget_yokyu.pdf`. Verified before locking (`CreationDate` 2023-08-04) and confirmed by its own title page (`令和6年度歳出概算要求書` for `02 国会所管（裁判官訴追委員会）`) to be the genuine request-stage document, distinct from the enacted-budget-stage `各目明細書` acquired in an earlier pass (which is retained as a separate, still-valid artifact for the out-of-scope family, not deleted). Contains a 総表 (7th confirmed cross-reference-summary instance) and a genuine 明細表. **This closes the sole remaining "acquired but out of scope" population entry** — all 33 originally-frozen population authorities are now either genuinely in-scope or precisely characterized as absent, with none remaining in an ambiguous or wrong-stage state.

`[FACT]` **復興庁 (Reconstruction Agency) — investigated, found categorically out of scope.** Its own budget page (`reconstruction.go.jp/topics/post-72.html`) confirms it publishes **no 一般会計 (general account) expenditure request at all** — its entire FY2024 budget mechanism operates exclusively through the 東日本大震災復興特別会計 (reconstruction special account), which is explicitly excluded by this census's own originating scope (special accounts out of scope). A 103-page special-account request file was located and locked for evidence/reference only, but is **not counted as an in-scope acquisition** for this authority — it is the first authority in this census whose *entire* budget request is categorically out of scope, not merely one document among several (contrast with sotsui, which had both an in-scope and an out-of-scope document). `[INTERPRETATION]` The file's own title (`9101 東日本大震災復興特別会計`, unqualified by any specific ministry) suggests it may be the coordinating, cross-government edition of the special-account book that other authorities' own smaller special-account fragments (内閣官房's `r6_16`/`r6_17`, 消費者庁's and 環境省's own `9101`-titled files) are individually excerpted from — not independently verified in this pass.

## 10.2d Sixth-pass resolution: 参議院 (Sangiin) — last genuinely-unresolved entry closed

`[FACT]` The user found the exact URL via web search: `https://www.sangiin.go.jp/jpn/annai/oshirase/pdf/r6gaisan-yokyusyo-250905.pdf`. This census's own automated attempts (5+ targeted `WebSearch` queries, direct filename-pattern-guessing against both sibling years' confirmed conventions) had failed to locate it.

Before locking, this task verified the file is genuinely FY2024 request-stage material, not a mislabeled later document — the filename's own `250905` suffix (which would suggest a September 2025 date) is misleading; `pdfinfo`'s own `CreationDate` field reads `2023-08-09`, consistent with every other authority's own FY2024 submission window. Content confirms: title page reads `令和６年度歳出概算要求書` for `02 国会所管（参議院）`; contains a 総表 (pages 1–2, cross-reference-summary style matching mlit/env/caa/dangai/mhlw) and a genuine row-level 明細表 (pages 3–21), showing the same `NNNNN-NNNN-NN-NNNN` subordinate accounting code convention (`95012-2122-08-1030`) seen throughout this census.

**This resolves the last genuinely-unresolved population entry.** As of this pass, all 33 originally-frozen population authorities have a closed status: 30 in-scope, 1 acquired-but-out-of-scope (sotsui), 1 precisely-confirmed-absent (ndl) — with one further discovery noted in §10.2e below.

## 10.2e A 34th authority discovered: 復興庁 (Reconstruction Agency)

`[FACT]` While investigating a user question about 裁判官訴追委員会's own absence from a *different* MOF index page, this task fetched `https://www.mof.go.jp/policy/budget/budger_workflow/budget/fy2024/2024gaisangaiyo_link.html` (a "概算要求書、要望一覧及び政策評価調書公開ページへのリンク先一覧（概要）" page, distinct from `2024yokyuippan_link.html`, the page this census's own population was originally frozen from). This second MOF index lists **30 authorities**, overlapping heavily with the frozen 33-authority population but with two differences:

- It does **not** list 裁判官訴追委員会 or 裁判官弾劾裁判所 (see §10.2f for why this is not a contradiction).
- It **does** list **復興庁 (Reconstruction Agency)** — an authority **not present in this census's own frozen 33-authority population** at all. This is a genuine gap in the original population freeze, not an acquisition failure for an already-known authority.

`[INTERPRETATION]` This suggests MOF maintains more than one cross-authority index page for FY2024, each with a slightly different membership, and this census's own population freeze (based on a single page) may not be perfectly complete. 復興庁 is recorded here as a newly-discovered 34th candidate population member, not yet acquired or inspected — see §10.9 for its addition to remaining scope.

## 10.2f What is 裁判官訴追委員会?

`[FACT]`, for context: 裁判官訴追委員会 (the Committee on the Impeachment of Judges) is a National-Diet-affiliated body, established under Japan's Constitution (Article 64) and the 裁判官弾劾法 (Judge Impeachment Act), responsible for **investigating and prosecuting** judges accused of misconduct sufficient to warrant removal from office. It works alongside — but is organizationally distinct from — 裁判官弾劾裁判所 (the Court of Impeachment for Judges), which actually **tries** the case the committee brings. Both are very small, standing Diet bodies (this census's own acquired sotsui-hosted document, itself out of scope, is only 24 pages and covers five such small bodies together; dangai's own request-stage document is only 9 pages). Their absence from the `2024gaisangaiyo_link.html` overview-specific index (§10.2e) is plausibly because such very small bodies may not separately publish a "概要" (overview) summary document — only their full request book — though this has not been independently verified in this task.

## 10.2c Fifth-pass: 内閣官房 (CAS) exhaustively re-confirmed

`[FACT]` The user asked whether more detail files exist beyond the 2 originally sampled (`r6_01.pdf`, `r6_02.pdf`). A full, exact link enumeration of `gaisan_youkyuu_r6.html` confirmed exactly **17 files** (not the earlier "~17" estimate) — all 17 were individually acquired and first-page-inspected in this pass, not merely sampled:

- **一般会計 (general account)**: 1 cover (`r6_01`) + 15 bureau-level detail files, covering **9 distinct bureaus/offices**: 総務官室 (4 sub-offices: 総務課/会計課/官邸事務所/厚生管理官室 — `r6_02`–`r6_05`), 内閣官房・人に伴う経費 (`r6_06`), 副長官補 (2 sub-offices: 副長官補/危機管理 — `r6_07`–`r6_08`, the largest detail file at 29 pages), 内閣広報室 (`r6_09`), 内閣情報調査室 (2 sub-offices: 内閣情報調査室/衛星情報センター — `r6_10`–`r6_11`, 19 pages), 内閣サイバーセキュリティセンター (`r6_12`), 内閣人事局 (`r6_13`), 国家安全保障局 (`r6_14`), 内閣感染症危機管理統括庁 (`r6_15`).
- **東日本大震災復興特別会計 (reconstruction special account)**: a separate 2-file cover+detail pair (`r6_16`–`r6_17`), mirroring the general account's own cover+detail structure at a smaller scale.

Every one of the 17 files is permission-only AES-encrypted; every one follows the same printed-page-label convention (`内（官）` for the general account, `復興特` for the special account). This confirms a **genuinely complete and clean bureau-level split**, the most granular *individually-verified* (as opposed to merely counted) package structure in this census. `familyConfidence` for this authority is upgraded to **high** — all 17 files acquired and inspected, not sampled.

## 10.2b Fourth-pass resolution: 厚生労働省 (MHLW) — MAJOR CORRECTION

`[FACT]` The user provided the exact URL `https://www.mhlw.go.jp/wp/yosan/yosan/24syokan/dl/05-1b-01.pdf`, previously unlocated by this census. This file is the LARGEST single document in the entire census (**1,723 pages**, exceeding 法務省's own 737 pages), Producer "List Creator," not encrypted, and contains:

1. A granular, expense-code-level 総表 (pages 1–12), itself already itemized to individual `01-95`/`03-95`/`05-95`-style expense-code rows with split `一般行政経費`/`その他の経費`/`計` amount subcolumns and an explicit `明細書頁数` cross-reference column — the **5th confirmed instance** of the cross-reference-summary mechanism (after mlit, env, caa, dangai), now the largest host document of it.
2. A genuine row-level `明細表` (pages 13–1,723) spanning **8 internal organizations** (010 厚生労働本省, 030 検疫所, 040 国立ハンセン病療養所, 045 厚生労働本省試験研究機関, 050 国立障害者リハビリテーションセンター, 070 地方厚生局, 080 都道府県労働局, 090 中央労働委員会), confirmed showing the standard `要求番号`/`事項`/`前年度予算額`/`対前年度比較増△減`/`備考` grammar and the same `NNNNN-NNNN-NN-NNNN` subordinate accounting code convention seen throughout this census (e.g. `95016-2111-05-1200`), printed page label `厚（本）`.

**MHLW is RECLASSIFIED from "narrative-only family" into both the cross-reference-summary family and the List-Creator combined-ledger family.** The narrative/policy-evaluation files found in the first two passes (`01-02.pdf`, `06-01.pdf` through `06-15.pdf`, etc.) remain valid, separately-existing artifacts for this same authority — both document types genuinely coexist on the same site; they are not mutually exclusive.

**Root cause of the miss (added to §10.7's own Failure/Learning discipline)**: two prior passes used `WebFetch` to enumerate links on this authority's own `index.html`, `03.html`, and `05.html` sub-pages. That enumeration surfaced a *sibling* file, `05-1a-01.pdf` (the revenue/歳入 counterpart), but never surfaced `05-1b-01.pdf` (the expenditure/歳出 counterpart actually being sought) — even though both files apparently exist on the same page. This is an **incomplete automated link-extraction result**, not a genuine absence of the file on the page. **Lesson**: `WebFetch`'s own summarized link enumeration is not guaranteed exhaustive, particularly among visually similar, densely-packed file lists differing only in a single character (`1a` vs `1b`) — a negative finding from an automated page-content summary is weaker evidence than a negative finding from a direct, exhaustive fetch of the page's raw HTML, and should be held with correspondingly less confidence when the stakes of a false negative are high (as they were here — this single miss drove two entire passes' worth of "narrative-only" classification).

## 10.2a Third-pass resolution: 外務省 (MOFA)

`[FACT]` MOFA's domain-wide Akamai block was re-confirmed in this pass at the DOMAIN level, not merely the file level: a full Playwright/Chromium session navigating to the mofa.go.jp HOMEPAGE (not just the target PDF) also returned HTTP 403 "Access Denied." This rules out any file-specific protection, referrer requirement, or JS-challenge-solvable mechanism — the block operates at the network edge before any page content is served, and is not solvable by any tooling available in this research environment (plain fetch, WebFetch, or a real Chromium browser).

**Resolution**: the user independently downloaded the target file (`https://www.mofa.go.jp/mofaj/files/100546568.pdf`) from a different network origin and supplied it locally (`incoming/100546568.pdf`). This task verified the file is a genuine, well-formed PDF (correct magic number, opens cleanly with `pdfinfo`/`pdftotext`, 314 pages, standard List-Creator ledger grammar confirmed on a sampled page) before locking it as `mofa-fy2024-general-account-expenditure-request`. This is the **first source in this entire research program acquired via user-provided-out-of-band delivery** rather than this repository's own fetch tooling — disclosed explicitly in both `source-lock.json`'s own `acquisitionMethod` field and this report, not silently treated as equivalent to an automated fetch. 外務省 is now in-scope, joining the List-Creator combined-ledger family.

## 10.2 Second-pass corrections (per explicit user instruction not to freeze the first pass's classifications prematurely)

`[FACT]` Two authorities were substantively re-investigated and reclassified after the user identified specific alternate entry points. See §10.7 (Failure/Learning) for the root cause of each original miss.

- **内閣官房 (CAS)**: RECLASSIFIED from "narrative-only family" to **List-Creator combined-ledger family** (split into ~17 files). The year-specific sub-page `gaisan_youkyuu_r6.html` (distinct from the general `index.html` landing page checked in the first pass) links to a genuine `令和６年度歳出概算要求額明細表` split by division, confirmed to show the identical `010 内閣官房/010 内閣官房共通費/①/01-95/内閣官房一般行政に必要な経費` opening template as case-002/003/004/005's own selected rows. The originally-found narrative overview PDF remains a separate, still-valid artifact for this authority (both exist).
- **防衛省 (MOD) and 外務省 (MOFA)**: re-attempted via the user's provided direct PDF URLs (found independently to match via web search too). **MOD succeeded** — its landing page is blocked (HTTP 403) but the direct, year-specific PDF URL returns HTTP 200 and was acquired (540 pages, standard ledger grammar). **MOFA's block was confirmed domain-wide** (the mofa.go.jp homepage itself, not just the target file, returns "Access Denied" even via a full Playwright/Chromium session), then **resolved in a third pass** via user-provided-out-of-band file delivery — see §10.2a.
- **衆議院 (Shugiin), 裁判官弾劾裁判所 (Dangai)**: RESOLVED. Both had genuine FY2024 request-stage documents, findable via web search using year-specific filename patterns not linked from the authorities' own general landing pages.
- **裁判官訴追委員会 (Sotsui)**: RESOLVED in a seventh pass (§10.2g) via a user-identified URL. The originally-acquired document (still retained as a separate artifact) remains a genuine example of the enacted-budget-stage 各目明細書 family, illustrating that one authority can host both an in-scope and an out-of-scope document simultaneously.
- **参議院 (Sangiin)**: RESOLVED in a sixth pass (§10.2d) via a user-found URL, after 5+ web searches and filename-pattern-guessing by this census's own tooling had failed.
- **国立国会図書館 (NDL)**: precisely re-characterized (not resolved) via a full listing of the authority's own current finances page: R7/R8/R9 request-stage documents are retained, R6's is not, but R6's own FINAL BUDGET document is still retained — confirming a request-stage-specific retention window distinct from (and shorter than) the final-budget retention window.

## 10.3 Observed common grammar

`[OBSERVATION]`, with counts, across the 25 in-scope authorities where the standard ledger grammar was directly confirmed on a sampled page (デジタル庁, 経済産業省, 総務省, 文部科学省, 国土交通省 from case-001–005, plus 農林水産省, こども家庭庁, 警察庁, 財務省, 人事院, 公正取引委員会, カジノ管理委員会, 内閣法制局, 内閣本府, 内閣官房, 個人情報保護委員会, 皇室費, 宮内庁, 裁判所, 会計検査院, 防衛省, 衆議院, 裁判官弾劾裁判所, and — visually, not textually — 金融庁, 法務省):

- 組織 → 項 → 経費 hierarchy: confirmed on every sampled ledger page across all 25.
- 要求番号 column: confirmed present as a column on every sampled ledger page.
- 前年度予算額 / 概算要求額 / 対前年度比較増△減 three-column amount structure: confirmed on every sampled ledger page.
- 備考 column: confirmed present (populated or visibly empty) on every sampled ledger page.
- `NNNNN-NNNN-NN-NNNN`-shaped subordinate accounting codes: directly observed in 警察庁, 法務省, カジノ管理委員会, 内閣法制局, 宮内庁 — at least **5 confirmations beyond case-004**.
- Printed page-label prefixes tied to authority identity (e.g. `農（本）`, `内（金）`, `法（本）`, `会（会）`, `皇（皇）`, `内（人）`, `防（本）`, `国（衆）`, `内（官）`): confirmed as a broadly shared convention.

This list is **not** extended to claim universality: several acquired authorities were only sampled at a single interior page (disclosed per-row in the CSV's own `familyConfidence` column).

## 10.4 Format families (provisional)

`[INTERPRETATION]` Families induced from observed features, not fixed in advance. This section supersedes the first pass's 8-family sketch — CAS is now a List-Creator-family member, not a narrative-only outlier.

1. **List-Creator combined-ledger family** — single or split PDF, Producer "List Creator", standard ledger grammar, text layer present. Largest family: デジタル庁 (unclassified pending re-integration), 経済産業省, 総務省, 国土交通省, 農林水産省, こども家庭庁, 外務省, 財務省, カジノ管理委員会, 個人情報保護委員会, 皇室費, 宮内庁, 内閣官房 (split variant, 17 files, exhaustively confirmed), 内閣本府 (extreme-split variant, ~50 files).
2. **Split-package encrypted-ledger family (4-file)** — case-004/文部科学省 alone so far. Encryption and packaging-split are shown by this census to be **independent axes**: many authorities are encrypted without a 4-file split (財務省, カジノ管理委員会, 個人情報保護委員会, 消費者庁, 内閣本府, 内閣官房), and none replicate MEXT's specific cover/summary/detail/staffing 4-way split.
3. **Cross-reference-summary family** — 国土交通省(case-005), 環境省, 消費者庁, 裁判官弾劾裁判所, 厚生労働省, 参議院, 裁判官訴追委員会: a 総表 with split 一般行政経費/その他の経費/計 amount subcolumns and an explicit page-number cross-reference into a detail section. Now confirmed in **7 authorities**, ranging from an 8-page body (sotsui) to a 1,723-page one (mhlw) — the mechanism is not correlated with authority size, and is now the single most widely-confirmed provisional family in this census after the List-Creator combined-ledger family itself.
4. **Rasterized-no-text-layer ledger family** — 金融庁, 法務省: visually identical standard ledger grammar, zero embedded fonts / zero extractable text. **Not present in any of case-001–005.**
5. **JUST-PDF-toolchain ledger family** — 内閣法制局, 裁判所, 会計検査院 (JUST PDF 3/4/5), 警察庁, 防衛省 (JUST PDF 4), 衆議院/裁判官弾劾裁判所 (via List Creator, not this family — corrected). Standard ledger grammar, text layer present.
6. **DocuWorks-toolchain family, mixed text-layer status** — 金融庁 (no text layer) and 公正取引委員会 (text layer present) — direct evidence producer alone cannot determine family.
7. **Narrative-only family (no independent ledger)** — NO LONGER any authority's sole classification (empty as of the fourth pass): both 内閣官房 (§10.2) and 厚生労働省 (§10.2b) were reclassified after being found to also publish genuine ledgers, coexisting with their own narrative materials. This family is retained as a conceptual category — a document set consisting ONLY of narrative/project-explanation content, no ledger anywhere — but this census has not yet confirmed any authority actually belongs to it exclusively.
8. **Enacted-budget-stage 各目明細書 (out of scope)** — 裁判官訴追委員会's own acquired document: a genuinely different document TYPE from every in-scope family above, structurally distinct (4-level 組織/項/事項/目 hierarchy, 要求額+積算内訳 instead of the 3-year-triple+備考 structure), correctly excluded rather than forced into an in-scope family.
9. **Not yet classified** — デジタル庁 (case-001 predates current profiling conventions, not re-derived here).

## 10.5 Outliers

`[FACT]`

- **厚生労働省 (MHLW)**: RESOLVED, no longer an outlier in the "no ledger" sense (§10.2b) — but now a notable outlier for a different reason: it is the ONLY authority in this census confirmed to publish BOTH a large family of narrative/policy-evaluation documents (10+ files) AND a separate, single-file, 1,723-page combined 総表+明細表 covering 8 organizations — the largest document in the census, and the clearest demonstration that narrative materials and a formal ledger are not mutually exclusive at the authority level.
- **金融庁 (FSA) and 法務省 (MOJ)**: rasterized/scanned, zero-text-layer ledgers.
- **内閣本府 (CAO)**: ~50-file package split, the most granular observed.
- **裁判官訴追委員会's own enacted-budget-stage document**: retained as the clearest illustration in this census that one authority can host both an in-scope request-stage document and an out-of-scope enacted-budget-stage document simultaneously, at different URLs on the same site.
- **財務省 (MOF)**: fullwidth-romanized-letter (ｉ/ｊ/ｋ) sub-item marker convention.
- **会計検査院・衆議院 (jbaudit, shugiin)**: circled-numeral sub-item marker conventions.
- **裁判官訴追委員会's own combined 各目明細書**: reveals that 衆議院/参議院/国立国会図書館/裁判官弾劾裁判所/裁判官訴追委員会 are administratively grouped as one "国会所管" (Diet jurisdiction) for enacted-budget purposes, even though several of them publish their own SEPARATE request-stage documents.

## 10.6 Failure log (revised)

`[FACT]`

| Authority | Status | Detail |
|---|---|---|
| 国立国会図書館 (NDL) | Precisely confirmed absent | Own current page retains R7-R9 request-stage docs and R6's own final-budget doc, but not R6's own request-stage doc — a request-stage-specific retention window, precisely characterized |

`[FACT]` Resolved from earlier passes: 防衛省 (direct PDF URL works despite landing-page block), 衆議院, 裁判官弾劾裁判所 (both found via web search after their general landing pages proved unhelpful), 内閣官房 (reclassified, §10.2, exhaustively re-confirmed, §10.2c), 外務省 (resolved via user-provided-out-of-band delivery after a confirmed domain-wide block, §10.2a), 厚生労働省 (major reclassification, §10.2b), 参議院 (resolved via user-found URL, §10.2d).

## 10.7 Failure/Learning: why the first pass's classifications were wrong

`[FACT]`, per explicit instruction to preserve this as a methodological finding, not merely fix it silently:

- **Root cause for CAS's original misclassification**: the first pass checked only the authority's own GENERAL landing page (`cas.go.jp/jp/yosan/index.html`), which surfaces, for the current year, only a narrative overview PDF. The genuine ledger lived at a YEAR-SPECIFIC sub-page (`gaisan_youkyuu_r6.html`) not linked from the general page in a way the first pass's navigation surfaced. **Lesson**: a ministry's own "current budget page" is not guaranteed to link every past year's own request-stage sub-page equally prominently — a general landing page returning only an overview is evidence of "this specific navigation path didn't find a ledger," not evidence "no ledger exists."
- **Root cause for MOD/MOFA's original "acquisition failure" framing being incomplete**: the first pass tested only the general landing page and concluded "WAF-consistent failure" for both. Testing the DIRECT PDF URL (once known) revealed MOD's block was landing-page-specific, not domain-wide — a meaningfully different failure mode that the first pass's single-URL test could not distinguish. **Lesson**: a landing-page 403 should be tested against a known or guessable direct-file URL before being characterized as a domain-wide block; only MOFA turned out to actually warrant that stronger characterization.
- **Root cause for Shugiin/Dangai's original "not found"**: the first pass's WebFetch of each authority's own general landing/index page did not surface a working FY2024 link (both pages emphasize later fiscal years). A targeted web search using year-specific filename conventions (learned from adjacent authorities' own naming patterns) found both. **Lesson**: "the current live page doesn't show it" and "no such document exists" are not the same claim — a targeted search for the specific expected filename pattern is a necessary additional step before concluding non-existence, not merely helpful.
- **Root cause for Sotsui's original miss and this pass's own new mistake (now corrected)**: the first pass's WebSearch query was `裁判官訴追委員会 令和6年度 予算` — a broad query that surfaced only `budget/images/r4_budget.pdf`/`r3_budget.pdf`, both labeled `各目明細書` in the search snippet ITSELF. This pass initially reused that same URL pattern (guessing `r6_budget.pdf`) without registering that the snippet's own label indicated the wrong document stage — the acquisition succeeded (HTTP 200, valid PDF) but the CONTENT was the wrong stage. This was only caught by actually reading the document's own page-1 title and comparing its table grammar against the now-well-established request-stage grammar, not by the URL or search snippet alone. **Lesson, the most important one from this task**: a successfully-acquired, well-formed PDF that matches a search query is not sufficient evidence of being in-scope — the document's own internal content (title, grammar) must be checked against the census's own explicit scope boundary (request-stage only, explicitly excluding "after the initial budget is enacted") every time, regardless of how it was found.

## 10.8 Candidate cases 006+ (preliminary, not finalized)

`[RECOMMENDATION]`, ranked per the originating task's own priority order (format diversity over authority importance) — unchanged in substance from the first pass, since none of this pass's corrections introduced a new family, only corrected family membership:

1. **金融庁 or 法務省** — rasterized-no-text-layer family, entirely unrepresented in case-001–005.
2. **環境省, 消費者庁, or 裁判官弾劾裁判所** — cross-reference-summary family, now 4 confirmed instances; selecting a row directly from this structure (rather than case-005's own 明細表-only row) would newly test the cross-reference mechanism itself. 裁判官弾劾裁判所's own 9-page document is notably the smallest in this census, offering a low-cost way to test the mechanism without a 1000+-page document's own confounds.
3. **内閣本府 or 内閣官房** — extreme/granular-split packaging (~50 and 17 files respectively), testing whether case-004's context findings hold when "the table" is fragmented across dozens of tiny files.
4. **厚生労働省** — now that a genuine ledger has been located (§10.2b), its own 1,723-page combined 総表+明細表 spanning 8 organizations is itself a strong case-006+ candidate: the largest single document in the census, testing whether context/pagination findings from case-004 hold at an even larger scale, while also uniquely offering a coexisting narrative-document family for any future, differently-scoped benchmark of that document type.

`[INTERPRETATION]` Not decided in this task. Multi-page/context-carry-over investigation across all in-scope authorities, per the originating task's own completion criteria (§18 of the originating instructions), remains outstanding before a final family/candidate determination — see §10.9.

## 10.9 Remaining scope before census completion

`[FACT]` Per the originating task's own completion criteria, this pass still does not close the census:

- **Multi-page and context-carry-over sampling** has not yet been performed for any of the 31 in-scope authorities — every acquired authority beyond case-001–005 has been sampled at only one or two interior pages, not the range needed to characterize header-repeat/context-dependency behavior per the originating task's own §8-I.
- **Format families remain provisional** (§10.4) and case-006+ selection remains preliminary (§10.8) — per the user's own explicit instruction, these are not finalized until the remaining population gaps are closed and deeper per-authority inspection is performed.

---

**This report reflects a seventh-pass, still-incomplete FY2024 all-authority format census. All 33 originally-frozen population authorities now have a closed status: 31 acquired and in-scope (source-safe tooling only — pdfinfo/pdffonts/pdftotext/pdftoppm; no compared benchmark engine; 外務省 via user-provided-out-of-band file delivery after a confirmed domain-wide block; 厚生労働省 substantively reclassified after a user-identified URL revealed a 1,723-page ledger two prior passes had missed; 内閣官房 exhaustively re-confirmed across all 17 of its own detail files; 参議院 and 裁判官訴追委員会 each resolved via user-identified URLs after this census's own search failed or found the wrong document stage), 1 precisely confirmed absent. A 34th candidate authority (復興庁) has been investigated and found categorically out of scope. No row was selected; no Ground Truth was created; no benchmark engine was run.**
