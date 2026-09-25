# case-002 Selection Protocol (Preregistration)

Status: **frozen protocol, row not yet selected, source not yet acquired, Ground Truth not yet created.**

Date: 2026-09-26 (Asia/Tokyo)

This document defines, in advance of examining any benchmark engine's output, how the specific `case-002` row will be selected once its source PDF is acquired. It is committed before that selection happens so the choice cannot be influenced — consciously or not — by knowing how `pdfjs-baseline`, `pymupdf-baseline`, or `docling` perform on any candidate row.

## Intended source

- Ministry: 経済産業省 (METI)
- Document: 令和6年度歳出概算要求書（一般会計）(FY2024 general-account expenditure request)
- Official PDF: `https://www.meti.go.jp/main/yosangaisan/fy2024/pdf/ippan_o.pdf`
- Official landing page: `https://www.meti.go.jp/main/yosangaisan/fy2024/index.html`
- Registered (not yet locked) as `meti-fy2024-general-account-request` in `sources/source-registry.csv`.

**This source has not yet been acquired.** See `state/CHANGELOG.md` for the acquisition-failure details (AWS WAF JS challenge). Nothing in this protocol may be applied until the binary is acquired and SHA-256-locked in `sources/source-lock.json`, per `protocol/RESEARCH_PROTOCOL.md`'s source-provenance rules and ADR-009.

## Selection objective

`case-002` is an out-of-sample test of four hypotheses formed while building `case-001` (see `reports/document-understanding/case-001-evaluation.md`, `scripts/document-understanding/benchmark/src/normalize-docling.mjs`):

1. Does Docling's table-cell column separation (which resolved `expense_name_exact_match_after_line_join` on `case-001`) generalize to a different ministry's budget-request PDF?
2. Does the Docling numeric-token reversal normalization (`reconstructNumericToken` in `normalize-docling.mjs`) generalize, or was it specific to whatever produced case-001's PDF?
3. Does the CJK wrapped-label space-closing normalization (`closeCjkWrapSpaces`) generalize?
4. Does the header-row hierarchy ambiguity (`item_name_exact_match` failing for all three engines on `case-001`) behave similarly on another ministry's formal budget-request PDF, or was it an artifact specific to that page's layout?

## Avoiding selection bias

The row for `case-002` must **not** be selected because:

- Docling parses it well,
- pdf.js/PyMuPDF parse it poorly,
- it produces a desired score difference,
- it reproduces the exact `case-001` failure pattern (hierarchy ambiguity, unit-label absence, etc.) — those are *observations to make afterward*, not selection criteria,
- its expected values are especially convenient to transcribe or evaluate.

## Deterministic eligibility criteria

A row is **eligible** for `case-002` if and only if all of the following, document-semantic properties hold. These are properties visible on the page itself, independent of any extraction engine's output:

- **E1 — Correct table.** The row belongs to the formal general-account expenditure *detail* table (明細表), not the summary/total table (総表) that precedes it — the same structural distinction as `case-001` (item-level detail page, not the item-level summary-table row).
- **E2 — Native expense code.** The row is an expense-level (目) row carrying an explicit expense code in the document's own numbering scheme (analogous to case-001's `01-95`), not a bare subtotal or a header-only row with no code.
- **E3 — Multi-line wrap.** The row's item name and/or expense name visually wraps across two or more printed lines in the source PDF (this is what exercises multi-line cell reconstruction — the capability actually being tested).
- **E4 — Standard amount triple.** The row carries the document's standard three-column previous-budget / current-request / delta relationship in its native layout, structurally analogous to `case-001`, so the same benchmark fields (`previousBudget`, `fy2024Request`, `delta`, `deltaRaw`) remain meaningful and comparable.
- **E5 — Sufficiency.** The row is complete enough to populate every `case-001`-schema field that is expected to be recoverable from the page itself (i.e. not a row where the amount triple is clearly split across a page boundary or otherwise physically unrecoverable from a single page).

### Explicitly NOT an eligibility criterion: the `△` (decrease) glyph

`case-001`'s delta happened to carry a `△` (decrease) glyph incidentally — it was not selected for that reason. `case-002`'s eligibility criteria **do not** require a negative delta. If the deterministically-selected row's delta happens to be positive, `raw_delta_glyph_preserved`-successor checks (`delta_glyph_observed_and_associated`) will simply be exercised in the direction where no glyph should be observed and no glyph should be fabricated — still a valid test of the same code path (see `common.mjs`'s `parseAmountToken` / `normalize-docling.mjs`'s `reconstructNumericToken`, both of which already have dedicated tests for "no glyph anywhere means never signed negative"). If the row happens to carry `△` anyway, that is an observation, not a designed hypothesis.

