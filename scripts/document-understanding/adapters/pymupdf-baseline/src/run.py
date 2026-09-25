#!/usr/bin/env python3
"""pymupdf-baseline adapter.

A second, independent Document Understanding baseline, deliberately isolated
from the existing PDF.js extractor (scripts/pdf-extraction). It re-opens the
same locked, hash-verified raw PDF binary and uses PyMuPDF's own text
reconstruction (page.get_text("text")) rather than reusing any PDF.js output.

This does not repair or reinterpret extracted text with an LLM or any
heuristic beyond PyMuPDF's own built-in line reconstruction.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[5]
CASES_DIR = ROOT / "fixtures" / "document-understanding"
DERIVED_DIR = ROOT / "derived" / "document-understanding"
RAW_DIR = ROOT / "sources" / "raw"

UNIT_RE = re.compile(r"\(単位[:：]?\s*([^)]+)\)")


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def find_unit_label(lines):
    for line in lines:
        m = UNIT_RE.search(line)
        if m:
            return m.group(1).strip()
    return None


def run(case_id: str) -> dict:
    ground_truth = json.loads((CASES_DIR / case_id / "ground-truth.json").read_text(encoding="utf-8"))
    source_id = ground_truth["sourceId"]
    expected_sha256 = ground_truth["sourceSha256"]
    page_index = ground_truth["pdfPageIndex"]

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

    doc = pymupdf.open(pdf_path)
    page = doc[page_index]
    # sort=True asks PyMuPDF for top-to-bottom, left-to-right reading order
    # rather than raw content-stream draw order. Without it, spans come back
    # in an arbitrary order unrelated to visual layout, which would make this
    # an unfair/uninteresting baseline (comparing "no reading-order effort" to
    # PDF.js's coordinate-based reconstruction, not comparing engine quality).
    text = page.get_text("text", sort=True)
    raw_lines = [line.strip() for line in text.split("\n") if line.strip() != ""]
    lines = [{"lineIndex": i, "text": line} for i, line in enumerate(raw_lines)]

    raw = {
        "schemaVersion": 1,
        "caseId": case_id,
        "engine": "pymupdf",
        "engineVersion": pymupdf.__version__,
        "orderingVersion": "get_text-text-mode-sort-true-v1",
        "sourceId": source_id,
        "sourceSha256": actual_sha256,
        "page": page_index,
        "unit": find_unit_label(raw_lines),
        "lines": lines,
        "provenance": {
            "extractionMethod": "page.get_text('text', sort=True)",
            "note": (
                "Uses PyMuPDF's own built-in reading-order text reconstruction, "
                "independent of the PDF.js-based extractor in scripts/pdf-extraction. "
                "sort=True requests top-to-bottom/left-to-right ordering; PyMuPDF still "
                "has no column/table structure detection, so a two-column layout at the "
                "same visual row can still be concatenated onto one output line."
            ),
        },
    }

    out_path = DERIVED_DIR / case_id / "pymupdf-baseline.raw.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(raw, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return raw


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: run.py <caseId>", file=sys.stderr)
        sys.exit(1)
    result = run(sys.argv[1])
    print(f"RAW pymupdf-baseline/{result['caseId']}: page={result['page']} lines={len(result['lines'])} unit={result['unit']}")
