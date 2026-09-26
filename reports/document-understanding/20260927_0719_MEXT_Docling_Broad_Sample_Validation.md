# MEXT Docling Anomaly Signal — Broad-Sample Validation

Status: **exploratory, read-only validation. No production/schema change. No Ground Truth/benchmark change. No new benchmark target registered. No case-005 started.**

Date: 2026-09-27 (Asia/Tokyo)

## 1. Research question

> Does the Docling-native signal frozen in the prior 16-page survey (`acaf550`) — specifically `maxNumCols` and `totalSpanningCellCount` — retain information distinguishing ordinary variation from known special structures when carried out to a machine-selected, ~120-page sample spread across the whole MEXT document?

This task's explicit purpose is to **falsify** the prior small-sample clean separation by testing it against broader ordinary variation, not to build a new detector, not to rank p1327 highly, and not to rescue the prior finding if it fails.

## 2. Frozen inputs / integrity (verified before and after this task)

- Branch `research/case-004-mext-preregistration`; pre-task `HEAD` `acaf550`; working tree clean; `main` unchanged at `3b29ebd`.
- Source `mext-fy2024-general-account-expenditure-request-detail`, SHA-256 `6df221dfd22c48e0f32dd59bcf2dbcbaad19720083be43005ce700b984a6bf71` — recomputed by the scratch script itself and independently via `shasum`; matches.
- case-004 selection protocol (`c2b2c28`), selection record (`fa82c13`), Ground Truth (`f9b2f35`), first frozen benchmark (`49f5ca6`), organization-010/020 diagnostics (`187a8e9`/`aedea1c`), the geometry survey (`075474e`), the text/grammar survey (`a9c0092`), and the prior 16-page Docling survey (`acaf550`) — all re-verified byte-identical to their freeze commits, both before this task began and again immediately before commit. None was rewritten.

## 3. Prior small-sample claim (repeated verbatim, not adjusted)

From `acaf550` (16-page fixed sample: 7 baseline, 9 known/reference): `maxNumCols` ≤9 for every baseline page, `maxNumCols` ≥11 for every known/reference page — a clean, zero-overlap separation, explicitly flagged there as unproven at whole-document scale.

## 4. Sampling protocol (frozen before any feature was computed)

Deterministic, evenly-spaced `pdfPageIndex` values over `[0, N-1]`:

```
N = 1339
sampleSize = 120
indices[i] = round(i * (N-1) / (sampleSize-1))  for i in range(sampleSize)
```

Deduplicated after rounding. This method was chosen, per the task's own instruction, for reproducibility, freedom from semantic knowledge, broad cross-document coverage, and the absence of any random-seed dependency — not adjusted to include or exclude any known page.

## 5. Frozen sample (recorded before known-page evaluation)

Formula above produced exactly **120 unique indices** (no duplicates from rounding) spanning `pdfPageIndex` 0 through 1338:

```
0, 11, 22, 34, 45, 56, 67, 79, 90, 101, 112, 124, 135, 146, 157, 169, 180, 191, 202, 214,
225, 236, 247, 259, 270, 281, 292, 304, 315, 326, 337, 349, 360, 371, 382, 394, 405, 416,
427, 439, 450, 461, 472, 483, 495, 506, 517, 528, 540, 551, 562, 573, 585, 596, 607, 618,
630, 641, 652, 663, 675, 686, 697, 708, 720, 731, 742, 753, 765, 776, 787, 798, 810, 821,
832, 843, 855, 866, 877, 888, 899, 911, 922, 933, 944, 956, 967, 978, 989, 1001, 1012, 1023,
1034, 1046, 1057, 1068, 1079, 1091, 1102, 1113, 1124, 1136, 1147, 1158, 1169, 1181, 1192,
1203, 1214, 1226, 1237, 1248, 1259, 1271, 1282, 1293, 1304, 1316, 1327, 1338
```

**Disclosed, not adjusted**: `pdfPageIndex` 1169 (one of the 9 known/reference pages) fell into this systematic sample by coincidence of the arithmetic spacing. No other known page coincided. This overlap was not created or removed after the fact; it is reported as-is, per the task's own instruction not to avoid or engineer such overlaps.

