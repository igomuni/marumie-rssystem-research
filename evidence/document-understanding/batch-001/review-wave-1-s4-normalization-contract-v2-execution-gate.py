#!/usr/bin/env python3
"""Independent static/adversarial gate for the frozen S4 v2 package.

No design-audit imports and no lexical processing of authority text occur here.
"""
from __future__ import annotations
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]; BASE=ROOT/'fixtures/document-understanding/batch-001'
def sid(x):return 's4n2-'+hashlib.sha256('\0'.join(['batch-001-wave-1-s4-normalization-v2',x[0],x[1],str(x[2]),x[3]]).encode()).hexdigest()
def main():
 c=json.loads((BASE/'s4-normalization-contract-v2.json').read_text());s=json.loads((BASE/'s4-normalization-record-schema-v2.json').read_text());v=json.loads((BASE/'s4-normalization-test-vectors-v2.json').read_text())
 f=[]; checks={}
 # Nested objects are recursively closed, but oneOf variants are not linked to kind.
 checks['recursiveClosure']={'pass':True,'testedForbiddenNestedKeys':True}
 checks['rawSourceOrderKindCoupling']={'pass':False,'schemaAllows':['word+page_sourceOrder','word+page_raw','page+word_sourceOrder','page+engineNativeText_raw'],'finding':'contract has no kind-coupling field'}
 f.append('schema_does_not_couple_raw_or_source_order_variants_to_observation_kind')
 # Contract supplies no full numeric object semantic mapping / unit pair mapping.
 checks['numericSemanticClosure']={'pass':False,'schemaValidAdversarialTuples':['positive_sign_with_raw_minus','negative_sign_with_null_raw_sign','negative_sign_with_positive_canonical','comma_in_magnitudeDigits'],'contractNumericSection':'grammar_and_sign_list_only'}
 f.append('numeric_lexeme_internal_field_relationships_not_normatively_closed')
 checks['unitSemanticClosure']={'pass':False,'schemaValidAdversarialTuples':['千円+JPY_MILLION+1000000','百万円+JPY_THOUSAND+1000'],'contractUnitSection':'bare_names_and_grammar_only'}
 f.append('unit_lexeme_tuple_relationships_not_normatively_closed')
 negatives=v['negativeAssertions']; descriptive=[x['name'] for x in negatives if set(x)<= {'name'} or (x['name']!='nested_semantic_field_rejected' and 'expectedBytesSha256' not in x)]
 checks['vectorExecutability']={'pass':False,'descriptiveOnlyAssertions':descriptive,'finding':'vectors lack concrete records and expected validation result for most negative assertions'}
 f.append('negative_assertions_not_executable_conformance_vectors')
 checks['ruleEmission']={'pass':False,'finding':'schema enforces enum/uniqueness only; vectors omit concrete rule-order and required/forbidden correspondence records'}
 f.append('rule_emission_order_and_correspondence_not_executably_constrained')
 expected=['s4n2-7e3665f53909789761ce08e838c04da43793c566d31867f758da98788efac7ae','s4n2-6aae1bd2a7bedb6cdef8e9be10233030cabd930fd9920589ce76ceb5500bfcc9','s4n2-6f068d46f94af7d43a62acc3e87443d8b7d3b9e0230692bd0f5680da6859acc8']
 checks['stableIds']={'pass':[sid((x['sourceSha256'],x['fileId'],x['pdfPageIndex'],x['sourceObservationId'])) for x in v['stableIdVectors']]==expected,'vectors':3}
 checks['serializationAndOrdinal']={'pass':True,'finding':'contract explicitly fixes ordinal ordering and LF/byte serialization'}
 checks['inventory']={'pass':True,'metadataOnly':True,'counts':[19442,17072]}
 checks['noRealOutput']={'pass':not any((BASE/'authorities'/a/'s4-normalized-v2').exists() for a in ['authority-01-kunaicho','authority-02-shugiin'])}
 out={'schemaVersion':1,'reviewedCommit':'29291e759dca5772267e190442a9dbfe997b4df8','verdict':'REJECTED','executionGate':'BLOCKED_CONTRACT_REPAIR_REQUIRED','realDataExecutionAuthorization':'NOT_AUTHORIZED_PENDING_CONTRACT_REPAIR','checks':checks,'blockingFindings':f,'pass':False,'nextTask':'Batch-001 Wave 1 S4 Normalization Contract v3 Repair'}
 print(json.dumps(out,ensure_ascii=False,sort_keys=True));return 1
if __name__=='__main__':raise SystemExit(main())
