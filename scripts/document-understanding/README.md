# Document Understanding Benchmark

This layer is separate from `scripts/pdf-extraction`. That layer answers "can we deterministically get glyphs/text/coordinates out of a locked PDF binary?" (yes, as of Workspace Phase 1D). This layer answers a harder question: "given that text, can an engine correctly recover the *document structure* — reading order, multi-line cell reconstruction, table region detection, row/column association, merged cells, and which amount belongs to which header?"

## Why this is a separate layer

```text
1. source acquisition            (sources/, scripts/source-acquisition)
2. PDF glyph/text extraction     (scripts/pdf-extraction)
3. layout/document understanding (scripts/document-understanding)  <- this layer
4. normalization
5. semantic interpretation
6. evaluation
```

Layers 3–6 are kept explicitly distinct inside this directory (`adapters/` produce raw per-engine output; `benchmark/src/normalize.mjs` reconstructs structure deterministically; `benchmark/src/evaluate.mjs` scores against ground truth). Collapsing them would make it impossible to tell whether a wrong answer came from bad extraction, bad structure recovery, or bad scoring logic.

## Directory layout

```text
scripts/document-understanding/
  README.md                  (this file)
  adapters/
    pdfjs-baseline/           implemented — reuses scripts/pdf-extraction's already-locked output
    pymupdf-baseline/         implemented — independent PyMuPDF-based baseline (pinned version)
    docling/                  implemented — table-structure-aware engine (pinned version)
    mineru/                   investigation notes only (not yet integrated)
    paddle/                   investigation notes only (not yet integrated)
  benchmark/
    src/
      common.mjs              shared paths + generic, case-blind row-parsing rules (flat-text engines)
      normalize.mjs           flat-line raw artifact -> benchmark result schema (never reads ground truth values)
      normalize-docling.mjs   table-cell raw artifact -> benchmark result schema (Docling only; never reads ground truth values)
      evaluate.mjs            normalized result + ground truth -> per-field pass/fail (only step that reads ground truth values; identical for every engine)
      run.mjs                 orchestrates adapters -> per-engine normalizer -> evaluate -> evidence + report + comparison matrix

fixtures/document-understanding/
  case-001/
    ground-truth.json         case config (which page) + expected result — kept separate from all engine output
    README.md                 why this case, what it tests

derived/document-understanding/   git-ignored: raw + normalized + evaluation artifacts (regenerate with `npm run docbench`)
evidence/document-understanding/  committed: compact per-case result summaries
reports/document-understanding/   committed: generated Markdown evaluation reports
```

## Running the benchmark

```bash
npm run sources:fetch   # materialize the locked raw PDFs (does not modify sources/source-lock.json)
npm run extract         # (for pdfjs-baseline) produce scripts/pdf-extraction's deterministic output first
npm run docbench        # runs case-001 by default; npm run docbench -- case-XXX for another case
```

