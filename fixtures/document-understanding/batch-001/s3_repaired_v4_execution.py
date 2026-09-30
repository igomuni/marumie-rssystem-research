#!/usr/bin/env python3
"""Research-only Wave 1 S3 repair v4 executor.

V4 consumes immutable S2 only.  It pins its two repository-local helpers in
the execution manifest, retains every actual header word-to-source-line link,
and accepts outer-row evidence only on strict observed x-range overlap.
"""
from __future__ import annotations

import argparse, hashlib, json, platform
from collections import Counter, defaultdict
from pathlib import Path

import s3_repaired_v3_execution as v3

SPEC = v3.SPEC
NS = v3.NS
OUTER = v3.OUTER
LOCAL = v3.LOCAL
EDGE = v3.EDGE


def dump(value): return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def write_json(path, value): Path(path).write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
def write_jsonl(path, values): Path(path).write_text("".join(dump(x) + "\n" for x in values), encoding="utf-8")
def box(value): return v3.box(value)
def union(values): return v3.union(values)
def locator(values): return v3.locator(values)


def identity(kind, page, rule, supports):
    observed = {x["observationId"]: x for x in supports}
    return v3.ident(kind, page, rule, list(observed.values()))


def page_node(authority, page):
    return {
        "nodeId": identity("page", page, "source-observed-page", [page]), "stage": "S3_REPAIRED_V4", "namespace": NS,
        "authorityId": authority, "nodeType": "page", "evidenceClass": "source_observed", "sourceSha256": page["sourceSha256"],
        "fileId": page["fileId"], "pdfPageIndex": page["pdfPageIndex"], "supportingObservationIds": [page["observationId"]],
        "evidenceLocator": locator([page]), "state": "observed_value", "geometry": {"bbox": None},
    }


def inferred_node(authority, kind, rule, profile, page, supports, status, ambiguity, rule_input):
    direct = {x["observationId"]: x for x in supports}
    values = list(direct.values())
    return {
        "nodeId": identity(kind, page, rule, values), "stage": "S3_REPAIRED_V4", "namespace": NS, "authorityId": authority,
        "nodeType": kind, "evidenceClass": "structurally_inferred", "inferenceRule": rule, "profileVersion": profile,
        "ambiguityState": ambiguity, "structuralStatus": status, "sourceSha256": page["sourceSha256"], "fileId": page["fileId"],
        "pdfPageIndex": page["pdfPageIndex"], "supportingObservationIds": sorted(direct), "evidenceLocator": locator(values),
        "ruleInput": rule_input, "state": "not_applicable", "geometry": {"bbox": union(values)},
    }


def inferred_edge(parent, child, rule, profile, supports, status, ambiguity, rule_input):
    direct = {x["observationId"]: x for x in supports}
    values = list(direct.values())
    return {
        "edgeId": identity(EDGE, child, rule, values), "idPrimitive": EDGE, "stage": "S3_REPAIRED_V4", "namespace": NS,
        "relationshipType": "contains", "fromNodeId": parent["nodeId"], "toNodeId": child["nodeId"],
        "evidenceClass": "structurally_inferred", "inferenceRule": rule, "profileVersion": profile, "ambiguityState": ambiguity,
        "structuralStatus": status, "sourceSha256": child["sourceSha256"], "fileId": child["fileId"], "pdfPageIndex": child["pdfPageIndex"],
        "supportingObservationIds": sorted(direct), "evidenceLocator": locator(values), "ruleInput": rule_input, "state": "not_applicable",
    }


def source_lines_for_word(word, lines):
    """All immutable S2 text lines geometrically containing this word."""
    wb = box(word)
    return [line for line in lines if (lambda lb: lb[0] <= wb[0] and lb[2] >= wb[2] and lb[1] <= wb[1] and lb[3] >= wb[3])(box(line))]


def header_lines_and_relations(groups, lines, max_height):
    mapping, line_by_id = {}, {}
    for group_index, group in enumerate(groups):
        for word in group:
            members = source_lines_for_word(word, lines)
            mapping[word["observationId"]] = [x["observationId"] for x in members]
            for line in members: line_by_id[line["observationId"]] = line
    member_lines = [line_by_id[x] for x in sorted(line_by_id)]
    relations = []
    for i, left in enumerate(member_lines):
        for right in member_lines[i + 1:]:
            a, b = box(left), box(right)
            relation = a[1] <= b[3] + max_height and a[3] >= b[1] - max_height
            relations.append({"leftLineObservationId": left["observationId"], "rightLineObservationId": right["observationId"], "overlapOrTouchWithinPageMaximumLineHeight": relation})
    return member_lines, mapping, relations


