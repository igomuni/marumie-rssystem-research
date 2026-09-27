# Case-006 法務省 (MOJ) — Source Survey

Status: **source survey only. No selection protocol, no row selection, no Ground Truth, no benchmark run, no OCR experiment. Frozen Case-006 premise (Selection Freeze `654e3c5`) confirmed, not contradicted, but materially refined on one point — see §7.**

Date: 2026-09-28 (Asia/Tokyo)

Branch: `research/case-006-moj-source-survey`, from `research/fy2024-all-authority-format-census@654e3c5`.

## 1. Executive summary

法務省's FY2024 general-account expenditure request (already acquired and locked in the census, SHA-256 re-verified byte-identical) is confirmed, via three independent methods, to have **zero extractable text and zero embedded raster images on every sampled page** — but the underlying mechanism is more specific than "rasterized/scanned": direct PDF object inspection shows every sampled page's entire visible content, including what visually reads as Japanese ledger text, is drawn using **vector path-drawing operators** (filled Bézier curves and lines), with zero font resources and zero XObject (image) resources anywhere. This is a materially different technical mechanism from a photographic scan, even though the observable symptom for a text-extraction pipeline (`pdftotext` returns nothing) is identical. This refinement does not contradict the Case-006 Selection Freeze's own premise (raster-only source representation as the primary axis remains accurate at the level the freeze itself operates), but it does sharpen what "raster-only" means for this specific authority, and this survey reports it rather than silently absorbing it into the existing "rasterized-no-text-layer" census label.

Visual inspection (no OCR) confirms the standard ledger grammar already established across the census — 組織/項/経費 hierarchy, 要求番号, `NN-NN`/`NNNNN-NNNN-NN-NNNN` codes, the three-column amount triple, 備考 — is fully present and legible when rendered, spanning 8 internal organizations across a single 737-page combined file that also contains an embedded cross-reference-summary 総表 and an embedded 定員表 (staffing table), the same "multiple grammars in one file" pattern already found in Courts (Case-008) but not previously recorded for MOJ.

## 2. Task boundary

This task performed: source-identity/SHA re-verification, PDF technical-profile inspection, raster-only verification via three independent methods, visual (non-OCR) sampling of ledger grammar and structural boundaries, and a comparison against case-001–005 and the wider census. This task did **not** perform: OCR of any kind, target row selection, selection protocol design or freeze, Ground Truth creation, any benchmark engine run (pdf.js/PyMuPDF/Docling), or any parser/normalizer/evaluator change.

## 3. Canonical source identity