`npm run docbench` runs every registered adapter for the case (skipping `pymupdf-baseline` or `docling` with a clear message if their `.venv` has not been set up — see each adapter's README), normalizes each engine's raw output with its own normalizer, evaluates every engine against the SAME `fixtures/document-understanding/<caseId>/ground-truth.json` via the SAME `evaluate.mjs`, and writes `evidence/document-understanding/<caseId>-results.json` + `reports/document-understanding/<caseId>-evaluation.md` (which includes a compact per-check comparison matrix across all engines that ran).

## Benchmark result schema

```json
{
  "caseId": "case-001",
  "engine": "pdfjs-baseline",
  "engineVersion": "4.10.38",
  "sourceId": "digital-r6-request-table-01",
  "sourceSha256": "b77f25b2...",
  "rawArtifact": "derived/document-understanding/case-001/pdfjs-baseline.raw.json",
  "result": {
    "itemCode": null,
    "itemName": null,
    "requestNo": null,
    "expenseCode": null,
    "expenseName": null,
    "previousBudget": null,
    "fy2024Request": null,
    "deltaRaw": null,
    "delta": null,
    "unit": null,
    "page": null
  }
}
```

A `null` field is a recorded extraction/structure-recovery gap, never silently filled in — consistent with the repository-wide `unknown != zero` invariant (`protocol/RESEARCH_PROTOCOL.md`), applied here as "an engine's miss is not the ground-truth value."

## What a normalizer is and is not allowed to know

Both `normalize.mjs` and `normalize-docling.mjs` read `ground-truth.json`'s `pdfPageIndex` (case configuration: which page to look at) but **never** its `result` object (the expected answer). Row detection uses only generic, page-wide structural patterns:
- `common.mjs` (pdfjs-baseline, pymupdf-baseline): three-digit item codes, `NN NN-NN` expense-row prefixes, trailing amount triples, and a general one-line continuation-join rule derived from the dominant wrapping pattern observed across the whole page.
- `normalize-docling.mjs` (docling): the same item/expense-code label patterns, but matched against individual table cells rather than flat lines, plus two Docling-specific general rules verified across multiple independent cells on the page (not fitted to any expected value): closing a wrap-induced space between two CJK characters, and reversing a numeric cell's whitespace-separated comma-groups (Docling was observed to assemble them in reverse order — see `reports/document-understanding/case-001-evaluation.md`).

`evaluate.mjs` is the only file permitted to read `ground-truth.json`'s `result` object, and is identical for every engine — it only consumes the `{ result, candidates }` shape both normalizers produce.

## Known first-pass limitation: header-row ambiguity

`case-001`'s target page contains multiple rows shaped like `NNN <name>` (item codes `036`, `041`, `046`, and the target `020`) — some are `項`-level headers, some are `目`-level sub-item headers nested under a *different* item, and none of the three current engines' structures resolve this on their own. When more than one such row is found, the normalizer reports `result.itemName = null` rather than guessing, and `evaluate.mjs` adds a diagnostic check (`item_name_present_among_candidates`) confirming whether the *correct* row was still extracted and reconstructed correctly among the candidates — it was, for all three engines. Resolving this ambiguity (e.g. via indentation/hierarchy-level detection) is future work, not something this first pass papers over.

## Docling integration result (case-001)

Integrating Docling (table-cell-structure-aware, unlike the two flat-text baselines) and running it through the identical evaluator produced a genuinely different, informative result rather than a uniform improvement:

```text
check                                      pdfjs   pymupdf   docling
item_name_exact_match                      FAIL    FAIL      FAIL
expense_name_exact_match_after_line_join   FAIL    FAIL      PASS
unit_exact_match                           FAIL    FAIL      FAIL
(all other checks)                         PASS    PASS      PASS
```

Docling's table-cell structure genuinely resolved the two-column conflation that broke both baselines' expense-name reconstruction (the wrapped label and an unrelated annotation column landed in *separate* cells). It did not resolve the header-row hierarchy ambiguity, and the page-level unit label is absent from the target page for every engine, Docling included — see `reports/document-understanding/case-001-evaluation.md` for the full per-check breakdown and `adapters/docling/README.md` for what was empirically observed about Docling's table-cell text assembly (including a reproducible, general numeric-cell-ordering artifact that the Docling-specific normalizer corrects deterministically, documented there in detail).

## Adding a new engine

1. Add `scripts/document-understanding/adapters/<engine>/` that reads `fixtures/document-understanding/<caseId>/ground-truth.json` for case configuration (page index, source id/hash) only, and writes `derived/document-understanding/<caseId>/<engine>.raw.json`. If the engine naturally produces flat text lines, match the existing `lines: [{lineIndex, text}]` shape and reuse `normalize.mjs` as-is. If it produces richer structure (tables, cells, blocks — as Docling does), **preserve that structure in the raw artifact** rather than flattening it, and add a small engine-specific normalizer (see `normalize-docling.mjs`) that emits the same `{ result, candidates: { itemRows, expenseRows } }` shape `evaluate.mjs` already consumes generically. Both `itemRows`/`expenseRows` entries need an `order` field (a comparable reading-order key) for the `item_to_amount_relationship` check.
2. Register it in `benchmark/src/run.mjs`'s `ENGINES` list, with its own `normalize` function reference.
3. Pin the engine's exact version (a `package.json` dependency, a `requirements.txt`, or equivalent) the same way `scripts/pdf-extraction` pins `pdfjs-dist` and `pymupdf-baseline`/`docling` pin their Python packages in an isolated `.venv/`.
