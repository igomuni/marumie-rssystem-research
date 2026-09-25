# docling — investigation notes (not yet integrated)

Status: **not implemented**. This is a documentation-only investigation for the recommended second engine to add after the baselines.

## Package

- PyPI: `docling` (verified available: latest `2.130.0` at investigation time, active releases going back to `0.1.0`).
- Pure Python, MIT-licensed (IBM / Deep Search project, formerly `docling` under the `DS4SD` org).

## Installation method

```bash
pip install docling
```

On first run against a PDF, Docling downloads its own layout-analysis and `TableFormer` table-structure-recognition models (PyTorch, distributed via Hugging Face Hub) to a local cache directory. No separate framework install (unlike PaddleOCR's `paddlepaddle`) is required beyond `torch`, which is pulled in as a dependency.

## Runtime requirements

- CPU-only execution is supported and is Docling's documented common path; PyTorch's Apple Silicon (`mps`) backend can accelerate it further, but is not required for correctness.
- No GPU/CUDA requirement.
- Model download: on the order of a few hundred MB for the layout + table-structure models (one-time download to Docling's model cache).

## CPU / Mac M4 feasibility

Best fit of the three candidates for this repository's environment:

- Pure Python + PyTorch stack, no separate compiled framework to install (unlike `paddlepaddle`, which has historically had a rockier story on Apple Silicon).
- Designed and commonly benchmarked for CPU-only inference on a single document.
- `arm64` wheels for its dependencies (PyTorch, etc.) are broadly available.

## Expected outputs

Docling produces a `DoclingDocument` object exportable to Markdown, JSON, or HTML, with:
- reading-order-aware text blocks,
- detected table regions with row/column/cell structure (via TableFormer), not just a text blob,
- page/bounding-box provenance per element (so a "which page/coordinates did this come from" answer is available, matching this benchmark's provenance requirements).

## Where it would plug into the benchmark interface

`scripts/document-understanding/adapters/docling/src/run.py` (not yet written) would:
1. Read `fixtures/document-understanding/<caseId>/ground-truth.json` for `sourceId`/`sourceSha256`/`pdfPageIndex` (case config only, as the existing adapters do).
2. Open the locked, hash-verified PDF from `sources/raw/`.
3. Run Docling's document converter, restricted to (or filtered down to) the target page.
4. Emit the target page's Docling table-structure output as `lines` in the shared raw-artifact shape — likely one entry per detected table cell/text block rather than one entry per plain text line, which would require `benchmark/src/normalize.mjs`'s row-detection rules to be extended (or a Docling-specific normalization path added) to consume structured cells instead of re-parsing flat text with regex. This is a real design point to resolve during integration, not a drop-in swap.

## Recommendation

**Docling is the recommended next engine to integrate**, consistent with the task's hint, now verified rather than assumed: it is the only one of the three with (a) a pure-Python/PyTorch install path, (b) no separate heavyweight framework dependency, and (c) native table-structure output that maps more directly onto this benchmark's row/column requirements than a flat-text baseline.
