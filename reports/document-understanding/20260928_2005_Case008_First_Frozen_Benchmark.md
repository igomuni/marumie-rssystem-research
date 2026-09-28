# Case-008 Courts — First Frozen Benchmark

Date: 2026-09-28 (Asia/Tokyo)

## 1. Executive summary

The existing, unmodified benchmark pipeline completed successfully for the frozen Case-008 target. `pdfjs-baseline` and `pymupdf-baseline` each passed 10/11 checks. Both recovered the target page, wrapped expense label, row-local amount triple, unit, and item/expense-to-amount relationships, but left `result.itemName` null because the generic normalizer found multiple item-code-shaped rows. `docling` passed 3/11: it identified page 6 and the section-local unit, but its one detected table was structurally fragmented and did not yield an eligible expense candidate or associated amount triple.

The first run was preserved before analysis. A second run of the identical command produced byte-identical raw and normalized artifacts for all three engines; the two evaluation outputs differ only in generated/evaluated timestamps. No source, selection, Ground Truth, parser, normalizer, evaluator, engine configuration, or OCR configuration was changed.

## 2. Scope and non-goals

This is the first frozen benchmark of the already-selected standard-ledger row only. It is not a parser, normalizer, evaluator, source, or Ground Truth review. No adaptation, extra engine, configuration tuning, MOF/RS linkage, production change, or separate OCR experiment was performed.

## 3. Freeze chain

| artifact | commit |
|---|---|
| Source Survey | `e10d56c529ce9c8197f71dd71df32297ea3675fb` |
| Selection Protocol | `3cf4a4f23f036c96cae6852f97a8a17801725299` |
| Selection Record | `0ccea62537dea8b97e2792a4ced1f70bd5f95f85` |
| Ground Truth | `55bda2319c761745debcab1df9bc2921b541fabe` |

The protocol, selection record, Ground Truth JSON, and Ground Truth evidence were checked against their respective freeze commits before the run and were byte-identical. This task began at the expected `55bda2319c761745debcab1df9bc2921b541fabe` HEAD.

## 4. Source and Ground Truth integrity

The locked source is `courts-fy2024-general-account-expenditure-request`: one 127-page PDF, SHA-256 `df43f2dc183da84fa9952ae4c5e17888177df186ad4c556ed1a519ba584e3c06`, 736,439 bytes. The locally held raw file re-hashed to that locked SHA before execution.

The benchmark read the existing `fixtures/document-understanding/case-008/ground-truth.json`; no chat value was manually supplied to an engine. The frozen locator remains standard-ledger `pdfPageIndex` 6 (printed `裁（裁）3`), not the staffing or policy-framework sections.

## 5. Exact commands and runtime result

First attempt:

```text
npm run extract
npm run docbench -- case-008
```

The extraction command exited successfully. The benchmark command exited successfully and ran the repository-configured engine set: pdf.js baseline 4.10.38, PyMuPDF baseline 1.28.2, and Docling 2.130.0. Docling logged its normal RapidOCR initialization and a `7x26` grid warning that two of 314 PDF cells were dropped. These are engine runtime observations, not an added experiment.

Reproducibility confirmation:

```text
npm run docbench -- case-008
```

The second attempt also exited successfully with the same summaries.

## 6. Raw extraction by engine

| engine | raw target-page observation | result |
|---|---|---|
| pdfjs-baseline | page 6, 40 lines, `千円`; separate header, hierarchy, expense line, and visual-label continuation signals | target row signal present |
| pymupdf-baseline | page 6, 40 lines, `千円`; same logical row/continuation signals, with engine-native spacing differences | target row signal present |
| docling | page 6, 1 table, 53 cells, 0 standalone texts, `千円` | source characters/cells present, but identifiers, labels, and numeric material are split and merged across the table grid |

The raw inspection preceded reading evaluator outcomes. It used the native raw artifacts as they were produced; no Ground Truth value was used as a raw-artifact search key.

## 7. Normalized output by engine

The two flat-text normalizers each produced one expense candidate with the wrapped label joined, row-local request/expense identifiers, the three values, a glyph-free positive delta string, page 6, and `千円`. They retained four item-code-shaped candidates, including the correct item, and consequently emitted `itemName: null` rather than guessing a single owner.

Docling's normalizer received one 53-cell table but formed two malformed item candidates and zero expense candidates. Its result therefore retained only the target page and `千円`; target identifiers, label, amounts, and relationships are null. This is a faithful representation of that engine's supplied table structure, not a repair by the normalizer.

## 8. Complete evaluation matrix

| check | pdfjs-baseline | pymupdf-baseline | docling |
|---|---|---|---|
| item_name_exact_match | FAIL | FAIL | FAIL |
| item_name_present_among_candidates | PASS | PASS | FAIL |
| expense_name_exact_match_after_line_join | PASS | PASS | FAIL |
| previous_budget_exact_match | PASS | PASS | FAIL |
| fy2024_request_exact_match | PASS | PASS | FAIL |
| signed_delta_exact_match | PASS | PASS | FAIL |
| unit_exact_match | PASS | PASS | PASS |
| page_identification | PASS | PASS | PASS |
| delta_sign_evidence_matches_source | PASS | PASS | PASS |
| item_to_amount_relationship | PASS | PASS | FAIL |
| expense_to_amount_relationship | PASS | PASS | FAIL |

