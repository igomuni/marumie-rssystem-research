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
    docling/                  investigation notes only (not yet integrated)
    mineru/                   investigation notes only (not yet integrated)
    paddle/                   investigation notes only (not yet integrated)
  benchmark/
    src/
      common.mjs              shared paths + generic, case-blind row-parsing rules
      normalize.mjs           raw artifact -> benchmark result schema (never reads ground truth values)
      evaluate.mjs            normalized result + ground truth -> per-field pass/fail (only step that reads ground truth values)
      run.mjs                 orchestrates adapters -> normalize -> evaluate -> evidence + report

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

`npm run docbench` runs every registered adapter for the case (skipping `pymupdf-baseline` with a clear message if its `.venv` has not been set up — see `adapters/pymupdf-baseline/README.md`), normalizes each engine's raw output, evaluates it against `fixtures/document-understanding/<caseId>/ground-truth.json`, and writes `evidence/document-understanding/<caseId>-results.json` + `reports/document-understanding/<caseId>-evaluation.md`.

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

## What the normalizer is and is not allowed to know

`normalize.mjs` reads `ground-truth.json`'s `pdfPageIndex` (case configuration: which page to look at) but **never** its `result` object (the expected answer). Row detection (`common.mjs`) uses only generic, page-wide structural patterns — three-digit item codes, `NN NN-NN` expense-row prefixes, trailing amount triples, and a general one-line continuation-join rule derived from the dominant wrapping pattern observed across the whole page (see the comment in `common.mjs`). None of this logic is tuned to any specific case's expected values.

`evaluate.mjs` is the only file permitted to read `ground-truth.json`'s `result` object.

## Known first-pass limitation: header-row ambiguity

`case-001`'s target page contains four rows shaped like `NNN <name>` (item codes `036`, `041`, `046`, and the target `020`) — some are `項`-level headers, some are `目`-level sub-item headers nested under a *different* item, and the generic parser cannot yet tell them apart. When more than one such row is found, `normalize.mjs` reports `result.itemName = null` rather than guessing, and `evaluate.mjs` adds a diagnostic check (`item_name_present_among_candidates`) confirming whether the *correct* row was still extracted and reconstructed correctly among the candidates — it was, for both current baselines. Resolving this ambiguity (e.g. via indentation/hierarchy-level detection) is future work, not something this first pass papers over.

## Adding a new engine

1. Add `scripts/document-understanding/adapters/<engine>/` that reads `fixtures/document-understanding/<caseId>/ground-truth.json` for case configuration (page index, source id/hash) only, extracts the target page, and writes `derived/document-understanding/<caseId>/<engine>.raw.json` matching the raw-artifact shape used by the existing adapters (`schemaVersion`, `engine`, `engineVersion`, `sourceId`, `sourceSha256`, `page`, `unit`, `lines: [{lineIndex, text}]`, `provenance`).
2. Register it in `benchmark/src/run.mjs`'s `ENGINES` list.
3. Pin the engine's exact version (a `package.json` dependency, a `requirements.txt`, or equivalent) the same way `scripts/pdf-extraction` pins `pdfjs-dist` and `pymupdf-baseline` pins `pymupdf`.
