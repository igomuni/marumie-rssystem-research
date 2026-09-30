# Current Handoff

Last completed Research Phase: 15
Workspace Phase: 1D (deterministic page-aware PDF extraction, hash-verified against the Phase 1C lock)

Current focus:
Batch-001 Wave 1 repaired S3 v2 reviewed; execution v3 required

Next action:
Execute a separately versioned S3 repair v3 while preserving v1/v2. The v2 review accepted its locator, scope, local/nested cluster, and direct-ID corrections but found unsupported outer-ledger row-pattern evidence and an A02 local-unit-anchor graph/manifest mismatch. Normalization remains unauthorized.

Read first:
- START_HERE.md
- protocol/RESEARCH_PROTOCOL.md
- protocol/DECISIONS.md
- protocol/REPRODUCIBILITY.md
- state/CURRENT_STATE.json
- state/RESEARCH_SUMMARY.md
- reports/workspace-phase-1d-pdf-extraction-analysis.md (see "Integration Validation" section for actual local results)

Reproducibility checks:
```bash
npm run validate              # offline: fixture -> staging -> normalized -> validation
npm run sources:lock          # network: acquire + hash-lock the registered primary PDFs
npm run sources:verify        # network: re-download and compare against sources/source-lock.json
npm run sources:fetch         # network: materialize sources/raw/ from the committed lock without changing it
npm run extract                # offline (needs sources/raw/): deterministic page-aware PDF extraction
npm run extraction:test        # offline: golden page-text assertions
npm run extraction:determinism # offline: two clean runs must hash-match
npm run extraction:compare     # offline: classify historical fixture rows against extracted lines
```

Important:
Do not restart the FY2024 research from scratch.
Do not infer missing values from summaries.
Use repository evidence and source provenance.
Do not conflate Research Phase (substantive investigation, through 15) with Workspace Phase (repository bootstrap work, 0/1A/1B/1C/1D/...).
`sources/source-lock.json` is the reproducibility anchor for the two primary PDFs; never overwrite its hashes except by an explicit, reviewable `npm run sources:lock` re-run (see ADR-009).
Historical fixtures under `scripts/request-ingestion/fixtures/` are hand-curated and have not been modified; `npm run extraction:compare` documents how each fixture row traces back to the deterministic extraction (see `evidence/pdf-extraction-fixture-comparison.json`), but does not mean the fixture is generated mechanically. Do not rewrite fixtures to improve match statistics — document divergences instead.
