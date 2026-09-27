# case-005 First Frozen Benchmark Run — MLIT (国土交通省) FY2024 General-Account Expenditure Request

Status: **first frozen out-of-sample benchmark result. No adaptation applied.**

Date: 2026-09-27 (Asia/Tokyo)

## 1. Purpose

> With the case-005 source, selection, and Ground Truth already frozen and unmodified benchmark semantics, what do `pdfjs-baseline`, `pymupdf-baseline`, and `docling` actually produce on MLIT's target row — and how does this compare to the four prior cases' own first-frozen and current results?

This is an observation/diagnosis task. No extraction, normalization, adapter, or evaluator code was changed to improve any result. If the result had been poor, it would have been preserved unchanged — it happens to be the strongest first-frozen result in this research program so far, and is reported with the same scrutiny as any other outcome, not with extra credit for looking good.

## 2. Freeze chain (verified before this run)

- Branch `research/case-005-mlit-source-survey`; pre-task `HEAD` `e1ed08e`; working tree clean; `origin/main` unchanged at `34c9424`.
- Selection protocol: `9b292c0` — re-verified byte-identical.
- Selection record: `bab422f` — re-verified byte-identical.
- Ground Truth (`ground-truth.json` + evidence): `e1ed08e` — re-verified byte-identical, both before this run and again after.
- `sourceId`: `mlit-fy2024-general-account-expenditure-request`, SHA-256 `4eebb84cec72a4b3b11a2b89c41093550bef5a07095d5c7b178e238406b08217` — recomputed via `shasum -a 256`, matches.
- Target row: `pdfPageIndex` 28, printed `国（本） 19`, item `002 国土交通本省共通費`, request no. `①`, expense code `05-95`, `国土交通本省一般行政に必要な経費`.

## 3. Source/GT integrity

Re-verified via direct `git diff` against each freeze commit, both before this task's first command and again immediately before commit: the selection protocol, selection record, and Ground Truth (JSON + evidence) are all byte-identical to their respective freeze commits. No case-001–004 file, and no file under `scripts/`, was modified anywhere on this branch (confirmed via `git diff --stat origin/main -- scripts/` returning empty).

## 4. Benchmark semantics confirmation

Re-confirmed by direct reading of the source files actually used for this run — `common.mjs`, `normalize.mjs`, `normalize-docling.mjs`, `evaluate.mjs`, `run.mjs`, and all three adapters' `run` scripts — that none was edited in this task. The same 11 checks, the same `closeCjkWrapSpaces`/`reconstructNumericToken` normalization rules, and the same adapter set (`pdfjs-baseline`, `pymupdf-baseline`, `docling`) already used for case-001–004 were used unchanged. No new check, no case-005-specific branch, and no OCR/MinerU/PaddleOCR engine was added.

## 5. Extraction prerequisite

`npm run extract` had not yet processed the MLIT source — `derived/pdf-extraction/run-manifest.json` listed only the five pre-existing sources (digital-r6-request-table-01, digital-r6-important-policy, meti, mic, mext). Running the existing, unmodified command reprocessed **all six** locked PDF sources (this command iterates every `application/pdf` entry in `sources/source-lock.json`, not a per-case selection). The five previously-processed sources produced byte-identical `linesJsonlSha256` hashes to their historical values (`bd29feaef...`, `3688fcc79...`, `6f51498ed...`, `7384522d3...`, `e56cc46cb...` — all unchanged, verified directly against the manifest's own pre-run values recorded before this task's first command), confirming this was purely a missing-prerequisite run, not a semantic or code change. MLIT itself extracted as `pages=1097 items=429241 lines=43918`, completing in a few seconds with no encryption-related issue (the source is unencrypted, per the source survey). This is a data-generation prerequisite, not a benchmark-semantic change.

## 6. First-attempt outcome

`npm run docbench -- case-005` ran to completion on the **first attempt**, with no failure, retry, or environment issue of any kind. No runtime/harness problem occurred, so there is no failure-preservation obligation beyond recording that the first attempt succeeded cleanly.

## 7. Complete result matrix (case-005, first frozen run)

