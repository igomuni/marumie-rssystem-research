# Evaluator Correction — Post-hoc Re-evaluation of case-001 and case-002

**This is a benchmark-methodology correction, not an engine-tuning change.** It corrects an evaluation-semantics defect in `evaluate.mjs` discovered by the first frozen `case-002` out-of-sample run (`379043d`), then re-evaluates both `case-001` and `case-002` under the corrected evaluator. It is explicitly **not** a replacement for that first frozen result, which remains historically preserved (see "Historical preservation" below).

Date: 2026-09-26 (Asia/Tokyo)

Original first frozen case-002 result: `379043d` (report: `reports/document-understanding/20260926_0923_Case002_First_Frozen_Benchmark_Run.md`)
Case-002 Ground Truth freeze: `5a2eb32` (unchanged throughout this task)
Evaluator-correction commit: filled in after commit — see `state/CHANGELOG.md`

## A. The defect

The old check (`delta_glyph_observed_and_associated`) was:

```js
const deltaRawHasGlyph = typeof r.deltaRaw === 'string' && r.deltaRaw.includes('△');
checks.push({ id: 'delta_glyph_observed_and_associated', pass: deltaRawHasGlyph, expected: 'contains △', ... });
```

This unconditionally expects the engine's `deltaRaw` to contain `△` — a constant, not something derived from Ground Truth. That happened to be correct for `case-001`, whose frozen `ground-truth.json` has `"deltaRaw": "△32,920,906"`. It is **not** correct for `case-002`, whose frozen `ground-truth.json` has `"deltaRaw": "4,556,824"` (no glyph, visually confirmed against six neighboring rows on the same page — see `fixtures/document-understanding/case-002/20260926_0908_Case002_Ground_Truth_Evidence.md`). Under the old check, **no engine could ever pass this check on `case-002`, even a hypothetically perfect one**, because the check's expectation was baked in from `case-001`'s specific source condition rather than read from `case-002`'s own Ground Truth. This is a benchmark-methodology defect discovered through out-of-sample testing — not an extraction failure, not a normalization failure, and not Ground Truth contamination into the engine pipeline (Ground Truth was never used by any adapter or normalizer; the defect was entirely within the evaluator's own check logic).

## B. Corrected semantics

New check id: **`delta_sign_evidence_matches_source`** (replaces `delta_glyph_observed_and_associated`; the old name is retired because it implied "glyph must be present" as an absolute, not a source-conditional, requirement).

Ground Truth field used to determine the expected glyph state: **`expected.deltaRaw`** — Ground Truth's own raw/visual field — never the sign of `expected.delta` (a normalized/derived numeric value). This matches the task's explicit instruction to prefer the most direct source-derived field over inferring "source expects a glyph" from an unrelated value.

Exact rules (implemented as the pure, exported, unit-tested function `deltaSignEvidenceMatches(expectedDeltaRaw, actualDeltaRaw)` in `evaluate.mjs`):

```text
expectedHasGlyph = expectedDeltaRaw contains △
actualHasGlyph   = actualDeltaRaw (engine/normalizer output) contains △

if expectedHasGlyph:   PASS iff actualHasGlyph is true   (glyph must be genuinely present and associated)
if not expectedHasGlyph: PASS iff actualHasGlyph is false (no glyph may be fabricated)
```

Both directions are symmetric; neither is privileged. The provenance invariant is preserved unchanged: `actualHasGlyph` is computed purely from the engine/normalizer's own `deltaRaw`, never from Ground Truth — a `△` only ever counts as "observed" if it is genuinely present in the pipeline's own output.

**Ground Truth schema note (not a limitation that blocked this task):** the schema has no explicit `unknown`/`unreadable` glyph state, and none was invented. This is safe under the existing process discipline — `case-002`'s own Ground Truth evidence document states plainly "No field was ambiguous or illegible... Nothing was marked unknown," and the same holds for `case-001`. A frozen Ground Truth `deltaRaw` is therefore always either definitely glyph-present or definitely glyph-absent by construction of the freeze process itself; there is currently no code path that could produce an "unknown" `deltaRaw` to feed this check. If a future case's Ground Truth ever needs to express glyph-ambiguity, this check must be revisited then — it is not silently treated as "no glyph" now because that situation cannot currently arise, not because it was assumed away.

**Important interpretive note documented directly in the check's own `note` field:** a `null` `deltaRaw` (nothing extracted at all) PASSes this check when no glyph is expected, because no false decrease indicator was introduced. This does **not** mean the engine successfully recovered the delta — that is separately, correctly scored by `signed_delta_exact_match`, `previous_budget_exact_match`, and `fy2024_request_exact_match`, all three of which remain FAIL for every `case-002` engine (see section F). This check is deliberately narrow: it is about glyph-fabrication avoidance, not overall extraction completeness.

## C. Scope integrity — confirmed unchanged

```bash
git diff --stat -- fixtures/document-understanding/                                    # empty
git diff --stat -- scripts/document-understanding/adapters/                            # empty
git diff --stat -- scripts/document-understanding/benchmark/src/common.mjs             # empty
git diff --stat -- scripts/document-understanding/benchmark/src/normalize.mjs          # empty
git diff --stat -- scripts/document-understanding/benchmark/src/normalize-docling.mjs  # empty
git diff --stat -- scripts/document-understanding/benchmark/src/run.mjs                # empty
```

Ground Truth (`case-001` and `case-002`), the case-002 selection protocol/record, source selection, all three adapters, both normalizers, and the orchestrator are byte-for-byte unchanged. Only `evaluate.mjs` (the check itself) and `test.mjs` (new tests) were edited.

Raw and normalized artifacts were independently diffed before and after the full engine rerun (timestamp fields excluded): identical for all three engines on both cases. This confirms the rerun exercised the exact same extraction/normalization behavior as the first frozen run — only the evaluator changed.

## D. Tests

Nine new unit tests were added to `scripts/document-understanding/benchmark/src/test.mjs`, targeting the exported pure function `deltaSignEvidenceMatches` directly (no on-disk fixture files needed):

- glyph expected + glyph observed → PASS
- glyph expected + no glyph observed → FAIL
- glyph expected + nothing observed (`null`) → FAIL
- no glyph expected + no glyph observed → PASS
- no glyph expected + glyph incorrectly fabricated → FAIL
- no glyph expected + nothing observed (`null`) → PASS (with an inline comment explaining this is not evidence of successful recovery)
- a 4-assertion symmetry check confirming the function has no hardcoded "glyph must be present" bias

All 26 tests in the suite pass (17 pre-existing + 9 new):

```bash
npm run validate          # PASS
npm run extraction:test   # PASS
npm run docbench:test     # PASS, 26/26
git diff --check          # clean
```

## E. Case-001 before/after

```text
check                                      old (delta_glyph_observed_and_associated)   corrected (delta_sign_evidence_matches_source)
pdfjs-baseline sign/glyph check             PASS                                        PASS
pymupdf-baseline sign/glyph check           PASS                                        PASS
docling sign/glyph check                    PASS                                        PASS

totals            old      corrected
pdfjs-baseline     8/11      8/11
pymupdf-baseline   8/11      8/11
docling            9/11      9/11
```

Unchanged. `case-001`'s Ground Truth `deltaRaw` (`"△32,920,906"`) expects a glyph, and all three engines' normalized `deltaRaw` genuinely contained one (`"△ 32,920,906"`, `"△     32,920,906"`, `"△ 906 920, 32,"` respectively) — the corrected check's glyph-expected branch is identical in effect to the old check for this case. No other check changed.

## F. Case-002 before/after

```text
check                                      old       corrected
delta glyph/sign evidence                  FAIL      PASS
item_name_exact_match                      FAIL      FAIL           (unchanged, all 3 engines)
item_name_present_among_candidates         mixed     mixed          (unchanged: pdfjs FAIL, pymupdf PASS, docling FAIL — same as before)
expense_name_exact_match_after_line_join   FAIL      FAIL           (unchanged, all 3 engines)
previous_budget_exact_match                FAIL      FAIL           (unchanged, all 3 engines)
fy2024_request_exact_match                 FAIL      FAIL           (unchanged, all 3 engines)
signed_delta_exact_match                   FAIL      FAIL           (unchanged, all 3 engines)
unit_exact_match                           PASS      PASS           (unchanged, all 3 engines)
page_identification                        PASS      PASS           (unchanged, all 3 engines)
item_to_amount_relationship                FAIL      FAIL           (unchanged, all 3 engines)
expense_to_amount_relationship             FAIL      FAIL           (unchanged, all 3 engines)

totals            old      corrected
pdfjs-baseline     2/11      3/11
pymupdf-baseline   3/11      4/11
docling            2/11      3/11
```

Every engine's `deltaRaw` for `case-002` is `null` (extraction did not reach the amount triple at all — see the original frozen report's root-cause analysis, unchanged and unrepaired in this task). Ground Truth's `deltaRaw` (`"4,556,824"`) has no glyph, so under the corrected check, `null` (no glyph fabricated) now correctly PASSes the narrow glyph-fabrication-avoidance question — while `signed_delta_exact_match`, `previous_budget_exact_match`, and `fy2024_request_exact_match` all remain FAIL, honestly reflecting that no delta was actually recovered. Net effect: exactly `+1` per engine, matching the hypothesis stated in the task (computed, not forced).

