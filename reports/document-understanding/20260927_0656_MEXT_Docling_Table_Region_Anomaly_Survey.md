# MEXT Docling Table-Region Anomaly Survey

Status: **exploratory, read-only survey. No production/schema change. No Ground Truth/benchmark change. No new benchmark target registered.**

Date: 2026-09-27 (Asia/Tokyo)

## 1. Research question

> Can Docling's already-existing table-region/cell-grid/layout representation, independent of the geometry channel (`075474e`) and the text/grammar channel (`a9c0092`), candidate structural deviation from the ordinary MEXT ledger without knowing any special structure's name in advance — and does it add genuinely new information the other two channels missed?

This survey's deliverable is not "prove Docling finds p1327" — it is to determine whether Docling's own native table representation is a materially different, additive observation channel, or largely redundant with what the coordinate-geometry and text/grammar channels already showed.

## 2. Frozen inputs / integrity (verified before and after this task)

- Branch `research/case-004-mext-preregistration`; pre-task `HEAD` `a9c0092`; working tree clean; `main` unchanged at `3b29ebd`.
- Source `mext-fy2024-general-account-expenditure-request-detail`, SHA-256 `6df221dfd22c48e0f32dd59bcf2dbcbaad19720083be43005ce700b984a6bf71` — recomputed by the scratch script itself before any Docling call, and independently via `shasum` before/after this task; matches.
- case-004 selection protocol (`c2b2c28`), selection record (`fa82c13`), Ground Truth (`f9b2f35`), first frozen benchmark (`49f5ca6`), organization-010/020 diagnostics (`187a8e9`/`aedea1c`), the geometry survey (`075474e`), and the text/grammar survey (`a9c0092`) — all re-verified byte-identical to their freeze commits, before this task began and again immediately before commit. None was rewritten.
- Known locator (evaluation reference only, not a training target): viewer/1-based PDF page **1327** = `pdfPageIndex` **1326** = printed **文（ス） 1335**.

## 3. Docling raw representation inventory (confirmed, not assumed)

Before deciding any signal, the already-committed adapter (`scripts/document-understanding/adapters/docling/src/run.py`) and one already-generated raw artifact (`derived/document-understanding/case-004/docling.raw.json`) were read directly to establish exactly what Docling's raw output actually contains in this repository's own usage:

**Confirmed present** (used as features below):
- Per page: a list of `tables`, each with `tableIndex`, `numRows`, `numCols`, and a flat `cells` list.
- Each cell: `row`, `col`, `rowSpan`, `colSpan`, `text` (`start_row_offset_idx`/`start_col_offset_idx`/`row_span`/`col_span`/`text` on Docling's own `TableCell` object).
- A separate `texts` list (non-table text blocks), each currently reduced to a plain string by this repository's adapter (`t.text` only).
- `doc.export_to_markdown()` — not used as a numeric feature in this task, but confirmed available.

**Confirmed present, but not exposed by the existing adapter** — checked directly against Docling's own `TableCell` objects in this task's own scratch script, not assumed: a `bbox` attribute **is** present on Docling's table-cell objects in the installed version (confirmed via `hasattr(cell, 'bbox')` returning a non-`None` value on every page tested). This means true bounding-box/page-occupancy signals (task category F) are **available in principle**, though this survey's own frozen features (§6) did not end up depending on bbox values themselves — only on their confirmed availability, reported here as inventory, not exploited further within this task's time budget (disclosed as a limitation, §18).

**Not confirmed / not investigated**: whether `doc.texts` objects carry their own bounding boxes (not checked, since this task's features did not require it); merged/spanning-cell semantics beyond the `rowSpan`/`colSpan` integers themselves (e.g., whether Docling ever emits a cell whose span extends beyond the table's own declared `numRows`/`numCols` — not tested); table-to-table positional relationships (moot in this run, since **every single page tested, in both the baseline and known groups, produced exactly one Docling table object** — see §9).

## 4. Anti-overfitting protocol

No feature below references `事務事業別内訳表`, `国庫債務負担行為`, `16-15`, `111`, any known special-family name, Ground Truth values, or the known-anomaly page list from `075474e`/`a9c0092`. The feature-computation script (§7) was written and frozen before it was run against any page, and the known-page group was analyzed in the **same single script execution** as the baseline group — both groups' features were computed by the identical, unmodified code path; only the after-the-fact grouping label (`sampleGroup: baseline` vs. `known`) distinguishes them in the output, and that label was never read by the feature-computation logic itself. No threshold was adjusted after seeing where known pages landed.

## 5. Production benchmark separation

This survey does **not** reuse `scripts/document-understanding/benchmark/src/normalize-docling.mjs` (which is deliberately scoped to a single case's `pdfPageIndex` and Ground-Truth-adjacent row-matching logic). Instead, a standalone Python scratch script (kept outside the repository, in this session's own scratch directory; not committed) calls Docling's `DocumentConverter` directly, mirroring only the **raw-extraction** field shape already used by the production adapter (`run.py`'s own `tables`/`cells`/`texts` construction) — never its Ground-Truth-reading or row-matching logic. The script never opens `ground-truth.json` and never imports anything from `scripts/document-understanding/benchmark/` or `.../adapters/docling/`.