## 6. Frozen features (unchanged from `acaf550`)

`tableCount`, `maxNumCols`, `maxNumRows`, `maxCellCount`, `totalSpanningCellCount`, `incompatibleGridsFlag` (ratio threshold 1.5, unchanged), `emptyCellRatioProxy`, `numericHeavyCellRatio` — every definition copied verbatim from the prior survey's own script into this task's own standalone, uncommitted research script (which again calls `DocumentConverter` directly, never reads `ground-truth.json`, and never reuses the production normalizer). No field was added, no threshold was changed, and `bbox` was **not** newly exploited as a ranking feature, per the task's explicit prohibition.

## 7. Coverage / missingness

All 120 sampled pages, plus all 9 known/reference pages, were processed in a single, uninterrupted script execution. **Zero errors, zero missing/unusable Docling table data** — every page produced exactly one Docling table object (see §10 for what this itself means). No value was backfilled with 0; none was needed.

## 8. `maxNumCols` distribution (broad sample, n=120)

| Statistic | Value |
|---|---:|
| min | 0 |
| median | 10 |
| Q1 | 8 |
| Q3 | 12 |
| p90 | 14.1 |
| p95 | 17 |
| p99 | 19.8 |
| max | 22 |
| count ≤9 | 47 (39%) |
| count =10 | 14 (12%) |
| **count ≥11** | **59 (49%)** |
| count ≥15 | 12 (10%) |
| count ≥18 | 5 (4.2%) |
| count ≥20 | 2 (1.7%) |

**The prior small-sample boundary (`≥11` = known-family territory) is met or exceeded by essentially half of this broad, semantically-blind sample.** This alone falsifies the literal threshold as a usable discriminator at document scale.

## 9. `totalSpanningCellCount` distribution (broad sample, n=120)

| Statistic | Value |
|---|---:|
| min | 0 |
| median | 0 |
| p90 | 6 |
| p95 | 8 |
| p99 | 25.5 |
| max | 33 |
| count =0 | 90 (75%) |
| count ≥5 | 15 (12.5%) |
| count ≥10 | 4 (3.3%) |

Unlike `maxNumCols`, `totalSpanningCellCount` is zero for three-quarters of the broad sample — a much more skewed, long-tailed distribution. It does **not** track `maxNumCols` cleanly: several high-`maxNumCols` pages have zero spanning cells (e.g. `pdfPageIndex` 315: `maxNumCols`=19, spans=0), while some moderate-`maxNumCols` pages have very high spanning counts (e.g. `pdfPageIndex` 630: `maxNumCols`=12, spans=**33**, the single highest spanning count in the entire broad sample — not independently visually inspected in this task, a disclosed gap, §19).

## 10. High-tail pages and visual inspection

Per the predeclared rule (highest-ranked pages + boundary-near pages, deduplicated against the known set), 8 pages were selected for inspection; 5 were actually rendered and read within this task's time budget (disclosed limitation, §19):

| `pdfPageIndex` (printed) | Selection basis | `maxNumCols` | Visual finding |
|---|---|---:|---|
| 866 (875) | Highest-tail, #2 | 20 | **Genuine `事務事業別内訳表`-shaped matrix** — item `002 ユネスコ事業計画の推進`, same family as the known group, blank-triple header, new instance |
| 315 (324) | Highest-tail, #3 | 19 | **Genuine same-family matrix** — item `080 初等中等教育段階におけるグローバル人材の育成` → `005 小・中・高等学校を通じた英語教育強化事業`, another new instance |
| 1091 (1100) | Highest-tail, #4 | 19 | **Genuine same-family matrix** — item `015 メディア芸術の振興` → `001 メディア芸術の創造・発信プラン`, another new instance, in a third organization (`文（文）` printed-label prefix, i.e. within 文化庁) |
| `pdfPageIndex` 11 (20) | Boundary-near (`=11`) | 11 | **Genuinely ordinary** — `005 叙勲褒章費等`, a deeply-nested but entirely ordinary numbered remarks breakdown (no embedded matrix); Docling's own segmentation happened to produce 11 columns from this page's dense quantity×unit-price remarks formatting |
| `pdfPageIndex` 22 (31) | Boundary-near (`=11`) | 11 | **Genuinely ordinary** — a continuation page of nested remarks-column calculations, no embedded matrix |
| 1271, 585, 34 | Highest-tail #5, boundary-near | 18, 17, 11 | **Not inspected in this task** (time-budget limitation, §19) |

