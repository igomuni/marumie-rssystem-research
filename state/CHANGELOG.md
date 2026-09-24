# Research Workspace Changelog

## Unreleased

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
