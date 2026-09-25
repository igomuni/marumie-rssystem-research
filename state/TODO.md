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

- Resolve header-row (項 vs 目) ambiguity so `item_name_exact_match` can resolve on pages with multiple 3-digit-code rows, instead of only via the `item_name_present_among_candidates` diagnostic — still unresolved for all three engines (pdfjs, PyMuPDF, Docling) after Docling integration
- Recover the request-number column for Docling (currently `null` for case-001's target row — Docling's table structure produced no cell for that column on that specific row)
- Add a general per-page/document-level unit-label lookup (currently `unit_exact_match` correctly fails for all three engines because the "千円" label lives only on the document's earlier summary page, not on case-001's page)
- Consider extending Docling's per-cell reading-order fix (`normalize-docling.mjs`'s numeric-token reversal) to a second case to confirm it generalizes beyond case-001's page before relying on it further
- Add more benchmark cases beyond case-001 (e.g. a case exercising true multi-row table association, a case with no wrapping, a case testing whether Docling's table detection holds up on a differently-formatted page)
- Recommended next experiment: add a second case on a *different* page of the same PDF (or the important-policy PDF) to see whether Docling's table detection and the two general Docling-specific rules (CJK wrap-space closing, numeric-token reversal) hold up outside the one page they were derived from
- Merge this branch to `main` once reviewed
