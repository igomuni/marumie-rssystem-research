# case-003 — First Frozen Out-of-Sample Benchmark Run (MIC / 総務省)

**This is the first-ever execution of the unchanged, case-001/case-002-derived Document Understanding pipeline against `case-003`.** No benchmark code (adapters, normalizers, evaluator, check definitions) was changed before, during, or after this run. This report records what happened, without repair.

Date: 2026-09-26 (Asia/Tokyo)

## Freeze chain

```text
Source acquired/locked  ->  a12ce47 (acquisition immutability fix, source itself locked earlier in the survey task)
Selection protocol frozen -> 8b65364
Target row selected/frozen -> 31c4626
Ground Truth frozen        -> 1bc6c4e
First benchmark run (this report) -> committed after this report
```

All four upstream freezes were verified byte-identical to their freeze commits immediately before this run (`git diff <commit> -- <path>`, all empty). `git log 1bc6c4e..HEAD -- scripts/document-understanding/ scripts/pdf-extraction/ scripts/source-acquisition/` was empty: no benchmark, extraction, or acquisition code changed since the Ground Truth freeze.

## Benchmark environment

- pdfjs-baseline: `pdfjs-dist` 4.10.38 (per evidence `engineVersion`)
- pymupdf-baseline: PyMuPDF 1.28.2
- docling: 2.130.0
- Node.js: v24.9.0
- Source: `mic-fy2024-general-account-expenditure-request`, SHA-256 `cc54dbe5...`, 454 pages, A4 landscape, Producer "List Creator"

## Prerequisite step (generic, not case-003-specific)

