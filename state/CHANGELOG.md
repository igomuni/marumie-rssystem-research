# Research Workspace Changelog

## Unreleased

### case-002 preregistration (branch: research/case-002-meti-preregistration)

- Attempted to acquire the METI FY2024 general-account expenditure request PDF (`https://www.meti.go.jp/main/yosangaisan/fy2024/pdf/ippan_o.pdf`) using the repository's existing plain-`fetch()`-based acquisition method. **Initial acquisition failed.** The server (CloudFront) returns HTTP 202 with `x-amzn-waf-action: challenge` and an AWS WAF Bot Control JavaScript-challenge page (a token-based `challenge.js` from `awswaf.com`) instead of the PDF, for both the PDF URL and the landing page. This requires executing JavaScript in a real browser; it is not solvable by a plain HTTP client. Confirmed persistent across repeated requests and with a browser-like `User-Agent` header; not a transient or simple-header issue.
- **Methodological finding:** `scripts/source-acquisition/src/acquire.mjs`'s `lockCommand`/`verifyCommand` only reject responses outside the `[200, 300)` status range. An HTTP `202` WAF-challenge response (as observed here) falls inside that range, so if this source had been added to the existing lock manifest and `npm run sources:lock` had been run, the tool would have silently locked the SHA-256 of the *challenge HTML page* as if it were the real PDF — a silent corruption risk. `acquire.mjs` was not modified; the new browser-fetch tool (below) independently validates the PDF magic number instead.
- Added `scripts/source-acquisition/browser-fetch/` (Node + Playwright, pinned `1.63.0`): a real headless-Chromium acquisition path for sources a plain HTTP client cannot reach. Visiting the landing page first (in the same browser context) satisfied the bot-challenge state; requesting the PDF URL cold did not. Verifies the downloaded bytes start with `%PDF-` before writing anything to `sources/source-lock.json`, refusing to lock a captured challenge/interstitial page.
- **Successfully acquired and locked** `meti-fy2024-general-account-request` via this tool: 106 pages, A4 landscape, 255,946 bytes, SHA-256 `ba64c25df327161a33c293374a7255c203cc9a527130ece848574badefbf909a` (independently reproduced twice — once in a disposable scratch test, once for the real repository lock — with identical hashes). Basic file identification only (`pdfinfo`: page count, PDF version, producer, encryption status); no text/content extraction was performed. Recorded in `sources/source-lock.json` with extra provenance fields (`acquisitionMethod: "playwright-chromium"`, `playwrightVersion`, `landingPageUrl`) and in `sources/source-registry.csv`.
- Wrote and committed the frozen `case-002` selection protocol (`fixtures/document-understanding/case-002/20260926_0834_Case002_Selection_Protocol.md`) *before* any row was examined and *before* the source was acquired: deterministic eligibility criteria (E1–E5), an explicit non-requirement of the `△` glyph and of hierarchy ambiguity as selection criteria (to avoid selecting for a known case-001 outcome), a deterministic tie-break (earliest eligible row in document order), and an explicit circularity-avoidance rule — eligible-row enumeration must use direct visual inspection of the rendered PDF, not `pdfjs-baseline`/`pymupdf-baseline`/`docling` (all three are compared engines; using any of them to scan for candidate rows would leak that engine's own interpretation into the selection).
- Confirmed: no benchmark engine, OCR tool, or LLM/vision extraction was run against any METI PDF content. No candidate row was examined or selected. `fixtures/document-understanding/case-002/ground-truth.json` does not exist.
- `case-001`'s Ground Truth, scores, and normalizers were not touched.

### Docling adapter integration (branch: research/document-understanding-benchmark)

- Added `scripts/document-understanding/adapters/docling/` (pinned `docling==2.130.0`, isolated venv), a third, structurally different engine that emits native table-cell objects (row/col/span/text) rather than flat text lines.
- Empirically verified before implementation (not assumed): Docling detected a real, borderless (no visible gridlines) table on case-001's target page — 21 rows × 14 columns, 119 cells.
- Preserved Docling's native structure in the raw artifact (`tables`/`texts`/`markdown`), not flattened to text lines, per task scope.
- Added `scripts/document-understanding/benchmark/src/normalize-docling.mjs`, a Docling-specific normalizer (the minimal interface addition this integration required) producing the same `{ result, candidates }` shape `evaluate.mjs` already consumed — `evaluate.mjs` itself required only one small, engine-agnostic fix: an `order` field (added to both normalizers) replacing an assumption that every candidate row has a `lineIndex`, which table-cell candidates don't.
- Documented and handled two genuine, general (not case-specific) Docling behaviors found via direct inspection of its cell output: (1) a wrap-induced ASCII space between two CJK characters where the printed line broke — closed deterministically; (2) multi-comma-group numeric cells assembled with their whitespace-separated groups in reversed order (verified consistent across every multi-group numeric cell checked on the page) — reversed deterministically to recover the value. Neither rule references case-001's expected values.
- Found and fixed a related false-positive: numeric/annotation cells could incidentally match the "three digits + text" item-code shape; the guard now requires an actual CJK character in the matched name, not merely "any non-digit character."
- Result: Docling scores 9/11 on `case-001` vs. 8/11 for each existing baseline. It resolves `expense_name_exact_match_after_line_join` via genuine table-cell column separation (the wrapped label and an unrelated annotation column land in different cells). It does not resolve `item_name_exact_match` (same header-row hierarchy ambiguity persists) or `unit_exact_match` (unit label absent from this page for every engine). The request-number column has no corresponding cell for the target row — recorded as `null`, not guessed.
- Extended the generated report (`reports/document-understanding/case-001-evaluation.md`) with a compact cross-engine comparison matrix (one row per check, one column per engine).
- Added 10 new unit tests for the Docling-specific normalizer (CJK-space closing, numeric-token reversal, sign-only-from-observed-glyph, no-glyph-means-never-negative, missing-request-number-is-null) — all with synthetic data using different numbers than any real case, to demonstrate the logic is general.
- `npm run validate`, `npm run extraction:test`, and both existing baseline adapters are unaffected and re-verified passing.
- PR #1 review fix: renamed the `raw_delta_glyph_preserved` evaluation check to `delta_glyph_observed_and_associated` and rewrote its note. The old name/description implied `deltaRaw` was always a single literal raw engine token; for Docling it can be a normalizer-constructed concatenation of a separate glyph-only cell and a magnitude cell. Verified by code inspection that for all three engines the `△` glyph in `deltaRaw`, when present, always originates from genuine engine raw output (never from ground truth or inference) — see `reports/document-understanding/case-001-evaluation.md`. No score changed (8/11, 8/11, 9/11 unchanged); evidence/report regenerated for consistency.

### Document Understanding Benchmark layer (branch: research/document-understanding-benchmark)

- Added `scripts/document-understanding/` as a new layer distinct from `scripts/pdf-extraction`: extraction answers "can we get text out," this layer measures "can an engine recover document structure" (reading order, multi-line cell reconstruction, row/column association).
- Added `case-001` (`fixtures/document-understanding/case-001/`): the item-020 (`情報通信技術調達等適正・効率化推進費`) detail row on PDF page index 11, with manually-verified ground truth stored separately from all engine output.
- Implemented two independent baseline adapters: `pdfjs-baseline` (reuses `scripts/pdf-extraction`'s already-locked, already-verified output) and `pymupdf-baseline` (pinned `pymupdf==1.28.2`, isolated venv, independent re-verification of the source hash).
- Implemented a generic, case-blind row parser (`benchmark/src/common.mjs`) and a strict normalize/evaluate separation: `normalize.mjs` never reads ground-truth *values* (only case config, e.g. which page), `evaluate.mjs` is the only step that reads them.
- Added root commands `docbench` and `docbench:test`.
- Ran the harness against both baselines: 8/11 checks pass for each. Both correctly fail `unit_exact_match` (the "千円" label is genuinely absent from this page) and `expense_name_exact_match_after_line_join` (both engines independently hit the same two-column-conflation artifact merging the wrapped label with an unrelated annotation heading) — failures are recorded verbatim, not repaired. `item_name_exact_match` fails because the page has four structurally-identical `NNN <name>` rows (`020`/`036`/`041`/`046`) at different hierarchy levels the harness does not yet disambiguate; a diagnostic check (`item_name_present_among_candidates`) confirms the correct row was nonetheless extracted and reconstructed correctly by both engines.
- Surveyed three external engines (Docling, MinerU, PaddleOCR/PP-StructureV3) without installing any of them; verified package availability via `pip index versions`. Recommended Docling as the next engine to integrate (see `reports/document-understanding/external-engine-survey.md`).
- `npm run validate`, `npm run extraction:test`, and the rest of the existing pipeline are unaffected and re-verified passing.

### Workspace Phase 1D — Deterministic page-aware PDF extraction

- Imported a ChatGPT-produced research/handoff bundle (`incoming/workspace-phase-1d-chat-research-bundle.zip`, SHA-256 verified) via a new local-only `incoming/` handoff directory (git-ignored).
- Added `scripts/pdf-extraction/` pinned to `pdfjs-dist@4.10.38`, turning a locked, hash-verified raw PDF into raw text items with coordinates, deterministically reconstructed lines, and page text (all generated output git-ignored under `derived/pdf-extraction/`).
- Added `sources:fetch` to `scripts/source-acquisition/` (materializes `sources/raw/` from the committed lock; verifies hash/size; never rewrites the lock).
- Added root commands `sources:fetch`, `extract`, `extraction:test`, `extraction:determinism`, `extraction:compare`. `npm run validate` remains offline and unaffected.
- Fixed three integration issues found while running the bundle locally (documented in the report): (1) the bundle's `package-lock.json` had ChatGPT-sandbox-specific `resolved` URLs — regenerated locally per the bundle's own documented fallback, `pdfjs-dist` still pinned to exactly `4.10.38`; (2) `extract.mjs` was missing `cMapUrl`/`cMapPacked`, causing 0-item extraction on the CJK-heavy request PDF — fixed; (3) `extract.mjs` recorded output paths relative to `process.cwd()` instead of `ROOT`, breaking `extraction:test` — fixed.
- Added a narrowly-scoped, general comparison rule (`compactTextIgnoringDeltaGlyph` / `contiguous_delta_glyph_normalized` match class) recognizing the `△` decrease-indicator glyph as a presentation-only sign, not fixture-specific tuning; raw extraction output is untouched.
- Ran full acceptance: source hashes match the Phase 1C lock, extraction succeeds (32 + 1 pages), golden page-text assertions pass, two clean runs produce identical canonical output hashes, and all 25 historical fixture rows (across both PDFs) classify with an explainable match method — zero unexplained `not_found`.
- Added `evidence/historical-fixture-provenance-chat-observation.json` (ChatGPT's own public-parser audit) and `evidence/pdf-extraction-fixture-comparison.json` (local deterministic result); both are preserved as distinct evidence.
- Appended an "Integration Validation" section to `reports/workspace-phase-1d-pdf-extraction-analysis.md` with actual local results.
- Historical fixtures under `scripts/request-ingestion/fixtures/` were not modified.
- Updated `protocol/REPRODUCIBILITY.md`: primary binary acquisition/materialization and PDF page-aware extraction are now reproducible; historical fixture *generation* remains explicitly marked partial/curated.

### Workspace Phase 1C — Primary source acquisition and SHA-256 lock

- Updated the Git / Commit Policy: authorized AI sessions may now commit and push directly (subject to validation and safety checks), superseding the prior manual-only policy.
- Added `scripts/source-acquisition/` (Node-built-ins only) with `lock` and `verify` commands.
- Locked the two registered Digital Agency PDFs: downloaded, hashed (SHA-256), and recorded in the new `sources/source-lock.json`.
- Added `npm run sources:lock` and `npm run sources:verify` at the repository root; `npm run validate` remains offline and unaffected.
- Reconciled `scripts/request-ingestion/source_manifest.json` and `sources/source-registry.csv` with the verified `fetchedAt`/`sha256` values from the lock.
- Added ADR-009 (source identity includes binary hash, not URL alone) and the `same URL != same source binary` invariant.
- Updated `.gitignore` so `sources/raw/*` (downloaded binaries) is excluded while `sources/raw/.gitkeep` is kept.
- Updated `protocol/REPRODUCIBILITY.md` maturity table: primary URL registry, binary acquisition, and SHA-256 verification are now reproducible.

### Workspace Phase 1B — Request-ingestion PoC restoration

- Restored the request-ingestion PoC under `scripts/request-ingestion/`, unmodified and passing (`npm test` -> `validation PASS`).
- Added root `package.json` with an `npm run validate` entry point.
- Added `protocol/REPRODUCIBILITY.md` documenting the current reproducibility boundary and maturity table.
- Added `scripts/request-ingestion/poc-manifest.json` as a machine-readable PoC manifest.
- Reconciled `source_manifest.json` with provenance fields (`mimeType`, `fetchedAt`, `sha256`, `provenanceStatus`) without fabricating unknown values.
- Registered the two Digital Agency source PDFs in `sources/source-registry.csv`.
- Updated `.gitignore` to exclude generated `scripts/request-ingestion/out/*` while keeping `.gitkeep`.
- Documented the Research Phase / Workspace Phase distinction in `protocol/RESEARCH_PROTOCOL.md`.

### Workspace Phase 1A — Research protocol/state restoration

- Imported validated research invariants from the FY2024 IT-budget investigation.
- Added durable ADRs for linkage, stage separation, zero/unknown handling, parent-child overlap, RS 5-1 interpretation, and public-repository policy.
- Added current research summary through Phase 15.
- Updated canonical state to the post-Phase-15 position.

### Workspace Phase 0 — Initialization

- Initialized research workspace structure.
