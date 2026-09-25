# MinerU — investigation notes (not yet integrated)

Status: **not implemented**. Documentation-only investigation.

## Package

- PyPI: `mineru` (verified available: latest `4.0.7` at investigation time; the project was previously distributed as `magic-pdf`, also still published and verified available at `1.3.12`). Origin: OpenDataLab.
- Apache-2.0 licensed, full PDF-to-Markdown/JSON pipeline (layout detection + OCR + table recognition + formula recognition), not just a text/structure extractor.

## Installation method

```bash
pip install mineru[core]   # extras vary by release; a "core" or similar extra typically pulls in the model-serving deps
```

Model weights (layout detector, OCR recognizer, table-structure model, optionally a formula-recognition model) are downloaded separately, either automatically on first run or via an explicit model-download step depending on release — this is a heavier, multi-model download compared to Docling's single table-structure model.

## Runtime requirements

- CPU execution is supported but is explicitly the slower path; the project's own documentation and community usage strongly favor GPU (CUDA) for practical throughput, since it chains several vision models (layout + OCR + table + optionally formula).
- Model download size is substantially larger than Docling's (multiple models, commonly reported in the multi-GB range depending on which components are enabled).

## CPU / Mac M4 feasibility

Weakest fit of the three for this repository's environment:

- No CUDA on Apple Silicon; CPU-only inference across several chained vision models is likely to be noticeably slower than Docling for a single-document benchmark case.
- Heavier install and model-download footprint than Docling.
- Originates from and is most actively validated against Chinese-document workloads; Japanese-document layout/OCR accuracy has not been verified here and should not be assumed equivalent to its Chinese-document results.

## Expected outputs

Markdown and structured JSON (layout blocks, OCR text, table structure as HTML or a structured table representation), with bounding-box/page provenance per detected element — similar in spirit to Docling's output shape but produced by a different (OCR-centric rather than native-PDF-text-centric) pipeline. Because it includes OCR, it can also handle scanned/image-only pages, which neither the current PDF.js/PyMuPDF baselines nor Docling (which relies on the PDF's embedded text/layout where available) are designed for.

## Where it would plug into the benchmark interface

Same shape as the Docling adapter would: a `run.py` reading case config from `ground-truth.json`, invoking MinerU's pipeline on the locked PDF, and emitting the target page's structured output into the shared raw-artifact shape. Given the heavier runtime, this adapter would likely need its own explicit opt-in (e.g. a documented one-time model-download step) rather than being expected to "just work" the way `pymupdf-baseline` does.

## Recommendation

Not recommended as the next integration target. Its OCR-and-scanned-document strength is not needed for these already-text-native Digital Agency PDFs, and its CPU/Apple-Silicon story and install/model-download weight are both worse than Docling's for this repository's current needs. Worth revisiting if/when a scanned (non-text-layer) primary source needs to be benchmarked.
