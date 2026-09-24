# Current Handoff

Last completed Research Phase: 15
Workspace Phase: 1C (primary-source acquisition and SHA-256 lock)

Current focus:
Research reproducibility

Next action:
Implement deterministic PDF text extraction and compare it with historical fixtures.

Read first:
- START_HERE.md
- protocol/RESEARCH_PROTOCOL.md
- protocol/DECISIONS.md
- protocol/REPRODUCIBILITY.md
- state/CURRENT_STATE.json
- state/RESEARCH_SUMMARY.md

Reproducibility checks:
```bash
npm run validate         # offline: fixture -> staging -> normalized -> validation
npm run sources:lock     # network: acquire + hash-lock the registered primary PDFs
npm run sources:verify   # network: re-download and compare against sources/source-lock.json
```

Important:
Do not restart the FY2024 research from scratch.
Do not infer missing values from summaries.
Use repository evidence and source provenance.
Do not conflate Research Phase (substantive investigation, through 15) with Workspace Phase (repository bootstrap work, 0/1A/1B/1C/...).
`sources/source-lock.json` is the reproducibility anchor for the two primary PDFs; never overwrite its hashes except by an explicit, reviewable `npm run sources:lock` re-run (see ADR-009).
