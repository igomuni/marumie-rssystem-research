#!/usr/bin/env python3
"""Independent, read-only audit for Wave 1 repaired S3 execution v2.

This intentionally does not import the executor.  It independently checks
immutable/v1 preservation, provenance closure, page scope, direct-tuple IDs,
and the emitted word-level header/row cluster evidence.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

SPEC = "batch-001-wave-1-s3-repair-v1"
NS = "s3r1"
V1 = {
    "authority-01-kunaicho": {
        "s3-repaired-v1/nodes.jsonl": "6d85ab08503e8495e36af72b0544b4dc3bafb6057359f2af3db4ee290bbb6156",
        "s3-repaired-v1/edges.jsonl": "7bb247babf7e1c8a90c5379dd1e640c1108706aa9fd9c9d769f63395cdf65cd3",
        "s3-repaired-v1/structural-interpretation-manifest.json": "4b95b682f3efc71f875dd37f32ed1fc93d3e886a50031a95bbd77001d474c80d",
        "s3-repaired-v1/repair-execution-manifest.json": "a6156fcd4500398adede65d51634714867a3b5183fa1ba6873b95ffda61eca39",
    },
    "authority-02-shugiin": {
        "s3-repaired-v1/nodes.jsonl": "16b2bcd1c6c5676b6cd3500951a4ad464fe7a1bd70c958deb22d37abbf3637ac",
        "s3-repaired-v1/edges.jsonl": "95318747f9f20157ffde7e060e693e1aa0c0a1fe9a95d4989b4371767d4e82e0",
        "s3-repaired-v1/structural-interpretation-manifest.json": "6b065f974604afa94e346710c80c5ad09dba69d6ac7bf3d8572b6e247ab5db3c",
        "s3-repaired-v1/repair-execution-manifest.json": "3e07e3dc8e5eac3ade89950301390e2417f7b2768decbee278b41590cd4e42f3",
    },
}

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load_jsonl(p): return [json.loads(x) for x in Path(p).read_text(encoding="utf-8").splitlines() if x]
def expected_id(kind, record):
    bits=[SPEC,record["sourceSha256"],record["fileId"],str(record["pdfPageIndex"]),kind,record["inferenceRule"],*sorted(record["supportingObservationIds"])]
    return f"{NS}-{kind}-{hashlib.sha256('\x1f'.join(bits).encode()).hexdigest()[:20]}"
def bbox(record):
    return record.get("geometry",{}).get("bbox")

def audit_authority(root, directory, spec):
    base=root/"fixtures/document-understanding/batch-001/authorities"/directory
    authority="kunaicho" if directory.endswith("kunaicho") else "shugiin"
    immutable={rel: sha(base/rel)==want for rel,want in spec["immutableBaseline"]["authorityArtifactHashes"][authority].items()}
    v1={rel: sha(base/rel)==want for rel,want in V1[directory].items()}
    observations={x["observationId"]:x for x in load_jsonl(base/"source-observations.jsonl")}
    repaired=base/"s3-repaired-v2"
    nodes=load_jsonl(repaired/"nodes.jsonl"); edges=load_jsonl(repaired/"edges.jsonl")
    by_id={x["nodeId"]:x for x in nodes}
    issues=[]; locators=0; ids=0; cluster_groups=0; cluster_failures=[]
    for record in [*nodes,*edges]:
        inferred=record.get("evidenceClass")=="structurally_inferred"
        if inferred:
            expected=expected_id(record.get("idPrimitive",record.get("nodeType")),record)
            actual=record.get("edgeId",record.get("nodeId"))
            ids+=1
            if actual!=expected: issues.append({"kind":"id","id":actual,"expected":expected})
            if not record.get("supportingObservationIds"): issues.append({"kind":"empty-support","id":actual})
        for loc in record.get("evidenceLocator",[]):
            locators+=1; source=observations.get(loc["observationId"])
            if not source or loc.get("sourceOrder")!=source.get("sourceOrder") or loc.get("bbox")!=bbox(source):
                issues.append({"kind":"locator","record":record.get("edgeId",record.get("nodeId")),"observationId":loc["observationId"]})
        for oid in record.get("supportingObservationIds",[]):
            source=observations.get(oid)
            if not source or any(record[k]!=source[k] for k in ("sourceSha256","fileId","pdfPageIndex")):
                issues.append({"kind":"support-identity","record":record.get("edgeId",record.get("nodeId")),"observationId":oid})
        if inferred and record.get("nodeType") in {"nestedStructure","boundedLocalTable"}:
            cluster_groups+=1; ri=record["ruleInput"]
            h=ri.get("headerXClusters",[]); rows=ri.get("rowXClusters",[]); matches=ri.get("headerToRowClusterMatches",[])
            good=len(h)>=2 and len(rows)>=2 and len(matches)>=2 and all(len(x)>=2 for x in matches)
            cluster_ids=[oid for c in h for oid in c.get("memberObservationIds",[])] + [oid for row in rows for c in row for oid in c.get("memberObservationIds",[])]
            if not good or not cluster_ids or any(oid not in observations for oid in cluster_ids):
                cluster_failures.append(record["nodeId"])
    endpoint_fail=[]; cross_page=0; cross_file=0; outer_local=0
    for edge in edges:
        a,b=by_id.get(edge["fromNodeId"]),by_id.get(edge["toNodeId"])
        if not a or not b: endpoint_fail.append(edge["edgeId"]); continue
        if a["fileId"]!=b["fileId"]: cross_file+=1
        if a["pdfPageIndex"]!=b["pdfPageIndex"]: cross_page+=1
        if {a.get("nodeType"),b.get("nodeType")} & {"outerLedger"} and {a.get("nodeType"),b.get("nodeType")} & {"nestedStructure","boundedLocalTable"}: outer_local+=1
    hyakuman=[]
    if authority=="shugiin":
        manifest=json.loads((repaired/"structural-interpretation-manifest.json").read_text())
        hyakuman=manifest["a02HyakumanYenReconciliation"]
        source_count=sum(1 for x in observations.values() if x["observationKind"]=="textLine" and "百万円" in x.get("raw",{}).get("engineNativeText",""))
        if source_count!=46 or len(hyakuman)!=46 or len({x["observationId"] for x in hyakuman})!=46:
            issues.append({"kind":"hyakuman-reconciliation","sourceCount":source_count,"treatmentCount":len(hyakuman)})
    return {
        "authorityId":authority,"immutableBaselineHashPass":all(immutable.values()),"reviewedV1HashPass":all(v1.values()),
        "v2Hashes":{p.name:sha(p) for p in sorted(repaired.iterdir()) if p.is_file()},"nodeCount":len(nodes),"edgeCount":len(edges),
        "nodeTypes":dict(sorted(Counter(x.get("nodeType") for x in nodes).items())),"statuses":dict(sorted(Counter(x.get("structuralStatus","source_observed") for x in nodes).items())),
        "locatorCount":locators,"exactLocatorSourceOrderAndBBoxFailures":sum(x["kind"]=="locator" for x in issues),"directTupleRecordsChecked":ids,"directTupleIdFailures":sum(x["kind"]=="id" for x in issues),
        "clusterGroupsChecked":cluster_groups,"clusterEvidenceFailures":cluster_failures,"endpointResolutionFailures":endpoint_fail,"derivedCrossPageEdgeCount":cross_page,"derivedCrossFileEdgeCount":cross_file,"outerLocalDirectEdgeCount":outer_local,
        "a02HyakumanTreatments":dict(sorted(Counter(x["treatment"] for x in hyakuman).items())),"issues":issues,
    }

def main():
    p=argparse.ArgumentParser(); p.add_argument("--repo",type=Path,default=Path.cwd()); args=p.parse_args(); root=args.repo.resolve()
    spec=json.loads((root/"fixtures/document-understanding/batch-001/wave-1-s3-structural-repair-spec.json").read_text())
    results=[audit_authority(root,"authority-01-kunaicho",spec),audit_authority(root,"authority-02-shugiin",spec)]
    print(json.dumps({"schemaVersion":1,"audit":"independent-v2-execution-audit","specVersion":SPEC,"authorities":results,"pass":all(not a["issues"] and not a["endpointResolutionFailures"] and not a["clusterEvidenceFailures"] and a["immutableBaselineHashPass"] and a["reviewedV1HashPass"] for a in results)},ensure_ascii=False,sort_keys=True,indent=2))

if __name__=="__main__": main()