### Explicitly NOT an eligibility criterion: hierarchy ambiguity

Whether the selected row's page also contains other structurally-identical `NNN <name>`-shaped rows (the source of `case-001`'s `item_name_exact_match` failure) is **not** a selection criterion. It is hypothesis 4 above, to be *observed* on whatever page the deterministic rule selects, not engineered by picking a page known in advance to have (or lack) that property.

## Deterministic final selection (tie-break)

If more than one row satisfies E1–E5, the tie-break is:

> **The earliest eligible row in document order** — lowest printed page number, then topmost eligible row position on that page (top-to-bottom reading order).

Justification: this is the simplest possible deterministic rule. It requires no scoring function, no hash-based pseudo-randomization, and no judgment call about which candidate is "most interesting" — it mirrors how a human auditor would naturally proceed through the document from the front, which is a neutral, unbiased convention rather than one tuned to produce a particular outcome.

## Avoiding circularity in row enumeration

This is the most important methodological constraint in this protocol.

`pdfjs-baseline` (reusing `scripts/pdf-extraction`'s PDF.js-based reconstruction) and `pymupdf-baseline` are two of the three engines being compared. **Using either engine's text reconstruction to enumerate or scan candidate rows for eligibility would be circular** — it would mean the selection process already "saw" one compared engine's interpretation of the document before selection was frozen, and any bias in that engine's reconstruction (e.g. which rows it renders cleanly vs. garbles) could silently influence which row looks "eligible" first. The same applies to `docling`.

Resolution (binding for the next task, when this protocol is applied):

- Eligible-row enumeration and the E1–E5 check will be performed by **direct visual inspection of the rendered PDF pages** (viewing the PDF as a human would — e.g. a PDF viewer or an image-based reading of the page), not by running any text-extraction or document-understanding tool. This is the same method already used to produce `case-001`'s Ground Truth (`groundTruthSource: "manual_visual_verification_against_locked_pdf"` in `fixtures/document-understanding/case-001/ground-truth.json`) — this protocol extends that same precedent to the *selection* step, not just Ground Truth creation.
- If a non-visual tool is ever judged necessary purely to confirm a basic structural fact (e.g. total page count, whether the PDF has a text layer at all), it must **not** be one of the three compared engines (`pdfjs-dist`, `pymupdf`, `docling`) or any other document-understanding/OCR engine, and its output must never be used to judge or rank how well an engine would parse a candidate row.
- `pdfinfo` (poppler) is acceptable for this narrow purpose (page count / basic PDF validity) precisely because it does not perform text/layout reconstruction and is not one of the compared engines.

## Selection process provenance

- **What may be inspected before freezing:** the official landing page (for document identity/context), and the rendered PDF pages themselves (visually), for the sole purpose of applying E1–E5 and the tie-break above.
- **What is prohibited before selection is frozen:** running `pdfjs-baseline`, `pymupdf-baseline`, `docling`, or `npm run docbench` against this source; running MinerU or PaddleOCR/PP-StructureV3 against it; running any OCR, LLM, or vision-based extraction intended to reveal candidate row content; running any script that scores, ranks, or filters candidate rows by predicted or actual engine success.
- **Deterministic tie-break:** earliest eligible row in document order (lowest printed page, then topmost position on that page) — see above.
- **What constitutes a protocol violation:** selecting, rejecting, or re-justifying eligibility for a row based on any engine's output; changing E1–E5 or the tie-break rule after candidate rows have already been visually identified, in a way that changes which row would be selected; running any of the prohibited engines/tools against this source before the selected row is recorded.
- **When the selected row becomes frozen:** the moment E1–E5 and the tie-break are applied and the specific row identifier (printed page + item code + expense code) is recorded in a follow-up commit to this repository. From that point, the row identity must not change based on subsequent engine performance.
- **When Ground Truth may be created:** only after the row is frozen and recorded. Ground Truth values are then transcribed by direct visual inspection of that specific, already-frozen row (same method as `case-001`), still before any engine is run against it.

## What this task did and did not do

This protocol was written and committed **before** the METI source was successfully acquired (acquisition is currently blocked — see `state/CHANGELOG.md`) and **before** any row was examined. No candidate row has been identified. No benchmark engine, OCR tool, or LLM/vision extraction has been run against any METI PDF content. `fixtures/document-understanding/case-002/ground-truth.json` does not exist yet.
