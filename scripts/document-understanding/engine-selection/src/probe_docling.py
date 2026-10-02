"""Engine-selection probe: Docling native DoclingDocument (export_to_dict) for the probe page set.

Usage: <docling venv python> src/probe_docling.py <label> <default|no-ocr>
  default : DocumentConverter() unchanged (same as the research docling adapter; RapidOCR enabled)
  no-ocr  : PdfPipelineOptions(do_ocr=False), otherwise default (native text layer only)
Writes derived/document-understanding/engine-selection/docling-<mode>-<label>/<probeId>.json
(native structured document, not Markdown) plus _summary.json.
"""
import hashlib, json, pathlib, resource, sys, time
import docling
from importlib.metadata import version
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions

ROOT = pathlib.Path(__file__).resolve().parents[4]
label, mode = sys.argv[1], sys.argv[2]
cfg = json.loads((ROOT / "fixtures/document-understanding/engine-selection/probe-pages.json").read_text())
out_dir = ROOT / "derived/document-understanding/engine-selection" / f"docling-{mode}-{label}"
out_dir.mkdir(parents=True, exist_ok=True)

if mode == "default":
    converter = DocumentConverter()
elif mode == "no-ocr":
    opts = PdfPipelineOptions(); opts.do_ocr = False
    converter = DocumentConverter(format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=opts)})
else:
    raise SystemExit("mode must be default|no-ocr")

summary = {"engine": "docling", "version": version("docling"), "doclingCore": version("docling-core"), "mode": mode, "label": label, "pages": []}
checked = set()
for p in cfg["pages"]:
    pdf = ROOT / "sources/raw" / f"{p['sourceId']}.pdf"
    if p["sourceId"] not in checked:
        if hashlib.sha256(pdf.read_bytes()).hexdigest() != p["sourceSha256"]:
            raise SystemExit("sha mismatch")
        checked.add(p["sourceId"])
    n = p["pdfPageIndex"] + 1
    t0 = time.perf_counter()
    res = converter.convert(str(pdf), page_range=(n, n))
    secs = time.perf_counter() - t0
    d = res.document.export_to_dict()
    for pg in (d.get("pages") or {}).values():
        pg.pop("image", None)
    data = json.dumps({"probeId": p["probeId"], "pdfPageIndex": p["pdfPageIndex"], "status": str(res.status), "document": d}, ensure_ascii=False, sort_keys=True)
    (out_dir / f"{p['probeId']}.json").write_text(data)
    tables = d.get("tables", [])
    summary["pages"].append({"probeId": p["probeId"], "seconds": round(secs, 2), "texts": len(d.get("texts", [])),
        "tables": len(tables), "tableCells": [len(t["data"]["table_cells"]) for t in tables],
        "tableShape": [[t["data"]["num_rows"], t["data"]["num_cols"]] for t in tables],
        "groups": len(d.get("groups", [])), "sha256": hashlib.sha256(data.encode()).hexdigest()})
    print(summary["pages"][-1], flush=True)
summary["maxRssMB"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1048576)
(out_dir / "_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2))
print("maxRssMB", summary["maxRssMB"])