def literal_local_band(lines, max_height):
    """Connected direct source-line band, with a non-chained compact span."""
    if not lines: return False, {"reason": "no_source_header_lines"}
    pending, seen = [0], {0}
    boxes = [box(x) for x in lines]
    while pending:
        i = pending.pop()
        for j in range(len(lines)):
            if j in seen: continue
            a, b = boxes[i], boxes[j]
            if a[1] <= b[3] + max_height and a[3] >= b[1] - max_height:
                seen.add(j); pending.append(j)
    span = max(x[3] for x in boxes) - min(x[1] for x in boxes)
    return len(seen) == len(lines) and span <= 2 * max_height, {"connected": len(seen) == len(lines), "verticalSpan": span, "nonChainedLocality": span <= 2 * max_height}


def strict_outer_candidate(page, lines, words):
    """Candidate grouping uses v3's pinned source-local helper; acceptance is v4 strict."""
    maximum = v3.height(lines)
    for seed in v3.bands(lines):
        seed_box = union(seed)
        window = [line for band in v3.bands(lines) for line in band if union(band)[1] <= seed_box[3] + maximum and union(band)[3] >= seed_box[1] - maximum]
        header = v3.v2.outer_header(window, words)
        if not header: continue
        groups, group_boxes = header
        header_lines, word_lines, relations = header_lines_and_relations(groups, lines, maximum)
        if any(not x for x in word_lines.values()): continue
        literal_pass, locality = literal_local_band(header_lines, maximum)
        if not literal_pass: continue
        header_box = union([word for group in groups for word in group])
        rows = []
        for band in v3.bands(lines):
            band_box = union(band)
            if band_box[1] <= header_box[3] + maximum: continue
            matches = []
            for index, header_box_x in enumerate(group_boxes):
                direct_words = [word for word in v3.words_window(words, band_box) if (lambda wb: wb[0] <= header_box_x[2] and wb[2] >= header_box_x[0])(box(word))]
                if direct_words:
                    matches.append({"headerGroupIndex": index, "headerXRange": header_box_x, "rowWordObservationIds": [x["observationId"] for x in direct_words], "rowWordBBoxes": [box(x) for x in direct_words], "strictObservedXRangeOverlap": True})
            if len(matches) >= 2: rows.append((band, [word for match in matches for word in [next(x for x in words if x["observationId"] == oid) for oid in match["rowWordObservationIds"]]], matches))
        if len(rows) >= 2:
            return {"groups": groups, "groupBoxes": group_boxes, "headerLines": header_lines, "wordToLines": word_lines, "lineRelations": relations, "locality": locality, "maximum": maximum, "rows": rows[:2]}
    return None


def local_detail(authority, page, profile, candidate):
    # The frozen local rule is unchanged; reuse only its S2-based candidate builder.
    kind, status, ambiguity, supports, rule_input = v3.local_node(authority, page, profile, candidate)
    return kind, status, ambiguity, supports, rule_input


