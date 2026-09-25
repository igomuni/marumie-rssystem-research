# pymupdf-baseline

A second, independent Document Understanding baseline engine, pinned to `pymupdf==1.28.2`. Deliberately isolated from `scripts/pdf-extraction` (PDF.js): it re-opens the same locked, hash-verified raw PDF binary directly and uses PyMuPDF's own built-in text reconstruction, so the benchmark harness can compare two genuinely different extraction engines against the same ground truth.

## Setup

```bash
cd scripts/document-understanding/adapters/pymupdf-baseline
python3 -m venv .venv
./.venv/bin/pip install -r requirements.txt
```

`.venv/` is git-ignored; `requirements.txt` pins the exact version for reproducibility, the same way `scripts/pdf-extraction/package.json` pins `pdfjs-dist`.

## Run

Requires the locked source binary to be materialized first (never modifies `sources/source-lock.json`):

```bash
npm run sources:fetch
./.venv/bin/python3 src/run.py case-001
```

This writes `derived/document-understanding/case-001/pymupdf-baseline.raw.json` (git-ignored generated output).

## What it does and does not do

- Opens the exact PDF binary referenced by the case's `sourceSha256` and re-verifies the hash itself (fails loudly on mismatch, independent of any other tool's verification).
- Extracts the target page's text via `page.get_text("text")` — PyMuPDF's own reading-order line reconstruction, not a custom coordinate-clustering algorithm.
- Does not attempt table/column structure detection beyond what `get_text("text")` provides natively.
- Does not use an LLM or any semantic repair step.
