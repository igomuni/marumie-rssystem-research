# Case-006 法務省 (MOJ) — First Frozen Benchmark Run

Status: **first frozen benchmark run preserved as-is, using the existing, unmodified pipeline and evaluator semantics. No OCR was added, no parser/normalizer/evaluator was changed, no Ground Truth was modified.**

Date: 2026-09-28 (Asia/Tokyo)

Branch: `research/case-006-moj-source-survey`.

## 1. Executive summary

The first frozen benchmark run against Case-006's own already-selected row produced a genuinely **unexpected, non-uniform result**: `pdfjs-baseline` and `pymupdf-baseline` both scored 2/11 with a clean, honest null extraction (zero lines, matching the source survey's own exhaustive text-absence finding exactly), but `docling` **also** scored 2/11 — not via a null result, but via its own **pre-existing, unmodified default OCR fallback** (RapidOCR, part of Docling's own library defaults, never configured or touched by this repository's adapter code or by this task). Docling's OCR correctly recognized most individual glyphs on the page, including **every one of the six amount figures** and the item/expense-level codes, but its table-structure-to-grid reconstruction step badly scrambled which glyphs belong to which row/column, so no single check that requires a *correctly associated* value could pass. All three engines converge on the identical 2/11 score for different reasons at different failure layers — this is disclosed precisely, not smoothed into a single "all engines got 2/11" statement.

## 2. Task boundary

This task ran the existing, unmodified benchmark pipeline (`npm run extract` then `npm run docbench -- case-006`) exactly as used for case-001–005, preserved the first result as-is, performed a reproducibility check, ran the repository's own regression-safety tests, and analyzed the result by failure layer using only already-frozen source-side evidence. This task did **not**: add OCR, add a Case-006-specific adapter or special case, modify any parser/normalizer/evaluator, modify Ground Truth, or begin any Case-007 work.

## 3. Frozen inputs / commit chain

| Artifact | Commit |
|---|---|
| Source survey | `b4a9cd2` |
| Selection protocol freeze | `7ef2250` |
| Selection record freeze | `e2253ee` |
| Ground Truth freeze | `952a0c1` |
| Case-006–010 Selection Freeze | `654e3c5` |
| Pre-task HEAD (this task) | `952a0c1`, re-confirmed via `git fetch`/`git status` immediately before this task's first command |

All five re-verified byte-identical to their own freeze commits after this task's own run (§15).

## 4. Source representation recap (not re-derived, cited from already-frozen evidence)

Per the Case-006 source survey: 737 pages, zero extractable text (exhaustively confirmed across all pages), zero font/image/XObject resources on every sampled page, visible content drawn as filled vector path outlines. Per the Case-006–010 Selection Freeze's own binding methodology note: a null/empty result from the compared engines must be analyzed as a **pipeline-applicability-boundary** finding, not scored as an ordinary document-understanding failure. This run's own actual result (§6) required that framing to be applied more carefully than anticipated, since only two of the three engines actually produced a null result.

## 5. Benchmark command / environment

```text
npm run extract
npm run docbench -- case-006
```

Engine versions, as recorded by the existing, unmodified pipeline's own evaluation output: `pdfjs-baseline` (pdfjs-dist 4.10.38), `pymupdf-baseline` (1.28.2), `docling` (2.130.0). No engine was added, removed, or reconfigured for this case.

## 6. First-attempt runtime result

All three engines completed without a runtime error. Console output from the extraction and benchmark commands:

```text
EXTRACTED moj-fy2024-general-account-expenditure-request pages=737 items=0 lines=0 linesSha256=01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b

RAW pdfjs-baseline/case-006: page=8 lines=0 unit=null
RAW pymupdf-baseline/case-006: page=8 lines=0 unit=None
[RapidOCR init logs — see §7]
2026-09-28 08:14:38,443 MatchingPostProcessor WARNING  1 of 146 pdf cells matched neither a row nor a column band of the 22x57 grid and were dropped from the table
RAW docling/case-006: page=8 tables=1 cells=88 texts=2 unit=None

=== Summary ===
pdfjs-baseline: 2/11 checks passed
pymupdf-baseline: 2/11 checks passed
docling: 2/11 checks passed
```

**This first-attempt result is preserved as-is and was not re-run with any changed configuration.** The reproducibility check (§14) used only a second, identically-configured run for verification, not to alter this preserved result.

## 7. Raw extraction outcome by engine

