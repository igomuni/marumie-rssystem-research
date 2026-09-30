#!/usr/bin/env python3
"""Independent, read-only acceptance review for Wave 1 S3 repair v3.

This procedure deliberately imports neither an executor nor an execution audit.
It reads immutable S2 and the emitted graph, reconstructing the review checks
with conservative geometry predicates.  It creates no S3 records.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

SPEC = "batch-001-wave-1-s3-repair-v1"
NS = "s3r1"
EDGE = "edge:contains"
AUTHORITIES = {
    "kunaicho": ("authority-01-kunaicho", "batch-001-wave-1-a01-v1"),
    "shugiin": ("authority-02-shugiin", "batch-001-wave-1-a02-v1"),
}
HISTORICAL_CORE = {
    "authority-01-kunaicho": {
        "s3-repaired-v1/nodes.jsonl": "6d85ab08503e8495e36af72b0544b4dc3bafb6057359f2af3db4ee290bbb6156",
        "s3-repaired-v1/edges.jsonl": "7bb247babf7e1c8a90c5379dd1e640c1108706aa9fd9c9d769f63395cdf65cd3",
        "s3-repaired-v2/nodes.jsonl": "45564b6ef46a4fdef61358c7c07b8c5a9a8d309dd95c303d40d5400c0422288c",
        "s3-repaired-v2/edges.jsonl": "7597c1c8fdd0766837e2f4f349482c793ee2c0be059806476263d9a5b43a43dd",
    },
    "authority-02-shugiin": {
        "s3-repaired-v1/nodes.jsonl": "16b2bcd1c6c5676b6cd3500951a4ad464fe7a1bd70c958deb22d37abbf3637ac",
        "s3-repaired-v1/edges.jsonl": "95318747f9f20157ffde7e060e693e1aa0c0a1fe9a95d4989b4371767d4e82e0",
        "s3-repaired-v2/nodes.jsonl": "8923c3d70b38d9c5dfb11383b25fcd44522b27872ab91a936f4ad9c912702b7f",
        "s3-repaired-v2/edges.jsonl": "42236fbc1d0df56fff72421976539ff0d6f3b1e3ab8e85545228c523dcfc6ff4",
    },
}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_jsonl(path):
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line]


def bbox(record_or_box):
    value = record_or_box
    if isinstance(value, dict) and "geometry" in value:
        value = value["geometry"].get("bbox")
    if isinstance(value, dict):
        return [float(value[x]) for x in ("xMin", "yMin", "xMax", "yMax")]
    return [float(x) for x in value]


def union(records):
    boxes = [bbox(x) for x in records]
    return [min(x[0] for x in boxes), min(x[1] for x in boxes), max(x[2] for x in boxes), max(x[3] for x in boxes)]


def id_for(kind, record):
    text = chr(31).join([
        SPEC, record["sourceSha256"], record["fileId"], str(record["pdfPageIndex"]),
        kind, record["inferenceRule"], *sorted(record["supportingObservationIds"]),
    ])
    return f"{NS}-{kind}-{hashlib.sha256(text.encode()).hexdigest()[:20]}"


def overlaps_x(left, right):
    return left[0] <= right[2] and left[2] >= right[0]


def vertical_connected(lines, tolerance):
    """Graph connectivity from source-line y intervals expanded by max height.

    A page-wide transitive chain is rejected: a band has to be compact as well
    as connected, bounding its y span to two max-line-height intervals.
    """
    if not lines:
        return False, {"reason": "no_header_source_lines"}
    boxes = [bbox(x) for x in lines]
    todo, seen = [0], {0}
    while todo:
        i = todo.pop()
        for j in range(len(boxes)):
            if j in seen:
                continue
            a, b = boxes[i], boxes[j]
            if a[1] <= b[3] + tolerance and a[3] >= b[1] - tolerance:
                seen.add(j); todo.append(j)
    span = max(x[3] for x in boxes) - min(x[1] for x in boxes)
    return len(seen) == len(lines) and span <= 2 * tolerance, {
        "lineObservationIds": [x["observationId"] for x in lines],
        "lineBBoxes": boxes, "pageMaximumObservedLineHeight": tolerance,
        "connected": len(seen) == len(lines), "verticalSpan": span,
        "nonChainedLocalBand": span <= 2 * tolerance,
    }


def source_lines_for_words(words, lines):
    """Use source geometry only: line contains word's entire bbox."""
    selected = []
    for line in lines:
        lb = bbox(line)
        if any(lb[0] <= bbox(word)[0] and lb[2] >= bbox(word)[2] and lb[1] <= bbox(word)[1] and lb[3] >= bbox(word)[3] for word in words):
            selected.append(line)
    return selected


