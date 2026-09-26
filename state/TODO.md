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
- **First frozen out-of-sample benchmark run completed** (`379043d`, preserved unchanged in history): pdfjs-baseline 2/11, pymupdf-baseline 3/11, docling 2/11 — a severe regression from case-001's 8-9/11. Full analysis: `reports/document-understanding/20260926_0923_Case002_First_Frozen_Benchmark_Run.md`.
- **Evaluator-overfit defect fixed and re-evaluated** (methodology correction, not engine tuning): `delta_glyph_observed_and_associated` hardcoded `expected: 'contains △'`, which could never pass for case-002's correctly-glyph-free Ground Truth. Corrected to `delta_sign_evidence_matches_source` (derives expected glyph state from Ground Truth's own `deltaRaw`, in `evaluate.mjs`). Re-evaluation: case-001 unchanged (8/11, 8/11, 9/11); case-002 up by exactly `+1` each (3/11, 4/11, 3/11). No extraction/normalization/Ground Truth changed (verified via diff). See `reports/document-understanding/20260926_1231_Case002_Evaluator_Corrected_Reevaluation.md`.
- **Next action (follow-up, not yet started) — extraction/parser failures remain unfixed:**
  1. Investigate generalizing `common.mjs`'s `splitTrailingTriple` trailing-anchor assumption so an annotation column following (not just wrapping after) the amount triple on the same reconstructed line doesn't break triple extraction — without reintroducing amount-similarity-as-selection-evidence risk. (Recommended single next experiment.)
  2. Add a `closeCjkWrapSpaces`-equivalent step to `common.mjs`/`normalize.mjs`, verifying it doesn't regress case-001, to fix the asymmetry with `normalize-docling.mjs` (case-002's `item_name_present_among_candidates` diverged between pdfjs and pymupdf purely due to this gap).
  3. Investigate Docling's coarser/misaligned table grid on case-002's page (wrong-row selection reported as unambiguous — arguably worse than the flat-text baselines' honest `null`s).
  4. Consider a `case-003`, selected via the same source-only protocol, to test whether the "annotation on the same line as the triple" pattern found on case-002 is common or rare across ministries.
- Do not modify case-001 Ground Truth, scores, or normalizers while doing this — case-002 tests generalization of frozen behavior.
- PR #2 (case-002 + Case Package checkpoint, plus the browser-fetch immutability fix) was reviewed and **merged to `main` by the user** at `f8e32ef`.
- **`acquire.mjs`'s missing PDF-magic-byte check and lock-overwrite bug: FIXED.** Both `acquire.mjs` (plain fetch) and `browser-fetch.mjs` (Playwright) now share one immutable lock-decision/mutation policy (`scripts/source-acquisition/src/lock-policy.mjs`): identical re-fetch is a no-op, mismatched re-fetch fails loudly without mutating the lock or raw file, and PDF-magic-byte validation runs before any write. Covered by 8 new tests (`scripts/source-acquisition/src/test.mjs`, injected/fixture-based, no live network). All existing locked sources (case-001 x2, METI case-002, MIC case-003 candidate) verified byte-identical before and after.

## case-003 (branch: research/case-003-mic-preregistration) — source survey only, no row selected

- MIC (総務省) FY2024 source survey complete: `fixtures/document-understanding/case-003/20260926_1443_Case003_MIC_Source_Survey.md`. Confirmed via two independently agreeing routes (MIC's own navigation + MOF's official cross-ministry link table) that the task's lead (`000897932.pdf`) is a 38-page summary-only document (byte-identical to `000898534.pdf`), and that the genuinely detailed, row-level candidate is `mic-fy2024-general-account-expenditure-request` (`https://www.soumu.go.jp/main_content/000901372.pdf`, 454 pages, A4 landscape, Producer "List Creator" — same toolchain fingerprint as case-002's METI source), containing an explicit `令和6年度歳出概算要求額明細表` starting at page 5.
- Source locked (SHA-256 `cc54dbe5f689116619a1f8453747d47bca5b960137f90869ead26954d651703b`) via plain `fetch()` (no WAF observed on `soumu.go.jp`; Playwright/browser-fetch not used) reusing the already-fixed immutable-lock logic from `browser-fetch.mjs`.
- The normal HTTP acquisition path's (`acquire.mjs`) lock-overwrite/no-PDF-validation defect (surfaced by this survey) was fixed separately — see `scripts/source-acquisition/src/lock-policy.mjs`, commit `a12ce47`. MIC's lock entry/raw file were verified byte-identical before and after that fix.
- **Row-selection protocol frozen**: `fixtures/document-understanding/case-003/20260926_1548_Case003_Selection_Protocol.md`. Selection universe: `010 総務本省` organization, PDF pages 5–245 (of 454), within `令和6年度歳出概算要求額明細表` — chosen over the entire 明細表 (pages 5–450, spans structurally distinct external-bureau organizations of unknown internal convention) and justified from the document's own table of contents. Eligibility (ME1–ME5) adapts case-002's E1–E5 (all retained, none rejected; E3's multi-line-wrap requirement re-justified as a capability-comparability criterion, not outcome-selection, since no engine has run against MIC).
- **Target row selected and frozen**: `fixtures/document-understanding/case-003/20260926_1603_Case003_Selection_Record.md`. Row: `pdfPageIndex` 8 (PDF page 9, printed `総(本) 5`), organization `010 総務本省`, item `010 総務省共通費`, request no. `①`, expense code `01-95`, `総務本省一般行政に必要な経費` — the first row passing ME1–ME5, after two rejected candidates (the `010 総務本省` organization aggregate and the `010 総務省共通費` item aggregate, both failing ME2 for lacking an expense-level code). Structurally the same pattern as case-002's own selected row (also the first `①01-95 ...一般行政に必要な経費` row under the ministry's own headquarters item header).
- **Ground Truth frozen**: `fixtures/document-understanding/case-003/ground-truth.json` + `fixtures/document-understanding/case-003/20260926_1618_Case003_Ground_Truth_Evidence.md`. Row: itemCode `010`/`総務本省共通費`, requestNo `1` (from `①`), expenseCode `01-95`/`総務本省一般行政に必要な経費`, previousBudget `38472070`, fy2024Request `41763907`, deltaRaw `"3,291,837"` (no `△`, positive), unit `千円` (page-level). Arithmetic check PASS (41,763,907 − 38,472,070 = 3,291,837). No same-page `△`-bearing row was available for cross-validation (unlike case-002); the glyph convention was instead confirmed present elsewhere in the same organization (PDF page 10, already viewed during the source survey) to rule out a rendering artifact.
- **Next action (not yet started):** run the existing benchmark engines (pdfjs-baseline, pymupdf-baseline, docling) against case-003 for the first time, unchanged, and preserve that first-run result before any adaptation — mirroring case-002's own first-frozen-run discipline.
- Not done, by design: no benchmark engine run against MIC yet, no Case Package (`document-profile.json`/`research-history.jsonl`) created for case-003 yet.

