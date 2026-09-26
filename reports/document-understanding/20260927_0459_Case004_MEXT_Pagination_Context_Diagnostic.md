# case-004 MEXT Pagination / Structural-Context Diagnostic

Status: **read-only source-structure diagnostic. No benchmark run. No production change.**

Date: 2026-09-27 (Asia/Tokyo)

## Research question

> How far, and in what structural direction, must context extend from a first expense row to recover its governing item header and relevant unit evidence in this MEXT document?

This is a source-structure diagnostic, not a benchmark run or an adaptation experiment. It investigates whether case-004's missing-item-header and missing-unit findings (from the first frozen benchmark run) are isolated to the one frozen target row or reflect a recurring structural pattern within organization `010 文部科学本省`.

## Frozen state (verified, unchanged)

- Branch `research/case-004-mext-preregistration`; pre-task `HEAD` `49f5ca6`; working tree clean before this task's first command; `main` unchanged at `3b29ebd`.
- Source `mext-fy2024-general-account-expenditure-request-detail`, SHA-256 `6df221dfd22c48e0f32dd59bcf2dbcbaad19720083be43005ce700b984a6bf71` — recomputed via `shasum -a 256`, matches.
- Selection protocol (`c2b2c28`), selection record (`fa82c13`), Ground Truth (`f9b2f35`) — all re-verified byte-identical to their freeze commits.
- First frozen benchmark result (`49f5ca6`): `pdfjs-baseline` 7/11, `pymupdf-baseline` 7/11, `docling` 5/11 — re-verified byte-identical (`evidence/document-understanding/case-004-results.json`, `reports/document-understanding/case-004-evaluation.md`, and the narrative report `20260926_2127_Case004_First_Frozen_Benchmark_Run.md` all unchanged). None of these historical artifacts were rewritten by this task.

## Source

`mext-fy2024-general-account-expenditure-request-detail`, 1,339 pages, unchanged and unmodified. No re-lock performed.

For sampling purposes only, the sibling cover/TOC file (`..._01.pdf`, `令和6年度歳出概算要求額目次`, independently re-fetched, SHA-256 `91b39e9902610e13aa7be445db2d2d2a3e38166fd5f449bd11f94cfe5fe3b6d5`) was read to obtain the document's own detailed item-level table of contents — the same kind of source-safe navigational use already made of this file during the case-004 source survey. It was not locked as a case source (it isn't; `_03.pdf` remains the sole locked case-004 source) and no amount value was read from it.

## Sampling method

Restricted entirely to organization `010 文部科学本省` (per the frozen selection universe). Sample boundaries (item-header row → its first expense row) were chosen directly from the sibling TOC file's own page-number column — a source-structure criterion, not an engine outcome — deliberately spanning early, lower-middle, middle, mid-late, later, and near-the-very-end positions within the ~895-page organization, and including both same-page and cross-page examples as the TOC's own page numbers revealed them (not selected to force a particular ratio). The frozen target boundary (`①01-95`) is included as sample 1. 8 boundaries were sampled (within the requested 6–10 range); no exhaustive survey of the ~41 item headers TOC-listed under organization `010` was performed.

For each sampled boundary, only the item-header page and the first-expense page were rasterized (`pdftoppm`, 200dpi) and read directly — no OCR, no Docling/pdfjs/PyMuPDF benchmark, no `docbench`. The printed-page-to-`pdfPageIndex` offset established during Ground Truth creation (printed page 9 = `pdfPageIndex` 0) was used to locate PDF pages from the TOC's printed-page numbers, and was re-confirmed correct (via each rendered page's own printed corner label matching the TOC's stated number exactly) at every one of the 8 sampled points, spanning printed pages 10 through 903 with zero drift.

No budget amount was transcribed into this report; amounts are described only qualitatively (present / blank / self-contained), except where a raw magnitude is unavoidable context for describing a structural pattern (e.g., "0/0" to describe a genuinely zero-valued row) — no such value is Ground-Truth-relevant.

## Sample table

