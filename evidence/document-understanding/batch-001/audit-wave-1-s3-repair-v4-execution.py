#!/usr/bin/env python3
"""Read-only v4 execution audit; does not import any executor or helper."""
from __future__ import annotations
import argparse, hashlib, json
from collections import Counter, defaultdict
from pathlib import Path

SPEC='batch-001-wave-1-s3-repair-v1'; NS='s3r1'; EDGE='edge:contains'

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def jl(p): return [json.loads(x) for x in Path(p).read_text(encoding='utf-8').splitlines() if x]
def b(x):
 x=x.get('geometry',{}).get('bbox') if isinstance(x,dict) and 'geometry' in x else x
 return [float(x[k]) for k in ('xMin','yMin','xMax','yMax')] if isinstance(x,dict) else [float(v) for v in x]
def iid(kind,r):
 s=chr(31).join([SPEC,r['sourceSha256'],r['fileId'],str(r['pdfPageIndex']),kind,r['inferenceRule'],*sorted(r['supportingObservationIds'])])
 return f'{NS}-{kind}-{hashlib.sha256(s.encode()).hexdigest()[:20]}'
def source_lines(word,lines):
 w=b(word);return [x for x in lines if (lambda z:z[0]<=w[0] and z[2]>=w[2] and z[1]<=w[1] and z[3]>=w[3])(b(x))]
