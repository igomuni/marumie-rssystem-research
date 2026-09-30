# Batch-001 Wave 1 S4 Normalization Contract v2 Independent Review

Reviewed v2 commit: `29291e759dca5772267e190442a9dbfe997b4df8`
Canonical observed: `38f29ba8af4d2cd8a9795895726d5f7a06373490` (unchanged)

## Verdict

`REJECTED` — `REJECT_V2_CONTRACT`; execution gate `BLOCKED_CONTRACT_REPAIR_REQUIRED`.

V2 correctly preserves the rejected-v1 evidence, has closed nested keys, fixed stable IDs, source-record ordinal ordering, byte serialization rules, metadata-only S2 inventory reproduction, and no real S4 output. Those findings do not close the remaining relationship defects.

| Finding | Independent result |
| --- | --- |
| V1 recursive open nested keys | Closed and passes |
| Raw/sourceOrder kind coupling | Fails: page/word variants are separate valid `oneOf` branches but not linked to enclosing kind |
| Numeric semantic tuple | Fails: schema accepts inconsistent sign/glyph/canonical/magnitude tuples; contract gives only grammar/sign list |
| Unit semantic tuple | Fails: cross-mixed unit/code/multiplier triples remain schema-valid and are not normatively paired |
| Rule correspondence | Fails: enum/uniqueness exist, but wrong ordering and required/forbidden correspondence are not executable conformance cases |
| Negative assertions | Fails: most are labels without concrete input/expected outcomes |

The design audit is useful preservation evidence but only statically scans recursive closure and counts negative assertions. It does not instantiate adversarial records or test kind coupling, numeric/unit tuple consistency, or rule correspondence.

Real S4 execution remains `NOT_AUTHORIZED_PENDING_CONTRACT_REPAIR` and `NOT_STARTED`. The exact next task is **Batch-001 Wave 1 S4 Normalization Contract v3 Repair**.

No real S4 normalization, S5--S7, GT, benchmark, OCR, CSV, MOF, Wave 2, source replacement, frozen/historical mutation, canonical integration, history rewrite, or production adaptation occurred.
