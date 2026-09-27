# Document Understanding Benchmark — case-006

Generated: 2026-09-27T23:16:29.973Z

| engine | passed | failed | total |
|---|---|---|---|
| pdfjs-baseline (4.10.38) | 2 | 9 | 11 |
| pymupdf-baseline (1.28.2) | 2 | 9 | 11 |
| docling (2.130.0) | 2 | 9 | 11 |

The score alone is not the main result — see which *specific* checks differ below.

## Comparison matrix

| check | pdfjs-baseline | pymupdf-baseline | docling |
|---|---|---|---|
| item_name_exact_match | FAIL | FAIL | FAIL |
| item_name_present_among_candidates | FAIL | FAIL | FAIL |
| expense_name_exact_match_after_line_join | FAIL | FAIL | FAIL |
| previous_budget_exact_match | FAIL | FAIL | FAIL |
| fy2024_request_exact_match | FAIL | FAIL | FAIL |
| signed_delta_exact_match | FAIL | FAIL | FAIL |
| unit_exact_match | FAIL | FAIL | FAIL |
| page_identification | PASS | PASS | PASS |
| delta_sign_evidence_matches_source | PASS | PASS | PASS |
| item_to_amount_relationship | FAIL | FAIL | FAIL |
| expense_to_amount_relationship | FAIL | FAIL | FAIL |

## pdfjs-baseline

| check | pass | actual | expected | note |
|---|---|---|---|---|
| item_name_exact_match | FAIL | `null` | `"法務本省共通費"` | Only passes if the harness resolved a single unambiguous item-code row; see item_name_present_among_candidates for a diagnostic on ambiguous pages. |
| item_name_present_among_candidates | FAIL | `[]` | `{"itemCode":"010","itemName":"法務本省共通費"}` | Diagnostic only: on a page with multiple item-code-shaped rows, this checks whether the correct row was extracted and reconstructed correctly at all, independent of whether the harness's single-match selection resolved it into `result`. |
| expense_name_exact_match_after_line_join | FAIL | `null` | `"法務本省一般行政に必要な経費"` | Deterministic line-join only (common.mjs joinWrappedLabel); no semantic repair. |
| previous_budget_exact_match | FAIL | `null` | `112183723` |  |
| fy2024_request_exact_match | FAIL | `null` | `131650389` |  |
| signed_delta_exact_match | FAIL | `null` | `19466666` | FAIL here must mean the engine failed to preserve/associate the sign, not that we substituted the ground-truth sign. |
| unit_exact_match | FAIL | `null` | `"千円"` |  |
| page_identification | PASS | `8` | `8` |  |
| delta_sign_evidence_matches_source | PASS | `null` | `"does not contain △ (source-derived Ground Truth deltaRaw carries no decrease glyph)"` | Checks whether the ground-truth-blind normalizer output's observed sign evidence agrees with the source-derived Ground Truth's own deltaRaw glyph state — in either direction, not only "glyph present". This check is narrowly about glyph-fabrication avoidance, not overall delta-extraction completeness (see signed_delta_exact_match / previous_budget_exact_match / fy2024_request_exact_match for that): when Ground Truth expects no glyph, a null deltaRaw (nothing extracted, nothing fabricated) also PASSes this specific check, because no false decrease indicator was introduced — it is not evidence that the engine successfully recovered the delta value. A PASS when a glyph IS expected still requires the glyph to be genuinely present in the engine's own raw output and associated with this delta value by the deterministic normalizer, exactly as before. For a flat-line engine (pdfjs-baseline, pymupdf-baseline), a present deltaRaw is a single literal raw-line substring. For a table-cell engine (docling), a present deltaRaw may instead be a normalizer-constructed concatenation of two separate raw cells (a glyph-only cell and a magnitude cell) that the same table row placed together — still traceable to genuine raw engine output, never to the ground truth, but not necessarily one literal raw token. |
| item_to_amount_relationship | FAIL | `{"nearestPrecedingItemCode":null,"resultPreviousBudget":null}` | `{"itemCode":"010","previousBudget":112183723}` | The amount triple must belong to the expense row nested under the correct item-code row, not merely appear somewhere on the page. |
| expense_to_amount_relationship | FAIL | `null` | `{"expenseCode":"01-95","hasTriple":true}` | The amount triple must be parsed from the same structural row as the expense code, not an adjacent/unrelated row. |

## pymupdf-baseline