def execute(root, output_root, authority, directory, profile):
    base = root / "fixtures/document-understanding/batch-001/authorities" / directory
    observations = load_jsonl(base / "source-observations.jsonl")
    by_id = {x["observationId"]: x for x in observations}
    pages = defaultdict(list)
    for observation in observations: pages[observation["pdfPageIndex"]].append(observation)
    out = output_root / "fixtures/document-understanding/batch-001/authorities" / directory / "s3-repaired-v4"
    out.mkdir(parents=True, exist_ok=True)
    nodes, edges, page_summaries, outer_diagnostics = [], [], [], []
    for index, items in sorted(pages.items()):
        page = next(x for x in items if x["observationKind"] == "page")
        lines = [x for x in items if x["observationKind"] == "textLine"]
        words = [x for x in items if x["observationKind"] == "word"]
        blocks = [x for x in items if x["observationKind"] == "textBlock"]
        page_record = page_node(authority, page); nodes.append(page_record)
        candidate = strict_outer_candidate(page, lines, words)
        if candidate:
            row_supports = [x for band, row_words, _ in candidate["rows"] for x in [*band, *row_words]]
            supports = [page, *[x for group in candidate["groups"] for x in group], *candidate["headerLines"], *row_supports]
            rule_input = {
                "headerGroups": [{"index": i, "memberObservationIds": [x["observationId"] for x in group], "rawGlyphContributions": [x["raw"]["engineNativeText"] for x in group], "unionBBox": candidate["groupBoxes"][i]} for i, group in enumerate(candidate["groups"])],
                "leftToRightHeaderGroupIndexes": [0, 1, 2, 3, 4],
                "headerSourceLineObservationIds": [x["observationId"] for x in candidate["headerLines"]], "headerSourceLineBBoxes": [box(x) for x in candidate["headerLines"]],
                "headerWordToSourceLineObservationIds": candidate["wordToLines"], "headerLineRelations": candidate["lineRelations"],
                "pageMaximumObservedLineHeight": candidate["maximum"], "localHeaderBandUnionBBox": union(candidate["headerLines"]), "localHeaderBandDiagnostic": candidate["locality"],
                "rowPatternEvidence": [{"rowBandLineObservationIds": [x["observationId"] for x in band], "rowBandUnionBBox": union(band), "matchedHeaderRanges": matches} for band, _, matches in candidate["rows"]],
                "samePageOnly": True, "noPageWideTokenRule": True, "strictXOverlapOnly": True,
            }
            outer = inferred_node(authority, "outerLedger", OUTER, profile, page, supports, "structurally_supported", "not_ambiguous", rule_input)
        else:
            fallback = [page, *(v3.bands(lines)[0] if v3.bands(lines) else [])]
            rule_input = {"pageMaximumObservedLineHeight": v3.height(lines), "samePageOnly": True, "noPageWideTokenRule": True, "strictXOverlapOnly": True, "failureReason": "literal-local-header-band-or-two-strict-row-x-range-pattern-not-supported"}
            outer = inferred_node(authority, "unclassifiedStructure", OUTER, profile, page, fallback, "unclassified", rule_input["failureReason"], rule_input)
        nodes.append(outer)
        edge_support = [page, *[by_id[x] for x in outer["supportingObservationIds"] if x != page["observationId"]]]
        edges.append(inferred_edge(page_record, outer, OUTER, profile, edge_support, outer["structuralStatus"], outer["ambiguityState"], {"parentAnchorObservationIds": [page["observationId"]], "childDirectObservationIds": outer["supportingObservationIds"], "samePageOnly": True}))
        local_count = 0
        for block in blocks:
            local_candidate = v3.v2.local_candidate(block, lines, words, authority == "shugiin")
            if not local_candidate: continue
            kind, status, ambiguity, supports, rule_input = local_detail(authority, page, profile, local_candidate)
            node = inferred_node(authority, kind, LOCAL, profile, page, supports, status, ambiguity, rule_input); nodes.append(node); local_count += 1
            edges.append(inferred_edge(page_record, node, LOCAL, profile, supports, status, ambiguity, {"parentAnchorObservationIds": [page["observationId"]], "childDirectObservationIds": node["supportingObservationIds"], "samePageOnly": True}))
        outer_diagnostics.append({"pdfPageIndex": index, "v4Classification": outer["nodeType"], "v4Status": outer["structuralStatus"], "reason": outer["ambiguityState"]})
        page_summaries.append({"pdfPageIndex": index, "outerPartitionNodeId": outer["nodeId"], "outerPartitionStatus": outer["structuralStatus"], "localOrNestedGroupCount": local_count})
    treatments = []
    if authority == "shugiin":
        supported = [x for x in nodes if x.get("nodeType") == "boundedLocalTable" and x.get("structuralStatus") == "structurally_supported"]
        anchor_groups = defaultdict(list)
        for node in supported:
            for oid in node["ruleInput"].get("localUnitAnchorObservationIds", []): anchor_groups[oid].append(node)
        for observation in observations:
            if observation["observationKind"] != "textLine" or "百万円" not in observation.get("raw", {}).get("engineNativeText", ""): continue
            direct = anchor_groups.get(observation["observationId"], [])
            bbox_only = [x["nodeId"] for x in supported if x["pdfPageIndex"] == observation["pdfPageIndex"] and v3.contains(box(x), box(observation))]
            if len(direct) == 1: treatment, reason, group = "member_of_supported_boundedLocalTable", "direct-local-unit-anchor", direct[0]["nodeId"]
            elif len(direct) > 1: treatment, reason, group = "member_of_ambiguous_structural_group", "shared-direct-local-unit-anchor", None
            else: treatment, reason, group = "not_structurally_grouped_representation_limited", "no-direct-local-unit-anchor", None
            value = {"observationId": observation["observationId"], "pdfPageIndex": observation["pdfPageIndex"], "sourceOrder": observation["sourceOrder"], "bbox": observation["geometry"]["bbox"], "directUnitAnchorGroupIds": [x["nodeId"] for x in direct], "bboxContainmentOnlyGroupIds": bbox_only, "finalTreatment": treatment, "reason": reason}
            if group: value["groupNodeId"] = group
            treatments.append(value)
    nodes.sort(key=lambda x: x["nodeId"]); edges.sort(key=lambda x: x["edgeId"]); treatments.sort(key=lambda x: (x["pdfPageIndex"], x["observationId"]))
    write_jsonl(out / "nodes.jsonl", nodes); write_jsonl(out / "edges.jsonl", edges)
    manifest = {"schemaVersion": 1, "artifactType": "batch-001-wave-1-s3-repaired-v4-manifest", "stage": "S3_REPAIRED_V4", "stageStatus": "COMPLETE_NOT_CANONICAL_FROZEN", "executionRevision": "v4", "specVersion": SPEC, "namespace": NS, "authorityId": authority, "profileVersion": profile, "sourceSha256": next(x for x in observations if x["observationKind"] == "page")["sourceSha256"], "inputSourceObservations": {"path": f"fixtures/document-understanding/batch-001/authorities/{directory}/source-observations.jsonl", "sha256": sha(base / "source-observations.jsonl")}, "nodeCount": len(nodes), "edgeCount": len(edges), "countsByStructuralStatus": dict(sorted(Counter(x.get("structuralStatus", "source_observed") for x in nodes).items())), "nodeCountsByType": dict(sorted(Counter(x["nodeType"] for x in nodes).items())), "pageSummaries": page_summaries, "outerDiagnostics": outer_diagnostics, "crossPageInferredStructuralEdgeCount": 0, "crossFileInferredStructuralEdgeCount": 0, "documentMembershipEdgeCount": 0, "outerLocalUnitInheritanceEdgeCount": 0, "normalizationStatus": "not_created", "semanticCandidateStatus": "not_created", "financialAssociationStatus": "not_created", "canonicalFreezeStatus": "not_created"}
    if authority == "shugiin": manifest["a02HyakumanYenReconciliation"] = treatments
    write_json(out / "structural-interpretation-manifest.json", manifest)
    this = Path(__file__)
    dependencies = [{"path": "fixtures/document-understanding/batch-001/s3_repaired_v3_execution.py", "sha256": sha(this.with_name("s3_repaired_v3_execution.py")), "role": "S2 geometry and frozen local-structure helper access"}, {"path": "fixtures/document-understanding/batch-001/s3_repaired_v2_execution.py", "sha256": sha(this.with_name("s3_repaired_v2_execution.py")), "role": "transitive v3 S2 geometry and local-candidate helper"}]
    execution_manifest = {"schemaVersion": 1, "artifactType": "batch-001-wave-1-s3-repair-v4-execution-manifest", "executionRevision": "v4", "specVersion": SPEC, "namespace": NS, "authorityId": authority, "profileVersion": profile, "procedure": {"path": "fixtures/document-understanding/batch-001/s3_repaired_v4_execution.py", "sha256": sha(this), "repositoryLocalDependencies": dependencies}, "runtime": {"pythonVersion": platform.python_version(), "ocrUsed": False, "sourceNativeS2Only": True}, "idPolicy": {"nodeAndEdgeInputs": ["specVersion", "sourceSha256", "fileId", "pdfPageIndex", "structural primitive type", "inferenceRule", "sorted supportingObservationIds"], "edgePrimitive": EDGE, "parentOrChildIdsExcluded": True}, "serialization": {"encoding": "UTF-8", "newlines": "LF", "jsonKeyOrder": "sorted", "recordOrder": "stable ID ascending", "absolutePathsExcluded": True}, "historicalV1V2V3Preserved": True, "documentContainmentOmittedFromPageScopedGraph": True}
    write_json(out / "repair-execution-manifest.json", execution_manifest)
    return {"authority": authority, "nodes": nodes, "edges": edges, "manifest": manifest, "out": out}


