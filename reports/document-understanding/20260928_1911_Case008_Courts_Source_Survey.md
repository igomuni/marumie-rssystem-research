# Case-008 Courts Source Survey

Status: **source survey only.** No selection protocol, row selection, Ground Truth, benchmark, OCR experiment, parser/normalizer/evaluator change, MOF linkage, or production adaptation.

Date: 2026-09-28 19:11 (Asia/Tokyo)

Branch: `research/case-008-courts-baseline`
Base: `origin/main@2adf323899eb229558fbcfe461227a32e8af20fb`

## 1. Executive summary

**SUITABLE WITH CAVEATS.** The official Courts FY2024 general-account expenditure-request source is one locked, unencrypted, A4-landscape, 127-page PDF with an intact text layer. It is emphatically **one file, not one grammar**. Direct source inspection establishes six document-level sections: cover, TOC, standard cross-reference summary, standard amount-ledger detail, a two-page staffing table separated by blank pages, and an embedded important-policy-framework summary/detail pair.

The standard ledger is a bounded eligible-universe candidate for a later protocol. The staffing table and the policy-framework sections must be treated as distinct grammars, not as header-missing ledger pages. This refines the census header-ratio framing: its core observation (pages around printed 109--111 are not missing ledger data) remains correct, but the source-safe rule is section-aware rather than a document-global header rule.

## 2. Scope and non-goals

This survey verifies source identity and document structure only. It does not choose a section or row, transcribe target amounts, create Ground Truth, compare engines, or propose a Case Package/schema change.

## 3. Canonical prior evidence reviewed

- `fixtures/document-understanding/fy2024-format-census/20260928_0642_Case006_010_Selection_Freeze.md`: Case-008 is fixed as Courts, third in the strict one-case-at-a-time sequence, with embedded multi-grammar structure as its primary axis.
- `reports/document-understanding/20260927_2110_FY2024_Census_Checkpoint_Overview.md`: recorded a single combined Courts file, a staffing-table anomaly around printed pages 109--111, blank separators, and an apparent header-ratio exception.
- `reports/document-understanding/20260928_0634_Case006_010_Selection_Rationale_Review.md`: recorded prior spot-check exposure to the staffing section and the embedded policy-framework summary.
- `reports/document-understanding/20260928_1755_Case007_NULL_Result_Structural_Review.md`: Case-007 is closed as a NULL result; its CAS hierarchy is not assumed for Courts.
- Cases 001--006 were consulted only for relevant comparison, especially Case-004/MEXT's separately packaged staffing table and its local/table-wide context distinction.

## 4. Source identity

| Field | Value |
|---|---|
| Authority / FY / stage | 裁判所 / FY2024 (令和6年度) / request |
| Title | `令和6年度一般会計歳出概算要求書等` |
| Source ID | `courts-fy2024-general-account-expenditure-request` |
| Landing URL | `https://www.courts.go.jp/about/yosan_kessan/vcmsFolder_1269/vcms_1269.html` |
| PDF URL | `https://www.courts.go.jp/vc-files/courts/2023/R06saisyutsu_gaisanyoukyusyo_720kb.pdf` |
| Raw path | `sources/raw/courts-fy2024-general-account-expenditure-request.pdf` (git-ignored) |
| SHA-256 | `df43f2dc183da84fa9952ae4c5e17888177df186ad4c556ed1a519ba584e3c06` |
| Bytes / physical pages | 736,439 / 127 |
| Lock acquisition | `plain-fetch`, HTTP 200, 2026-09-27T10:23:37.010Z |

## 5. Acquisition and integrity

The local raw binary was re-hashed in this task and exactly matches `sources/source-lock.json`. No download, lock update, registry update, or raw-binary tracking occurred. The source lock, registry, and source identity therefore remain frozen inputs.

## 6. PDF representation

`pdfinfo` reports PDF 1.4, Producer `JUST PDF 3`, creation 2023-09-04 JST, modification 2023-09-05 JST, no encryption, no rotation, A4 landscape (842 x 595pt), and no tagging. `pdffonts` identifies embedded Japanese fonts; `pdftotext -layout` yields readable Japanese table text. Native object inspection (`pdfimages -list`) shows small image/mask resources in the late policy-framework pages, not an all-raster representation. Visual render checks of representative summary, ledger, staffing, and policy-detail pages were legible.

## 7. Full-document section map

`pdfPageIndex` is zero-based; printed labels are independent source labels.

