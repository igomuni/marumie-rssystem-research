# case-002 — First Frozen Out-of-Sample Benchmark Run

**This is the first-ever execution of the unchanged, case-001-derived Document Understanding pipeline against `case-002`.** No code was changed after seeing this result. This report records what happened, without repair.

Date: 2026-09-26 (Asia/Tokyo)

Ground Truth freeze commit: `5a2eb32`
Benchmark execution/report commit: filled in after commit (see `state/CHANGELOG.md` for the SHA)
Source SHA-256: `ba64c25df327161a33c293374a7255c203cc9a527130ece848574badefbf909a` (`meti-fy2024-general-account-request`)

Compact machine-generated artifacts (produced by the unmodified `run.mjs`, same as `case-001`'s): `evidence/document-understanding/case-002-results.json`, `reports/document-understanding/case-002-evaluation.md`. This document adds the narrative interpretation those two do not contain.

## Pre-run verification

- Branch `research/case-002-meti-preregistration` at `5a2eb32` (clean working tree) before this task's first edit.
- `git log 5a2eb32..HEAD -- scripts/document-understanding/` was empty: no benchmark code changed since the Ground Truth freeze.
- `fixtures/document-understanding/case-002/ground-truth.json` unchanged since `5a2eb32`.
- Local `sources/raw/meti-fy2024-general-account-request.pdf` SHA-256 independently re-verified against `sources/source-lock.json`: exact match.

## Harness plumbing note (case-generic, not case-002-specific)

`scripts/document-understanding/benchmark/src/run.mjs`, both normalizers, and all three adapters already take `caseId` as a parameter with **zero case-001 hardcoding** — `npm run docbench -- case-002` worked with no code change whatsoever.

One *prerequisite data-generation step* was required, not a code change: `scripts/pdf-extraction` (which `pdfjs-baseline` reuses) had only ever been run against the two original Digital Agency PDFs; its output simply didn't include `meti-fy2024-general-account-request` yet, because `npm run extract` had not been re-run since METI was added to `sources/source-lock.json` in an earlier task. Running the existing, unmodified `npm run extract` (already documented in `scripts/document-understanding/README.md`'s "Running the benchmark" section as a required step before `pdfjs-baseline` can run) reprocessed **all three** locked sources. The two original PDFs produced byte-identical line-reconstruction hashes to before (`bd29feaef177e...`, `3688fcc7942df...` — unchanged), confirming this was purely a missing prerequisite run, not a semantic or code change, and did not touch existing behavior for `case-001`.

No other file was modified to make case-002 executable.

## First-run comparison matrix

```text
check                                      pdfjs   pymupdf   docling
item_name_exact_match                      FAIL    FAIL      FAIL
item_name_present_among_candidates         FAIL    PASS      FAIL
expense_name_exact_match_after_line_join   FAIL    FAIL      FAIL
previous_budget_exact_match                FAIL    FAIL      FAIL
fy2024_request_exact_match                 FAIL    FAIL      FAIL
signed_delta_exact_match                   FAIL    FAIL      FAIL
unit_exact_match                           PASS    PASS      PASS
page_identification                        PASS    PASS      PASS
delta_glyph_observed_and_associated        FAIL    FAIL      FAIL
item_to_amount_relationship                FAIL    FAIL      FAIL
expense_to_amount_relationship             FAIL    FAIL      FAIL
```

Scores: **pdfjs-baseline 2/11, pymupdf-baseline 3/11, docling 2/11** — a severe regression from `case-001`'s 8/11, 8/11, 9/11. This is recorded as-is; no tuning was attempted.

## Raw vs. normalized findings, per engine

### pdfjs-baseline and pymupdf-baseline

Both reconstructed the target line correctly and completely at the raw stage:

```text
"1 01-95 経済産業本省一般行政に 42,331,005 46,887,829 4,556,824 （要求要旨）"
"必要な経費 「経済産業省設置法」に定める本省内部部局所掌の一般事務を処理するため必要な庁費等"
```

