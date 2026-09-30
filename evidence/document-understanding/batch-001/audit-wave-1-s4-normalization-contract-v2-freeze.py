#!/usr/bin/env python3
"""Static, synthetic, and metadata-only design audit for S4 v2; no S4 execution."""
from __future__ import annotations
import hashlib, json, re, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]; BASE=ROOT/'fixtures/document-understanding/batch-001'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def sid(c,x): return 's4n2-'+hashlib.sha256('\0'.join([c['contractVersion'],x['sourceSha256'],x['fileId'],str(x['pdfPageIndex']),x['sourceObservationId']]).encode()).hexdigest()
def closed(x):
    if isinstance(x,dict):
        if x.get('type')=='object' and x.get('additionalProperties') is not False:return False
        return all(closed(v) for v in x.values())
    if isinstance(x,list): return all(closed(v) for v in x)
    return True
def main():
 c=json.loads((BASE/'s4-normalization-contract-v2.json').read_text()); s=json.loads((BASE/'s4-normalization-record-schema-v2.json').read_text()); v=json.loads((BASE/'s4-normalization-test-vectors-v2.json').read_text()); inv=json.loads((ROOT/'evidence/document-understanding/batch-001/wave-1-s4-normalization-v2-s2-shape-inventory.json').read_text())
 fail=[]
 if c['contractVersion']!='batch-001-wave-1-s4-normalization-v2' or c['namespace']!='s4n2':fail.append('identity')
 if not closed(s):fail.append('recursive_schema_closure')
 required={'raw','sourceOrder','provenance','numericLexeme','unitLexeme','sourceRecordOrdinal','textChanged'}
 if not required <= set(s['properties']):fail.append('required_shapes')
 if s['properties']['appliedRuleIds']['items'].get('enum') != c['ruleEmission']['allowed']:fail.append('rule_enum')
 if s['properties']['sourceState'].get('const')!='observed_value':fail.append('state_matrix')
 if 'nativeSourceOrderTuple' in json.dumps(c):fail.append('legacy_order')
 if c['serialization']['prettyJson'].get('finalNewline')!='exactly_one':fail.append('pretty_newline')
 if any(sid(c,x)!=x['expected'] for x in v['stableIdVectors']):fail.append('stable_ids')
 b=b''.join(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()+b'\n' for x in [{'sourceRecordOrdinal':0,'v':'b'},{'sourceRecordOrdinal':1,'v':'a'}])
 expected=next(x['expectedBytesSha256'] for x in v['negativeAssertions'] if x['name']=='source_record_ordinal_orders_jsonl')
 if sha256:=hashlib.sha256(b).hexdigest()!=expected: fail.append('serialization_bytes')
 if c['normalization']['numeric']['grammar']!='^(?:[+\\-−△▲])?(?:[0-9]+|[0-9]{1,3}(?:,[0-9]{3})+)$':fail.append('numeric_grammar')
 if c['unsupportedWordCharacters']!=['U+0009','U+000A','U+000D']:fail.append('whitespace')
 for auth,data in inv['authorities'].items():
  p=ROOT/'fixtures/document-understanding/batch-001/authorities'/auth/'source-observations.jsonl'; lines=p.read_bytes().splitlines()
  if not lines or any(not line for line in lines) or len(lines)!=data['recordCount'] or sha(p)!=data['sourceObservationsSha256']:fail.append('inventory:'+auth)
  # Metadata-only parse: IDs/kinds/states/order/raw keys; never inspect raw values.
  seen=set()
  for n,line in enumerate(lines):
   x=json.loads(line); seen.add(x['observationId'])
   if x['observationKind'] not in data['observationKinds'] or x['state'] not in data['sourceStates']:fail.append('shape:'+auth);break
  if len(seen)!=len(lines):fail.append('unique_ids:'+auth)
 entry=subprocess.run([sys.executable,str(ROOT/'evidence/document-understanding/batch-001/audit-wave-1-s4-entry-freeze-v2.py')],cwd=ROOT,text=True,capture_output=True)
 if entry.returncode:fail.append('entry_verifier')
 for name in ['authority-01-kunaicho','authority-02-shugiin']:
  if (BASE/'authorities'/name/'s4-normalized-v2').exists() or (BASE/'authorities'/name/'s4-normalized-v1').exists():fail.append('real_output')
 print(json.dumps({'pass':not fail,'failures':sorted(set(fail)),'metadataOnlyInventory':True,'stableIdVectors':3,'negativeAssertions':len(v['negativeAssertions'])},sort_keys=True));return 1 if fail else 0
if __name__=='__main__':raise SystemExit(main())