def audit(root,authority,directory):
 base=root/'fixtures/document-understanding/batch-001/authorities'/directory; obs=jl(base/'source-observations.jsonl'); by={x['observationId']:x for x in obs}; nodes=jl(base/'s3-repaired-v4/nodes.jsonl'); edges=jl(base/'s3-repaired-v4/edges.jsonl'); nby={x['nodeId']:x for x in nodes}
 spec=json.loads((root/'fixtures/document-understanding/batch-001/wave-1-s3-structural-repair-spec.json').read_text()); imm={k:sha(base/k)==v for k,v in spec['immutableBaseline']['authorityArtifactHashes'][authority].items()}
 locator=[]; support=[]; ids=[]; boundary=[]; outer=[]; local=[]
 for r in [*nodes,*edges]:
  if r.get('evidenceClass')!='structurally_inferred':continue
  ident=r.get('nodeId',r.get('edgeId')); kind=r.get('nodeType',r.get('idPrimitive'))
  if iid(kind,r)!=ident:ids.append(ident)
  loc={x['observationId']:x for x in r.get('evidenceLocator',[])}
  for oid in r['supportingObservationIds']:
   o=by.get(oid)
   if not o or any(o[k]!=r[k] for k in ('sourceSha256','fileId','pdfPageIndex')):support.append([ident,oid]);continue
   if oid not in loc or loc[oid].get('sourceOrder')!=o.get('sourceOrder') or loc[oid].get('bbox')!=o.get('geometry',{}).get('bbox'):locator.append([ident,oid])
 for e in edges:
  a,z=nby.get(e['fromNodeId']),nby.get(e['toNodeId'])
  if not a or not z or a['pdfPageIndex']!=z['pdfPageIndex'] or a['fileId']!=z['fileId'] or a['authorityId']!=z['authorityId']:boundary.append(e['edgeId'])
 for n in nodes:
  if n.get('nodeType')=='outerLedger':
   ri=n['ruleInput']; lines=[x for x in obs if x['pdfPageIndex']==n['pdfPageIndex'] and x['observationKind']=='textLine']; err=[]
   header_words=[by[oid] for g in ri['headerGroups'] for oid in g['memberObservationIds']]
   actual={x['observationId'] for w in header_words for x in source_lines(w,lines)}; retained=set(ri['headerSourceLineObservationIds'])
   if actual!=retained:err.append('header-word-to-source-line-membership-incomplete')
   if not actual.issubset(set(n['supportingObservationIds'])):err.append('header-source-lines-omitted-from-direct-support')
   h=ri['pageMaximumObservedLineHeight']; lbs=[b(by[x]) for x in retained]; todo=[0] if lbs else []; seen={0} if lbs else set()
   while todo:
    i=todo.pop()
    for j in range(len(lbs)):
     if j not in seen and lbs[i][1]<=lbs[j][3]+h and lbs[i][3]>=lbs[j][1]-h:seen.add(j);todo.append(j)
   if not lbs or len(seen)!=len(lbs) or max(x[3] for x in lbs)-min(x[1] for x in lbs)>2*h:err.append('literal-local-header-band-not-reconstructible')
   rows=ri['rowPatternEvidence']
   if len(rows)<2:err.append('fewer-than-two-row-bands')
   for row in rows:
    strict=0
    for m in row['matchedHeaderRanges']:
     hb=b(m['headerXRange']); ws=[by[x] for x in m['rowWordObservationIds']]
     if not ws or any(x['observationId'] not in n['supportingObservationIds'] for x in ws):err.append('row-word-direct-support-missing');continue
     if any((lambda wb:wb[0]<=hb[2] and wb[2]>=hb[0])(b(w)) for w in ws):strict+=1
    if strict<2:err.append('row-band-lacks-two-strict-x-overlaps')
   outer.append({'nodeId':n['nodeId'],'pdfPageIndex':n['pdfPageIndex'],'failures':sorted(set(err))})
  if n.get('nodeType') in {'nestedStructure','boundedLocalTable'}:
   ri=n['ruleInput']; err=[]
   if len(ri.get('headerXClusters',[]))<2 or len(ri.get('rowXClusters',[]))<2 or any(len(x)<2 for x in ri.get('headerToRowClusterMatches',[])):err.append('cluster-evidence-incomplete')
   if n['nodeType']=='boundedLocalTable' and not ri.get('localUnitAnchorObservationIds'):err.append('missing-local-unit-anchor')
   local.append({'nodeId':n['nodeId'],'failures':err})
 out={'authorityId':authority,'immutableBaselineHashPass':all(imm.values()),'nodes':len(nodes),'edges':len(edges),'nodeTypes':dict(Counter(x['nodeType'] for x in nodes)),'statuses':dict(Counter(x.get('structuralStatus','source_observed') for x in nodes)),'locatorFailures':locator,'supportFailures':support,'idFailures':ids,'boundaryFailures':boundary,'outerFailures':[x for x in outer if x['failures']],'outerAudit':outer,'localFailures':[x for x in local if x['failures']]}
 manifest=json.loads((base/'s3-repaired-v4/structural-interpretation-manifest.json').read_text())
 if authority=='shugiin':
  rec=manifest['a02HyakumanYenReconciliation']; anchors=defaultdict(list)
  for n in nodes:
   if n.get('nodeType')=='boundedLocalTable' and n.get('structuralStatus')=='structurally_supported':
    for oid in n['ruleInput']['localUnitAnchorObservationIds']:anchors[oid].append(n['nodeId'])
  hy=[x for x in obs if x['observationKind']=='textLine' and '百万円' in x.get('raw',{}).get('engineNativeText','')]; rows={x['observationId']:x for x in rec}
  out['a02OccurrenceCount']=len(hy);out['a02Treatments']=dict(Counter(x['finalTreatment'] for x in rec));out['a02AnchorTreatmentMismatches']=[x['observationId'] for x in hy if anchors.get(x['observationId']) and rows[x['observationId']]['finalTreatment']=='not_structurally_grouped_representation_limited'];out['a02SharedAnchors']={x:y for x,y in anchors.items() if len(y)>1}
 execution=json.loads((base/'s3-repaired-v4/repair-execution-manifest.json').read_text()); deps=execution['procedure'].get('repositoryLocalDependencies',[]);out['effectiveProcedureDependencyHashFailures']=[x['path'] for x in deps if sha(root/x['path'])!=x['sha256']];out['effectiveProcedureDependenciesPinned']=len(deps)
 return out
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path.cwd());p.add_argument('--output',type=Path);a=p.parse_args();root=a.repo.resolve();r={'schemaVersion':1,'artifactType':'batch-001-wave-1-s3-repair-v4-execution-audit','independence':'Does not import executors, execution audits, or helpers.','authorities':[audit(root,'kunaicho','authority-01-kunaicho'),audit(root,'shugiin','authority-02-shugiin')]};txt=json.dumps(r,ensure_ascii=False,sort_keys=True,indent=2)+'\n';a.output.write_text(txt,encoding='utf-8') if a.output else print(txt,end='')
if __name__=='__main__':main()