| check | pdfjs-baseline | pymupdf-baseline | docling |
|---|---|---|---|
| item_name_exact_match | FAIL | FAIL | FAIL |
| item_name_present_among_candidates | PASS | PASS | PASS |
| expense_name_exact_match_after_line_join | PASS | PASS | PASS |
| previous_budget_exact_match | PASS | PASS | PASS |
| fy2024_request_exact_match | PASS | PASS | PASS |
| signed_delta_exact_match | PASS | PASS | PASS |
| unit_exact_match | PASS | PASS | PASS |
| page_identification | PASS | PASS | PASS |
| delta_sign_evidence_matches_source | PASS | PASS | PASS |
| item_to_amount_relationship | PASS | PASS | PASS |
| expense_to_amount_relationship | PASS | PASS | PASS |

This is the complete, unmodified check set emitted by `evaluate.mjs` — no check was added or removed for this task.

## 8. Scores

| Case | pdfjs-baseline | pymupdf-baseline | docling |
|---|---|---|---|
| case-001 (current) | 8/11 | 8/11 | 9/11 |
| case-002 (current, evaluator-corrected) | 4/11 | 4/11 | 3/11 |
| case-003 (current) | 10/11 | 10/11 | 3/11 |
| case-004 (current) | 7/11 | 7/11 | 5/11 |
| **case-005 (first frozen)** | **10/11** | **10/11** | **10/11** |

**case-005 is the strongest first-frozen result in this research program so far, and the first case where Docling's score equals the flat-text engines'.** Per this task's own instruction, this is reported plainly, not treated as a reason to relax scrutiny — every PASS below was individually verified against the raw/normalized artifacts, not assumed from the score.

## 9. Raw observations

- **pdfjs-baseline / pymupdf-baseline**: the target row is reconstructed as a single clean line (`"1 05-95 国土交通本省一般行政に 118,052,728 136,727,866 18,675,138"` for pdfjs), with its wrapped label continuation absent from this line — **[OBSERVATION]** unlike every prior case, here the raw line for the target row already contains the code and the *first* line of the label together with the full amount triple, while the label's second line (`必要な経費`) appears to have been captured within the same reconstructed line already in this instance (confirmed via the normalized output §10, since `joinWrappedLabel` correctly produced the full label — see §12 for the precise mechanism).
- **[OBSERVATION] CJK-spacing artifact confirmed present and correctly closed**: the raw lines for both header/aggregate rows on this page (`"010 国 土 交 通 本 省 5,439,976,254 ..."`, `"002 国 土 交 通 本 省 共 通 費 119,106,358 ..."`) show the same wide-letter-spacing artifact already documented in case-002/003/004 (MLIT's Producer is "List Creator", the same toolchain already associated with this artifact). The target expense row's own raw line (`"1 05-95 国土交通本省一般行政に ..."`) shows **no** such spacing — consistent with the established finding that this artifact affects header/total-style rows specifically, not ordinary expense rows, and is not new to case-005.
- **Docling**: the target row's own cell (`row 4, col 1`) already contains the joined label as one string (`"05-95 国土交通本省一般行政に 必要な経費"`) — Docling's own cell-text assembly naturally concatenates the wrapped label's two visual lines with a space, which `closeCjkWrapSpaces` then closes in normalization. Amount cells show the already-known reversed-comma-group artifact (e.g. `"728 052, 118,"` for `118,052,728`), handled deterministically by the existing `reconstructNumericToken`. **[OBSERVATION]** No column-fusion or row-misalignment artifact (the specific failure modes that reduced Docling's score on case-003/004) occurred here — Docling's own table for this page (23 rows × 10 columns, 97 cells) cleanly separated the target row's own previous/current/delta cells into three distinct cells, each independently reversible.
- **[OBSERVATION] Item context, unlike case-004**: the item-level header row (`002　国土交通本省共通費`) is on the **same page** as the target expense row (both `pdfPageIndex` 28) — a direct contrast with case-004 (MEXT), where the equivalent item header was on the immediately *preceding* page and therefore invisible to any engine's single-page-scope extraction. This is the direct, observed reason `item_name_present_among_candidates` PASSes for all three engines here, unlike case-004's uniform FAIL.
- **[OBSERVATION] Unit**: `"(単位:千円)"` is printed directly on the target's own page (`pdfPageIndex` 28), immediately beneath the table title — exactly matching the Ground Truth evidence's own page-level scope finding (§11 of the GT evidence document), and unlike case-004's table-wide-remote-only convention.
- **[OBSERVATION] Remarks**: the two aggregate rows preceding the target (`010`, `002`) both carry lengthy free-text remarks blocks on this same page (visible in every engine's raw output, e.g. pdfjs's lines 7–17). This did **not** interfere with the target row's own triple extraction or its item/expense association — the remarks-column contamination pattern that broke case-002's `splitTrailingTriple` regex did not recur here, because (per direct inspection) the target row's own remarks cell is empty, structurally the same "empty remarks on the target row" pattern already found in case-003.

