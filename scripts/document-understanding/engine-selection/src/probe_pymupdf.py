"""Engine-selection probe: PyMuPDF native text representations for the probe page set.

Usage: <pymupdf venv python> src/probe_pymupdf.py <label>
Writes derived/document-understanding/engine-selection/pymupdf-<label>/<probeId>.json with the
native words / blocks / dict / rawdict outputs as produced (no merge or repair), plus _summary.json.
"""
import hashlib, json, pathlib, resource, sys, time
import pymupdf

ROOT = pathlib.Path(__file__).resolve().parents[4]
label = sys.argv[1]
cfg = json.loads((ROOT / "fixtures/document-understanding/engine-selection/probe-pages.json").read_text())
out_dir = ROOT / "derived/document-understanding/engine-selection" / f"pymupdf-{label}"
out_dir.mkdir(parents=True, exist_ok=True)

def strip_rawdict(d):
    # keep per-char c/bbox/origin; drop image payloads
    for b in d["blocks"]:
        b.pop("image", None)
    return d

docs = {}
summary = {"engine": "pymupdf", "version": pymupdf.VersionBind, "label": label, "pages": []}
for p in cfg["pages"]:
    sid = p["sourceId"]
    if sid not in docs:
        pdf = ROOT / "sources/raw" / f"{sid}.pdf"
        if hashlib.sha256(pdf.read_bytes()).hexdigest() != p["sourceSha256"]:
            raise SystemExit(f"sha mismatch {sid}")
        t0 = time.perf_counter(); docs[sid] = (pymupdf.open(pdf), time.perf_counter() - t0)
    doc, open_s = docs[sid]
    page = doc[p["pdfPageIndex"]]
    timings = {}
    t0 = time.perf_counter(); words = page.get_text("words", sort=False); timings["words"] = time.perf_counter() - t0
    t0 = time.perf_counter(); blocks = page.get_text("blocks", sort=False); timings["blocks"] = time.perf_counter() - t0
    t0 = time.perf_counter(); dct = page.get_text("dict", sort=False); timings["dict"] = time.perf_counter() - t0
    t0 = time.perf_counter(); raw = strip_rawdict(page.get_text("rawdict", sort=False)); timings["rawdict"] = time.perf_counter() - t0
    for b in dct["blocks"]:
        b.pop("image", None)
    out = {"probeId": p["probeId"], "pdfPageIndex": p["pdfPageIndex"], "pymupdfVersion": pymupdf.VersionBind,
           "rect": list(page.rect), "rotation": page.rotation, "words": words, "blocks": blocks, "dict": dct, "rawdict": raw}
    data = json.dumps(out, ensure_ascii=False)
    (out_dir / f"{p['probeId']}.json").write_text(data)
    summary["pages"].append({"probeId": p["probeId"], "words": len(words), "blocks": len(blocks),
        "spans": sum(len(l["spans"]) for b in dct["blocks"] if b.get("type") == 0 for l in b["lines"]),
        "ms": {k: round(v * 1000, 1) for k, v in timings.items()}, "docOpenMs": round(open_s * 1000, 1),
        "sha256": hashlib.sha256(data.encode()).hexdigest()})
summary["maxRssMB"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1048576)
(out_dir / "_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2))
for x in summary["pages"]:
    print(x["probeId"], x["words"], x["blocks"], x["spans"], x["ms"])
print("maxRssMB", summary["maxRssMB"])
