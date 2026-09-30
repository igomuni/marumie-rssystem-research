# Batch-001 Wave 1 S4 Normalization Contract Independent Review

Reviewed contract commit: `0a3f47509b5a6365921b8001addf6a7babef8cfa`
Canonical observed: `38f29ba8af4d2cd8a9795895726d5f7a06373490` (unchanged)

## Verdict

`REJECTED` — `BLOCKED_CONTRACT_REPAIR_REQUIRED`.

The frozen boundary, protocol, profiles, contract, schema, vectors, and design-audit bytes were preserved and verified. The design-side audit and S4-entry-freeze-v2 verifier pass, but neither is acceptance evidence.

The independent procedure confirms that the lexical numeric/unit grammar, explicit Unicode mapping boundary, 22 synthetic vector values, three externally fixed stable-ID digest vectors, and no-real-output condition pass. No real A01/A02 normalization was performed.

## Blocking findings

1. The closed top-level schema has five recursively open objects: `raw`, `sourceOrder`, `provenance`, `numericLexeme`, and `unitLexeme`. A schema-valid record can therefore hide `ownerNodeId`, `candidateId`, `mof`, or semantic metadata inside an object.
2. Those same open objects leave raw/sign/numeric/unit/provenance field shapes and null behavior undefined. `normalizationDisposition` is likewise an unrestricted string.
3. Source states and observation kinds are unrestricted strings, and no legal state/kind/disposition matrix is frozen.
4. `appliedRuleIds` accepts arbitrary strings and does not specify when numeric or unit recognition IDs are emitted.
5. Eligible word observations containing CR/LF/tab have no exact blocked disposition/output shape.
6. `nativeSourceOrderTuple` is named but not constructed. Two executors can choose different record ordering. The pretty-JSON policy also omits a final-newline rule.

The design audit did not expose these gaps: its stable-ID check is self-consistency rather than a known digest, and the listed negative assertions are labels rather than executed tests.

## Gate and next task

S4 stage authorization and the frozen v2 entry boundary remain valid; real-data execution remains `NOT_AUTHORIZED_PENDING_CONTRACT_REPAIR` and `NOT_STARTED`. The exact next task is **Batch-001 Wave 1 S4 Normalization Contract v2 Repair**. It must create a separately versioned contract/schema/vector package and preserve v1 as rejected research evidence.

No real S4 normalization, S5--S7, GT, benchmark, OCR, CSV, MOF, Wave 2, source replacement, frozen artifact mutation, canonical integration, history rewrite, or production adaptation occurred.