| pdfPageIndex range | Printed labels | Section / grammar | Unit | Boundary evidence |
|---|---|---|---|---|
| 0 | none | Cover / high-level contents | n/a | title lists total, detail, and staffing sections |
| 1 | none | Blank separator | n/a | native text empty; visual blank |
| 2 | `1` | Detailed TOC | n/a | maps total to 1, detail to 3, staffing to 109 |
| 3 | none | Blank separator | n/a | native text empty; visual blank |
| 4 | `裁 1` | `歳出概算要求額総表` cross-reference summary | 千円 | split general/other/total columns plus `明細書頁数` |
| 5 | none | Blank separator | n/a | native text empty; visual blank |
| 6--110 | `裁（裁）3`--`裁（裁）107` | Standard `歳出概算要求額明細表` ledger | 千円 at opening | title and full standard header at index 6; repeated header through index 110 |
| 111 | none | Blank separator | n/a | native text empty; follows ledger printed 107 and precedes staffing printed 109 |
| 112 | `裁（裁）109` | `概算要求定員表`, budget-staffing table | 人 | staffing title; personnel-change columns |
| 113 | none | Blank separator | n/a | native text empty, between staffing pages 109 and 111 |
| 114 | `裁（裁）111` | `概算要求定員表`, continued / distinct short-time reemployment table | 人 | repeated staffing title and staffing-specific header |
| 115 | no printed label observed | `重要政策推進枠要望額総表` | 千円 | title, policy headings, `明細書頁数` cross-reference column |
| 116--126 | `1`--`11` | `重要政策推進枠要望額明細表` | 千円 at opening | new title, fresh local page series, policy-framework hierarchy |

## 8. Standard-ledger grammar

The eligible standard-ledger candidate universe is **only** pdfPageIndex 6--110, subject to a later protocol's explicit rule. Its opening page declares `03 裁判所所管`, organization `010 裁判所`, then internal items such as `010 最高裁判所`, request number, `NN-NN` expense code, label, previous-year/FY2024/delta triple, and remarks. The header is `要求番号 / 事項 / 前年度予算額 / 6年度概算要求額 / 対前年度比較増△減 / 備考`; it repeats on every page in that mapped range. Nested cost/object lines and local commitment-schedule boxes occur inside ledger pages, so a later protocol must assess a physical row's own printed triple rather than infer one from descendants or boxes.

## 9. Embedded substructures

There are at least three non-ledger document grammars inside the same PDF: (1) the leading cross-reference summary, (2) the staffing table, and (3) the important-policy-framework summary/detail pair. The policy detail uses a three-value amount structure but not the standard ledger's request-number schema; it has a policy-framework hierarchy and its own fresh printed page sequence. No existing classification count was imposed on the source. Local commitment-schedule boxes inside ledger pages are additionally observed as nested, locally-unitized substructures; their full population was not separately enumerated.

## 10. Staffing table (`定員表`)

The staffing section is pdfPageIndex 112 and 114, flanked/interrupted by blank indices 111 and 113. It is titled `令和6年度概算要求定員表`, explicitly uses `（単位：人）`, and organizes rows by budget staffing / organization / item-like personnel categories rather than request-number/expense-code records. Its columns cover prior-year-end staffing, new hires, reductions, transfers, net change, FY-end staffing, and narrative calculation detail (including occupation/grade/months/person count). Organization and item-like headings appear locally, but these are personnel-table semantics, not an extension of the amount ledger.

## 11. Blank and separator pages

Indices 1, 3, 5, 111, and 113 are empty in native text and visual inspection. Their positions align with layout transitions: cover→TOC, TOC→summary, summary→ledger, ledger→staffing, and staffing-page-109→staffing-page-111. They are recorded as source blank/separator pages, **not** as missing data. Authorial intent beyond the visible placement is not asserted.

## 12. Header behavior

The census's practical conclusion is retained: the apparent Courts exceptions do not establish missing ledger headers or missing data. This survey refines the classification:

- standard-ledger header: repeats on every mapped standard-ledger page (indices 6--110);
- staffing header: a distinct personnel-table header on indices 112 and 114;
- policy-summary header: a distinct cross-reference-summary header at index 115;
- policy-detail header: a distinct policy-detail header, opening at index 116 and continuing across its local page series;
- blank pages: no header is expected.

Thus “header missing” must not be used for a page outside the standard-ledger grammar. This is a **refinement**, not a correction, of the census's embedded-staffing observation.

## 13. Organization context

For the standard ledger, `010 裁判所` is explicitly declared at its section opening (index 6), with successive internal organizational/item hierarchy below it. This is best classified as **section-scoped with local hierarchical declarations**, not CAS-style file-scoped context: the file contains several grammars, so source file identity cannot alone resolve the governing grammar or unit. For the staffing and policy sections, `(組織)裁判所` is locally printed at their own openings. A later protocol must resolve organization only within its selected section and must not carry hierarchy across a section boundary without direct evidence.

