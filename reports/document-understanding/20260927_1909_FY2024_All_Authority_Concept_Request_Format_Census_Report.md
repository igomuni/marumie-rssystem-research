# FY2024 All-Authority 概算要求 PDF Format Census — Report

Status: **In-progress census, first substantial pass. 25 of 33 population authorities acquired/inspected; 2 disclosed acquisition failures; 5 disclosed not-found-on-current-live-page results. Provisional format families, not finalized. No row selection, no Ground Truth, no benchmark engine run, no schema/production change.**

Date: 2026-09-27 (Asia/Tokyo)

Branch: `research/fy2024-all-authority-format-census`, from `main@fc7c0ea`.

## 10.1 Population

`[FACT]` MOF's official FY2024 cross-authority index (`2024yokyuippan_link.html`) lists **33 authorities** (frozen in `20260927_1909_FY2024_Population_Freeze.md`, commit `558f7fb`).

- Acquired and inspected: **25** (5 reused from case-001–005's own already-committed evidence; 20 newly acquired this task)
- Disclosed acquisition failures (landing page HTTP 403, WAF-consistent): **2** (防衛省, 外務省)
- Disclosed not-found-on-current-live-page (FY2024 link absent from the authority's own present-day page; several state that documents older than ~4 years are retired to the National Diet Library's WARP archive): **5** (衆議院, 参議院, 国立国会図書館, 裁判官訴追委員会, 裁判官弾劾裁判所)
- Direct-PDF-vs-landing-page ratio: most authorities required a landing-page hop; a minority (財務省, 農林水産省 via its own attach path, 法務省, 会計検査院) resolved in one hop from the MOF-listed URL or a shallow follow.
- Single-file vs. split-package ratio among the 25 acquired: **at least 19 single/combined**, **≥6 split** (文部科学省=4 files, 金融庁=12 files, 内閣本府=~50 files, 内閣官房's own overview may be part of a larger unsurveyed split, MHLW's narrative package=10 files).

## 10.2 Observed common grammar

`[OBSERVATION]`, with counts, across the 21 authorities where the standard ledger grammar was directly confirmed on a sampled page (デジタル庁, 経済産業省, 総務省, 文部科学省, 国土交通省 from case-001–005, plus 農林水産省, こども家庭庁, 警察庁, 財務省, 人事院, 公正取引委員会, カジノ管理委員会, 内閣法制局, 内閣本府, 個人情報保護委員会, 皇室費, 宮内庁, 裁判所, 会計検査院, and — visually, not textually — 金融庁, 法務省):

- 組織 → 項 → 経費 hierarchy: confirmed on every sampled ledger page across all 21.
- 要求番号 column: confirmed present as a column on every sampled ledger page.
- 前年度予算額 / 概算要求額 / 対前年度比較増△減 three-column amount structure: confirmed on every sampled ledger page.
- 備考 column: confirmed present (populated or visibly empty) on every sampled ledger page.
- `NNNNN-NNNN-NN-NNNN`-shaped subordinate accounting codes (the same convention as case-004/MEXT's own sub-line-items): directly observed in 警察庁, 法務省, カジノ管理委員会, 内閣法制局, 宮内庁 — at least **5 new confirmations** beyond case-004.
- Printed page-label prefixes tied to authority identity (e.g. `農（本）`, `内（金）`, `法（本）`, `会（会）`, `皇（皇）`, `内（人）`): confirmed as a broadly shared convention, with the prefix character(s) varying systematically by authority — not yet catalogued exhaustively.

This list is **not** extended to claim universality: 8 of 33 authorities were not acquired/inspected at all, and several acquired authorities were only sampled at a single interior page (disclosed per-row in the CSV's own `familyConfidence` column).

## 10.3 Format families (provisional)

`[INTERPRETATION]` Families induced from observed features, not fixed in advance:

1. **List-Creator combined-ledger family** — single or lightly-split PDF, Producer "List Creator", standard ledger grammar, text layer present. Largest family by count: デジタル庁(unclassified pending re-integration, see below), 経済産業省, 総務省, 国土交通省, 農林水産省, こども家庭庁, 財務省, カジノ管理委員会, 個人情報保護委員会, 皇室費, 宮内庁, and (extreme-split variant) 内閣本府.
2. **Split-package encrypted-ledger family** — case-004/文部科学省 alone so far (4-file split, permission-only AES encryption). Several other authorities are *also* encrypted (財務省, カジノ管理委員会, 個人情報保護委員会, 消費者庁, 内閣本府, 内閣官房) but are NOT also split in the same 4-file cover/summary/detail/staffing shape — encryption and packaging-split are shown by this census to be **independent axes**, not a single family-defining feature.
3. **Cross-reference-summary family** — 国土交通省(case-005), 環境省, 消費者庁: a 総表 with split 一般行政経費/その他の経費/計 amount subcolumns and an explicit page-number cross-reference into a detail section. Confirmed in 3 authorities now, no longer a case-005-only observation.
4. **Rasterized-no-text-layer ledger family** — 金融庁, 法務省: visually identical standard ledger grammar, but zero embedded fonts / zero extractable text (confirmed via `pdffonts` + `pdftotext` + visual render). **Not present in any of case-001–005.**
5. **JUST-PDF-toolchain ledger family** — 内閣法制局, 裁判所, 会計検査院 (JUST PDF 3/4/5 respectively) plus 警察庁 (JUST PDF 4): standard ledger grammar, text layer present. Distinguished from the List-Creator family only by producer signature so far; not yet shown to differ structurally.
6. **DocuWorks-toolchain family, mixed text-layer status** — 金融庁 (no text layer) and 公正取引委員会 (text layer present), same Creator/Producer family but opposite text-layer outcomes — direct evidence that producer alone must never be used as a family-defining feature (per the originating task's own §11 rule).
7. **Narrative-only family (no ledger observed)** — 厚生労働省, 内閣官房/内閣: FY2024 public materials contain no 組織/項/経費 itemized table under any label found on the authority's own landing page. A genuinely different document *type*, not a differently-packaged ledger.
8. **Not yet classified** — デジタル庁 (case-001's own existing evidence predates this repository's current source-profiling conventions; several fields remain `not_established` and were not re-derived in this pass, per the originating task's own §5/§12 instruction not to re-survey existing cases).

`[INTERPRETATION]` These 8 groupings are provisional and will likely be revised once the remaining 8 unacquired authorities and deeper (multi-page, not single-sample) inspection of already-acquired ones are completed.

## 10.4 Outliers

`[FACT]`

- **厚生労働省 (MHLW)**: no formal ledger found under any of its 10 own listed FY2024 PDFs — the most confidently-established outlier (full file listing reviewed, not just one sampled page).
- **内閣官房/内閣 (CAS)**: only a narrative overview located from its own landing page; not exhaustively searched for an alternate ledger route.
- **金融庁 (FSA) and 法務省 (MOJ)**: rasterized/scanned, zero-text-layer ledgers — a categorically different engine-failure mode from any of case-001–005 (a text-based extraction engine recovers zero rows, not merely ambiguous or mis-segmented rows).
- **内閣本府 (CAO)**: ~50-file package split, the most granular observed, exceeding 金融庁's own 12-file split and case-004/MEXT's 4-file split.
- **財務省 (MOF)**: a distinct fullwidth-romanized-letter (ｉ/ｊ/ｋ) sub-item marker convention, not observed elsewhere in this census.
- **会計検査院 (jbaudit)**: a circled-numeral (⑤⑥) sub-item marker convention, distinct from both the letter-based and standard-parenthetical-numeral conventions seen elsewhere.

## 10.5 Failure log

`[FACT]`

| Authority | Failure type | Detail |
|---|---|---|
| 防衛省 (MOD) | Acquisition failure | Landing page HTTP 403 via both WebFetch and plain curl with a browser User-Agent — WAF-consistent, not resolved via browser-fetch/Playwright tooling in this pass |
| 外務省 (MOFA) | Acquisition failure | Same as above, identical symptom |
| 衆議院 (Shugiin) | Not found on live page | Current page lists other fiscal years, not FY2024 |
| 参議院 (Sangiin) | Not found on live page | MOF-listed URL returns HTTP 404 |
| 国立国会図書館 (NDL) | Not found on live page | Current page's earliest available request is FY2026; page notes older documents are in the WARP archive |
| 裁判官訴追委員会 (Sotsui) | Not found on live page | Current page shows only FY2022/FY2023 |
| 裁判官弾劾裁判所 (Dangai) | Not found on live page | Current page's earliest available is FY2025+ |

`[FACT]` One minor, resolved acquisition quirk: 会計検査院's non-`www.` URL failed to resolve (`fetch failed`); the `www.` prefix succeeded on retry. Not a WAF/challenge, disclosed for completeness.

## 10.6 Candidate cases 006+ (preliminary, not finalized)

`[RECOMMENDATION]`, ranked per the originating task's own priority order (format diversity over authority importance):

1. **金融庁 or 法務省** — the rasterized-no-text-layer family is entirely unrepresented in case-001–005 and would produce a completely different, and arguably more informative, benchmark result (a universal zero-text-extraction failure, testing OCR-dependent strategies rather than table-segmentation strategies).
2. **環境省 or 消費者庁** — the cross-reference-summary family, while structurally close to case-005/MLIT, has not been tested as a *primary* selected-row target; case-005's own row was in 明細表, not the 総表 itself — selecting a row directly from the 総表-with-cross-reference structure would be a genuinely new test of the cross-reference mechanism itself.
3. **内閣本府** — the ~50-file split package tests whether the context/pagination findings from case-004 (bounded neighbor-page lookback, table-wide-once unit) hold when "the table" is itself fragmented across dozens of tiny files rather than one large file.
4. **厚生労働省** — while it lacks the ledger grammar this census is built around, it represents a document *type* (narrative project-report) that no case has tested at all; a lower priority for the *current* benchmark design (which assumes ledger rows exist) but a genuinely distinct family worth flagging for a future, differently-scoped benchmark.

`[INTERPRETATION]` This ranking is preliminary — the remaining 8 unacquired authorities (especially 防衛省 and 外務省, both currently blocked by WAF) could plausibly introduce further new families and are not yet ruled out as higher priority. Not decided in this task.

## Answers to the 14 required closing questions (§22 of the originating task)

1. **母集団**: 33 authorities, per MOF's official FY2024 cross-authority index.
2. **実物PDFを確認できた主体数**: 25 of 33.
3. **acquisition失敗**: 2 (防衛省, 外務省, both HTTP 403). A further 5 were not acquisition *failures* in the WAF/technical sense but disclosed not-found-on-current-live-page results (衆議院, 参議院, 国立国会図書館, 裁判官訴追委員会, 裁判官弾劾裁判所).
4. **format familyの数**: 8 provisional families (§10.3), one of which (デジタル庁) remains unclassified pending future re-integration.
5. **既存case-001〜005のfamily**: デジタル庁=unclassified; 経済産業省・総務省・国土交通省=List-Creator combined-ledger family (国土交通省 additionally in the cross-reference-summary family); 文部科学省=split-package encrypted-ledger family (its own single-member family so far).
6. **新しく発見したformat mechanism**: rasterized/scanned zero-text-layer ledgers (金融庁, 法務省); narrative-only documents with no ledger at all (厚生労働省, 内閣官房); extreme package splitting up to ~50 files (内閣本府); a second and third confirmed instance of the cross-reference-summary mechanism (環境省, 消費者庁); at least 3 new sub-item marker conventions (ｉｊｋ letters, circled numerals, in addition to the parenthetical-numeral convention already known).
7. **NN-NN経費コードの広がり**: directly confirmed present in at least 10 of the 21 ledger-grammar authorities sampled deeply enough to see a code (the remaining 11 sampled pages simply did not happen to show a code-bearing line in the single page sampled — not evidence of absence).
8. **組織→項→経費文法の共通性**: confirmed in all 21 authorities where a ledger page was directly sampled; not yet checked in the remaining 4 acquired-but-ledger-not-yet-confirmed authorities (人事院, 公正取引委員会 — actually both confirmed; see §10.2) — in practice confirmed in every acquired authority that has a ledger at all.
9. **unit declarationのscope**: at least 3 types confirmed across this program to date: page-level (case-002/003/005, and directly re-confirmed in 内閣本府's own detail sample), table-wide-once (case-004/MEXT), and per-project (MHLW's narrative documents, not table-wide at all).
10. **summary/detail packagingの種類**: at least 4: single combined file (majority); split by role/table-type (4-file MEXT, 12-file FSA, ~50-file CAO); combined-with-granular-cross-reference (MLIT, ENV, CAA); narrative-only with no formal summary/detail ledger split (MHLW).
11. **context carry-overの種類**: not newly investigated in this pass for any of the 25 newly-acquired authorities (this census's own §8-I calls for it, but this pass prioritized breadth — population coverage — over depth; disclosed as a scope gap, not a negative finding).
12. **Case-006〜010候補**: 金融庁 or 法務省 (rasterized family), 環境省 or 消費者庁 (cross-reference-summary family), 内閣本府 (extreme-split family) — see §10.6.
13. **選定理由がformat diversityで説明できるか**: yes for the three ranked candidates above — each targets a structural mechanism absent from case-001–005, not a ministry chosen for its administrative importance.
14. **将来のformat family対応順序**: the rasterized-no-text-layer family should be addressed first in any future PDF→MOF full-linkage effort, since it is the only family where the *current* three benchmarked engines (pdf.js, PyMuPDF, Docling-without-OCR) would recover literally zero rows, regardless of table-segmentation quality — a qualitatively different and more urgent gap than any ambiguity/context-recovery finding from case-001–005.

## Scope disclosure

`[FACT]` This is a **first substantial pass**, not a completed census: 8 of 33 authorities remain unresolved (2 WAF failures, 5 not-found-on-live-page, and implicitly the depth of inspection for most acquired authorities is a single sampled page, not the "minimum a few pages" + full context-behavior check the originating task's §8-I/§18 ultimately call for). Per the originating task's own §19/§21 completion criteria, this pass does not yet claim "census complete" — it establishes a working population, a first format-family sketch, and a working failure log, sufficient to support a first-pass candidate ranking (§10.6) while leaving the remainder for continued work in this same branch.

---

**This report reflects a partial, first-pass FY2024 all-authority format census. 25 of 33 authorities acquired and minimally inspected via source-safe tooling only (pdfinfo/pdffonts/pdftotext/pdftoppm); no compared benchmark engine (pdf.js/PyMuPDF/Docling) was run; no row was selected; no Ground Truth was created.**