**Finding an ordinary page with `maxNumCols ≥11` is, per the task's own framing, the single most valuable result of this validation, not a failure.** Two such pages were found and are recorded above without qualification.

## 11. Ordinary high-column counterexamples (source vs. engine anomaly)

For the two confirmed-ordinary boundary pages (`pdfPageIndex` 11, 22): the **source-side visual structure** is an entirely ordinary vertical ledger row followed by a dense, multi-line, quantity×unit-price remarks paragraph (e.g. `2回　＠763,518円　1.1`) — a structure already well-documented across every prior case in this repository, not a special table. The **Docling-side representation** segments this dense remarks text into many short cell-like fragments, producing a `maxNumCols` of 11 purely as an artifact of how TableFormer's grid-fitting handles closely-spaced numeric/label fragments in a narrow remarks column — **not** because the source page itself has 11 semantic columns. This is a clean, disclosed instance of **engine anomaly (Docling's own segmentation behavior on dense remarks text) being mistakeable for source anomaly** if `maxNumCols` alone were trusted without visual confirmation — exactly the risk the task asked to be kept separate.

For the three confirmed-special pages (866, 315, 1091): the source-side visual structure genuinely is a wide, multi-column matrix distinct from the ordinary ledger rhythm (§4.2 of `075474e`, reconfirmed here) — in these cases, Docling's high `maxNumCols` **does** correspond to a genuine source-side structural difference, not merely an engine artifact.

**Conclusion: the same numeric signal value (`maxNumCols` around 11–20) can arise from two structurally different underlying causes — a genuine embedded matrix, or Docling's own dense-remarks-text segmentation — and cannot be told apart without visual confirmation.** This is the central, load-bearing finding of this validation.

## 12. Known-page reference results (evaluated after sampling/feature freeze)

| `pdfPageIndex` | `maxNumCols` | `totalSpanningCellCount` | In broad sample? |
|---|---:|---:|---|
| 84 | 20 | 0 | No |
| 182 | 18 | 29 | No |
| 264 | 18 | 12 | No |
| 713 | 15 | 6 | No |
| 770 | **11** | 0 | No |
| 845 | **11** | 2 | No |
| 1169 | 22 | 5 | **Yes** (coincidental) |
| 1278 | 20 | 1 | No |
| 1326 (flagship) | 20 | 16 | No |

All values re-confirmed byte-identical to the prior 16-page survey's own results (same script logic, same source). `pdfPageIndex` 1326 (viewer 1327) itself remains at `maxNumCols`=20 — well above the broad sample's median (10) and squarely within its own top ~5% (`p95`=17, so 20 exceeds `p95`), **but no longer above a clean, non-overlapping threshold**, since 59/120 broad-sample pages already exceed the old boundary of 11, and 2/120 even reach or exceed the flagship's own tier of ≥20.

## 13. Small-sample claim verdict

**Verdict for `maxNumCols`: B — Partially survives, with an important sub-family caveat.**

- The **literal threshold** from the small sample (`≥11` separates known from ordinary) **collapses completely** at broad-document scale — this specific numeric claim is falsified (matching category D for that specific threshold).
- However, **as a continuous measure**, the *extreme* tail (`≥18`, the top ~4% of the broad sample) still shows a strong — though small-n and not perfectly clean — concentration of genuine special-family pages: of the 5 broad-sample pages at this tier, 4 (315, 866, 1091, plus the coincidentally-included known page 1169) are confirmed genuine family members via direct visual inspection or prior knowledge, and only 1 (1271) remains unconfirmed (not a disclosed counterexample, simply un-inspected). Two of the nine known/reference pages (770, 845 — the per-country/per-region itemization sub-family) sit at exactly the collapsed `11` boundary and are **not** distinguishable from ordinary variation by this signal at all at broad-document scale.
- **This is not a uniform verdict across the whole known family**: the project/committee-matrix sub-family (84, 182, 264, 713, 1169, 1278, 1326) remains reasonably well-separated in the extreme tail; the per-country/per-region itemization sub-family (770, 845) does not survive at all.

