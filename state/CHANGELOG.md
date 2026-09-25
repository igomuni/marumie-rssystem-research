# Research Workspace Changelog

## Unreleased

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