- **Official landing/PDF URL**: `https://www.moj.go.jp/content/001402818.pdf` (already established in the census's own source survey; re-confirmed accessible, not re-fetched in this task).
- **Title (from the document's own cover page)**: `令和6年度歳出概算要求書`, `21 法務省所管`.

## 4. Acquisition / SHA integrity

`[FACT]` Re-verified before any inspection: the already-locked raw file's SHA-256 (`bd5ce9c5dee48b03407e9a8d4050f3992c8a515f510c0339364316448dd9cf8c`) matches `sources/source-lock.json`'s own recorded value exactly. Byte size (147,742,864 bytes) matches. **No re-download was performed** — the already-acquired raw file was reused throughout this survey, per instruction to avoid unnecessary re-fetching. No source mutation was found or suspected.

## 5. PDF technical profile

| Field | Value |
|---|---|
| Pages | 737 |
| PDF version | 1.5 |
| Producer | JUST PDF 5 |
| Creator | not recorded |
| CreationDate / ModDate | 2023-09-04 11:22:04 JST / 2023-09-04 11:24:59 JST |
| Encrypted | No |
| Page size | 595.276 × 841.89 pts (A4) |
| Page rotation | 90° (page objects are portrait-dimensioned but rotated to display landscape — a technical convention, not a genuinely portrait-native page) |
| Tagged PDF | No |

## 6. Package model

`[FACT]` **Single combined PDF**, confirmed via the document's own cover/TOC page (PDF page 1, printed `21 法務省所管`), which itself lists three internal sections with their own page references:

1. `令和6年度歳出概算要求額総表` (summary table) — printed page 1
2. `令和6年度歳出概算要求額明細表` (detail table) — printed page 5, spanning 8 organizations: `010 法務本省` (p5), `020 法務総合研究所` (p153), `040 検察庁` (p176), `050 矯正官署` (p222), `060 更生保護官署` (p464), `065 法務局` (p537), `075 出入国在留管理庁` (p625), `080 公安審査委員会` (p705), `090 公安調査庁` (p708)
3. `令和6年度概算要求定員表` (staffing/personnel request table) — printed page 729

`[OBSERVATION]` This is the **same "single file containing multiple distinct sections" pattern already found in 裁判所/Courts** (Case-008's own justification) — MOJ was not previously recorded in the census CSV as having this multi-section richness (its own `notableDifference` field only recorded the rasterized-representation finding). This survey adds that observation without altering Case-006's own frozen primary axis.

## 7. Raster-only verification methodology and findings — the survey's own central finding

Per the task's own explicit requirement, verification used three independent methods, none of which used OCR.

### Method A — standard text extraction (exhaustive)

`[FACT]` `pdftotext -layout` was run against the **entire 737-page document in one pass** (not merely sampled), splitting output on form-feed page boundaries. Result: **0 of 738 page-segments contain any non-whitespace character**. This is an exhaustive, not sampled, confirmation that `extractableText` is absent across the whole document as currently rendered by this standard tool.

### Method B — PDF object/content-stream inspection (sampled: pages 1, 100, 400, 501, 737)

`[FACT]` Using direct PDF object access (`pypdf`, not a text-extraction library call), each sampled page's own `/Resources` dictionary and decoded content stream were inspected directly:

| PDF page (1-based) | Font resources | XObject resources | Content stream size | Text-showing ops (Tj/TJ/BT) | Vector path ops (m/c/l) | Fill ops | XObject-paint (Do) | Inline image (BI) |
|---|---|---|---|---|---|---|---|---|
| 1 | 0 | 0 | 423,789 bytes | 0 | 1,095 / 7,226 / 5,502 | 563 | 0 | 0 |
| 100 | 0 | 0 | 826,437 bytes | 0 | 1,882 / 13,880 / 12,283 | — | 0 | 0 |
| 400 | 0 | 0 | 759,757 bytes | 0 | 1,818 / 12,331 / 12,391 | — | 0 | 0 |
| 501 | 0 | 0 | 499,448 bytes | 0 | 1,195 / 8,433 / 7,620 | — | 0 | 0 |
| 737 | 0 | 0 | 1,360,124 bytes | 0 | 3,384 / 22,922 / 18,803 | — | 0 | 0 |

`[FACT]` Every one of the 5 sampled pages has **zero font resources, zero XObject resources, zero text-showing operators, and zero inline images**, but a substantial (400 KB – 1.3 MB decoded) content stream consisting almost entirely of vector path-drawing operators (`m`/moveto, `c`/curveto, `l`/lineto), closed with `h` (closepath) and painted with `f` (fill).

`[INTERPRETATION]` This is the survey's own central, disclosed refinement: MOJ's visible content — including everything that visually reads as Japanese text — is drawn as **filled vector path outlines**, not as PDF text objects with font references, and not as an embedded raster/scanned bitmap image. This is a third, distinct technical mechanism from both "normal extractable text" and "scanned photographic image," even though its *symptom* for a text-extraction pipeline (zero output) is identical to a true scanned document's own symptom.

`[FACT]` **No hidden/invisible OCR text layer was found**: zero `BT` (begin-text-object) operators exist in any sampled content stream, which rules out the specific mechanism (an invisible, rendering-mode-3 `Tj`/`TJ` inside a `BT`/`ET` block) by which a hidden OCR layer would normally be represented in a PDF.

### Method C — visual render (no OCR)

`[FACT]` `pdftoppm` renders of PDF pages 1, 5, 9, 100, 153, and 400 (100 dpi) all show **crisp, fully legible Japanese ledger text and table gridlines with no scan noise, skew, or photographic artifact** — visually consistent with vector-drawn content (Method B), not with a photographic scan of a paper document. `imageResolutionEstimate` is **not applicable**: since Method B already confirmed zero XObject/image resources on every sampled page, there is no embedded raster image whose resolution could be estimated.

### Representation scope / coverage — explicitly not over-generalized

| Field | Value |
|---|---|
| `extractableText` | absent |
| `verificationCoverage` (text extraction) | **exhaustive** — all 737 pages |
| `verificationCoverage` (object inspection) | **sampled** — 5 of 737 pages |
| `verificationCoverage` (visual render) | **sampled** — 6 pages |
| `pageVisualContent` | present (confirmed via Method C) |
| `textObjectsObserved` | 0 (sampled pages) |
| `imageObjectsObserved` | 0 (sampled pages) |
| `fontResourcesObserved` | 0 (sampled pages) |
| `representationScope` | Exhaustively confirmed absent-text for **all** pages; the specific vector-path mechanism is confirmed only for the 5 object-sampled + 6 visually-rendered pages, **not proven identical on literally every one of the 737 pages** |

This distinction is deliberate: the census's own broader "rasterized-no-text-layer" family label remains accurate at the level it operates (zero extractable text), but this survey does not claim the *mechanism* (vector-outlined vs. genuinely rasterized) is confirmed beyond the pages actually sampled.

## 8. Visual ledger grammar (confirmed via rendered pages, no OCR)

`[FACT]` Every rendered ledger page shows the standard grammar already established across case-001–005 and the wider census:

- 組織 → 項 → 経費 hierarchy (confirmed, e.g., `010 法務本省 → 010 法務本省共通費 → ...`)
- 要求番号 column (circled-numeral style confirmed on the detail-table's own opening page)
- `NN-NN` expense code (`01-95`) and `NNNNN-NNNN-NN-NNNN` subordinate accounting codes (`95014-2111-02-0000`, matching the convention already seen throughout this census)
- Three-column amount structure: 前年度予算額 / 6年度概算要求額 / 対前年度比較増△減
- 備考 column, populated with detailed sub-item breakdowns and unit-cost calculation annotations (e.g., `@455,000 × 0.6 × 1.10`)
- Aggregate rows (organization- and item-level, no native code) preceding expense-level rows, matching the pattern already established in every prior case's own selection protocol
- Subordinate numbered breakdown lines beneath expense rows

## 9. Context sampling (representative, not exhaustive — per Case-006's own primary axis being representation, not context)

`[FACT]` Locators sampled: PDF page 9 (明細表 opening, printed `法（本） 5`), PDF page 100 (printed `96 法（本）`), PDF page 153 (printed `法（本） 149`, still within organization `010`), PDF page 400 (printed `396 法（矯）`, within organization `050 矯正官署`, an organization-specific printed-label prefix — `（矯）` — matching the already-established convention of organization-tied page-label prefixes seen throughout the census). Column header (要求番号/事項/前年度予算額/概算要求額/対前年度比較増△減/備考) is present and legible on every rendered ledger page sampled. This is a representative sample, not the exhaustive per-page mechanical scan performed for other in-scope authorities in the census checkpoint — consistent with the task's own instruction that Case-006's primary axis is representation, not context, and context need not be fully sampled here.

## 10. Unit behavior

`[OBSERVATION]` The 総表's own opening page (PDF page 5, printed `法 1`) shows `(単位:千円)` in its own header, matching the cross-reference-summary family's own convention already seen in mlit/env/caa/dangai/mhlw/sangiin/sotsui. This is disclosed as a structural observation; unit-scope behavior across the full 737-page document (table-section-opening only vs. embedded-box-local re-declaration, per the census checkpoint's own §3.4.2 taxonomy) was **not** exhaustively re-verified in this survey, consistent with Case-006's own primary axis.

## 11. Column-header behavior

`[OBSERVATION]` Present and legible on every one of the 6 visually-rendered pages sampled. Full mechanical per-page verification (as performed for other census authorities) was not repeated here, since the column header itself is drawn as vector paths and cannot be mechanically detected via the same text-based scan used elsewhere in the census — visual confirmation is the only available method for this authority.

## 12. Embedded/unusual structures

`[FACT]` Two structural sections beyond the standard 明細表 are confirmed present in the same combined file, per the document's own cover/TOC: an embedded 総表 (cross-reference-summary grammar, printed pages 1–4) and an embedded 定員表 (staffing/personnel request table, printed starting page 729) — the latter not visually rendered in this task, its existence confirmed only via the TOC's own page reference. This mirrors the multi-grammar pattern already found in 裁判所/Courts (Case-008), previously unrecorded for MOJ in the census's own CSV.

## 13. Comparison with case-001–005 and the wider census

| Feature | Case-006 candidate (MOJ) | Existing comparison |
|---|---|---|
| Package | Single combined file, 3 internal sections (総表/明細表/定員表) | Same single-file pattern as case-002/003/005; multi-section-in-one-file richness closer to 裁判所 (Case-008 candidate) than to any of case-001–005 |
| Orientation | A4, page-rotated-to-landscape (page objects portrait-dimensioned) | A4 landscape-native in case-001–005; MOJ's own rotation convention is a technical variant, not a different visual layout |
| Ledger grammar | Standard (組織/項/経費, 要求番号, NN-NN code, 3-column triple, 備考) | Identical grammar to case-002/003/004/005 |
| Text layer | **Absent** (vector-outlined content, no fonts/images/text-objects) | **Not present in any of case-001–005** — MOJ is the first candidate case in this program's own history to have this property |
| Producer | JUST PDF 5 | Different from case-002/003/005's own List Creator; case-004/MEXT's own sibling files also show varied producers |
| Context behavior | Sampled only (representative locators); not exhaustively verified | Not directly comparable at the same depth as case-004's own dedicated diagnostics |
| Unit behavior | Table-section-opening `(単位:千円)` confirmed on 総表's own opening page | Consistent with the majority baseline pattern found across the census |
| Embedded structures | 総表 (cross-reference-summary) + 定員表 (staffing table), both in the same file | Not present in case-001–005; structurally closer to Courts/Case-008 than to any existing case |

`[FACT]` **Source representation is the only axis that genuinely differs from case-001–005; layout (the ledger grammar itself) does not differ.** This directly answers RQ6: MOJ's visual grammar is not a new layout family — it is the same standard grammar already well-understood from case-002 onward — but its *representation* (how that grammar is encoded in the PDF) is categorically new to this research program.

## 14. Source vs. extraction boundary analysis (RQ7 / RQ12)

Per the task's own explicit requirement to keep these four categories separate:

- **Source-side fact**: the sampled ledger pages contain legible, human-readable table structure and Japanese text when rendered (Method C); the underlying PDF objects contain zero font resources, zero image resources, and thousands of vector path-drawing operators per page (Method B).
- **Extraction observation**: `pdftotext` returns empty output for all 737 pages (Method A); `pdffonts` reports zero font entries for the whole document.
- **Interpretation**: a text-based extraction pipeline (pdf.js, PyMuPDF, or Docling operating on the PDF's own text layer) has no text-object input to read at all for this source — it is not that such a pipeline would extract wrong or incomplete text, but that there is no text-bearing PDF object of any kind for it to attempt to read. This is consistent with, and gives concrete mechanical grounding to, the Selection Freeze's own framing of this as a **pipeline-applicability-boundary** question rather than a document-understanding failure.
- **Unconfirmed / left open**: whether a future OCR-based or Docling-OCR-mode strategy could recover accurate text from a rendered image of these vector-outlined pages; whether the vector-outline mechanism (as opposed to a true bitmap scan) might make some *non-OCR* recovery approach possible (e.g., a hypothetical shape-based glyph-recognition step operating directly on the vector paths, distinct from raster OCR) — this survey neither attempts nor evaluates any such approach, per its own explicit OCR prohibition.

## 15. Selection-protocol handoff facts (for a future task — not a selection protocol itself)

- **Selection universe candidate**: organization `010 法務本省`, PDF pages 9 onward (明細表's own opening), mirroring every prior case's own choice of the ministry's own headquarters organization as the selection universe.
- **First detail page locator**: PDF page 9 (0-indexed 8), printed `法（本） 5`.
- **Organization/item boundary observation**: at least one further organization boundary was TOC-referenced (`020 法務総合研究所` beginning at printed page 153) but not directly rendered in this survey.
- **Ordinary expense-row visual existence**: confirmed present on PDF page 9 itself (see §16, incidental exposure).
- **Because this authority is raster-only, any future selection protocol must rely on visual inspection exclusively** — no mechanical page-locator confirmation (e.g., the header-presence scan used for other census authorities) is possible here, since the ledger's own text is not machine-readable at all.
- **TOC/page-reference navigation aid**: the document's own cover page provides an internal page-number TOC for both 総表 and 明細表 sections, usable for structural navigation without needing OCR (the TOC page numbers were read visually in this survey, not extracted mechanically).

## 16. Incidental exposure disclosure

`[FACT]`, per the task's own explicit instruction not to treat visible rows as selection candidates: while rendering PDF page 9 (明細表's own opening page) to confirm ledger grammar, a row matching the same structural template already observed at the start of every one of case-002 through case-005's own selected rows (`010 [ministry]本省 → 010 [ministry]本省共通費 → ①/01-95/[ministry]本省一般行政に必要な経費`) was visible in the rendered image. **No amount value from this or any other row was transcribed or recorded in this report or in the accompanying evidence JSON.** This disclosure exists solely so a future selection protocol can honestly account for this prior exposure, exactly as case-005's own protocol disclosed its own analogous prior exposure — it is not a recommendation, and it does not constitute a selection.

## 17. Limitations

- Object-level (font/XObject/operator) inspection covered 5 of 737 pages, not all — the vector-outline mechanism is confirmed for those pages plus the 6 visually-rendered pages, not proven identical across literally every page.
- The 定員表 (staffing table) section's own grammar was not directly rendered or inspected in this task, only located via the document's own cover-page TOC.
- Context-carry-over behavior (organization/item continuation across page boundaries) was sampled at only a handful of locators, consistent with Case-006's own primary axis being representation rather than context.
- Whether the vector-outline mechanism is unique to MOJ or shared with other rasterized-family census authorities (e.g., 金融庁/FSA) was not investigated in this task — FSA's own object-level representation has not been re-verified against this same methodology.

## 18. Recommended next task

Per the frozen execution order (`20260928_0642_Case006_010_Selection_Freeze.md`), the next task is Case-006's own **selection protocol freeze** — applying the same source-structural, pre-registered-criteria methodology already used in case-001–005, informed by this survey's own handoff facts (§15), without re-opening the raster-only premise itself (confirmed, and refined but not contradicted, in §7). Per the Selection Freeze's own binding methodology note, the eventual first-frozen benchmark run (a separate, later task) must use the existing, unmodified three-engine pipeline, preserve a null/empty result as-is, and defer any OCR experiment to a still-later, separately-scoped task.

---

**No Case-006 selection protocol, row selection, Ground Truth, benchmark run, OCR experiment, parser change, MOF linkage, or production adaptation was performed.**
