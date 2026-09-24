# Reproducibility

This document states, honestly, what part of the research pipeline can currently be re-run from a clean checkout of this repository, and what cannot.

## Currently reproducible

```text
fixture text
-> staging
-> normalized
-> validation
```

Run from the repository root:

```bash
npm run validate
```

This executes the restored `scripts/request-ingestion` PoC, which parses the curated fixture text under `scripts/request-ingestion/fixtures/`, produces staging and normalized records under `scripts/request-ingestion/out/`, and checks them against the golden totals recorded in `scripts/request-ingestion/poc-manifest.json`.

## Not yet reproducible

```text
primary PDF
-> downloaded binary
-> deterministic text/table extraction
-> fixture generation
```

The fixtures under `scripts/request-ingestion/fixtures/` are hand-curated excerpts from the original PDFs, not the output of an automated extraction step. There is currently no code in this repository that downloads the source PDFs, verifies their hash, or extracts text/tables from them deterministically.

Phase 3-15 research transformations (parent/child reconciliation, RS 5-1 flow-graph classification, allocation-mode generalization, and related analysis) are also not yet represented as executable scripts; they exist only as documented findings in `state/RESEARCH_SUMMARY.md`.

## Maturity table

```text
Layer                                      Status
------------------------------------------------------------
Primary URL registry                       partial
Primary binary acquisition                 not implemented
SHA-256 verification                       not implemented
PDF extraction                             not implemented
Fixture -> staging                         reproducible
Staging -> normalized                      reproducible
Golden validation                          reproducible
Phase 3-15 transformations                 partial/manual
Report generation                          manual
```

## Workspace phase vs. research phase

See `protocol/RESEARCH_PROTOCOL.md` for the distinction between a **Research Phase** (a substantive investigation phase, currently completed through Phase 15) and a **Workspace Phase** (repository/reproducibility bootstrap work: 0, 1A, 1B, ...). This reproducibility document describes Workspace Phase progress; it does not imply that additional Research Phases have been completed.
