# Case-009 Cabinet Office (CAO) — First Frozen Benchmark

Date: 2026-09-28 (Asia/Tokyo)

## 1. Executive summary

The existing, unmodified benchmark pipeline completed successfully against frozen Case-009 Ground Truth. `pdfjs-baseline` and `pymupdf-baseline` each passed **10/11** checks. Both recovered the selected page, expense row, wrapped label, amount triple, unsigned delta, unit, and item-to-amount relationship. They retained the correct item among six candidates but left `result.itemName` null rather than guess a single item owner.

`docling` passed **8/11**. It recovered the target page, unit, expense name, amount triple, and expense-to-amount relationship from one native table, but its `23x15` table reconstruction did not yield the correct target item candidate or an item-to-amount association. The first attempt was retained through its artifact hashes before the same command was rerun. All six raw/normalized artifacts were byte-identical across runs; generated evaluation artifacts changed timestamp-bearing bytes while reproducing the same matrix and scores.

The CAO 51-file package and its context-bearing file partitions remain confirmed source-side findings. This target is the first page of the already-locked `1.pdf`, where its local division scope is visible. No raw or normalized result demonstrates that package order, another PDF, or file-identity loss caused a benchmark failure. The evidence-supported conclusion is therefore: **source/package mechanism confirmed, but no causal benchmark interference demonstrated for this frozen target.**

## 2. Scope and non-goals

This is the first benchmark of the already selected and frozen Case-009 row. No source acquisition, selection, Ground Truth review, parser/normalizer/evaluator change, engine tuning, OCR experiment, MOF/RS linkage, or production adaptation was performed.

## 3. Freeze-chain provenance and integrity

| artifact | commit |
|---|---|
| Source Survey | `e640dc21c5bf536ab5ca40b20ed4b3ea8b2b3c11` |
| Selection Protocol | `d42b7b89f2671c8e9cad04b75116fbd7b64b7af6` |
| Row Selection | `985f77ed1ffa3cd29ae9e5b90f2b5de8fa74b969` |
| Ground Truth | `0d238d247d76d99c986541c6b8fa5ca03551ef3a` |

Before execution, the working tree was clean, HEAD matched the Ground Truth freeze commit, Ground Truth/evidence were byte-identical to that commit, and the local locked PDF re-hashed to `7b5de5dbd397c7067cab4ea527ef02681e91265914057651ee5b886174de7f4e`.

## 4. Exact commands and runtime result

First attempt:

```text
npm run extract
npm run docbench -- case-009
```

Both commands completed successfully. The configured engines were pdf.js baseline 4.10.38, PyMuPDF baseline 1.28.2, and Docling 2.130.0. Docling's unchanged normal pipeline initialized RapidOCR and logged that one of 323 PDF cells did not match a row or column band in a `23x24` matching grid and was dropped. This is a normal-engine runtime observation, not a separate OCR experiment or configuration change.

Reproducibility command:

```text
npm run docbench -- case-009
```

It also completed successfully with the same summary.

## 5. Raw extraction by engine

| engine | raw target-page result | source signal / structural observation |
|---|---|---|
| pdfjs-baseline | page 0; 40 lines; `千円` | target label, request/expense signal, and amount-bearing row signal present in flat native text |
| pymupdf-baseline | page 0; 40 lines; `千円` | same target-row signals with engine-native spacing differences |
| docling | page 0; 1 table; 130 retained cells; 1 standalone text; `千円` | target expense label and its three amount fragments occur in the native table, but table cells split/reorder some numeric strings and merge item hierarchy material |

The raw audit preceded evaluator interpretation. It inspected engine-native artifacts as generated, not a Ground Truth-based raw-output search.

## 6. Normalized output and candidate state

| engine | normalized target state | correct target candidate | unique item resolution |
|---|---|---|---|
| pdfjs-baseline | one expense row with request `1`, expense code, label, triple, unsigned delta, unit, and page | correct expense and correct item are retained; 6 item candidates | No; `itemName` is null |
| pymupdf-baseline | same semantic result, with source-native spacing differences upstream | correct expense and correct item are retained; 6 item candidates | No; `itemName` is null |
| docling | one expense candidate with expense code, label, triple, unsigned delta, unit, and page; request number null | correct expense/triple retained; correct item absent from its 2 item candidates | No; malformed item candidates only |

Thus the flat-text engines do not fail to extract the target; they refuse an ambiguous single-item resolution. Docling recovers the target expense/triple but fails the parent-item association because its candidate generation begins from malformed table-row structure.

## 7. Complete engine × check matrix

| check | pdfjs-baseline | pymupdf-baseline | docling |
|---|---|---|---|
| item_name_exact_match | FAIL | FAIL | FAIL |
| item_name_present_among_candidates | PASS | PASS | FAIL |
| expense_name_exact_match_after_line_join | PASS | PASS | PASS |
| previous_budget_exact_match | PASS | PASS | PASS |
| fy2024_request_exact_match | PASS | PASS | PASS |
| signed_delta_exact_match | PASS | PASS | PASS |
| unit_exact_match | PASS | PASS | PASS |
| page_identification | PASS | PASS | PASS |
| delta_sign_evidence_matches_source | PASS | PASS | PASS |
| item_to_amount_relationship | PASS | PASS | FAIL |
| expense_to_amount_relationship | PASS | PASS | PASS |

The complete native evaluator records are in `evidence/document-understanding/case-009-results.json`, `reports/document-understanding/case-009-evaluation.md`, and engine-specific derived artifacts.

## 8. Score and earliest failure layer