(pdfjs-baseline; pymupdf-baseline's raw text is the same content with different whitespace.) The requestNo (`1`) and expenseCode (`01-95`) were correctly parsed. But `common.mjs`'s `splitTrailingTriple` requires the amount triple to be the **literal end** of the line (anchored `\s*$`), and here the annotation column text `（要求要旨）` follows the triple on the *same* reconstructed line — unlike `case-001`, where the annotation text only ever appeared on *continuation* lines, after the triple had already been successfully split off the initial row. Because the trailing-triple regex doesn't match, `previousBudget`/`fy2024Request`/`deltaRaw`/`delta` are all correctly recorded as `null` (a real miss, not a silent zero), and the unparsed remainder (label + numbers + annotation) is treated as `expenseNameFragment`, which `joinWrappedLabel` then extends by one more line — pulling in the *rest* of the annotation. Net effect: `expenseName` is a large garbled string containing the numbers and the full annotation text, not a name.

This is a genuinely new failure mode, not the same one `case-001` exposed: in `case-001`, the triple parsed cleanly and only the *label* wrapping got contaminated by a neighboring column on a later line. Here, the annotation column contaminates the *same* line as the triple, breaking triple extraction itself, before name reconstruction is even reached.

`item_name_present_among_candidates` diverges between the two engines for an unrelated, independently interesting reason: both found the same 4 item-code-shaped candidates (`010`/`010`/`001`/`001` — the header-hierarchy ambiguity persists, see H6), but pdfjs-dist's line reconstruction inserted a literal space between every CJK character in header-style rows (`"経 済 産 業 本 省 共 通 費"`), the same letter-spacing artifact discovered in Workspace Phase 1D's PDF-extraction work — while PyMuPDF's `sort=True` reconstruction did not, producing the compact `"経済産業本省共通費"` that exact-matches Ground Truth. **This exposes a real asymmetry in the current benchmark that case-001 never surfaced**: `normalize-docling.mjs` has a `closeCjkWrapSpaces` step; `common.mjs`/`normalize.mjs` (used by both flat-text baselines) has no equivalent CJK-space-closing step at all. `evaluate.mjs`'s `item_name_present_among_candidates` check does a plain `===` string comparison against the candidate's `itemNameFragment`, so this single difference in an unrelated document's line-reconstruction spacing is enough to flip PASS/FAIL for a check that has nothing to do with amounts or signs.

### docling

Docling's TableFormer built a **23×12 grid** for this page (`case-001`'s page was 21×14) and logged: `1 of 322 pdf cells matched neither a row nor a column band of the 24x20 grid and were dropped from the table`. Inspecting the raw cells directly shows the grid's row boundaries do not correspond 1:1 with the source's visual rows the way they did on `case-001`:

```text
row 2, col 1:  "経済産業本省 010経済産業本省共通費 経済産業本省一般行政に"   <- THREE logical rows' labels merged into one cell
row 2, col 11: "010"                                                          <- item code, alone, no label in the same cell
row 3, col 11: "01-95"                                                        <- expense code, alone, no label in the same cell
row 4, col 1:  "001 人件費 95016-2111-02-0000 職員基本給 02-0100 職員俸給"     <- a DIFFERENT, deeper-nested "001" grouping code
```

The amount triple was split *across* grid rows 2 and 3 by column, not by source row: row 2's amount cells concatenate the previous-budget values of all three merged label rows (`"234,599,916"` + `"45,924,345"` + our row's `"42,331,005"`, all in one cell, reversed-token-group style), while row 3's amount cells hold the fy2024Request and delta for *only* our row. Because our target row's code (`01-95`) and its label live in different cells with no code+label pairing in either, `normalize-docling.mjs`'s `EXPENSE_CODE_RE` (which requires `code + whitespace + name` **in the same cell**, matching `case-001`'s cell shape) matches nothing for this row: `expenseCandidateCount: 0`.

The single `itemCode` candidate normalize-docling *did* find (`itemCandidateCount: 1`, no ambiguity flagged) is the wrong row entirely — cell `row 4, col 1` (`"001 人件費 ..."`) is a *different*, deeper hierarchy level (a 経費区分 grouping beneath the expense row we selected), not our item header. It only looked unambiguous because none of the *other* real item/expense-level cells on this page happen to satisfy `ITEM_CODE_RE`'s "code + name in one cell" shape at all (their codes and names are scattered across different cells by this page's grid).

**H1 is not supported here** — Docling's table-cell separation, which resolved `case-001`'s two-column conflation, does not generalize to this page's coarser/misaligned grid; if anything it produced a different and arguably worse failure (silently picking a wrong row as if it were unambiguous) than the two flat-text baselines' `null`-and-garbled-string honesty.

