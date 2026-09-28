# Document Understanding Benchmark — case-009

Generated: 2026-09-28T13:13:11.744Z

| engine | passed | failed | total |
|---|---|---|---|
| pdfjs-baseline (4.10.38) | 10 | 1 | 11 |
| pymupdf-baseline (1.28.2) | 10 | 1 | 11 |
| docling (2.130.0) | 8 | 3 | 11 |

The score alone is not the main result — see which *specific* checks differ below.

## Comparison matrix

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

## pdfjs-baseline

| check | pass | actual | expected | note |
|---|---|---|---|---|
| item_name_exact_match | FAIL | `null` | `"内閣本府共通費"` | Only passes if the harness resolved a single unambiguous item-code row; see item_name_present_among_candidates for a diagnostic on ambiguous pages. |
| item_name_present_among_candidates | PASS | `[{"itemCode":"010","itemName":"内閣本府"},{"itemCode":"010","itemName":"内閣本府共通費"},{"itemCode":"011","itemName":"経常事務費"},{"itemCode":"006","itemName":"総務課一般事務処理費 69,676 75,017 5,341 ３０年度元年度２年度３年度４年度( 73,159)( 78,884)( 69,907)( 81,632)( 71,218)"},{"itemCode":"016","itemName":"一般事務処理費"},{"itemCode":"001","itemName":"総務課行政特別推進費 8,430 8,431 1 ３０年度元年度２年度３年度４年度( 32,590)( 26,124)( 136,360)( 8,461)( 8,430)"}]` | `{"itemCode":"010","itemName":"内閣本府共通費"}` | Diagnostic only: on a page with multiple item-code-shaped rows, this checks whether the correct row was extracted and reconstructed correctly at all, independent of whether the harness's single-match selection resolved it into `result`. |
| expense_name_exact_match_after_line_join | PASS | `"内閣本府一般行政に必要な経費"` | `"内閣本府一般行政に必要な経費"` | Deterministic line-join only (common.mjs joinWrappedLabel); no semantic repair. |
| previous_budget_exact_match | PASS | `79533` | `79533` |  |
| fy2024_request_exact_match | PASS | `84991` | `84991` |  |
| signed_delta_exact_match | PASS | `5458` | `5458` | FAIL here must mean the engine failed to preserve/associate the sign, not that we substituted the ground-truth sign. |
| unit_exact_match | PASS | `"千円"` | `"千円"` |  |
| page_identification | PASS | `0` | `0` |  |
| delta_sign_evidence_matches_source | PASS | `"5,458"` | `"does not contain △ (source-derived Ground Truth deltaRaw carries no decrease glyph)"` | Checks whether the ground-truth-blind normalizer output's observed sign evidence agrees with the source-derived Ground Truth's own deltaRaw glyph state — in either direction, not only "glyph present". This check is narrowly about glyph-fabrication avoidance, not overall delta-extraction completeness (see signed_delta_exact_match / previous_budget_exact_match / fy2024_request_exact_match for that): when Ground Truth expects no glyph, a null deltaRaw (nothing extracted, nothing fabricated) also PASSes this specific check, because no false decrease indicator was introduced — it is not evidence that the engine successfully recovered the delta value. A PASS when a glyph IS expected still requires the glyph to be genuinely present in the engine's own raw output and associated with this delta value by the deterministic normalizer, exactly as before. For a flat-line engine (pdfjs-baseline, pymupdf-baseline), a present deltaRaw is a single literal raw-line substring. For a table-cell engine (docling), a present deltaRaw may instead be a normalizer-constructed concatenation of two separate raw cells (a glyph-only cell and a magnitude cell) that the same table row placed together — still traceable to genuine raw engine output, never to the ground truth, but not necessarily one literal raw token. |
| item_to_amount_relationship | PASS | `{"nearestPrecedingItemCode":"010","resultPreviousBudget":79533}` | `{"itemCode":"010","previousBudget":79533}` | The amount triple must belong to the expense row nested under the correct item-code row, not merely appear somewhere on the page. |
| expense_to_amount_relationship | PASS | `{"expenseCode":"01-95","hasTriple":true}` | `{"expenseCode":"01-95","hasTriple":true}` | The amount triple must be parsed from the same structural row as the expense code, not an adjacent/unrelated row. |
## pymupdf-baseline

