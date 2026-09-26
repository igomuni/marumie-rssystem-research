# Document Understanding Benchmark — case-001

Generated: 2026-09-26T09:13:48.622Z

| engine | passed | failed | total |
|---|---|---|---|
| pdfjs-baseline (4.10.38) | 8 | 3 | 11 |
| pymupdf-baseline (1.28.2) | 8 | 3 | 11 |
| docling (2.130.0) | 9 | 2 | 11 |

The score alone is not the main result — see which *specific* checks differ below.

## Comparison matrix

| check | pdfjs-baseline | pymupdf-baseline | docling |
|---|---|---|---|
| item_name_exact_match | FAIL | FAIL | FAIL |
| item_name_present_among_candidates | PASS | PASS | PASS |
| expense_name_exact_match_after_line_join | FAIL | FAIL | PASS |
| previous_budget_exact_match | PASS | PASS | PASS |
| fy2024_request_exact_match | PASS | PASS | PASS |
| signed_delta_exact_match | PASS | PASS | PASS |
| unit_exact_match | FAIL | FAIL | FAIL |
| page_identification | PASS | PASS | PASS |
| delta_sign_evidence_matches_source | PASS | PASS | PASS |
| item_to_amount_relationship | PASS | PASS | PASS |
| expense_to_amount_relationship | PASS | PASS | PASS |

## pdfjs-baseline

| check | pass | actual | expected | note |
|---|---|---|---|---|
| item_name_exact_match | FAIL | `null` | `"情報通信技術調達等適正・効率化推進費"` | Only passes if the harness resolved a single unambiguous item-code row; see item_name_present_among_candidates for a diagnostic on ambiguous pages. |
| item_name_present_among_candidates | PASS | `[{"itemCode":"036","itemName":"公金受取口座登録業務支援経費"},{"itemCode":"041","itemName":"デジタル推進委員等環境整備事業費"},{"itemCode":"046","itemName":"デジタル臨時行政調査会事務局の運営等経費"},{"itemCode":"020","itemName":"情報通信技術調達等適正・効率化推進費"}]` | `{"itemCode":"020","itemName":"情報通信技術調達等適正・効率化推進費"}` | Diagnostic only: on a page with multiple item-code-shaped rows, this checks whether the correct row was extracted and reconstructed correctly at all, independent of whether the harness's single-match selection resolved it into `result`. |
| expense_name_exact_match_after_line_join | FAIL | `"情報通信技術調達等適正・効率化の推進に必要な（要求要旨）"` | `"情報通信技術調達等適正・効率化の推進に必要な経費"` | Deterministic line-join only (common.mjs joinWrappedLabel); no semantic repair. |
| previous_budget_exact_match | PASS | `481188232` | `481188232` |  |
| fy2024_request_exact_match | PASS | `448267326` | `448267326` |  |
| signed_delta_exact_match | PASS | `-32920906` | `-32920906` | FAIL here must mean the engine failed to preserve/associate the sign, not that we substituted the ground-truth sign. |
| unit_exact_match | FAIL | `null` | `"千円"` |  |
| page_identification | PASS | `11` | `11` |  |
| delta_sign_evidence_matches_source | PASS | `"△ 32,920,906"` | `"contains △ (source-derived Ground Truth deltaRaw carries the decrease glyph)"` | Checks whether the ground-truth-blind normalizer output's observed sign evidence agrees with the source-derived Ground Truth's own deltaRaw glyph state — in either direction, not only "glyph present". This check is narrowly about glyph-fabrication avoidance, not overall delta-extraction completeness (see signed_delta_exact_match / previous_budget_exact_match / fy2024_request_exact_match for that): when Ground Truth expects no glyph, a null deltaRaw (nothing extracted, nothing fabricated) also PASSes this specific check, because no false decrease indicator was introduced — it is not evidence that the engine successfully recovered the delta value. A PASS when a glyph IS expected still requires the glyph to be genuinely present in the engine's own raw output and associated with this delta value by the deterministic normalizer, exactly as before. For a flat-line engine (pdfjs-baseline, pymupdf-baseline), a present deltaRaw is a single literal raw-line substring. For a table-cell engine (docling), a present deltaRaw may instead be a normalizer-constructed concatenation of two separate raw cells (a glyph-only cell and a magnitude cell) that the same table row placed together — still traceable to genuine raw engine output, never to the ground truth, but not necessarily one literal raw token. |
| item_to_amount_relationship | PASS | `{"nearestPrecedingItemCode":"020","resultPreviousBudget":481188232}` | `{"itemCode":"020","previousBudget":481188232}` | The amount triple must belong to the expense row nested under the correct item-code row, not merely appear somewhere on the page. |
| expense_to_amount_relationship | PASS | `{"expenseCode":"01-95","hasTriple":true}` | `{"expenseCode":"01-95","hasTriple":true}` | The amount triple must be parsed from the same structural row as the expense code, not an adjacent/unrelated row. |