- **`pdfjs-baseline`**: `page=8 lines=0 unit=null`. The underlying `npm run extract` step (which this baseline reuses, per its own documented provenance) processed all 737 pages of the source and produced `items=0 lines=0` for the entire document — an exhaustive, document-wide zero, not merely a zero on the one target page. This matches the source survey's own exhaustive `pdftotext` finding exactly.
- **`pymupdf-baseline`**: `page=8 lines=0 unit=None`. Identical outcome and identical underlying cause (no text objects anywhere in the source).
- **`docling`**: `page=8 tables=1 cells=88 texts=2 unit=None`. **Not a null result.** Docling detected one table region and populated 88 cells from it, plus 2 non-table text fragments. The console log shows Docling's own pipeline initializing `RapidOCR` (three separate model-loading log blocks: detection, classification, recognition) — Docling's own library default behavior when a page has no usable text layer, entirely unconfigured and unmodified by this repository's adapter code (confirmed by direct inspection of `scripts/document-understanding/adapters/docling/src/run.py`: the converter is instantiated as `DocumentConverter()` with zero options, meaning every setting, including OCR, is Docling's own library default — this has been true, unchanged, since before case-001, and has simply never been visibly consequential until a genuinely text-layer-less source was benchmarked).

## 8. Complete engine × check matrix

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

Full per-check `actual`/`expected`/`note` detail: `reports/document-understanding/case-006-evaluation.md` (auto-generated by the unmodified evaluator, not hand-edited).

## 9. Scores under unchanged evaluator semantics

`pdfjs-baseline`: 2/11. `pymupdf-baseline`: 2/11. `docling`: 2/11. **The identical score conceals a materially different situation per engine** (§10) — this report does not stop at the score.

