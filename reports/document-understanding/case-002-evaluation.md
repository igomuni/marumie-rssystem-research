# Document Understanding Benchmark — case-002

Generated: 2026-09-26T00:20:42.158Z

| engine | passed | failed | total |
|---|---|---|---|
| pdfjs-baseline (4.10.38) | 2 | 9 | 11 |
| pymupdf-baseline (1.28.2) | 3 | 8 | 11 |
| docling (2.130.0) | 2 | 9 | 11 |

The score alone is not the main result — see which *specific* checks differ below.

## Comparison matrix

| check | pdfjs-baseline | pymupdf-baseline | docling |
|---|---|---|---|
| item_name_exact_match | FAIL | FAIL | FAIL |
| item_name_present_among_candidates | FAIL | PASS | FAIL |
| expense_name_exact_match_after_line_join | FAIL | FAIL | FAIL |
| previous_budget_exact_match | FAIL | FAIL | FAIL |
| fy2024_request_exact_match | FAIL | FAIL | FAIL |
| signed_delta_exact_match | FAIL | FAIL | FAIL |
| unit_exact_match | PASS | PASS | PASS |
| page_identification | PASS | PASS | PASS |
| delta_glyph_observed_and_associated | FAIL | FAIL | FAIL |
| item_to_amount_relationship | FAIL | FAIL | FAIL |
| expense_to_amount_relationship | FAIL | FAIL | FAIL |

## pdfjs-baseline

| check | pass | actual | expected | note |
|---|---|---|---|---|
| item_name_exact_match | FAIL | `null` | `"経済産業本省共通費"` | Only passes if the harness resolved a single unambiguous item-code row; see item_name_present_among_candidates for a diagnostic on ambiguous pages. |
| item_name_present_among_candidates | FAIL | `[{"itemCode":"010","itemName":"経 済 産 業 本 省"},{"itemCode":"010","itemName":"経 済 産 業 本 省 共 通 費"},{"itemCode":"001","itemName":"既 定 定 員 に 伴 う 経 費"},{"itemCode":"001","itemName":"人 件 費"}]` | `{"itemCode":"010","itemName":"経済産業本省共通費"}` | Diagnostic only: on a page with multiple item-code-shaped rows, this checks whether the correct row was extracted and reconstructed correctly at all, independent of whether the harness's single-match selection resolved it into `result`. |
| expense_name_exact_match_after_line_join | FAIL | `"経済産業本省一般行政に 42,331,005 46,887,829 4,556,824 （要求要旨）必要な経費 「経済産業省設置法」に定める本省内部部局所掌の一般事務を処理するため必要な庁費等"` | `"経済産業本省一般行政に必要な経費"` | Deterministic line-join only (common.mjs joinWrappedLabel); no semantic repair. |
| previous_budget_exact_match | FAIL | `null` | `42331005` |  |
| fy2024_request_exact_match | FAIL | `null` | `46887829` |  |
| signed_delta_exact_match | FAIL | `null` | `4556824` | FAIL here must mean the engine failed to preserve/associate the sign, not that we substituted the ground-truth sign. |
| unit_exact_match | PASS | `"千円"` | `"千円"` |  |
| page_identification | PASS | `8` | `8` |  |
| delta_glyph_observed_and_associated | FAIL | `null` | `"contains △"` | Checks the ground-truth-blind normalizer output, not the ground truth. A PASS means the △ glyph was genuinely present somewhere in the engine's own raw output and the deterministic normalizer associated it with this delta value. For a flat-line engine (pdfjs-baseline, pymupdf-baseline), deltaRaw is a single literal raw-line substring. For a table-cell engine (docling), deltaRaw may instead be a normalizer-constructed concatenation of two separate raw cells (a glyph-only cell and a magnitude cell) that the same table row placed together — still traceable to genuine raw engine output, never to the ground truth, but not necessarily one literal raw token. |
| item_to_amount_relationship | FAIL | `{"nearestPrecedingItemCode":"010","resultPreviousBudget":null}` | `{"itemCode":"010","previousBudget":42331005}` | The amount triple must belong to the expense row nested under the correct item-code row, not merely appear somewhere on the page. |
| expense_to_amount_relationship | FAIL | `{"expenseCode":"01-95","hasTriple":false}` | `{"expenseCode":"01-95","hasTriple":true}` | The amount triple must be parsed from the same structural row as the expense code, not an adjacent/unrelated row. |

## pymupdf-baseline