**Verdict for `totalSpanningCellCount`, judged independently: inconclusive, leaning toward D (collapses) as a standalone signal.** Its distribution is dominated by zeros (75% of the broad sample) and does not track `maxNumCols` consistently (§9) — a broad-sample page (`pdfPageIndex` 630) reaches the single highest spanning-cell count observed in this entire task (33, higher than the flagship page's own 16) while having only a moderate `maxNumCols` (12); this page was not visually inspected, so it is recorded as an open, unresolved data point (§19), not classified either way — but its mere existence, at a value exceeding every known-family page's own spanning count, is itself sufficient to show `totalSpanningCellCount` alone does not reliably track the known family either.

## 14. Source vs. engine anomaly (restated as the central methodological finding)

§11 already gives the concrete evidence; this section restates it as the task's own required, explicit separation: a raw Docling structural signal value, by itself, is **never sufficient** to conclude either "source has unusual structure" or "source is ordinary" — both a genuine embedded-matrix page and a genuinely ordinary but remarks-dense page can produce the same `maxNumCols` value, for entirely different underlying reasons (one reflects the source PDF's own layout; the other reflects Docling's own text-to-grid fitting behavior on dense narrow-column text). Every classification in §10 required visual confirmation; none was inferred from the Docling numbers alone.

## 15. Updated Docling-channel interpretation

- **Small-sample separation was not maintained** as a clean, whole-document-usable rule (§13) — this materially revises `acaf550`'s own more optimistic small-sample framing.
- **False-positive ordinary variation is substantial**: roughly half the broad sample exceeds the old boundary, and at least 2 of those (11, 22) are confirmed, not merely suspected, ordinary pages whose high column count is a Docling remarks-segmentation artifact, not a source anomaly.
- **The high tail is not source-anomaly-free either, though it is dominated by genuine positives in this small check**: 3 of 3 additional high-tail pages actually inspected in this task, beyond the already-known ones, turned out to be genuine new instances of the known special family — a striking, unplanned discovery (§16) suggesting the known family is **considerably more common in this document than the original 6–9 known instances suggested**, not a rare anomaly.
- **Combining channels remains valuable**: given `maxNumCols` alone cannot distinguish source anomaly from Docling segmentation artifact (§11), cross-referencing with the geometry channel's own coordinate-based signal (`075474e`) or the text/grammar channel's rhythm-break signal (`a9c0092`) — both of which are sensitive to different aspects of the same pages — remains a more defensible basis for candidate generation than any single channel alone.
- **Docling alone should likely not be a sole candidate trigger** for this document family, given the demonstrated confusability with dense-remarks-text segmentation; it may be more defensible as a **corroborating/disagreement signal** — i.e., "does this page's Docling table shape look unusual *and* does another channel also flag it" — than as a standalone ranking source.

## 16. Unplanned discovery (disclosed per the task's own instruction)

Three genuinely new instances of the known `事務事業別内訳表`-shaped matrix family were found in this validation's own high-tail inspection (`pdfPageIndex` 866, 315, 1091), spanning at least one organization (文化庁, via `pdfPageIndex` 1091's `文（文）` printed-label prefix) not previously represented among the specific pages checked in `075474e`/`a9c0092`/`acaf550`. Per the task's own framing: this discovery occurred **after** sampling and feature freeze, using only the frozen features, and was classified only after visual inspection — the sampling and feature definitions were not adjusted to find these, nor were they sought deliberately (they were simply the highest-ranked unexamined pages in a predeclared inspection subset). This reinforces §15's suggestion that the "known family" may be a **common, recurring representational convention** in this document rather than a rare special case — a significant reframing worth carrying into any future work on this source, though not proven exhaustively here (only 3 additional confirmed instances, from a 120-page sample, not a full census).

## 17. Architecture implications