def load_jsonl(path): return [json.loads(x) for x in Path(path).read_text(encoding="utf-8").splitlines() if x]


def main():
    parser = argparse.ArgumentParser(); parser.add_argument("--repo", type=Path, default=Path.cwd()); parser.add_argument("--out-root", type=Path)
    args = parser.parse_args(); root = args.repo.resolve(); out_root = args.out_root.resolve() if args.out_root else root
    spec = json.loads((root / "fixtures/document-understanding/batch-001/wave-1-s3-structural-repair-spec.json").read_text(encoding="utf-8"))
    if spec["specVersion"] != SPEC: raise SystemExit("frozen spec mismatch")
    results = []
    for authority, directory, profile in [("kunaicho", "authority-01-kunaicho", "batch-001-wave-1-a01-v1"), ("shugiin", "authority-02-shugiin", "batch-001-wave-1-a02-v1")]:
        base = root / "fixtures/document-understanding/batch-001/authorities" / directory
        for rel, wanted in spec["immutableBaseline"]["authorityArtifactHashes"][authority].items():
            if sha(base / rel) != wanted: raise SystemExit(f"immutable baseline mismatch: {authority} {rel}")
        results.append(execute(root, out_root, authority, directory, profile))
    print(dump({"status": "ok", "authorities": [{"authority": x["authority"], "nodes": len(x["nodes"]), "edges": len(x["edges"])} for x in results]}))


if __name__ == "__main__": main()
