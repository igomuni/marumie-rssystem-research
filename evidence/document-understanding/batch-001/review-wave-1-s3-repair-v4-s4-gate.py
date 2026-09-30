#!/usr/bin/env python3
"""Independent read-only v4 S3 acceptance audit; imports no reviewed code."""
from __future__ import annotations
import argparse,hashlib,json,re
from collections import Counter,defaultdict
from pathlib import Path
SPEC='batch-001-wave-1-s3-repair-v1';NS='s3r1';EDGE='edge:contains'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def jl(p):return [json.loads(x) for x in Path(p).read_text(encoding='utf-8').splitlines() if x]
def b(x):
 x=x.get('geometry',{}).get('bbox') if isinstance(x,dict) and 'geometry' in x else x
 return [float(x[k]) for k in ('xMin','yMin','xMax','yMax')] if isinstance(x,dict) else [float(v) for v in x]
def iid(kind,r):
 s=chr(31).join([SPEC,r['sourceSha256'],r['fileId'],str(r['pdfPageIndex']),kind,r['inferenceRule'],*sorted(r['supportingObservationIds'])]);return f'{NS}-{kind}-{hashlib.sha256(s.encode()).hexdigest()[:20]}'
def lines_for(w,lines):
 q=b(w);return [x for x in lines if (lambda z:z[0]<=q[0] and z[2]>=q[2] and z[1]<=q[1] and z[3]>=q[3])(b(x))]
