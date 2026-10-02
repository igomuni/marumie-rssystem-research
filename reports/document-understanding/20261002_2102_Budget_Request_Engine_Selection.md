# Budget Request Document Understanding — Engine Selection Re-evaluation

Date: 2026-10-02 (Asia/Tokyo)
Branch: `research/budget-request-engine-selection` (from `687787c`)
Evidence: `evidence/document-understanding/20261002_2102_engine-selection-probe-results.json`
Probe set: `fixtures/document-understanding/engine-selection/probe-pages.json`
Hierarchy GT (evaluation only): `fixtures/document-understanding/engine-selection/mhlw-hierarchy-ground-truth.json`
Probe/analysis scripts: `scripts/document-understanding/engine-selection/src/`
Raw native outputs: `derived/document-understanding/engine-selection/` (generated, not committed)

## 0. Answer in one paragraph

On these born-digital ledgers, pdf.js and PyMuPDF return **the same glyphs, in the same content-stream order, at the same run granularity**, deterministically. Neither one is better for the token layer, so switching engines buys nothing. Docling (2.130.0, native `DoclingDocument`, OCR on or off) gives a usable row×column grid on one page type, the 総表. It loses or fuses structure on the TOC, on detail pages and on METI. It reverses comma groups on every page and costs 1.6–3.4 GB RSS. It does **not** provide the evidence that the custom layers produce, and it does not replace them. The remaining hard problem is **document-level hierarchy across pages** (目次 / 総表 / 明細). It is not page-local layout, and no engine tested solves it. Every engine's output contains what is needed to solve it (labels, code shapes, x-indent, page refs). Recommendation: **keep** the pdf.js SourceToken → TableGeometry → LogicalRow foundation. **Pause** the page-local interpretation layers (SpatialRegion … PageTemplate). **Do not adopt** Docling/MinerU/Paddle now. Next, measure document-level hierarchy reconstruction from the document's own index structures, scored against TOC GT.

## 21.1 Current state