## 6. Docling-native candidate signals (frozen before evaluation)

Given the confirmed inventory (§3), the following independent, non-combined signals were defined:

- **A — table count**: `tableCount` per page.
- **B — grid shape**: `maxNumCols`, `maxNumRows`, `maxCellCount` (the largest table's own column/row/cell counts, per page).
- **C — multiple incompatible grids**: `incompatibleGridsFlag` = true only if `tableCount ≥ 2` **and** the ratio of the largest to smallest table's `numCols` on that page is ≥1.5 (an arbitrary but pre-declared generic ratio threshold, fixed before any page was analyzed).
- **D — cell occupancy/sparsity and numeric density**: `emptyCellRatioProxy` = 1 − (total cells actually present ÷ total `numRows×numCols` grid slots, summed across the page's tables) — a *proxy*, explicitly caveated (§17) since Docling's own `table_cells` list may already represent post-span-merge logical cells rather than every raw grid slot, so a high value here is not proven to mean "genuinely sparse source table" as opposed to "Docling's own span bookkeeping." `numericHeavyCellRatio` = the fraction of all cells whose text matches a generic numeric/punctuation-only pattern (digits, commas, `△`, parentheses, whitespace) — a generic amount-cell density proxy, not tied to any specific column name.
- **E — grid discontinuity across pages**: not implemented as a standalone signal in this task (disclosed gap, §17) — the small, non-contiguous sample (§9) does not support a meaningful adjacent-page comparison.
- **F — table-region occupancy via bbox**: bbox availability confirmed (§3) but not computed into a scored feature in this task (disclosed gap, §17, §20).
- **G — parse-instability-as-signal**: `totalSpanningCellCount` (sum of cells with `rowSpan>1` or `colSpan>1`) is reported descriptively as a candidate proxy for "this one merged table actually reconciles rows of very different natural width" — explicitly **not** conflated with "source structural anomaly" without visual confirmation (§11).

## 7. Feature freeze

The script (kept in this session's own scratch directory, not committed) was finalized — every field above, the `1.5` ratio threshold, and the fixed page lists below — **before** it was executed even once. It was then run in a single execution covering both groups (§9); the known-page group's results were written to the same output file, in the same pass, as the baseline group's — there was no separate "tune, then check known pages" step possible even in principle, since both groups came from one unmodified run. Missing/failed pages would have been recorded with an explicit `error` field (none occurred; every one of the 16 pages attempted succeeded). No numeric feature was backfilled with 0 for any page; none was needed here since none failed.

**Baseline definition, declared before analysis**: pages already independently confirmed ordinary in prior tasks (`pdfPageIndex` 1 — the same-page item-header-and-first-expense sample from the organization-010 diagnostic; `pdfPageIndex` 2 — the frozen case-004 target itself; `pdfPageIndex` 119 — an organization-010 same-page sample; `pdfPageIndex` 896 — an organization-020 same-page sample), plus three additional pages chosen by a simple, predeclared machine rule (round-numbered 1-based pages 50, 500, 1000 — chosen for arithmetic simplicity and spread across the document, not for any content property).

## 8. Document-wide vs. broad-sample scope decision (disclosed, not hidden)

Running Docling's full model pipeline (layout + TableFormer) once per page, individually, across all 1,339 pages was judged computationally excessive for this task's time budget — each single-page `DocumentConverter.convert()` call reloads/re-runs the model pipeline, and this repository's own case-004 benchmark run already took several seconds for one page. **This survey therefore used a fixed, predeclared 16-page sample** (7 baseline + 9 known/reference), not a whole-document or broad random sample, and does **not** claim any page's whole-document percentile rank — a materially narrower scope than the geometry and text/grammar surveys' own full 1,338-page runs. This is the single most important scope limitation of this report and is repeated in §18.

## 9. Results (baseline vs. known/reference group, single unmodified run)

| Group | `pdfPageIndex` | `tableCount` | `maxNumCols` | `maxNumRows` | `maxCellCount` | `totalSpanningCellCount` | `emptyCellRatioProxy` | `numericHeavyCellRatio` | `incompatibleGridsFlag` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| baseline | 1 | 1 | 6 | 2 | 9 | 0 | 0.25 | 0.22 | false |
| baseline | 2 (frozen target) | 1 | 9 | 32 | 149 | 2 | 0.48 | 0.57 | false |
| baseline | 49 | 1 | 9 | 2 | 10 | 0 | 0.44 | 0.10 | false |
| baseline | 119 | 1 | 6 | 2 | 12 | 0 | 0.00 | 0.25 | false |
| baseline | 499 | 1 | 9 | 2 | 10 | 0 | 0.44 | 0.20 | false |
| baseline | 896 | 1 | 6 | 2 | 9 | 1 | 0.25 | 0.33 | false |
| baseline | 999 | 1 | 9 | 24 | 97 | 0 | 0.55 | 0.56 | false |
| known | 84 | 1 | **20** | 26 | 263 | 0 | 0.49 | 0.81 | false |
| known | 182 | 1 | **18** | 23 | 148 | **29** | 0.64 | 0.49 | false |
| known | 264 | 1 | **18** | 20 | 139 | **12** | 0.61 | 0.67 | false |
| known | 713 | 1 | **15** | 18 | 179 | 6 | 0.34 | 0.10 | false |
| known | 770 | 1 | **11** | 2 | 18 | 0 | 0.18 | 0.22 | false |
| known | 845 | 1 | **11** | 3 | 14 | 2 | 0.58 | 0.07 | false |
| known | 1169 | 1 | **22** | 20 | 202 | 5 | 0.54 | 0.74 | false |
| known | 1278 | 1 | **20** | 18 | 200 | 1 | 0.44 | 0.82 | false |
| known | 1326 (flagship) | 1 | **20** | 22 | 158 | **16** | 0.64 | 0.68 | false |

**Headline finding, within this 16-page predeclared sample**: `maxNumCols` **cleanly separates the two groups with zero overlap** — every baseline page has `maxNumCols ≤ 9`; every known/reference page has `maxNumCols ≥ 11`. This is a materially cleaner separation, in this small sample, than either the geometry channel's own coordinate-based proxy (`075474e`: known family ranked 35th–58th of 1,338 on its own best signal) or the text/grammar channel's own signals (`a9c0092`: known family often outside even the top 10%). **This is reported with its scope limitation attached, not as a whole-document result** — see §8, §18.

`incompatibleGridsFlag` is **false for every single page in both groups**, without exception — see §11 for what this means.

## 10. Blind new-candidate inspection

Per the task's own instruction, this section's rule was to select top-unseen candidates from the frozen signals, excluding already-known pages, then inspect visually. **Given this survey's scope was fixed to the predeclared 16-page sample (§8) rather than a whole-document or broad-sample run, no *additional* unseen top-ranked candidates exist to select from** beyond the 16 pages already analyzed — the frozen sample and the evaluation set are, in this specific task, the same 16 pages. This is disclosed honestly as a direct consequence of the §8 scope decision, not concealed: **a genuine blind new-candidate discovery step, as performed in the geometry and text/grammar surveys, was not possible within this task's scope** and is deferred to the recommended next experiment (§20).

## 11. Source anomaly vs. engine anomaly

- **The visually-observed "two-layer" structure (§13) is not represented by Docling as two separate table regions on any page tested** — `tableCount` is 1 and `incompatibleGridsFlag` is false everywhere, including on the flagship page. This is a genuine, informative **negative** result for the literal "multiple table regions" framing (task category A/C): in this Docling version/configuration, TableFormer merges the entire page's grid-like content, embedded matrix and ordinary ledger rows alike, into one single table object with a wide, irregular column structure — not into two coexisting, independently-identifiable regions.
- The consequence is a genuine **engine-representation choice**, not evidence about the source PDF's own layout: the source page visually contains what looks like two structurally distinct regions (§13), but Docling's own segmentation collapses them into one. Attributing the *resulting* high `maxNumCols`/`totalSpanningCellCount` values directly to "the source has two tables" would conflate a source fact with an engine's specific merging behavior — this report keeps the two separate: the **source-observable** fact is what §4.2 of the prior geometry survey already established by direct visual inspection (an embedded matrix distinct from the ordinary ledger); the **engine-derived** fact established here is that Docling represents that same page as one wide, spanning-cell-heavy table, not as two.
- No evidence was found in this task of a genuine Docling *parsing failure* (e.g., a crash, an empty result, or a grid whose `numRows×numCols` is wildly inconsistent with its own `cellCount` in a way suggesting fragmentation) — every one of the 16 pages produced a well-formed single table with a plausible cell count relative to its own declared dimensions. **`emptyCellRatioProxy` values in the 0.5–0.65 range (seen on both some known and some baseline pages, e.g. baseline `pdfPageIndex` 999's 0.55) were not independently confirmed, in this task, as either genuine source sparsity or engine-side span bookkeeping** — this ambiguity is disclosed rather than resolved, per the task's own caution against conflating the two.

## 12. Three-channel comparison

| Page/family | Geometry (`075474e`) | Text/grammar (`a9c0092`) | Docling-native (this task) | Visual interpretation |
|---|---|---|---|---|
| `pdfPageIndex` 1326 (flagship) | `maxRowBandWidth` rank 58/1338 (~top 4%) | Best text signal rank 187/1338 (~top 14%); never top-10% | `maxNumCols`=20, cleanly above the entire baseline group's ≤9 (16-page sample only) | Embedded matrix + resumed ledger, blank header triple |
| 84, 845 | Both inspected/confirmed anomalous | Both reach top-10% on text signals — the two channels' clearest agreement | Both cleanly separated from baseline by `maxNumCols` too | Committee-matrix and per-country-itemization respectively — **all three channels agree on both** |
| 264, 1169, 1278, 713 | Ranked more sharply by geometry than by text | Ranked only moderately-to-poorly by text | All four cleanly separated from baseline by `maxNumCols` in this sample | The Docling channel, within its own small sample, separates this family **at least as cleanly as geometry**, though not compared at whole-document scale |
| 182, 770 | Not part of `075474e`'s own inspected set | **Found first** by text/grammar | Also cleanly separated from baseline by `maxNumCols`, once added to this task's sample | Confirms text/grammar's own finding; Docling's signal, had it been run at whole-document scale, would very plausibly have found these too — not proven, since no whole-document Docling run was performed |

**Answers to the task's specific questions:**
- **Strong in all three?** `pdfPageIndex` 84 and 845 — the only two pages with independent confirmation across geometry, text/grammar, and Docling-native signals in this survey's actual (small) inspected/sampled sets.
- **Geometry only?** None of the seven original known pages were *missed* by Docling's `maxNumCols` in this sample; geometry's own advantage was in having already covered the *whole* document, not in detecting something Docling's proxy structurally cannot.
- **Text only?** `pdfPageIndex` 182 and 770 were discovered first by text/grammar, not because Docling could not see them (it separates them cleanly once tested, §9), but because Docling was never run against the whole document to find them independently.
- **Docling only?** None found in this task — Docling's own signal was only evaluated against pages the other two channels had already identified or that were chosen as generic baseline, so it had no opportunity to surface a page neither other channel had already touched (§10's scope limitation).
- **Which family is easiest to see in which representation?** The `事務事業別内訳表`-shaped matrix family (84, 182, 264, 1169, 1278, 1326) is captured cleanly by all three channels once tested. The per-country/per-region itemization family (770, 845) is captured cleanly by Docling's `maxNumCols` and by geometry's proxies, but was comparatively weak on several text/grammar signals (`a9c0092` §9) — text/grammar's `denseNumericUnmatchedCount` was its one strong signal for this specific sub-family.
- **Did the Docling channel add genuinely independent information?** **Within this survey's own scope, only partially confirmed**: it did not surface any page the other two channels had not already found (§10's limitation), but it **did** separate the entire known/reference group from a baseline group more cleanly, on a single simple metric (`maxNumCols`), than either other channel's own best single metric managed against the *whole* document. Whether this cleanliness would survive a genuine whole-document Docling run (with its much larger and more varied baseline) is **not established here** — a materially important caveat, not a proven claim.
- **Is Docling failure-as-signal valuable or risky?** Not testable in this task, since no failure occurred in the 16-page sample; the risk described in §11 (conflating engine-merging behavior with source structure) is real and was actually observed here (the "two tables" hypothesis being an engine artifact, not confirmed source truth), even without an outright Docling *failure*.

No ensemble score was built, per the task's instruction.

## 13. 2-layer structure observations (source-safe/mechanical only)

Re-examining the already-documented visual facts from `075474e` §4.2 through this task's own mechanical lens:

- **Multiple table regions**: not observed in Docling's own segmentation (§9, §11) — zero pages produced `tableCount ≥ 2`.
- **Incompatible grid geometries**: not observed as *separate* incompatible grids (since there is only ever one table object); however, the *within-table* column count (`maxNumCols`) on every known/reference page is substantially wider than every baseline page's own single table, and spanning-cell counts are frequently elevated (182: 29, 264: 12, 1326: 16) — consistent with, though not proof of, a single merged table object internally reconciling two structurally different row-widths via cell-spanning, which is the same underlying visual fact (§4.2's "the row rhythm changes and returns") expressed through Docling's own specific representation choice.
- **Ledger-like + matrix-like coexistence**: source-safe-observable via direct rendering (already established in `075474e`), but **not independently confirmed via Docling's own structure** beyond the elevated column-count/spanning-cell proxy above — Docling's flattened single-table view does not, on its own, distinguish "this row belongs to the ledger-like region" from "this row belongs to the matrix-like region."
- **Blank header-row amount area + separate numeric grid**: not independently re-confirmed via Docling cell inspection in this task (would require reading individual cell `row`/`col`/`text` values for the flagship page, not done here — a disclosed limitation, §18).

Semantic interpretation (supplementary representation, cross-tab, duplicate representation) is, per the task's instruction, **not** discussed further here — those terms were only ever used in the prior surveys' own post-visual-inspection sections, not as detection input anywhere in this task.

## 14. Request-scope observations

No new visual inspection of any candidate's request-number column was performed in this task specifically for this purpose — the request-scope evidence already gathered in the text/grammar survey (`a9c0092` §12: the request-number column does not reset across the internal representation change, confirmed for `pdfPageIndex` 1326 and 1278) is **not re-derived here**, and this task adds no new request-scope evidence. This is disclosed as a scope gap rather than silently omitted, since the task explicitly asked for this where practical — it was judged not practical to re-derive within this task's Docling-focused time budget, given the evidence already exists from the prior survey.

## 15. Architecture implications (conceptual only, no implementation)

Extending the three-channel flow proposed in this task:

```text
Raw PDF
  ↓
raw extraction/layout observations
  ├─ flat text/order channel        (a9c0092: pure text, weakest single-channel separation of the known family)
  ├─ coordinate geometry channel    (075474e: pdf.js coordinates, moderate separation, whole-document scale)
  └─ table/layout-engine channel    (this task: Docling, cleanest small-sample separation, NOT run at whole-document scale)
          ↓
structural anomaly candidates
          ↓
cross-channel evidence             (§12: agreement on 84/845; each channel individually incomplete)
          ↓
context expansion / document understanding / representation-role classification / semantic interpretation
```

- **Is the Docling signal source-safe or engine-derived?** Firmly **engine-derived**, more so than either other channel: `maxNumCols`/`totalSpanningCellCount` are specific artifacts of Docling's own TableFormer segmentation and merging decisions (§11), not something a human reading the raw PDF would independently produce as a number — a different table-structure model could plausibly segment the same page differently (e.g., into two tables instead of one wide one), which would change these exact values without the source page changing at all.
- **How to separate source structural anomaly from Docling parse anomaly?** This task's own experience (§11) is itself the answer: a signal computed from one engine's structural output must always be checked against direct visual inspection of the source before being called a "source" fact — this task explicitly avoided concluding "the source page has two tables" from Docling's own single-table output, and equally avoided concluding "the source page has one table" from the same fact, reporting instead exactly what Docling's segmentation choice was and flagging it as a choice, not a source truth.
- **Could this feed Strategy Selection?** Plausibly, but with a caveat this task surfaces cleanly: an engine-derived anomaly signal (like Docling's own `maxNumCols`) is only as trustworthy as that specific engine's own segmentation stability — a future Strategy Selector relying on it should ideally also track whether *multiple* engines' signals agree (§12's cross-channel agreement column), not trust any single engine's structural choice in isolation.
- **Case Package: raw observation or derived feature?** This task's own practice supports recording the **raw observation** (`tableCount`, `numRows`, `numCols`, `cellCount`, `spanningCellCount`, all directly read from Docling's own object model) rather than a derived "is this anomalous" label — the derived interpretation (§9's baseline/known separation) is downstream of, and should remain revisable independent of, the raw numbers.
- **Engine consensus/disagreement as a signal?** Not tested in this task (no second table-structure engine was run for comparison), but conceptually motivated by this task's own §11 finding: since Docling's single-table merging is itself a modeling choice, a genuinely different table-segmentation engine disagreeing with it (e.g., reporting two tables where Docling reports one) would itself be informative — a plausible future direction, not tested here.
- **`unknown` preservation**: no candidate in this task's fixed 16-page sample required an `unknown` classification (every page was already independently classified as either baseline-ordinary or a known-family member from the prior two surveys); the category remains conceptually available and unused in this particular run, not eliminated.

## 16. MOF CSV implications

- Docling's own single-merged-table representation (§9, §11) is a concrete illustration of the risk already flagged in `075474e`/`a9c0092`: an automated pipeline trusting one engine's table segmentation at face value could easily fail to distinguish "canonical ledger row" cells from "embedded matrix" cells **within the very same Docling table object**, since both now share one `tableIndex` — a naive "read every cell of every Docling table as a canonical ledger row" strategy would not only risk double-counting, it would not even have an engine-provided seam at which to split the two representations apart.
- This reinforces that Docling's own table segmentation, at least as currently observed, is **not sufficient on its own** to identify provenance regions (task's own hoped-for use) for this specific document family — it collapses exactly the distinction a provenance-aware mapping would need to preserve.
- No page in this task is classified as `繰入`, `移替`, or any other MOF-specific concept; none was tested against that question here.

