#!/usr/bin/env python3
import argparse,hashlib,json,sys
from pathlib import Path
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path.cwd());a=p.parse_args();r=a.repo.resolve();f=json.loads((r/'evidence/document-understanding/batch-001/wave-1-s4-entry-freeze.json').read_text());bad=[]
 for x in f['pinned']:
  if not (r/x['path']).exists() or sha(r/x['path'])!=x['sha256']:bad.append(x['path'])
 for name,x in f['authorities'].items():
  d=r/x['s4Graph']['directory'];nodes=[json.loads(z) for z in (d/'nodes.jsonl').read_text().splitlines() if z];edges=[json.loads(z) for z in (d/'edges.jsonl').read_text().splitlines() if z]
  if len(nodes)!=x['s4Graph']['nodes'] or len(edges)!=x['s4Graph']['edges']:bad.append(name+' graph counts')
  for k,v in x['s4Graph'].items():
   if k not in {'directory','nodes','edges'} and sum(n.get('nodeType')==k for n in nodes)!=v:bad.append(name+' '+k)
 verdict=json.loads((r/'evidence/document-understanding/batch-001/wave-1-s3-repair-v4-review-s4-gate.json').read_text())
 if verdict.get('globalS4Authorization')!='AUTHORIZED':bad.append('review authorization')
 print(json.dumps({'pass':not bad,'failures':bad},sort_keys=True));sys.exit(1 if bad else 0)
if __name__=='__main__':main()