## Research architecture (design-only, not implemented — see ADR-010, ADR-011, ADR-012)

- **Case Package Reconstruction Benchmark v0: DONE.** 33/35 checklist items correctly reconstructed across case-001/case-002, zero hallucinations, critical temporal test (evaluator-correction chronology) passed cleanly in both directions. See `reports/document-understanding/20260926_1348_Case_Package_Reconstruction_Benchmark_v0_Report.md` and its 4 companion artifacts.
- **Next: v1 of the reconstruction benchmark with genuinely sandboxed isolation** (v0's isolation was instructed, not tool-access-enforced — see ADR-012). Not started.

- Design document: `reports/document-understanding/20260926_1316_Case_Based_Document_Understanding_and_LLM_Strategy_Selection_Research_Architecture.md`. Proposes Case Package / Document Profile / Analysis Strategy concepts, a document-family/layout-specific-interpretation layer, a conservative LLM strategy-selection role, a 3-level benchmark, and a leave-one-case-out evaluation protocol.
- **Phase 1 gate: DONE.** `document-profile.json` and `research-history.jsonl` backfilled for case-001 and case-002 from existing prose/commits (no new case, no strategy selection). See `fixtures/document-understanding/case-001/{document-profile.json,research-history.jsonl}` and the case-002 equivalents.
- Do not build strategy selection, retrieval, or an LLM integration before at least 3 demonstrably distinct layout families exist in the corpus (Phase 2 gate, not started).
- Schema follow-ups noted during Phase 1 backfill (not fixed, since this was backfill-only):
  1. case-001's research-history events use a coarser `result` granularity than case-002's (which distinguishes `experiment` from `result`), because case-001's history was reconstructed after the fact at lower resolution than case-002's contemporaneously-written reports. A future case created with the schema in place from the start should use `experiment` consistently for a first frozen run.
  2. ADR-011's A/B discovery-provenance rule (feature classified by how it was *actually* discovered here, not how it theoretically could be) should be re-applied whenever a new case's Document Profile is backfilled, since it is easy to default to the more convenient theoretical classification.