- **"Engine failure/disagreement can be useful evidence without being accepted as source truth"** — this principle **held up under broad-sample testing**, and arguably more clearly than before: §11's two ordinary-but-high-`maxNumCols` pages are a concrete demonstration that an engine's own segmentation behavior (not a failure exactly, but a modeling choice under dense text) must be treated as evidence to be corroborated, never as source truth on its own.
- Given the demonstrated confusability, a future architecture should treat **any single-channel structural signal as a candidate-generation input requiring corroboration**, not a standalone anomaly classifier — consistent with, and now more strongly supported than, the multi-channel framing already proposed in the three prior surveys.
- The unplanned discovery (§16) suggests that if this document family's known special structure is genuinely common (not rare), a future Document Profile might more usefully record "does this item's own breakdown use the multi-category matrix convention" as a **document-family-level structural fact** worth checking systematically, rather than treating each instance as an independent one-off anomaly to be discovered by candidate ranking.
- No schema or ADR change is implemented from this section, per the task's own stop condition (§18 below).

## 18. MOF CSV / provenance implications

- The confirmed confusability (§11, §14) directly reinforces that a Docling-derived wide-grid signal must **never** be treated as equivalent to "the source PDF genuinely has N semantic columns here" — in at least two confirmed cases in this broad sample, it instead reflects Docling's own remarks-text segmentation.
- The signal **can** still be useful for *discovering supplementary-representation candidates* (as §16's unplanned discovery demonstrates) — but only as a candidate list requiring visual/cross-channel confirmation, never as an automatic classification.
- **Docling's own table boundary cannot be used as a canonical provenance-region boundary** for MOF-CSV reverse linkage: since the same Docling table object can represent either an ordinary remarks-dense row or a genuinely-different embedded matrix (§11), and since `075474e` already established that Docling merges even a visually-two-region page into one single table object, there is no reliable engine-provided seam to trust for splitting canonical ledger rows from alternate/supplementary representations. Any such splitting would need to rely on visual/geometry evidence (as this whole line of surveys has done), not on Docling's own table boundaries.
- No page in this task is classified as `繰入`, `移替`, or any other MOF-specific concept; none was tested against that question here.

## 19. Limitations

- Only 5 of the 8 predeclared high-tail/boundary candidate pages were actually rendered and visually inspected (`pdfPageIndex` 866, 315, 1091, 11, 22); `pdfPageIndex` 1271, 585, and 34 were not inspected — a time-budget limitation, not a claim about their content.
- `pdfPageIndex` 630's outlier `totalSpanningCellCount` (33, the highest in the entire task) was not visually inspected — its status (genuine anomaly, Docling artifact, or something else) is genuinely unresolved, not merely unmentioned.
- The 120-page systematic sample, while broad and unbiased by construction, is still roughly 9% of the full 1,339-page document — a genuinely exhaustive whole-document run was not performed, and the true population-wide frequency of the known special-table family (suggested by §16 to be considerably higher than previously thought) is not established with precision here.
- `emptyCellRatioProxy`'s own ambiguity (already disclosed in `acaf550`, between genuine source sparsity and Docling's internal span bookkeeping) was not re-investigated or resolved in this task.
- No bbox-based feature was computed, per the task's own explicit prohibition on adding new ranking features in this validation task.

## 20. Recommended next step

Per this task's own stop condition (§15 of the originating instructions), **no further MEXT-detector tuning is recommended as the immediate next step**. Consistent with that instruction, the single most valuable next action is a **repository-level scope decision**: package/consolidate the case-004 MEXT research line (selection, Ground Truth, first frozen benchmark, both context diagnostics, and all four anomaly-channel surveys) for review, rather than continuing to refine anomaly signals on this source — or, alternatively, begin the source-survey phase of a **case-005** on a new ministry, following the same methodology already validated across four cases. Both options are stop-and-report only; **neither is executed in this task**.

Not executed in this task.

---

## Answers required by the originating task

