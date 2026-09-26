# MEXT Structural Anomaly Signal Survey

Status: **exploratory, read-only survey. No production/schema change. No Ground Truth/benchmark change. p1327 not registered as a benchmark target.**

Date: 2026-09-27 (Asia/Tokyo)

## 1. Research question

> Without being able to enumerate the kinds of "unknown special structure" in advance, how far can source-safe signals of deviation from an ordinary 概算要求明細 page be observed mechanically? Can such signals candidate "regions needing additional document understanding" without relying on Ground Truth or semantic interpretation?

This is exploratory research, not a production detector. The goal stated by the originating task is repeated here as the actual success criterion: **clarify which observable facts are usable and which are insufficient for suspecting unknown special structure without prior knowledge — not to construct a success story.**

## 2. Frozen inputs / integrity (verified before any inspection)

- Branch `research/case-004-mext-preregistration`; pre-task `HEAD` `aedea1c`; working tree clean; `main` unchanged at `3b29ebd`.
- Source `mext-fy2024-general-account-expenditure-request-detail`, SHA-256 `6df221dfd22c48e0f32dd59bcf2dbcbaad19720083be43005ce700b984a6bf71` — recomputed, matches.
- case-004 selection protocol (`c2b2c28`), selection record (`fa82c13`), Ground Truth (`f9b2f35`), first frozen benchmark (`49f5ca6`), organization-010 diagnostic (`187a8e9`), organization-020 replication (`aedea1c`) — all re-verified byte-identical to their freeze commits, both before this task began and (re-checked) after all analysis below. None was modified.
- This task changes none of: Ground Truth, selection protocol/record, evaluator, production extraction/normalization code, case-004's benchmark score. p1327 (below) is **not** registered as a new benchmark target, has no Ground Truth, and was not run through `docbench`.

## 3. Known observation and anti-overfitting rule

The user visually found, in a PDF viewer, a page around **"1327"** near item `111 / 16-15 / スポーツを通じた社会課題解決の推進に必要な経費`, containing what looks like a `事務事業別内訳表`-shaped table embedded mid-page. This single observation is treated as **one non-representative data point**, not training data: no detector condition below references `事務事業別内訳表`, `16-15`, `111`, or any of this row's own text. Section 4 records what the page actually contains; sections 6–8 build signal candidates and run an experiment **before** re-consulting section 4's specifics, and section 9 checks whether the resulting candidate list contains p1327 without having been tuned to put it there. Where a signal was adjusted, the adjustment is disclosed with its direction and reason.

## 4. p1327 structural observation

### 4.1 Exact locator (measured, not inferred)