## 10. Normalized observations

- `findItemCodeRows`/Docling's `findRows` correctly identified four item-code-shaped candidates on this page (`010`, `002`, `001`, `006`) — the same generic hierarchy-ambiguity pattern already observed in every prior case, here occurring because `001`/`006` are genuine subordinate breakdown codes (item-level and sub-item-level respectively) that share the same 3-digit-prefix shape as the true item header `002`.
- `closeCjkWrapSpaces` correctly closed the wide-letter-spacing artifact on both aggregate rows' own item names (`"010"` → `"国土交通本省"`, `"002"` → `"国土交通本省共通費"`, both unspaced in the normalized output) — observed after the run, not predicted in advance; this is the same rule already frozen in `common.mjs` from prior cases, unmodified.
- `reconstructNumericToken` correctly reversed Docling's own comma-group ordering for all three amount cells on the target row, producing the correct magnitudes.
- No normalizer needed any new rule, branch, or exception for MLIT.

## 11. Evaluated observations

- **10 of 11 checks PASS for all three engines** — the target row's own code, label (with correct 2-line join), amount triple, unit, page, delta-sign evidence, and both relationship checks (item-to-amount, expense-to-amount) all resolve correctly.
- **`item_name_exact_match` FAILs for all three engines** — the sole shared failure, caused by the same hierarchy-ambiguity mechanism already documented in every prior case: `singleItem` resolution requires exactly one item-code-shaped candidate, but four exist on this page, so `itemName` resolves to `null` regardless of the fact that the *correct* candidate (`002`/`国土交通本省共通費`) is genuinely present and correctly reconstructed (confirmed via the passing diagnostic check, `item_name_present_among_candidates`).

## 12. Failure-layer analysis

Using this repository's own ADR-010 architecture taxonomy:

- **Source acquisition**: no findings — source correctly locked, unencrypted, rendered without issue.
- **Extraction representation**: no findings — every engine's own raw output for this page is accurate to what is actually printed.
- **Engine-specific normalization**: no findings — `closeCjkWrapSpaces` and `reconstructNumericToken` both behaved exactly as already established, with no new gap exposed.
- **Structural context selection**: no findings — the item header is on the same page as the target row here, so the single-page-scope architecture's known limitation (fully exposed in case-004) is simply not triggered by this particular row's own position.
- **Document/layout-family interpretation**: this is where the one shared failure (`item_name_exact_match`) lives — the current architecture's `singleItem`-requires-exactly-one-candidate resolution rule cannot disambiguate among multiple genuine item-code-shaped rows on one page (organization-level, item-level, and subordinate-breakdown codes all share the same generic 3-digit-prefix shape). This is not a semantic-matching/evaluation-layer defect: `evaluate.mjs` correctly and transparently reports the miss; the ambiguity is unresolved earlier, in how item-code-shaped rows are distinguished from each other before comparison.
- **Semantic matching/evaluation**: no defect found — every check faithfully compares the already-produced normalized result against Ground Truth, with no silent repair or credit.

**This is the fifth independent case (001–005) in which the identical `item_name_exact_match` failure mode reproduces for every engine** — the single most robust, cross-case-replicated finding in this entire research program.

## 13. Raw / normalized / evaluated separation

