#!/usr/bin/env python3
"""Independent acceptance audit for the Wave 1 S3 repair v2 gate.

It intentionally does not import the executor or its execution audit.  In
addition to preservation, locator, scope and ID checks, it tests whether the
graph's cited observations are enough to reproduce the frozen outer and local
geometry claims.  In particular, an outer row-band textLine is not treated as
word-level column evidence merely because it spans several columns.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

SPEC="batch-001-wave-1-s3-repair-v1"; NS="s3r1"; EDGE="edge:contains"
V1={
 "authority-01-kunaicho":{"s3-repaired-v1/nodes.jsonl":"6d85ab08503e8495e36af72b0544b4dc3bafb6057359f2af3db4ee290bbb6156","s3-repaired-v1/edges.jsonl":"7bb247babf7e1c8a90c5379dd1e640c1108706aa9fd9c9d769f63395cdf65cd3","s3-repaired-v1/structural-interpretation-manifest.json":"4b95b682f3efc71f875dd37f32ed1fc93d3e886a50031a95bbd77001d474c80d","s3-repaired-v1/repair-execution-manifest.json":"a6156fcd4500398adede65d51634714867a3b5183fa1ba6873b95ffda61eca39"},
 "authority-02-shugiin":{"s3-repaired-v1/nodes.jsonl":"16b2bcd1c6c5676b6cd3500951a4ad464fe7a1bd70c958deb22d37abbf3637ac","s3-repaired-v1/edges.jsonl":"95318747f9f20157ffde7e060e693e1aa0c0a1fe9a95d4989b4371767d4e82e0","s3-repaired-v1/structural-interpretation-manifest.json":"6b065f974604afa94e346710c80c5ad09dba69d6ac7bf3d8572b6e247ab5db3c","s3-repaired-v1/repair-execution-manifest.json":"3e07e3dc8e5eac3ade89950301390e2417f7b2768decbee278b41590cd4e42f3"}}

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def jl(p): return [json.loads(x) for x in Path(p).read_text(encoding="utf-8").splitlines() if x]
def sid(kind,r):
 bits=[SPEC,r["sourceSha256"],r["fileId"],str(r["pdfPageIndex"]),kind,r["inferenceRule"],*sorted(r["supportingObservationIds"])]
 return f"{NS}-{kind}-{hashlib.sha256(chr(31).join(bits).encode()).hexdigest()[:20]}"
def bb(r):
 b=r.get("geometry",{}).get("bbox")
 if not b:return None
 return [float(x) for x in b] if isinstance(b,list) else [float(b[k]) for k in ("xMin","yMin","xMax","yMax")]
def inside(outer,inner): return outer and inner and inner[0]>=outer[0] and inner[1]>=outer[1] and inner[2]<=outer[2] and inner[3]<=outer[3]
def overlap(a,b): return a and b and min(a[2],b[2])>max(a[0],b[0]) and min(a[3],b[3])>max(a[1],b[1])

def audit(root,directory,spec):
 base=root/"fixtures/document-understanding/batch-001/authorities"/directory; auth="kunaicho" if directory.endswith("kunaicho") else "shugiin"
 obs=jl(base/"source-observations.jsonl"); by={x["observationId"]:x for x in obs}
 nodes=jl(base/"s3-repaired-v2/nodes.jsonl"); edges=jl(base/"s3-repaired-v2/edges.jsonl"); nby={x["nodeId"]:x for x in nodes}
 immutable={k:sha(base/k)==v for k,v in spec["immutableBaseline"]["authorityArtifactHashes"][auth].items()}; v1={k:sha(base/k)==v for k,v in V1[directory].items()}
 locfail=[]; supportfail=[]; idfail=[]
 for r in [*nodes,*edges]:
  if r.get("evidenceClass")!="structurally_inferred":continue
  if r.get("nodeType") or r.get("idPrimitive"):
   kind=r.get("nodeType",r.get("idPrimitive")); actual=r.get("nodeId",r.get("edgeId"))
   if sid(kind,r)!=actual:idfail.append(actual)
  for oid in r.get("supportingObservationIds",[]):
   o=by.get(oid)
   if not o or any(r[k]!=o[k] for k in ("sourceSha256","fileId","pdfPageIndex")):supportfail.append([r.get("nodeId",r.get("edgeId")),oid])
  got={x["observationId"]:x for x in r.get("evidenceLocator",[])}
  for oid in r.get("supportingObservationIds",[]):
   o=by.get(oid); l=got.get(oid)
   if not l or l.get("sourceOrder")!=o.get("sourceOrder") or l.get("bbox")!=o.get("geometry",{}).get("bbox"):locfail.append([r.get("nodeId",r.get("edgeId")),oid])
 endpoints=[]; crosspage=[]; crossfile=[]; outerlocal=[]
 for e in edges:
  a=nby.get(e["fromNodeId"]);b=nby.get(e["toNodeId"])
  if not a or not b:endpoints.append(e["edgeId"]);continue
  if a["pdfPageIndex"]!=b["pdfPageIndex"]:crosspage.append(e["edgeId"])
  if a["fileId"]!=b["fileId"]:crossfile.append(e["edgeId"])
  if {a.get("nodeType"),b.get("nodeType")} & {"outerLedger"} and {a.get("nodeType"),b.get("nodeType")} & {"nestedStructure","boundedLocalTable"}:outerlocal.append(e["edgeId"])
 # Outer requirement: output has row-line supports, but its ruleInput retains
 # only line IDs/match indices.  Independently prove whether the required
 # word-level x evidence is actually cited in the inferred record.
 outers=[x for x in nodes if x.get("nodeType")=="outerLedger"]
 outer_word_evidence_omissions=[]; outer_band_fail=[]
 for n in outers:
  ri=n["ruleInput"]; row_ids={oid for row in ri.get("repeatingRowBands",[]) for oid in row}; word_ids={oid for oid in n["supportingObservationIds"] if by[oid].get("observationKind")=="word"}
  # The executor supplies no word IDs per row; word observations are required
  # to reconstruct a repeated header x-range rather than a broad line bbox.
  if row_ids and not any(oid in word_ids for oid in row_ids): outer_word_evidence_omissions.append(n["nodeId"])
  # Literal local-band sanity: all cited header word bboxes must fit within a
  # one-height-tolerance vertical band; this does not repair the row defect.
  hs=[by[oid] for g in ri.get("headerGroups",[]) for oid in g]
  ys=[bb(x) for x in hs if bb(x)]; h=float(ri.get("pageMaximumObservedLineHeight",0))
  if ys and max(x[3] for x in ys)-min(x[1] for x in ys)>2*h:outer_band_fail.append(n["nodeId"])
 local=[x for x in nodes if x.get("nodeType") in {"nestedStructure","boundedLocalTable"}]
 local_fail=[]
 for n in local:
  ri=n["ruleInput"]; hc=ri.get("headerXClusters",[]); rows=ri.get("rowXClusters",[]); matches=ri.get("headerToRowClusterMatches",[])
  # Independently recompute each emitted range from its S2 word members.
  bad=not(len(hc)>=2 and len(rows)>=2 and len(matches)>=2 and all(len(m)>=2 for m in matches))
  for clusters in [hc,*rows]:
   for c in clusters:
    xs=[bb(by[oid]) for oid in c.get("memberObservationIds",[]) if oid in by]
    if not xs or c.get("xRange") != [min(x[0] for x in xs),max(x[2] for x in xs)]:bad=True
  if bad:local_fail.append(n["nodeId"])
 result={"authorityId":auth,"immutableBaselinePass":all(immutable.values()),"reviewedV1Pass":all(v1.values()),"nodeCount":len(nodes),"edgeCount":len(edges),"nodeTypes":dict(Counter(x.get("nodeType") for x in nodes)),"statuses":dict(Counter(x.get("structuralStatus","source_observed") for x in nodes)),"locatorFailures":locfail,"supportIdentityFailures":supportfail,"directTupleIdFailures":idfail,"endpointFailures":endpoints,"crossPageEdges":crosspage,"crossFileEdges":crossfile,"outerLocalDirectEdges":outerlocal,"outerLedgers":len(outers),"outerLiteralBandFailures":outer_band_fail,"outerRowWordEvidenceOmissions":outer_word_evidence_omissions,"localClusterFailures":local_fail}
 if auth=="shugiin":
  units=[x for x in obs if x["observationKind"]=="textLine" and "百万円" in x.get("raw",{}).get("engineNativeText","")]
  tables=[x for x in local if x["nodeType"]=="boundedLocalTable"]; contain=Counter(); unit_use=defaultdict(list); overlaps=[]; entries=[]
  for t in tables:
   for u in t["ruleInput"].get("localUnitAnchorObservationIds",[]):unit_use[u].append(t["nodeId"])
  for u in units:
   groups=[t["nodeId"] for t in tables if t["pdfPageIndex"]==u["pdfPageIndex"] and inside(bb(t),bb(u))]
   contain[len(groups)]+=1; entries.append({"observationId":u["observationId"],"pdfPageIndex":u["pdfPageIndex"],"sourceOrder":u["sourceOrder"],"bbox":u["geometry"]["bbox"],"containingSupportedGroupIds":groups,"unitAnchorGroupIds":unit_use.get(u["observationId"],[])})
  for i,a in enumerate(tables):
   for b in tables[i+1:]:
    if a["pdfPageIndex"]==b["pdfPageIndex"] and overlap(bb(a),bb(b)):overlaps.append([a["nodeId"],b["nodeId"]])
  manifest=json.loads((base/"s3-repaired-v2/structural-interpretation-manifest.json").read_text())
  treatments={x["observationId"]:x for x in manifest["a02HyakumanYenReconciliation"]}
  anchor_treatment_mismatches=[e["observationId"] for e in entries if e["unitAnchorGroupIds"] and treatments[e["observationId"]]["treatment"]!="member_of_supported_boundedLocalTable"]
  result.update({"a02HyakumanCount":len(units),"a02HyakumanContainmentDistribution":dict(contain),"a02SharedUnitAnchors":{k:v for k,v in unit_use.items() if len(v)>1},"a02SupportedTableOverlaps":overlaps,"a02ManifestTreatments":dict(Counter(x["treatment"] for x in treatments.values())),"a02AnchorTreatmentMismatches":anchor_treatment_mismatches,"a02HyakumanEntries":entries})
 return result

def main():
 p=argparse.ArgumentParser();p.add_argument("--repo",type=Path,default=Path.cwd());a=p.parse_args();root=a.repo.resolve();spec=json.loads((root/"fixtures/document-understanding/batch-001/wave-1-s3-structural-repair-spec.json").read_text())
 out=[audit(root,"authority-01-kunaicho",spec),audit(root,"authority-02-shugiin",spec)]
 print(json.dumps({"schemaVersion":1,"audit":"independent-v2-acceptance-review","specVersion":SPEC,"authorities":out},ensure_ascii=False,sort_keys=True,indent=2))
if __name__=="__main__":main()