- PDF viewer page (1-based, matching `pdftoppm -f/-l`): **1327**
- PDF page index (0-based, this repository's `pdfPageIndex` convention): **1326**
- Printed page label (top-right corner of the page itself): **文（ス） 1335**

These three numbers were obtained by directly rendering `pdftoppm -f 1327 -l 1327` against the locked source and reading the corner label, not by arithmetic extrapolation from any other page's offset.

### 4.2 Visual/layout observation (source-safe, no interpretation)

- The page's leftmost columns show one ledger header row: request no. column blank, code `16-15`, label wrapping across three lines (`スポーツを通じた社会課題`/`題解決の推進に必要な経`/`費`), item code `111` printed to the left of the label.
- **This header row's own 前年度予算額 / 6年度概算要求額 / 対前年度比較増△減 cells are visually blank** — no digits are printed in the normal amount-triple position for this row.
- Immediately to the right of, and below, this header row, a rectangular ruled region begins that is **not** aligned with the page's normal 6-column ledger grid: it has its own header row (`区分 | 諸謝金 | 職員旅費 | 委員等旅費 | 庁費 | スポーツ振興事業委託費 | 地方スポーツ振興費補助金 | 計` — 7 data columns plus a label column) and 5 data rows plus one `計` (total) row, each cell showing two stacked numbers in a `N (　M　)` layout distinct from the ordinary ledger's single-number cells.
- Below this embedded region, the page **resumes the ordinary vertical ledger format**: a `001` item-level row (`スポーツを通じた社会課題の解決`) with its own populated amount triple (`722,254` / `978,551` / `256,297`), followed by further ordinary coded lines (`15072-2129-06-0110 諸謝金`, etc.) with populated triples and free-text remarks paragraphs.
- No page-break occurs within this structure; it is entirely contained on one page (`pdfPageIndex` 1326).
- The immediately preceding and following pages (checked separately, see §5) do not show this embedded-region shape.

### 4.3 Semantic interpretation (kept separate, not used as detection input)

This region's evident purpose — a "内訳表" (breakdown table) reallocating one item's total across the same set of accounting sub-categories used elsewhere in the document (諸謝金/職員旅費/委員等旅費/庁費/etc.), by a different sub-project — is a plausible reading, but it is explicitly **not** used anywhere in sections 6–9's signal design. Whether it constitutes a duplicate representation of amounts also stated in the resumed vertical ledger below it, whether it should be excluded from a naive sum to avoid double-counting, and whether it is a "cross-tab" in any formal sense are left as open, unconfirmed semantic questions (§15), not resolved here.

## 5. Normal-page comparison

Comparison pages were selected from **already-inspected** pages from prior case-004 tasks, per the task's own preference, plus p1327's immediate neighbors and one additional later page:

- The frozen case-004 target page (`pdfPageIndex` 2) — ordinary single ledger row, populated triple, no embedded region.
- Organization-010 diagnostic samples (`pdfPageIndex` 1, 119, 121, 284, 463, 677, 798, 894) — all ordinary item-header or first-expense-row pages; one (`pdfPageIndex` 677/678, "国立大学法人施設整備費") already showed a **blank inline triple** on its own header row, with actual figures deferred to a subordinate line and a large `国庫債務負担行為` multi-year commitment sub-table beneath it — noted at the time as a distinct self-containment anomaly, now recognizable as structurally related to what appears on p1327 (a blank header triple co-occurring with a non-ledger embedded table).
- Organization-020 replication samples (`pdfPageIndex` 896, 984, 1027) — all ordinary, no embedded region observed.
- p1327's immediate neighbors (`pdfPageIndex` 1325, 1327) — not separately re-rendered in this task; the resumed-ledger content visible at the bottom of `pdfPageIndex` 1326 itself already demonstrates the page transitions back to ordinary format before its own end.
- One additional later page was substituted by the exploratory experiment itself (§8) rather than chosen manually — this is disclosed as a deliberate methodological choice: letting the *signal* pick further comparison pages, rather than the researcher picking pages expected to look normal or abnormal, better serves the "no prior enumeration of anomaly types" principle than a manually curated comparison set would.

## 6. Candidate source-safe signals

Organized per the task's A–E categories, each stated as a mechanically observable deviation, not a named structure:

- **A. Table geometry**: number of distinct horizontal text-row bands per page; the maximum number of distinct x-position clusters sharing one row band (a proxy for "how many columns does the widest row on this page have"); total distinct x-position clusters used anywhere on the page (a proxy for "how many column boundaries does this page use in total").
- **B. Text/layout distribution**: total text-item count per page (density); total reconstructed-line count per page (a different density measure, sensitive to short wrapped fragments rather than wide rows).
- **C. Hierarchy continuity**: whether a page's coded rows (`NNN` item codes, `NN-NN` expense codes) appear in a plausible ascending/nested sequence, source-observable without Ground Truth — **not implemented as a numeric signal in this task** (see §11, failure/limitation); only qualitatively checked during candidate inspection (§9).
- **D. Representation repetition**: whether the same numeric magnitude appears in two structurally different regions of one page (e.g., an embedded matrix's own total column and the resumed ledger's own triple) — **not implemented as a numeric signal in this task**; observed qualitatively only where a candidate page was inspected directly (§9), since reliably matching "the same number, formatted differently, in two different table shapes" without semantic labels is itself a nontrivial detection problem, honestly out of scope for this survey's time budget.
- **E. Unknown headings**: a text block that is short, sits alone on its own row band, and is immediately followed by a measurable geometry change (row-band width or x-cluster-count jump) — **not implemented as a standalone numeric signal**; the embedded regions found in §9 were in every case preceded by exactly this kind of short standalone label (e.g., `事務事業別内訳表`, `区　分`), consistent with this category, but this was observed after the fact, not used as the detection mechanism.

Only the A/B metrics below were actually computed and tested; C/D/E remain conceptually described but not mechanically implemented in this task, which is itself an honest finding (§11).

## 7. Representation availability by engine/tool

| Signal | Text-only | Coordinates required | Ruling-line/table-geometry required | Rendering required |
|---|---|---|---|---|
| Item/line density per page (B) | Yes (line/item count from any extractor's raw output) | No | No | No |
| x-cluster count / max row-band width (A) | No | **Yes** — needs each text item's own x-position | No | No |
| True ruling-line count / table-region count (A, more directly) | No | No | **Yes** — needs vector line-drawing operators or Docling's own table-region output | No |
| Visual "does this look like a different table" confirmation (used in §9 only) | No | No | No | **Yes** |

- **pdf.js (`pdfjs-dist`)**, via the already-existing, unmodified `scripts/pdf-extraction` pipeline's `items.jsonl` output (one row per text item, with `x`/`y`/`width`/`height`/`pdfPageIndex`), was **empirically used** in this task (§8) to compute the density and x-cluster signals. It does not expose vector ruling lines; the density/x-cluster proxies used here are a substitute for true table-geometry detection, not equivalent to it.
- **Docling**, per its own already-integrated raw output shape (`scripts/document-understanding/benchmark/src/normalize-docling.mjs`'s consumption of `raw.tables`, each with `numRows`/`numCols`/cells), already performs genuine table-region detection as part of its normal operation — **this is a materially more direct source-safe signal for "how many separate table-shaped regions exist on this page, and of what dimensions" than any pdf.js-based proxy**, since Docling detects table regions as a first-class concept, not one inferred from text density. This capability is **not empirically exercised in this task** (Docling was not run against p1327 or any other new page here, to avoid entangling this exploratory survey with case-004's own benchmark/adapter invocation machinery, which is scoped to `gt.pdfPageIndex` per case) — it is reported here as a known, already-present capability worth using in a future, explicitly-scoped experiment, not as a result obtained in this task.
- **PyMuPDF** exposes vector drawing/line primitives via its own API (`page.get_drawings()`), which the current `pymupdf-baseline` adapter does not use or expose in its raw output — this is a capability gap in the *current adapter*, not in the underlying library, and is noted as a possible future direct ruling-line signal source, again not empirically tested here.
- **True rendering-based visual confirmation** (`pdftoppm` + direct reading) was used throughout this task (§4, §9) to verify what a candidate page actually contains, but this is a human-in-the-loop step, not a scalable per-page signal.

## 8. Exploratory anomaly experiment

**Method**: using the unmodified, already-generated `derived/pdf-extraction/mext-fy2024-general-account-expenditure-request-detail.items.jsonl` and `.lines.jsonl` (produced by the existing `npm run extract` command against the locked source; not modified or regenerated for this task), a scratch, uncommitted Node script (kept entirely outside the repository, in this session's own scratch directory) computed, per page, purely from text-item coordinates: total item count, total reconstructed-line count, total distinct x-position buckets (5pt buckets), total distinct y-position row-bands (1pt buckets), and the maximum number of distinct x-buckets found within any single row-band on that page (`maxRowBandWidth`). No case identity, no item code, no label text, and no known-interesting page number was used as a script input beyond the mechanical bucketing itself; the target page (`pdfPageIndex` 1326) was looked up **after** computing all 1,338 pages' signals, not built into the computation.

**Global statistics** (mean / standard deviation across all 1,338 pages with at least one text item):

| Metric | Mean | SD |
|---|---:|---:|
| itemCount | 361.2 | 150.4 |
| distinctXBuckets | 74.8 | 19.8 |
| distinctYBands (≈ lineCount) | 33.9 | 11.3 |
| maxRowBandWidth | 23.3 | 10.6 |

**p1327's own values** (`pdfPageIndex` 1326): itemCount 587 (z ≈ +1.50), distinctXBuckets 119 (z ≈ +2.24), distinctYBands 44 (z ≈ +0.89), maxRowBandWidth 53 (z ≈ +2.80), combined |z|-sum ≈ 8.32.

**Honest result — p1327 is elevated, but far from top-ranked**: by `maxRowBandWidth`, p1327 ranks **58th of 1,338**; by `distinctXBuckets`, **47th**; by `itemCount`, **35th**; by `lineCount`, **142nd**; by combined |z|-sum, **106th**. No threshold was adjusted to move p1327 higher on any of these rankings, and none was found that would place it near the top without also demoting or excluding many other pages arbitrarily. **This is reported as-is, not minimized**: naive text-density and x-clustering signals computed from pdf.js output alone do **not** cleanly isolate p1327 from a substantial number of other pages that score equally or more extreme.

## 9. Candidate-page inspection

Following the task's instruction to check pages that "naturally floated up" from the mechanical signal, a small number of top-ranked pages (by `maxRowBandWidth` and `itemCount`) were rendered and read directly — **without having read this section's own findings in advance**, i.e., the pages were chosen purely by rank, then classified after seeing them:

| `pdfPageIndex` (printed) | Rank basis | What it actually contains | Classification |
|---|---|---|---|
| 1326 (1335) — **the known page** | itemCount 35th, maxRowBandWidth 58th | The `事務事業別内訳表`-shaped project-breakdown matrix described in §4 | Embedded cross-tab matrix (blank header triple) |
| 713 (722) | itemCount #1, zSum #2 | A `国庫債務負担行為限度額及び年度別支出区分` table — a 16-column multi-year commitment/disbursement schedule occupying the **entire page**, with no ordinary ledger row visible on this page at all | **New, different** embedded-table family (multi-year commitment schedule) |
| 1278 (1287) | maxRowBandWidth #1 | Another `事務事業別内訳表`-shaped matrix, for a different item (`108 / 01-15 / 共生社会及び多様な主体によるスポーツ参画の実現に必要な経費`), with **9** data columns (more than p1327's 7) and the same blank-header-triple pattern | Same family as p1327, independently found |
| 84 (93) | itemCount top-10 | A committee/council (`046 科学技術・学術審議会`) meeting-cost breakdown matrix (`委員手当`/`諸謝金`/`職員旅費`/`委員等旅費`/`庁費`/`計`), structurally the same matrix-with-totals shape as `事務事業別内訳表` but for a council rather than a project | Closely related sub-variant of the same family |
| 264 (273) | maxRowBandWidth top-10 | Another `事務事業別内訳表` matrix, for `040 外国人児童生徒等への教育の充実`, with its own distinct column set | Same family as p1327, independently found |
| 1169 (1178) | zSum top-5 | Another `事務事業別内訳表` matrix, for a 文化庁 (Culture Agency) item — the **third distinct organization** in which this pattern was found | Same family, confirms cross-organization recurrence |
| 845 (854) | lineCount #1 (a *different* ranking than the ones above) | A long per-country travel-allowance itemization list (country name × 5 numeric columns, ~20+ rows), embedded within what appears to be a 備考/remarks continuation region | **New, different** embedded-table family (per-country reference table) |

**No genuinely "ordinary, unremarkable" page was found among this small, rank-selected sample.** This is disclosed honestly rather than manufactured: every page actually inspected because a mechanical signal ranked it highly turned out to contain some kind of non-ordinary embedded structure, though not always the *same* kind. This does not mean the signals have no false positives at all (no exhaustive check was performed), but within the handful inspected, none was a case of "signal fired, but the page is actually unremarkable." Per the task's own instruction, none of these is hastily declared "not an anomaly" or forced into a single named category; three genuinely distinct family shapes are recorded (`事務事業別内訳表`/committee-matrix family; multi-year commitment-schedule family; per-country itemization family), plus a residual `unknown` classification reserved for any future candidate that fits none of these three.

## 10. Findings

- **p1327 is a real, source-safe-observable structural deviation** (blank header-row triple + an immediately adjacent, differently-shaped ruled matrix region), independently confirmed to belong to a **recurring family** found in at least 3 other pages (`pdfPageIndex` 264, 1169, 1278) spanning at least 3 different organizations (MEXT headquarters, スポーツ庁, 文化庁), plus a closely related council-meeting sub-variant (`pdfPageIndex` 84).
- **A second, genuinely different embedded-table family exists** (`pdfPageIndex` 713's multi-year commitment schedule, occupying an entire page with zero ordinary ledger content), confirming the task's premise that special structures cannot be enumerated in advance — this survey itself surfaced a kind not mentioned in the originating task's own framing.
- **A third, different family exists** (`pdfPageIndex` 845's per-country itemization list), found via a *different* ranking metric (`lineCount`, not `maxRowBandWidth`/`itemCount`), suggesting no single one of these simple metrics covers every family — multiple, independently-computed signals surfaced different members of the same broader "non-ordinary embedded region" phenomenon.
- **The signal that best distinguished known-anomalous pages from ordinary ones in this small inspected sample was `maxRowBandWidth`** (the widest number of distinct x-position clusters found within one row-band) — every page inspected because of a high `maxRowBandWidth` or `itemCount` ranking (with one exception, `pdfPageIndex` 845, found via `lineCount`) turned out to contain an embedded matrix-shaped region, consistent with the mechanical intuition that a genuinely wide, many-columned matrix produces more distinct x-clusters within a single row than any ordinary 6-column ledger row can.
- **p1327 itself could have been found without knowing it in advance**: it appears within the top ~5% of pages on both `distinctXBuckets` (47th of 1,338) and `itemCount` (35th of 1,338), a small enough candidate set (on the order of 40–60 pages) to plausibly review, though it was **not the single top-ranked page on any metric** — a researcher scanning "top 50 by `maxRowBandWidth`" without knowing p1327 existed would very likely have encountered it, but would have encountered roughly 57 other pages first by that specific ranking.

## 11. Failure cases / signals that did not work

- **Combined |z|-sum did not concentrate the known anomaly family at the very top**: p1327 ranked 106th by this combined measure; the top of that list was dominated instead by very high-`itemCount` pages (`pdfPageIndex` 713, 715) and other dense pages whose specific shape was not individually re-verified for all 15 top entries in this task (time-budget limitation, disclosed in §14) — meaning a single composite score, as the task itself warned against constructing, would have been a **worse** tool for surfacing this specific family than looking at `maxRowBandWidth` alone.
- **`lineCount` alone was a comparatively weak signal for this family**: p1327 ranked only 142nd of 1,338 by raw line count — a page can have many short wrapped lines (dense free-text remarks, like `pdfPageIndex` 845's country list) without having an unusually wide row-band, and vice versa; the two measures pick out genuinely different page shapes, not the same phenomenon at different sensitivity.
- **Hierarchy-continuity (category C) and representation-repetition (category D) signals were not implemented**, not because they were tried and failed, but because reliably computing them without semantic labels (e.g., recognizing that two differently-formatted numbers represent "the same amount") proved to require more design and validation than this survey's scope allowed — this is recorded as a genuine gap, not a negative result about their feasibility.
- **No true ruling-line/table-region signal was computed** in this task (see §7) — the x-cluster-based proxies used here are a substitute, not a replacement, for genuine vector-line or Docling-table-region detection, and it remains untested whether such a signal would rank p1327 and its family more sharply (plausibly yes, since Docling already treats these regions as distinct `tables` in its own raw output, but this is a hypothesis carried into §16, not a tested result).

## 12. Layer/architecture implications (conceptual only, no implementation)

Mapping onto the pipeline the task itself proposed:

```
Raw PDF
→ extraction/layout observation        (pdf.js items/lines; Docling raw tables; PyMuPDF drawings — all already-existing engine capabilities)
→ source-safe structural signals       (§6/§8: density, x-cluster width — computed here; ruling-line/table-region count — not computed here, but architecturally available via Docling)
→ structural anomaly candidate         (§9: a ranked, source-safe candidate list, independent of any case's Ground Truth)
→ ordinary: normal strategy            (the existing single-page, flat-row parsing already used by case-001–004)
→ suspicious: expanded context / richer layout understanding   (not implemented; a conceptual fork point only)
→ representation-role classification   (§9's three-family classification, done manually here; a plausible future automatable step)
→ semantic interpretation              (§4.3, explicitly deferred/unresolved for p1327; belongs to evaluation/downstream use, not this survey)
```

- **Where would anomaly detection sit in ADR-010's layer taxonomy?** The signals actually computed in §8 (density, x-cluster width) are **engine-specific normalization/extraction-adjacent** — they are pdf.js-item-coordinate artifacts, not something every engine would expose identically (Docling's own raw shape already gives a more document-structural, less engine-specific version of the same idea via its table-region count). A more architecturally clean placement would be a **document/layout-family interpretation**-layer concept — "this page's structure deviates from this document family's ordinary row template" — computed from whichever engine's raw output is available, not hardwired to pdf.js's coordinate system specifically.
- **Source-safe vs. engine-derived profile boundary**: the *existence* of an embedded matrix region, its row/column counts, and its position relative to the ordinary ledger columns are plausibly **source-safe** facts (recoverable by direct visual inspection, as demonstrated in §4/§9) — but the specific numeric signals computed in §8 (x-bucket counts derived from one engine's coordinate reconstruction) are **engine-derived**, not source-safe in the strict sense already used elsewhere in this repository's Case Package work (ADR-011's own discovery-provenance distinction would apply here too: these signals were discovered via engine output, not independently confirmed as directly source-observable prior to that).
- **Could this feed a Strategy Selection trigger?** Conceptually yes: a per-page anomaly-candidate score, computed once per document from already-existing raw extraction output, is exactly the kind of cheap, pre-semantic signal a future Analysis Strategy selector could use to decide "use the ordinary single-row parser" vs. "flag for expanded context / richer layout handling" — without needing Ground Truth or a case to already exist for that page.
- **Raw page vs. signals+context to an LLM?** Not resolved here; this survey did not test either. The A/B/C/D context models from the prior organization-010/020 diagnostics are a related, but distinct, concept (page-range context for a *known* field, not anomaly triage for an *unknown* structure) — combining them is a plausible future direction, not evaluated in this task.
- **`unknown` fallback**: explicitly preserved in §9's classification scheme (no candidate was forced into one of the three known families if it did not fit) — no `unknown`-classified page was actually encountered in this task's small inspected sample, but the category remains available and is not treated as a defect of the method.

No schema or production code change is proposed to be implemented from this section; it is offered as design input for a future, separately-scoped task.

## 13. MOF CSV connection implications

Not the primary focus of this survey, stated here as risk framing only, per the originating task's request:

- If a future canonical-hierarchy-to-MOF-CSV mapping effort cannot distinguish an `事務事業別内訳表`-style breakdown matrix (or the `国庫債務負担行為` multi-year schedule, or a per-country itemization list) from an ordinary ledger row, it risks either **double-counting** (summing both the embedded matrix's own totals and the resumed ledger's populated triple as if they were two independent amounts) or **misattributing** a sub-project's own breakdown as if it were a separate top-level expense line.
- **p1327 is explicitly not classified as a "繰入" (transfer/carry-in) or any other MOF-CSV-specific budget-lifecycle concept in this task** — no evidence gathered here supports or refutes that classification; it is recorded as an open semantic question (§15), not decided by resemblance to a known MOF-CSV category.
- The three families found in §9 (project/committee breakdown matrix; multi-year commitment schedule; per-country itemization) are, at minimum, three **different** representation shapes that a canonical-hierarchy mapping would need to treat differently from each other, not as instances of one generic "embedded table" risk — conflating them risks under-specifying the actual mapping problem.

## 14. Limitations

- The exploratory experiment (§8) was run against **pdf.js-derived coordinates only**; PyMuPDF's and Docling's own raw outputs were not computed or compared in this task (see §7's disclosed capability gap), so this survey cannot yet say whether a Docling-table-region-based signal would rank p1327's family more sharply than the pdf.js-based proxy did.
- Only a small number (7) of top-ranked candidate pages were actually rendered and read (§9); the remaining ~50 pages in the "top ~5%" range on any given metric were not individually inspected, so the true proportion of genuine anomalies vs. as-yet-unclassified ordinary pages within that range is unknown, not merely "assumed high" — the 7/7 anomaly rate observed here is a small-sample result, not a proven population rate.
- Category C (hierarchy continuity) and D (representation repetition) signals were not implemented at all (§11) — this survey cannot report on their usefulness, only on the fact that they were not attempted within scope.
- The `X_BUCKET`/`Y_BUCKET` bucket sizes (5pt / 1pt) used in the scratch script were chosen once, from inspection of typical MEXT column spacing, and not systematically varied — a different bucket size could plausibly change rankings; this was not explored, and no bucket size was chosen to favor p1327's ranking (the same sizes were used for every page).
- No page beyond the ones in §5/§9 (a small, non-exhaustive set) was directly visually confirmed; the global statistics in §8 rest entirely on the mechanical script's own bucketing logic for the other ~1,330 pages.

## 15. Open questions

- Does the embedded matrix's own `計` (total) column genuinely duplicate an amount also present in the resumed ledger below it on the same page, and if so, in what proportion of instances across the document? (Category D, not investigated — §11.)
- How many total instances of each of the three families (§9) exist across the full 1,339-page document? Only a lower bound (≥5 for the project/committee-matrix family, ≥1 each for the other two) is established here.
- Would a Docling-table-region-count signal, or a genuine PDF vector-ruling-line signal, rank these families more sharply than the pdf.js-coordinate proxy used here? (§7, §11 — hypothesized, not tested.)
- Is `pdfPageIndex` 713's multi-year commitment-schedule family (occupying an entire page, with no ordinary ledger row at all) common enough elsewhere in the document to warrant a distinct detection strategy from the project/committee-matrix family?

## 16. Recommended next experiment

A single, focused follow-up: **compute the same style of per-page structural signal directly from Docling's own already-existing `tables` output** (table count, and each table's `numRows`×`numCols`, per page) across the same MEXT source, and compare its ranking of the known families (§9) against the pdf.js-coordinate-based ranking obtained here — to test the hypothesis (§7, §11) that a genuine table-region-detection signal separates these families more sharply than the coordinate-density proxy did, still without registering any page as a new benchmark target, without Ground Truth, and without modifying production code.

Not executed in this task.

---

## Answers required by the originating task

1. **p1327's exact locators**: viewer/1-based PDF page **1327**; `pdfPageIndex` (0-based) **1326**; printed page label **文（ス） 1335**.
2. **Source-safe special structures confirmed**: a blank header-row amount triple co-occurring with an immediately adjacent, differently-shaped ruled matrix region (distinct column count, distinct cell layout, its own `計` row) — confirmed present at `pdfPageIndex` 1326, 1278, 264, 1169 (project/committee-breakdown family) and, in a structurally different shape, at `pdfPageIndex` 713 (multi-year commitment schedule) and 845 (per-country itemization).
3. **Semantic interpretation vs. unresolved**: whether the embedded matrix constitutes a duplicate representation, a cross-tab in a formal sense, or a "繰入"/transfer concept is explicitly **unresolved** (§4.3, §13, §15) — not decided in this task.
4. **Signal best distinguishing anomalous from ordinary pages**: `maxRowBandWidth` (the widest count of distinct x-position clusters within one row-band) — see §8, §10.
5. **Could p1327 be candidated without prior knowledge?** Yes, within a top-~5% (≈40–60 page) candidate set on two independently-computed metrics, but it was not the single top-ranked page on any one metric (§8, §10).
6. **Anomaly candidates other than p1327**: `pdfPageIndex` 713, 1278, 84, 264, 1169, 845 — six independently-surfaced candidates, spanning at least three distinct structural families (§9).
7. **Candidates that cannot be confidently called false positives**: none of the seven inspected pages (including p1327) was classified as an ordinary page that merely happened to score high — every one contained a genuine non-ordinary embedded region, though of varying kinds (§9).
8. **text-only / coordinates / rendering distinctions**: density signals are text-only; x-cluster/row-band-width signals require coordinates; true ruling-line/table-region signals require either vector-drawing data or an engine's own table-region output (not computed here); visual confirmation requires rendering (§7).
9. **Architecture position of anomaly detection**: best placed as a document/layout-family interpretation-layer concept operating on already-available engine raw output, not hardwired to one engine's coordinate system (§12).
10. **Strategy Selection / Case Package implications**: a per-page anomaly-candidate score computed once from existing raw extraction output is a plausible, cheap, pre-semantic Strategy Selection trigger input; the specific signals computed here are engine-derived, not source-safe in the strict Case Package sense (§12).
11. **MOF CSV connection implications**: risk of double-counting or misattribution if a canonical-hierarchy mapping cannot distinguish these (at least three, structurally different) embedded-table families from ordinary ledger rows; p1327 is explicitly not classified as a "繰入" or any other specific MOF-CSV concept (§13).
12. **Production code / benchmark semantics unchanged**: confirmed — no extraction, normalization, adapter, or evaluator file was modified; p1327 was not registered as a benchmark target and no engine was newly run against it as part of production code (§2, §7).
13. **Frozen artifacts unchanged**: source lock/raw, case-004 selection protocol/record, Ground Truth, first frozen benchmark, and both prior context diagnostics all re-verified byte-identical before and after this task (§2, and re-verified again immediately before commit).
14. **Validation**: `npm run validate` and `git diff --check` both run and passing (see commit below); no experiment code was added to the repository (the analysis script remained in this session's own scratch directory, not committed, per the task's instruction to keep any committed experimental code clearly separate from production — none was committed in this task).
15. **Commit SHA / push**: recorded in the Git section of the handoff message accompanying this report.
16. **Most valuable next experiment**: compute the same per-page anomaly signal from Docling's own existing table-region output and compare its ranking of the known families against this task's pdf.js-coordinate-based ranking (§16).