def audit_outer(node, observations):
    by_id = {x["observationId"]: x for x in observations}
    page_lines = [x for x in observations if x["pdfPageIndex"] == node["pdfPageIndex"] and x["observationKind"] == "textLine"]
    ri = node["ruleInput"]
    headers = ri.get("headerGroups", [])
    header_errors = []
    header_words = []
    required = ["要求番号", "事項", "前年度予算額", "概算要求額", "備考"]
    if len(headers) != 5:
        header_errors.append("required_header_group_count")
    for index, group in enumerate(headers):
        words = [by_id.get(x) for x in group.get("memberObservationIds", [])]
        if not words or any(x is None or x["observationKind"] != "word" for x in words):
            header_errors.append(f"header_{index}_missing_word_support")
            continue
        header_words.extend(words)
        raw = "".join(x.get("raw", {}).get("engineNativeText", "") for x in sorted(words, key=lambda x: (bbox(x)[0], bbox(x)[1], x["observationId"])))
        if index < len(required) and not all(ch in raw for ch in required[index]):
            header_errors.append(f"header_{index}_raw_glyph_group_mismatch")
        if group.get("unionBBox") != union(words):
            header_errors.append(f"header_{index}_union_bbox_mismatch")
    header_boxes = [x.get("unionBBox") for x in headers]
    if len(header_boxes) == 5 and any(bbox(header_boxes[i])[0] > bbox(header_boxes[i + 1])[0] for i in range(4)):
        header_errors.append("header_groups_not_left_to_right")
    max_height = ri.get("literalHeaderBand", {}).get("pageMaximumObservedLineHeight")
    if not isinstance(max_height, (int, float)):
        header_errors.append("missing_page_maximum_line_height")
        band = {"reason": "missing_page_maximum_line_height"}
        literal_ok = False
    else:
        actual_lines = source_lines_for_words(header_words, page_lines)
        literal_ok, band = vertical_connected(actual_lines, float(max_height))
        emitted = set(ri.get("literalHeaderBand", {}).get("memberLineObservationIds", []))
        if not set(x["observationId"] for x in actual_lines).issubset(emitted):
            header_errors.append("header_source_lines_not_retained_in_emitted_band")
    row_results = []
    for row in ri.get("rowPatternEvidence", []):
        strict, tolerance_only, invalid_support = 0, 0, []
        for match in row.get("matchedHeaderRanges", []):
            hb = bbox(match["headerXRange"])
            words = [by_id.get(x) for x in match.get("rowWordObservationIds", [])]
            if not words or any(x is None or x["observationKind"] != "word" for x in words):
                invalid_support.append(match.get("headerGroupIndex")); continue
            if any(x["observationId"] not in node["supportingObservationIds"] for x in words):
                invalid_support.append(match.get("headerGroupIndex")); continue
            if any(overlaps_x(bbox(word), hb) for word in words):
                strict += 1
            elif any(bbox(word)[0] <= hb[2] + float(max_height) and bbox(word)[2] >= hb[0] - float(max_height) for word in words):
                tolerance_only += 1
        row_results.append({"rowBandLineObservationIds": row.get("rowBandLineObservationIds", []), "strictHeaderRangeMatches": strict, "toleranceDependentOnlyMatches": tolerance_only, "invalidSupportGroups": invalid_support})
    row_ok = len(row_results) >= 2 and all(x["strictHeaderRangeMatches"] >= 2 and not x["invalidSupportGroups"] for x in row_results)
    return {
        "nodeId": node["nodeId"], "pdfPageIndex": node["pdfPageIndex"],
        "headerErrors": header_errors, "literalBand": band, "literalBandPass": literal_ok and not header_errors,
        "rowResults": row_results, "rowWordStrictPass": row_ok,
        "reviewClassification": "outerLedger" if literal_ok and not header_errors and row_ok else "unclassifiedStructure",
    }


