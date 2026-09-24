# Research Workspace Changelog

## Unreleased

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