## G. Unexpected changes

None. Every check other than the sign/glyph check produced an identical PASS/FAIL outcome before and after, for both cases and all three engines, confirmed by direct comparison of the full check lists (not just totals). This is consistent with the change being scoped to exactly one check's internal logic.

## H. Historical preservation

- Commit `379043d` (and its parent chain) remains in `research/case-002-meti-preregistration`'s history, untouched, unamended, unreverted. `git log --oneline | grep 379043d` still finds it.
- `reports/document-understanding/20260926_0923_Case002_First_Frozen_Benchmark_Run.md`, the first-frozen-run report, is **not modified or deleted** by this task — it still describes the original evaluator's semantics and the original 2/11, 3/11, 2/11 scores, explicitly and permanently.
- `evidence/document-understanding/case-002-results.json` and `reports/document-understanding/case-002-evaluation.md` **are** regenerated (by the unmodified `run.mjs`, per existing repository convention that these are always-current compact artifacts) to reflect the corrected evaluator — their prior (first-frozen) contents remain fully recoverable via `git show 379043d:evidence/document-understanding/case-002-results.json` and the equivalent for the report.
- This new report (`20260926_1231_Case002_Evaluator_Corrected_Reevaluation.md`) is a **new, separate** artifact — it does not overwrite or rename the first-frozen report.
- No evaluator-version metadata field was added to the evidence schema (would have required a broader schema change than this narrow correction warrants); the evaluator-correction commit SHA is instead the authoritative version marker, recorded here and in `state/CHANGELOG.md`.

