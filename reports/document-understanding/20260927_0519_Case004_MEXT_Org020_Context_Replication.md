# case-004 MEXT Organization-020 Context-Pattern Replication

Status: **read-only source-structure diagnostic. No benchmark run. No row selected. No production change.**

Date: 2026-09-27 (Asia/Tokyo)

## Research question

> Does organization `020 文部科学本省所轄機関` show the same item-header → first-expense-row context-distance pattern as organization `010 文部科学本省`? Does the table-level unit convention remain separate from local item-header context across the organization boundary?

This replicates `reports/document-understanding/20260927_0459_Case004_MEXT_Pagination_Context_Diagnostic.md`'s method in a second organization within the same locked source, to test whether its findings generalize across an internal organization boundary. It is not row selection, Ground Truth creation, or benchmark execution.

## Frozen state (verified, unchanged)

- Branch `research/case-004-mext-preregistration`; pre-task `HEAD` `187a8e9`; working tree clean before this task's first command; `main` unchanged at `3b29ebd`.
- Source `mext-fy2024-general-account-expenditure-request-detail`, SHA-256 `6df221dfd22c48e0f32dd59bcf2dbcbaad19720083be43005ce700b984a6bf71` — recomputed, matches.
- Selection protocol (`c2b2c28`), selection record (`fa82c13`), Ground Truth (`f9b2f35`), first frozen benchmark (`49f5ca6`), and the organization-010 diagnostic (`187a8e9`) — all re-verified byte-identical to their freeze commits. None was rewritten by this task; the organization-010 result is treated as historical comparison evidence, not a template organization-020 is expected to match.

## Source

`mext-fy2024-general-account-expenditure-request-detail`, 1,339 pages, unchanged. No re-lock performed. As in the organization-010 diagnostic, the sibling cover/TOC file (`..._01.pdf`) was independently re-fetched for source-safe navigation only — SHA-256 `91b39e9902610e13aa7be445db2d2d2a3e38166fd5f449bd11f94cfe5fe3b6d5`, byte-identical to the copy fetched during the prior diagnostic, confirming it is stable. It remains unlocked (not a case-004 source); no amount value was read from it.

The prior diagnostic's incidental finding — the `010`→`020` organization boundary falls at printed page 903/904 — was re-verified (not re-derived) by rendering the organization-020-level aggregate row's own page (printed page 904, `pdfPageIndex` 895): it shows `020　文部科学本省所轄機関`, confirming the boundary exactly. No further boundary study was performed.

## Replication methodology

