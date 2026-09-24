# PDF Extraction

Workspace Phase 1D extraction layer.

This directory turns an already locked PDF binary into deterministic, page-aware text artifacts while preserving raw PDF.js text items separately from reconstructed lines.

## Boundary

```text
sources/source-lock.json
      ↓
sources/raw/<sourceId>.pdf  (git-ignored, hash-verified)
      ↓
pdfjs-dist 4.10.38
      ↓
raw text items + reconstructed lines + page text
```

This layer does **not** replace the historical curated request-ingestion fixtures. `npm run compare` measures whether those fixtures can be traced back to the locked PDF extraction.

## Commands

From this directory:

```bash
npm install
npm run extract
npm run compare
npm test
```

From the repository root after integration:

```bash
npm run sources:fetch
npm run extract
npm run extraction:compare
npm run extraction:test
```

## Output

Generated and git-ignored under `derived/pdf-extraction/`:

- `<sourceId>.items.jsonl` — raw PDF.js text items with coordinates
- `<sourceId>.lines.jsonl` — deterministic line reconstruction
- `<sourceId>.pages.txt` — human-readable debug representation
- `run-manifest.json` — page/item counts and output hashes

The authoritative provenance key is:

```text
source SHA-256 + PDF page index/number + extracted text/coordinates + extractor version + ordering version
```

Historical `Lxxx@Pyy` markers are retained only as legacy extraction metadata.
