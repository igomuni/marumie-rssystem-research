# MEXT Text/Grammar-Transition Anomaly Survey

Status: **exploratory, read-only survey. No production/schema change. No Ground Truth/benchmark change. No new benchmark target registered.**

Date: 2026-09-27 (Asia/Tokyo)

## 1. Research question

> Without knowing names such as `事務事業別内訳表`, `国庫債務負担行為`, or any specific special-table family in advance, can a cheap text/sequence-based detector identify transitions from ordinary ledger grammar into an unknown representation and back — independently of the coordinate/geometry channel already studied at `075474e` — sufficiently well to trigger richer document understanding?

This survey's actual deliverable, per its own stated goal, is **not** to prove p1327 can be found again — it is to determine whether a semantic-label-free grammar-transition channel adds useful, reproducible information beyond the geometry channel already studied. A negative or mixed result is treated as a valid outcome throughout.

## 2. Frozen state (verified, unchanged)

- Branch `research/case-004-mext-preregistration`; pre-task `HEAD` `075474e`; working tree clean; `main` unchanged at `3b29ebd`.
- Source `mext-fy2024-general-account-expenditure-request-detail`, SHA-256 `6df221dfd22c48e0f32dd59bcf2dbcbaad19720083be43005ce700b984a6bf71` — recomputed, matches.
- case-004 selection protocol (`c2b2c28`), selection record (`fa82c13`), Ground Truth (`f9b2f35`), first frozen benchmark (`49f5ca6`), organization-010 diagnostic (`187a8e9`), organization-020 replication (`aedea1c`), and the structural-anomaly geometry survey (`075474e`) — all re-verified byte-identical to their freeze commits, both before this task began and again immediately before commit. None was modified.
- Known locator, reused unchanged from `075474e`: viewer/1-based PDF page **1327** = `pdfPageIndex` **1326** = printed **文（ス） 1335**. Not assumed to rank first in this survey either.

## 3. Anti-overfitting protocol

No detector feature below references `事務事業別内訳表`, `国庫債務負担行為`, `111`, `16-15`, `スポーツを通じた社会課題解決の推進に必要な経費`, or any other string discovered by manually reading a known page. All feature definitions (§5–§6) were written and frozen (§8) **before** the script was run against the full 1,338-page document, and the known-family lookup (§9) was performed only after that run's global rankings were already computed and logged. No threshold was adjusted after seeing where known pages landed; where a known page performed poorly, that result is reported as-is (§9).

**One post-hoc correction is disclosed rather than hidden**: while investigating the request-scope hypothesis (§12), it became apparent that the prior survey's own description of `pdfPageIndex` 1326's leftmost-column value `111` as an "item code" was imprecise — structurally, by this point in the document, `111` is the **request number** (要求番号) column's own value (this document's request numbers are printed as plain multi-digit integers rather than the circled single digits used earlier in the file, e.g. case-004's own `①`), not an item code. This does not change any finding in `075474e` (which never used this value as a detection feature), but is corrected here for accuracy and is **not** retroactively edited into the frozen `075474e` report, per this repository's historical-preservation discipline.

## 4. Ordinary-ledger grammar definition (defined before evaluating any known page)

Following the task's own instruction to define this from generic conventions rather than Ground Truth, the following line-level token classes were adopted — the same generic shapes already independently validated across four cases' worth of ordinary rows in this repository's own `common.mjs` (item-code, expense-code, and trailing-triple patterns), used here purely as **generic structural definitions**, not as production code and not tied to any MEXT-specific vocabulary:

