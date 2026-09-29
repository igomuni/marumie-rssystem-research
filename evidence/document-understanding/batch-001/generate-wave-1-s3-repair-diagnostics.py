#!/usr/bin/env python3
"""Non-production design diagnostic for the frozen Wave 1 S3 repair spec.

Reads immutable S2 JSONL only.  It creates diagnostic evidence; it neither
creates nor changes an S3 graph.
"""
import hashlib
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "evidence/document-understanding/batch-001/wave-1-s3-repair-design-diagnostics.json"
AUTHORITIES = {
    "authority-01-kunaicho": {"id": "kunaicho", "source": "ffab15073beb2411d9396f7ca0cbb1ce33ccdf99be05e6d0d88e29366912e261"},
    "authority-02-shugiin": {"id": "shugiin", "source": "30d0dfc363a1f4f7e37b64a0059b48c2f03f13f997eb251e7ef5acaabd37c435"},
}

def load_jsonl(path):
    return [json.loads(line) for line in path.read_text().splitlines()]

def main():
    result = {"artifactType": "wave-1-s3-repair-design-diagnostics", "stage": "design_only", "authorities": []}
    for directory, meta in AUTHORITIES.items():
        base = ROOT / "fixtures/document-understanding/batch-001/authorities" / directory
        observations = load_jsonl(base / "source-observations.jsonl")
        by_order = {tuple(sorted(item["sourceOrder"].items())): item for item in observations}
        per_page = defaultdict(list)
        for item in observations:
            per_page[item["pdfPageIndex"]].append(item)
        units = []
        page_signals = []
        for page in sorted(per_page):
            lines = [item for item in per_page[page] if item["observationKind"] == "textLine"]
            text = "\n".join(item["raw"]["engineNativeText"] for item in lines)
            page_signals.append({
                "pdfPageIndex": page,
                "lineCount": len(lines),
                "headerTokenPresence": {token: token in text for token in ["要求", "番号", "備", "考"]},
                "unitLineCount": sum("単位" in item["raw"]["engineNativeText"] for item in lines),
            })
            for line in lines:
                if "百万円" not in line["raw"]["engineNativeText"]:
                    continue
                order = line["sourceOrder"]
                block_key = tuple(sorted({k: order[k] for k in ("page", "flow", "block")}.items()))
                block = by_order.get(block_key)
                units.append({
                    "pdfPageIndex": page,
                    "observationId": line["observationId"],
                    "sourceOrder": order,
                    "geometry": line["geometry"],
                    "rawText": line["raw"]["engineNativeText"],
                    "containingBlockObservationId": block["observationId"] if block else None,
                    "containingBlockGeometry": block["geometry"] if block else None,
                    "containingBlockTextSha256": hashlib.sha256(block["raw"]["engineNativeText"].encode()).hexdigest() if block else None,
                    "proposedTreatment": "localTableAnchorCandidate; no unit inheritance outside a future same-page bounded local structure",
                })
        result["authorities"].append({
            "authorityId": meta["id"],
            "sourceSha256": meta["source"],
            "s2ObservationPath": str(base.relative_to(ROOT) / "source-observations.jsonl"),
            "pageSignals": page_signals,
            "hundredMillionYenOccurrences": units,
            "hundredMillionYenOccurrenceCount": len(units),
        })
    OUT.write_text(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n")

if __name__ == "__main__":
    main()