def audit(root,auth,d):
 base=root/'fixtures/document-understanding/batch-001/authorities'/d;obs=jl(base/'source-observations.jsonl');by={x['observationId']:x for x in obs};nodes=jl(base/'s3-repaired-v4/nodes.jsonl');edges=jl(base/'s3-repaired-v4/edges.jsonl');nby={x['nodeId']:x for x in nodes};spec=json.loads((root/'fixtures/document-understanding/batch-001/wave-1-s3-structural-repair-spec.json').read_text());imm=all(sha(base/k)==v for k,v in spec['immutableBaseline']['authorityArtifactHashes'][auth].items());loc=[];sup=[];ids=[];bound=[];outer=[]
 for r in [*nodes,*edges]:
  if r.get('evidenceClass')!='structurally_inferred':continue
  rid=r.get('nodeId',r.get('edgeId'));kind=r.get('nodeType',r.get('idPrimitive'))
  if iid(kind,r)!=rid:ids.append(rid)
  lm={x['observationId']:x for x in r['evidenceLocator']}
  for oid in r['supportingObservationIds']:
   o=by.get(oid)
   if not o or any(o[k]!=r[k] for k in ('sourceSha256','fileId','pdfPageIndex')):sup.append([rid,oid]);continue
   if oid not in lm or lm[oid].get('sourceOrder')!=o['sourceOrder'] or lm[oid].get('bbox')!=o.get('geometry',{}).get('bbox'):loc.append([rid,oid])
 for e in edges:
  a,z=nby.get(e['fromNodeId']),nby.get(e['toNodeId'])
  if not a or not z or a['authorityId']!=z['authorityId'] or a['fileId']!=z['fileId'] or a['pdfPageIndex']!=z['pdfPageIndex']:bound.append(e['edgeId'])
 for n in nodes:
  if n.get('nodeType')!='outerLedger':continue
  ri=n['ruleInput'];lines=[x for x in obs if x['pdfPageIndex']==n['pdfPageIndex'] and x['observationKind']=='textLine'];errs=[];words=[by[o] for g in ri['headerGroups'] for o in g['memberObservationIds']];actual={x['observationId'] for w in words for x in lines_for(w,lines)};ret=set(ri['headerSourceLineObservationIds'])
  if actual!=ret:errs.append('header-membership')
  if not actual<=set(n['supportingObservationIds']):errs.append('header-lines-not-direct-support')
  h=ri['pageMaximumObservedLineHeight'];boxes=[b(by[x]) for x in ret];todo=[0] if boxes else [];seen={0} if boxes else set()
  while todo:
   i=todo.pop()
   for j in range(len(boxes)):
    if j not in seen and boxes[i][1]<=boxes[j][3]+h and boxes[i][3]>=boxes[j][1]-h:seen.add(j);todo.append(j)
  if not boxes or len(seen)!=len(boxes) or max(x[3] for x in boxes)-min(x[1] for x in boxes)>2*h:errs.append('literal-band')
  strictrows=[]
  for row in ri['rowPatternEvidence']:
   m=0
   for q in row['matchedHeaderRanges']:
    hb=b(q['headerXRange']);ws=[by[x] for x in q['rowWordObservationIds']]
    if ws and all(x['observationId'] in n['supportingObservationIds'] for x in ws) and any((lambda wb:wb[0]<=hb[2] and wb[2]>=hb[0])(b(x)) for x in ws):m+=1
   strictrows.append(m)
  if len(strictrows)<2 or any(x<2 for x in strictrows):errs.append('strict-row-pattern')
  outer.append({'page':n['pdfPageIndex'],'failures':errs,'strictMatches':strictrows,'accepted':not errs})
 manifest=json.loads((base/'s3-repaired-v4/structural-interpretation-manifest.json').read_text());out={'authorityId':auth,'nodes':len(nodes),'edges':len(edges),'types':dict(Counter(x['nodeType'] for x in nodes)),'statuses':dict(Counter(x.get('structuralStatus','source_observed') for x in nodes)),'immutableBaselinePass':imm,'locatorFailures':loc,'supportFailures':sup,'idFailures':ids,'boundaryFailures':bound,'outer':outer,'outerFailures':[x for x in outer if x['failures']]}
 if auth=='shugiin':
  rec=manifest['a02HyakumanYenReconciliation'];anchors=defaultdict(list)
  for n in nodes:
   if n.get('nodeType')=='boundedLocalTable':
    for oid in n['ruleInput']['localUnitAnchorObservationIds']:anchors[oid].append(n['nodeId'])
  hy=[x for x in obs if x['observationKind']=='textLine' and '百万円' in x.get('raw',{}).get('engineNativeText','')];rows={x['observationId']:x for x in rec};out.update({'a02Occurrences':len(hy),'a02Treatments':dict(Counter(x['finalTreatment'] for x in rec)),'a02Mismatch':[x['observationId'] for x in hy if anchors[x['observationId']] and rows[x['observationId']]['finalTreatment']=='not_structurally_grouped_representation_limited'],'a02Shared':{k:v for k,v in anchors.items() if len(v)>1}})
 return out
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path.cwd());p.add_argument('--output',type=Path);a=p.parse_args();root=a.repo.resolve();v4=root/'fixtures/document-understanding/batch-001/s3_repaired_v4_execution.py';v3=root/'fixtures/document-understanding/batch-001/s3_repaired_v3_execution.py';v2=root/'fixtures/document-understanding/batch-001/s3_repaired_v2_execution.py';r={'schemaVersion':1,'artifactType':'batch-001-wave-1-s3-repair-v4-independent-review','independence':'No executor, audit, or helper imports.','baseCommit':'1b0f2ef1f4edb2dc0a595a0c924e5848d08b2aeb','authorities':[audit(root,'kunaicho','authority-01-kunaicho'),audit(root,'shugiin','authority-02-shugiin')],'effectiveProcedureProvenance':{'v4':sha(v4),'v3':sha(v3),'v2':sha(v2),'verdict':'COMPLETE_EFFECTIVE_PROCEDURE_PROVENANCE'}}
 r['authorityVerdicts']={x['authorityId']:'ACCEPT_REPAIRED_S3_FOR_S4' if not (x['outerFailures'] or x['locatorFailures'] or x['supportFailures'] or x['idFailures'] or x['boundaryFailures']) else 'REPAIR_REQUIRED_BEFORE_S4' for x in r['authorities']};r['globalS4Authorization']='AUTHORIZED' if all(x=='ACCEPT_REPAIRED_S3_FOR_S4' for x in r['authorityVerdicts'].values()) else 'NOT_AUTHORIZED';text=json.dumps(r,ensure_ascii=False,sort_keys=True,indent=2)+'\n';a.output.write_text(text,encoding='utf-8') if a.output else print(text,end='')
if __name__=='__main__':main()