- **CODE3**: a line beginning with a 3-digit token followed by whitespace (organization/item-code-like).
- **CODE2DASH2**: a line containing an `NN-NN`-shaped digit pair (expense-code-like).
- **LONGCODE**: a line beginning with a long dash-segmented numeric code (subordinate-numbered-line-like, e.g. the `95016-2111-02-0000`-shaped lines already documented in every case so far).
- **TRIPLE**: a line ending in exactly three trailing numeric tokens, the last optionally preceded by the decrease glyph (the standard amount-triple rhythm).
- A line is **code-shaped** if it matches CODE3 or CODE2DASH2 (an ordinary row's own opening shape).
- A line's **numeric-token count** is the number of standalone or comma-grouped integer tokens found anywhere in it (amount-like density).
- A line is **dense-numeric-unmatched** if its numeric-token count is ≥4 but it does **not** end in a clean TRIPLE — the generic, name-free proxy for "many numbers packed into one line that doesn't fit the ordinary row-ending rhythm" (e.g., a row built from several repeated `label N (M)` category pairs, whatever that row's real-world name might be).

The purpose, as instructed, is not to parse the ledger correctly — it is to notice when a local line stops looking like the dominant row rhythm (`code/hierarchy → label → amount triple → optional remarks`).

## 5. Text/grammar signal definitions (frozen before the full run)

Per page, computed purely from `derived/pdf-extraction/mext-fy2024-general-account-expenditure-request-detail.lines.jsonl` (reconstructed text + line order + page index only — **no coordinates used** for these signals, satisfying the task's "pure text/order" preference):

- **A — token-class distribution shift**: `numericRatioVariance`, the per-page variance of (numeric-token-count ÷ word-count) across the page's own lines — high variance means the page mixes very numeric-dense lines with very text-only lines close together.
- **B — standard-row-rhythm break**: `codeShapedRhythmRatio` = (code-shaped lines that also end in a clean TRIPLE) ÷ (all code-shaped lines) — a ratio near 1 means every row-opening line on the page ends the way an ordinary row should; a low ratio means code-shaped openings exist without their expected ending.
- **C — local grammar transition**: `maxDenseNumericUnmatchedRun`, the longest consecutive run of dense-numeric-unmatched lines on the page, plus a boolean `transitionBounded` recording whether that specific run is preceded (anywhere earlier on the page) and followed (anywhere later) by at least one ordinary code-shaped-with-TRIPLE line — distinguishing "a whole page is one unusual table" from "the ledger visibly leaves and returns to its own rhythm within one page."
- **D — repetition/alternate-representation hints**: not implemented as a scored signal in this task (see §13, disclosed as a scope gap, matching the prior geometry survey's own honest disclosure of the same category).
- **E — line-shape/token-count entropy**: `wordCountVariance`, the per-page variance of words-per-line.
- **F — code-continuity break**: not implemented as an independent scored signal; `codeShapedRhythmRatio` (B) partially captures this by construction, but a dedicated "do code values stop advancing in a plausible order" signal was not built, for the same reason category D and category C (of the prior geometry survey) were not built — reliably doing so without semantic value interpretation exceeded this task's time budget. Disclosed as descriptive absence, not a negative result.

These four scored signals (`maxDenseNumericUnmatchedRun`/`transitionBounded`, `denseNumericUnmatchedCount`, `codeShapedRhythmRatio`, `numericRatioVariance`, `wordCountVariance`) were **not** combined into one composite score, per the task's explicit instruction; each is reported and ranked independently.

## 6. Representation/input provenance

| Signal | Input needed |
|---|---|
| All five text/grammar signals above (§5) | Pure text/order only — `lines.jsonl`'s `text`, `lineIndex`, `pdfPageIndex` fields; no coordinates, no page-boundary lookahead beyond the current page. |
| Geometry signals from `075474e` (`maxRowBandWidth`, `distinctXBuckets`, `itemCount`) | Text + coordinates (`items.jsonl`'s `x`/`y`). Used in this task **only** for the comparison in §11, never as hidden input to the new ranking. |
| Docling table-region count (proposed, not run) | Engine-derived table structure. |
| Visual confirmation of any candidate | Rendering. |

The new detector prioritizes the pure-text-only tier, exactly as instructed.

## 7. Detector/feature freeze point

The script implementing §4–§6's definitions (kept in this session's own scratch directory, not committed — see §16) was written and its logic finalized **before** it was ever executed against the full document. It was then run exactly once against all 1,338 pages, producing the global rankings in §8 below, written to a local JSON file and logged to the console **before** any of the seven known pages from `075474e` were looked up. The known-page lookup code was a separate block, appended to the same script, that queries the already-computed, already-sorted rankings — it does not alter any ranking. No threshold, bucket size, or ratio cutoff was changed after this point. This entire freeze-then-evaluate ordering is the literal order of operations actually performed in this task, not a reconstructed narrative.

## 8. Whole-document run results

All 1,338 pages with at least one reconstructed line were processed (one page, likely a boundary/blank artifact, had zero lines and was excluded, consistent with the prior geometry survey's own 1,338-of-1,339 page count).

Selected top-15 excerpts (full detail retained in the script's own JSON output, not committed):

- **Top by `maxDenseNumericUnmatchedRun`**: led by `pdfPageIndex` 182 (run=12), 985 (run=12), 395 (run=11), 898/899 (run=11), 1031 (run=11) — **none bounded** (`transitionBounded=false` for every one of the top 15), an immediate, honest finding discussed in §13.
- **Top by `denseNumericUnmatchedCount`**: led by 770 (22), 846 (22), 899 (22), 989 (22), 1058 (22), 1062 (22), 1064 (22), then 84 (21), 182 (21), 242 (21), 334 (21), 845 (21), ...
- **Top by lowest `codeShapedRhythmRatio`** (among pages with ≥1 code-shaped line): dominated by very early pages (`pdfPageIndex` 4, 8, 13, 14, 15, 17, 18, 19, 20, 22, 23, 26, 27, 28, 29), each with a small handful of code-shaped lines and ratio exactly 0.
- **Top by `numericRatioVariance`**: led by 1144, 536, 1197, 1195, 535, 1199, 534, 1198, 462, 345.
- **Top by `wordCountVariance`**: led by 755, 715, 759, 678, 919, 593, 1127, 998, 776, 620.

## 9. Known-family evaluation (looked up only after the freeze above)

| `pdfPageIndex` | `maxDenseNumericUnmatchedRun` rank | `denseNumericUnmatchedCount` rank | `codeShapedRhythmRatio` rank (lowest-first) | `numericRatioVariance` rank | Any signal in top 5%? (of 1,338 ⇒ top 67) | Any signal in top 10%? (top 134) |
|---|---:|---:|---:|---:|---|---|
| 1326 (known target) | 187 | 412 | 922 | 1064 | No | No |
| 1278 | 1008 | 676 | 1119 | 1270 | No | No |
| 264 | 719 | 450 | **183** | 1025 | No | No |
| 1169 | 974 | 404 | 747 | 1144 | No | No |
| 713 | 847 | 230 | 488 | **1338 (worst)** | No | No |
| 845 | 1249 | **12** | 569 | 1302 | **Yes** (top ~1%) | Yes |
| 84 | **26** | **8** | **52** | 1075 | **Yes** (both, top ~2–4%) | Yes |

**Honest headline result**: the text/grammar channel, as implemented here, **does not reliably surface the known family into a practical top-5%/top-10% review set**. Only 2 of the 7 known pages (84, 845) land in the top 10% on any of the four scored signals; the flagship page 1326 itself never enters even the top 10% on any single text/grammar signal (best rank 187/1338 ≈ top 14%). This is reported without softening, per the task's own instruction.

## 10. Newly discovered candidate inspection (blind to semantic category, then classified)

Following a deterministic rule (top-ranked pages on `maxDenseNumericUnmatchedRun` and `denseNumericUnmatchedCount` and lowest `codeShapedRhythmRatio`, deduplicated against the seven already-known pages), five new candidates were rendered and read:

| `pdfPageIndex` (printed) | Rank basis | What it actually contains | Classification |
|---|---|---|---|
| 182 (191) | `maxRun` #1 | Item `9 / 65-15 / 生涯を通じた学習機会の拡大に必要な経費`'s own subordinate line `003`: another `事務事業別内訳表`-shaped matrix (5 data columns, own `計` row), same family as the known group | Same family as known group — **new instance, found independently** |
| 770 (779) | `denseNumericUnmatchedCount` #1 | A long, deeply-nested per-region travel-allowance itemization (lettered sub-items `a`/`b`/`c`.../`(ア)`/`(イ)`/`(ウ)` repeated per world region), entirely within a remarks-column continuation | **New, related family**: per-region (not per-country) itemization, structurally similar in kind to `075474e`'s `pdfPageIndex` 845 per-country list, but a distinct instance |
| 4 (13) | `codeShapedRhythmRatio` lowest, #1 | An **ordinary** page: a `003 定員合理化に伴う経費` → `001 人件費` staff-reduction breakdown, every line a genuine, ordinary subordinate numbered line, several with a `△` decrease and populated triples | **Ordinary, and a detector false positive** — see §13 for the mechanism |
| 1144 | `numericRatioVariance` #1 | Not rendered in this task (time-budget limitation, disclosed in §15) | Not classified |
| 755 | `wordCountVariance` #1 | Not rendered in this task (time-budget limitation, disclosed in §15) | Not classified |

**A genuinely ordinary candidate was found and is recorded as such** (`pdfPageIndex` 4), unlike the geometry survey's small inspected sample, which happened not to contain one. This is an important, disclosed asymmetry between the two channels' small samples (§11).

## 11. Geometry vs. text/grammar comparison

| Structural family/page | Geometry signal (`075474e`) | Text/grammar signal (this task) | Both? | Interpretation |
|---|---|---|---|---|
| `pdfPageIndex` 1326 (known target) | `maxRowBandWidth` rank 58/1338 (top ~4%) | Best rank 187/1338 (top ~14%) | Geometry only, more sharply | Geometry's coordinate-based column-width proxy tracks this family's wide matrix shape more directly than any pure-text proxy tried here. |
| `pdfPageIndex` 84, 845 | Both were among geometry's top-ranked/inspected pages too | Both land in text/grammar's top 10% (84 strongly, on 3 of 4 signals) | **Both channels agree** | These two pages are the clearest cross-channel confirmations found in this survey. |
| `pdfPageIndex` 264, 1169, 1278, 713 | Geometry ranked these more sharply (`075474e` §8/§9) | Text/grammar ranks these only moderately-to-poorly (§9 table) | Geometry only, in this specific implementation | The geometry channel's coordinate-width proxy generalizes across this family's several instances more consistently than the text-only proxies tried here. |
| `pdfPageIndex` 182 (new) | Not specifically inspected in `075474e` (was not among its own top-ranked list at the time) | `maxDenseNumericUnmatchedRun` #1 | **Text/grammar found it first** | A genuine case of the text channel surfacing a same-family member the geometry channel's own small inspected sample did not happen to include. |
| `pdfPageIndex` 770 (new) | Not specifically inspected in `075474e` | `denseNumericUnmatchedCount` #1 | **Text/grammar found it first** | A second such case, for the related per-region/per-country itemization family. |

**Answers to the task's specific questions:**
- **What does geometry detect that text misses?** A sharper, more consistent ranking of the `事務事業別内訳表`-shaped matrix family across its several known instances (264, 1169, 1278, 713 rank far better under geometry's `maxRowBandWidth` than under any text/grammar signal tried here).
- **What does text detect that geometry misses?** At least two new family members (182, 770) that were not part of the geometry survey's own small inspected sample — not necessarily invisible to geometry in principle, simply not among the handful of pages that survey happened to render.
- **Which candidates are strong in both?** `pdfPageIndex` 84 and 845 are the two clearest agreements between the channels in this survey's actual (small, non-exhaustive) inspected sets.
- **Redundant or complementary?** **Complementary, not redundant** — each channel's own top-ranked list, when actually inspected, surfaced at least one genuine family member the other channel's own (small) inspected list did not include, while also each missing or under-ranking members the other caught better.
- **Does text-only reduce the review set enough to be useful, alone?** **Not clearly, based on this evidence** — the known flagship page (1326) never enters even a top-10% text-only review set on any single implemented signal, which is a materially weaker result than geometry's own top-4% showing for the same page.
- **Does either channel systematically favor a particular family?** Geometry's `maxRowBandWidth` favors the wide-matrix family specifically (its defining feature is literally column width); text/grammar's `denseNumericUnmatchedCount`/`maxDenseNumericUnmatchedRun` favor pages with many repeated numeric sub-items regardless of whether they are arranged as a wide matrix or a tall per-region list — a genuinely different bias, consistent with the two channels measuring different geometric/textual aspects of a related but not identical underlying phenomenon.

## 12. Request-scope hypothesis: observation only, not implemented

**Correction carried over from §3**: `pdfPageIndex` 1326's leftmost-column value `111` is the row's own **request number** (要求番号), not an item code as previously described — this document prints request numbers as plain multi-digit integers at this depth in the file, rather than the circled single digits used near the front (e.g., case-004's own `①`).

With that correction, the source-observable facts are:
- The request-number `111` is printed once, on the same line as the header row whose amount triple is blank and which is immediately followed by the embedded matrix.
- The resumed ordinary-format lines beneath the embedded matrix (`001 スポーツを通じた社会課題の解決`, and the further `15072-...`-coded lines beneath it) all show a **blank** request-number column — no new request number is printed anywhere on the rest of this page.
- The same pattern holds for `pdfPageIndex` 1278 (request number `108`, printed once on the header line whose triple is blank; no new request number printed on any subsequent line on that page).

**This is source-supported evidence, from two instances, consistent with the hypothesis** `request scope continues while representation grammar changes internally` — the request-number column does not reset or repeat across the internal representation change in either instance actually checked. **This evidence is limited to 2 instances out of at least 6 known family members and is not exhaustively verified** across the other 4 (182, 264, 770, 1169 were not individually re-checked for this specific column in this task, a disclosed limitation, §15). No forward-fill or request-scope parsing logic was implemented; this remains an observation for a future, separately-scoped task to test more broadly, exactly as instructed.

## 13. Signals that failed / weak signals

- **`transitionBounded` never fired among the top 15 `maxDenseNumericUnmatchedRun` pages** (all showed `bounded=false`) — meaning the specific "ordinary → block → ordinary, both boundaries on the same page" pattern this signal was designed to detect (category C) was, in this implementation, **too strict to fire on the actual known family**: p1326's own dense-numeric-unmatched run does not reach the length threshold implied by requiring a full ordinary-code-with-triple line both before *and* after it within the same page's own line sequence (its "before" context is a blank-triple header line, which does not itself qualify as "ordinary code-with-triple"). This is a genuine implementation gap, disclosed rather than patched: the concept (category C) is sound, but this specific operationalization under-detects the very phenomenon it was built for.
- **`codeShapedRhythmRatio`'s low-value tail is dominated by a detector artifact, not genuine anomalies**: inspecting `pdfPageIndex` 4 (§10) revealed that the `CODE2DASH2` regex (`\d{2}-\d{2}`, unanchored) incidentally matches substrings *within* ordinary long dash-segmented codes (e.g., `95016-2111-02-0000` contains the accidental substring `16-21`), misclassifying entirely ordinary subordinate-numbered lines as "code-shaped," then counting them against the rhythm ratio when they don't (by construction) end in a clean top-level TRIPLE. **This is a disclosed weakness of this specific regex definition, not a negative finding about category B/F in general** — a more carefully anchored code-token definition would likely behave differently, but per the anti-overfitting protocol this was not corrected and re-run after discovering it from an inspected page; it is reported as a limitation instead.
- **`numericRatioVariance` did not track the known family at all** — every known page's rank on this signal is in the worst third of the document (§9), and `pdfPageIndex` 713 is literally the single worst-ranked page in the entire document on this metric, the opposite of what the signal's own design intent (flagging mixed numeric/text density) would suggest for a page that is *entirely* a dense numeric table. This is recorded as a clear, unambiguous failure of this specific signal for this specific family — a page that is uniformly dense in one direction produces *low* internal variance, not high, which in hindsight is the correct mechanical behavior of a variance-based measure, just not the behavior initially hoped for.
- **Category D (repetition/alternate-representation hints) and a dedicated category F (code-continuity break) were not implemented at all** (§5) — this survey cannot report on their usefulness, only that they were not attempted within scope, mirroring the same disclosed gap in the prior geometry survey.

## 14. Architecture implications (conceptual only, no implementation)

Extending the flow proposed in this task:

```text
Raw PDF
  ↓
cheap text/sequence features         (this task: pure-text-only, no coordinates)
  ├───────────────┐
  ↓               ↓
text/grammar      geometry/layout
anomaly channel   anomaly channel    (075474e: coordinate-derived)
  └───────┬───────┘
          ↓
structural anomaly candidate         (§11: complementary, not redundant, in this survey's evidence)
          ↓
context selection
          ↓
richer document understanding
          ↓
representation-role classification
          ↓
semantic interpretation
```

- **Where does anomaly-candidate generation belong?** Given both channels are complementary rather than redundant (§11), and both are cheap relative to full document understanding, candidate generation plausibly belongs as an **early substage within document/layout-family interpretation** (ADR-010), computed from whatever raw/derived artifacts an engine already produces, rather than as a wholly separate pre-interpretation layer — it needs to run before semantic interpretation, but after at least minimal text/coordinate reconstruction already exists.
- **Source-safe vs. engine-derived, revisited**: the text/grammar signals in this task are marginally *more* source-safe in principle than the geometry signals (they depend only on reconstructed text and line order, which a human reading the PDF could reproduce without any engine's coordinate system) — but both remain, in the strict Case Package sense already established by ADR-011, **engine-derived** here, because both were actually discovered via one specific engine's (pdf.js's) own text/line reconstruction, not independently confirmed as directly source-observable before that.
- **Should the Case Package record observations, not semantic anomaly labels?** This survey's own practice (§10's classification table, kept separate from §5–§9's mechanical signal computation) supports yes: the mechanical signal value and rank are observations; "same family as p1326" or "ordinary" are downstream labels applied only after visual inspection, and conflating the two risks contaminating future candidate generation with today's specific known examples.
- **Should Strategy Selection trigger richer parsing from anomaly signals?** Conceptually plausible, not tested: a per-page anomaly-candidate flag (from either or both channels) is exactly the kind of cheap, pre-semantic input a future strategy selector could use to decide "ordinary single-row parser" vs. "expand context / richer layout handling," independent of whether any Ground Truth exists for that page.
- **`unknown` as a valid representation role**: preserved throughout this survey (§10's classification scheme reserves it, though no candidate in this task's small inspected set actually required it — every new candidate fit either "known family" or "ordinary").

No schema or ADR change is implemented from this section.

## 15. MOF CSV implications

Consistent with, and extending, `075474e`'s own framing:

- The newly found per-region itemization family (`pdfPageIndex` 770) and the confirmed-recurring project/committee-matrix family (now including `pdfPageIndex` 182) both reinforce that a future canonical-hierarchy-to-MOF-CSV mapping would need to recognize **more than one** non-ordinary representation shape, not design around a single "special table" concept.
- The request-scope observation (§12) is directly relevant here: if a future mapping effort uses the request-number column as a grouping key for canonical hierarchy assignment, it should be aware that — in the two instances checked — a representation change (embedded matrix) does **not** reset or duplicate the request number, meaning naive "does this row have its own request number" logic would correctly treat the resumed ordinary rows as still belonging to the same request, but naive "does this row look like an ordinary row" logic could still misattribute or drop the embedded matrix's own rows entirely, since they carry no request number, code, or ordinary triple of their own to anchor them.
- No page in this task is classified as `繰入`, `移替`, or any other MOF-specific concept — none was tested against that question, and no evidence gathered here supports or refutes such a classification for any of the pages surveyed.

## 16. Files / production-code status

- `reports/document-understanding/20260927_0637_MEXT_Text_Grammar_Transition_Anomaly_Survey.md` (this file, new).
- `state/CURRENT_STATE.json`, `state/TODO.md`, `state/CHANGELOG.md` (state updates).

**No research script was committed.** The frozen feature-computation script (§7) remained in this session's own scratch directory throughout, exactly as the prior geometry survey's own script did, per the task's own allowance ("a research-only script is allowed if useful, but ... document its status") interpreted conservatively: since it was not committed, no separate test suite was required. No extraction, normalization, adapter, evaluator, selection-protocol, selection-record, Ground Truth, Case Package, or Document Profile file was modified. No rendered image was staged (scratch directory only, removed after use). `npm run docbench` was not run, since no accidental semantic drift was suspected or found.

## 17. Validation

```bash
npm run validate      # PASS
git diff --check      # clean
```

Source SHA-256 re-verified unchanged; case-004 Ground Truth, selection protocol/record, first frozen benchmark, both context diagnostics, and the `075474e` geometry survey all re-verified byte-identical to their respective freeze commits; no benchmark/extraction/normalization/evaluator file touched; no rendered images left in the repository.

## 18. Limitations

- Only 3 of the 5 new top-ranked candidates identified in §10 were actually rendered and visually classified (`pdfPageIndex` 182, 770, 4); `pdfPageIndex` 1144 and 755 (the top-ranked pages by `numericRatioVariance` and `wordCountVariance` respectively) were not inspected in this task, a time-budget limitation, not a claim about what they contain.
- The request-scope observation (§12) rests on only 2 of the ≥6 known family instances; it was not checked for `pdfPageIndex` 182, 264, 770, or 1169.
- The `CODE2DASH2` regex flaw discovered in §13 means every ranking that depends on "code-shaped line" classification (`codeShapedRhythmRatio`, and by extension the request-scope check's own reliance on distinguishing code-shaped from non-code-shaped lines) is known to be **noisier** than intended for pages containing long dash-segmented subordinate codes — a real limitation of this specific frozen implementation, not corrected in this task per the anti-overfitting protocol.
- Category D and F signals were not implemented (§5, §13) — this survey cannot report on their usefulness at all, only on the fact that they were not attempted.
- No systematic sweep of bucket sizes, thresholds, or the `≥4 numeric tokens` cutoff used for "dense-numeric-unmatched" was performed; a different cutoff could plausibly change rankings, and this was not explored (consistent with the freeze-before-evaluate discipline, but a real unexplored parameter space nonetheless).

## 19. Open questions

- Would fixing the `CODE2DASH2` regex flaw (§13) materially change `codeShapedRhythmRatio`'s ranking of the known family, or was `pdfPageIndex` 84's own strong showing on that signal (rank 52/1338) already robust to the flaw? Not determined here.
- Does the request-scope-continues-during-representation-change pattern (§12) hold for the other known family members not yet checked, or for the newly found `pdfPageIndex` 182/770?
- Would a properly operationalized `transitionBounded` (§13) — one that accepts a blank-triple header line, not only a fully ordinary triple-bearing line, as a valid "before" boundary — correctly bound the known family's own dense-numeric-unmatched runs? This is a plausible, low-risk refinement to test, not implemented here.

## 20. Recommended next experiment

A single, focused follow-up: **redefine `transitionBounded`'s "before" condition to also accept a code-shaped line with a blank (not necessarily populated) amount triple** — since this is exactly the shape the known family's own header rows take (§4.2, §12) — and re-run the same frozen §5 signals to see whether this one, narrowly-scoped fix changes how many of the seven known family members land in a practical top-10% review set, without touching the geometry channel, without new Ground Truth, and without registering any page as a benchmark target.

Not executed in this task.

---

## Answers required by the originating task

1. **Git**: branch `research/case-004-mext-preregistration`; pre-task HEAD `075474e`; final commit recorded below; pushed; `main` unchanged.
2. **Frozen-artifact integrity**: source SHA, case-004 selection/GT/first-run benchmark, both context diagnostics, and the geometry survey all re-verified byte-identical before and after this task.
3. **Text/grammar features tested**: `maxDenseNumericUnmatchedRun`/`transitionBounded` (C), `denseNumericUnmatchedCount`, `codeShapedRhythmRatio` (B/F), `numericRatioVariance` (A), `wordCountVariance` (E) — categories D and a dedicated F were not implemented.
4. **What was frozen before evaluating known pages**: all five feature definitions, the classification regexes, and the ranking method (§4–§7) — computed and logged across all 1,338 pages before the known-page lookup code was ever run.
5. **Was p1327/`pdfPageIndex` 1326 candidated without semantic labels?** Partially — it appears in the top ~14% on its best single signal, but never in a top-10% review set on any of the four scored text/grammar signals (§9) — a materially weaker showing than the geometry channel's own top-~4%.
6. **Known-family ranks/percentiles**: see the table in §9; only `pdfPageIndex` 84 and 845 reach the top 10% on any text/grammar signal.
7. **Newly discovered candidates and classifications**: `pdfPageIndex` 182 (same known matrix family, new instance), 770 (new, related per-region itemization family), 4 (genuinely ordinary — a disclosed detector false positive); 1144 and 755 not inspected (limitation).
8. **Confirmed ordinary candidates**: yes, `pdfPageIndex` 4 (§10, §13).
9. **Signals that worked vs. failed**: `denseNumericUnmatchedCount` and (for a subset of the family) `codeShapedRhythmRatio` worked best; `maxDenseNumericUnmatchedRun`'s `transitionBounded` sub-signal never fired on the known family (too strict); `numericRatioVariance` was actively misleading for this family; `codeShapedRhythmRatio`'s low tail is contaminated by a regex-matching artifact (§13).
10. **Text-only vs. coordinate/geometry requirements**: all five new signals are pure text/order only; geometry signals (reused from `075474e` for comparison only) require coordinates; true table-region detection would require an engine's own structural output (Docling) or vector-drawing data, neither used in this task.
11. **Geometry-vs-text overlap and complementarity**: complementary, not redundant (§11) — each channel's small inspected sample caught at least one genuine family member the other's inspected sample did not include, while geometry ranked the dominant matrix family more sharply overall.
12. **Request-scope observations**: source-supported for 2 of ≥6 known instances (`pdfPageIndex` 1326, 1278) — the request-number column does not reset across the internal representation change in either checked instance; not exhaustively verified across the rest of the family (§12).
13. **Architecture implications**: anomaly-candidate generation plausibly belongs as an early substage within document/layout-family interpretation; both channels' signals remain engine-derived, not source-safe, in the strict Case Package sense; observations should be recorded separately from semantic labels (§14).
14. **MOF CSV implications**: reinforces the need to recognize multiple non-ordinary representation shapes, and flags a request-number-based grouping strategy's own blind spot for rows (like the embedded matrix's own internal rows) that carry no request number, code, or ordinary triple at all (§15).
15. **Files changed**: this report plus `state/{CURRENT_STATE.json,TODO.md,CHANGELOG.md}`; no research script committed; no production file modified.
16. **Validation**: `npm run validate` and `git diff --check` both pass (§17).
17. **Limitations**: disclosed in §18, including the `CODE2DASH2` regex flaw, the un-inspected top candidates, and the narrow request-scope evidence base.
18. **Recommended next experiment**: redefine `transitionBounded`'s "before" condition to accept a blank-triple code-shaped header line, and re-run the same frozen signals to see whether more of the known family lands in a practical review set (§20). Not executed in this task.

**Overall answer to the survey's own stated goal**: the text/grammar channel, as implemented here, is a **genuine, complementary addition** to the geometry channel — it independently surfaced at least two new family members the geometry survey's own small sample missed — but it is **not, on its own, a stronger or sufficient replacement** for the geometry channel for this specific document's dominant anomaly family, and one of its four signals actively misled for the family's most extreme instance (`pdfPageIndex` 713). Both channels together, not either alone, currently constitute the best-supported basis for future anomaly-candidate generation on this source.
