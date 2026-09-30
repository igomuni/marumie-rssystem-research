#!/usr/bin/env python3
"""Independent, review-only audit for the Wave 1 s3r1 repair output.

It intentionally does not import the executor.  It recomputes identity,
provenance, graph-boundary, and geometry checks from immutable S2 records.
"""
from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

SPEC_VERSION = "batch-001-wave-1-s3-repair-v1"
OUTER_RULE = "s3-repair-v1:localized-outer-ledger-header"
LOCAL_RULE = "s3-repair-v1:same-page-bounded-structural-group"
STATUSES = {"structurally_supported", "structurally_ambiguous", "unclassified", "representation_limited", "prohibited_cross_page", "profile_contradiction"}


def digest(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def load(path): return json.loads(Path(path).read_text(encoding="utf-8"))
def jsonl(path): return [json.loads(x) for x in Path(path).read_text(encoding="utf-8").splitlines() if x]
def compact(record): return "".join(record.get("raw", {}).get("engineNativeText", "").split())
def bbox(record):
    value = record.get("geometry", {}).get("bbox")
    if not value: return None
    return tuple(float(value[k]) for k in ("xMin", "yMin", "xMax", "yMax"))
def bbox_union(records):
    values = [bbox(x) for x in records if bbox(x)]
    return [min(x[0] for x in values), min(x[1] for x in values), max(x[2] for x in values), max(x[3] for x in values)] if values else None
def equal_bbox(a, b): return a is None and b is None or a is not None and b is not None and all(abs(float(x)-float(y)) < 0.000001 for x,y in zip(a,b))


def stable_node_id(item):
    rule = item.get("inferenceRule", "source-observed-page")
    parts = [SPEC_VERSION, item["sourceSha256"], item["fileId"], str(item["pdfPageIndex"]), item["nodeType"], rule, *sorted(item["supportingObservationIds"])]
    return "s3r1-%s-%s" % (item["nodeType"], hashlib.sha256("\x1f".join(parts).encode()).hexdigest()[:20])


def stable_edge_id(item):
    parts = [SPEC_VERSION, item["fromNodeId"], item["toNodeId"], item.get("inferenceRule", ""), *sorted(item["supportingObservationIds"])]
    return "s3r1-edge-%s" % hashlib.sha256("\x1f".join(parts).encode()).hexdigest()[:20]


def max_line_height(observations, page):
    return max((bbox(x)[3]-bbox(x)[1] for x in observations.values() if x["pdfPageIndex"] == page and x["observationKind"] == "textLine" and bbox(x)), default=0)


def line_x_clusters(records, tolerance):
    xs = sorted(bbox(x)[0] for x in records if bbox(x))
    clusters = []
    for x in xs:
        if not clusters or x - clusters[-1][-1] > tolerance:
            clusters.append([x])
        else: clusters[-1].append(x)
    return [sum(c)/len(c) for c in clusters]


def matching_x_count(left, right, tolerance):
    return sum(1 for x in left if any(abs(x-y) <= tolerance for y in right))


def audit_authority(root, spec, authority, directory, expected_profile):
    base = root / "fixtures/document-understanding/batch-001/authorities" / directory
    expected_hashes = spec["immutableBaseline"]["authorityArtifactHashes"][authority]
    immutable = {name: digest(base / name) == value for name,value in expected_hashes.items()}
    observations = {x["observationId"]: x for x in jsonl(base / "source-observations.jsonl")}
    output = base / "s3-repaired-v1"
    nodes, edges = jsonl(output / "nodes.jsonl"), jsonl(output / "edges.jsonl")
    exceptions, closure = [], {"inferredRecords": 0, "nonemptySupport": 0, "resolvedSupport": 0, "locatorIdsMatch": 0, "locatorGeometryMatches": 0, "locatorSourceOrderMatches": 0, "validRuleInput": 0}
    node_ids, edge_ids = [x["nodeId"] for x in nodes], [x["edgeId"] for x in edges]
    if len(node_ids) != len(set(node_ids)): exceptions.append("duplicate-node-id")
    if len(edge_ids) != len(set(edge_ids)): exceptions.append("duplicate-edge-id")
    node_map = {x["nodeId"]:x for x in nodes}
    cross_page = cross_file = unit_inheritance = endpoint_failures = 0
    for edge in edges:
        parent, child = node_map.get(edge["fromNodeId"]), node_map.get(edge["toNodeId"])
        if not parent or not child:
            endpoint_failures += 1; continue
        cross_page += parent["pdfPageIndex"] != child["pdfPageIndex"]
        cross_file += parent["fileId"] != child["fileId"]
        unit_inheritance += {parent["nodeType"], child["nodeType"]} & {"outerLedger", "boundedLocalTable", "nestedStructure"} == {"outerLedger", "boundedLocalTable"}
    for record in [*nodes, *edges]:
        inferred = record.get("evidenceClass") == "structurally_inferred"
        if inferred:
            closure["inferredRecords"] += 1
            required = ["inferenceRule", "profileVersion", "ambiguityState", "sourceSha256", "fileId", "pdfPageIndex", "supportingObservationIds", "evidenceLocator", "ruleInput", "structuralStatus"]
            if any(x not in record for x in required) or not record["supportingObservationIds"]:
                exceptions.append("missing-required-inference-field:" + record.get("nodeId",record.get("edgeId","unknown")))
                continue
            closure["nonemptySupport"] += 1
            supports = [observations.get(x) for x in record["supportingObservationIds"]]
            if any(x is None for x in supports):
                exceptions.append("unresolved-support:" + record.get("nodeId",record.get("edgeId","unknown"))); continue
            if any(x["sourceSha256"] != record["sourceSha256"] or x["fileId"] != record["fileId"] or x["pdfPageIndex"] != record["pdfPageIndex"] for x in supports):
                exceptions.append("support-source-page-mismatch:" + record.get("nodeId",record.get("edgeId","unknown"))); continue
            closure["resolvedSupport"] += 1
            locator_by_id = {x["observationId"]:x for x in record["evidenceLocator"]}
            if set(locator_by_id) != set(record["supportingObservationIds"]):
                exceptions.append("locator-id-mismatch:" + record.get("nodeId",record.get("edgeId","unknown"))); continue
            closure["locatorIdsMatch"] += 1
            if not all(equal_bbox(locator_by_id[x]["bbox"], bbox(observations[x])) for x in locator_by_id):
                exceptions.append("locator-geometry-mismatch:" + record.get("nodeId",record.get("edgeId","unknown"))); continue
            closure["locatorGeometryMatches"] += 1
            if not all(locator_by_id[x]["sourceOrder"] == observations[x]["sourceOrder"] for x in locator_by_id):
                exceptions.append("locator-source-order-mismatch:" + record.get("nodeId",record.get("edgeId","unknown"))); continue
            closure["locatorSourceOrderMatches"] += 1
            if record["profileVersion"] != expected_profile or record["structuralStatus"] not in STATUSES:
                exceptions.append("profile-or-status-mismatch:" + record.get("nodeId",record.get("edgeId","unknown"))); continue
            closure["validRuleInput"] += 1
        if record.get("nodeId") and record["nodeId"] != stable_node_id(record): exceptions.append("node-id-contract-mismatch:" + record["nodeId"])
        if record.get("edgeId") and record["edgeId"] != stable_edge_id(record): exceptions.append("edge-id-nondeterministic:" + record["edgeId"])
    outer_results, local_results = [], []
    required_sets = [set("要求番号"), set("事項"), set("前年度予算額"), set("概算要求額"), set("備考")]
    for node in nodes:
        if node.get("nodeType") == "outerLedger":
            r = node["ruleInput"]; groups = r.get("headerGroups", [])
            group_records = [[observations[x] for x in group] for group in groups]
            groups_present = len(groups) == 5 and all(set("".join(compact(x) for x in g)) >= need for g,need in zip(group_records,required_sets))
            group_boxes = [bbox_union(g) for g in group_records]
            ordered = all(group_boxes[i][0] < group_boxes[i+1][0] for i in range(4)) if len(group_boxes)==5 else False
            height = max_line_height(observations,node["pdfPageIndex"])
            local = all(box[3]-box[1] <= 2*height+0.000001 for box in group_boxes if box)  # root-window consequence tested independently
            row_ids = r.get("repeatingRowBands", [])
            row_records = [[observations[x] for x in band] for band in row_ids]
            repeats = len(row_records) >= 2 and all(len(line_x_clusters(x,height)) >= 2 for x in row_records[:2])
            raw_sequences=["".join(compact(x) for x in group) for group in group_records]
            outer_results.append({"nodeId":node["nodeId"],"page":node["pdfPageIndex"],"headerGlyphSetsPresent":groups_present,"leftToRight":ordered,"localHeaderGeometry":local,"twoConcreteRowBands":repeats,"rawGlyphSequences":raw_sequences,"literalHorizontalPhraseSequence":raw_sequences == ["要求番号","事項","前年度予算額","概算要求額","備考"],"reviewStatus":"supported-by-recorded-S2-inputs" if all([groups_present,ordered,local,repeats]) else "rule-input-defect"})
        if node.get("nodeType") in {"nestedStructure","boundedLocalTable"}:
            r=node["ruleInput"]; block=observations[r["candidateBlockObservationId"]]; height=max_line_height(observations,node["pdfPageIndex"])
            header = [observations[x] for x in r["headerAnchorObservationIds"]]
            rows = [[observations[x] for x in band] for band in r["repeatingRowBandObservationIds"]]
            header_x=line_x_clusters(header,height); row_x=[line_x_clusters(band,height) for band in rows]
            repeated = len(row_x)>=2 and matching_x_count(row_x[0],row_x[1],height)>=2
            header_repeat = all(matching_x_count(header_x, band, height)>=2 for band in row_x[:2])
            item={"nodeId":node["nodeId"],"page":node["pdfPageIndex"],"type":node["nodeType"],"sourceEmittedBoxGlyphs": "┌" in compact(block) and "│" in compact(block),"samePage":all(x["pdfPageIndex"]==node["pdfPageIndex"] for x in [block,*header,*sum(rows,[])]),"headerAnchorObservationCount":len(header),"twoRowsRepeatAtLeastTwoXClusters":repeated,"twoRowsMatchAtLeastTwoHeaderXClusters":header_repeat,"ruleInputDoesNotEncodeClusterComparison":True}
            if authority == "shugiin":
                units=[observations[x] for x in r["localUnitAnchorObservationIds"]]
                item["localUnitAnchorObserved"] = bool(units) and all("（単位：百万円）" in compact(x) for x in units)
                item["localHeaderLiteralObserved"] = any("総額及び計画年次" in compact(x) for x in header)
            local_results.append(item)
    hyakuman = [x for x in observations.values() if x["observationKind"]=="textLine" and "百万円" in x.get("raw",{}).get("engineNativeText","")]
    manifest=load(output/"structural-interpretation-manifest.json")
    treatments=manifest.get("a02HyakumanYenReconciliation",[])
    treatment_ids={x["observationId"] for x in treatments}
    result={
      "immutableBaselineHashes": immutable, "counts":{"nodes":len(nodes),"edges":len(edges),"supportedOuter":len(outer_results),"localOrNested":len(local_results),"unclassified":sum(x.get("nodeType")=="unclassifiedStructure" for x in nodes)},
      "idAudit":{"uniqueNodeIds":len(node_ids)==len(set(node_ids)),"uniqueEdgeIds":len(edge_ids)==len(set(edge_ids)),"nodeIdsReconstructExactly":not any(x.startswith("node-id-contract") for x in exceptions),"edgeIdsDeterministicByImplementation":not any(x.startswith("edge-id-nondeterministic") for x in exceptions),"edgeIdFrozenTupleFidelity":"NONCONFORMANT: edge IDs use parent/child IDs rather than the frozen direct source/file/page/primitive tuple"},
      "closure":closure,"exceptions":exceptions,"boundaries":{"endpointFailures":endpoint_failures,"crossPageEdges":cross_page,"crossFileEdges":cross_file,"outerLocalDirectEdges":unit_inheritance},
      "outerRuleReview":outer_results,"localRuleReview":local_results,
      "a02HyakumanYen":{"immutableS2TextLineOccurrences":len(hyakuman),"allHaveTreatment":set(x["observationId"] for x in hyakuman)==treatment_ids,"allTreatmentsResolveToS2":treatment_ids <= set(observations),"treatmentCount":len(treatments)}
    }
    return result


def main():
    root=Path(__file__).resolve().parents[3]
    spec=load(root/"fixtures/document-understanding/batch-001/wave-1-s3-structural-repair-spec.json")
    result={"schemaVersion":1,"artifactType":"independent-review-audit","reviewerDoesNotImportExecutor":True,"specVersion":spec["specVersion"],"specSha256":digest(root/"fixtures/document-understanding/batch-001/wave-1-s3-structural-repair-spec.json"),"authorities":{}}
    for a,d,p in [("kunaicho","authority-01-kunaicho","batch-001-wave-1-a01-v1"),("shugiin","authority-02-shugiin","batch-001-wave-1-a02-v1")]: result["authorities"][a]=audit_authority(root,spec,a,d,p)
    print(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2))

if __name__=="__main__": main()