`npm run extract` (pdfjs-baseline's prerequisite) had not yet processed the MIC source. Running the existing, unmodified command reprocessed **all four** locked sources. The three previously-processed sources produced byte-identical `linesSha256` hashes to before (`bd29feaef...`, `3688fcc79...`, `6f51498ed...` — all unchanged, verified via `shasum` before/after), confirming this was purely a missing-prerequisite run, not a semantic or code change. MIC itself extracted as `pages=454 items=150030 lines=16004`.

## A genuine harness-reliability finding, distinct from the benchmark's semantic result

`npm run docbench -- case-003` (the documented, normal invocation) failed deterministically and repeatedly with `ENOENT: ... docling.raw.json` — `normalizeDocling()` tried to read a raw artifact that `docling`'s adapter had not written. Direct inspection established:

- The docling Python adapter (`scripts/document-understanding/adapters/docling/src/run.py`), invoked **directly from a shell**, succeeded reliably every time it was tried (confirmed repeatedly).
- The identical, unmodified script invoked via Node's `child_process.spawnSync(..., { stdio: 'inherit' })` — exactly what `run.mjs`'s `venvPythonAdapter` does — succeeded on the *first* attempt in this session (producing the complete, valid result preserved below) but then failed on **four consecutive subsequent attempts** in the same session, each time with `docling.raw.json` never written and **no docling subprocess output at all** reaching the parent's inherited stdio (not even the RapidOCR model-loading log lines that appear on every successful invocation). A final retry succeeded again, end to end, reproducing byte-identical scores to the first success.
- `npm run docbench -- case-002` was re-run in the same session as a control and succeeded on the first attempt, reproducing byte-identical (modulo timestamps) results to the historical record — so this is not a general regression in the npm-wrapped invocation path, and not a `case-002` regression.
- No code was changed to investigate or work around this. No root cause was conclusively established (candidates considered but not confirmed: resource contention from repeated `torch`/RapidOCR model loads within one shell session; some Node `spawnSync`/child-stdio interaction specific to this adapter's process tree). This is recorded as an **open infrastructure-reliability question**, separate from the benchmark's semantic findings below, which are all drawn from a fully completed, internally consistent, and reproduced-twice successful run.

**The preserved first-run result below is the first successful, complete execution** (compact evidence/report files were only ever written by `run.mjs` after all three engines' full pipelines completed; every failed attempt crashed before reaching that write, so the committed `evidence/document-understanding/case-003-results.json` / `reports/document-understanding/case-003-evaluation.md` were never touched by a failed attempt). A second full success later in the session reproduced identical scores, confirming determinism of the underlying benchmark once it runs to completion.

## First-run comparison matrix

```text
check                                      pdfjs   pymupdf   docling
item_name_exact_match                      FAIL    FAIL      FAIL
item_name_present_among_candidates         FAIL    PASS      FAIL
expense_name_exact_match_after_line_join   PASS    PASS      FAIL
previous_budget_exact_match                PASS    PASS      FAIL
fy2024_request_exact_match                 PASS    PASS      FAIL
signed_delta_exact_match                   PASS    PASS      FAIL
unit_exact_match                           PASS    PASS      PASS
page_identification                        PASS    PASS      PASS
delta_sign_evidence_matches_source         PASS    PASS      PASS
item_to_amount_relationship                PASS    PASS      FAIL
expense_to_amount_relationship             PASS    PASS      FAIL
```

**Scores: pdfjs-baseline 9/11, pymupdf-baseline 10/11, docling 3/11.**

## Scores in context (current evaluator, all three cases)

| Case | pdfjs-baseline | pymupdf-baseline | docling |
|---|---|---|---|
| case-001 | 8/11 | 8/11 | 9/11 |
| case-002 (corrected) | 3/11 | 4/11 | 3/11 |
| **case-003** | **9/11** | **10/11** | **3/11** |

case-003's flat-text engines scored *higher* than either prior case — this is not "case-003 is easy" in general; it is precisely explained below by one specific structural fact (the empty remarks column), not by MIC being an inherently simpler document family.

## Raw vs. normalized findings, per engine

### pdfjs-baseline and pymupdf-baseline

Both reconstructed the target line completely and cleanly at the raw stage. pdfjs-baseline's raw line:

```text
"1 01-95 総務本省一般行政に必要 38,472,070 41,763,907 3,291,837"
```

pymupdf-baseline's raw line is the same content with different whitespace. **Critically, the amount triple is the literal end of the line in both engines' raw output — nothing follows it.** `common.mjs`'s `splitTrailingTriple` therefore matched cleanly, unmodified, and every downstream amount/relationship check passed for both engines.

The only difference between the two: `item_name_present_among_candidates` — pdfjs-baseline **FAILs**, pymupdf-baseline **PASSes**, for the exact same reason found on case-002: pdfjs-dist's line reconstruction inserts a literal space between every CJK character in header-style rows (`"総 務 本 省 共 通 費"`), while PyMuPDF's `sort=True` reconstruction does not (`"総務本省共通費"`, an exact match to Ground Truth). `common.mjs`/`normalize.mjs` still has no `closeCjkWrapSpaces`-equivalent step; `normalize-docling.mjs` still does. This is now a **second, independent confirmation** of this exact asymmetry, on a different ministry's document.

Both engines' `item_name_exact_match` **FAILs** for the same reason as case-001 and case-002: header-row hierarchy ambiguity. Four item-code-shaped candidates were found (`010 総務本省`, `010 総務本省共通費`, `001 既定定員に伴う経費`, `001 人件費...`), and the harness correctly declines to guess among them, reporting `null` rather than a wrong pick. This is now a **third independent confirmation**, across three different ministries, of the same unresolved structural gap.

### docling

Docling's TableFormer built a **31×16 grid** for this page. Inspecting the raw cells directly:

```text
row 3, col 1: "010 総 務 本 省 010 総 務 本 省 共 通 費 01-95 総務本省一般行政に必要 な経費"
                <- THREE logical rows' item/expense codes and labels merged into ONE cell
row 3, col 4: "866 894, 830, 16, 232 650, 785, 17, 366 755, 954, 913 783, 39, 868 125, 43, 955 341, 3, 070 472, 38,"
                <- reversed-token amount fragments for multiple merged rows' figures, concatenated in one cell
row 3, col 0: "1"                                    <- request number, isolated in its own cell
row 4, col 1: "001"                                   <- a DIFFERENT, deeper row (既定定員に伴う経費), cleanly separated
```

Unlike case-002 (where the target code and its label landed in **separate, unpaired** cells), case-003's failure is the **opposite geometry**: the target row's own code+label is present and intact, but **fused together with its two ancestor header rows' codes and labels inside a single cell**, with no columns 5/9 (FY2024-request/delta) populated for this row at all — those values appear to have been absorbed into the same reversed-token blob in column 4 rather than kept in their own columns. `normalize-docling.mjs`'s `EXPENSE_CODE_RE` (which expects `code + whitespace + name` as effectively the entire relevant cell content) does not match cleanly against a cell that also contains two *other* rows' codes and labels ahead of the one being searched for — resulting in `expenseCandidateCount: 0` for this row, exactly as case-002 also ended in zero expense candidates, but via a different route.

**A genuinely new failure sub-mode was also observed**: the second `item_name_present_among_candidates` entry, `{"itemCode":"316","itemName":"712, 3, 特"}`, is a **false-positive item-code match** — `316` and its neighboring text are fragments of a reversed numeric token (`"3,712,316"`, itself a fragment of the personnel-count figure `2,537人` context) plus a stray kanji character (`特`, from `特別職`), which happened to satisfy the item-code-shaped regex pattern. This is a previously-unobserved artifact: Docling's numeric-token reversal, in combination with the coarse grid, can produce text that spuriously *looks like* a valid item code to the generic candidate-matching regex, not just fail to find real ones.

**Docling's `item_name_exact_match` and `expense_name_exact_match_after_line_join` both correctly return `null`, not a confidently wrong value** — this is an **honest-null failure**, structurally different from case-002's Docling behavior, where it *confidently and wrongly* selected an unrelated, deeper-hierarchy row with `itemCandidateCount: 1` (no ambiguity signal at all). On case-003, Docling's own candidate enumeration shows two shaped-but-wrong candidates and correctly declines to resolve `result.itemName`/`result.expenseName` to either. **This is a materially better failure mode than case-002's, and is recorded as such — not glossed over as "still 3/11 either way."**

## Focused case-002 comparison

### Flat-text amount triple

**Does pdf.js/PyMuPDF recover the amount triple on case-003 without modification? Yes, cleanly, for both engines.** case-003's remarks (`備考`) column is visually empty for the target row (confirmed in the Ground Truth evidence record), and the raw reconstructed line confirms the amount triple is the literal end of the line with nothing trailing it. **This strengthens the diagnosis that case-002's `splitTrailingTriple` failure was caused specifically by that page's same-line annotation content, not by a general METI/ministry-template incompatibility with the trailing-anchor regex.** It does not yet prove the regex generalizes to *all* ministries — it proves the regex's known failure condition (trailing non-numeric content on the same line) is genuinely conditional on a page-level structural feature (annotation presence) that varies even within a single document, not a fixed property of "government budget PDFs" as a class.

### Docling grid behavior

**Does the same failure recur? Similar in category (grid misalignment → no clean code+label+amount pairing → zero expense candidates), but the specific mechanism differs and is, in one respect, less severe.** case-002's grid *split* a paired code+label across unconnected cells; case-003's grid *over-merged* three rows' worth of codes+labels into one cell. Both end in the same downstream symptom (no usable expense candidate), but case-003's version does not produce a confidently-wrong final answer, while case-002's did. **This is two data points showing the same broad category of failure (coarse/misaligned TableFormer grid near header-row transitions) manifesting through two different, non-identical specific mechanisms** — evidence for "Docling's grid detection is unreliable at item/expense header boundaries in this document family," not yet evidence for a single universal Docling grid bug with one fix.

### Numeric-token reversal

**Exercised, and successful where it was reachable, but not reachable for the target cell.** The reversal pattern is visibly present and internally consistent in the merged column-4 blob (`"070 472, 38,"` does reverse to `38,472,070`, matching Ground Truth) and in numerous other cells further down the page (`"013 430, 33," -> 33,430,013`, etc.) — the *rule itself* is not shown to fail. It was simply never given a cleanly-isolated target cell to operate on for row 3, because the cell-merging problem occurs one level upstream of where the reversal rule runs. Same conclusion as case-002 for this specific hypothesis: **inconclusive-by-non-exercise for the target row, but the rule's own correctness is independently reaffirmed elsewhere on the page.**

### CJK wrapping

The target expense name (`総務本省一般行政に必要な経費`) wraps across two printed lines in the source. pdfjs-baseline and pymupdf-baseline both **correctly reconstruct it** (`expense_name_exact_match_after_line_join`: PASS for both) — `common.mjs`'s `joinWrappedLabel` handles this case-003 instance of the same wrap pattern already exercised on case-001/002 without any change. Docling never reaches this check meaningfully (its `expenseName` is `null`) because the cell-merge problem occurs before the CJK-wrap-closing rule would even apply — `closeCjkWrapSpaces` is not shown to fail here, it is simply not exercised for this row.

### Hierarchy / intermediate levels

MIC's page exposes one additional intermediate breakdown level compared to case-001/002's target pages (`001 既定定員に伴う経費` → `001 人件費` → individually-coded allowance lines, all beneath the target row, still visible on the same page). This did **not** change the *candidate count* for the header-ambiguity check (still exactly 4 candidates for both flat-text engines, matching case-001's and case-002's own 4-candidate pattern) — the extra nesting level sits *below* the target row in the hierarchy, not among its siblings, so it does not add a fifth ambiguous candidate at the same level. It **did**, however, plausibly contribute to Docling's over-merging: the target row's line-height/row-band proximity to its two ancestor headers (with the next distinct row, `001 既定定員に伴う経費`, immediately following) may be exactly what caused TableFormer to fuse rows 1–3's header chain into one row-band while still correctly separating row 4 onward. This is a plausible, evidence-consistent hypothesis, not a proven mechanism.

### Unit

`(単位: 千円)` is recovered correctly by **all three engines** (`unit_exact_match`: PASS, PASS, PASS) — matching case-002's pattern (page-level label present and recovered by everyone) and contrasting with case-001 (label absent from the target page, correctly failed by everyone). This is now the **second confirmation** that unit-label recovery tracks page-context (label presence), not engine capability or ministry identity — consistent with case-002's own H4 finding.

### Positive delta

The frozen Ground Truth has a positive delta (`3,291,837`) with no `△`. **No engine fabricated a glyph.** `delta_sign_evidence_matches_source` PASSes for all three (trivially for docling, whose `deltaRaw` is `null`; substantively for pdfjs/pymupdf, whose genuinely-recovered `deltaRaw` strings contain no glyph). The corrected evaluator semantics (from the case-002 evaluator-overfit fix) behave exactly as designed on a second positive-delta case.

## Similar / different / new

**Similar to prior cases:**
- Header-row hierarchy ambiguity (4 candidates, correct row present but unresolved) — now confirmed on all three cases.
- The `common.mjs` CJK-wrap-space-closing gap affecting `item_name_present_among_candidates` specifically for pdfjs-baseline (not pymupdf-baseline) — confirmed on a second, independent ministry.
- Docling's amount/expense-name recovery blocked by a grid/cell-boundary problem near the target row's header transition, ending in zero expense candidates.
- Page-level unit-label recovery succeeding for all three engines when the label is present on the page (case-002 and case-003 both).

**Different despite similar document structure:**
- Flat-text amount-triple recovery: **fails** on case-002, **succeeds** on case-003 — directly attributable to the presence/absence of trailing same-line annotation content, not to any difference in ministry, engine version, or general template.
- Docling's specific cell-merge geometry: case-002 under-pairs (code and label split across cells); case-003 over-merges (three rows fused into one cell). Same broad failure category, opposite specific mechanism.
- Docling's failure honesty: case-002 produced a **confidently wrong** answer with no ambiguity signal; case-003 produced an **honest null** with two visibly wrong-shaped candidates. A meaningfully better (less dangerous) failure mode, on the same engine, same broad document family.

**Genuinely new:**
- A false-positive item-code-shaped candidate (`316`) arising from a reversed-numeric-token fragment plus a stray character — not previously observed on case-001 or case-002.
- The additional intermediate hierarchy level beneath the target row (`001 既定定員に伴う経費` → `001 人件費` → coded allowance lines) as a plausible (not proven) contributing factor to Docling's specific over-merge pattern.
- The harness-reliability finding itself (intermittent `docling.raw.json` non-production under Node's `spawnSync` in this session) — not a prior-case phenomenon, and not yet understood.

## Hypotheses (disciplined labels)

- **H-triple — "case-002's trailing-triple failure was layout/annotation-specific, not a ministry-template-general failure": SUPPORTED**, more strongly than before. A second ministry's document, with the annotation column empty, parses the triple correctly unmodified.
- **H-docling-grid — "Docling's grid-density/misalignment problem generalizes across ministries in the same specific way": WEAKENED / PARTIALLY CONTRADICTED.** The broad *category* (grid misalignment causing zero expense candidates) recurs, but the specific mechanism (split vs. merge) and the failure's honesty (confident-wrong vs. honest-null) both differ. Two ministries is not enough to call this a stable per-family signature yet.
- **H-cjk-gap — "`common.mjs` lacks a CJK-wrap-space-closing step, and this is a genuine cross-case gap, not a one-off": SUPPORTED**, now confirmed on two independent ministries with the identical pdfjs-vs-pymupdf divergence pattern.
- **H-hierarchy — "header-row hierarchy ambiguity is a document-family-independent normalizer gap, not case-001-specific": SUPPORTED**, now confirmed on all three cases with the same 4-candidate shape.
- **H-numeric-reversal — "Docling's `reconstructNumericToken` rule is correct but was never a general recovery mechanism for cell-boundary problems": SUPPORTED, INCONCLUSIVE for the target row specifically** (not exercised there), consistent with case-002's own finding.
- **H-unit — "unit-label recovery is page-context-dependent, not engine- or ministry-dependent": SUPPORTED** for a second time.

## Silent wrong answers

**None on case-003.** Every failure across all three engines on this case is either an honest `null` (pdfjs/pymupdf's ambiguous item name; docling's expense name/amounts) or a diagnostic-only candidate list correctly not promoted to `result`. This is a notable, favorable contrast with case-002's Docling behavior and worth flagging explicitly as a genuine difference, not assumed away.

## Layer diagnosis

| Finding | Layer |
|---|---|
| pdfjs/pymupdf raw line reconstruction, amount triple intact | 2 (raw representation) — succeeded |
| `splitTrailingTriple` succeeding here | 3/5 boundary — confirms the rule is layout-conditional (document-family/layout-specific in the ADR-010 sense), not a generic-vs-broken binary; this specific page's layout simply doesn't trigger the known failure condition |
| CJK-space gap (pdfjs only) | 4 (engine-specific normalization gap) |
| Header-row hierarchy ambiguity | 5/6 boundary (document-family/layout-interpretation and/or semantic-interpretation — no hierarchy-level detection exists yet at either layer) |
| Docling's row-merging at the header/expense transition | 1 (engine behavior — TableFormer's own row-clustering) |
| Docling's false-positive item-code candidate from a reversed token | 4 (engine-specific normalization) crossed with 7 (evaluation/candidate-matching regex too permissive against unexpected input shapes) |
| Unit recovery (all three) | 5 (document/layout — page-context, not engine capability) |
| Delta sign evaluator behavior | 7 (evaluation) — working exactly as corrected |
| The `docbench` npm-wrapping reliability issue | Outside the 7-layer taxonomy — a harness/tooling reliability concern, not a research-architecture layer |

## Strategy-selection implications (source-safe features only; no Ground Truth leakage)

Features that, if captured in a future case's Document Profile, would plausibly have helped anticipate this case's specific outcomes **without consulting Ground Truth or engine output for this document**:

- **Remarks-column visual emptiness for the target row** (source-safe, visually observable before any engine runs, already noted in this case's Ground Truth evidence as an "empty 備考 column" observation) — plausibly predictive of flat-text triple-extraction success, in contrast to case-002's visually-occupied remarks column at the same row position. This is exactly the kind of source-safe feature the case-based architecture report's Document Profile concept was designed to capture.
- **Presence of a page-level unit label** (source-safe, already part of the existing Document Profile schema for case-001/002) — correctly predictive of `unit_exact_match` success for both case-002 and case-003.
- **Presence of multiple `NNN <name>`-shaped rows near the target** (source-safe, visually countable without running an engine) — would have correctly predicted the hierarchy-ambiguity failure recurring here, exactly as it did on all three cases.
- **Docling grid density/row-count relative to page content density is NOT source-safe** (only knowable after running Docling) and must remain engine-derived, per the architecture report's leakage rule — it cannot be used to decide whether to run Docling in the first place without circularity.

## Proposed follow-ups (prioritized, not implemented)

1. Investigate the `docbench` harness-reliability issue (intermittent Docling subprocess non-completion under Node's `spawnSync` in this environment) — this affects the trustworthiness of *any* future automated case-003+ run, independent of any parsing/normalization question.
2. Add a `closeCjkWrapSpaces`-equivalent step to `common.mjs`/`normalize.mjs` and re-verify against case-001, case-002, and case-003 together — now supported by two independent confirmations rather than one.
3. Investigate a hierarchy-level detection mechanism (indentation, code-length, or code-prefix-based) to resolve the now-three-times-confirmed header-row ambiguity, rather than leaving it as a permanent diagnostic-only gap.
4. Investigate whether Docling's row-clustering at header/expense transitions can be given a lower-confidence signal when a matched cell's own regex match is only a *substring* of a larger merged cell (as opposed to the cell's entire content) — this might generalize to catch both case-002's and case-003's Docling failures without needing to unify their differing specific mechanisms.
5. Consider a `case-004` from a third, structurally distinct ministry/document-family to test whether the "empty vs. occupied remarks column" and "grid-merge vs. grid-split" axes are genuinely independent, useful discriminating features or coincidental to these two cases.

## Ground Truth integrity

- Ground Truth values were read only by `evaluate.mjs`, exactly as designed; `git diff 1bc6c4e -- fixtures/document-understanding/case-003/ground-truth.json` is empty (unchanged throughout this task).
- No engine output, extraction heuristic, or normalization rule was adjusted based on what Ground Truth said.
- Selection protocol and selection record re-verified byte-identical to their freeze commits (`8b65364`, `31c4626`) before and after this run.

## Unexpected findings

1. **The `docbench` harness-reliability issue** — genuinely unanticipated, not predicted by any prior hypothesis, and not fully root-caused. Documented above as distinct from the benchmark's semantic findings.
2. **Docling's false-positive item-code candidate from a reversed numeric-token fragment** — a new artifact sub-mode not seen on case-001 or case-002.
3. **case-003 scoring higher than either prior case on the flat-text engines** — not because MIC is a generally "easier" document family, but because of one specific, source-observable structural fact (empty remarks column for this specific row) that a future Document Profile should capture explicitly rather than let get absorbed into an undifferentiated per-case score.

## Recommended next step

Investigate and characterize the `docbench` harness-reliability issue (Docling subprocess intermittently failing to complete under Node's `spawnSync` in this environment) as a **standalone diagnostic task**, before attempting any adaptation experiment on `common.mjs`, `normalize-docling.mjs`, or the header-hierarchy-ambiguity gap — because an unreliable harness would undermine confidence in the results of any such experiment. This is chosen over jumping directly to "fix `splitTrailingTriple`'s generalization" (case-002's own recommendation) because case-003's own evidence shows that specific fix would not even be exercised as a generalization test here (the trailing-triple regex already succeeded on this row), and over "add `closeCjkWrapSpaces`" because, while now doubly-supported, it is a smaller-blast-radius change than confirming the benchmark's own execution reliability first. Not executed in this task.