## pymupdf-baseline

| check | pass | actual | expected | note |
|---|---|---|---|---|
| item_name_exact_match | FAIL | `null` | `"情報通信技術調達等適正・効率化推進費"` | Only passes if the harness resolved a single unambiguous item-code row; see item_name_present_among_candidates for a diagnostic on ambiguous pages. |
| item_name_present_among_candidates | PASS | `[{"itemCode":"036","itemName":"公金受取口座登録業務支援経費"},{"itemCode":"041","itemName":"デジタル推進委員等環境整備事業費"},{"itemCode":"046","itemName":"デジタル臨時行政調査会事務局の運営等経費"},{"itemCode":"020","itemName":"情報通信技術調達等適正・効率化推進費"}]` | `{"itemCode":"020","itemName":"情報通信技術調達等適正・効率化推進費"}` | Diagnostic only: on a page with multiple item-code-shaped rows, this checks whether the correct row was extracted and reconstructed correctly at all, independent of whether the harness's single-match selection resolved it into `result`. |
| expense_name_exact_match_after_line_join | FAIL | `"情報通信技術調達等適正・効率化の推進に必要な（要求要旨）"` | `"情報通信技術調達等適正・効率化の推進に必要な経費"` | Deterministic line-join only (common.mjs joinWrappedLabel); no semantic repair. |
| previous_budget_exact_match | PASS | `481188232` | `481188232` |  |
| fy2024_request_exact_match | PASS | `448267326` | `448267326` |  |
| signed_delta_exact_match | PASS | `-32920906` | `-32920906` | FAIL here must mean the engine failed to preserve/associate the sign, not that we substituted the ground-truth sign. |
| unit_exact_match | FAIL | `null` | `"千円"` |  |
| page_identification | PASS | `11` | `11` |  |
| delta_sign_evidence_matches_source | PASS | `"△     32,920,906"` | `"contains △ (source-derived Ground Truth deltaRaw carries the decrease glyph)"` | Checks whether the ground-truth-blind normalizer output's observed sign evidence agrees with the source-derived Ground Truth's own deltaRaw glyph state — in either direction, not only "glyph present". This check is narrowly about glyph-fabrication avoidance, not overall delta-extraction completeness (see signed_delta_exact_match / previous_budget_exact_match / fy2024_request_exact_match for that): when Ground Truth expects no glyph, a null deltaRaw (nothing extracted, nothing fabricated) also PASSes this specific check, because no false decrease indicator was introduced — it is not evidence that the engine successfully recovered the delta value. A PASS when a glyph IS expected still requires the glyph to be genuinely present in the engine's own raw output and associated with this delta value by the deterministic normalizer, exactly as before. For a flat-line engine (pdfjs-baseline, pymupdf-baseline), a present deltaRaw is a single literal raw-line substring. For a table-cell engine (docling), a present deltaRaw may instead be a normalizer-constructed concatenation of two separate raw cells (a glyph-only cell and a magnitude cell) that the same table row placed together — still traceable to genuine raw engine output, never to the ground truth, but not necessarily one literal raw token. |
| item_to_amount_relationship | PASS | `{"nearestPrecedingItemCode":"020","resultPreviousBudget":481188232}` | `{"itemCode":"020","previousBudget":481188232}` | The amount triple must belong to the expense row nested under the correct item-code row, not merely appear somewhere on the page. |
| expense_to_amount_relationship | PASS | `{"expenseCode":"01-95","hasTriple":true}` | `{"expenseCode":"01-95","hasTriple":true}` | The amount triple must be parsed from the same structural row as the expense code, not an adjacent/unrelated row. |