Identical conceptual method to the organization-010 diagnostic: item-header → first-expense-row boundaries were identified from the sibling TOC file's own page-number column (source structure, not engine output), each boundary's two candidate pages (or one, if shared) were rasterized at 200dpi via `pdftoppm` and read directly, and the offset established during Ground Truth creation (printed page 9 = `pdfPageIndex` 0) was used throughout — re-confirmed correct at every sampled point in this task (printed pages 904 through 1037, zero drift, consistent with the prior diagnostic's own zero-drift finding up to page 903).

**Organization `020 文部科学本省所轄機関`'s full extent, per the TOC**: printed pages 904–1052 (the next organization, `030 文化庁`, begins at printed page 1053) — 149 pages, substantially smaller than organization `010`'s ~895 pages.

**Sample construction**: the TOC lists exactly **three** `項` (item)-level headers within this range: `010 国立教育政策研究所` (page 905), `020 科学技術・学術政策研究所` (page 993), and `030 日本学士院` (page 1036) — no more exist before organization `030` begins. Per the task's own instruction for an insufficient population, **all three available boundaries were sampled** (not a subset chosen to hit a target count); no cherry-picking was applied, and no additional boundaries could have been added without leaving organization `020`.

No `docbench`, engine, or OCR was run. No amount value is transcribed below except where unavoidable to describe presence/blankness/self-containment qualitatively (as in the prior diagnostic).

## Organization-020 sample table

| # | Item (項) | Header `pdfPageIndex` (printed) | First-expense `pdfPageIndex` (printed) | Same page? | Distance | Item context repeated on expense page? | Expense row self-contained? | Unit visible? | Remarks observation |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `010 国立教育政策研究所` | 896 (905) | 897 (906) | No | 1 | No | Yes (triple present directly) | Neither | Header row's own remarks: blank |
| 2 | `020 科学技術・学術政策研究所` | 984 (993) | 984 (993) | Yes | 0 | — (same page) | Yes | Neither | First-expense row carries a populated legal-basis remarks annotation (`文部科学省組織令第91条...`) |
| 3 | `030 日本学士院` | 1027 (1036) | 1028 (1037) | No | 1 | No | Yes | Neither | Header row's own remarks: **populated** (`(要旨)　学術上功績顕著な科学者を優遇する...`) — a pure item-aggregate row carrying remarks text, not seen in any organization-010 sample |

Additionally, organization `020`'s own opening aggregate page (`020 文部科学本省所轄機関`, `pdfPageIndex` 895, printed page 904) was inspected for a possible new organization-level unit declaration: none was found — the page shows only the organization-aggregate row and no unit text.

## Boundary-distance findings

- **Same-page**: 1 of 3 (sample 2).
- **One-page-back**: 2 of 3 (samples 1, 3) — in both, the header occupies its page with no other item's content, and the first expense row begins on the very next page with no repetition of the header's own code or name.
- **Farther-than-one**: 0 of 3.
- **Repeated/carry-forward context**: never observed, identical to organization `010`.

## Unit findings

- **Local repetition**: none of the 3 sampled header pages, 3 sampled first-expense pages (2 unique, since sample 2's pair collapses to one page), or organization `020`'s own opening aggregate page (`pdfPageIndex` 895) show any unit text.
- **New organization-level declaration**: **none found.** Crossing from organization `010` into `020` did not introduce a fresh `(単位：...)` statement anywhere inspected.
- **Relationship to the table-opening declaration**: organization `020` continues to rely entirely on the single declaration made once at the document's true first page (`pdfPageIndex` 0), exactly as organization `010` did. No other convention was observed.

## Unexpected structural observations

Per the task's instruction, these were noticed incidentally, not searched for:

- **Blank-inline-triple / nested-value pattern** (organization-010 sample 6's phenomenon): **not encountered** in any of the 3 organization-020 samples — every sampled first-expense row here carries its own triple directly. This diagnostic makes no claim about its frequency elsewhere in organization `020`.
- **Populated remarks on a pure item-aggregate header row**: encountered in sample 3 (`030 日本学士院`'s own header row carries a `(要旨)` annotation) — this is **new relative to organization `010`**, where every sampled pure item-header row (samples 1, 3, 5, 6, 8 in the prior diagnostic) had a blank remarks column. Classified here as a **remarks/layout behavior** observation, not a context-distance phenomenon — it does not change any header-distance or unit finding above.
- **Printed-page-label prefix**: organization `020`'s pages are labeled `文（所）` (所 = affiliated institution) rather than organization `010`'s `文（本）` (本 = headquarters) — a source-observable convention change tied to which organization a page belongs to, noted here as a structural fact, not evaluated for any benchmark implication.

## Organization-010 vs. organization-020 comparison

| Metric | Org 010 | Org 020 |
|---|---:|---:|
| sample count | 8 | 3 |
| same-page header | 4 | 1 |
| one-page-back header | 4 | 2 |
| farther-than-one | 0 | 0 |
| cross-page with repeated context | 0 | 0 |
| locally visible unit | 0 of 16 sampled local pages | 0 of 5 sampled local pages (+0 of 1 organization-opening page) |

As proportions: organization `010` split evenly (50%/50%) between same-page and one-page-back; organization `020`'s much smaller sample skews toward one-page-back (33%/67%). Per the task's own caution, this difference in proportion is **not treated as a meaningful statistical divergence** given organization `020`'s sample size of 3 — it is easily consistent with ordinary sampling variation around a shared underlying pattern. What *is* directly comparable and identical across both organizations, independent of sample size, is categorical: **zero instances of a header more than one page away, and zero instances of repeated/carry-forward context on a cross-page boundary**, in 11 combined samples.

## Replication verdict

**Partially replicated — the categorical pattern is confirmed identically; the same-page/cross-page proportion is directionally consistent but statistically inconclusive given organization `020`'s small population.**

Evidence for this verdict:
- The core categorical claim from organization `010` — "the item header is either on the same page or exactly one page back, never farther, and never repeated on the expense page" — holds **without exception** in all 3 organization-020 samples, exactly as in all 8 organization-010 samples (11/11 combined).
- The unit-context claim — "table-opening-only, never repeated locally, no organization-level declaration" — also holds **without exception**, now additionally confirmed not to reset or restate at an organization boundary (a question organization `010` alone could not answer, since it was the document's first organization).
- The specific same-page/cross-page *ratio* is not confirmed to be the same 50/50 split; organization `020`'s n=3 is too small to distinguish "the same underlying ratio, sampled differently" from "a genuinely different, more cross-page-leaning ratio in this smaller organization." This is why the verdict is "partial," not "strong": the qualitative mechanism replicates cleanly, the quantitative proportion does not have enough evidence to replicate or refute.

## Combined context-model sufficiency (organizations 010 + 020, source-context only)

Counting all 11 sampled boundaries together (8 from organization `010`, 3 from organization `020`):

- **A — target page only**: item-header context available for **5 of 11** (the 5 same-page samples: org-010's 4 plus org-020's 1). Unit context available for **0 of 11**.
- **B — target + immediately previous page**: item-header context available for **11 of 11** — every cross-page sample across both organizations had its header exactly one page back, with no counter-example. Unit context remains **0 of 11** (the unit declaration is always far more than one page back from any sampled boundary in either organization).
- **C — scan backward to nearest governing item header**: item-header context available for **11 of 11**, by construction, identical to B's outcome in this specific combined sample (no boundary in either organization ever required looking back more than one page, so B and C are empirically indistinguishable *here*, though they remain conceptually different strategies — see below).
- **D — table/document metadata context + local structural context**: item-header context **11 of 11** (via the same local mechanism as B/C) and unit context **11 of 11**, but only because this model explicitly separates the table-wide-once unit declaration (recoverable only via a document/table-metadata mechanism, confirmed in this task to hold across the organization boundary too) from the page-local item-header mechanism — the two remain genuinely different mechanisms serving different-scoped evidence, not one generalized "look nearby" rule.

**This diagnostic still does not claim any model would parse correctly if implemented** — only that B, C, and D would each make the necessary source context available for item-header recovery across both organizations sampled, and only D's two-mechanism design would also cover unit recovery.

## Architecture implications

The organization-020 replication strengthens, rather than newly establishes, the case-004 diagnostic's original architectural distinction: **structural context selection** (how far to look for a governing item header) and **document/table-metadata context** (where a once-only, document-wide declaration like the unit label lives) are evidenced here as needing genuinely different mechanisms, not degrees of the same one. A single fixed-window strategy (model B) is empirically sufficient for item-header recovery across 11/11 samples in this source, but would still fail unit recovery entirely, regardless of how large the fixed window were made, because the unit declaration's distance from most boundaries (up to ~1,028 pages, in the farthest organization-020 sample) is not analogous to a "slightly wider local window" problem — it is a different *kind* of context (whole-table metadata) that a page-window model does not represent at all. This reinforces treating a future Analysis Strategy's context-selection concept and its metadata-context concept as two independent knobs, not one.

Model C ("nearest governing header," no fixed distance) remains conceptually more principled than B ("fixed one-page lookback") even though this task's combined 11-sample evidence cannot yet distinguish them empirically — B happens to work here only because no observed boundary exceeded one page; C would not need that fact to remain true to keep working, which is a real semantic-clarity difference in provenance/robustness, not merely a coverage-count tie. This is stated as a research-decision preference, not as a proposal to implement C.

## Files changed

- `reports/document-understanding/20260927_0519_Case004_MEXT_Org020_Context_Replication.md` (this file, new).
- `state/CURRENT_STATE.json`, `state/TODO.md`, `state/CHANGELOG.md` (state updates).

No source-acquisition, benchmark, normalization, evaluator, selection-protocol, selection-record, Ground Truth, Case Package, or Document Profile file was modified. No row was selected or scored. No rendered image was staged (scratch directory only, removed after use).

## Validation

```bash
npm run validate      # PASS
git diff --check      # clean
```

Source SHA-256 re-verified unchanged; case-004 Ground Truth, selection protocol/record, first frozen benchmark, and the organization-010 diagnostic all re-verified byte-identical to their respective freeze commits; no benchmark/extraction/normalization/evaluator file touched; no rendered images left in the repository.

## Limitations

- Organization `020` provided only 3 valid item-header boundaries in total (its own entire population, not a sample of a larger pool) — smaller than the requested 6–10 range and smaller than organization `010`'s 8-sample diagnostic, which limits how confidently any *proportion* (as opposed to the categorical zero/one-page-distance claim) can be compared between the two organizations.
- Whether the "populated remarks on a pure item-aggregate row" observation (sample 3) is common elsewhere in organization `020` or specific to `030 日本学士院` was not investigated.
- Whether the same header-distance and unit-convention patterns hold in organization `030 文化庁` or later organizations remains unknown; this task's scope was explicitly limited to `010`→`020`.

## Recommended next experiment

A single, still read-only follow-up: **check whether organization `030 文化庁`'s own item-header boundaries (a third, differently-sized organization within the same document) continue to show the same zero-or-one-page-distance pattern and the same table-opening-only unit convention**, to determine whether two replications (`010`, `020`) generalize to a third independent organization or whether `020`'s smaller, more cross-page-leaning sample was itself an early sign of organization-size-dependent variation — still without selecting, scoring, or creating Ground Truth for any row, and still without running any engine.

Not executed in this task.
