# Case-010 厚生労働省 (MHLW) — Source Survey

Status: **source/document/package/context survey only**. Created 2026-09-29 06:25 Asia/Tokyo.

## 1. Executive summary

The canonical Case-010 source is one locked, native-text **1,723-page** PDF, `令和６年度歳出概算要求書（一般会計）総表・明細表`, for `25 厚生労働省所管`. Its SHA-256 was rehashed before inspection and matches the lock exactly. It is the largest single document in the FY2024 census, but it is not a multi-file package and it is not a text-layer boundary case.

The source has two principal table grammars separated by intentional blank pages: a 12-page cross-reference **総表** at `pdfPageIndex 8–19`, and a 1,703-page standard-ledger **明細表** at `20–1722`. The latter begins with `010 厚生労働本省` and spans eight TOC-declared organizations. It has the familiar request-number / matter / prior budget / FY2024 request / delta / remarks grammar and a section-opening `千円` declaration. However, its remarks region can contain extensive explanatory hierarchies and compact embedded tables, including locally declared units. Those embedded structures are not interchangeable with the primary ledger merely because they share a page.

**Suitability verdict: SUITABLE WITH CAVEATS.** A later Selection Protocol can consider the standard-ledger detail section, but must define a main-ledger versus embedded-remarks boundary, preserve section and organization provenance, and handle nonuniform header repetition and cross-page continuation without treating the file-wide unit or a visible embedded table as automatic context.

## 2. Scope and non-goals

This survey revalidated source identity, representation, section structure, context cues, unit behavior, and coverage. It did not freeze a Selection Protocol; enumerate or select candidate rows; transcribe target amounts; create Ground Truth; run a benchmark; run OCR; change a parser, normalizer, evaluator, OCR setting, source lock/registry, or production code.

## 3. Pre-task repository state

Work began from fresh `main` at `f4eaf58fba72e0098becea57dd21d0ffded330d8`, the PR #9 merge commit, after Case-009 closeout. The frozen Case-006–010 execution order makes Case-010 the final large-scale stress case. Its frozen purpose is scale, not a presumption that an embedded table is the selection target.

## 4. Canonical source identity and integrity

| field | value |
| --- | --- |
| Source ID | `mhlw-fy2024-general-account-expenditure-request-summary-detail` |
| Official URL | `https://www.mhlw.go.jp/wp/yosan/yosan/24syokan/dl/05-1b-01.pdf` |
| Title | `令和６年度歳出概算要求書（一般会計）総表・明細表` |
| Authority / FY | `25 厚生労働省所管`, FY2024 request |
| SHA-256 | `09d26048b20d1b1dac7aab236ab6da452e482a12f4d97a8f6c28ec7c420eb192` |
| Bytes / pages | 3,444,358 / 1,723 |
| Lock status | existing lock entry; local rehash PASS; no acquisition or mutation |
| Package | one combined PDF, not a package |

The authority also has separately published narrative/policy files in the registry. They are not the canonical ledger source for Case-010 and were not used here.

## 5. PDF representation and extraction-layer observations

`pdfinfo` reports PDF 1.3, List Creator, no encryption, A4 landscape (842 × 595 pt), zero rotation, created 2023-09-07. `pdffonts` reports five CID TrueType rows (including embedded/subset font entries). `pdfimages -list` reports no image rows. This is a native-text/vector-layout PDF, not a raster or vector-outline-only representation like Case-006.

`pdftotext -layout` produced non-whitespace text for 1,721 of the 1,723 actual PDF pages. `pdfPageIndex 1` and `7` are blank separators; the trailing form-feed segment is not a PDF page. This is an exhaustive text-presence observation, not a claim that plain-text extraction preserves every layout relationship.

## 6. Package and grammar map

| pdfPageIndex | printed page(s) | source-side title/grammar | handling fact |
| --- | --- | --- | --- |
| 0 | — | cover and high-level contents | not a ledger |
| 1 | — | blank separator | not missing data |
| 2–6 | 1–5 | detailed contents / locator | cross-reference/navigation grammar |
| 7 | — | blank separator | not missing data |
| 8–19 | 1–12 | `令和６年度歳出概算要求額総表` | split general/other/total amount subcolumns plus `明細書頁数`; section-opening `千円` |
| 20–1722 | 13–1715 | `令和６年度歳出概算要求額明細表` | main standard ledger; section-opening `千円`; nested remarks material exists |

The cover TOC declares eight organization starts in the detail section: `010 厚生労働本省` (printed 13 / index 20), `030 検疫所` (1220 / 1227), `040 国立ハンセン病療養所` (1248 / 1255), `045 厚生労働本省試験研究機関` (1273 / 1280), `050 国立障害者リハビリテーションセンター` (1462 / 1469), `070 地方厚生局` (1547 / 1554), `080 都道府県労働局` (1595 / 1602), and `090 中央労働委員会` (1693 / 1700). The `pdfPageIndex = printed page + 7` relation holds for both principal table sections.

No dedicated staffing-table section is listed in this source’s TOC. This distinguishes it from the separately embedded staffing sections observed in Cases 006 and 008.

## 7. Standard-ledger grammar and embedded substructures

The detail opening page (`pdfPageIndex 20`, printed `厚（本） 13`) visibly contains organization and item aggregates, request number, expense-code/matter line, the three main amount columns, delta, and a remarks column. It also contains subordinate accounting-code lines and explanatory material. Its standard-ledger table is therefore a plausible later selection-grammar candidate, but this task deliberately did not evaluate row eligibility.