- **marumie-rssystem (main `2f83491`)**: Pipeline V2 extraction PoC on pdfjs-dist 5.4.296 (`disableNormalization: true`). Layers: SourceToken → TableGeometry → LogicalRow → SpatialRegion → RegionRelation → SemanticRecordCandidate → RecordAnchor → PageTemplateObservation (#355–#362). All are evidence-only observations on 4 Golden pages. None is scored against a ground truth.
- **marumie-rssystem-research**: benchmark harness with pdfjs-baseline (4.10.38), pymupdf-baseline (1.28.2, flat `get_text("text")`) and docling (2.130.0) adapters. There are 10 frozen cases scored by an 11-check evaluator. This evaluation does not depend on, and is not part of, any other research track.
  - Background only: when it started, a separate research branch (Batch-001) was in progress. It is not merged into `main`, and this report neither relies on it nor changes it.
  - The next research question comes from this evaluation alone: document-level hierarchy / cross-page context reconstruction (§21.9–21.10).

## 21.2 Problem definition (from the real PDFs)

The measurements below separate four sub-problems:

1. **Glyph/token acquisition** — solved by every engine on these pages. △, ASCII `-` in codes, fullwidth digits and box-drawing glyphs all come through (§21.5).
2. **Value assembly** — the PDFs draw each comma group of an amount as its own text run (`17,` `396,` `623`). METI draws them right-to-left in the content stream. Whole amounts need a deterministic, geometry-based join. Every engine needs this step (Docling does it wrongly).
3. **Row / column association on a page** — geometry rows (same baseline) are clean on 総表 and detail pages for pdf.js/PyMuPDF. Docling is right on 総表 and wrong on TOC, detail pages and METI.
4. **Document hierarchy (組織→項→要求→費目) across pages** — the unsolved part. Detail pages encode level as x-indent and code shape. 総表 lists 組織/項/要求 rows with page references. The TOC gives the full tree. A request's parent 項 can sit on an earlier page or above an intervening history table (p1555). Research cases 001–010 already showed this: flat-text engines failed only `item_name_exact_match` (ambiguity/context). Docling failed earlier, at table/row association.

## 21.3 Existing research findings (cited, not re-run)

| case | pdfjs / PyMuPDF / Docling (of 11) | relevant observation |
| --- | --- | --- |
| 001 Digital | 8 / 8 / 9 | Docling separates annotation column, reverses comma groups, puts △ in its own cell, drops request-number cell |
| 002 METI p9 | 4 / 4 / 3 | regression on out-of-sample page |
| 003 MIC, 005 MLIT, 009 CAO | 10 / 10 / 3–10 | Docling variable |
| 006 MOJ | 2 / 2 / 2 | vector-outline text (no text layer) |
| 008 Courts, 010 MHLW | 10 / 10 / 3 | flat text fails only unique item resolution; Docling fails at table/row association (010: one 99-cell table, merged item material) |

`item_name_exact_match` fails for every engine on every case, so hierarchy context is the common failure. The external-engine survey (`external-engine-survey.md`, 2026-09-26) is six days old. It was not refreshed from the web.

## 21.4 Engine capability matrix

Measured on 8 pages (case-001 p12, METI p9, MHLW p1268/p1555/p7-TOC/p19-総表/p1603, MEXT p876). `—` = not measured; `?` = unknown.

| capability | current custom (pdf.js + layers) | pdf.js 4.10.38 / 5.4.296 | PyMuPDF 1.28.2 | Docling 2.130.0 | MinerU | Paddle |
| --- | --- | --- | --- | --- | --- | --- |
| glyph fidelity | = pdf.js | complete; = PyMuPDF on all pages | complete (reference) | 95.1–100% chars; content duplicated on p1555; `－`→`-` on p19 | ? | ? |
| raw sign preservation (△) | yes, no inference | yes | yes | yes (count doubled on p1555 by duplication) | ? | ? |
| bbox fidelity | derived from transform + style ascent/descent | origin + width; height from font matrix | per-char/span/line/block bbox + origin | per text item/cell bbox; no per-token bbox | ? | ? |
| font/style metadata | font id only | font id, generic family, ascent/descent | font name (mojibake: `lr¾©`/`lrSVbN` for ＭＳ明朝/ゴシック), size, flags, color | none in document model | ? | ? |
| reading order | raw + visual kept separately | content-stream order | content-stream order (sort=False) = pdf.js | model order; TOC collapsed into one cell | ? | ? |
| physical row reconstruction | yes (TableGeometry) | needs grouping | `lines` group only same-run spans; needs grouping | rows on 総表 only | ? | ? |
| comma-group amount join | yes | needs join | needs join | joins but **reverses** groups (7/7 pages with comma amounts) | ? | ? |
| multi-line reconstruction | continuation candidates | needs logic | needs logic | joins wraps in cell text with spaces | ? | ? |
| table-region detection | SpatialRegion candidates | none | none (no `find_tables` measured) | always 1 table/page | ? | ? |
| cell boundaries | none (columns by gaps) | none | none | yes, wrong on TOC/detail/METI | ? | ? |
| row/column association | geometry, page-local | — | — | good on 総表; lost on TOC (0/5 rows); multi-row merge on METI | ? | ? |
| two-column separation (TOC) | not tested | 28 column switches in native order; recoverable by x | same as pdf.js | none (left column = one cell) | ? | ? |
| hierarchy/header distinction (page) | indent clusters + page-local stack | labels/x available | labels/x available | fuses 組織/項/要求 in one cell (p1603, p1555) | ? | ? |
| document-level hierarchy | not addressed | — | — | — | ? | ? |
| cross-page context | not addressed | — | — | — | ? | ? |
| MEXT right-side calculation | region/relation candidates | rows clean by geometry | rows clean by geometry | per-row cells present (cols 7–9) | ? | ? |
| provenance | token ids, bbox, raw text | item index | block/line/span/char path | `self_ref`, prov bbox, charspan | ? | ? |
| reversibility to source | yes | yes | yes | partial (normalized/merged text) | ? | ? |
| determinism | yes | 2 runs byte-identical; v4 = v5 byte-identical; normalized = raw text | 2 runs byte-identical | 2 runs byte-identical; OCR on = off | ? | ? |
| runtime (8 pages) | — | 0.53 s | 0.31 s | 21.3 s no-OCR (0.45–9 s/page incl. model load); OCR roughly 2× | ? (survey: slower, GPU-favoring) | ? |
| memory | — | 216 MB RSS | 72 MB | 1.6 GB (no-OCR) / 3.4 GB (OCR) | ? (survey: multi-GB models) | ? |
| Mac M4 feasibility | yes | yes | yes | yes (CPU) | ? (survey: weak) | ? (survey: arm64 wheel unverified) |
| Node integration cost | native | native | Python subprocess | Python + torch subprocess | Python + models | Python + paddlepaddle |
| license | — | Apache-2.0 | **AGPL-3.0 or commercial** | MIT (docling, docling-ibm-models); RapidOCR Apache-2.0 | (survey: Apache-2.0) | ? |

## 21.5 Golden sample observations

**Glyphs.** The pdf.js and PyMuPDF counts of △, ▲, U+2010/2011/2212, ASCII `-`, fullwidth `－` and fullwidth digits are equal on all 8 pages. Request codes come out as ASCII `01-95` in all three engines. The U+2011 seen earlier in `pdftotext` output is a poppler artifact. Docling keeps every glyph class, but duplicates text on p1555 (△ 14 vs 7, box-drawing 753 vs 377) and maps one `－` to `-` on p19.

**Amounts.** On every page with comma amounts, the share of amounts that appear whole inside one native unit is identical for pdf.js items, PyMuPDF words and PyMuPDF spans (0 on METI/総表, 0.01 on p1603, 0.11 on case-001, 0.61–0.94 elsewhere). Measured that way, the token layer cannot tell pdf.js from PyMuPDF. METI p9 runs `916` `599,` `234,` (= 234,599,916) in that order in both engines, with x restoring the order. Docling outputs `916 599, 234, 243, 345 924, 45, …`: reversed groups, and several rows merged into one cell.

**MHLW hierarchy (GT: TOC p7, 11 nodes: 組織 070/080, 項 010/011/012/010, 要求 186–189/195).**

- **TOC p7**: grouping pdf.js or PyMuPDF units into geometry rows per column, then applying a generic label stack (`（組織）NNN` / `（項）NNN` / `NNN NN-NN name page`), places **5/5 requests with code and parent correct** in both engines. Docling puts the entire left column into one cell and the request numbers and page numbers into two other single cells. The same stack recovers **0/5**. Caveat: the GT was transcribed from this same page, so this measures TOC extraction fidelity. It is not independent evidence of hierarchy inference.
- **総表 p19**: geometry rows read cleanly, e.g. `186 · 01-95 · 地方厚生局一般行政に必要な経費 · 13, · 893, · 142 · … · 1547`. 組織 and 項 names are letter-spaced (one run per character). Docling's grid is correct here: one row per 組織/項/要求, with request number, code+name, amounts and page in separate columns. It is the one page type where Docling's structure is as good as geometry rows, and its amounts are still reversed (`388 28,`).
- **Detail p1555 / p1603**: level is printed as x-indent: 組織 code x=51.8, 項 code 58.7, 要求番号 36.2 with code 65.6, 費目 72.5/79.4. On p1555 a five-year history table sits between 項 010 (y=69) and request 186 (y=424). Docling fuses `080 都 道 府 県 労 010 都道府県労働局共通費 195 01-95` into one cell on p1603 and `070 地 方 厚 010` on p1555.
- **marumie-rssystem PageTemplate on p1555** (existing main output): clean indentation clusters (51.765 / 58.666 / 65.569) and 4 hierarchy relation candidates. 070→010 is observed; 010→186 is not, because the history table intervenes and the request number sits left of the 組織 column. This is a page-local limit, not a threshold issue.

**MEXT p876 right side.** Geometry rows give `１．事業選定審査謝金 · 14,260 6 2 · @ 円 人 回 · 171 · ( · 171 · )`: the operands and the unit labels are separate runs on the same baseline. Docling yields per-row cells for the right columns. Neither engine produces the formula structure. That is project semantics.

**case-001 p12.** Docling's output shape (21×14, 119 cells) matches the research-recorded observation. Nothing changed between Docling runs or versions.

## 21.6 Current custom pipeline assessment

| layer | assessment | basis |
| --- | --- | --- |
| SourceToken (rawText, bbox, raw vs visual order, no sign inference, unknown≠zero) | **valuable, engine-independent** | Every engine needs this contract. pdf.js already matches PyMuPDF content exactly. |
| TableGeometry (gap clustering, value-run join) | **valuable** | Comma-group join and right-to-left run order are required for all engines; Docling gets them wrong. |
| LogicalRow (physical rows, continuation) | **valuable** | Geometry rows are clean on 総表/detail pages. Continuation is needed for wrapped names (p19). |
| SpatialRegion / RegionRelation | **unproven** | No GT check. Docling's table regions are not better on these pages, so this is not a re-implementation of a working library feature. It is also not shown to be needed. |
| SemanticRecordCandidate / RecordAnchor | **unproven, overlaps project semantics** | Page-local. The research flat-text normalizer already reaches 10/11 on native-text cases. |
| PageTemplateObservation | **observed limit** | Indent clusters correct, but hierarchy relations are page-local and miss 010→186 on p1555. The real hierarchy needs cross-page evidence. |

## 21.7 Library assessment

- **pdf.js (Apache-2.0, Node-native)**: 4.10.38 and 5.4.296 are byte-identical on all items. `disableNormalization` does not change text on these pages. No per-char bbox, and the font name is an internal id. It is enough for the token layer as built.
- **PyMuPDF (AGPL-3.0/commercial, Python)**: same content and order as pdf.js. Adds true per-char bbox, font size/flags/color, and 3× lower memory. `blocks`/`lines` group only same-run spans, so they do not replace row grouping or value join. The AGPL license and Python boundary are real costs for a public Node project. Adopting it is justified only if per-char bbox becomes a measured need.
- **Docling (MIT, Python+torch)**: the native document model gives text items with prov bbox/charspan, and tables with row/col/span cells. Hierarchy/grouping (`groups`) is empty on all 8 pages. Its structure is reliable only on grid-like 総表 pages. OCR (default) adds time and memory with zero output change on born-digital pages. Markdown export was not evaluated, because the native model already shows the structural loss.
- **MinerU / PaddleOCR PP-StructureV3**: not measured. They are OCR-centric, multi-model and heavier than Docling (survey, 2026-09-26). Their strength (scanned pages) is not this corpus's problem, except for vector-outline sources like case-006. They are unknown on every capability axis.

## 21.8 Architecture alternatives

| | strengths | weaknesses / risks | migration cost |
| --- | --- | --- | --- |
| **A. Current custom** (pdf.js → geometry → custom DU) | deterministic, provenance-complete, Node-native; foundation measured equal to PyMuPDF | layers 4–8 page-local and ungraded; risk of more interpretation layers without a GT signal | none |
| **B. PyMuPDF foundation** | richer metadata, char bbox, low memory | same content as A; AGPL; Python boundary; still needs value join/rows/hierarchy | rewrite token layer + subprocess; no measured gain |
| **C. Docling + provenance adapter** | real table cells on 総表; MIT | reversal, multi-row merge, level fusion, TOC collapse, char loss up to 4.9%, content duplication; 1.6–3.4 GB; adapter would mostly repair Docling | high, plus repair rules (forbidden style) |
| **D. Hybrid** (tokens + Docling observations) | Docling grid could cross-check 総表 rows | on the only page type where Docling is right, geometry rows are already clean, so the cross-check adds cost, not information | medium-high; no measured benefit |

## 21.9 Recommendation

```text
KEEP:
  SourceToken provenance model (rawText, bbox, raw/visual order, no sign inference, unknown != zero)
  pdf.js as token engine (= PyMuPDF content on all probes; Node-native; Apache-2.0)
  TableGeometry value-run join and LogicalRow physical rows/continuation

PAUSE:
  Extension of SpatialRegion / RegionRelation / SemanticRecordCandidate / RecordAnchor / PageTemplate
  (no DocumentTemplateObservation, RecordAnchorRefinement, FieldResolver until a GT-scored need exists)

REPLACE:
  Nothing. Docling/PyMuPDF do not replace any custom layer on measured evidence.

EXPERIMENT NEXT (one):
  MHLW document-level hierarchy reconstruction from the document's own structures.
  Use the existing pdf.js SourceToken/LogicalRow output of the 総表 pages and the
  detail-page header rows. Apply generic rules: code shape NNN vs NN-NN, 組織/項 label or
  x-indent, page reference. Score 組織→項→要求 parent edges and start pages against the TOC
  GT (evaluation only, never input). Add 080/010/195 and one other ministry's 総表-equivalent
  as out-of-sample checks.
```

## 21.10 Stop condition

- If the experiment recovers the TOC-GT parent edges and start pages from 総表 + detail headers (pdf.js tokens only), main repo work continues on A-trimmed. The next PR is a document-level hierarchy observation layer. Paused layers stay frozen.
- If it fails because the token/row evidence is missing (not because of rule design), return to engine selection: measure PyMuPDF `rawdict` char bbox, and Docling only on 総表-type pages.
- If 総表-equivalent structures are absent in other ministries, record the hierarchy as page-local and context-limited, and do not tune rules to MHLW.

## 22. Self-review of past decisions

- **Why the custom layers were added.** Each layer followed an instruction to observe the next structural level. Every step was justified as "observation, not interpretation". None was gated on a GT-scored need.
- **Were the research benchmarks consulted?** Not sufficiently. During #355–#362 the research repo was not read. Cases 001–010 already showed two things. First, flat pdf.js/PyMuPDF text recovers row labels and amounts (10/11 on native-text cases). Second, the shared failure is hierarchy/context (`item_name_exact_match`). That pointed to document-level hierarchy, not to more page-local geometry.
- **Was an existing library re-implemented?** Mostly no. No tested engine provides correct value joins or row/level association on these ledgers. The one overlap is minor: PyMuPDF `lines` partly overlaps TableGeometry row grouping, for same-run spans only.
- **Was going as far as PageTemplate justified?** Weakly. Its indent clusters are correct, but it stayed page-local. On the first hierarchy case it misses the 010→186 edge, and it adds about 110 KB of ungraded observation per page. The agent did not flag this, although project rules ask it to point out a request that looks mis-directed.
- **When to return to engine selection.** After LogicalRow (#357). The value/row foundation existed then, and the open question (hierarchy/context) was already visible in the research evidence. A GT-scored hierarchy check should have come before SpatialRegion.

## Negative findings and limitations

- 8 pages, 3 ministries plus Digital. They are not a corpus sample. All pages are born-digital (vector-outline sources were not probed).
- Character coverage uses PyMuPDF `rawdict` as the reference. pdf.js = 1.0 against it shows agreement, not independent truth.
- Name-presence counts on detail/総表 pages are per native unit and under-count letter-spaced names. Geometry rows contain the full names (shown in §21.5). The counts are reported but not used for conclusions.
- The TOC 5/5 result is circular with the TOC-derived GT (extraction fidelity only).
- Docling was run only in its default layout/table configuration (± OCR). No TableFormer mode, image scale or backend variations were tried (an untested alternative, not a tuning target).
- PyMuPDF `find_tables()` and `get_text(sort=True)` were not measured.
- The main-repo PoC CLIs were not re-run on TOC/総表/p1603. Only the existing p1555 PageTemplate output was inspected.
- MinerU/Paddle remain unmeasured. Licenses come from installed package metadata. Model-weight licenses were not checked.

## Reproduce

```bash
node scripts/document-understanding/engine-selection/src/probe-pdfjs.mjs scripts/pdf-extraction/node_modules/pdfjs-dist v4-run1
node scripts/document-understanding/engine-selection/src/probe-pdfjs.mjs <marumie-rssystem>/node_modules/pdfjs-dist v5-run1
scripts/document-understanding/adapters/pymupdf-baseline/.venv/bin/python scripts/document-understanding/engine-selection/src/probe_pymupdf.py run1
scripts/document-understanding/adapters/docling/.venv/bin/python scripts/document-understanding/engine-selection/src/probe_docling.py run1 no-ocr
scripts/document-understanding/adapters/docling/.venv/bin/python scripts/document-understanding/engine-selection/src/probe_docling.py run1 default
node scripts/document-understanding/engine-selection/src/analyze.mjs > derived/document-understanding/engine-selection/analysis.json
```
