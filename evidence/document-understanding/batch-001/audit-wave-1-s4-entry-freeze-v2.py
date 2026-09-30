#!/usr/bin/env python3
"""Build/verify the complete byte-pinned Wave 1 S4 entry freeze v2."""
from __future__ import annotations
import argparse, hashlib, json, sys
from collections import Counter
from pathlib import Path

V1='evidence/document-understanding/batch-001/wave-1-s4-entry-freeze.json'
V2='evidence/document-understanding/batch-001/wave-1-s4-entry-freeze-v2.json'
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def entry(root,path,role,stage,authority=None):
 p=root/path; x={'path':path,'sha256':sha(p),'byteSize':p.stat().st_size,'role':role,'stage':stage}
 if authority:x['authority']=authority
 return x
def inputs(root):
 common=[
 ('fixtures/document-understanding/canonical-semantic-extraction/20260929_1801_Canonical_Semantic_Extraction_Protocol.md','governingContract','protocol'),
 ('fixtures/document-understanding/batch-001/wave-1-s3-structural-repair-spec.json','governingContract','repairSpec'),
 ('fixtures/document-understanding/batch-001/s3_repaired_v4_execution.py','effectiveProcedureProvenance','v4'),
 ('fixtures/document-understanding/batch-001/s3_repaired_v3_execution.py','effectiveProcedureProvenance','v3-transitive'),
 ('fixtures/document-understanding/batch-001/s3_repaired_v2_execution.py','effectiveProcedureProvenance','v2-transitive'),
 ('evidence/document-understanding/batch-001/review-wave-1-s3-repair-v4-s4-gate.py','acceptanceEvidence','procedure'),
 ('evidence/document-understanding/batch-001/wave-1-s3-repair-v4-review-s4-gate.json','acceptanceEvidence','verdict'),
 ('reports/document-understanding/20260930_2040_Batch001_Wave1_S3_Repair_v4_Review_and_S4_Gate.md','acceptanceEvidence','report')]
 out=[entry(root,*x) for x in common]
 for aid,d,source in [('kunaicho','authority-01-kunaicho','ffab15073beb2411d9396f7ca0cbb1ce33ccdf99be05e6d0d88e29366912e261'),('shugiin','authority-02-shugiin','30d0dfc363a1f4f7e37b64a0059b48c2f03f13f997eb251e7ef5acaabd37c435')]:
  b=f'fixtures/document-understanding/batch-001/authorities/{d}/'
  for rel,role,stage in [('authority-preflight-profile.json','authorityProfile','S1'),('source-manifest.json','sourceIdentity','S0'),('source-observations.jsonl','s2Evidence','S2'),('observation-manifest.json','s2Evidence','S2'),('raw/poppler-bbox-layout.xml','s2Evidence','S2raw')]:out.append(entry(root,b+rel,role,stage,aid))
  for rel in ['nodes.jsonl','edges.jsonl','structural-interpretation-manifest.json','repair-execution-manifest.json']:out.append(entry(root,b+'s3-repaired-v4/'+rel,'acceptedS3','S3',aid))
 return out
def build(root):
 return {'schemaVersion':2,'artifactType':'batch-001-wave-1-s4-entry-freeze','freezeVersion':'v2','status':'FROZEN_S4_ENTRY_NOT_EXECUTED','supersedes':{'path':V1,'sha256':sha(root/V1)},'repairReason':['s2_bytes_not_pinned','v4_s3_bytes_not_pinned','profile_and_source_identity_not_verified','excluded_boundary_not_enforced'],'entrySourceCommit':'2e5a619d601050ff815cdfc67fef9167f490334d','integrationCommit':'14736a442ce1160b3baa13b35a9c568b60484a74','s4':{'authorization':'AUTHORIZED','entryBoundary':'FROZEN','execution':'NOT_STARTED'},'s4Inputs':inputs(root),'excludedInputs':['baseline S3','s3-repaired-v1','s3-repaired-v2','s3-repaired-v3','GT','benchmark','OCR','CSV','MOF','Wave 2','production artifacts'],'authorities':{'kunaicho':{'sourceSha256':'ffab15073beb2411d9396f7ca0cbb1ce33ccdf99be05e6d0d88e29366912e261','s2RecordCount':19442,'pages':33,'graphCounts':{'nodes':67,'edges':34,'outerLedger':20,'unclassifiedStructure':13,'nestedStructure':1,'page':33}},'shugiin':{'sourceSha256':'30d0dfc363a1f4f7e37b64a0059b48c2f03f13f997eb251e7ef5acaabd37c435','s2RecordCount':17072,'pages':36,'graphCounts':{'nodes':95,'edges':59,'outerLedger':15,'unclassifiedStructure':21,'boundedLocalTable':23,'page':36}}}}
def verify(root):
 f=json.loads((root/V2).read_text());bad=[]; paths=[x['path'] for x in f['s4Inputs']]
 for x in f['s4Inputs']:
  p=root/x['path'];
  if not p.exists() or sha(p)!=x['sha256'] or p.stat().st_size!=x['byteSize']:bad.append(x['path']);continue
  if p.suffix=='.json':json.loads(p.read_text())
  if p.suffix=='.jsonl':[json.loads(z) for z in p.read_text().splitlines() if z]
 for aid,d in [('kunaicho','authority-01-kunaicho'),('shugiin','authority-02-shugiin')]:
  b=root/f'fixtures/document-understanding/batch-001/authorities/{d}';a=f['authorities'][aid]; sm=json.loads((b/'source-manifest.json').read_text());om=json.loads((b/'observation-manifest.json').read_text());pr=json.loads((b/'authority-preflight-profile.json').read_text());obs=[json.loads(z) for z in (b/'source-observations.jsonl').read_text().splitlines() if z]
  vals=json.dumps([sm,om,pr]);
  if a['sourceSha256'] not in vals or len(obs)!=a['s2RecordCount'] or len({x['pdfPageIndex'] for x in obs if x['observationKind']=='page'})!=a['pages']:bad.append(aid+' source')
  ns=[json.loads(z) for z in (b/'s3-repaired-v4/nodes.jsonl').read_text().splitlines() if z];es=[json.loads(z) for z in (b/'s3-repaired-v4/edges.jsonl').read_text().splitlines() if z]
  c=a['graphCounts'];
  if len(ns)!=c['nodes'] or len(es)!=c['edges'] or any(sum(x.get('nodeType')==k for x in ns)!=v for k,v in c.items() if k not in {'nodes','edges'}):bad.append(aid+' graph')
 verdict=json.loads((root/'evidence/document-understanding/batch-001/wave-1-s3-repair-v4-review-s4-gate.json').read_text())
 if verdict.get('globalS4Authorization')!='AUTHORIZED' or any(x not in {'ACCEPT_REPAIRED_S3_FOR_S4'} for x in verdict.get('authorityVerdicts',{}).values()):bad.append('verdict')
 if any(any(term.lower() in p.lower() for term in ['s3-repaired-v1','s3-repaired-v2','s3-repaired-v3','ground-truth','benchmark','ocr','csv','mof','wave-2','production']) for p in paths):bad.append('excluded inputs')
 print(json.dumps({'pass':not bad,'failures':bad},sort_keys=True));return not bad
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path.cwd());p.add_argument('--write-freeze',action='store_true');a=p.parse_args();r=a.repo.resolve()
 if a.write_freeze:(r/V2).write_text(json.dumps(build(r),ensure_ascii=False,sort_keys=True,indent=2)+'\n')
 sys.exit(0 if verify(r) else 1)
if __name__=='__main__':main()