The two PASSing checks for all three engines:
- `page_identification`: PASSes trivially for all three, since the page number itself is supplied by the harness/adapter invocation (`page=8`), not derived from the source's own text content — this check does not depend on text-layer presence at all.
- `delta_sign_evidence_matches_source`: PASSes for `pdfjs-baseline`/`pymupdf-baseline` because Ground Truth expects no `△` glyph and the engines observed nothing (no false glyph fabricated — a "no glyph expected, nothing observed" PASS, not evidence of successful delta recovery, per this check's own documented semantics). For `docling`, the same PASS occurs for the same reason: its own OCR did not fabricate a `△` glyph either, even though its table-structure reconstruction failed to associate any amount value with the target row at all (`triple: null` for both the item and expense candidate rows in `docling.normalized.json`).

## 10. Earliest failure layer by engine

Per the Selection Freeze's own explicit instruction not to collapse this into "document-understanding failure" without checking, and using only already-frozen source-side evidence (§4):

- **`pdfjs-baseline` / `pymupdf-baseline`**: earliest failure layer is **text extraction itself**. There is no text object anywhere in the source for either engine to read (confirmed exhaustively in the source survey and re-confirmed by the document-wide `items=0 lines=0` extraction result, §7). Document/layout understanding, normalization, and semantic interpretation are never reached — there is nothing for those later layers to operate on.
- **`docling`**: earliest failure layer is **document/layout understanding** (specifically, table-structure-to-grid reconstruction) — a categorically *later* layer than the other two engines. Docling's own built-in OCR step did **not** fail at text extraction: the raw markdown output (`docling.raw.json`) shows individually legible, largely correct character recognition, including **all six amount figures exactly as they appear in Ground Truth** (`170,106,288`, `186,770,475`, `113,117,914`, `132,359,205`, `112,183,723`, `131,650,389`) and the delta values (`16,664,187`, `19,241,291`, `19,466,666`), plus the item/expense identifiers (`010`, `01-95`, `①`). The failure is that Docling's own `MatchingPostProcessor` mis-assigned these correctly-recognized text fragments to the wrong cells of an ill-fitting 22×57 grid (the console warning `1 of 146 pdf cells matched neither a row nor a column band ... and were dropped` is the visible symptom of a broader mismatch, not an isolated single-cell issue — the normalizer's own candidate extraction shows the item-code cell containing only `"010 法"` — missing `務本省`, which appears scrambled into a different row's own cell — and the expense-code cell containing `"01-95 な経費 001 001人"`, a fusion of the correct expense fragment with unrelated sub-item content from a lower row). Normalization and semantic interpretation are reached and executed correctly *given their own malformed input* (the deterministic normalizer faithfully reports `triple: null` because no amount cell was ever co-located with the identifier cells it examined) — the fault lies upstream, in Docling's own table-structure model's reconstruction step, not in this repository's own normalizer.

## 11. Raw vs. normalized behavior

- `pdfjs-baseline`/`pymupdf-baseline`: raw = `lines: []` (empty array, not null — the extraction succeeded as a process, it simply found nothing); normalized = `result` with every content field `null`, `unit: null`. No interpretation was mixed into the raw artifact; the raw file is preserved exactly as produced.
- `docling`: raw = a populated `markdown` table representation, one table with 88 cells (`docling.raw.json`), preserved exactly as Docling itself produced it — including its own garbled cell placements, not cleaned up or reinterpreted by this repository's own code. Normalized = `docling.normalized.json`'s own `candidates`/`result`, which faithfully reports what the raw structure actually contained (a `null` triple for both candidate rows), not a reconstruction or repair of the raw data.

## 12. Comparison with human-visible Ground Truth

Every value in `ground-truth.json` (itemCode `010`, itemName `法務本省共通費`, requestNo `1`, expenseCode `01-95`, expenseName `法務本省一般行政に必要な経費`, previousBudget `112183723`, fy2024Request `131650389`, delta `19466666`, unit `千円`) was independently confirmed, in this task, to be **individually present as recognizable text** in Docling's own raw OCR output (§10) — the human-readable source and Docling's own OCR agree at the character level, on this specific page, far more than the final 2/11 score alone would suggest. The gap between "characters recognized" and "values correctly extracted" is entirely a table-structure-association failure, not a character-recognition failure, for this specific engine on this specific page.

## 13. Why this is / is not a document-understanding failure

For `pdfjs-baseline` and `pymupdf-baseline`, this is **not** a document-understanding failure — it is a **pipeline-applicability-boundary** finding, exactly as the Selection Freeze's own methodology note anticipated: there is no text-layer input for document understanding to even begin operating on. For `docling`, the situation is more nuanced and was **not** fully anticipated by the Selection Freeze's own framing (which assumed a uniform null result across all three engines): Docling's own OCR step *does* cross the text-extraction boundary that stops the other two engines, meaning Docling's own failure genuinely *is* a document-understanding-layer failure (table-structure reconstruction) — but one triggered by an unusual, OCR-derived input that Docling's own table-structure model was evidently not well-suited to handle, rather than by any weakness in this repository's own document-family-specific normalization logic (which faithfully processed whatever candidate structure Docling handed it, per §10). This distinction — "document understanding failure given a genuinely available text signal" vs. "no text signal exists at all" — is the single most important finding of this run, and is exactly the kind of nuance the Selection Freeze's own methodology note existed to make room for.

## 14. Cross-case comparison with case-001–005

`[FACT]`, stated at the correct strength per the originating task's own explicit caution against a naive "Case-006 is worse" comparison:

| Dimension | case-001–005 | Case-006 |
|---|---|---|
| Ledger grammar | Standard (組織/項/経費, etc.) | Identical standard grammar (confirmed in the source survey) |
| Source representation | Full text layer | Zero text layer; vector-outlined glyphs |
| Ground Truth availability | Established via direct visual transcription | Established via direct visual transcription — **identical method**, unaffected by representation |
| `pdfjs-baseline`/`pymupdf-baseline` extraction applicability | Applicable (text present) | **Not applicable** — zero text objects exist; this is the boundary condition the case exists to test |
| `docling` extraction applicability | Applicable via native text/table-structure reading | **Applicable via its own OCR fallback**, but with degraded table-structure fidelity on this specific page — a **new** failure mode not observed in any of case-001–005 (whose own Docling failures were table-grid misalignment/row-merging *on a genuine text layer*, not OCR-fallback table-structure degradation) |

Case-006's own 2/11 score is **not directly comparable** to case-005's own 10/11 as a claim that "the engines got worse" — the two scores measure different things: case-005's score reflects document-understanding quality given a fully available text signal; Case-006's `pdfjs-baseline`/`pymupdf-baseline` score reflects a signal that was never available at all (a representation-boundary result), and Case-006's own `docling` score reflects a *third*, previously-unobserved situation: an OCR-recovered signal whose *content* was largely correct but whose *structural association* failed.

## 15. Reproducibility result

A second, identically-configured run (`npm run docbench -- case-006`) was performed for verification only, not to replace the preserved first result. Byte-for-byte comparison of `derived/document-understanding/case-006/*.raw.json` and `*.normalized.json` between the two runs found **zero differences** in content — including Docling's own garbled cell placements, which reproduced identically both times (deterministic, not flaky). The only differences found anywhere were `evaluatedAt`/`generatedAt` wall-clock timestamp fields in the evaluation JSON and Markdown outputs, which are expected to differ on every run. **The result is fully reproducible.**

## 16. Unexpected findings

1. **The uniform-null-result assumption did not hold.** Only 2 of 3 engines produced a genuine null; Docling produced substantial, largely-correct OCR content that nonetheless failed the same checks for a structural, not a recognition, reason.
2. **Docling's own OCR fallback (RapidOCR) is a pre-existing, unmodified default of the already-committed adapter code**, silently present since before case-001, never previously visible in this program's own results because every prior case had a genuine text layer for Docling to prefer. This is a genuine discovery about the *existing* pipeline's own behavior, not a change introduced by this task.
3. **OCR-recognized character content and structurally-correct extraction are not the same thing** — Docling's own raw output shows every Ground Truth amount value individually present and legible, yet zero of them made it into a structurally-associated, checkable result.

## 17. Limitations

- This analysis covers only the single already-selected target row; Docling's own table-structure failure was not characterized across the rest of `pdfPageIndex` 8 or any other page.
- Whether Docling's own OCR fallback would behave similarly (partial, correct-character/wrong-structure) on other pages of this same document, or on other rasterized-family census authorities (e.g., 金融庁/FSA), was not investigated in this task.
- No attempt was made to determine why Docling's own `MatchingPostProcessor` produced a 22×57 grid for this specific page, or whether a different Docling configuration (explicitly not tried, per this task's own prohibition on adaptation) would produce a better-structured result.

