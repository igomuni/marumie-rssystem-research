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

## Document Understanding benchmark (merged to main via PR #1)

- Resolve header-row (項 vs 目) ambiguity so `item_name_exact_match` can resolve on pages with multiple 3-digit-code rows, instead of only via the `item_name_present_among_candidates` diagnostic — still unresolved for all three engines (pdfjs, PyMuPDF, Docling) after Docling integration
- Recover the request-number column for Docling (currently `null` for case-001's target row — Docling's table structure produced no cell for that column on that specific row)
- Add a general per-page/document-level unit-label lookup (currently `unit_exact_match` correctly fails for all three engines because the "千円" label lives only on the document's earlier summary page, not on case-001's page)

## case-002 (branch: research/case-002-meti-preregistration)

- **Blocked:** acquire the METI FY2024 general-account request PDF (`https://www.meti.go.jp/main/yosangaisan/fy2024/pdf/ippan_o.pdf`) — currently returns an AWS WAF JS challenge (HTTP 202, `x-amzn-waf-action: challenge`) to the repository's plain-fetch acquisition tooling. Needs either a manually-supplied copy (with independent SHA-256 verification against the same official URL once accessible) or an explicitly-authorized browser-capable acquisition method — do not substitute a mirror.
- Once acquired and locked: apply the frozen selection protocol (`fixtures/document-understanding/case-002/20260926_0834_Case002_Selection_Protocol.md`) via direct visual inspection (not via pdfjs/PyMuPDF/Docling, to avoid circularity) to select and freeze the exact row.
- Only after the row is frozen: create `fixtures/document-understanding/case-002/ground-truth.json` by visual transcription, then run the three existing engines against it to test whether the case-001-derived findings (table-cell column separation, numeric-token reversal, CJK-space closing, header-hierarchy ambiguity) generalize.
- Do not modify case-001 Ground Truth, scores, or normalizers while doing this — case-002 tests generalization of frozen behavior.
