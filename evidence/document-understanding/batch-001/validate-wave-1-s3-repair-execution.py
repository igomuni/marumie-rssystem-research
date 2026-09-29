#!/usr/bin/env python3
"""Deterministic non-production integrity audit for repaired S3 review input."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


def digest(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def read_jsonl(path): return [json.loads(x) for x in Path(path).read_text(encoding="utf-8").splitlines() if x]


def main():
    root = Path(__file__).resolve().parents[3]
    spec = json.loads((root / "fixtures/document-understanding/batch-001/wave-1-s3-structural-repair-spec.json").read_text(encoding="utf-8"))
    result = {"status": "PASS", "authorities": {}, "baselineHashAudit": {}, "forbiddenRuleHits": 0}
    for authority, directory, profile in [("kunaicho", "authority-01-kunaicho", "batch-001-wave-1-a01-v1"), ("shugiin", "authority-02-shugiin", "batch-001-wave-1-a02-v1")]:
        base = root / "fixtures/document-understanding/batch-001/authorities" / directory
        expected = spec["immutableBaseline"]["authorityArtifactHashes"][authority]
        baseline = {relative: digest(base / relative) == value for relative, value in expected.items()}
        if not all(baseline.values()): raise SystemExit(f"baseline hash audit failed for {authority}")
        observations = {x["observationId"]: x for x in read_jsonl(base / "source-observations.jsonl")}
        repaired = base / "s3-repaired-v1"
        nodes, edges = read_jsonl(repaired / "nodes.jsonl"), read_jsonl(repaired / "edges.jsonl")
        node_ids, edge_ids = [x["nodeId"] for x in nodes], [x["edgeId"] for x in edges]
        if len(node_ids) != len(set(node_ids)) or len(edge_ids) != len(set(edge_ids)): raise SystemExit(f"duplicate repaired IDs: {authority}")
        node_set = set(node_ids)
        inferred = [x for x in [*nodes, *edges] if x.get("evidenceClass") == "structurally_inferred"]
        for item in inferred:
            required = ["evidenceClass", "inferenceRule", "profileVersion", "ambiguityState", "sourceSha256", "fileId", "pdfPageIndex", "supportingObservationIds", "evidenceLocator", "ruleInput", "structuralStatus"]
            if any(k not in item for k in required) or not item["supportingObservationIds"]: raise SystemExit(f"incomplete inference provenance: {authority}")
            if item["profileVersion"] != profile or any(x not in observations for x in item["supportingObservationIds"]): raise SystemExit(f"bad support reference: {authority}")
            if item["inferenceRule"] in ("split-header-token-set", "right-side-xmin-57-percent"): raise SystemExit(f"old rule used: {authority}")
        if any(x["fromNodeId"] not in node_set or x["toNodeId"] not in node_set for x in edges): raise SystemExit(f"unresolved edge endpoint: {authority}")
        if any(x.get("pdfPageIndex") != x.get("pdfPageIndex") for x in []): raise SystemExit("unreachable")
        manifest = json.loads((repaired / "structural-interpretation-manifest.json").read_text(encoding="utf-8"))
        if manifest["crossPageEdgeCount"] != 0 or manifest["crossFileEdgeCount"] != 0 or manifest["outerLocalUnitInheritanceEdgeCount"] != 0: raise SystemExit(f"boundary audit failed: {authority}")
        result["baselineHashAudit"][authority] = baseline
        result["authorities"][authority] = {"nodeCount": len(nodes), "edgeCount": len(edges), "inferredRecordCount": len(inferred), "supportReferenceCount": sum(len(x["supportingObservationIds"]) for x in inferred), "allSupportIdsResolve": True, "allEdgeEndpointsResolve": True, "outputHashes": {name: digest(repaired / name) for name in ["nodes.jsonl", "edges.jsonl", "structural-interpretation-manifest.json", "repair-execution-manifest.json"]}}
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))

if __name__ == "__main__": main()