| # | Item (項) | Header `pdfPageIndex` (printed) | First-expense `pdfPageIndex` (printed) | Same page? | Distance | Item context repeated on expense page? | Expense row self-contained (own triple present)? | Unit visible (header pg / expense pg / neither)? |
|---|---|---|---|---|---|---|---|---|
| 1 (frozen target) | `010 文部科学本省共通費` | 1 (10) | 2 (11) | No | 1 | No | Yes | Neither |
| 2 | `020 文部科学本省施設費` | 119 (128) | 119 (128) | Yes | 0 | — (same page) | Yes | Neither |
| 3 | `030 教育政策推進費` | 121 (130) | 122 (131) | No | 1 | No | Yes | Neither |
| 4 | `060 初等中等教育振興費` | 284 (293) | 284 (293) | Yes | 0 | — (same page) | Yes | Neither |
| 5 | `140 高等教育振興費` | 463 (472) | 464 (473) | No | 1 | No | Yes | Neither |
| 6 | `280 国立大学法人施設整備費` | 677 (686) | 678 (687) | No | 1 | No | **No** (own triple blank; real amounts appear only in a subordinate `001 文教施設費` line beneath) | Neither |
| 7 | `325 国立研究開発法人日本医療研究開発機構運営費` | 798 (807) | 798 (807) | Yes | 0 | — (same page) | Yes | Neither |
| 8 | `620 国立研究開発法人海洋研究開発機構施設整備費` (near the very end of organization `010`) | 894 (903) | 894 (903) | Yes | 0 | — (same page) | Yes (values are `0`/`0`/`0`, a genuinely zero-valued row) | Neither |

## Boundary-event observations (narrative)