## 18. What was deliberately not changed

Per the task's own explicit prohibitions: no Case-006-specific adapter was added; no vector-outline-specific processing was added; no OCR fallback was added (Docling's own was already present, unmodified, and untouched); no empty-result special case was added to the evaluator; no normalization, check definition, or scoring logic was changed; no engine was added, removed, or reconfigured for this case specifically; the Ground Truth was not adjusted to match any engine's output in either direction.

## 19. Recommended next experiment (not executed)

Per the originating task's own instruction to only recommend, not execute:

- **Case-006 closeout** (packaging this research line for review) is the most conservative next step, consistent with the frozen execution order's own "one case at a time" discipline.
- A **separate, later, separately-scoped Docling-OCR characterization experiment** (not an "OCR experiment for Case-006" in the sense of trying to fix its score, but a study of *why* Docling's own table-structure model degrades on OCR-derived input) would be a natural follow-up, given how much correct character content this run's own raw output already contains.
- An **evaluator/applicability concept review** (§20 below) is worth a dedicated, separate design task, not implemented here.

If a Docling-OCR characterization experiment is pursued, it must be a **separate commit/task** from this first-frozen benchmark preservation, per the originating task's own explicit instruction.

## 20. Evaluator/applicability-concept discussion (proposal only, not implemented)

The Selection Rationale Review had left open whether a new evaluator check category is needed to represent a "pipeline-applicability-boundary" result distinctly from an ordinary FAIL. This run's own actual result sharpens, rather than resolves, that question: the existing 11 checks correctly report FAIL for every content-accuracy check regardless of *why* the value is missing (no signal at all, vs. a signal that was recognized but structurally misplaced) — the score alone genuinely cannot distinguish these two, materially different situations, and this report's own §10/§13 analysis exists precisely because the score could not do that job. `[PROPOSAL, NOT IMPLEMENTED]`: a future evaluator or Case Package schema extension might record, per engine per case, a per-check-independent `applicabilityStatus` (e.g., `no-signal` / `signal-present-structurally-misassociated` / `signal-present-correctly-associated`) as metadata alongside the existing PASS/FAIL matrix — this would let a future cross-case report distinguish Case-006's own `pdfjs-baseline` result from its own `docling` result programmatically, rather than requiring a bespoke narrative analysis like this report's own §10 every time. This is recorded as a discussion point for a future, separate design task, not implemented here.

---

**The Case-006 first frozen benchmark was preserved using the existing, unmodified pipeline and evaluator semantics. No OCR, parser adaptation, normalization change, evaluator change, or Ground Truth modification was performed.**