| check | pass | actual | expected | note |
|---|---|---|---|---|
| item_name_exact_match | FAIL | `null` | `"経済産業本省共通費"` | Only passes if the harness resolved a single unambiguous item-code row; see item_name_present_among_candidates for a diagnostic on ambiguous pages. |
| item_name_present_among_candidates | PASS | `[{"itemCode":"010","itemName":"経 済 産 業 本 省"},{"itemCode":"010","itemName":"経済産業本省共通費"},{"itemCode":"001","itemName":"既定定員に伴う経費"},{"itemCode":"001","itemName":"人    件    費"}]` | `{"itemCode":"010","itemName":"経済産業本省共通費"}` | Diagnostic only: on a page with multiple item-code-shaped rows, this checks whether the correct row was extracted and reconstructed correctly at all, independent of whether the harness's single-match selection resolved it into `result`. |
| expense_name_exact_match_after_line_join | FAIL | `"経済産業本省一般行政に                 42,331,005      46,887,829                                     4,556,824 （要求要旨）必要な経費                                                  「経済産業省設置法」に定める本省内部部局所掌の一般事務を処理するため必要な庁費等"` | `"経済産業本省一般行政に必要な経費"` | Deterministic line-join only (common.mjs joinWrappedLabel); no semantic repair. |
| previous_budget_exact_match | FAIL | `null` | `42331005` |  |
| fy2024_request_exact_match | FAIL | `null` | `46887829` |  |
| signed_delta_exact_match | FAIL | `null` | `4556824` | FAIL here must mean the engine failed to preserve/associate the sign, not that we substituted the ground-truth sign. |
| unit_exact_match | PASS | `"千円"` | `"千円"` |  |
| page_identification | PASS | `8` | `8` |  |
| delta_glyph_observed_and_associated | FAIL | `null` | `"contains △"` | Checks the ground-truth-blind normalizer output, not the ground truth. A PASS means the △ glyph was genuinely present somewhere in the engine's own raw output and the deterministic normalizer associated it with this delta value. For a flat-line engine (pdfjs-baseline, pymupdf-baseline), deltaRaw is a single literal raw-line substring. For a table-cell engine (docling), deltaRaw may instead be a normalizer-constructed concatenation of two separate raw cells (a glyph-only cell and a magnitude cell) that the same table row placed together — still traceable to genuine raw engine output, never to the ground truth, but not necessarily one literal raw token. |
| item_to_amount_relationship | FAIL | `{"nearestPrecedingItemCode":"010","resultPreviousBudget":null}` | `{"itemCode":"010","previousBudget":42331005}` | The amount triple must belong to the expense row nested under the correct item-code row, not merely appear somewhere on the page. |
| expense_to_amount_relationship | FAIL | `{"expenseCode":"01-95","hasTriple":false}` | `{"expenseCode":"01-95","hasTriple":true}` | The amount triple must be parsed from the same structural row as the expense code, not an adjacent/unrelated row. |

## docling

| check | pass | actual | expected | note |
|---|---|---|---|---|
| item_name_exact_match | FAIL | `"人件費 95016-2111-02-0000 職員基本給 02-0100 職員俸給"` | `"経済産業本省共通費"` | Only passes if the harness resolved a single unambiguous item-code row; see item_name_present_among_candidates for a diagnostic on ambiguous pages. |
| item_name_present_among_candidates | FAIL | `[{"itemCode":"001","itemName":"人件費 95016-2111-02-0000 職員基本給 02-0100 職員俸給"}]` | `{"itemCode":"010","itemName":"経済産業本省共通費"}` | Diagnostic only: on a page with multiple item-code-shaped rows, this checks whether the correct row was extracted and reconstructed correctly at all, independent of whether the harness's single-match selection resolved it into `result`. |
| expense_name_exact_match_after_line_join | FAIL | `null` | `"経済産業本省一般行政に必要な経費"` | Deterministic line-join only (common.mjs joinWrappedLabel); no semantic repair. |
| previous_budget_exact_match | FAIL | `null` | `42331005` |  |
| fy2024_request_exact_match | FAIL | `null` | `46887829` |  |
| signed_delta_exact_match | FAIL | `null` | `4556824` | FAIL here must mean the engine failed to preserve/associate the sign, not that we substituted the ground-truth sign. |
| unit_exact_match | PASS | `"千円"` | `"千円"` |  |
| page_identification | PASS | `8` | `8` |  |
| delta_glyph_observed_and_associated | FAIL | `null` | `"contains △"` | Checks the ground-truth-blind normalizer output, not the ground truth. A PASS means the △ glyph was genuinely present somewhere in the engine's own raw output and the deterministic normalizer associated it with this delta value. For a flat-line engine (pdfjs-baseline, pymupdf-baseline), deltaRaw is a single literal raw-line substring. For a table-cell engine (docling), deltaRaw may instead be a normalizer-constructed concatenation of two separate raw cells (a glyph-only cell and a magnitude cell) that the same table row placed together — still traceable to genuine raw engine output, never to the ground truth, but not necessarily one literal raw token. |
| item_to_amount_relationship | FAIL | `{"nearestPrecedingItemCode":null,"resultPreviousBudget":null}` | `{"itemCode":"010","previousBudget":42331005}` | The amount triple must belong to the expense row nested under the correct item-code row, not merely appear somewhere on the page. |
| expense_to_amount_relationship | FAIL | `null` | `{"expenseCode":"01-95","hasTriple":true}` | The amount triple must be parsed from the same structural row as the expense code, not an adjacent/unrelated row. |

