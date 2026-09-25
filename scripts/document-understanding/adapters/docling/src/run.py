#!/usr/bin/env python3
"""docling adapter.

A third, independent Document Understanding engine, deliberately different in
kind from pdfjs-baseline and pymupdf-baseline: those two reconstruct flat text
lines from coordinates; Docling runs a learned layout + table-structure model
(TableFormer) and can emit actual table-cell objects (row/col indices, spans,
per-cell text), not just a text blob.

This adapter preserves Docling's native structured output (tables with cells,
and any non-table text blocks) rather than flattening everything to plain text
lines, per the task's explicit instruction not to discard useful structure
just to imitate the other two baselines' raw-artifact shape. A Docling-specific
normalizer (benchmark/src/normalize-docling.mjs) is responsible for turning
this structure into the shared benchmark result schema.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
CASES_DIR = ROOT / "fixtures" / "document-understanding"
DERIVED_DIR = ROOT / "derived" / "document-understanding"
RAW_DIR = ROOT / "sources" / "raw"

UNIT_RE = re.compile(r"\(単位[:：]?\s*([^)]+)\)")


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def find_unit_label(texts):
    for t in texts:
        m = UNIT_RE.search(t)
        if m:
            return m.group(1).strip()
    return None


def run(case_id: str) -> dict:
    import docling
    from docling.document_converter import DocumentConverter

    ground_truth = json.loads((CASES_DIR / case_id / "ground-truth.json").read_text(encoding="utf-8"))
    source_id = ground_truth["sourceId"]
    expected_sha256 = ground_truth["sourceSha256"]
    page_index = ground_truth["pdfPageIndex"]
    page_number = page_index + 1  # Docling's page_range is 1-based inclusive.

    pdf_path = RAW_DIR / f"{source_id}.pdf"
    if not pdf_path.exists():
        raise SystemExit(
            f"Missing {pdf_path}. Run `npm run sources:fetch` first to materialize "
            f"the locked binary without changing sources/source-lock.json."
        )

    actual_sha256 = sha256_of(pdf_path)
    if actual_sha256 != expected_sha256:
        raise SystemExit(
            f"Source hash mismatch for {source_id}\nexpected: {expected_sha256}\nactual:   {actual_sha256}"
        )

    converter = DocumentConverter()
    result = converter.convert(str(pdf_path), page_range=(page_number, page_number))
    doc = result.document

    tables = []
    for table_index, table in enumerate(doc.tables):
        cells = []
        for cell in table.data.table_cells:
            cells.append({
                "row": cell.start_row_offset_idx,
                "col": cell.start_col_offset_idx,
                "rowSpan": cell.row_span,
                "colSpan": cell.col_span,
                "text": cell.text,
            })
        tables.append({
            "tableIndex": table_index,
            "numRows": table.data.num_rows,
            "numCols": table.data.num_cols,
            "cells": cells,
        })

    non_table_texts = [t.text for t in doc.texts]
    all_cell_texts = [c["text"] for tbl in tables for c in tbl["cells"]]

    raw = {
        "schemaVersion": 1,
        "caseId": case_id,
        "engine": "docling",
        "engineVersion": docling.__version__,
        "orderingVersion": "docling-native-table-structure-v1",
        "sourceId": source_id,
        "sourceSha256": actual_sha256,
        "page": page_index,
        "unit": find_unit_label(non_table_texts + all_cell_texts),
        "markdown": doc.export_to_markdown(),
        "tables": tables,
        "texts": non_table_texts,
        "provenance": {
            "extractionMethod": "DocumentConverter.convert(page_range=(N,N)); doc.tables[*].data.table_cells",
            "note": (
                "Preserves Docling's native table-cell structure (row/col indices, spans, "
                "per-cell text) rather than flattening to plain text lines. Cell text order "
                "within a cell is Docling's own assembly, not re-sorted by this adapter; "
                "known reordering artifacts (e.g. reversed comma-groups in multi-token "
                "numeric cells) are handled deterministically in the normalizer, not here."
            ),
        },
    }

    out_path = DERIVED_DIR / case_id / "docling.raw.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(raw, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return raw


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: run.py <caseId>", file=sys.stderr)
        sys.exit(1)
    result = run(sys.argv[1])
    n_tables = len(result["tables"])
    n_cells = sum(len(t["cells"]) for t in result["tables"])
    print(
        f"RAW docling/{result['caseId']}: page={result['page']} "
        f"tables={n_tables} cells={n_cells} texts={len(result['texts'])} unit={result['unit']}"
    )
