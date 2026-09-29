#!/usr/bin/env python3
"""Research-only deterministic executor for frozen Batch-001 Wave 1 S3 repair.

This is deliberately not production document-understanding code.  It reads
only immutable S2 observations and writes a separately versioned, review-ready
S3 graph.  It never changes baseline S2 or experimental S3 artifacts.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

SPEC_VERSION = "batch-001-wave-1-s3-repair-v1"
NAMESPACE = "s3r1"
OUTER_RULE = "s3-repair-v1:localized-outer-ledger-header"
LOCAL_RULE = "s3-repair-v1:same-page-bounded-structural-group"


def stable_json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path, values):
    Path(path).write_text("".join(stable_json(x) + "\n" for x in values), encoding="utf-8")


def rect(record):
    b = record.get("geometry", {}).get("bbox") or record.get("raw", {}).get("bbox") or record.get("bbox")
    if isinstance(b, dict):
        return [float(b[k]) for k in ("xMin", "yMin", "xMax", "yMax")]
    if isinstance(b, list) and len(b) == 4:
        return [float(x) for x in b]
    return None


def union_rect(records):
    boxes = [rect(r) for r in records if rect(r)]
    if not boxes:
        return None
    return [min(x[0] for x in boxes), min(x[1] for x in boxes), max(x[2] for x in boxes), max(x[3] for x in boxes)]


def raw_text(record):
    raw = record.get("raw", {})
    return raw.get("text") or raw.get("rawText") or raw.get("engineNativeText") or record.get("text") or ""


def glyph_text(record):
    """Raw-glyph matching aid only; it never replaces stored raw source text."""
    return "".join(raw_text(record).split())


def source_order(record):
    order = record.get("sourceOrder", {})
    return order.get("path") or order.get("index") or record.get("sourceOrderPath") or record.get("observationId")


def record_id(authority, primitive, rule, page, supports, source_sha, file_id):
    material = "\x1f".join([SPEC_VERSION, source_sha, file_id, str(page), primitive, rule, *sorted(supports)])
    return f"{NAMESPACE}-{primitive}-{hashlib.sha256(material.encode('utf-8')).hexdigest()[:20]}"


def locator(records):
    return [{"observationId": r["observationId"], "sourceOrder": source_order(r), "bbox": rect(r)} for r in records]


def vertical_bands(lines, tolerance):
    """Group source lines at a common observed y baseline (no reading-order repair)."""
    ordered = sorted((x for x in lines if rect(x)), key=lambda x: (rect(x)[1], rect(x)[0], x["observationId"]))
    bands = []
    for line in ordered:
        box = rect(line)
        # A row band is not a chained vertical neighborhood: adjacent table
        # rows must remain distinct.  `tolerance` is retained for callers'
        # documented page-local header-window calculations.
        if not bands or abs(box[1] - bands[-1][0]["_band_ymin"]) > 0.000001:
            line = dict(line)
            line["_band_ymax"] = box[3]
            line["_band_ymin"] = box[1]
            bands.append([line])
        else:
            line = dict(line)
            line["_band_ymax"] = max(bands[-1][-1]["_band_ymax"], box[3])
            line["_band_ymin"] = bands[-1][0]["_band_ymin"]
            bands[-1].append(line)
    for band in bands:
        for item in band:
            item.pop("_band_ymax", None)
            item.pop("_band_ymin", None)
    return bands


def page_index(record):
    return record.get("pdfPageIndex")


def direct_words(lines, words_by_page):
    line_orders = {(x.get("sourceOrder", {}).get("block"), x.get("sourceOrder", {}).get("flow"), x.get("sourceOrder", {}).get("line")) for x in lines}
    result = []
    for word in words_by_page:
        order = word.get("sourceOrder", {})
        parent = (order.get("block"), order.get("flow"), order.get("line"))
        if parent in line_orders:
            result.append(word)
    return result


def matches_chars(words, chars, xmin=None, xmax=None):
    selected = []
    remaining = Counter(chars)
    for word in sorted(words, key=lambda x: (rect(x)[0] if rect(x) else 0, rect(x)[1] if rect(x) else 0, x["observationId"])):
        text = glyph_text(word)
        box = rect(word)
        if not box or not any(character in remaining and remaining[character] > 0 for character in text):
            continue
        if xmin is not None and box[0] < xmin:
            continue
        if xmax is not None and box[2] > xmax:
            continue
        selected.append(word)
        for character in text:
            if character in remaining and remaining[character] > 0:
                remaining[character] -= 1
    return selected if not any(remaining.values()) else []


def header_groups(band_lines, page_words):
    words = direct_words(band_lines, page_words)
    issue = matches_chars(words, "事項")
    remarks = matches_chars(words, "備考")
    if not issue or not remarks:
        return None
    issue_box, remarks_box = union_rect(issue), union_rect(remarks)
    request = matches_chars(words, "要求番号", xmax=issue_box[0])
    previous = matches_chars(words, "前年度予算額", xmin=issue_box[2], xmax=remarks_box[0])
    requested = matches_chars(words, "概算要求額", xmin=issue_box[2], xmax=remarks_box[0])
    groups = [request, issue, previous, requested, remarks]
    if not all(groups):
        return None
    boxes = [union_rect(g) for g in groups]
    if any(boxes[i][0] >= boxes[i + 1][0] for i in range(len(boxes) - 1)):
        return None
    return {"groups": groups, "boxes": boxes}


def row_bands_below(bands, header_box, page_words, header_boxes, tolerance):
    out = []
    for lines in bands:
        b = union_rect(lines)
        if not b or b[1] <= header_box[3] + tolerance:
            continue
        words = direct_words(lines, page_words)
        ranges = []
        for hbox in header_boxes:
            # page-local maximum line-height is also the only permitted positional tolerance.
            if any(rect(w) and rect(w)[0] <= hbox[2] + tolerance and rect(w)[2] >= hbox[0] - tolerance for w in words):
                ranges.append(hbox)
        if len(ranges) >= 2:
            out.append({"lines": lines, "bbox": b, "matchingHeaderRangeCount": len(ranges)})
    return out


def block_table_candidate(block, page_lines, page_words, local_required=False):
    text = glyph_text(block)
    box = rect(block)
    if not box:
        return None
    in_block = [line for line in page_lines if rect(line) and rect(line)[0] >= box[0] and rect(line)[2] <= box[2] and rect(line)[1] >= box[1] and rect(line)[3] <= box[3]]
    heights = [(rect(x)[3] - rect(x)[1]) for x in in_block if rect(x)]
    tolerance = max(heights) if heights else 0
    bands = vertical_bands(in_block, tolerance)
    multi = [b for b in bands if len(direct_words(b, page_words)) >= 2]
    table_text = "┌" in text and "│" in text and len(multi) >= 3
    if not table_text:
        return None
    header = next((band for band in multi if "総額及び計画年次" in "".join(glyph_text(x) for x in band)), multi[0])
    header_box = union_rect(header)
    rows = [band for band in multi if union_rect(band)[1] > header_box[3]]
    repeated = [b for b in rows if len(direct_words(b, page_words)) >= 2]
    if len(repeated) < 2:
        return None
    unit_lines = [x for x in in_block if "（単位：百万円）" in glyph_text(x)]
    has_local_header = "総額及び計画年次" in text and len(direct_words(header, page_words)) >= 2
    if local_required and (not unit_lines or not has_local_header):
        return {"status": "structurally_ambiguous", "block": block, "header": header, "rows": repeated, "unitLines": unit_lines, "reason": "local-unit-anchor-or-local-multicolumn-header-not-fully-supported"}
    return {"status": "structurally_supported", "block": block, "header": header, "rows": repeated, "unitLines": unit_lines, "reason": "same-page-contiguous-block-with-own-header-and-repeated-x-cluster-row-bands"}


def obs_maps(records):
    pages = defaultdict(list)
    for record in records:
        pages[page_index(record)].append(record)
    return pages


def inferred_node(authority, primitive, rule, profile, page_obs, supports, status, ambiguity, rule_input):
    page = page_index(page_obs)
    source_sha = page_obs["sourceSha256"]
    file_id = page_obs["fileId"]
    direct = {r["observationId"]: r for r in supports}
    values = list(direct.values())
    return {
        "nodeId": record_id(authority, primitive, rule, page, list(direct), source_sha, file_id),
        "stage": "S3_REPAIRED", "namespace": NAMESPACE, "authorityId": authority,
        "nodeType": primitive, "evidenceClass": "structurally_inferred", "inferenceRule": rule,
        "profileVersion": profile, "ambiguityState": ambiguity, "structuralStatus": status,
        "sourceSha256": source_sha, "fileId": file_id, "pdfPageIndex": page,
        "supportingObservationIds": sorted(direct), "evidenceLocator": locator(values), "ruleInput": rule_input,
        "state": "not_applicable", "geometry": {"bbox": union_rect(values)}
    }


def inferred_edge(authority, parent, child, rule, profile, supports, status, ambiguity, rule_input):
    direct = {r["observationId"]: r for r in supports}
    material = "\x1f".join([SPEC_VERSION, parent["nodeId"], child["nodeId"], rule, *sorted(direct)])
    return {
        "edgeId": f"{NAMESPACE}-edge-{hashlib.sha256(material.encode('utf-8')).hexdigest()[:20]}",
        "stage": "S3_REPAIRED", "namespace": NAMESPACE, "relationshipType": "contains",
        "fromNodeId": parent["nodeId"], "toNodeId": child["nodeId"], "evidenceClass": "structurally_inferred",
        "inferenceRule": rule, "profileVersion": profile, "ambiguityState": ambiguity,
        "structuralStatus": status, "sourceSha256": child["sourceSha256"], "fileId": child["fileId"],
        "pdfPageIndex": child["pdfPageIndex"], "supportingObservationIds": sorted(direct),
        "evidenceLocator": locator(list(direct.values())), "ruleInput": rule_input, "state": "not_applicable"
    }


def source_node(authority, primitive, page_obs, supports):
    source_sha, file_id, page = page_obs["sourceSha256"], page_obs["fileId"], page_index(page_obs)
    return {
        "nodeId": record_id(authority, primitive, "source-observed-page", page, [x["observationId"] for x in supports], source_sha, file_id),
        "stage": "S3_REPAIRED", "namespace": NAMESPACE, "authorityId": authority, "nodeType": primitive,
        "evidenceClass": "source_observed", "sourceSha256": source_sha, "fileId": file_id, "pdfPageIndex": page,
        "supportingObservationIds": sorted(x["observationId"] for x in supports), "evidenceLocator": locator(supports),
        "state": "observed_value", "geometry": {"bbox": union_rect(supports)}
    }


def execute_authority(root, out_root, spec, authority, directory, profile_version):
    base = root / "fixtures/document-understanding/batch-001/authorities" / directory
    records = [json.loads(line) for line in (base / "source-observations.jsonl").read_text(encoding="utf-8").splitlines() if line]
    by_page = obs_maps(records)
    profile = json.loads((base / "authority-preflight-profile.json").read_text(encoding="utf-8"))
    source_sha = profile["sources"]["files"][0]["sha256"]
    out = out_root / "fixtures/document-understanding/batch-001/authorities" / directory / "s3-repaired-v1"
    out.mkdir(parents=True, exist_ok=True)
    nodes, edges, page_summaries, a01_candidates, unit_treatments = [], [], [], [], []
    document_support = [next(x for x in records if x.get("observationKind") == "page" and page_index(x) == min(by_page))]
    document = source_node(authority, "document", document_support[0], document_support)
    nodes.append(document)
    for page in sorted(by_page):
        all_records = by_page[page]
        page_obs = next(x for x in all_records if x.get("observationKind") == "page")
        lines = [x for x in all_records if x.get("observationKind") == "textLine"]
        blocks = [x for x in all_records if x.get("observationKind") == "textBlock"]
        words = [x for x in all_records if x.get("observationKind") == "word"]
        page_node = source_node(authority, "page", page_obs, [page_obs])
        nodes.append(page_node)
        heights = [(rect(x)[3] - rect(x)[1]) for x in lines if rect(x)]
        tolerance = max(heights) if heights else 0
        bands = vertical_bands(lines, tolerance)
        outer = None
        for index, seed in enumerate(bands):
            seed_box = union_rect(seed)
            # A local header window expands from the seed only; it does not
            # chain through a page of touching table rows.
            band = [line for other in bands if union_rect(other)[1] <= seed_box[3] + tolerance and union_rect(other)[3] >= seed_box[1] - tolerance for line in other]
            header = header_groups(band, words)
            if not header:
                continue
            header_records = [r for group in header["groups"] for r in group]
            hbox = union_rect(header_records)
            rows = row_bands_below(bands, hbox, words, header["boxes"], tolerance)
            if len(rows) >= 2:
                supports = [page_obs, *header_records, *(r for row in rows[:2] for r in row["lines"])]
                outer = inferred_node(authority, "outerLedger", OUTER_RULE, profile_version, page_obs, supports,
                                      "structurally_supported", "not_ambiguous", {
                                          "headerGroups": [[x["observationId"] for x in g] for g in header["groups"]],
                                          "headerUnionBboxes": header["boxes"], "pageMaximumObservedLineHeight": tolerance,
                                          "repeatingRowBands": [[x["observationId"] for x in row["lines"]] for row in rows[:2]],
                                          "noPageWideTokenRule": True
                                      })
                break
        if outer is None:
            supports = [page_obs, *(bands[0] if bands else [])]
            outer = inferred_node(authority, "unclassifiedStructure", OUTER_RULE, profile_version, page_obs, supports,
                                  "unclassified", "insufficient-localized-header-and-repeated-row-pattern-evidence", {
                                      "pageMaximumObservedLineHeight": tolerance, "noPageWideTokenRule": True
                                  })
        nodes.append(outer)
        edges.append(inferred_edge(authority, document, page_node, "s3-repair-v1:source-document-page", profile_version,
                                   [page_obs], "structurally_supported", "not_ambiguous", {"sourceObservedPage": page_obs["observationId"]}))
        edges.append(inferred_edge(authority, page_node, outer, OUTER_RULE, profile_version,
                                   [page_obs, *[x for x in records if x["observationId"] in outer["supportingObservationIds"]]],
                                   outer["structuralStatus"], outer["ambiguityState"], {"childDirectObservationIds": outer["supportingObservationIds"], "parentAnchorObservationIds": [page_obs["observationId"]]}))
        local_count = 0
        for block in blocks:
            candidate = block_table_candidate(block, lines, words, local_required=(authority == "shugiin"))
            if not candidate:
                continue
            support = [page_obs, block, *candidate["header"], *(line for band in candidate["rows"][:2] for line in band), *candidate["unitLines"]]
            primitive = "boundedLocalTable" if authority == "shugiin" and candidate["status"] == "structurally_supported" else ("nestedStructure" if candidate["status"] == "structurally_supported" else "ambiguousStructuralGroup")
            status = candidate["status"]
            ambiguity = "not_ambiguous" if status == "structurally_supported" else candidate["reason"]
            local = inferred_node(authority, primitive, LOCAL_RULE, profile_version, page_obs, support, status, ambiguity, {
                "candidateBlockObservationId": block["observationId"], "headerAnchorObservationIds": [x["observationId"] for x in candidate["header"]],
                "repeatingRowBandObservationIds": [[x["observationId"] for x in band] for band in candidate["rows"][:2]],
                "localUnitAnchorObservationIds": [x["observationId"] for x in candidate["unitLines"]],
                "samePageOnly": True, "noRightSideRule": True, "noInferredPdfFrame": True
            })
            nodes.append(local); local_count += 1
            edges.append(inferred_edge(authority, page_node, local, LOCAL_RULE, profile_version, support, status, ambiguity, {
                "childDirectObservationIds": [block["observationId"], *[x["observationId"] for x in candidate["header"]]],
                "parentAnchorObservationIds": [page_obs["observationId"]], "samePageOnly": True
            }))
            if authority == "kunaicho":
                a01_candidates.append({"page": page, "blockObservationId": block["observationId"], "treatment": primitive, "structuralStatus": status, "reason": candidate["reason"]})
            if authority == "shugiin":
                for record in all_records:
                    if record.get("observationKind") == "textLine" and "百万円" in glyph_text(record):
                        b = rect(record)
                        bb = rect(block)
                        if b and bb and b[0] >= bb[0] and b[2] <= bb[2] and b[1] >= bb[1] and b[3] <= bb[3]:
                            unit_treatments.append({"observationId": record["observationId"], "pdfPageIndex": page, "treatment": "member_of_supported_boundedLocalTable" if status == "structurally_supported" else "member_of_ambiguous_structural_group", "groupNodeId": local["nodeId"], "blockObservationId": block["observationId"]})
        page_summaries.append({"pdfPageIndex": page, "outerPartitionNodeId": outer["nodeId"], "outerPartitionStatus": outer["structuralStatus"], "localOrNestedGroupCount": local_count})
    # Account for A02 occurrences that are not within a qualified candidate block.
    if authority == "shugiin":
        handled = {x["observationId"] for x in unit_treatments}
        for record in records:
            if record.get("observationKind") == "textLine" and "百万円" in glyph_text(record) and record["observationId"] not in handled:
                unit_treatments.append({"observationId": record["observationId"], "pdfPageIndex": page_index(record), "treatment": "not_structurally_grouped_representation_limited", "reason": "no-qualified-same-page-local-header-and-repeated-pattern-group"})
        unit_treatments.sort(key=lambda x: (x["pdfPageIndex"], x["observationId"]))
    nodes.sort(key=lambda x: x["nodeId"]); edges.sort(key=lambda x: x["edgeId"])
    write_jsonl(out / "nodes.jsonl", nodes); write_jsonl(out / "edges.jsonl", edges)
    summary = {
        "schemaVersion": 1, "artifactType": "batch-001-wave-1-s3-repaired-manifest", "stage": "S3_REPAIRED", "stageStatus": "COMPLETE_NOT_CANONICAL_FROZEN",
        "specVersion": SPEC_VERSION, "namespace": NAMESPACE, "authorityId": authority, "profileVersion": profile_version,
        "inputSourceObservations": {"path": f"fixtures/document-understanding/batch-001/authorities/{directory}/source-observations.jsonl", "sha256": sha256(base / "source-observations.jsonl")},
        "sourceSha256": source_sha, "nodeCount": len(nodes), "edgeCount": len(edges),
        "countsByStructuralStatus": dict(sorted(Counter(x.get("structuralStatus", "source_observed") for x in nodes).items())),
        "pageSummaries": page_summaries, "crossPageEdgeCount": 0, "crossFileEdgeCount": 0, "outerLocalUnitInheritanceEdgeCount": 0,
        "normalizationStatus": "not_created", "semanticCandidateStatus": "not_created", "financialAssociationStatus": "not_created", "canonicalFreezeStatus": "not_created"
    }
    if authority == "kunaicho": summary["a01NestedCandidateAudit"] = a01_candidates
    else: summary["a02HyakumanYenReconciliation"] = unit_treatments
    write_json(out / "structural-interpretation-manifest.json", summary)
    execution = {
        "schemaVersion": 1, "artifactType": "batch-001-wave-1-s3-repair-execution-manifest", "specVersion": SPEC_VERSION,
        "namespace": NAMESPACE, "procedure": {"path": "fixtures/document-understanding/batch-001/s3_repaired_v1_execution.py", "sha256": sha256(Path(__file__))},
        "authorityId": authority, "sourceSha256": source_sha, "profileVersion": profile_version,
        "serialization": {"encoding": "UTF-8", "newlines": "LF", "jsonKeyOrder": "sorted", "recordOrder": "stable ID ascending", "absolutePathsExcluded": True},
        "mechanics": {"lineBandTolerance": "page maximum observed textLine height", "outerRule": OUTER_RULE, "localRule": LOCAL_RULE, "rightSideThresholdUsed": False, "pageWideTokenRuleUsed": False, "crossPageInference": False, "crossFileInference": False},
        "outputBoundary": "s3-repaired-v1", "baselineS2AndExperimentalS3Mutated": False
    }
    write_json(out / "repair-execution-manifest.json", execution)
    return {"authority": authority, "directory": directory, "output": out, "nodes": nodes, "edges": edges, "summary": summary}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[4])
    parser.add_argument("--out-root", type=Path, default=None)
    args = parser.parse_args()
    root = args.repo.resolve(); out_root = args.out_root.resolve() if args.out_root else root
    spec = json.loads((root / "fixtures/document-understanding/batch-001/wave-1-s3-structural-repair-spec.json").read_text(encoding="utf-8"))
    if spec["specVersion"] != SPEC_VERSION: raise SystemExit("frozen spec version mismatch")
    for authority, values in spec["immutableBaseline"]["authorityArtifactHashes"].items():
        directory = "authority-01-kunaicho" if authority == "kunaicho" else "authority-02-shugiin"
        base = root / "fixtures/document-understanding/batch-001/authorities" / directory
        for relative, expected in values.items():
            actual = sha256(base / relative)
            if actual != expected: raise SystemExit(f"immutable baseline mismatch: {authority} {relative}")
    results = [
        execute_authority(root, out_root, spec, "kunaicho", "authority-01-kunaicho", "batch-001-wave-1-a01-v1"),
        execute_authority(root, out_root, spec, "shugiin", "authority-02-shugiin", "batch-001-wave-1-a02-v1")
    ]
    print(stable_json({"status": "ok", "authorities": [{"authority": r["authority"], "nodes": len(r["nodes"]), "edges": len(r["edges"])} for r in results]}))


if __name__ == "__main__":
    main()