| check | pass | actual | expected | note |
|---|---|---|---|---|
| item_name_exact_match | FAIL | `null` | `"内閣本府共通費"` | Only passes if the harness resolved a single unambiguous item-code row; see item_name_present_among_candidates for a diagnostic on ambiguous pages. |
| item_name_present_among_candidates | PASS | `[{"itemCode":"010","itemName":"内閣本府"},{"itemCode":"010","itemName":"内閣本府共通費"},{"itemCode":"011","itemName":"経常事務費"},{"itemCode":"006","itemName":"総務課一般事務処理費                  69,676         75,017                                        5,341          ３０年度元年度２年度３年度４年度(        73,159) (        78,884) (        69,907) (        81,632) (        71,218)"},{"itemCode":"016","itemName":"一般事務処理費"},{"itemCode":"001","itemName":"総務課行政特別推進費                   8,430          8,431                                            1          ３０年度元年度２年度３年度４年度(        32,590) (        26,124) (       136,360) (         8,461) (         8,430)"}]` | `{"itemCode":"010","itemName":"内閣本府共通費"}` | Diagnostic only: on a page with multiple item-code-shaped rows, this checks whether the correct row was extracted and reconstructed correctly at all, independent of whether the harness's single-match selection resolved it into `result`. |
| expense_name_exact_match_after_line_join | PASS | `"内閣本府一般行政に必要な経費"` | `"内閣本府一般行政に必要な経費"` | Deterministic line-join only (common.mjs joinWrappedLabel); no semantic repair. |
| previous_budget_exact_match | PASS | `79533` | `79533` |  |
| fy2024_request_exact_match | PASS | `84991` | `84991` |  |
| signed_delta_exact_match | PASS | `5458` | `5458` | FAIL here must mean the engine failed to preserve/associate the sign, not that we substituted the ground-truth sign. |
| unit_exact_match | PASS | `"千円"` | `"千円"` |  |
| page_identification | PASS | `0` | `0` |  |
| delta_sign_evidence_matches_source | PASS | `"5,458"` | `"does not contain △ (source-derived Ground Truth deltaRaw carries no decrease glyph)"` | Checks whether the ground-truth-blind normalizer output's observed sign evidence agrees with the source-derived Ground Truth's own deltaRaw glyph state — in either direction, not only "glyph present". This check is narrowly about glyph-fabrication avoidance, not overall delta-extraction completeness (see signed_delta_exact_match / previous_budget_exact_match / fy2024_request_exact_match for that): when Ground Truth expects no glyph, a null deltaRaw (nothing extracted, nothing fabricated) also PASSes this specific check, because no false decrease indicator was introduced — it is not evidence that the engine successfully recovered the delta value. A PASS when a glyph IS expected still requires the glyph to be genuinely present in the engine's own raw output and associated with this delta value by the deterministic normalizer, exactly as before. For a flat-line engine (pdfjs-baseline, pymupdf-baseline), a present deltaRaw is a single literal raw-line substring. For a table-cell engine (docling), a present deltaRaw may instead be a normalizer-constructed concatenation of two separate raw cells (a glyph-only cell and a magnitude cell) that the same table row placed together — still traceable to genuine raw engine output, never to the ground truth, but not necessarily one literal raw token. |
| item_to_amount_relationship | PASS | `{"nearestPrecedingItemCode":"010","resultPreviousBudget":79533}` | `{"itemCode":"010","previousBudget":79533}` | The amount triple must belong to the expense row nested under the correct item-code row, not merely appear somewhere on the page. |
| expense_to_amount_relationship | PASS | `{"expenseCode":"01-95","hasTriple":true}` | `{"expenseCode":"01-95","hasTriple":true}` | The amount triple must be parsed from the same structural row as the expense code, not an adjacent/unrelated row. |

## docling

| check | pass | actual | expected | note |
|---|---|---|---|---|
| item_name_exact_match | FAIL | `null` | `"内閣本府共通費"` | Only passes if the harness resolved a single unambiguous item-code row; see item_name_present_among_candidates for a diagnostic on ambiguous pages. |
| item_name_present_among_candidates | FAIL | `[{"itemCode":"011","itemName":"経常事務費 006 総務課一般事務処理費"},{"itemCode":"001","itemName":"総務課行政特別推進費"}]` | `{"itemCode":"010","itemName":"内閣本府共通費"}` | Diagnostic only: on a page with multiple item-code-shaped rows, this checks whether the correct row was extracted and reconstructed correctly at all, independent of whether the harness's single-match selection resolved it into `result`. |
| expense_name_exact_match_after_line_join | PASS | `"内閣本府一般行政に必要な経費"` | `"内閣本府一般行政に必要な経費"` | Deterministic line-join only (common.mjs joinWrappedLabel); no semantic repair. |
| previous_budget_exact_match | PASS | `79533` | `79533` |  |
| fy2024_request_exact_match | PASS | `84991` | `84991` |  |
| signed_delta_exact_match | PASS | `5458` | `5458` | FAIL here must mean the engine failed to preserve/associate the sign, not that we substituted the ground-truth sign. |
| unit_exact_match | PASS | `"千円"` | `"千円"` |  |
| page_identification | PASS | `0` | `0` |  |
| delta_sign_evidence_matches_source | PASS | `"458 5,"` | `"does not contain △ (source-derived Ground Truth deltaRaw carries no decrease glyph)"` | Checks whether the ground-truth-blind normalizer output's observed sign evidence agrees with the source-derived Ground Truth's own deltaRaw glyph state — in either direction, not only "glyph present". This check is narrowly about glyph-fabrication avoidance, not overall delta-extraction completeness (see signed_delta_exact_match / previous_budget_exact_match / fy2024_request_exact_match for that): when Ground Truth expects no glyph, a null deltaRaw (nothing extracted, nothing fabricated) also PASSes this specific check, because no false decrease indicator was introduced — it is not evidence that the engine successfully recovered the delta value. A PASS when a glyph IS expected still requires the glyph to be genuinely present in the engine's own raw output and associated with this delta value by the deterministic normalizer, exactly as before. For a flat-line engine (pdfjs-baseline, pymupdf-baseline), a present deltaRaw is a single literal raw-line substring. For a table-cell engine (docling), a present deltaRaw may instead be a normalizer-constructed concatenation of two separate raw cells (a glyph-only cell and a magnitude cell) that the same table row placed together — still traceable to genuine raw engine output, never to the ground truth, but not necessarily one literal raw token. |
| item_to_amount_relationship | FAIL | `{"nearestPrecedingItemCode":null,"resultPreviousBudget":79533}` | `{"itemCode":"010","previousBudget":79533}` | The amount triple must belong to the expense row nested under the correct item-code row, not merely appear somewhere on the page. |
| expense_to_amount_relationship | PASS | `{"expenseCode":"01-95","hasTriple":true}` | `{"expenseCode":"01-95","hasTriple":true}` | The amount triple must be parsed from the same structural row as the expense code, not an adjacent/unrelated row. |
