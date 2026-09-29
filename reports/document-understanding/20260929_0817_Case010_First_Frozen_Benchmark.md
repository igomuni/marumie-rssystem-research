# Case-010 MHLW — First Frozen Benchmark

Date: 2026-09-29 (Asia/Tokyo)

## 1. Executive summary

The existing, unmodified benchmark pipeline completed successfully against frozen Case-010 Ground Truth. `pdfjs-baseline` and `pymupdf-baseline` each passed **10/11** checks. Both reached `pdfPageIndex 20`, recovered the selected expense row, label, row-local amount triple, unsigned delta, and `千円`, and retained the correct item among four item candidates. Both left `result.itemName` null rather than select one item candidate.

`docling` passed **3/11**. It reached the target page and recovered `千円`, but its one 99-cell table produced merged item material and no eligible expense candidate, so the selected row's label, triple, and associations are null in normalized output. The earliest demonstrated issue is table/row association, not text-layer absence or page identification.

The full 1,723-page native-text PDF completed through extraction without a target-page loss, timeout, or resource error. No scale-specific interference is demonstrated for this frozen target. The target page contains embedded remarks-side material, but the generated artifacts do not isolate that material as the cause of Docling's local table-association failure; its causal role is **possible but unproven**.

## 2. Scope and non-goals

This is the first frozen benchmark of the already-selected Case-010 main-ledger row. No source acquisition, protocol/selection/GT change, parser or normalizer adaptation, evaluator change, engine configuration change, separate OCR experiment, MOF/RS linkage, or production adaptation was performed.

## 3. Freeze-chain provenance and integrity

| artifact | commit |
| --- | --- |
| Source Survey | `cc5115b80076159dc58570fb9fa4e7d7267a14f5` |
| Selection Protocol | `2f910f218a35a776d57d32c30f10322b0b945209` |
| Row Selection | `4b98acea75c4abad9b4086ecd76a3c3261b1bab5` |
| Ground Truth | `ce985191d02993584fe3c99716691fa7013983d9` |

Before execution, HEAD matched the Ground Truth freeze commit; the working tree was clean; Ground Truth/evidence, Selection Record, Protocol, and Source Survey/evidence were byte-identical to their respective freeze commits. The Case-006–010 Selection Freeze, Cases 001–009, `scripts/`, source lock/registry, parser/normalizer/evaluator, and production code were unchanged.

## 4. Source integrity and frozen target

The locked source `mhlw-fy2024-general-account-expenditure-request-summary-detail` re-hashed to `09d26048b20d1b1dac7aab236ab6da452e482a12f4d97a8f6c28ec7c420eb192` before execution. It is one native-text 1,723-page PDF.

The benchmark read the committed `fixtures/document-understanding/case-010/ground-truth.json`; no value was manually supplied to an engine. The frozen target is the main standard-ledger row at `pdfPageIndex 20` (printed `厚（本）13`), under `010 厚生労働本省` / `001 厚生労働本省共通費`, not the embedded remarks-side structure.

## 5. Exact commands and runtime result

First completed pipeline run:

```text
npm run extract
npm run docbench -- case-010
```

Both commands exited successfully. Extraction processed the full locked MHLW PDF (`pages=1723`, `items=712665`, `lines=68789`). The configured engines were pdf.js baseline 4.10.38, PyMuPDF baseline 1.28.2, and Docling 2.130.0.

The execution environment's nonpersistent 30-second wrapper ended two earlier full-corpus extraction invocations before an exit code or Case-010 result artifact was produced. Those wrapper-boundary observations are not treated as completed benchmark results. The identical command above then completed in a persistent terminal session without any pipeline setting change.

Docling's unchanged normal pipeline initialized RapidOCR models on CPU. This is a runtime observation of the pre-existing engine, not a separate OCR experiment or adaptation. The logs do not isolate whether OCR materially contributed on this native-text target page.

Reproducibility command:

```text
npm run docbench -- case-010
```

It exited successfully with the same target-page raw counts and score summary.

