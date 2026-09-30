#!/usr/bin/env python3
"""Static/synthetic design audit for the frozen Batch-001 S4 contract.

This procedure intentionally never opens authority source-observations or emits
normalization records.  It validates the boundary, contract, schema, and
synthetic vectors only.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "fixtures/document-understanding/batch-001"
CONTRACT = BASE / "s4-normalization-contract-v1.json"
VECTORS = BASE / "s4-normalization-test-vectors-v1.json"
SCHEMA = BASE / "s4-normalization-record-schema-v1.json"
FREEZE = ROOT / "evidence/document-understanding/batch-001/wave-1-s4-normalization-contract-freeze.json"
ENTRY_AUDIT = ROOT / "evidence/document-understanding/batch-001/audit-wave-1-s4-entry-freeze-v2.py"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stable_id(contract: dict, source_sha: str, file_id: str, page: int, observation_id: str) -> str:
    preimage = "\0".join([contract["contractVersion"], source_sha, file_id, str(page), observation_id])
    return f'{contract["namespace"]}-{hashlib.sha256(preimage.encode("utf-8")).hexdigest()}'


def normalize_text(contract: dict, text: str) -> tuple[str, list[str]]:
    values = text
    rules = []
    for rule, mapping_key in [("s4v1_fullwidth_digits", "fullwidthDigitMap"), ("s4v1_fullwidth_numeric_punctuation", "fullwidthNumericPunctuationMap"), ("s4v1_circled_number", "circledNumberMap")]:
        changed = "".join(contract["normalization"][mapping_key].get(ch, ch) for ch in values)
        if changed != values:
            rules.append(rule)
        values = changed
    return values, rules


def numeric_lexeme(text: str):
    sign = ""
    magnitude = text
    if magnitude and magnitude[0] in "+-−△▲":
        sign, magnitude = magnitude[0], magnitude[1:]
    valid = bool(re.fullmatch(r"[0-9]+", magnitude) or re.fullmatch(r"[0-9]{1,3}(,[0-9]{3})+", magnitude))
    if not valid:
        return None
    return ("-" if sign and sign in "-−△▲" else "") + magnitude.replace(",", ""), sign or None


def unit_lexeme(contract: dict, text: str):
    bare = contract["normalization"]["unit"]["bare"]
    if text in bare:
        return bare[text]
    match = re.fullmatch(contract["normalization"]["unit"]["declarationGrammar"], text)
    return bare[match.group(1)] if match else None


def main() -> int:
    failures = []
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    vectors = json.loads(VECTORS.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    freeze = json.loads(FREEZE.read_text(encoding="utf-8"))
    for pinned in freeze["pinned"]:
        path = ROOT / pinned["path"]
        if not path.exists() or path.stat().st_size != pinned["bytes"] or sha256(path) != pinned["sha256"]:
            failures.append(f'freeze_pin:{pinned["path"]}')
    entry = contract["entryBoundary"]
    if sha256(ROOT / entry["path"]) != entry["sha256"]:
        failures.append("entry_freeze_hash")
    entry_run = subprocess.run([sys.executable, str(ENTRY_AUDIT)], cwd=ROOT, text=True, capture_output=True)
    if entry_run.returncode or '"pass": true' not in entry_run.stdout:
        failures.append("entry_freeze_verifier")
    expected_order = ["s4v1_fullwidth_digits", "s4v1_fullwidth_numeric_punctuation", "s4v1_circled_number", "s4v1_numeric_lexeme", "s4v1_unit_lexeme"]
    if contract["normalization"]["characterPipeline"] != expected_order or len(set(expected_order)) != len(expected_order):
        failures.append("rule_order_or_uniqueness")
    circled = contract["normalization"]["circledNumberMap"]
    if len(circled) != 51 or circled.get("⓪") != "0" or circled.get("㊿") != "50":
        failures.append("circled_map")
    if "global_unicode_normalization" not in contract["prohibited"]:
        failures.append("global_unicode_prohibition")
    if schema.get("additionalProperties") is not False or any(key in schema["properties"] for key in ["ownerNodeId", "candidateId", "mof"]):
        failures.append("schema_scope")
    for vector in vectors["vectors"]:
        state = vector.get("sourceState", "observed_value")
        raw = vector.get("rawText")
        if state != "observed_value":
            if vector.get("expectedText") is not None:
                failures.append(f"state_vector:{state}")
            continue
        normalized, rules = normalize_text(contract, raw)
        if "expectedText" in vector and normalized != vector["expectedText"]:
            failures.append(f"text_vector:{raw}")
        numeric = numeric_lexeme(normalized)
        if "expectedNumeric" in vector and (numeric is None or numeric[0] != vector["expectedNumeric"]):
            failures.append(f"numeric_vector:{raw}")
        if "numeric" in vector and vector["numeric"] is None and numeric is not None:
            failures.append(f"numeric_negative:{raw}")
        if "expectedSign" in vector and (numeric is None or numeric[1] != vector["expectedSign"]):
            failures.append(f"sign_vector:{raw}")
        if "unitCode" in vector and (unit_lexeme(contract, normalized) or {}).get("unitCode") != vector["unitCode"]:
            failures.append(f"unit_vector:{raw}")
    sample = stable_id(contract, "a" * 64, "source-file", 7, "obs-9")
    if sample != stable_id(contract, "a" * 64, "source-file", 7, "obs-9") or not re.fullmatch(r"s4n1-[0-9a-f]{64}", sample):
        failures.append("stable_id")
    for authority in ["authority-01-kunaicho", "authority-02-shugiin"]:
        if (BASE / "authorities" / authority / "s4-normalized-v1").exists():
            failures.append(f"real_output_exists:{authority}")
    print(json.dumps({"contract": str(CONTRACT.relative_to(ROOT)), "failures": failures, "pass": not failures, "syntheticVectors": len(vectors["vectors"]), "stableIdSample": sample}, ensure_ascii=False, sort_keys=True))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
