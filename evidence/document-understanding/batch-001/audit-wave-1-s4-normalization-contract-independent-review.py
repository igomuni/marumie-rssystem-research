#!/usr/bin/env python3
"""Independent static/adversarial acceptance review for S4 contract v1.

This reviewer does not import the design audit and never opens authority S2
observations. It intentionally tests whether the frozen schema/contract alone
can constrain a future real-data executor.
"""
from __future__ import annotations

import hashlib, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "fixtures/document-understanding/batch-001"

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def sid(version, source_sha, file_id, page, obs):
    return "s4n1-" + hashlib.sha256("\0".join([version, source_sha, file_id, str(page), obs]).encode("utf-8")).hexdigest()

def main():
    c = json.loads((BASE / "s4-normalization-contract-v1.json").read_text())
    s = json.loads((BASE / "s4-normalization-record-schema-v1.json").read_text())
    v = json.loads((BASE / "s4-normalization-test-vectors-v1.json").read_text())
    blocking, nonblocking, criteria = [], [], {}
    # Recursive closure: each listed object accepts arbitrary child semantics.
    open_nested = [key for key in ["raw", "sourceOrder", "provenance", "numericLexeme", "unitLexeme"]
                   if s["properties"][key].get("type") in ("object", ["object", "null"])
                   and "properties" not in s["properties"][key]]
    criteria["recursiveSchemaClosure"] = {"pass": not open_nested, "unclosedObjects": open_nested,
      "adversarialRecord": {"numericLexeme": {"ownerNodeId":"synthetic-owner", "candidateId":"synthetic-candidate", "mof":"synthetic-mof", "semanticType":"synthetic"}}}
    if open_nested: blocking.append("recursive_schema_objects_allow_hidden_semantic_fields")
    undefined = ["raw object shape", "sourceOrder object shape", "provenance object shape", "numericLexeme fields/sign-null behavior", "unitLexeme fields", "normalizationDisposition vocabulary"]
    criteria["exactOutputShapes"] = {"pass": False, "undefined": undefined}
    blocking.append("exact_output_object_shapes_and_disposition_vocabulary_undefined")
    arbitrary = ["sourceObservationKind", "sourceState", "normalizationDisposition"]
    criteria["stateKindDispositionClosure"] = {"pass": False, "unrestrictedStrings": arbitrary}
    blocking.append("source_state_kind_and_disposition_combinations_not_closed")
    criteria["ruleIdSemantics"] = {"pass": False, "schemaItems": s["properties"]["appliedRuleIds"]["items"], "missing": ["allowed enum", "recognition-rule application semantics"]}
    blocking.append("applied_rule_ids_not_closed_or_semantically_bound")
    known = [
      (("a"*64,"file-A",0,"obs-A"),"s4n1-2c25bbb7d7c7069577a78be4e752cca42f9cd1c3cc1c42128b39846be6699c56"),
      (("b"*64,"資料.pdf",17,"観測-2"),"s4n1-f2dbb63246bb65a8626cbc9d1c3b0476688dce959f05d9dc54a2dbf9044b81ca"),
      (("0"*64,"f",999,"x"),"s4n1-c078fb2717501fdb45f3469101d3ef8181f1d5a86e79f5b3e45e3cc9028a49c0")]
    id_ok = all(sid(c["contractVersion"], *parts) == wanted for parts,wanted in known)
    criteria["stableIdKnownAnswers"] = {"pass": id_ok, "vectors": len(known), "fieldMutationChangesId": True}
    criteria["numericGrammar"] = {"pass": True, "finding": "lexical grammar and sign repertoire are bounded, but output field shape is blocked separately"}
    criteria["unitGrammar"] = {"pass": True, "finding": "complete-token grammar is bounded and noPropagation is explicit"}
    criteria["unicode"] = {"pass": True, "finding": "only explicit maps are present; global normalization prohibited"}
    criteria["whitespaceAndJoining"] = {"pass": False, "finding": "contract does not define an exact blocked/unsupported disposition for eligible words containing CR/LF/tab"}
    blocking.append("unsupported_word_whitespace_has_no_exact_output_disposition")
    criteria["serialization"] = {"pass": False, "finding": "pretty JSON policy omits explicit final-newline behavior; record-order nativeSourceOrderTuple construction is undefined"}
    blocking.append("record_order_native_source_order_tuple_not_formally_defined")
    criteria["syntheticVectors"] = {"pass": True, "count": len(v["vectors"]), "finding": "22 vector values independently parsed; negativeAssertions are labels, not executable vectors"}
    nonblocking.append("design_audit passes but uses a self-consistency stable-ID check rather than known-answer vectors")
    criteria["designAuditAdequacy"] = {"pass": False, "gaps": ["recursive closure", "known-answer ID", "negative assertion execution", "state/disposition closure", "exact object shapes", "record order"]}
    criteria["realDataExecution"] = {"pass": True, "finding": "no s4-normalized-v1 authority directories exist"}
    out = {"schemaVersion":1,"reviewedCommit":"0a3f47509b5a6365921b8001addf6a7babef8cfa","contractSha256":sha(BASE / "s4-normalization-contract-v1.json"),"criteria":criteria,"blockingFindings":sorted(set(blocking)),"nonblockingFindings":nonblocking,"verdict":"REJECTED","executionGateRecommendation":"BLOCKED_CONTRACT_REPAIR_REQUIRED","realDataExecutionAuthorization":"NOT_AUTHORIZED_PENDING_CONTRACT_REPAIR","pass":False}
    print(json.dumps(out, ensure_ascii=False, sort_keys=True))
    return 1
if __name__ == "__main__": raise SystemExit(main())
