# Current Handoff

Last completed Research Phase: 15
Workspace Phase: 1B (request-ingestion PoC restored and reproducible)

Current focus:
Research reproducibility

Next action:
Implement primary-source acquisition and SHA-256 verification.

Read first:
- START_HERE.md
- protocol/RESEARCH_PROTOCOL.md
- protocol/DECISIONS.md
- protocol/REPRODUCIBILITY.md
- state/CURRENT_STATE.json
- state/RESEARCH_SUMMARY.md

Reproducibility check:
```bash
npm run validate
```
runs the restored `scripts/request-ingestion` PoC (fixture text -> staging -> normalized -> validation) and should print `validation PASS`.

Important:
Do not restart the FY2024 research from scratch.
Do not infer missing values from summaries.
Use repository evidence and source provenance.
Do not conflate Research Phase (substantive investigation, through 15) with Workspace Phase (repository bootstrap work, 0/1A/1B/...).
