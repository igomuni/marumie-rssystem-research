# TODO

## Next

- Make curated fixture generation reproducible from deterministic PDF extraction, preserving historical golden equivalence
- Define adapter interface for extraction, per document type
- Define phase manifest schema
- Define automated handoff workflow
- Add repository validation command (beyond `npm run validate`)

## Later

- Restore Phase 3-15 evidence corpus incrementally
- Convert manual transformation logic into scripts
- Build golden tests for major research totals
- Evaluate allocationMode golden cases

## Document Understanding benchmark (branch: research/document-understanding-benchmark)

- Resolve header-row (項 vs 目) ambiguity so `item_name_exact_match` can resolve on pages with multiple 3-digit-code rows, instead of only via the `item_name_present_among_candidates` diagnostic
- Integrate Docling as the first table-structure-aware engine (see `reports/document-understanding/external-engine-survey.md` for rationale); extend `benchmark/src/normalize.mjs` or add a Docling-specific normalization path to consume structured table cells rather than flat text lines
- Add a general per-page unit-label lookup (currently `unit_exact_match` correctly fails because the "千円" label lives only on the document's earlier summary page, not on case-001's page)
- Add more benchmark cases beyond case-001 (e.g. a case exercising true multi-row table association, a case with no wrapping)
- Merge this branch to `main` once reviewed