## docling

| check | pass | actual | expected | note |
|---|---|---|---|---|
| item_name_exact_match | FAIL | `null` | `"情報通信技術調達等適正・効率化推進費"` | Only passes if the harness resolved a single unambiguous item-code row; see item_name_present_among_candidates for a diagnostic on ambiguous pages. |
| item_name_present_among_candidates | PASS | `[{"itemCode":"036","itemName":"公金受取口座登録業務支援経費 95016-2123-09-1040 情報処理業務庁費 041 デジタル推進委員等環境"},{"itemCode":"046","itemName":"デジタル臨時行政調査会事務局の運営等経費"},{"itemCode":"020","itemName":"情報通信技術調達等適正・効率化推進費"}]` | `{"itemCode":"020","itemName":"情報通信技術調達等適正・効率化推進費"}` | Diagnostic only: on a page with multiple item-code-shaped rows, this checks whether the correct row was extracted and reconstructed correctly at all, independent of whether the harness's single-match selection resolved it into `result`. |
| expense_name_exact_match_after_line_join | PASS | `"情報通信技術調達等適正・効率化の推進に必要な経費"` | `"情報通信技術調達等適正・効率化の推進に必要な経費"` | Deterministic line-join only (common.mjs joinWrappedLabel); no semantic repair. |
| previous_budget_exact_match | PASS | `481188232` | `481188232` |  |
| fy2024_request_exact_match | PASS | `448267326` | `448267326` |  |
| signed_delta_exact_match | PASS | `-32920906` | `-32920906` | FAIL here must mean the engine failed to preserve/associate the sign, not that we substituted the ground-truth sign. |
| unit_exact_match | FAIL | `null` | `"千円"` |  |
| page_identification | PASS | `11` | `11` |  |
| delta_sign_evidence_matches_source | PASS | `"△ 906 920, 32,"` | `"contains △ (source-derived Ground Truth deltaRaw carries the decrease glyph)"` | Checks whether the ground-truth-blind normalizer output's observed sign evidence agrees with the source-derived Ground Truth's own deltaRaw glyph state — in either direction, not only "glyph present". This check is narrowly about glyph-fabrication avoidance, not overall delta-extraction completeness (see signed_delta_exact_match / previous_budget_exact_match / fy2024_request_exact_match for that): when Ground Truth expects no glyph, a null deltaRaw (nothing extracted, nothing fabricated) also PASSes this specific check, because no false decrease indicator was introduced — it is not evidence that the engine successfully recovered the delta value. A PASS when a glyph IS expected still requires the glyph to be genuinely present in the engine's own raw output and associated with this delta value by the deterministic normalizer, exactly as before. For a flat-line engine (pdfjs-baseline, pymupdf-baseline), a present deltaRaw is a single literal raw-line substring. For a table-cell engine (docling), a present deltaRaw may instead be a normalizer-constructed concatenation of two separate raw cells (a glyph-only cell and a magnitude cell) that the same table row placed together — still traceable to genuine raw engine output, never to the ground truth, but not necessarily one literal raw token. |
| item_to_amount_relationship | PASS | `{"nearestPrecedingItemCode":"020","resultPreviousBudget":481188232}` | `{"itemCode":"020","previousBudget":481188232}` | The amount triple must belong to the expense row nested under the correct item-code row, not merely appear somewhere on the page. |
| expense_to_amount_relationship | PASS | `{"expenseCode":"01-95","hasTriple":true}` | `{"expenseCode":"01-95","hasTriple":true}` | The amount triple must be parsed from the same structural row as the expense code, not an adjacent/unrelated row. |