def audit_local(node, observations):
    by_id = {x["observationId"]: x for x in observations}
    ri = node.get("ruleInput", {})
    problems = []
    clusters = ri.get("headerXClusters", [])
    rows = ri.get("rowXClusters", [])
    matches = ri.get("headerToRowClusterMatches", [])
    if len(clusters) < 2 or len(rows) < 2 or len(matches) < 2:
        problems.append("missing_cluster_or_row_evidence")
    for cluster_set in [clusters, *rows]:
        for cluster in cluster_set:
            members = [by_id.get(x) for x in cluster.get("memberObservationIds", [])]
            if not members or any(x is None or x["observationKind"] != "word" for x in members):
                problems.append("cluster_missing_word_evidence"); continue
            want = [min(bbox(x)[0] for x in members), max(bbox(x)[2] for x in members)]
            if cluster.get("xRange") != want:
                problems.append("cluster_xrange_mismatch")
    if any(len(x) < 2 for x in matches):
        problems.append("row_does_not_repeat_two_clusters")
    if node["nodeType"] == "boundedLocalTable":
        anchors = ri.get("localUnitAnchorObservationIds", [])
        if len(anchors) != 1 or any("百万円" not in by_id.get(x, {}).get("raw", {}).get("engineNativeText", "") for x in anchors):
            problems.append("missing_or_invalid_local_hyakuman_anchor")
    return {"nodeId": node["nodeId"], "pdfPageIndex": node["pdfPageIndex"], "problems": sorted(set(problems)), "pass": not problems}


