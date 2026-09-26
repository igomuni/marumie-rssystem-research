# TODO

## Next

- Make curated fixture generation reproducible from deterministic PDF extraction, preserving historical golden equivalence
- Define adapter interface for extraction, per document type
- Define phase manifest schema
- Define automated handoff workflow
- Add repository validation command (beyond `npm run validate`)

## Later

- Restore Phase 3-15 evidence corpus incrementally
- Convert manual transformation logic into scripts
- Build golden tests for major research totals
- Evaluate allocationMode golden cases

## Document Understanding benchmark (merged to main via PR #1)

- Resolve header-row (項 vs 目) ambiguity so `item_name_exact_match` can resolve on pages with multiple 3-digit-code rows, instead of only via the `item_name_present_among_candidates` diagnostic — still unresolved for all three engines (pdfjs, PyMuPDF, Docling) after Docling integration
- Recover the request-number column for Docling (currently `null` for case-001's target row — Docling's table structure produced no cell for that column on that specific row)
- Add a general per-page/document-level unit-label lookup (currently `unit_exact_match` correctly fails for all three engines because the "千円" label lives only on the document's earlier summary page, not on case-001's page)

## case-002 (branch: research/case-002-meti-preregistration)

- Source acquired and SHA-256-locked: the METI FY2024 general-account request PDF (`https://www.meti.go.jp/main/yosangaisan/fy2024/pdf/ippan_o.pdf`, 106 pages) was blocked by an AWS WAF JS challenge under the plain-fetch tooling, then successfully acquired via a new Playwright-based tool (`scripts/source-acquisition/browser-fetch/`). See `sources/source-lock.json` (`sourceId: meti-fy2024-general-account-request`).
- Target row frozen via the pre-registered protocol: PDF page 9 (printed `経(本) 5`), the first eligible row in 令和6年度歳出概算要求額明細表 — request no. `①`, expense code `01-95`. See `fixtures/document-understanding/case-002/20260926_0852_Case002_Selection_Record.md` for the full E1–E5 justification and inspection trail.
- Ground Truth frozen by direct visual transcription (same method as case-001): `fixtures/document-understanding/case-002/ground-truth.json`, evidence in `fixtures/document-understanding/case-002/20260926_0908_Case002_Ground_Truth_Evidence.md`. Notably, this row's delta is **positive** (`4556824`, no `△` glyph observed) — unlike case-001's negative delta.
- **First frozen out-of-sample benchmark run completed** (no code changed after seeing results): pdfjs-baseline 2/11, pymupdf-baseline 3/11, docling 2/11 — a severe regression from case-001's 8-9/11. Full analysis: `reports/document-understanding/20260926_0923_Case002_First_Frozen_Benchmark_Run.md`.
- **Next action (follow-up, not yet started):**
  1. Add a `closeCjkWrapSpaces`-equivalent step to `common.mjs`/`normalize.mjs`, verifying it doesn't regress case-001, to fix the newly-discovered asymmetry with `normalize-docling.mjs` (case-002's `item_name_present_among_candidates` diverged between pdfjs and pymupdf purely due to this gap).
  2. Investigate generalizing `splitTrailingTriple`'s trailing-anchor assumption so an annotation column following (not just wrapping after) the amount triple on the same reconstructed line doesn't break triple extraction — without reintroducing amount-similarity-as-selection-evidence risk.
  3. Investigate Docling's coarser/misaligned table grid on case-002's page (wrong-row selection reported as unambiguous — arguably worse than the flat-text baselines' honest `null`s).
  4. Revisit `evaluate.mjs`'s `delta_glyph_observed_and_associated` check, which hardcodes `expected: 'contains △'` instead of deriving it from Ground Truth's actual `deltaRaw` — it structurally cannot pass for any case whose correct delta has no glyph (case-002 included), regardless of engine correctness.
  5. Consider a `case-003`, selected via the same source-only protocol, to test whether the "annotation on the same line as the triple" pattern is common or rare across ministries.
- Do not modify case-001 Ground Truth, scores, or normalizers while doing this — case-002 tests generalization of frozen behavior.
- Consider whether `scripts/source-acquisition/src/acquire.mjs`'s missing PDF-magic-byte check (flagged during acquisition) should be backported from `browser-fetch.mjs` for consistency.