| engine | score | earliest demonstrated failure layer | evidence-bounded interpretation |
|---|---:|---|---|
| pdfjs-baseline | 10/11 | normalization / candidate resolution | raw and normalized target expense signals are present; six item-code-shaped candidates prevent a unique `itemName` |
| pymupdf-baseline | 10/11 | normalization / candidate resolution | same source-safe ambiguity outcome through its own native text representation |
| docling | 8/11 | document/layout understanding — table/row association | the raw table preserves the target expense/triple but fails to form the correct item candidate and item-parent association |

No source-acquisition, representation/text-signal, page-identification, unit, or expense-to-triple association failure was demonstrated.

## 9. Candidate presence versus resolution

The two 10/11 results are not a simple extraction miss: the target item is among their candidates and the target expense/triple is normalized correctly. The single failing check is a deliberate null single-item result under multiple candidate rows.

Docling differs. Its normalized target expense candidate contains the target label, triple, and unsigned delta, but its only item candidates correspond to later merged hierarchy material rather than the frozen target item. It therefore fails both item-candidate presence and item-to-amount relationship. The evidence does not support repairing this with a normalizer change in this task.

## 10. Case-009 package/context relevance

The source survey confirms 51 official PDFs, local scope partitions, and file identity as required provenance. The frozen benchmark intentionally uses only locked `1.pdf`, `pdfPageIndex 0`, whose file-opening division scope and `千円` unit are on the target page.

No engine selected another PDF, required package order, or surfaced a missing cross-file context. The two flat-text failures arise after recovery of the local ledger content; Docling's failure is in target-page table/item reconstruction. Accordingly, neither 51-file packaging nor file identity was demonstrated as a causal interference mechanism for this target result. This does not disprove an effect on a different file or target.

## 11. Comparison with Cases 006–008

Case-006's flat-text 2/11 outcomes were source-representation/text-extraction boundary results on a no-text-layer source, unlike Case-009's native-text 10/11 outcomes. Case-006 Docling had OCR-derived signal but later table association failure; Case-009 Docling has native signal and an item/table-association failure, so equal terminology does not establish the same detailed mechanism.

Case-008's pdf.js/PyMuPDF results were also 10/11 because correct item candidates existed but the normalizer declined a unique item result. Case-009 reproduces that candidate-resolution pattern for the flat-text engines. Case-008 Docling scored 3/11 because it did not form an eligible expense candidate/triple; Case-009 Docling's 8/11 retains those fields but still fails the parent item candidate/relationship. Case-007 has no GT benchmark and is not score-comparable.

## 12. Evaluator applicability and unexpected findings

The evaluator distinguishes correct-item-among-candidates from a unique resolved item, and it separately exposes Docling's absent target item candidate and failed item-to-amount relationship. It does not encode source-file scope, file identity, or earliest failure layer; those remain evidence-backed analysis rather than score fields.

The unexpected result is the narrower-than-Case-008 Docling failure: despite a table grid warning and fragment/reordering, it reconstructed the selected expense label and amount triple correctly, leaving only item hierarchy association unresolved.

## 13. Reproducibility

The first attempt's raw/normalized SHA-256 values were recorded before rerun. The same six hashes were obtained after rerun:

| artifact | SHA-256 |
|---|---|
| pdf.js raw | `b43da6bc11a1bb2e011ef69754ad7fc5ced3a3f89cb9a22f7fb750171d9d90e7` |
| pdf.js normalized | `6d745695fd5e4caea3343b79eb151c6e16e323a8608753835da408fad216250d` |
| PyMuPDF raw | `d4fb04a70002c56a985d82b59af377644fbe67ec9fe2a73e84e73bb50845bb86` |
| PyMuPDF normalized | `81869a80b6f5997bddb83975febf7005a9823d27db70d364f249efdc7286bd92` |
| Docling raw | `8aed5e4c56df0416f8ac894b073ea3b652ea9e036fb941cfcef957462b47fb46` |
| Docling normalized | `d3e96b10e65458d49a35e66976aca3d696a024794b3915790e56cf629504dca1` |

The generated evaluation JSON/Markdown and combined evidence changed byte hashes between attempts because their generated/evaluated timestamps changed. The two observed command summaries and check matrices are identical. No setting, source, or code was changed between runs.

## 14. Limitations and deferred experiments

- One row on one page of one locked detail file does not test package-wide or cross-file behavior.
- The exact cause of Docling's table fragmentation/row association was not investigated.
- No source-safe general method for unique item selection was introduced.
- Whether file-scope partitions affect another CAO detail file remains unresolved.
- A separate table-structure or candidate-resolution study would require a separately scoped future task; none was performed here.

## 15. Frozen-artifact integrity, validation, and next task

The Source Survey/evidence, Selection Protocol, Selection Record, and GT/evidence remain unchanged from their freeze commits. Cases 001–008, the Case-006–010 Selection Freeze, source lock/registry, `scripts/`, parser/normalizer/evaluator, and production semantics were not changed. Generated benchmark artifacts, this report, and state updates are the intended changes.

Validation: `npm run validate`, `npm run extraction:test`, `npm run docbench:test`, `npm run sources:test`, and `git diff --check` are required before commit. No additional benchmark or OCR experiment is part of validation.

Recommended next task: **Case-009 Closeout** — audit the frozen chain and synthesize the source-side and benchmark findings without adaptation.

**The Case-009 first frozen benchmark was preserved using the existing, unmodified pipeline and evaluator semantics. The 51-file package/context structure was treated as a source-side property and was not assumed to be a benchmark failure cause without direct evidence. No parser adaptation, normalization change, evaluator change, Ground Truth modification, or separate OCR experiment was performed.**