1. **Git**: branch `research/case-004-mext-preregistration`; pre-task HEAD `acaf550`; final commit recorded below; pushed; `main` unchanged.
2. **Frozen-artifact integrity**: source SHA and all prior case-004/anomaly-survey artifacts re-verified byte-identical before and after.
3. **Exact sampling algorithm**: deterministic evenly-spaced `pdfPageIndex` values, `round(i*(N-1)/(sampleSize-1))` for `i` in `range(120)`, `N=1339`, deduplicated (§4).
4. **Actual sampled page count**: 120 unique indices, zero duplicates from rounding (§5).
5. **Sample coverage**: spans `pdfPageIndex` 0 through 1338, evenly spaced (§5).
6. **Missing/unusable Docling pages**: zero — every one of the 120 sample pages and 9 known pages produced a well-formed single table (§7).
7. **Frozen features**: `maxNumCols`, `totalSpanningCellCount`, plus the five auxiliary fields carried over unchanged from `acaf550` (§6).
8. **Broad `maxNumCols` distribution**: median 10, p95=17, p99≈19.8, max 22; 59/120 (49%) ≥11 (§8).
9. **Broad `totalSpanningCellCount` distribution**: median 0, 75% exactly zero, max 33 (§9).
10. **Pages with `maxNumCols ≥11`**: 59 of 120 (§8, full list retained in the script's own JSON output, not committed).
11. **Ordinary high-column counterexamples**: `pdfPageIndex` 11 and 22, both confirmed genuinely ordinary via direct visual inspection despite `maxNumCols`=11 (§10, §11).
12. **Newly discovered special structures**: yes — `pdfPageIndex` 866, 315, 1091, three new confirmed instances of the known `事務事業別内訳表`-shaped matrix family, found only after sampling/feature freeze (§16).
13. **Known-page reference results**: table in §12; all values reproduce the prior 16-page survey exactly.
14. **Did p1327 remain unusual?** Yes in absolute terms (top ~5% of the broad sample, `maxNumCols`=20 vs. broad p95=17), but **no longer above a clean, non-overlapping threshold** the way it was in the 16-page sample.
15. **A/B/C/D verdict for `maxNumCols`**: **B — partially survives**, with a confirmed sub-family split (project/committee-matrix family holds up reasonably at the extreme tail; per-country/per-region itemization family does not survive at all) (§13).
16. **Independent verdict for `totalSpanningCellCount`**: inconclusive, leaning toward collapse as a standalone signal — inconsistent with `maxNumCols`, and its own single highest value in this task belongs to an uninspected, unresolved page (§13, §19).
17. **Source anomaly vs. engine anomaly findings**: directly and concretely demonstrated in both directions — genuine source anomalies (866, 315, 1091) and genuine engine-segmentation-only artifacts (11, 22) both produce elevated `maxNumCols`, indistinguishable without visual confirmation (§11, §14).
18. **Updated role of Docling as an anomaly channel**: a corroborating/candidate-generation input requiring cross-channel or visual confirmation, not a standalone, sufficient anomaly classifier for this document (§15).
19. **Architecture implications**: reinforces treating any single engine-derived structural signal as needing corroboration before being trusted as source truth; suggests the known special structure may be a common document-family convention rather than a rare anomaly, worth recording as a structural fact rather than discovering ad hoc (§17).
20. **MOF CSV implications**: Docling's own table boundaries cannot be trusted as canonical provenance-region boundaries; the wide-grid signal is useful only as an unconfirmed candidate list (§18).
21. **Files changed**: this report plus `state/{CURRENT_STATE.json,TODO.md,CHANGELOG.md}`; no research script committed; no production file modified.
22. **Validation**: `npm run validate` and `git diff --check` both pass (recorded at commit time).
23. **Limitations**: disclosed in §19, most significantly the incomplete high-tail visual inspection and the still-partial (9%) document coverage.
24. **Recommended next step**: per this task's own stop condition, no further MEXT-detector tuning — the next valuable action is a repository-level scope decision (package the case-004 research line for review, or begin case-005) rather than another anomaly-signal experiment (§20). Not executed in this task.

**Overall answer to this validation's own central question**: the small-sample clean separation **did not survive intact** — it degrades to a partial, sub-family-dependent signal at broad scale, and the underlying value can arise from either genuine source structure or a purely Docling-side segmentation artifact on dense ordinary text, confirmed concretely in both directions within this same 120-page sample. The validation's most valuable output is not a preserved ranking but this confirmed **confusability**, plus an unplanned but well-evidenced signal that the "known special family" is more widespread in this document than previously understood.