## 17. Failed/weak signals

- **`incompatibleGridsFlag` (category C) never fired, on any page, in either group** — not because the underlying phenomenon (structurally different row-widths coexisting) is absent (§13's spanning-cell evidence suggests it is present, internally, within the single merged table), but because this specific signal's precondition (`tableCount ≥ 2`) was never satisfied by Docling's own segmentation choice in this sample. This is a clean, disclosed failure of the specific operationalization, not evidence against the underlying concept.
- **`emptyCellRatioProxy` did not cleanly separate the two groups** — baseline `pdfPageIndex` 999 (0.55) and 2 (0.48) overlap with known-group values (0.34–0.64); this signal, as defined, is not a reliable standalone anomaly indicator in this sample, and its own caveat (§6: possibly reflecting Docling's internal span bookkeeping rather than genuine source sparsity) further weakens confidence in it.
- **`numericHeavyCellRatio` was inconsistent across the known group** — very low for 713 (0.10), 845 (0.07), and 770 (0.22), but high for 84 (0.81), 1278 (0.82), and 1326 (0.68) — reflecting that the per-country/per-region itemization sub-family (713, 845, 770) actually contains more label text than raw amounts relative to the project/committee-matrix sub-family, a genuine within-family heterogeneity this single signal cannot resolve on its own.
- **Category E (grid discontinuity across adjacent pages) and category F (bbox-based occupancy) were not implemented as scored signals** (§6) — disclosed gaps, not negative results, mirroring the same honest disclosure pattern already used in both prior surveys.

## 18. Limitations

- **This survey's central limitation is scope, not method**: only a fixed, predeclared 16-page sample was analyzed (§8), not a whole-document or broad random sample — `maxNumCols`'s clean 9-vs-11 separation is a genuine finding *within this sample* but has **not** been shown to hold as a whole-document ranking claim comparable to the geometry and text/grammar surveys' own 1,338-page runs. A single unusually-wide but entirely ordinary table elsewhere in the document (not sampled here) could plausibly exist and would not have been caught by this task.
- No blind, whole-document-driven new-candidate discovery was possible under this scope (§10) — this is a materially weaker deliverable than the other two surveys' own genuine blind discoveries.
- `emptyCellRatioProxy`'s ambiguity between genuine source sparsity and Docling's own span-merging bookkeeping was not resolved by independently reading individual cells' `row`/`col` values against the source's own visual layout (§6, §11) — a real, disclosed gap.
- Bbox availability was confirmed (§3) but not exploited into an actual occupancy-ratio feature in this task, for time-budget reasons.
- No second table-structure engine was run for cross-engine agreement comparison (§15).
- Request-scope evidence (§14) was not independently re-derived in this task; it relies entirely on the prior survey's own findings.

## 19. Open questions

- Would `maxNumCols`'s clean separation survive a genuine whole-document Docling run, or would some ordinary pages elsewhere in the ~1,339-page document also exceed the ≤9 baseline ceiling observed here?
- Is the elevated `totalSpanningCellCount` on several known-family pages (182, 264, 1326) a reliable proxy for "two structurally different row-widths reconciled within one merged table," or coincidental to this specific small sample?
- Would a different table-structure engine (or a different Docling configuration/version) segment these same pages into two separate table objects instead of one, and if so, would that disagreement itself be a more informative signal than either engine's own single-table view?
- Does the per-country/per-region itemization sub-family (713, 845, 770) warrant its own, separately-tuned Docling-native signal, given its clearly different `numericHeavyCellRatio` profile from the project/committee-matrix sub-family?

## 20. Recommended next experiment

A single, focused follow-up: **run this same frozen `maxNumCols` (and `totalSpanningCellCount`) feature extraction across a genuinely broad, machine-selected sample of at least 100–150 pages spread evenly across the whole 1,339-page document** (not just the already-known 16), to test whether the clean 9-vs-11 separation observed here (§9) survives contact with a much larger and more varied baseline, or whether some ordinary pages elsewhere in the document also exceed the small-sample baseline ceiling — still without Ground Truth, without registering any new benchmark target, and without implementing a production detector.

Not executed in this task.

---

## Answers required by the originating task

1. **Git**: branch `research/case-004-mext-preregistration`; pre-task HEAD `a9c0092`; final commit recorded below; pushed; `main` unchanged.
2. **Frozen-artifact integrity**: source SHA, case-004 selection/GT/first-run benchmark, both context diagnostics, and both prior anomaly surveys all re-verified byte-identical before and after.
3. **What Docling raw representation actually provided**: per-page `tables` (tableIndex/numRows/numCols/cells with row/col/rowSpan/colSpan/text), non-table `texts` (plain strings only, in this repository's current adapter), and a confirmed-but-unexploited `bbox` attribute on cell objects (§3).
4. **Ordinary baseline**: 7 pages — 4 already-confirmed-ordinary pages from prior tasks plus 3 machine-picked round-numbered pages (§7); `maxNumCols` ≤9 for all 7.
5. **Frozen features**: `tableCount`, `maxNumCols`/`maxNumRows`/`maxCellCount`, `incompatibleGridsFlag` (threshold 1.5, never fired), `emptyCellRatioProxy`, `numericHeavyCellRatio`, `totalSpanningCellCount` (§6–§7).
6. **Whole-document/sample coverage**: a fixed, predeclared 16-page sample only — **not** whole-document, disclosed as the survey's central scope limitation (§8, §18).
7. **p1327 blind ranking**: within this 16-page sample, `pdfPageIndex` 1326's `maxNumCols`=20 places it cleanly above every baseline page (≤9) — a clean small-sample separation, not a whole-document percentile.
8. **Known-family results**: every one of the 9 known/reference pages shows `maxNumCols ≥ 11`, cleanly separated from all 7 baseline pages' `≤9` (§9 table).
9. **New blind candidates**: none — this survey's fixed scope (§8) did not include a whole-document or broad-sample pass, so no genuinely new, previously-unseen candidate could be surfaced (§10).
10. **Visually ordinary candidate**: none newly classified in this task (all 16 pages' classifications were already established by prior surveys or by construction as baseline); no new visual inspection was performed here.
11. **Source anomaly vs. Docling engine anomaly**: kept explicitly separate throughout — the visually-confirmed two-region source layout (from `075474e`) is **not** reproduced as two Docling table objects; Docling instead merges both regions into one wide, spanning-cell-heavy table, which is an engine segmentation choice, not new source evidence (§11).
12. **Three-channel comparison**: geometry and Docling-native both separate the known family cleanly from generic baselines using different mechanisms; text/grammar is comparatively weaker for the flagship page specifically but found two family members neither other channel's own inspected set included; all three agree on `pdfPageIndex` 84/845 (§12).
13. **2-layer structure in Docling representation**: not visible as two separate table regions; visible only indirectly, as an unusually wide single table with elevated spanning-cell counts on several known pages (§13).
14. **Request-scope evidence**: none newly gathered in this task; relies entirely on the prior text/grammar survey's own findings (§14).
15. **Architecture implications**: Docling signals are more clearly engine-derived than the other two channels; a raw-observation-not-derived-label Case Package practice is supported; cross-engine consensus is a plausible, untested future direction (§15).
16. **MOF CSV implications**: Docling's own single-table merging actively removes the very seam a provenance-aware mapping would need, reinforcing that engine table segmentation cannot be trusted alone for this purpose (§16).
17. **Files changed**: this report plus `state/{CURRENT_STATE.json,TODO.md,CHANGELOG.md}`; no research script committed; no production file modified.
18. **Validation**: `npm run validate` and `git diff --check` both pass (see below).
19. **Limitations**: the fixed 16-page (not whole-document) scope is the dominant limitation (§18), alongside the unresolved `emptyCellRatioProxy` ambiguity and unexploited bbox data.
20. **Recommended next experiment**: run the same frozen `maxNumCols`/`totalSpanningCellCount` extraction across a genuinely broad, machine-selected 100–150-page sample spanning the whole document, to test whether the clean small-sample separation survives a larger, more varied baseline (§20). Not executed in this task.

**Overall answer to the survey's own stated question**: within this task's necessarily limited (16-page, not whole-document) scope, Docling's native table representation produced the **cleanest single-metric separation** (`maxNumCols`, zero overlap) of the three channels tested so far — but this cleanliness is **not yet proven to generalize** to the whole document the way the other two channels' own findings are, and the channel did **not**, in this task, surface any genuinely new candidate the other two channels had not already found. Docling adds a materially different, engine-derived perspective — and, importantly, a cautionary one (§11's single-table-merging finding) — rather than a proven, whole-document-validated improvement over the other two channels.
