# External Document Understanding Engine Survey

Date: 2026-09-26

This survey documents installation method, runtime requirements, model-download requirements, CPU/Mac M4 feasibility, expected outputs, and benchmark integration points for three candidate open/local Document Understanding engines: **Docling**, **MinerU**, and **PaddleOCR / PP-StructureV3**. None of the three has been installed or integrated in this pass, per the task's explicit scope (build the harness + one deterministic local baseline first). Package existence and current version were verified via `pip index versions` against the live PyPI index (not assumed from memory); architectural/runtime claims beyond that draw on each project's established public documentation and are marked accordingly where not independently re-verified here.

Full detail for each engine is in its own adapter directory:

- `scripts/document-understanding/adapters/docling/README.md`
- `scripts/document-understanding/adapters/mineru/README.md`
- `scripts/document-understanding/adapters/paddle/README.md`

## Verified package availability (via `pip index versions`, arm64 host)

| package | latest verified version |
|---|---|
| `docling` | 2.130.0 |
| `mineru` | 4.0.7 (predecessor `magic-pdf` 1.3.12 also available) |
| `paddleocr` | 3.7.0 |
| `paddlepaddle` | 3.3.1 |

## Summary comparison

| | Docling | MinerU | PaddleOCR / PP-StructureV3 |
|---|---|---|---|
| Extra framework needed | No (uses `torch`) | No (uses `torch`) | **Yes** — separate `paddlepaddle` framework |
| CPU-only feasible | Yes, documented common path | Yes, but slow (multi-model pipeline) | Yes, if a working arm64 wheel is available |
| Apple Silicon (M-series) track record | Good — standard PyTorch wheels | Weaker — GPU-oriented | Uncertain — historically lagging arm64 support |
| Model download weight | Moderate (one table-structure model) | Heavy (layout + OCR + table, optional formula) | Moderate–heavy (layout + table + OCR) |
| Native strength | Table structure recognition on text-native PDFs | End-to-end OCR pipeline, handles scanned/image PDFs | Multi-language OCR + layout, incl. Japanese |
| Best fit for this repo's PDFs | **Yes** — these are text-native, not scanned | Overkill — OCR strength unneeded here | Possible, but heavier install risk |

## Recommendation

**Docling first.** The task noted Docling as the likely first candidate and asked that this be verified rather than assumed; the verification here (package availability confirmed, dependency-footprint and platform-support comparison against the other two) confirms it. Rationale:

1. This repository's primary sources are text-native government PDFs, not scanned documents — MinerU's OCR-centric design and PaddleOCR's OCR focus solve a problem this corpus does not currently have.
2. Docling requires no additional deep-learning framework beyond `torch`, which is a lighter, better-attested dependency on Apple Silicon than standing up `paddlepaddle`.
3. Docling's native table-structure output (cells, rows, columns, reading order, with page/bbox provenance) maps more directly onto this benchmark's schema (`itemCode`/`expenseCode`/amount-triple association) than a flat-text baseline, and is a meaningfully different approach from the two baselines already implemented (which both reconstruct plain text lines, not table cells).

MinerU and PaddleOCR remain documented, ready-to-revisit options — MinerU specifically for a future scanned/image-only primary source, PaddleOCR if Docling's table recognition proves insufficient in practice.

## Next step if integrating Docling

1. `pip install docling` in a dedicated venv under `scripts/document-understanding/adapters/docling/`, pinned via `requirements.txt` (matching the `pymupdf-baseline` pattern).
2. Write `adapters/docling/src/run.py` per the plug-in point documented in `adapters/docling/README.md` — noting that Docling's table-cell-structured output will likely need either an extension to `benchmark/src/common.mjs`'s row-detection rules or a Docling-specific normalization path in `benchmark/src/normalize.mjs`, since it does not produce flat text lines the way the two current baselines do.
3. Run `npm run docbench` against `case-001` and compare Docling's evaluation results directly against the two existing baselines already on record in `evidence/document-understanding/case-001-results.json`.
