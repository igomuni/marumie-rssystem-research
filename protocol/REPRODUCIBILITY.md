# Reproducibility

This document states, honestly, what part of the research pipeline can currently be re-run from a clean checkout of this repository, and what cannot.

## Currently reproducible

```text
primary URL
-> acquisition
-> raw binary
-> SHA-256 verification
-> page-aware PDF extraction

fixture text
-> staging
-> normalized
-> validation
```

Run from the repository root:

```bash
npm run validate            # offline, deterministic: fixture -> staging -> normalized -> validation
npm run sources:lock        # network: download registered sources, save raw binaries locally, write sources/source-lock.json
npm run sources:verify      # network: re-download each locked source and compare its SHA-256 against the committed lock
npm run sources:fetch       # network: materialize sources/raw/ from the committed lock; verifies hash/size, never writes the lock
npm run extract             # offline (once sources/raw/ is populated): deterministic page-aware PDF text extraction
npm run extraction:test     # offline: golden page-text assertions + output-hash self-check
npm run extraction:determinism  # offline: two clean extraction runs must produce identical canonical output hashes
npm run extraction:compare  # offline: classifies each historical fixture row against the extracted lines
```

`npm run validate` executes the restored `scripts/request-ingestion` PoC, which parses the curated fixture text under `scripts/request-ingestion/fixtures/`, produces staging and normalized records under `scripts/request-ingestion/out/`, and checks them against the golden totals recorded in `scripts/request-ingestion/poc-manifest.json`. It is intentionally offline and does not depend on network access, so it stays deterministic for CI and offline work.

`npm run sources:lock`, `npm run sources:verify`, and `npm run sources:fetch` are the explicit, network-dependent operations (`scripts/source-acquisition/`) that acquire and hash the two primary PDFs currently registered in `scripts/request-ingestion/source_manifest.json`. `sources:fetch` reconstructs `sources/raw/` from the committed lock on a clean checkout without ever rewriting `sources/source-lock.json`. The raw binaries are saved under `sources/raw/` (git-ignored, never committed); their SHA-256, HTTP status, size, MIME type, and redirect target are committed in `sources/source-lock.json`.

The committed SHA-256 proves whether a freshly retrieved copy of a source matches the historically locked source. It does not mean the binary itself is persisted in Git — the raw PDF is locally reproducible only for as long as the upstream government server keeps serving the locked bytes at that URL. See `same URL != same source binary` in `protocol/RESEARCH_PROTOCOL.md` and ADR-009 in `protocol/DECISIONS.md`.

`scripts/pdf-extraction/` (pinned to `pdfjs-dist@4.10.38`) turns a locked, hash-verified raw PDF into page-aware text: raw PDF.js text items with coordinates (`derived/pdf-extraction/<sourceId>.items.jsonl`), deterministically reconstructed lines (`<sourceId>.lines.jsonl`), and human-readable page text (`<sourceId>.pages.txt`). These generated files are git-ignored; only the pinned dependency, extraction code, and evidence/report artifacts are committed. Two clean extraction runs produce byte-identical canonical output hashes (verified by `npm run extraction:determinism`), and golden page-text assertions confirm known records (`財務省システム`, `厚生労働第１係` / `総務省システム`, `7,738,305`) recover on their expected pages.

## Historical fixture generation — still partial/curated

```text
locked PDF
-> deterministic extraction
-> explicit fixture-generation rules   <- NOT YET IMPLEMENTED
-> generated fixture
```

The fixtures under `scripts/request-ingestion/fixtures/` are still hand-curated excerpts from the original PDFs, not the mechanical output of the deterministic extractor. `npm run extraction:compare` measures how closely the historical fixture rows can be traced back to the locked-PDF extraction; as of this phase, all 22 normal-request fixture rows and all 3 important-policy fixture rows have an explainable source path on the expected page (12 `contiguous_reconstruction`, 7 `structured_row_match`, 3 `contiguous_delta_glyph_normalized` for the normal-request PDF; 3 `exact` for the important-policy PDF — see `evidence/pdf-extraction-fixture-comparison.json` and the Integration Validation section of `reports/workspace-phase-1d-pdf-extraction-analysis.md`). This confirms strong provenance; it does not mean fixture generation itself is mechanical. Turning "extraction recovers the fixture content" into "fixture is generated deterministically from extraction, without manual curation" is a separate, not-yet-attempted transformation.

Phase 3-15 research transformations (parent/child reconciliation, RS 5-1 flow-graph classification, allocation-mode generalization, and related analysis) are also not yet represented as executable scripts; they exist only as documented findings in `state/RESEARCH_SUMMARY.md`.

## Maturity table

```text
Layer                                      Status
------------------------------------------------------------
Primary URL registry                       reproducible
Primary binary acquisition/materialization reproducible
SHA-256 verification                       reproducible
PDF page-aware extraction                  reproducible
Historical fixture generation              partial/curated
Fixture -> staging                         reproducible
Staging -> normalized                      reproducible
Golden validation                          reproducible
Phase 3-15 transformations                 partial/manual
Report generation                          manual
```

## Workspace phase vs. research phase

See `protocol/RESEARCH_PROTOCOL.md` for the distinction between a **Research Phase** (a substantive investigation phase, currently completed through Phase 15) and a **Workspace Phase** (repository/reproducibility bootstrap work: 0, 1A, 1B, ...). This reproducibility document describes Workspace Phase progress; it does not imply that additional Research Phases have been completed.