## 6. Raw extraction by engine

| engine | raw target-page observation | source signal / structural observation |
| --- | --- | --- |
| pdfjs-baseline | page 20; 46 lines; `千円` | native flat text includes target request/expense/label/triple signal |
| pymupdf-baseline | page 20; 46 lines; `千円` | same target-row signal with engine-native spacing differences |
| docling | page 20; one table; 99 cells; two standalone texts; `千円` | source content survives in a native table but row/item text is merged into malformed table candidates |

The raw audit preceded evaluator interpretation. It inspected native artifacts as produced; it did not repair rows or use Ground Truth to modify engine output.

## 7. Normalized output and candidate state

| engine | normalized target state | target candidate / unique item resolution |
| --- | --- | --- |
| pdfjs-baseline | request `1`, expense code, label, triple, unsigned delta, unit, and page retained | one expense candidate; correct item among four candidates; no unique item result |
| pymupdf-baseline | same semantic result through its native text representation | one expense candidate; correct item among four candidates; no unique item result |
| docling | only unit and page retained in `result` | two malformed item candidates; zero expense candidates; no target item/triple association |

For the flat-text engines, the failure is not target-text or triple recovery: generic candidate resolution intentionally returns null for a non-unique item choice. For Docling, upstream table/row structure does not yield a source-safe expense candidate for normalization.

## 8. Complete engine × check matrix

| check | pdfjs-baseline | pymupdf-baseline | docling |
| --- | --- | --- | --- |
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

The generated machine-readable record is `evidence/document-understanding/case-010-results.json`; the evaluator rendering is `reports/document-understanding/case-010-evaluation.md`.

## 9. Score and earliest demonstrated failure layer

| engine | score | earliest demonstrated failure layer | evidence-bounded interpretation |
| --- | ---: | --- | --- |
| pdfjs-baseline | 10/11 | candidate resolution | raw/native text and normalized target expense/triple are present, but four item-code-shaped candidates prevent a unique `itemName` |
| pymupdf-baseline | 10/11 | candidate resolution | same candidate-ambiguity outcome through its own native text output |
| docling | 3/11 | document/layout understanding — table/row association | one source table reaches the target page, but merged row/item material produces no eligible expense candidate before normalization |

No source-acquisition, native-text availability, full-document processing, page-identification, or unit-recovery failure was demonstrated.

## 10. Target recovery and association

Both flat-text engines recovered the target expense label and same-row triple and passed expense-to-amount and item-to-amount relationship checks. Their only failure is `item_name_exact_match`, despite the exact item being present in the candidate set.

Docling reached the page and section unit but its item candidates merge the organization, item, and target expense text. It formed no expense candidate; consequently all target amount fields and both relationship checks fail. This is not evidence that the target amount glyphs were absent from the source.

## 11. Scale, embedded-substructure, and representation analysis

**Scale verdict: no scale interference demonstrated.** The ordinary extraction command processed all 1,723 pages and emitted target-page raw artifacts. Each engine reported page 20; no truncation, page omission, target-page timeout, or resource failure was observed. This does not prove that scale could not affect a different target or engine configuration.

**Embedded remarks-side verdict: possible but unproven.** The target page has embedded remarks-side material and Docling's table association fails locally. No raw or normalized evidence isolates a remarks-side cell as the contaminating source, nor demonstrates that the embedded material caused the failure. The page-level co-occurrence alone is insufficient for causal attribution.

**Representation interpretation:** Case-010 is a native-text source. pdf.js and PyMuPDF's target-row recovery rules out a text-layer absence explanation for their results. Docling's issue occurs later, in table/row reconstruction, not at representation acquisition.

## 12. Cross-case interpretation

Case-006 is not a representation analogue: its flat-text engines encountered a vector-outline/no-text boundary, while Case-010’s flat-text engines recover the target native text and only fail candidate resolution. Case-006 Docling had OCR-derived signal followed by a later structure failure; that does not establish the same detailed mechanism here.

