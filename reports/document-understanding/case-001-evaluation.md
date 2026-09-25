# Document Understanding Benchmark — case-001

Generated: 2026-09-25T22:38:28.948Z

| engine | passed | failed | total |
|---|---|---|---|
| pdfjs-baseline (4.10.38) | 8 | 3 | 11 |
| pymupdf-baseline (1.28.2) | 8 | 3 | 11 |

## pdfjs-baseline

| check | pass | actual | expected | note |
|---|---|---|---|---|
| item_name_exact_match | FAIL | `null` | `"情報通信技術調達等適正・効率化推進費"` | Only passes if the harness resolved a single unambiguous item-code row; see item_name_present_among_candidates for a diagnostic on ambiguous pages. |
| item_name_present_among_candidates | PASS | `[{"itemCode":"036","itemName":"公金受取口座登録業務支援経費"},{"itemCode":"041","itemName":"デジタル推進委員等環境整備事業費"},{"itemCode":"046","itemName":"デジタル臨時行政調査会事務局の運営等経費"},{"itemCode":"020","itemName":"情報通信技術調達等適正・効率化推進費"}]` | `{"itemCode":"020","itemName":"情報通信技術調達等適正・効率化推進費"}` | Diagnostic only: on a page with multiple item-code-shaped rows, this checks whether the correct row was extracted and reconstructed correctly at all, independent of whether the harness's single-match selection resolved it into `result`. |
| expense_name_exact_match_after_line_join | FAIL | `"情報通信技術調達等適正・効率化の推進に必要な （要求要旨）"` | `"情報通信技術調達等適正・効率化の推進に必要な経費"` | Deterministic line-join only (common.mjs joinWrappedLabel); no semantic repair. |
| previous_budget_exact_match | PASS | `481188232` | `481188232` |  |
| fy2024_request_exact_match | PASS | `448267326` | `448267326` |  |
| signed_delta_exact_match | PASS | `-32920906` | `-32920906` | FAIL here must mean the engine failed to preserve/associate the sign, not that we substituted the ground-truth sign. |
| unit_exact_match | FAIL | `null` | `"千円"` |  |
| page_identification | PASS | `11` | `11` |  |
| raw_delta_glyph_preserved | PASS | `"△ 32,920,906"` | `"contains △"` | Checks the RAW extracted token, not the ground truth. A pass here means the engine itself retained the decrease glyph. |
| item_to_amount_relationship | PASS | `{"nearestPrecedingItemCode":"020","resultPreviousBudget":481188232}` | `{"itemCode":"020","previousBudget":481188232}` | The amount triple must belong to the expense row nested under the correct item-code row, not merely appear somewhere on the page. |
| expense_to_amount_relationship | PASS | `{"expenseCode":"01-95","hasTriple":true}` | `{"expenseCode":"01-95","hasTriple":true}` | The amount triple must be parsed from the same structural row as the expense code, not an adjacent/unrelated row. |

## pymupdf-baseline

| check | pass | actual | expected | note |
|---|---|---|---|---|
| item_name_exact_match | FAIL | `null` | `"情報通信技術調達等適正・効率化推進費"` | Only passes if the harness resolved a single unambiguous item-code row; see item_name_present_among_candidates for a diagnostic on ambiguous pages. |
| item_name_present_among_candidates | PASS | `[{"itemCode":"036","itemName":"公金受取口座登録業務支援経費"},{"itemCode":"041","itemName":"デジタル推進委員等環境整備事業費"},{"itemCode":"046","itemName":"デジタル臨時行政調査会事務局の運営等経費"},{"itemCode":"020","itemName":"情報通信技術調達等適正・効率化推進費"}]` | `{"itemCode":"020","itemName":"情報通信技術調達等適正・効率化推進費"}` | Diagnostic only: on a page with multiple item-code-shaped rows, this checks whether the correct row was extracted and reconstructed correctly at all, independent of whether the harness's single-match selection resolved it into `result`. |
| expense_name_exact_match_after_line_join | FAIL | `"情報通信技術調達等適正・効率化の推進に必要な                                            （要求要旨）"` | `"情報通信技術調達等適正・効率化の推進に必要な経費"` | Deterministic line-join only (common.mjs joinWrappedLabel); no semantic repair. |
| previous_budget_exact_match | PASS | `481188232` | `481188232` |  |
| fy2024_request_exact_match | PASS | `448267326` | `448267326` |  |
| signed_delta_exact_match | PASS | `-32920906` | `-32920906` | FAIL here must mean the engine failed to preserve/associate the sign, not that we substituted the ground-truth sign. |
| unit_exact_match | FAIL | `null` | `"千円"` |  |
| page_identification | PASS | `11` | `11` |  |
| raw_delta_glyph_preserved | PASS | `"△     32,920,906"` | `"contains △"` | Checks the RAW extracted token, not the ground truth. A pass here means the engine itself retained the decrease glyph. |
| item_to_amount_relationship | PASS | `{"nearestPrecedingItemCode":"020","resultPreviousBudget":481188232}` | `{"itemCode":"020","previousBudget":481188232}` | The amount triple must belong to the expense row nested under the correct item-code row, not merely appear somewhere on the page. |
| expense_to_amount_relationship | PASS | `{"expenseCode":"01-95","hasTriple":true}` | `{"expenseCode":"01-95","hasTriple":true}` | The amount triple must be parsed from the same structural row as the expense code, not an adjacent/unrelated row. |