- **Sample 1 (frozen target)**: already fully documented in the Ground Truth evidence and first-run report; reused here unchanged, not re-inspected.
- **Sample 2**: header (`020 文部科学本省施設費`, no code, no request number, an item-level aggregate) and its first expense row (request no. `④`, code `01-95`) share one page. The expense row carries a populated 備考 (remarks) annotation (`(要旨)`/`(大学名等)` free text) — the first sampled instance of a populated remarks column, useful context for future annotation-contamination risk assessment, not evaluated further here.
- **Sample 3**: header (`030 教育政策推進費`) occupies its page alone, with no other content — the item header's page is not shared with any expense row at all. The first expense row (`⑥`, code `50-15`) appears on the very next page, with no repetition of the item header's own text on that page, and no unit text visible on either page. Structurally identical in mechanism to the frozen target.
- **Sample 4**: header (`060 初等中等教育振興費`) and its first expense row (`⑭`, code `02-15`) share one page, which also carries the tail end of an unrelated, earlier item's content in its upper half — page sharing does not imply the page is otherwise "about" only this one item.
- **Sample 5**: header (`140 高等教育振興費`) alone on its own page; first expense row (`㉘`, code `30-13`) on the next page, carrying its own triple directly plus an unusually large internal `事務事業別内訳表` breakdown sub-table (a different kind of internal richness than the frozen target's numbered sub-line-items, but a similar "the row is immediately followed by dense internal detail" pattern).
- **Sample 6**: header (`280 国立大学法人施設整備費`) alone on its own page; first expense row (`㊹`, code `01-15`) on the next page — but this row's own 前年度予算額/6年度概算要求額 cells are **visibly blank**, with a large `国庫債務負担行為` (multi-year commitment) sub-table beneath it, and the row's actual previous/current/delta figures appear only on a further-nested `001　文教施設費` line below that. This is a genuinely different self-containment failure mode than the frozen target's (whose own row does carry its triple directly) — recorded distinctly, not conflated with the header-distance question.
- **Sample 7**: header (`325 国立研究開発法人日本医療研究開発機構運営費`) and its first expense row (`56`, code `01-13`) share one page, triple present directly.
- **Sample 8**: header (`620 国立研究開発法人海洋研究開発機構施設整備費`) and its first expense row (`80`, code `01-13`) share one page, near the very end of organization `010` (organization `020` begins at the next item boundary) — triple present directly, values genuinely zero.

**No unit text (`(単位：...)`) was found on any of the 16 pages inspected across these 8 samples** (8 header pages + 8 first-expense pages, with 4 pairs collapsing to one page each since header and expense shared a page) — every one of them showed only the page-corner label and the column-header row.

## Unit context

Classified per the task's own categories: for every one of the 8 samples, unit evidence is **not observed locally** — neither the item-header page nor the first-expense page (whether the same page or different) carries `(単位：千円)` anywhere in this sample. This is consistent with, and generalizes, the frozen Ground Truth evidence's own finding for the target row specifically: the unit label is genuinely a **table-opening-only** convention for this document — printed exactly once, on the file's own true first page (`pdfPageIndex` 0, printed page 9, the page bearing the document-wide title `令和6年度歳出概算要求額明細表`), and not repeated at any subsequent item or organization boundary sampled here. No ambiguous case was found. This does not prove the label never repeats anywhere in the remaining ~1,323 unsampled pages, but across 8 deliberately varied boundaries it did not.

## Context-distance analysis

- **Same-page header count**: 4 of 8 (samples 2, 4, 7, 8).
- **One-previous-page count**: 4 of 8 (samples 1, 3, 5, 6) — in every one of these, the header occupies its own page entirely alone (no other item's content, no expense row), and the first expense row begins on the very next page with no repeated header text.
- **Farther-than-one-page count**: 0 of 8 observed.
- **Repeated/carry-forward context behavior**: never observed — in zero of the 4 cross-page samples does the expense row's own page repeat the item header's code or name.
- **Is the frozen target typical or unusual?** **Typical.** It falls in exactly the more common of the two structural patterns observed (4 of 8 samples share its "header alone on the preceding page" shape), not an outlier. The dominant open question this raises for the benchmark's own architecture is addressed in "Architecture implications" below.
- **Does unit context follow a different distance pattern than item-header context?** **Yes, and more extreme.** Item-header context is "sometimes 0 pages away, sometimes 1 page away" (roughly an even split in this sample); unit context is "always 0 additional pages away from the file's own opening page and never repeated," a categorically different (single-occurrence, document-scope, not item-scope) pattern, not merely a longer version of the same distance problem.

## Conceptual context models (A/B/C/D) — source-context sufficiency only

For each model, this counts how many of the 8 sampled boundaries **would have their item-header context available on the source pages that model defines as in-scope** — not whether any engine would actually parse or use that context correctly. No model was implemented or run.

- **A — target page only** (the current architecture): item-header context available for exactly the same-page samples: **4 of 8** (samples 2, 4, 7, 8). Unit context available for **0 of 8** (the unit label never falls on the target page itself in any sample, including the frozen target).
- **B — target + immediately previous page**: item-header context available for **8 of 8** — every cross-page sample in this diagnostic had its header exactly one page back, so this model's fixed one-page lookback would have covered all of them. Unit context remains available for **0 of 8** (the unit label is far more than one page back in every sample except none — it is always ≥1 page back from any sampled target, and in most samples very many pages back).
- **C — scan backward to nearest governing item header**: item-header context available for **8 of 8**, by construction (this model does not assume a fixed distance, so it would find the nearest header regardless of whether it is 0 or 1 pages back — within this sample, that is never more than 1). Unit context: this model is defined in terms of the nearest *item*-level header, not the table-level unit declaration, so it does not by itself guarantee unit recovery; see model D.
- **D — table/document metadata context + local structural context**: item-header context available for **8 of 8** via the same local-context reasoning as B/C; unit context available for **8 of 8**, but only because this model explicitly separates a document/table-wide metadata concept (where the once-only unit declaration genuinely lives) from page-local structural context (where the item header lives) — the two are recovered by two different mechanisms within this one model, not by the same "look nearby" logic.

**This diagnostic does not claim any of A–D would parse correctly if implemented** — only that B, C, and D would each make the necessary *source context* available for item-header recovery in this 8-sample diagnostic, while only D's explicit two-mechanism design would also make unit context available given how differently-scoped that evidence turned out to be.

## Keeping failure layers separate

Per the task's own instruction, three failure layers are kept distinct here, exactly as they were in the first frozen benchmark run:

- **Context availability** (source/document-layout fact): whether the governing item header is physically present on the page(s) a given architecture treats as in-scope. This is what this diagnostic measures.
- **Interpretation** (a different, hypothetical failure mode not observed in this diagnostic or the first run): a governing header being present on an in-scope page but not correctly recognized/associated by an engine or normalizer. Not investigated here — this diagnostic never ran an engine.
- **Extraction/table segmentation** (Docling's column-fusion artifact from the first frozen run): explicitly **not** attributed to pagination or context availability here. Docling's `previousBudget`/`fy2024Request` fusion on the frozen target's own page happened entirely within a single page's own table grid; nothing in this diagnostic's 8-sample pagination survey bears on that mechanism, and this report does not reinterpret or re-attribute it.

## Prior-case comparison (from committed evidence only, no rerun)

- **case-001**: `unit_exact_match` FAILs for all three engines in the current evaluator (`reports/document-understanding/case-001-evaluation.md`'s comparison matrix), and `state/TODO.md`'s own committed history records the reason explicitly: *"unit_exact_match correctly fails for all three engines because the 千円 label lives only on the document's earlier summary page, not on case-001's page."* This is the same **unit-context-absent-from-target-page** pattern observed throughout case-004's 8 samples, already present in the very first case of this research program — not a new phenomenon, but the first time it has been generalized beyond a single row via deliberate sampling.
- **case-001**: `item_name_present_among_candidates` **PASSes** for all three engines (same matrix) — meaning case-001's own target page did carry a genuine, on-page item-header candidate. **Established** from committed evidence: item-header context was present for case-001.
- **case-002**: `item_name_present_among_candidates` PASSes for both flat-text engines (`reports/document-understanding/case-002-evaluation.md`), and `unit_exact_match` PASSes for all three engines. case-003's own Ground Truth evidence (`fixtures/document-understanding/case-003/20260926_1618_Case003_Ground_Truth_Evidence.md`) explicitly states, comparing itself to case-002: *"Both target pages carry a page-level (単位：千円) unit label in the same position ... this matches case-002's page (which had the label)."* **Established**: item-header context and unit context were both present on case-002's own target page.
- **case-003**: `item_name_present_among_candidates` PASSes for both flat-text engines, and `unit_exact_match` PASSes for all three engines; case-003's own Ground Truth evidence directly documents visually re-verifying the unit label on its own target page. **Established**: both present.
- **Summary**: case-004 is the **first case in this research program where the item header is absent from the target's own page**, and the second (after case-001) where the unit label is absent from the target's own page. This diagnostic's 8-sample survey shows this is not a one-off accident of the frozen target row specifically, but a recurring structural feature of at least this part of MEXT's own document.

## Architecture implications (conceptual only, no schema/code change)

The evidence gathered supports treating the following as genuinely separable concepts, worth distinguishing explicitly in a future Analysis Strategy design, rather than folding all of them into "engine choice" or "extraction quality":

- **Extraction scope** (which raw page(s) an adapter reads) is currently hardcoded to exactly one page (`gt.pdfPageIndex`) for every engine, uniformly.
- **Structural context selection** (which *additional* pages, if any, are consulted to resolve a specific field like item name or unit) is currently not a concept the architecture has at all — it is implicitly always "none." The A/B/C/D comparison above suggests at least three qualitatively different context-selection strategies (`target_page_only`, `target_plus_previous`, `nearest_governing_header`) would behave differently on this specific document, and a fourth (`table_metadata_plus_local_pages`) is needed specifically because unit and item-header context in this document have different scopes (table-wide-once vs. item-local), not because either sub-problem alone is unsolved.
- **Document/layout-family interpretation** (ADR-010's existing layer) already conceptually covers "how is this document's structure organized," and this diagnostic's findings would sit naturally within that layer's remit — a document/layout-family profile could, in principle, record "this family's item headers are 0–1 pages before their first expense row" and "this family's unit declaration is table-wide-once" as source-safe structural facts, independent of which engine later tries to use them.
- **Semantic evaluation** (the existing `evaluate.mjs`) would not need to change its check *definitions* under any of B/C/D — it already compares a normalized `result` against Ground Truth regardless of how that result was assembled; only the *normalization* step's available input (which pages it may read) would differ.

No schema, adapter, normalizer, or evaluator change is proposed or implemented here. This section is intentionally conceptual, per the task's own scope limit.

## Limitations

- Only 8 of the roughly 41 TOC-listed item headers under organization `010` were sampled; the true proportion of same-page vs. cross-page boundaries across the full ~895-page organization is not established, only estimated from this deliberately varied but non-exhaustive sample.
- All 4 cross-page samples happened to have a distance of exactly 1 page; whether a distance of 2 or more ever occurs anywhere in this organization (or in organization `020` onward, entirely out of this diagnostic's scope) is unknown.
- The sibling `_01.pdf` TOC file's own page numbers were trusted as accurate; this was independently spot-checked against every sampled page's own printed corner label (8-for-8 exact matches spanning printed pages 10–903), which is strong but not exhaustive confirmation of the TOC's accuracy elsewhere in the document.
- Sample 6's blank-triple-at-the-header-row phenomenon was noticed incidentally while sampling for header distance, not searched for deliberately; whether it recurs elsewhere was not investigated.

## Unexpected findings

- Sample 6's own expense row (`①01-15`-equivalent header row for `国立大学法人施設整備に必要な経費`) has **no inline amount triple of its own at all** — a structurally distinct self-containment failure from anything seen in case-001/002/003 or in the frozen case-004 target, where the real amounts live several lines further down in a nested sub-line-item. This was not anticipated by this task's own preregistered questions and is disclosed here as a new, non-preregistered observation, not a confirmed hypothesis.
- Sample 2's populated 備考 (remarks) annotation on an otherwise structurally simple, same-page-header row is the first instance in this diagnostic of a genuinely populated remarks column within MEXT's own document family — worth keeping in mind for any future MEXT row-selection or annotation-contamination-risk work, though not investigated further here.

## Recommended next experiment

A single, still read-only follow-up: **extend this same boundary-sampling method to a small number of item headers within organization `020 文部科学本省所轄機関`** (the organization immediately following `010`, whose own boundary with `010` was incidentally confirmed in this diagnostic to fall at printed page 903/904) to check whether the same same-page/one-page-back header-distance pattern, and the same table-opening-only unit convention, generalize across organizational boundaries within this document family — still without selecting, scoring, or creating Ground Truth for any row, and still without running any engine.

Not executed in this task.