## 14. Item context

In the standard ledger, items are represented in the ledger hierarchy (internal item / request number / expense code / label) and may persist across subordinate rows and page continuation. The source establishes nearest-preceding, same-section hierarchy as a candidate context mechanism; it does **not** establish a document-global item context. The staffing and policy tables have their own row semantics and must not borrow the ledger's item rule. Exact lookback behavior at every standard-ledger page boundary remains for a later protocol to verify if it becomes selection-relevant.

## 15. Unit scope

Unit is section/local metadata, not a file-global scalar:

- standard summary and standard ledger: 千円;
- staffing table: 人;
- policy-framework summary/detail: 千円;
- local commitment schedule boxes observed within ledger pages: 百万円.

The last observation is especially important: even within the standard-ledger section, a nested calculation box can declare its own unit. A later selection protocol must bind unit to the selected row's governing table grammar, never to the file alone.

## 16. Multi-grammar boundary rules (observational)

Source-safe boundary signals are: explicit new title, fresh/local printed-page series, different header/column schema, local unit declaration, and blank separator position. The evidence supports `file identity != section identity != grammar identity != page locator`. This is an observation for Case-008 only; no schema proposal is made.

## 17. Comparison with existing cases

Case-004/MEXT publishes its staffing table as a separate sibling PDF; Courts embeds the same broad content type within a combined file. MEXT's staffing artifact cannot establish Courts semantics, but it supports the comparison that packaging is the variable here. Cases 002--006 establish familiar standard-ledger concepts, but Case-008 differs because they do not license treating a whole combined file as one selection universe. Case-007's file-scoped CAS mechanism is not observed or assumed here.

## 18. Case-008-specific findings

1. The combined PDF has a section/grammar topology that cannot safely be collapsed to one ledger.
2. The policy-framework detail starts a new local printed page sequence immediately after its own summary, despite staying in the same physical file.
3. The staffing section has an internal blank page between its two physical content pages; blank does not equal a missing personnel page.
4. Unit scope changes at both standalone sections and nested ledger boxes.

## 19. Prior exposure

Prior repository artifacts had already exposed the staffing area (around physical PDF page 113 / printed 109) and the policy summary (physical PDF page 116 / zero-based index 115 in the present map). This survey is therefore not claimed as blind. It re-verified these regions directly and expanded the full map. Standard-ledger pages were also read for structural classification; any amounts incidentally visible were not transcribed, compared, or used for selection.

## 20. Selection-protocol handoff facts

- Candidate universe: standard ledger only, pdfPageIndex 6--110, pending protocol freeze.
- Explicit exclusions pending protocol: cover/TOC, cross-reference summaries, staffing pages, policy-framework summary/detail, blank pages, and nested calculation boxes unless the protocol separately defines their role.
- Earliest standard-ledger locator: pdfPageIndex 6, printed `裁（裁）3`, organization `010 裁判所`, standard title/header.
- Context: section-scoped organization; local hierarchical item/request context; no evidence for file-global semantic carryover.
- Unit: standard-ledger row unit is 千円 at section opening, but nearby local boxes can be 百万円; section/box boundary must be honored.
- Ambiguity: exact candidate-row self-containment and page-boundary lookback are not selected or frozen here.
- Prior exposure: recorded in §19; it is non-criterion information.

## 21. Limitations and unknowns

- No row was evaluated for eligibility; the future protocol must inspect its chosen universe under predeclared rules.
- The complete population and boundaries of nested commitment-schedule boxes were not enumerated.
- This survey does not decide whether a future target should be in the standard ledger or whether the embedded policy detail can serve another research purpose; the current handoff restricts the eligible candidate suggestion to standard ledger for safety, not as a selected winner.
- No live landing-page re-fetch was required or performed; the locked binary, not a current URL response, is the verified source identity.

## 22. Suitability verdict

**SUITABLE WITH CAVEATS.** Courts is suitable for the frozen Case-008 purpose because a source-safe multi-grammar map, section boundaries, local units, and exclusions can be established before selection. The caveat is load-bearing: a protocol must choose and freeze a section-specific universe before looking for a row. It must not apply standard-ledger rules to staffing or policy-framework pages merely because they occupy the same PDF.

## 23. Recommended next task

Case-008 Selection Protocol Freeze. It should define a standard-ledger-only universe, explicit section/box exclusions, a section-aware context/unit rule, and a deterministic locator/tie-break before inspecting candidate rows. It must disclose the prior exposure noted above.

---

**No Case-008 selection protocol, row selection, Ground Truth, benchmark run, OCR experiment, parser change, normalization change, evaluator change, MOF linkage, or production adaptation was performed.**
