# docling

Status: **implemented**. Pinned to `docling==2.130.0`.

A third, independent Document Understanding engine — unlike `pdfjs-baseline` and `pymupdf-baseline` (which both reconstruct flat text lines from coordinates), Docling runs a learned layout + table-structure model (TableFormer) and can emit real table-cell objects: row/column indices, spans, and per-cell text.

## Setup

```bash
cd scripts/document-understanding/adapters/docling
python3 -m venv .venv
./.venv/bin/pip install -r requirements.txt
```

`.venv/` is git-ignored. On first run, Docling downloads its layout/table-structure models (PyTorch, via Hugging Face Hub) plus a small RapidOCR fallback model set (~130MB combined, observed) to `~/.cache/huggingface` and the venv's own `rapidocr/models/` directory — neither of which is part of this repository or committed.

## Run

Requires the locked source binary to be materialized first (never modifies `sources/source-lock.json`):

```bash
npm run sources:fetch
./.venv/bin/python3 src/run.py case-001
```

This writes `derived/document-understanding/case-001/docling.raw.json` (git-ignored generated output) containing Docling's native table-cell structure and Markdown export — not flattened text lines.

## What was actually observed (case-001, Digital Agency FY2024 request PDF, page index 11)

Verified empirically before writing the adapter/normalizer, not assumed:

- Docling **detected a real table** spanning the page body (21 rows × 14 columns, 119 cells), despite this table having no visible borders in the PDF (whitespace/column-alignment only). This was not a given — TableFormer is commonly trained mostly on bordered tables.
- The item-name and expense-name cells came back **cleanly separated** from the neighboring annotation-text column that both `pdfjs-baseline` and `pymupdf-baseline` conflated into the same line (the `（要求要旨）...` text). This is a genuine capability difference, not a normalization trick — see `reports/document-understanding/case-001-evaluation.md`.
- Multi-comma-group numeric cells (e.g. `481,188,232`) came back with their whitespace-separated groups in **reversed order** (`"232 188, 481,"`), consistently across every multi-group numeric cell checked on this page. `benchmark/src/normalize-docling.mjs` reverses the token order deterministically to recover the value — a general, documented, engine-specific rule verified against multiple independent cells, not a correction fitted to this case's expected numbers.
- The `△` decrease-sign glyph came back in its **own separate cell**, distinct from the magnitude cell — actually easier to detect reliably than in the flat-text baselines.
- The request-number column (e.g. `4`) had **no corresponding cell at all** for the target expense row — a genuine, unresolved extraction gap, recorded as `requestNo: null`, not guessed.

## Adapter boundary

`src/run.py`:
1. Reads `fixtures/document-understanding/<caseId>/ground-truth.json` for `sourceId`/`sourceSha256`/`pdfPageIndex` only (case configuration, never the expected `result`).
2. Re-verifies the locked PDF's SHA-256 itself.
3. Runs `DocumentConverter().convert(pdf_path, page_range=(N, N))` restricted to the target page.
4. Writes Docling's native `tables` (cells with row/col/span/text), non-table `texts`, and a full Markdown export to the raw artifact — no flattening to a `lines` array, per the task's instruction to preserve useful structure rather than imitate the other baselines' shape.

`scripts/document-understanding/benchmark/src/normalize-docling.mjs` (not `normalize.mjs`) turns this into the shared benchmark result schema:
- Finds item-code (`\d{3}\s+...`) and expense-code (`\d{2}-\d{2}\s+...`) label cells anywhere in the table.
- For each label cell, scans cells to its right in the same row for a previous/current/delta amount triple (skipping unrelated columns, e.g. the annotation-text column), and to its left for a request-number cell.
- Applies the two general Docling-specific rules above (CJK wrap-space closing, numeric-token-group reversal) — nothing case-specific.
- `evaluate.mjs` is **unmodified**: it only consumes the `{ result, candidates }` shape both normalizers produce, and remains the only file permitted to read ground truth values.

## Known limitation carried over

Like both baselines, this page contains four structurally-identical `NNN <name>` label cells (item codes `020`, `036`, `041`, `046`) at different hierarchy levels, and Docling's table structure does not by itself distinguish which is the target `項`-level header — the same ambiguity persists (see `item_name_present_among_candidates` in the evaluation report).