**H2 (numeric-token reversal) is not meaningfully testable on this row**: the reversal rule (`reconstructNumericToken`) still works correctly wherever it's applied — e.g. row 2/col2's merged cell `"916 599, 234, 45, 924, 345 331, 42, 005"` and row 3/col3's `"829 887, 46,"` do reverse to valid numbers when parsed — but because the *cell-to-row* assignment is wrong for our target, `findTripleToTheRight` never gets a chance to apply the rule to the right cell for this row. The reversal logic itself did not fail; it was never given the correct row to operate on. This is a distinct problem from the rule's own correctness.

**H3 (CJK wrap-space closing)** was not exercised for docling's target row, since no expense-row cell was matched at all; it cannot be assessed as pass/fail here.

## Hypotheses H1–H6

- **H1 — Table-cell separation generalizes: NOT SUPPORTED.** Docling's grid for this page merges multiple logical rows into single cells and splits one row's amount triple across two grid rows — the opposite of the clean per-row cell isolation seen on `case-001`.
- **H2 — Numeric-token reversal generalizes: INCONCLUSIVE (rule itself not shown to fail; not applied to the correct row).** Reversed-token cells elsewhere on the page still reverse to valid numbers; the rule was never given case-002's target cell to act on.
- **H3 — CJK wrap-space closing recovers the expense name: NOT SUPPORTED for docling (no candidate reached this step); NOT APPLICABLE to the flat-text baselines for expenseName (their name field is a fully separate, triple-anchored-regex failure, not a CJK-spacing issue) — but the *same* CJK-spacing gap in `common.mjs` (absent there, present only in `normalize-docling.mjs`) did surface via `item_name_present_among_candidates` and is a genuinely new, general finding.**
- **H4 — Unit handling: SUPPORTED for all three.** `unit_exact_match` PASSes for pdfjs-baseline, pymupdf-baseline, and docling — all three correctly recovered `"千円"` from this page's own `(単位: 千円)` label. This confirms `case-001`'s unit-recovery failure was a page-context limitation (the label lived on a different page), not a fundamental extraction/understanding limitation — exactly the distinction `case-001`'s documentation predicted this case might clarify.
- **H5 — Positive delta handled without introducing a false negative: SUPPORTED, but untested by design flaw in the check itself.** No engine introduced a spurious `△`/negative sign — `delta`/`deltaRaw` are `null` for all three (extraction did not reach the delta at all), never a fabricated negative value. However, `evaluate.mjs`'s `delta_glyph_observed_and_associated` check hardcodes `expected: 'contains △'` rather than deriving its expectation from Ground Truth's actual `deltaRaw`. For `case-002`, whose correct `deltaRaw` contains **no** glyph, this check can never PASS even for a hypothetically perfect engine that correctly recovered `"4,556,824"` with no glyph — it would still register as `FAIL` because the check literally always expects `△` to be present. **This is a real, previously-latent asymmetry in the evaluator, discovered only by this out-of-sample run, and is not fixed in this task per instructions.**
- **H6 — Hierarchy/item-selection ambiguity persists: SUPPORTED.** Both flat-text baselines found the same 4 item-code-shaped candidates (`010`, `010`, `001`, `001`) with no disambiguation, exactly mirroring `case-001`'s finding. Docling's version of this problem manifested differently (a single, wrongly-confident wrong-row match) rather than an explicit multi-candidate ambiguity — itself a notable difference worth investigating separately.

## case-001 vs. case-002 — capability-level comparison

| Capability | case-001 | case-002 |
|---|---|---|
| Expense-name / table separation (Docling) | Resolved the two-column conflation via genuine cell separation | Regressed: grid misalignment merges multiple rows and splits one row's amounts across grid rows |
| Item selection / hierarchy | Ambiguous for all 3 engines (4 candidates, correct row present among them) | Ambiguous for the 2 flat-text engines (4 candidates, correct row present); Docling picked a single **wrong** row with no ambiguity signal at all — a worse outcome, not just an unresolved one |
| Numeric parsing (flat-text triple regex) | Succeeded — triple was the literal end of the reconstructed line | Failed — annotation text follows the triple on the same line, breaking the trailing-anchor assumption |
| Numeric parsing (Docling reversal rule) | Succeeded, verified across multiple cells | Not exercised on the target row (wrong cell-to-row assignment); works correctly elsewhere on the page |
| Delta sign/glyph handling | Correctly signed negative from an observed `△` | No engine reached a delta value to sign at all; separately, the evaluator's own glyph check is structurally incapable of passing for a no-glyph Ground Truth |
| Unit recovery | Failed for all 3 (label on a different page) | **Passed for all 3** (label present on this page) — clarifies this is page-context-dependent, not a fundamental gap |
| Relationship checks (item/expense-to-amount) | Passed for all 3 | Failed for all 3 — direct consequence of the amount-triple extraction failures above, not a new/independent relationship-detection problem |