The full engine-native actual/expected values and check notes are retained in `evidence/document-understanding/case-008-results.json`; the generated evaluator rendering is `reports/document-understanding/case-008-evaluation.md`.

## 9. Score summary

| engine | passed | failed | total |
|---|---:|---:|---:|
| pdfjs-baseline | 10 | 1 | 11 |
| pymupdf-baseline | 10 | 1 | 11 |
| docling | 3 | 8 | 11 |

Scores do not make the engines interchangeable. In particular, the two 10/11 outcomes retain the correct item among candidates but honestly decline to resolve it, whereas Docling cannot form the target expense candidate at all.

## 10. Earliest failure layer

| engine | earliest observed failure layer | evidence-bounded interpretation |
|---|---|---|
| pdfjs-baseline | normalization / hierarchy disambiguation | raw text and target expense-row association are recovered; multiple item-code-shaped candidates prevent a single `itemName` result |
| pymupdf-baseline | normalization / hierarchy disambiguation | same outcome through its native text representation |
| docling | document/layout understanding | its table grid splits and fuses target-region material before a clean identifier/label/triple candidate can be constructed |

No source-acquisition, page-identification, or unit-recovery failure was observed. The Docling normalizer was not classified as the earliest failure: it preserves a null result when its upstream table does not provide a source-safe target row.

## 11. Target-row and section-aware provenance

All engines received and reported `pdfPageIndex` 6. The flat-text raw artifacts show the standard-ledger row and its wrap continuation; their normalized records retain the requested row-level expense association. Docling also reported page 6 and one table, but did not reconstruct that row's structure correctly.

The target provenance remains: the locked combined Courts file **plus the standard-ledger section plus page locator**. Nothing in these results identifies the staffing table or policy-framework section as the target.

## 12. Multi-grammar analysis

The source survey established that one file contains standard ledger, staffing, policy-framework, and blank-separator grammars. This benchmark processed the frozen target page rather than conducting a whole-file grammar experiment. None of the raw or normalized artifacts show a staffing/policy section being mistaken for page 6, or demonstrate an effect of those remote sections on its table segmentation.

Therefore the evidence-supported conclusion is: **multi-grammar source, but no demonstrated causal effect on this target result.** The possible whole-file effect remains unknown; the present result neither rules it out nor attributes Docling's target-page grid failure to it.

## 13. Unit and context behavior

All engines recovered `千円` and passed page identification. For the flat-text engines, the organization/item hierarchy appears in candidates and the expense triple is associated with the expense code; only generic single-item selection remains ambiguous. Docling recovers the section-local unit but not source-safe item or expense context. The staffing-table unit `人` did not appear in normalized target outputs.

## 14. Cross-case comparison

Case-005's committed evaluation also has 10/11 for its three engines, with shared `item_name_exact_match` failure; Case-008's two flat-text 10/11 outcomes consequently continue the established distinction between a correct candidate being present and an unresolved single result. That shared score does not establish identical source or hierarchy mechanics.

Case-006 illustrates the converse: equal low scores there concealed extraction-boundary failures for flat-text engines and a later layout failure for Docling. Case-008 supplies readable native text to the flat-text engines, while this Docling result is again a layout/table-structure failure. Case-007 has no Ground Truth or benchmark and is excluded from score comparison.

## 15. Unexpected findings and evaluator applicability

The main unexpected result is the large split between readable flat-text processing (10/11) and Docling's 3/11 on a native-text, standard-ledger page. Docling's grid warning and fragmented cells support a target-page structure-reconstruction problem; they do not prove a source-wide or multi-grammar cause.

The evaluator correctly exposes the practical distinction between flat-text candidate ambiguity and Docling's absent expense candidate through different checks. It does not independently encode section/grammar provenance or the earliest failure layer. Those are analysis observations, not a request to change evaluator semantics.

## 16. Reproducibility

All six raw/normalized artifacts (`3 engines × raw/normalized`) were byte-identical between the first and second benchmark runs. The result JSON and evaluation Markdown differed only in `generatedAt` / `evaluatedAt` timestamps. Scores, check matrix, raw counts, and Docling's grid-warning outcome reproduced.

## 17. Limitations and unresolved questions

- This benchmark evaluates exactly one frozen standard-ledger row, not every grammar in the 127-page file.
- The benchmark setup is target-page oriented, so it cannot establish a causal whole-file effect of staffing, policy, or blank sections.
- The mechanism behind Docling's `7x26` grid fragmentation was not investigated.
- The generic hierarchy ambiguity that leaves a correct item candidate unpromoted remains unresolved; no change was attempted.
- RapidOCR was visibly initialized by unmodified Docling. Whether it materially contributed on this native-text page was not isolated, because no separate OCR experiment was permitted.

## 18. Recommended next task

Proceed to a **Case-008 closeout** task: audit the freeze chain and first-run preservation, synthesize source-side and benchmark-side findings, and keep any adaptation or evaluator design work separately scoped.

---

**The Case-008 first frozen benchmark was preserved using the existing, unmodified pipeline and evaluator semantics. No parser adaptation, normalization change, evaluator change, Ground Truth modification, or separate OCR experiment was performed.**
