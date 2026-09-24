# Research Workspace Changelog

## Unreleased

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