| check | pass | actual | expected | note |
|---|---|---|---|---|
| item_name_exact_match | FAIL | `null` | `"法務本省共通費"` | Only passes if the harness resolved a single unambiguous item-code row; see item_name_present_among_candidates for a diagnostic on ambiguous pages. |
| item_name_present_among_candidates | FAIL | `[]` | `{"itemCode":"010","itemName":"法務本省共通費"}` | Diagnostic only: on a page with multiple item-code-shaped rows, this checks whether the correct row was extracted and reconstructed correctly at all, independent of whether the harness's single-match selection resolved it into `result`. |
| expense_name_exact_match_after_line_join | FAIL | `null` | `"法務本省一般行政に必要な経費"` | Deterministic line-join only (common.mjs joinWrappedLabel); no semantic repair. |
| previous_budget_exact_match | FAIL | `null` | `112183723` |  |
| fy2024_request_exact_match | FAIL | `null` | `131650389` |  |
| signed_delta_exact_match | FAIL | `null` | `19466666` | FAIL here must mean the engine failed to preserve/associate the sign, not that we substituted the ground-truth sign. |
| unit_exact_match | FAIL | `null` | `"千円"` |  |
| page_identification | PASS | `8` | `8` |  |
| delta_sign_evidence_matches_source | PASS | `null` | `"does not contain △ (source-derived Ground Truth deltaRaw carries no decrease glyph)"` | Checks whether the ground-truth-blind normalizer output's observed sign evidence agrees with the source-derived Ground Truth's own deltaRaw glyph state — in either direction, not only "glyph present". This check is narrowly about glyph-fabrication avoidance, not overall delta-extraction completeness (see signed_delta_exact_match / previous_budget_exact_match / fy2024_request_exact_match for that): when Ground Truth expects no glyph, a null deltaRaw (nothing extracted, nothing fabricated) also PASSes this specific check, because no false decrease indicator was introduced — it is not evidence that the engine successfully recovered the delta value. A PASS when a glyph IS expected still requires the glyph to be genuinely present in the engine's own raw output and associated with this delta value by the deterministic normalizer, exactly as before. For a flat-line engine (pdfjs-baseline, pymupdf-baseline), a present deltaRaw is a single literal raw-line substring. For a table-cell engine (docling), a present deltaRaw may instead be a normalizer-constructed concatenation of two separate raw cells (a glyph-only cell and a magnitude cell) that the same table row placed together — still traceable to genuine raw engine output, never to the ground truth, but not necessarily one literal raw token. |
| item_to_amount_relationship | FAIL | `{"nearestPrecedingItemCode":null,"resultPreviousBudget":null}` | `{"itemCode":"010","previousBudget":112183723}` | The amount triple must belong to the expense row nested under the correct item-code row, not merely appear somewhere on the page. |
| expense_to_amount_relationship | FAIL | `null` | `{"expenseCode":"01-95","hasTriple":true}` | The amount triple must be parsed from the same structural row as the expense code, not an adjacent/unrelated row. |

## docling

| check | pass | actual | expected | note |
|---|---|---|---|---|
| item_name_exact_match | FAIL | `"法"` | `"法務本省共通費"` | Only passes if the harness resolved a single unambiguous item-code row; see item_name_present_among_candidates for a diagnostic on ambiguous pages. |
| item_name_present_among_candidates | FAIL | `[{"itemCode":"010","itemName":"法"}]` | `{"itemCode":"010","itemName":"法務本省共通費"}` | Diagnostic only: on a page with multiple item-code-shaped rows, this checks whether the correct row was extracted and reconstructed correctly at all, independent of whether the harness's single-match selection resolved it into `result`. |
| expense_name_exact_match_after_line_join | FAIL | `"な経費 001 001人"` | `"法務本省一般行政に必要な経費"` | Deterministic line-join only (common.mjs joinWrappedLabel); no semantic repair. |
| previous_budget_exact_match | FAIL | `null` | `112183723` |  |
| fy2024_request_exact_match | FAIL | `null` | `131650389` |  |
| signed_delta_exact_match | FAIL | `null` | `19466666` | FAIL here must mean the engine failed to preserve/associate the sign, not that we substituted the ground-truth sign. |
| unit_exact_match | FAIL | `null` | `"千円"` |  |
| page_identification | PASS | `8` | `8` |  |
| delta_sign_evidence_matches_source | PASS | `null` | `"does not contain △ (source-derived Ground Truth deltaRaw carries no decrease glyph)"` | Checks whether the ground-truth-blind normalizer output's observed sign evidence agrees with the source-derived Ground Truth's own deltaRaw glyph state — in either direction, not only "glyph present". This check is narrowly about glyph-fabrication avoidance, not overall delta-extraction completeness (see signed_delta_exact_match / previous_budget_exact_match / fy2024_request_exact_match for that): when Ground Truth expects no glyph, a null deltaRaw (nothing extracted, nothing fabricated) also PASSes this specific check, because no false decrease indicator was introduced — it is not evidence that the engine successfully recovered the delta value. A PASS when a glyph IS expected still requires the glyph to be genuinely present in the engine's own raw output and associated with this delta value by the deterministic normalizer, exactly as before. For a flat-line engine (pdfjs-baseline, pymupdf-baseline), a present deltaRaw is a single literal raw-line substring. For a table-cell engine (docling), a present deltaRaw may instead be a normalizer-constructed concatenation of two separate raw cells (a glyph-only cell and a magnitude cell) that the same table row placed together — still traceable to genuine raw engine output, never to the ground truth, but not necessarily one literal raw token. |
| item_to_amount_relationship | FAIL | `{"nearestPrecedingItemCode":"010","resultPreviousBudget":null}` | `{"itemCode":"010","previousBudget":112183723}` | The amount triple must belong to the expense row nested under the correct item-code row, not merely appear somewhere on the page. |
| expense_to_amount_relationship | FAIL | `{"expenseCode":"01-95","hasTriple":false}` | `{"expenseCode":"01-95","hasTriple":true}` | The amount triple must be parsed from the same structural row as the expense code, not an adjacent/unrelated row. |