The headline is not "case-002 is a harder document" in a vague sense — it's that a **structural document convention that happened to be absent from case-001's target line** (an annotation column's text following, rather than only wrapping after, the amount triple) breaks a specific, narrow regex assumption in the flat-text normalizer, and a **different table-grid density** breaks Docling's cell-per-row assumption in a different, more severe way (wrong-but-confident row selection rather than a flagged ambiguity).

## Ground Truth integrity

- Ground Truth values were read only by `evaluate.mjs`, exactly as designed; `git diff 5a2eb32 -- fixtures/document-understanding/case-002/ground-truth.json` is empty (unchanged throughout this task).
- No engine output, extraction heuristic, or normalization rule was adjusted based on what Ground Truth said. Every `null`/mismatch above reflects the frozen pipeline's actual, first-attempt behavior.
- No expected-value fitting occurred — several of case-002's raw findings (e.g. Docling's wrong-row selection) were discovered only *after* comparing to Ground Truth in `evaluate.mjs`, and are reported as failures here rather than adjusted toward the expected answer.

## Unexpected findings

1. **Prerequisite step gap, not a bug**: `pdfjs-baseline` requires `scripts/pdf-extraction` to have already processed the target source; this is now documented plainly here in case a future new case runs into the same missing-prerequisite error.
2. **`common.mjs` lacks a CJK-space-closing step** that `normalize-docling.mjs` has — a genuine, previously-latent asymmetry between the two normalizer families, exposed only because `case-002`'s reconstructed header line happened to trigger pdfjs-dist's letter-spacing artifact in a place that mattered for scoring.
3. **`evaluate.mjs`'s `delta_glyph_observed_and_associated` check has a hardcoded expectation** (`'contains △'`) rather than deriving it from Ground Truth's actual `deltaRaw` — meaning this check cannot pass for any case whose correct answer has no decrease glyph, regardless of engine correctness. This was invisible with only `case-001` (whose Ground Truth does have a glyph) and is a design gap worth fixing in a future task, not this one.
4. **Docling's failure mode on this page is a silent wrong-answer, not an honest miss**: it reported `itemCandidateCount: 1` (implying no ambiguity) while actually selecting an unrelated row from deeper in the document's hierarchy. This is arguably more concerning than the flat-text baselines' `null` results, which at least honestly signal "extraction did not reach a value."

## Recommended next step

Do not fix any of the above in this task. Recommended follow-up experiments, in rough priority order:
1. Add a `closeCjkWrapSpaces`-equivalent step to `common.mjs`/`normalize.mjs` and re-run *both* `case-001` and `case-002` to confirm it doesn't regress `case-001` while fixing the `item_name_present_among_candidates` asymmetry found here.
2. Investigate whether `splitTrailingTriple`'s trailing-anchor assumption can be generalized (e.g. matching the triple anywhere followed only by non-numeric trailing content) without reintroducing the "amount similarity as selection evidence" risk `protocol/RESEARCH_PROTOCOL.md` warns against.
3. Investigate why Docling's TableFormer produced a coarser, misaligned grid for this specific page, and whether an `itemCandidateCount: 1` result should carry a lower-confidence signal when the winning cell's row position looks structurally inconsistent with neighboring cells (e.g. an expense code found in a different grid row than its own label).
4. Revisit `evaluate.mjs`'s `delta_glyph_observed_and_associated` check to derive its expectation from Ground Truth's `deltaRaw` (glyph-present vs. glyph-absent) rather than hardcoding `'contains △'`, so it can meaningfully score both sign directions.
5. Add a `case-003` deliberately selected (via the same source-only, engine-blind protocol methodology) to test whether the annotation-on-same-line-as-triple pattern found here is itself common or rare across ministries.