## I. Files changed

**Evaluator/test code:**
- `scripts/document-understanding/benchmark/src/evaluate.mjs` — replaced `delta_glyph_observed_and_associated` with `delta_sign_evidence_matches_source`, backed by the new exported pure function `deltaSignEvidenceMatches`
- `scripts/document-understanding/benchmark/src/test.mjs` — 9 new unit tests

**Evidence/reports (regenerated by unmodified `run.mjs`, plus this new report):**
- `evidence/document-understanding/case-001-results.json`, `reports/document-understanding/case-001-evaluation.md`
- `evidence/document-understanding/case-002-results.json`, `reports/document-understanding/case-002-evaluation.md`
- `reports/document-understanding/20260926_1231_Case002_Evaluator_Corrected_Reevaluation.md` (this file)

**State files:** `state/CURRENT_STATE.json`, `state/TODO.md`, `state/CHANGELOG.md`

**Not changed (verified via `git diff --stat`):** any Ground Truth file, the case-002 selection protocol/record, any adapter, `common.mjs`, `normalize.mjs`, `normalize-docling.mjs`, `run.mjs`.

**Ignored/generated (git-ignored, not committed):** `derived/document-understanding/{case-001,case-002}/*.{raw,normalized,evaluation}.json` — regenerated by the rerun; independently verified byte-identical (modulo timestamps) to their pre-rerun contents for the raw/normalized files.

## J. Methodological conclusion

This is best classified as **evaluator overfit to the first fixture's source condition** — specifically, a check that encoded "the correct answer always has property X" where X (a decrease glyph) was true of `case-001`'s particular row but is not a universal property of correct answers in general. This is a distinct failure category from an extraction bug, a normalization bug, or Ground Truth leakage into the pipeline: Ground Truth isolation was otherwise completely correct throughout (no adapter or normalizer ever touched it), yet the benchmark's own scoring logic still silently assumed something about the *shape* of a correct answer that only held for the one case it had been validated against. The general lesson: a single-fixture benchmark's checks can encode implicit assumptions from that fixture even when explicit Ground-Truth-contamination discipline is followed perfectly — checks themselves need to be re-examined against a second, independently-selected case before being trusted as fixture-independent, exactly as this out-of-sample methodology was designed to surface.

## K. Next step

Recommended single next follow-up experiment (not executed in this task): **generalize the trailing amount-triple parser (`common.mjs`'s `splitTrailingTriple`) as a separate, hypothesis-driven change** — specifically, investigate whether the trailing-anchor assumption can be relaxed to tolerate non-numeric trailing content (like `case-002`'s same-line `（要求要旨）` annotation) without reintroducing amount-similarity-as-selection-evidence risk — then re-evaluate `case-001` and `case-002` under the *unchanged* corrected evaluator, without touching any other behavior, to observe the isolated effect of that one parser change.
