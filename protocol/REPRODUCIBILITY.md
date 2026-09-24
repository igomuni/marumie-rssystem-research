# Reproducibility

This document states, honestly, what part of the research pipeline can currently be re-run from a clean checkout of this repository, and what cannot.

## Currently reproducible

```text
primary URL
-> acquisition
-> raw binary
-> SHA-256 verification

fixture text
-> staging
-> normalized
-> validation
```

Run from the repository root:

```bash
npm run validate         # offline, deterministic: fixture -> staging -> normalized -> validation
npm run sources:lock     # network: download registered sources, save raw binaries locally, write sources/source-lock.json
npm run sources:verify   # network: re-download each locked source and compare its SHA-256 against the committed lock
```

`npm run validate` executes the restored `scripts/request-ingestion` PoC, which parses the curated fixture text under `scripts/request-ingestion/fixtures/`, produces staging and normalized records under `scripts/request-ingestion/out/`, and checks them against the golden totals recorded in `scripts/request-ingestion/poc-manifest.json`. It is intentionally offline and does not depend on network access, so it stays deterministic for CI and offline work.

`npm run sources:lock` and `npm run sources:verify` are the explicit, network-dependent operations (`scripts/source-acquisition/`) that acquire and hash the two primary PDFs currently registered in `scripts/request-ingestion/source_manifest.json`. The raw binaries are saved under `sources/raw/` (git-ignored, never committed); their SHA-256, HTTP status, size, MIME type, and redirect target are committed in `sources/source-lock.json`.

The committed SHA-256 proves whether a freshly retrieved copy of a source matches the historically locked source. It does not mean the binary itself is persisted in Git — the raw PDF is locally reproducible only for as long as the upstream government server keeps serving the locked bytes at that URL. See `same URL != same source binary` in `protocol/RESEARCH_PROTOCOL.md` and ADR-009 in `protocol/DECISIONS.md`.

## Not yet reproducible

```text
raw PDF
-> deterministic text/table extraction
-> fixture generation
```

The fixtures under `scripts/request-ingestion/fixtures/` are still hand-curated excerpts from the original PDFs, not the output of an automated extraction step. There is currently no code in this repository that extracts text/tables from the locked PDF binaries deterministically; acquiring and hashing the binary (this phase) is a separate concern from parsing its contents (a later phase).

Phase 3-15 research transformations (parent/child reconciliation, RS 5-1 flow-graph classification, allocation-mode generalization, and related analysis) are also not yet represented as executable scripts; they exist only as documented findings in `state/RESEARCH_SUMMARY.md`.

## Maturity table

```text
Layer                                      Status
------------------------------------------------------------
Primary URL registry                       reproducible
Primary binary acquisition                 reproducible
SHA-256 verification                       reproducible
PDF extraction                             not implemented
Fixture -> staging                         reproducible
Staging -> normalized                      reproducible
Golden validation                          reproducible
Phase 3-15 transformations                 partial/manual
Report generation                          manual
```

## Workspace phase vs. research phase

See `protocol/RESEARCH_PROTOCOL.md` for the distinction between a **Research Phase** (a substantive investigation phase, currently completed through Phase 15) and a **Workspace Phase** (repository/reproducibility bootstrap work: 0, 1A, 1B, ...). This reproducibility document describes Workspace Phase progress; it does not imply that additional Research Phases have been completed.