Case-008 had the same 10/11 flat-text candidate-resolution pattern and a 3/11 Docling table/layout result. The shared score does not establish an identical cause: Case-010 has confirmed native target text and a 99-cell single-table reconstruction with no eligible expense candidate. Case-009 also had 10/11 flat-text candidate resolution, but its Docling result retained target expense/triple and scored 8/11; Case-010’s Docling loss occurs earlier at expense-candidate formation. Case-007 has no GT benchmark and is not score-comparable.

## 13. Evaluator applicability and unexpected findings

The evaluator usefully distinguishes a correct item being present among candidates from a unique resolved item, and separately shows Docling’s absent expense candidate and relationship failures. It does not encode scale, embedded-substructure provenance, or earliest failure layer; those remain evidence-backed analysis, not a reason to alter evaluator semantics.

The principal unexpected observation is that the largest single PDF in the study completed normally and yielded high flat-text coverage at the target. The observed Docling failure is a local structure-reconstruction result, not evidence that scale caused a pipeline failure.

## 14. Reproducibility

The first completed run's six raw/normalized hashes were recorded before rerun. All six matched byte-for-byte after the identical rerun:

| artifact | first / rerun SHA-256 |
| --- | --- |
| pdf.js raw | `9a8be94ba2b701a8c6fe72fa0c9aa52ad75092baaed7608a1584ab77612b8ffa` |
| pdf.js normalized | `03f3792bbac95db7b516bcc4bf0e56e70826b343e8e18a9de5ab7ecf5eeabd7e` |
| PyMuPDF raw | `f5eff7f46ff401d9acb41cdf8c62ad270721ff8af6742980620a4c36f939a1fb` |
| PyMuPDF normalized | `44fbe7398ac39982001ff37b901e02f7de3b7ff9cfdb1a5f144041c838e93935` |
| Docling raw | `cfbcc260233b540c58e5947d759591972474a8e6a42bd6626e7651697a943e40` |
| Docling normalized | `98bb822fae7c2cf9b5e0790c652cc2d3b3102178dd46b5acbebf02a1d73eb33b` |

Per-engine evaluation JSON bytes changed because `evaluatedAt` regenerated. The combined evidence and Markdown also regenerate timestamps. The observed first and rerun score summaries, raw counts, normalized results, and complete check matrix are the same; no setting, source, or code changed between runs.

## 15. Limitations and unresolved questions

- One frozen row cannot establish a whole-document scale effect or its absence on other pages.
- The precise mechanism of Docling’s 99-cell table/row association failure was not investigated.
- Whether the embedded remarks-side material contributes to that local failure remains unresolved.
- No source-safe general rule for resolving a single item among multiple item candidates was introduced.
- The host wrapper boundary noted above is not an engine result; it prevents treating the preliminary nonpersistent invocations as reproducible pipeline outcomes.

## 16. Integrity audit, explicit non-actions, and next task

The Source Survey/evidence, Selection Protocol, Selection Record, and GT/evidence remain unchanged from their freeze commits. Cases 001–009, the Case-006–010 Selection Freeze, `scripts/`, source lock/registry, parser/normalizer/evaluator, OCR configuration, and production semantics were not changed. The committed outputs for this task are the Case-010 benchmark evidence/evaluation, this report, and state updates; engine-native derived artifacts remain generated/ignored working artifacts.

No parser adaptation, normalizer change, evaluator change, Ground Truth modification, source change, engine tuning, separate OCR experiment, MOF linkage, production adaptation, or Case-010 closeout was performed.

Recommended next task: **Case-010 Closeout** — audit the full frozen chain and synthesize source, selection, GT, benchmark, and reproducibility findings without adaptation.

**The Case-010 first frozen benchmark was preserved using the existing, unmodified pipeline and evaluator semantics. Source scale and embedded substructures were treated as hypotheses to evaluate, not assumed failure causes. No parser adaptation, normalization change, evaluator change, Ground Truth modification, or separate OCR experiment was performed.**