Visual samples at printed 37, 1248, 1273, 1462, 1547, and 1693 show that the remarks region can host independent-looking plans, breakdown lists, and compact tables. In the printed-37 sample, a locally marked `単位：千円` table appears within a remarks area. Other samples show multiyear plans, historical execution/budget breakdowns, and personnel-related explanatory content. These observations establish **embedded substructure within the detail section**, not a document-global new unit or a second selection universe.

## 8. Context map

| context | source evidence | bounded interpretation |
| --- | --- | --- |
| File/authority | cover and main section title | file-scoped provenance only; no cross-file mechanism exists |
| Organization | TOC, organization-opening aggregate rows, and prefixes such as `厚（本）`, `厚（検）`, `厚（中）` | section/organization context is source-visible; later protocol should retain it in locators |
| Item/request/expense | main-ledger hierarchy and columns | row-local and same-page evidence exist, but continuation/subordinate material means association must be visually bounded |
| Cross-page | detail pages visibly continue detailed hierarchy; final page carries prior structural context | nearest preceding context within the same detail section may be relevant; exact rule remains unfreezed |
| Cross-file | no package split | not applicable |

Header repetition is not uniform in the visual sample: it is present at the detail opening and some organization pages, while other sampled continuation pages do not visibly repeat the full header. A later protocol must not use page index alone, or header repetition alone, as the sole grammar test.

## 9. Unit behavior

Both the summary opening (`pdfPageIndex 8`) and the main detail opening (`20`) declare `千円`. This supports section-opening scope for their respective grammars. The sampled embedded remarks tables can include a local `単位：千円` declaration. The text extraction has 94 pages containing a `単位` token, but that mechanical count is not a count of validated unit-scope declarations. It must not be treated as evidence that one file-global unit applies to every embedded structure.

## 10. Inspection coverage and prior exposure

| method | coverage | purpose |
| --- | --- | --- |
| SHA-256, `pdfinfo`, `pdffonts`, `pdfimages -list` | document-level | identity and representation |
| `pdftotext -layout` text presence | all 1,723 pages | native-text and blank-separator census |
| TOC + extracted locator map | all principal section/organization starts | section boundary and locator map |
| non-OCR visual render | pages 1, 3, 21, 45, 1222, 1228, 1256, 1281, 1470, 1555, 1603, 1701, 1723 (one-based) | cover, summary, detail opening, embedded structures, organization starts, final page |

Visual and native-text structural inspection necessarily exposed representative rows and figures, including nested tables, but no candidate order was enumerated and no amount was transcribed for a selection or Ground Truth purpose. This survey does not claim blindness.

## 11. Census classification: confirmed, refined, and not supported

**Confirmed:** the correct locked ledger is a 1,723-page single combined PDF; it contains a cross-reference summary and a large standard-ledger detail section, uses native text and List Creator, and is the census’s scale representative.

**Refined:** MHLW is not just a large standard ledger. Its detail section contains visually distinct explanatory/breakdown substructures in remarks, with local unit declarations observed in samples. Their existence matters for grammar boundaries, but does not make MHLW the primary embedded-substructure case; that role remains Courts under the Selection Freeze.

**Not supported by this survey:** a new file/package context mechanism, a raster/no-text representation mechanism, a dedicated staffing-table section, or a source-wide claim that every page has the same header or local unit behavior.

## 12. Comparison with Cases 006–009

Case-006 is also a single large combined file, but its visible ledger is vector-outline/no-text-layer; MHLW instead has a native text layer and embedded fonts. Case-007 and Case-009 required file-aware context because their sources were split packages; MHLW is one file, so cross-file inheritance is not applicable. Case-008 established explicitly separated standard-ledger, staffing, and policy grammars; MHLW has two primary sections plus embedded remarks substructures, without a TOC-listed staffing section. Relative to Cases 002–005, MHLW’s primary detail grammar is recognizably standard, while its scale and dense remarks-side material increase boundary and context risk.

## 13. Selection Protocol handoff facts (not a protocol)

- Canonical source: the already locked `05-1b-01.pdf`, identity and SHA above.
- Candidate grammar to consider: main `明細表`, `pdfPageIndex 20–1722`; no selection universe is frozen here.
- Exclusion candidates: cover/TOC, blank separators, summary grammar, and rows/tables contained in remarks-side embedded substructures unless a later protocol explicitly proves they belong to its universe.
- Context anchors: organization starts and printed-prefix family, main section title, physical `pdfPageIndex`, printed page; preserve both because the document is large.
- Unit: main detail has `千円` at section opening; do not inherit from embedded boxes or collapse all unit tokens into one file-global rule.
- Risks: nonuniform header repetition, cross-page continuations, nested rows/remarks tables, and the large section range.
- Prior exposure: representative detail content and amounts were visually exposed incidentally; no selection ranking may use that exposure.

## 14. Unresolved questions and suitability

Unresolved: the exact main-ledger boundary rule for all kinds of remarks-side embedded material; organization/item re-declaration frequency across all detail pages; the minimal safe lookback needed for cross-page continuation; and whether a later physical-row criterion is satisfiable without ambiguity in the chosen sub-universe. These are protocol-stage questions, not facts to decide here.

**SUITABLE WITH CAVEATS** for a separate Case-010 Selection Protocol Freeze. It should define a deterministic main-ledger universe and a source-side boundary rule before inspecting candidate rows.

## 15. Explicit non-actions

No Case-010 Selection Protocol, row selection, Ground Truth, benchmark run, separate OCR experiment, parser/normalizer/evaluator change, source-lock/registry change, MOF linkage, or production adaptation was performed.
