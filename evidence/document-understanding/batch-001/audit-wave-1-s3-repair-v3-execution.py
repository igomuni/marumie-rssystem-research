#!/usr/bin/env python3
"""Independent, read-only v3 execution audit; never imports either executor."""
from __future__ import annotations
import argparse,hashlib,json
from collections import Counter,defaultdict
from pathlib import Path
SPEC='batch-001-wave-1-s3-repair-v1';NS='s3r1';EDGE='edge:contains'
HISTORY={'authority-01-kunaicho':{'s3-repaired-v1/nodes.jsonl':'6d85ab08503e8495e36af72b0544b4dc3bafb6057359f2af3db4ee290bbb6156','s3-repaired-v1/edges.jsonl':'7bb247babf7e1c8a90c5379dd1e640c1108706aa9fd9c9d769f63395cdf65cd3','s3-repaired-v2/nodes.jsonl':'45564b6ef46a4fdef61358c7c07b8c5a9a8d309dd95c303d40d5400c0422288c','s3-repaired-v2/edges.jsonl':'7597c1c8fdd0766837e2f4f349482c793ee2c0be059806476263d9a5b43a43dd'},'authority-02-shugiin':{'s3-repaired-v1/nodes.jsonl':'16b2bcd1c6c5676b6cd3500951a4ad464fe7a1bd70c958deb22d37abbf3637ac','s3-repaired-v1/edges.jsonl':'95318747f9f20157ffde7e060e693e1aa0c0a1fe9a95d4989b4371767d4e82e0','s3-repaired-v2/nodes.jsonl':'8923c3d70b38d9c5dfb11383b25fcd44522b27872ab91a936f4ad9c912702b7f','s3-repaired-v2/edges.jsonl':'42236fbc1d0df56fff72421976539ff0d6f3b1e3ab8e85545228c523dcfc6ff4'}}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def jl(p):return [json.loads(x) for x in Path(p).read_text(encoding='utf-8').splitlines() if x]
def bid(r):
 b=r.get('geometry',{}).get('bbox');return [float(x) for x in b] if isinstance(b,list) else [float(b[k]) for k in ('xMin','yMin','xMax','yMax')]
def iid(kind,r):
 s=chr(31).join([SPEC,r['sourceSha256'],r['fileId'],str(r['pdfPageIndex']),kind,r['inferenceRule'],*sorted(r['supportingObservationIds'])]);return f'{NS}-{kind}-{hashlib.sha256(s.encode()).hexdigest()[:20]}'
def audit(root,d,auth,spec):
 base=root/'fixtures/document-understanding/batch-001/authorities'/d; obs=jl(base/'source-observations.jsonl');by={x['observationId']:x for x in obs};nodes=jl(base/'s3-repaired-v3/nodes.jsonl');edges=jl(base/'s3-repaired-v3/edges.jsonl');nby={x['nodeId']:x for x in nodes}
 imm=all(sha(base/k)==v for k,v in spec['immutableBaseline']['authorityArtifactHashes'][auth].items()); history=all(sha(base/k)==v for k,v in HISTORY[d].items())
 loc=[];ids=[];support=[];boundary=[];outer=[];local=[]
 for r in [*nodes,*edges]:
  if r.get('evidenceClass')!='structurally_inferred':continue
  kind=r.get('nodeType',r.get('idPrimitive'));actual=r.get('nodeId',r.get('edgeId'))
  if iid(kind,r)!=actual:ids.append(actual)
  got={x['observationId']:x for x in r['evidenceLocator']}
  for oid in r['supportingObservationIds']:
   o=by.get(oid)
   if not o or any(r[k]!=o[k] for k in ('sourceSha256','fileId','pdfPageIndex')):support.append([actual,oid]);continue
   if oid not in got or got[oid].get('sourceOrder')!=o['sourceOrder'] or got[oid].get('bbox')!=o.get('geometry',{}).get('bbox'):loc.append([actual,oid])
 for e in edges:
  a,b=nby.get(e['fromNodeId']),nby.get(e['toNodeId'])
  if not a or not b or a['pdfPageIndex']!=b['pdfPageIndex'] or a['fileId']!=b['fileId']:boundary.append(e['edgeId'])
 for n in nodes:
  if n.get('nodeType')=='outerLedger':
   ri=n['ruleInput']; h=ri['literalHeaderBand']['pageMaximumObservedLineHeight']; lineids=ri['literalHeaderBand']['memberLineObservationIds']; groups=ri['headerGroups']; rows=ri['rowPatternEvidence']; fail=False
   if not lineids or len(groups)!=5 or len(rows)<2:fail=True
   for row in rows:
    if len(row['matchedHeaderRanges'])<2:fail=True
    for m in row['matchedHeaderRanges']:
     ids2=m['rowWordObservationIds']
     if not ids2 or any(x not in n['supportingObservationIds'] or x not in by or by[x]['observationKind']!='word' for x in ids2):fail=True
     xs=[bid(by[x]) for x in ids2]
     if m['rowWordBBoxes']!=xs:fail=True
   # literal non-chained band check with retained header group geometry
   allboxes=[g['unionBBox'] for g in groups]
   if max(x[3] for x in allboxes)-min(x[1] for x in allboxes)>2*h:fail=True
   if fail:outer.append(n['nodeId'])
  if n.get('nodeType') in {'nestedStructure','boundedLocalTable'}:
   ri=n['ruleInput']; clusters=ri.get('headerXClusters',[]);rows=ri.get('rowXClusters',[]);matches=ri.get('headerToRowClusterMatches',[]);fail=not(len(clusters)>=2 and len(rows)>=2 and len(matches)>=2 and all(len(x)>=2 for x in matches))
   for cs in [clusters,*rows]:
    for c in cs:
     xs=[bid(by[x]) for x in c['memberObservationIds']]
     if c['xRange']!=[min(x[0] for x in xs),max(x[2] for x in xs)]:fail=True
   if fail:local.append(n['nodeId'])
 out={'authorityId':auth,'immutableBaselinePass':imm,'reviewedV1V2CoreHashPass':history,'nodes':len(nodes),'edges':len(edges),'nodeTypes':dict(Counter(x['nodeType'] for x in nodes)),'statuses':dict(Counter(x.get('structuralStatus','source_observed') for x in nodes)),'locatorFailures':loc,'supportFailures':support,'idFailures':ids,'boundaryFailures':boundary,'outerRuleFailures':outer,'localRuleFailures':local}
 if auth=='shugiin':
  m=json.loads((base/'s3-repaired-v3/structural-interpretation-manifest.json').read_text());rec=m['a02HyakumanYenReconciliation'];anchor_mismatch=[x['observationId'] for x in rec if x['directUnitAnchorGroupIds'] and x['finalTreatment']=='not_structurally_grouped_representation_limited'];out['a02Treatments']=dict(Counter(x['finalTreatment'] for x in rec));out['a02Count']=len(rec);out['a02AnchorTreatmentMismatches']=anchor_mismatch;out['a02SharedAnchors']={k:v for k,v in Counter(y for x in rec for y in x['directUnitAnchorGroupIds']).items() if v>1}
 return out
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path.cwd());a=p.parse_args();root=a.repo.resolve();spec=json.loads((root/'fixtures/document-understanding/batch-001/wave-1-s3-structural-repair-spec.json').read_text());r=[audit(root,'authority-01-kunaicho','kunaicho',spec),audit(root,'authority-02-shugiin','shugiin',spec)];print(json.dumps({'schemaVersion':1,'audit':'independent-v3-execution-audit','authorities':r},ensure_ascii=False,sort_keys=True,indent=2))
if __name__=='__main__':main()
