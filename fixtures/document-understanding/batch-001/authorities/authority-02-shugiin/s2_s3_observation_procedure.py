#!/usr/bin/env python3
"""Non-production, authority-local S2/S3 observation procedure.

Uses Poppler's native-text `pdftotext -bbox-layout` without a reading-order
sort flag. It preserves the resulting XML separately, emits raw page/line/word
observations in XML emission order, and derives only non-semantic structure.
"""
import argparse, hashlib, json, subprocess, sys
from pathlib import Path
from xml.etree import ElementTree as ET

NS = {"x": "http://www.w3.org/1999/xhtml"}
ID_VERSION = "experiment-local-s2-s3-v1"

def digest_bytes(data): return hashlib.sha256(data).hexdigest()
def stable_id(*parts): return "s2s3-" + hashlib.sha256("\x1f".join(map(str, parts)).encode()).hexdigest()[:24]
def write_json(path, value): path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")
def write_jsonl(path, rows): path.write_text("".join(json.dumps(r, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n" for r in rows))
def bbox(elem): return {k: elem.attrib.get(k) for k in ("xMin", "yMin", "xMax", "yMax")}
def raw_text(elem): return "".join(elem.itertext())

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--authority-id", required=True); ap.add_argument("--batch-authority-id", required=True)
    ap.add_argument("--file-id", required=True); ap.add_argument("--expected-sha256", required=True)
    ap.add_argument("--expected-pages", required=True, type=int); ap.add_argument("--profile", required=True)
    ap.add_argument("--survey-evidence", required=True); ap.add_argument("--provenance-caveat", default=None)
    args = ap.parse_args(); out = Path(args.out); raw_dir = out / "raw"; raw_dir.mkdir(parents=True, exist_ok=True)
    procedure_sha = digest_bytes(Path(__file__).read_bytes())
    pdf = Path(args.pdf); actual_sha = digest_bytes(pdf.read_bytes())
    if actual_sha != args.expected_sha256: raise SystemExit("source SHA mismatch")
    info = subprocess.run(["pdfinfo", str(pdf)], check=True, capture_output=True, text=True).stdout
    page_count = int(next(line.split(":", 1)[1].strip() for line in info.splitlines() if line.startswith("Pages:")))
    if page_count != args.expected_pages: raise SystemExit("source page count mismatch")
    profile_sha = digest_bytes(Path(args.profile).read_bytes())
    xml_path = raw_dir / "poppler-bbox-layout.xml"
    subprocess.run(["pdftotext", "-bbox-layout", str(pdf), str(xml_path)], check=True)
    xml_bytes = xml_path.read_bytes(); root = ET.fromstring(xml_bytes)
    pages = root.findall(".//x:body/x:doc/x:page", NS)
    if len(pages) != page_count: raise SystemExit("XML page count mismatch")
    observations, nodes, edges = [], [], []
    doc_id = stable_id(ID_VERSION, actual_sha, args.authority_id, args.file_id, "document")
    nodes.append({"nodeId": doc_id, "stage": "S3", "nodeType": "document", "evidenceClass": "source_observed", "sourceSha256": actual_sha, "fileId": args.file_id, "supportingObservationIds": [], "state": "observed_value"})
    per_page = []; unit_count = 0; repl_count = 0; block_count = line_count = word_count = 0
    for pidx, page in enumerate(pages):
        width, height = page.attrib["width"], page.attrib["height"]
        page_obs_id = stable_id(ID_VERSION, actual_sha, pidx, "page")
        observations.append({"observationId": page_obs_id, "stage": "S2", "authorityId": args.authority_id, "sourceSha256": actual_sha, "fileId": args.file_id, "pdfPageIndex": pidx, "sourceOrder": {"page": pidx}, "observationKind": "page", "raw": {"width": width, "height": height}, "geometry": {"coordinateSystem": "Poppler bbox-layout page coordinates", "width": width, "height": height}, "method": {"engine": "pdftotext", "mode": "-bbox-layout", "sortApplied": False, "rawEngineArtifact": "raw/poppler-bbox-layout.xml"}, "state": "observed_value", "provenance": {"engineEmissionOrder": pidx}})
        page_id = stable_id(ID_VERSION, actual_sha, pidx, "page-node")
        nodes.append({"nodeId": page_id, "stage": "S3", "nodeType": "page", "evidenceClass": "source_observed", "sourceSha256": actual_sha, "fileId": args.file_id, "pdfPageIndex": pidx, "supportingObservationIds": [page_obs_id], "state": "observed_value"})
        edges.append({"edgeId": stable_id(ID_VERSION, doc_id, page_id, "contains"), "stage": "S3", "relationshipType": "contains", "evidenceClass": "source_observed", "fromNodeId": doc_id, "toNodeId": page_id, "supportingObservationIds": [page_obs_id], "state": "observed_value"})
        page_line_ids=[]; page_word_ids=[]; page_block_ids=[]; all_line_text=[]; right_block_ids=[]
        flows = page.findall("x:flow", NS)
        for fi, flow in enumerate(flows):
          for bi, block in enumerate(flow.findall("x:block", NS)):
            block_count += 1; block_obs_id = stable_id(ID_VERSION, actual_sha, pidx, fi, bi, "block")
            block_id = stable_id(ID_VERSION, actual_sha, pidx, fi, bi, "block-node"); page_block_ids.append(block_id)
            observations.append({"observationId": block_obs_id, "stage": "S2", "authorityId": args.authority_id, "sourceSha256": actual_sha, "fileId": args.file_id, "pdfPageIndex": pidx, "sourceOrder": {"page": pidx, "flow": fi, "block": bi}, "observationKind": "textBlock", "raw": {"engineNativeText": raw_text(block)}, "geometry": {"coordinateSystem": "Poppler bbox-layout page coordinates", "bbox": bbox(block)}, "method": {"engine": "pdftotext", "mode": "-bbox-layout", "sortApplied": False, "rawEngineArtifact": "raw/poppler-bbox-layout.xml"}, "state": "observed_value", "provenance": {"engineEmissionOrder": [pidx,fi,bi]}})
            nodes.append({"nodeId": block_id, "stage": "S3", "nodeType": "sourceTextBlock", "evidenceClass": "source_observed", "sourceSha256": actual_sha, "fileId": args.file_id, "pdfPageIndex": pidx, "geometry": bbox(block), "supportingObservationIds": [block_obs_id], "state": "observed_value"})
            edges.append({"edgeId": stable_id(ID_VERSION, page_id, block_id, "contains"), "stage": "S3", "relationshipType": "contains", "evidenceClass": "source_observed", "fromNodeId": page_id, "toNodeId": block_id, "supportingObservationIds": [block_obs_id], "state": "observed_value"})
            if float(block.attrib.get("xMin", "0")) >= float(width) * 0.57: right_block_ids.append(block_id)
            for li, line in enumerate(block.findall("x:line", NS)):
              line_count += 1; text = raw_text(line); all_line_text.append(text)
              line_obs_id=stable_id(ID_VERSION, actual_sha,pidx,fi,bi,li,"line"); line_id=stable_id(ID_VERSION,actual_sha,pidx,fi,bi,li,"line-node"); page_line_ids.append(line_obs_id)
              observations.append({"observationId":line_obs_id,"stage":"S2","authorityId":args.authority_id,"sourceSha256":actual_sha,"fileId":args.file_id,"pdfPageIndex":pidx,"sourceOrder":{"page":pidx,"flow":fi,"block":bi,"line":li},"observationKind":"textLine","raw":{"engineNativeText":text},"geometry":{"coordinateSystem":"Poppler bbox-layout page coordinates","bbox":bbox(line)},"method":{"engine":"pdftotext","mode":"-bbox-layout","sortApplied":False,"rawEngineArtifact":"raw/poppler-bbox-layout.xml"},"state":"observed_value","provenance":{"engineEmissionOrder":[pidx,fi,bi,li]}})
              nodes.append({"nodeId":line_id,"stage":"S3","nodeType":"sourceTextLine","evidenceClass":"source_observed","sourceSha256":actual_sha,"fileId":args.file_id,"pdfPageIndex":pidx,"geometry":bbox(line),"supportingObservationIds":[line_obs_id],"state":"observed_value"})
              edges.append({"edgeId":stable_id(ID_VERSION,block_id,line_id,"contains"),"stage":"S3","relationshipType":"contains","evidenceClass":"source_observed","fromNodeId":block_id,"toNodeId":line_id,"supportingObservationIds":[line_obs_id],"state":"observed_value"})
              if "単位" in text: unit_count += 1
              repl_count += text.count("�")
              for wi, word in enumerate(line.findall("x:word", NS)):
                word_count += 1; wtext=raw_text(word); word_obs_id=stable_id(ID_VERSION,actual_sha,pidx,fi,bi,li,wi,"word"); page_word_ids.append(word_obs_id)
                observations.append({"observationId":word_obs_id,"stage":"S2","authorityId":args.authority_id,"sourceSha256":actual_sha,"fileId":args.file_id,"pdfPageIndex":pidx,"sourceOrder":{"page":pidx,"flow":fi,"block":bi,"line":li,"word":wi},"observationKind":"word","raw":{"engineNativeText":wtext},"geometry":{"coordinateSystem":"Poppler bbox-layout page coordinates","bbox":bbox(word)},"method":{"engine":"pdftotext","mode":"-bbox-layout","sortApplied":False,"rawEngineArtifact":"raw/poppler-bbox-layout.xml"},"state":"observed_value","provenance":{"engineEmissionOrder":[pidx,fi,bi,li,wi]}})
        page_text="\n".join(all_line_text)
        partition_kind="outerLedger" if all(token in page_text for token in ("要求", "番号", "備", "考")) else "unclassifiedStructure"
        partition_id=stable_id(ID_VERSION,actual_sha,pidx,partition_kind)
        nodes.append({"nodeId":partition_id,"stage":"S3","nodeType":partition_kind,"evidenceClass":"structurally_inferred","inferenceRule":"s2-s3-v1:split-header-token-set","sourceSha256":actual_sha,"fileId":args.file_id,"pdfPageIndex":pidx,"supportingObservationIds":page_line_ids,"state":"observed_value"})
        edges.append({"edgeId":stable_id(ID_VERSION,page_id,partition_id,"contains"),"stage":"S3","relationshipType":"contains","evidenceClass":"structurally_inferred","inferenceRule":"s2-s3-v1:split-header-token-set","fromNodeId":page_id,"toNodeId":partition_id,"supportingObservationIds":page_line_ids,"state":"observed_value"})
        if right_block_ids:
          remarks_id=stable_id(ID_VERSION,actual_sha,pidx,"remarks-region")
          nodes.append({"nodeId":remarks_id,"stage":"S3","nodeType":"remarksRegion","evidenceClass":"structurally_inferred","inferenceRule":"s2-s3-v1:right-side-block-geometry","sourceSha256":actual_sha,"fileId":args.file_id,"pdfPageIndex":pidx,"supportingObservationIds":page_line_ids,"state":"observed_value"})
          edges.append({"edgeId":stable_id(ID_VERSION,partition_id,remarks_id,"contains"),"stage":"S3","relationshipType":"contains","evidenceClass":"structurally_inferred","inferenceRule":"s2-s3-v1:right-side-block-geometry","fromNodeId":partition_id,"toNodeId":remarks_id,"supportingObservationIds":page_line_ids,"state":"observed_value"})
          for bid in right_block_ids:
            edges.append({"edgeId":stable_id(ID_VERSION,remarks_id,bid,"contains"),"stage":"S3","relationshipType":"contains","evidenceClass":"structurally_inferred","inferenceRule":"s2-s3-v1:right-side-block-geometry","fromNodeId":remarks_id,"toNodeId":bid,"supportingObservationIds":[],"state":"observed_value"})
        per_page.append({"pdfPageIndex":pidx,"wordObservationCount":len(page_word_ids),"lineObservationCount":len(page_line_ids),"structuralPartition":partition_kind,"remarksSideBlockCount":len(right_block_ids)})
    write_jsonl(out/"source-observations.jsonl", observations); write_jsonl(out/"nodes.jsonl", nodes); write_jsonl(out/"edges.jsonl", edges)
    def sha(path): return digest_bytes(path.read_bytes())
    source_manifest={"artifactType":"authority-source-manifest","stage":"S2_S3","authorityId":args.authority_id,"batchAuthorityId":args.batch_authority_id,"fileId":args.file_id,"sourceSha256":actual_sha,"pageCount":page_count,"canonicalLockedStatus":"matched_existing_lock","sourceLockReference":"sources/source-lock.json","frozenProfileReference":args.profile,"surveyEvidenceReference":args.survey_evidence,"provenanceCaveat":args.provenance_caveat,"stageStatus":"COMPLETE_NOT_CANONICAL_FROZEN"}
    obs_manifest={"artifactType":"observation-manifest","stage":"S2","stageStatus":"COMPLETE_NOT_CANONICAL_FROZEN","authorityId":args.authority_id,"sourceSha256":actual_sha,"pageCoverage":{"expected":page_count,"actual":len(pages),"failures":[]},"method":{"engine":"pdftotext","engineVersion":"Poppler 26.09.0","runtime":"Python "+sys.version.split()[0],"procedureSha256":procedure_sha,"command":["pdftotext","-bbox-layout","<locked-source>","raw/poppler-bbox-layout.xml"],"sortApplied":False,"sourceNativeText":True,"ocrUsed":False,"renderingUsedForMachineExtraction":False,"geometryLevel":"page/block/line/word bbox; no image payload","encodingBehavior":"Poppler XML entity-decoded text; raw XML retained","idScheme":{"version":ID_VERSION,"status":"EXPERIMENT_LOCAL_NOT_GLOBALLY_FROZEN","inputs":"source SHA, authority, file, page, engine emission order, observation kind"},"serialization":{"keyOrder":"lexicographic","newline":"LF","floatPolicy":"engine-emitted decimal strings","localeIndependent":True,"absolutePathsExcluded":True}},"rawEngineArtifact":{"path":"raw/poppler-bbox-layout.xml","sha256":digest_bytes(xml_bytes)},"recordCount":len(observations),"statistics":{"blocks":block_count,"lines":line_count,"words":word_count,"unitDeclarationLines":unit_count,"replacementCharacterCount":repl_count},"perPage":per_page,"downstreamStages":{"S4_normalization":"not_created","S5_semanticCandidates":"not_created","S6_financialObservations":"not_created","S7_canonicalFreeze":"not_created"}}
    structural_manifest={"artifactType":"structural-interpretation-manifest","stage":"S3","stageStatus":"COMPLETE_NOT_CANONICAL_FROZEN","authorityId":args.authority_id,"sourceSha256":actual_sha,"frozenProfile":{"path":args.profile,"sha256":profile_sha},"inputS2":{"path":"source-observations.jsonl","sha256":sha(out/"source-observations.jsonl")},"counts":{"nodes":len(nodes),"edges":len(edges),"sourceObservedNodes":len([n for n in nodes if n["evidenceClass"]=="source_observed"]),"structurallyInferredNodes":len([n for n in nodes if n["evidenceClass"]=="structurally_inferred"]),"structurallyInferredEdgeCount":len([e for e in edges if e["evidenceClass"]=="structurally_inferred"]),"unclassifiedStructurePages":len([p for p in per_page if p["structuralPartition"]=="unclassifiedStructure"]),"crossPageEdgeCount":0,"crossFileEdgeCount":0},"pagesWithUnresolvedStructures":[p["pdfPageIndex"] for p in per_page if p["structuralPartition"]=="unclassifiedStructure"],"profileContradictions":[],"downstreamStages":{"S4_normalization":"not_created","S5_semanticCandidates":"not_created","S6_financialObservations":"not_created","S7_canonicalFreeze":"not_created"}}
    write_json(out/"source-manifest.json", source_manifest); write_json(out/"observation-manifest.json", obs_manifest); write_json(out/"structural-interpretation-manifest.json", structural_manifest)
if __name__ == "__main__": main()