Explicitly kept separate throughout §9–§11 above, per the task's own instruction: §9 (raw) describes only what each engine's own extraction actually produced; §10 (normalized) describes only what the existing, unmodified normalizers changed; §11 (evaluated) describes only what the 11 checks concluded from the already-normalized result. No raw artifact was edited at any point.

## 14. Cross-case comparison

case-005 is the fifth ministry surveyed in this research program. Compared against already-committed evidence (no prior case was re-benchmarked for this comparison):

- **Similar to every prior case**: `item_name_exact_match` FAILs universally (5/5 cases, all engines) — now the most consistently-replicated finding across this entire program.
- **Similar to case-003**: the target row's own remarks column is empty, so the annotation-contamination pattern that broke case-002's regex does not recur; both flat-text engines score strongly (10/11) for the same underlying reason.
- **Different from case-004**: item-header context is present on the target's own page here (unlike MEXT's page-boundary loss), directly explaining why `item_name_present_among_candidates` and `item_to_amount_relationship` PASS here but FAILed for all three engines in case-004.
- **Different from case-002/003/004's own Docling results**: this is the **first case where Docling scores equal to the flat-text engines (10/11)** — neither case-002's row-under-pairing, case-003's row-over-merging, nor case-004's column-fusion artifact recurred on this specific page's own table geometry. This is recorded as an observation specific to this page, not a claim that Docling's general reliability has improved — a different MLIT page could plausibly still exhibit any of those prior failure modes, untested here.
- **New**: MLIT is the first source in this program where `Producer: List Creator` co-occurs with the target row's own item header on the *same* page as the target row (case-002's own equivalent header was also same-page; case-003 and case-004 were not) — reinforcing that same-page-vs-different-page item context is a property of the specific row selected, not a fixed property of a ministry's document family.

## 15. Reproducibility

A second complete `npm run docbench -- case-005` run was performed after the first. Every raw artifact (`pdfjs-baseline.raw.json`, `pymupdf-baseline.raw.json`, `docling.raw.json`) and every evaluation check array were compared field-by-field (via `JSON.stringify` diff) between the two runs: **byte-identical in both raw and evaluated content** for all three engines. No nondeterminism was observed; only the report's own `Generated:` timestamp differs between runs, consistent with already-established repository behavior.

## 16. Unexpected findings

- **Docling's `item_name_present_among_candidates` diagnostic shows a minor cross-row text fusion** for the `006` candidate (`"既定定員に伴う経費 05 人件費"` — the sub-item header's own label fused with the *next* sub-item's own header text) — this does not affect any PASS/FAIL outcome (the `006` candidate was never going to match the expected `002`/`国土交通本省共通費` pair regardless), but is recorded as a minor, genuinely new Docling cell-boundary artifact not previously documented in exactly this form.
- No runtime/harness issue of any kind occurred — a contrast with the case-003 investigation's own harness-reliability issue (already root-caused and fixed long before this task, and not re-encountered here).

## 17. No-adaptation confirmation

No extraction, normalization, adapter, or evaluator file was modified in this task. No result was rerun to seek a better outcome — the two runs performed were the first attempt and a single reproducibility check, both producing byte-identical results, and neither run's output was altered afterward. No Ground Truth value was adjusted based on any benchmark result.

## 18. Limitations

- Only one row (of potentially many eligible rows within organization `010`'s own ~480-page span) was benchmarked; this result says nothing about how MLIT's other pages, or its 11 other internal organizations, would score.
- The absence of Docling's own prior failure modes (column fusion, row misalignment) on this specific page does not establish that MLIT's document family is generally easier for Docling — only that this one page's own table geometry did not trigger those specific mechanisms.
- No investigation was made into whether the `繰入`-shaped expressions already known to exist in this document's 総表 would affect any other row's own extraction — out of scope for this task, per the originating instruction not to expand into `繰入` semantic analysis.

## 19. Recommended next step

Consistent with the originating task's own explicit deferral: a cross-case interim summary across all five surveyed ministries (case-001–005) is the natural next step, but is explicitly **not** performed in this task — it is reserved for a separately-scoped follow-up task, per the originating task's own instruction.

Not executed in this task.
