#!/usr/bin/env python3
"""Research-only Wave 1 S3 repair v3 executor.

Consumes immutable S2 only.  V3 preserves v2's namespace and mechanical
repairs, adds direct outer row-word evidence, and rebuilds A02 unit treatment
from the final graph rather than bbox containment.
"""
from __future__ import annotations
import argparse, hashlib, json
from collections import Counter, defaultdict
from pathlib import Path
import s3_repaired_v2_execution as v2

SPEC=v2.SPEC; NS=v2.NS; OUTER=v2.OUTER; LOCAL=v2.LOCAL; EDGE=v2.EDGE_PRIMITIVE
def dump(x): return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write_json(p,x): Path(p).write_text(json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
def write_jsonl(p,xs): Path(p).write_text(''.join(dump(x)+'\n' for x in xs),encoding='utf-8')
def box(x):
 b=x.get('geometry',{}).get('bbox')
 if isinstance(b,list): return [float(v) for v in b]
 return v2.box(x)
def union(xs): return v2.union(xs)
def locator(xs): return v2.locator(xs)
def ident(kind,page,rule,supports): return v2.id_for(kind,page['sourceSha256'],page['fileId'],page['pdfPageIndex'],rule,{x['observationId']:x for x in supports})
def bands(lines): return v2.y_bands(lines)
def height(lines): return v2.page_height(lines)
def words_window(words,b): return v2.words_in_window(words,b)
def contains(a,b): return v2.contains(a,b)

def page_node(authority,page):
 return {'nodeId':ident('page',page,'source-observed-page',[page]),'stage':'S3_REPAIRED_V3','namespace':NS,'authorityId':authority,'nodeType':'page','evidenceClass':'source_observed','sourceSha256':page['sourceSha256'],'fileId':page['fileId'],'pdfPageIndex':page['pdfPageIndex'],'supportingObservationIds':[page['observationId']],'evidenceLocator':locator([page]),'state':'observed_value','geometry':{'bbox':None}}
def inferred_node(authority,kind,rule,profile,page,supports,status,ambiguity,ri):
 direct={x['observationId']:x for x in supports}; vals=list(direct.values())
 return {'nodeId':ident(kind,page,rule,vals),'stage':'S3_REPAIRED_V3','namespace':NS,'authorityId':authority,'nodeType':kind,'evidenceClass':'structurally_inferred','inferenceRule':rule,'profileVersion':profile,'ambiguityState':ambiguity,'structuralStatus':status,'sourceSha256':page['sourceSha256'],'fileId':page['fileId'],'pdfPageIndex':page['pdfPageIndex'],'supportingObservationIds':sorted(direct),'evidenceLocator':locator(vals),'ruleInput':ri,'state':'not_applicable','geometry':{'bbox':union(vals)}}
def inferred_edge(parent,child,rule,profile,supports,status,ambiguity,ri):
 direct={x['observationId']:x for x in supports}; vals=list(direct.values())
 return {'edgeId':ident(EDGE,child,rule,vals),'idPrimitive':EDGE,'stage':'S3_REPAIRED_V3','namespace':NS,'relationshipType':'contains','fromNodeId':parent['nodeId'],'toNodeId':child['nodeId'],'evidenceClass':'structurally_inferred','inferenceRule':rule,'profileVersion':profile,'ambiguityState':ambiguity,'structuralStatus':status,'sourceSha256':child['sourceSha256'],'fileId':child['fileId'],'pdfPageIndex':child['pdfPageIndex'],'supportingObservationIds':sorted(direct),'evidenceLocator':locator(vals),'ruleInput':ri,'state':'not_applicable'}

def literal_band_ok(groups, window, max_height):
 """Non-chained local band: all header glyphs fit one window bounded by H."""
 gb=union([x for g in groups for x in g]); wb=union(window)
 return bool(gb and wb and gb[3]-gb[1] <= 2*max_height and gb[1] >= wb[1]-max_height and gb[3] <= wb[3]+max_height)

def outer_candidate(page, lines, words):
 h=height(lines); bs=bands(lines)
 for seed in bs:
  sb=union(seed)
  window=[line for band in bs for line in band if union(band)[1]<=sb[3]+h and union(band)[3]>=sb[1]-h]
  header=v2.outer_header(window,words)
  if not header: continue
  groups,gboxes=header
  if not literal_band_ok(groups,window,h): continue
  hbox=union([x for g in groups for x in g]); rows=[]
  for band in bs:
   bb=union(band)
   if bb[1]<=hbox[3]+h: continue
   row_words=words_window(words,bb); matches=[]
   for i,hb in enumerate(gboxes):
    direct=[w for w in row_words if box(w)[0]<=hb[2]+h and box(w)[2]>=hb[0]-h]
    if direct: matches.append({'headerGroupIndex':i,'headerXRange':hb,'rowWordObservationIds':[w['observationId'] for w in direct],'rowWordBBoxes':[box(w) for w in direct]})
   if len(matches)>=2: rows.append((band,row_words,matches))
  if len(rows)>=2:
   return {'groups':groups,'gboxes':gboxes,'window':window,'rows':rows[:2],'height':h}
 return None

def local_node(authority,page,profile,candidate):
 if candidate['status']!='structurally_supported':
  supports=[page,candidate['block'],*candidate.get('header',[])]; kind='ambiguousStructuralGroup';status='structurally_ambiguous';ambiguity=candidate['reason']
  ri={'candidateBlockObservationId':candidate['block']['observationId'],'samePageOnly':True,'ruleFailureReason':candidate['reason'],'sourceOrderContiguityEvidence':{'candidateBlockSourceOrder':candidate['block']['sourceOrder']}}
 else:
  supports=[page,candidate['block'],*candidate['header'],*candidate['headerWords'],*(x for band,row_words,_,_ in candidate['rows'] for x in [*band,*row_words]),*candidate['units']]
  kind='boundedLocalTable' if authority=='shugiin' else 'nestedStructure';status='structurally_supported';ambiguity='not_ambiguous'
  ri={'candidateBlockObservationId':candidate['block']['observationId'],'headerAnchorObservationIds':[x['observationId'] for x in candidate['header']],'headerAnchorUnionBBox':union(candidate['header']),'headerXClusters':candidate['headerClusters'],'repeatingRowBands':[[x['observationId'] for x in b] for b,_,_,_ in candidate['rows']],'rowXClusters':[c for _,_,c,_ in candidate['rows']],'headerToRowClusterMatches':[m for *_,m in candidate['rows']],'xClusterTolerance':candidate['height'],'xClusterToleranceBasis':'page maximum observed textLine height','localUnitAnchorObservationIds':[x['observationId'] for x in candidate['units']],'samePageOnly':True,'sourceOrderContiguityEvidence':{'candidateBlockSourceOrder':candidate['block']['sourceOrder'],'headerSourceOrders':[x['sourceOrder'] for x in candidate['header']],'rowBandSourceOrders':[[x['sourceOrder'] for x in b] for b,_,_,_ in candidate['rows']],'rowWordSourceOrders':[[x['sourceOrder'] for x in rw] for _,rw,_,_ in candidate['rows']]},'boxGlyphFilter':'source-emitted raw text only; not PDF drawing or cell evidence'}
 return kind,status,ambiguity,supports,ri

def execute(root,out_root,authority,directory,profile):
 base=root/'fixtures/document-understanding/batch-001/authorities'/directory; records=[json.loads(x) for x in (base/'source-observations.jsonl').read_text(encoding='utf-8').splitlines() if x]; byid={x['observationId']:x for x in records}; pages=defaultdict(list)
 for x in records: pages[x['pdfPageIndex']].append(x)
 out=out_root/'fixtures/document-understanding/batch-001/authorities'/directory/'s3-repaired-v3';out.mkdir(parents=True,exist_ok=True)
 nodes=[];edges=[];summaries=[];local_audit=[]
 for ix,items in sorted(pages.items()):
  page=next(x for x in items if x['observationKind']=='page');lines=[x for x in items if x['observationKind']=='textLine'];words=[x for x in items if x['observationKind']=='word'];blocks=[x for x in items if x['observationKind']=='textBlock'];p=page_node(authority,page);nodes.append(p)
  cand=outer_candidate(page,lines,words)
  if cand:
   supports=[page,*[x for g in cand['groups'] for x in g],*[x for b,rw,_ in cand['rows'] for x in [*b,*rw]]]
   ri={'literalHeaderBand':{'memberLineObservationIds':[x['observationId'] for x in cand['window']],'memberLineBBoxes':[box(x) for x in cand['window']],'unionBBox':union(cand['window']),'pageMaximumObservedLineHeight':cand['height'],'membershipRule':'non-chained source-observed line window; each header glyph bbox lies within the window plus page maximum observed line height'},'headerGroups':[{'index':i,'memberObservationIds':[x['observationId'] for x in g],'unionBBox':cand['gboxes'][i]} for i,g in enumerate(cand['groups'])],'leftToRightHeaderGroupIndexes':[0,1,2,3,4],'rowPatternEvidence':[{'rowBandLineObservationIds':[x['observationId'] for x in b],'rowBandUnionBBox':union(b),'matchedHeaderRanges':m} for b,rw,m in cand['rows']],'samePageOnly':True,'noPageWideTokenRule':True}
   outer=inferred_node(authority,'outerLedger',OUTER,profile,page,supports,'structurally_supported','not_ambiguous',ri)
  else:
   support=[page,*(bands(lines)[0] if bands(lines) else [])]
   outer=inferred_node(authority,'unclassifiedStructure',OUTER,profile,page,support,'unclassified','literal-local-header-band-or-direct-row-word-pattern-not-supported',{'pageMaximumObservedLineHeight':height(lines),'samePageOnly':True,'noPageWideTokenRule':True})
  nodes.append(outer);edges.append(inferred_edge(p,outer,OUTER,profile,[page,*[byid[x] for x in outer['supportingObservationIds'] if x!=page['observationId']]],outer['structuralStatus'],outer['ambiguityState'],{'parentAnchorObservationIds':[page['observationId']],'childDirectObservationIds':outer['supportingObservationIds'],'samePageOnly':True}))
  lc=0
  for block in blocks:
   candidate=v2.local_candidate(block,lines,words,authority=='shugiin')
   if not candidate:continue
   kind,status,ambiguity,support,ri=local_node(authority,page,profile,candidate);n=inferred_node(authority,kind,LOCAL,profile,page,support,status,ambiguity,ri);nodes.append(n);lc+=1
   edges.append(inferred_edge(p,n,LOCAL,profile,support,status,ambiguity,{'parentAnchorObservationIds':[page['observationId']],'childDirectObservationIds':n['supportingObservationIds'],'samePageOnly':True}))
   local_audit.append({'pdfPageIndex':ix,'nodeId':n['nodeId'],'type':kind,'structuralStatus':status,'candidateBlockObservationId':ri['candidateBlockObservationId'],'reason':candidate.get('reason','rule-satisfied')})
  summaries.append({'pdfPageIndex':ix,'outerPartitionNodeId':outer['nodeId'],'outerPartitionStatus':outer['structuralStatus'],'localOrNestedGroupCount':lc})
 treatments=[]
 if authority=='shugiin':
  supported=[n for n in nodes if n.get('nodeType')=='boundedLocalTable' and n.get('structuralStatus')=='structurally_supported']; anchors=defaultdict(list)
  for n in supported:
   for oid in n['ruleInput']['localUnitAnchorObservationIds']:anchors[oid].append(n)
  for x in records:
   if x['observationKind']!='textLine' or '百万円' not in x.get('raw',{}).get('engineNativeText',''):continue
   direct=anchors.get(x['observationId'],[]);bbox_only=[n['nodeId'] for n in supported if n['pdfPageIndex']==x['pdfPageIndex'] and contains(box(n),box(x))]
   if len(direct)==1: treatment='member_of_supported_boundedLocalTable';reason='direct-local-unit-anchor';group=direct[0]['nodeId']
   elif len(direct)>1: treatment='member_of_ambiguous_structural_group';reason='shared-direct-local-unit-anchor';group=None
   else: treatment='not_structurally_grouped_representation_limited';reason='no-direct-local-unit-anchor';group=None
   treatments.append({'observationId':x['observationId'],'pdfPageIndex':x['pdfPageIndex'],'sourceOrder':x['sourceOrder'],'bbox':x['geometry']['bbox'],'directUnitAnchorGroupIds':[n['nodeId'] for n in direct],'bboxContainmentOnlyGroupIds':bbox_only,'finalTreatment':treatment,'reason':reason,**({'groupNodeId':group} if group else {})})
  treatments.sort(key=lambda x:(x['pdfPageIndex'],x['observationId']))
 nodes.sort(key=lambda x:x['nodeId']);edges.sort(key=lambda x:x['edgeId']);write_jsonl(out/'nodes.jsonl',nodes);write_jsonl(out/'edges.jsonl',edges)
 m={'schemaVersion':1,'artifactType':'batch-001-wave-1-s3-repaired-v3-manifest','stage':'S3_REPAIRED_V3','stageStatus':'COMPLETE_NOT_CANONICAL_FROZEN','executionRevision':'v3','specVersion':SPEC,'namespace':NS,'authorityId':authority,'profileVersion':profile,'sourceSha256':page['sourceSha256'],'inputSourceObservations':{'path':f'fixtures/document-understanding/batch-001/authorities/{directory}/source-observations.jsonl','sha256':sha(base/'source-observations.jsonl')},'nodeCount':len(nodes),'edgeCount':len(edges),'countsByStructuralStatus':dict(sorted(Counter(x.get('structuralStatus','source_observed') for x in nodes).items())),'nodeCountsByType':dict(sorted(Counter(x['nodeType'] for x in nodes).items())),'pageSummaries':summaries,'crossPageInferredStructuralEdgeCount':0,'crossFileInferredStructuralEdgeCount':0,'documentMembershipEdgeCount':0,'outerLocalUnitInheritanceEdgeCount':0,'normalizationStatus':'not_created','semanticCandidateStatus':'not_created','financialAssociationStatus':'not_created','canonicalFreezeStatus':'not_created','localAudit':local_audit}
 if authority=='shugiin':m['a02HyakumanYenReconciliation']=treatments
 write_json(out/'structural-interpretation-manifest.json',m)
 e={'schemaVersion':1,'artifactType':'batch-001-wave-1-s3-repair-v3-execution-manifest','executionRevision':'v3','specVersion':SPEC,'namespace':NS,'authorityId':authority,'profileVersion':profile,'sourceSha256':page['sourceSha256'],'procedure':{'path':'fixtures/document-understanding/batch-001/s3_repaired_v3_execution.py','sha256':sha(Path(__file__))},'idPolicy':{'nodeAndEdgeInputs':['specVersion','sourceSha256','fileId','pdfPageIndex','structural primitive type','inferenceRule','sorted supportingObservationIds'],'edgePrimitive':EDGE,'parentOrChildIdsExcluded':True},'serialization':{'encoding':'UTF-8','newlines':'LF','jsonKeyOrder':'sorted','recordOrder':'stable ID ascending','absolutePathsExcluded':True},'historicalV1AndV2Preserved':True,'documentContainmentOmittedFromPageScopedGraph':True}
 write_json(out/'repair-execution-manifest.json',e);return {'authority':authority,'out':out,'nodes':nodes,'edges':edges,'manifest':m}

def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path.cwd());p.add_argument('--out-root',type=Path);a=p.parse_args();root=a.repo.resolve();out=a.out_root.resolve() if a.out_root else root;spec=json.loads((root/'fixtures/document-understanding/batch-001/wave-1-s3-structural-repair-spec.json').read_text())
 if spec['specVersion']!=SPEC:raise SystemExit('frozen spec mismatch')
 for auth,d in [('kunaicho','authority-01-kunaicho'),('shugiin','authority-02-shugiin')]:
  base=root/'fixtures/document-understanding/batch-001/authorities'/d
  for rel,want in spec['immutableBaseline']['authorityArtifactHashes'][auth].items():
   if sha(base/rel)!=want:raise SystemExit(f'immutable baseline mismatch: {auth} {rel}')
 result=[execute(root,out,'kunaicho','authority-01-kunaicho','batch-001-wave-1-a01-v1'),execute(root,out,'shugiin','authority-02-shugiin','batch-001-wave-1-a02-v1')]
 print(dump({'status':'ok','authorities':[{'authority':x['authority'],'nodes':len(x['nodes']),'edges':len(x['edges'])} for x in result]}))
if __name__=='__main__':main()
