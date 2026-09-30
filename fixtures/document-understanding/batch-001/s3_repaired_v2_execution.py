#!/usr/bin/env python3
"""Research-only v2 executor for the frozen Wave 1 S3 repair contract.

It preserves v1 and creates a separate execution revision.  It reads only
immutable S2 records and uses `s3r1`, the frozen semantic namespace.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

SPEC = "batch-001-wave-1-s3-repair-v1"
NS = "s3r1"
OUTER = "s3-repair-v1:localized-outer-ledger-header"
LOCAL = "s3-repair-v1:same-page-bounded-structural-group"
EDGE_PRIMITIVE = "edge:contains"


def dump(value): return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def write_json(path, value): Path(path).write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2)+"\n", encoding="utf-8")
def write_jsonl(path, values): Path(path).write_text("".join(dump(x)+"\n" for x in values), encoding="utf-8")
def text(x): return x.get("raw",{}).get("engineNativeText","")
def glyph(x): return "".join(text(x).split())
def box(x):
    b=x.get("geometry",{}).get("bbox")
    return [float(b[k]) for k in ("xMin","yMin","xMax","yMax")] if b else None
def union(xs):
    bs=[box(x) for x in xs if box(x)]
    return [min(x[0] for x in bs),min(x[1] for x in bs),max(x[2] for x in bs),max(x[3] for x in bs)] if bs else None
def order_key(x): return (box(x)[1] if box(x) else 0, box(x)[0] if box(x) else 0, x["observationId"])
def id_for(kind, source, file_id, page, rule, supports):
    raw="\x1f".join([SPEC,source,file_id,str(page),kind,rule,*sorted(supports)])
    return f"{NS}-{kind}-{hashlib.sha256(raw.encode()).hexdigest()[:20]}"
def locator(xs):
    # Copy sourceOrder and the engine-emitted bbox object verbatim: neither
    # is repaired geometry or semantic reading order.
    return [{"observationId":x["observationId"],"sourceOrder":x["sourceOrder"],"bbox":x.get("geometry",{}).get("bbox")} for x in xs]
def contains(outer, inner): return outer and inner and inner[0]>=outer[0] and inner[2]<=outer[2] and inner[1]>=outer[1] and inner[3]<=outer[3]


def y_bands(lines):
    grouped=defaultdict(list)
    for line in lines:
        if box(line): grouped[format(box(line)[1],".6f")].append(line)
    return [sorted(v,key=order_key) for _,v in sorted(grouped.items(),key=lambda kv: float(kv[0]))]


def page_height(lines): return max((box(x)[3]-box(x)[1] for x in lines if box(x)),default=0)


def words_in_window(words, window):
    return [x for x in words if box(x) and box(x)[3]>=window[1] and box(x)[1]<=window[3]]


def choose_chars(words, chars, xmin=None, xmax=None):
    remaining=Counter(chars); picked=[]
    for word in sorted(words,key=order_key):
        b=box(word); g=glyph(word)
        if not b or (xmin is not None and b[0]<xmin) or (xmax is not None and b[2]>xmax): continue
        if not any(remaining[c]>0 for c in g if c in remaining): continue
        picked.append(word)
        for c in g:
            if c in remaining and remaining[c]>0: remaining[c]-=1
    return picked if not any(remaining.values()) else []


def outer_header(window_lines, words):
    wb=union(window_lines); available=words_in_window(words,wb)
    issue=choose_chars(available,"事項"); remarks=choose_chars(available,"備考")
    if not issue or not remarks: return None
    ib,rb=union(issue),union(remarks)
    groups=[choose_chars(available,"要求番号",xmax=ib[0]),issue,choose_chars(available,"前年度予算額",xmin=ib[2],xmax=rb[0]),choose_chars(available,"概算要求額",xmin=ib[2],xmax=rb[0]),remarks]
    if not all(groups): return None
    boxes=[union(x) for x in groups]
    if any(boxes[i][0]>=boxes[i+1][0] for i in range(4)): return None
    return groups,boxes


def cluster_records(records, tolerance):
    """Geometry clusters, not PDF cells: contiguous observed x ranges only."""
    values=sorted((x for x in records if box(x)),key=lambda x:(box(x)[0],box(x)[2],x["observationId"]))
    clusters=[]
    for item in values:
        b=box(item)
        if not clusters or b[0]-clusters[-1][-1]["bbox"][2]>tolerance:
            clusters.append([{"observationId":item["observationId"],"bbox":b}])
        else: clusters[-1].append({"observationId":item["observationId"],"bbox":b})
    return [{"memberObservationIds":[x["observationId"] for x in c],"xRange":[min(x["bbox"][0] for x in c),max(x["bbox"][2] for x in c)],"representativeX":min(x["bbox"][0] for x in c)} for c in clusters]


def match_clusters(header, row, tolerance):
    return [{"headerClusterIndex":i,"rowClusterIndex":j,"headerXRange":h["xRange"],"rowXRange":r["xRange"]}
            for i,h in enumerate(header) for j,r in enumerate(row)
            if h["xRange"][0] <= r["xRange"][1]+tolerance and r["xRange"][0] <= h["xRange"][1]+tolerance]


def page_node(authority,page):
    return {"nodeId":id_for("page",page["sourceSha256"],page["fileId"],page["pdfPageIndex"],"source-observed-page",[page["observationId"]]),"stage":"S3_REPAIRED_V2","namespace":NS,"authorityId":authority,"nodeType":"page","evidenceClass":"source_observed","sourceSha256":page["sourceSha256"],"fileId":page["fileId"],"pdfPageIndex":page["pdfPageIndex"],"supportingObservationIds":[page["observationId"]],"evidenceLocator":locator([page]),"state":"observed_value","geometry":{"bbox":None}}


def inferred_node(authority,kind,rule,profile,page,supports,status,ambiguity,input_value):
    direct={x["observationId"]:x for x in supports}; values=list(direct.values())
    return {"nodeId":id_for(kind,page["sourceSha256"],page["fileId"],page["pdfPageIndex"],rule,direct),"stage":"S3_REPAIRED_V2","namespace":NS,"authorityId":authority,"nodeType":kind,"evidenceClass":"structurally_inferred","inferenceRule":rule,"profileVersion":profile,"ambiguityState":ambiguity,"structuralStatus":status,"sourceSha256":page["sourceSha256"],"fileId":page["fileId"],"pdfPageIndex":page["pdfPageIndex"],"supportingObservationIds":sorted(direct),"evidenceLocator":locator(values),"ruleInput":input_value,"state":"not_applicable","geometry":{"bbox":union(values)}}


def inferred_edge(parent,child,rule,profile,supports,status,ambiguity,input_value):
    direct={x["observationId"]:x for x in supports}; values=list(direct.values())
    edge_id=id_for(EDGE_PRIMITIVE,child["sourceSha256"],child["fileId"],child["pdfPageIndex"],rule,direct)
    return {"edgeId":edge_id,"idPrimitive":EDGE_PRIMITIVE,"stage":"S3_REPAIRED_V2","namespace":NS,"relationshipType":"contains","fromNodeId":parent["nodeId"],"toNodeId":child["nodeId"],"evidenceClass":"structurally_inferred","inferenceRule":rule,"profileVersion":profile,"ambiguityState":ambiguity,"structuralStatus":status,"sourceSha256":child["sourceSha256"],"fileId":child["fileId"],"pdfPageIndex":child["pdfPageIndex"],"supportingObservationIds":sorted(direct),"evidenceLocator":locator(values),"ruleInput":input_value,"state":"not_applicable"}


def local_candidate(block, lines, words, is_a02):
    bb=box(block); members=[x for x in lines if contains(bb,box(x))]; height=page_height(members); bands=y_bands(members)
    if "┌" not in glyph(block) or "│" not in glyph(block): return None
    # Header selection is source-local and explicit; A02's literal is a conservative filter only.
    headers=[band for band in bands if "総額及び計画年次" in "".join(glyph(x) for x in band)]
    if not headers and is_a02: return {"status":"structurally_ambiguous","reason":"no-source-observed-a02-local-header-literal","block":block,"members":members}
    header=headers[0] if headers else next((b for b in bands if len(cluster_records(b,height))>=2),None)
    if not header: return {"status":"structurally_ambiguous","reason":"no-independent-header-clusters","block":block,"members":members}
    hb=union(header); header_words=[x for x in words if box(x) and box(x)[3]>=hb[1] and box(x)[1]<=hb[3] and contains(bb,box(x))]
    header_clusters=cluster_records(header_words,height)
    # A line-span alone is insufficient: retain word-level observed columns.
    if len(header_clusters)<2: return {"status":"structurally_ambiguous","reason":"fewer-than-two-direct-header-x-clusters","block":block,"members":members,"header":header}
    rows=[]
    for band in bands:
        if union(band)[1] <= hb[3]: continue
        # A text-line bbox can span multiple printed columns.  Row-pattern
        # evidence therefore uses only the immutable word observations that
        # intersect this source-observed band, never the line bbox as a
        # synthetic cell or x-cluster.
        band_box=union(band)
        row_words=[x for x in words if box(x) and contains(bb,box(x))
                   and box(x)[3]>=band_box[1] and box(x)[1]<=band_box[3]]
        clusters=cluster_records(row_words,height); matches=match_clusters(header_clusters,clusters,height)
        if len(matches)>=2: rows.append((band,row_words,clusters,matches))
    units=[x for x in members if "（単位：百万円）" in glyph(x)]
    if len(rows)<2: return {"status":"structurally_ambiguous","reason":"fewer-than-two-row-bands-repeating-header-clusters","block":block,"members":members,"header":header}
    if is_a02 and not units: return {"status":"structurally_ambiguous","reason":"missing-local-hyakuman-unit-anchor","block":block,"members":members,"header":header}
    return {"status":"structurally_supported","block":block,"members":members,"header":header,"headerWords":header_words,"headerClusters":header_clusters,"rows":rows[:2],"units":units,"height":height}


def execute(root,out_root,authority,directory,profile):
    base=root/"fixtures/document-understanding/batch-001/authorities"/directory
    records=[json.loads(x) for x in (base/"source-observations.jsonl").read_text(encoding="utf-8").splitlines() if x]
    pages=defaultdict(list)
    for x in records: pages[x["pdfPageIndex"]].append(x)
    out=out_root/"fixtures/document-understanding/batch-001/authorities"/directory/"s3-repaired-v2"; out.mkdir(parents=True,exist_ok=True)
    nodes=[]; edges=[]; summaries=[]; candidates=[]; treatments=[]
    for index,items in sorted(pages.items()):
        page=next(x for x in items if x["observationKind"]=="page"); lines=[x for x in items if x["observationKind"]=="textLine"]; words=[x for x in items if x["observationKind"]=="word"]; blocks=[x for x in items if x["observationKind"]=="textBlock"]
        pnode=page_node(authority,page); nodes.append(pnode); height=page_height(lines); bands=y_bands(lines); outer=None
        for seed in bands:
            sb=union(seed); window=[line for band in bands for line in band if union(band)[1]<=sb[3]+height and union(band)[3]>=sb[1]-height]
            header=outer_header(window,words)
            if not header: continue
            groups,gboxes=header; hbox=union([x for g in groups for x in g]); rows=[]
            for band in bands:
                if union(band)[1]<=hbox[3]+height: continue
                row_words=words_in_window(words,union(band)); matches=[i for i,b in enumerate(gboxes) if any(box(w)[0]<=b[2]+height and box(w)[2]>=b[0]-height for w in row_words if box(w))]
                if len(matches)>=2: rows.append((band,matches))
            if len(rows)>=2:
                supports=[page,*[x for g in groups for x in g],*[x for b,_ in rows[:2] for x in b]]
                input_value={"headerBandObservationIds":[x["observationId"] for x in window],"headerGroups":[[x["observationId"] for x in g] for g in groups],"headerUnionBBoxes":gboxes,"pageMaximumObservedLineHeight":height,"headerBandMembershipRule":"root-band bbox expanded by page maximum observed line height; no chained page-wide band","repeatingRowBands":[[x["observationId"] for x in b] for b,_ in rows[:2]],"rowHeaderGroupMatches":[m for _,m in rows[:2]],"samePageOnly":True,"noPageWideTokenRule":True}
                outer=inferred_node(authority,"outerLedger",OUTER,profile,page,supports,"structurally_supported","not_ambiguous",input_value); break
        if outer is None:
            supports=[page,* (bands[0] if bands else [])]
            outer=inferred_node(authority,"unclassifiedStructure",OUTER,profile,page,supports,"unclassified","insufficient-localized-header-and-repeated-row-pattern-evidence",{"pageMaximumObservedLineHeight":height,"samePageOnly":True,"noPageWideTokenRule":True})
        nodes.append(outer); edges.append(inferred_edge(pnode,outer,OUTER,profile,[page,*[x for x in records if x["observationId"] in outer["supportingObservationIds"]]],outer["structuralStatus"],outer["ambiguityState"],{"childDirectObservationIds":outer["supportingObservationIds"],"parentAnchorObservationIds":[page["observationId"]],"samePageOnly":True}))
        local_count=0
        for block in blocks:
            candidate=local_candidate(block,lines,words,authority=="shugiin")
            if not candidate: continue
            if candidate["status"]!="structurally_supported":
                # Preserve partial structural evidence, never promote it.
                supports=[page,block,*candidate.get("header",[])]; kind="ambiguousStructuralGroup"; status="structurally_ambiguous"; ambiguity=candidate["reason"]
                input_value={"candidateBlockObservationId":block["observationId"],"samePageOnly":True,"sourceOrderContiguityEvidence":{"candidateBlockSourceOrder":block["sourceOrder"],"memberLineSourceOrders":[x["sourceOrder"] for x in candidate.get("members",[])[:3]]},"ruleFailureReason":candidate["reason"]}
            else:
                supports=[page,block,*candidate["header"],*candidate["headerWords"],*(x for band,row_words,_,_ in candidate["rows"] for x in [*band,*row_words]),*candidate["units"]]
                kind="boundedLocalTable" if authority=="shugiin" else "nestedStructure"; status="structurally_supported"; ambiguity="not_ambiguous"
                input_value={"candidateBlockObservationId":block["observationId"],"headerAnchorObservationIds":[x["observationId"] for x in candidate["header"]],"headerAnchorUnionBBox":union(candidate["header"]),"headerXClusters":candidate["headerClusters"],"repeatingRowBands":[[x["observationId"] for x in band] for band,_,_,_ in candidate["rows"]],"rowXClusters":[clusters for _,_,clusters,_ in candidate["rows"]],"headerToRowClusterMatches":[matches for *_,matches in candidate["rows"]],"xClusterTolerance":candidate["height"],"xClusterToleranceBasis":"page maximum observed textLine height","localUnitAnchorObservationIds":[x["observationId"] for x in candidate["units"]],"samePageOnly":True,"sourceOrderContiguityEvidence":{"candidateBlockSourceOrder":block["sourceOrder"],"headerSourceOrders":[x["sourceOrder"] for x in candidate["header"]],"rowBandSourceOrders":[[x["sourceOrder"] for x in band] for band,_,_,_ in candidate["rows"]],"rowWordSourceOrders":[[x["sourceOrder"] for x in row_words] for _,row_words,_,_ in candidate["rows"]]},"boxGlyphFilter":"source-emitted raw text only; not PDF drawing or cell evidence"}
            local=inferred_node(authority,kind,LOCAL,profile,page,supports,status,ambiguity,input_value); nodes.append(local); local_count+=1
            edges.append(inferred_edge(pnode,local,LOCAL,profile,supports,status,ambiguity,{"childDirectObservationIds":[block["observationId"],*[x["observationId"] for x in candidate.get("header",[])]],"parentAnchorObservationIds":[page["observationId"]],"samePageOnly":True}))
            candidates.append({"pdfPageIndex":index,"blockObservationId":block["observationId"],"nodeId":local["nodeId"],"type":kind,"structuralStatus":status,"reason":candidate.get("reason","header-and-row-cluster-rule-satisfied")})
        summaries.append({"pdfPageIndex":index,"outerPartitionNodeId":outer["nodeId"],"outerPartitionStatus":outer["structuralStatus"],"localOrNestedGroupCount":local_count})
    if authority=="shugiin":
        local_by_block={n["ruleInput"].get("candidateBlockObservationId"):n for n in nodes if n["nodeType"] in {"boundedLocalTable","ambiguousStructuralGroup"}}
        for x in records:
            if x["observationKind"]!="textLine" or "百万円" not in text(x): continue
            found=[]
            for bid,n in local_by_block.items():
                block=next(z for z in records if z["observationId"]==bid)
                if contains(box(block),box(x)): found.append(n)
            if len(found)==1 and found[0]["structuralStatus"]=="structurally_supported": treatments.append({"observationId":x["observationId"],"pdfPageIndex":x["pdfPageIndex"],"treatment":"member_of_supported_boundedLocalTable","groupNodeId":found[0]["nodeId"],"blockObservationId":found[0]["ruleInput"]["candidateBlockObservationId"]})
            elif len(found)==1: treatments.append({"observationId":x["observationId"],"pdfPageIndex":x["pdfPageIndex"],"treatment":"member_of_ambiguous_structural_group","groupNodeId":found[0]["nodeId"],"reason":found[0]["ambiguityState"]})
            else: treatments.append({"observationId":x["observationId"],"pdfPageIndex":x["pdfPageIndex"],"treatment":"not_structurally_grouped_representation_limited","reason":"no-unique-supported-same-page-group"})
        treatments.sort(key=lambda x:(x["pdfPageIndex"],x["observationId"]))
    nodes.sort(key=lambda x:x["nodeId"]); edges.sort(key=lambda x:x["edgeId"]); write_jsonl(out/"nodes.jsonl",nodes); write_jsonl(out/"edges.jsonl",edges)
    manifest={"schemaVersion":1,"artifactType":"batch-001-wave-1-s3-repaired-v2-manifest","stage":"S3_REPAIRED_V2","stageStatus":"COMPLETE_NOT_CANONICAL_FROZEN","specVersion":SPEC,"namespace":NS,"authorityId":authority,"profileVersion":profile,"sourceSha256":next(x["sourceSha256"] for x in records if x["observationKind"]=="page"),"inputSourceObservations":{"path":f"fixtures/document-understanding/batch-001/authorities/{directory}/source-observations.jsonl","sha256":sha(base/"source-observations.jsonl")},"nodeCount":len(nodes),"edgeCount":len(edges),"countsByStructuralStatus":dict(sorted(Counter(x.get("structuralStatus","source_observed") for x in nodes).items())),"pageSummaries":summaries,"crossPageInferredStructuralEdgeCount":0,"crossFileInferredStructuralEdgeCount":0,"documentMembershipEdgeCount":0,"outerLocalUnitInheritanceEdgeCount":0,"normalizationStatus":"not_created","semanticCandidateStatus":"not_created","financialAssociationStatus":"not_created","canonicalFreezeStatus":"not_created"}
    manifest["a01NestedCandidateAudit" if authority=="kunaicho" else "a02HyakumanYenReconciliation"]=candidates if authority=="kunaicho" else treatments
    write_json(out/"structural-interpretation-manifest.json",manifest)
    procedure=sha(Path(__file__)); execution={"schemaVersion":1,"artifactType":"batch-001-wave-1-s3-repair-v2-execution-manifest","executionRevision":"v2","specVersion":SPEC,"namespace":NS,"authorityId":authority,"profileVersion":profile,"sourceSha256":manifest["sourceSha256"],"procedure":{"path":"fixtures/document-understanding/batch-001/s3_repaired_v2_execution.py","sha256":procedure},"idPolicy":{"nodeAndEdgeInputs":["specVersion","sourceSha256","fileId","pdfPageIndex","structural primitive type","inferenceRule","sorted supportingObservationIds"],"edgePrimitive":EDGE_PRIMITIVE,"parentOrChildIdsExcluded":True},"serialization":{"encoding":"UTF-8","newlines":"LF","jsonKeyOrder":"sorted","recordOrder":"stable ID ascending","absolutePathsExcluded":True},"v1OutputPreserved":True,"documentContainmentOmittedFromPageScopedGraph":True}
    write_json(out/"repair-execution-manifest.json",execution)
    return {"authority":authority,"directory":directory,"out":out,"nodes":nodes,"edges":edges,"manifest":manifest}


def main():
    p=argparse.ArgumentParser();p.add_argument("--repo",type=Path,default=Path.cwd());p.add_argument("--out-root",type=Path);args=p.parse_args();root=args.repo.resolve();out_root=args.out_root.resolve() if args.out_root else root
    spec=json.loads((root/"fixtures/document-understanding/batch-001/wave-1-s3-structural-repair-spec.json").read_text(encoding="utf-8"))
    if spec["specVersion"]!=SPEC:raise SystemExit("frozen spec mismatch")
    for authority,d in [("kunaicho","authority-01-kunaicho"),("shugiin","authority-02-shugiin")]:
        base=root/"fixtures/document-understanding/batch-001/authorities"/d
        for rel,want in spec["immutableBaseline"]["authorityArtifactHashes"][authority].items():
            if sha(base/rel)!=want:raise SystemExit(f"immutable baseline mismatch: {authority} {rel}")
    result=[execute(root,out_root,"kunaicho","authority-01-kunaicho","batch-001-wave-1-a01-v1"),execute(root,out_root,"shugiin","authority-02-shugiin","batch-001-wave-1-a02-v1")]
    print(dump({"status":"ok","authorities":[{"authority":x["authority"],"nodes":len(x["nodes"]),"edges":len(x["edges"])} for x in result]}))


if __name__=="__main__":main()