def audit_authority(root, authority, directory, profile, spec):
    base = root / "fixtures/document-understanding/batch-001/authorities" / directory
    observations = load_jsonl(base / "source-observations.jsonl")
    nodes = load_jsonl(base / "s3-repaired-v3/nodes.jsonl")
    edges = load_jsonl(base / "s3-repaired-v3/edges.jsonl")
    by_obs = {x["observationId"]: x for x in observations}
    by_node = {x["nodeId"]: x for x in nodes}
    immutable = {rel: sha(base / rel) == wanted for rel, wanted in spec["immutableBaseline"]["authorityArtifactHashes"][authority].items()}
    historical = {rel: sha(base / rel) == wanted for rel, wanted in HISTORICAL_CORE[directory].items()}
    loc_fail, support_fail, id_fail, endpoint_fail, boundary_fail = [], [], [], [], []
    inferred = [x for x in [*nodes, *edges] if x.get("evidenceClass") == "structurally_inferred"]
    for record in inferred:
        actual = record.get("nodeId", record.get("edgeId"))
        kind = record.get("nodeType", record.get("idPrimitive"))
        if id_for(kind, record) != actual:
            id_fail.append(actual)
        locators = {x["observationId"]: x for x in record.get("evidenceLocator", [])}
        for oid in record.get("supportingObservationIds", []):
            source = by_obs.get(oid)
            if not source or any(source.get(k) != record.get(k) for k in ("sourceSha256", "fileId", "pdfPageIndex")):
                support_fail.append({"recordId": actual, "observationId": oid})
                continue
            locator = locators.get(oid)
            if not locator or locator.get("sourceOrder") != source.get("sourceOrder") or locator.get("bbox") != source.get("geometry", {}).get("bbox"):
                loc_fail.append({"recordId": actual, "observationId": oid})
    for edge in edges:
        source, target = by_node.get(edge["fromNodeId"]), by_node.get(edge["toNodeId"])
        if not source or not target:
            endpoint_fail.append(edge["edgeId"]); continue
        if source["authorityId"] != target["authorityId"] or source["fileId"] != target["fileId"] or source["pdfPageIndex"] != target["pdfPageIndex"]:
            boundary_fail.append(edge["edgeId"])
    outers = [x for x in nodes if x.get("nodeType") == "outerLedger"]
    outer = [audit_outer(x, observations) for x in outers]
    local = [audit_local(x, observations) for x in nodes if x.get("nodeType") in {"nestedStructure", "boundedLocalTable"}]
    pages = sorted({x["pdfPageIndex"] for x in observations if x["observationKind"] == "page"})
    by_outer_page = {x["pdfPageIndex"]: x for x in outer}
    matrix = []
    for page in pages:
        emitted = next(x for x in nodes if x["pdfPageIndex"] == page and x["nodeType"] in {"outerLedger", "unclassifiedStructure"})
        reconstructed = by_outer_page.get(page)
        review_class = reconstructed["reviewClassification"] if reconstructed else "unclassifiedStructure"
        matrix.append({"pdfPageIndex": page, "v3Classification": emitted["nodeType"], "reviewClassification": review_class, "agreement": emitted["nodeType"] == review_class, "reason": "complete independently reconstructed outer evidence" if reconstructed else "no independently complete page-local header-plus-strict-row-word evidence found; retained unclassified"})
    result = {
        "authorityId": authority, "nodeCount": len(nodes), "edgeCount": len(edges),
        "nodeTypes": dict(sorted(Counter(x["nodeType"] for x in nodes).items())),
        "structuralStatuses": dict(sorted(Counter(x.get("structuralStatus", "source_observed") for x in nodes).items())),
        "immutableBaselineHashPass": all(immutable.values()), "immutableBaselineHashResults": immutable,
        "historicalV1V2CoreHashPass": all(historical.values()), "historicalV1V2CoreHashResults": historical,
        "supportFailureCount": len(support_fail), "supportFailures": support_fail,
        "locatorFailureCount": len(loc_fail), "locatorFailures": loc_fail,
        "idFailureCount": len(id_fail), "idFailures": id_fail,
        "nodeIdDuplicates": len(nodes) - len(by_node), "edgeIdDuplicates": len(edges) - len({x["edgeId"] for x in edges}),
        "endpointFailureCount": len(endpoint_fail), "endpointFailures": endpoint_fail,
        "crossPageOrFileEdgeCount": len(boundary_fail), "crossPageOrFileEdges": boundary_fail,
        "outerReview": outer, "outerAcceptedCount": sum(x["reviewClassification"] == "outerLedger" for x in outer),
        "outerRejectedCount": sum(x["reviewClassification"] != "outerLedger" for x in outer),
        "outerFullPageMatrix": matrix, "outerFullPageAgreementCount": sum(x["agreement"] for x in matrix),
        "localNestedReview": local, "localNestedFailureCount": sum(not x["pass"] for x in local),
    }
    if authority == "shugiin":
        manifest = json.loads((base / "s3-repaired-v3/structural-interpretation-manifest.json").read_text(encoding="utf-8"))
        rec = manifest["a02HyakumanYenReconciliation"]
        all_occurrences = [x for x in observations if x["observationKind"] == "textLine" and "百万円" in x.get("raw", {}).get("engineNativeText", "")]
        supported = [x for x in nodes if x.get("nodeType") == "boundedLocalTable" and x.get("structuralStatus") == "structurally_supported"]
        anchors = defaultdict(list)
        for node in supported:
            for oid in node["ruleInput"].get("localUnitAnchorObservationIds", []):
                anchors[oid].append(node["nodeId"])
        treatments = {x["observationId"]: x for x in rec}
        mismatch, missing = [], []
        for occurrence in all_occurrences:
            row = treatments.get(occurrence["observationId"])
            direct = anchors.get(occurrence["observationId"], [])
            if not row:
                missing.append(occurrence["observationId"]); continue
            if direct and row["finalTreatment"] == "not_structurally_grouped_representation_limited":
                mismatch.append(occurrence["observationId"])
        result["a02HyakumanOccurrenceCount"] = len(all_occurrences)
        result["a02TreatmentCount"] = len(rec)
        result["a02TreatmentDistribution"] = dict(sorted(Counter(x["finalTreatment"] for x in rec).items()))
        result["a02DirectAnchorTreatmentMismatches"] = mismatch
        result["a02MissingTreatmentRows"] = missing
        result["a02SharedDirectAnchors"] = {x: y for x, y in anchors.items() if len(y) > 1}
        boxes = [(x["nodeId"], bbox(x)) for x in supported]
        overlaps = []
        for i, (a, ab) in enumerate(boxes):
            for b, bb in boxes[i + 1:]:
                node_a, node_b = by_node[a], by_node[b]
                if node_a["pdfPageIndex"] != node_b["pdfPageIndex"]:
                    continue
                if ab[0] <= bb[2] and ab[2] >= bb[0] and ab[1] <= bb[3] and ab[3] >= bb[1]: overlaps.append([a, b])
        result["a02SupportedTableOverlaps"] = overlaps
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = args.repo.resolve()
    spec_path = root / "fixtures/document-understanding/batch-001/wave-1-s3-structural-repair-spec.json"
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    result = {
        "schemaVersion": 1,
        "artifactType": "batch-001-wave-1-s3-repair-v3-independent-review-audit",
        "independence": "Does not import or invoke v1/v2/v3 executors or execution audits.",
        "reviewBaseCommit": "3c7eb223089f84b39527a84339c53d8562d3172e",
        "specVersion": SPEC, "specSha256": sha(spec_path),
        "authorities": [audit_authority(root, authority, directory, profile, spec) for authority, (directory, profile) in AUTHORITIES.items()],
    }
    dependency_findings = []
    for authority, (directory, _) in AUTHORITIES.items():
        execution_manifest = json.loads((root / "fixtures/document-understanding/batch-001/authorities" / directory / "s3-repaired-v3/repair-execution-manifest.json").read_text(encoding="utf-8"))
        procedure = execution_manifest.get("procedure", {})
        # The v3 source imports v2; the execution manifest pins only v3.
        dependency_findings.append({
            "authorityId": authority,
            "v3ProcedureHashPinned": bool(procedure.get("sha256")),
            "importedV2HelperHashPinned": bool(procedure.get("dependencies", {}).get("s3_repaired_v2_execution.py")),
            "finding": "INCOMPLETE_EFFECTIVE_PROCEDURE_PROVENANCE" if not procedure.get("dependencies", {}).get("s3_repaired_v2_execution.py") else "COMPLETE_EFFECTIVE_PROCEDURE_PROVENANCE",
        })
    result["effectiveProcedureDependencyFindings"] = dependency_findings
    authority_verdicts = {}
    for item in result["authorities"]:
        failures = item["outerRejectedCount"] + item["localNestedFailureCount"] + item["locatorFailureCount"] + item["supportFailureCount"] + item["idFailureCount"] + item["crossPageOrFileEdgeCount"]
        authority_verdicts[item["authorityId"]] = "ACCEPT_REPAIRED_S3_FOR_S4" if failures == 0 else "REPAIR_REQUIRED_BEFORE_S4"
    result["authorityVerdicts"] = authority_verdicts
    result["globalS4Authorization"] = "AUTHORIZED" if all(x == "ACCEPT_REPAIRED_S3_FOR_S4" for x in authority_verdicts.values()) and all(x["finding"] == "COMPLETE_EFFECTIVE_PROCEDURE_PROVENANCE" for x in dependency_findings) else "NOT_AUTHORIZED"
    result["nextAuthorizedTask"] = "Batch-001 Wave 1 S3 Repair Execution v4" if result["globalS4Authorization"] == "NOT_AUTHORIZED" else "Batch-001 Wave 1 Repaired S3 Integration and S4 Entry Freeze"
    text = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
