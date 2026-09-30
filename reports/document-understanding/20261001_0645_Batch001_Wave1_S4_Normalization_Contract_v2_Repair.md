# Batch-001 Wave 1 S4 Normalization Contract v2 Repair

Created: 2026-10-01 06:45 JST

V2 preserves rejected `s4n1` and its independent review, and freezes `batch-001-wave-1-s4-normalization-v2` / `s4n2` pending independent review. No authority normalization was performed.

| V1 finding | V2 repair | Enforcement |
| --- | --- | --- |
| Open nested objects | Recursive closed `raw`, `sourceOrder`, `provenance`, numeric, and unit shapes | `additionalProperties: false` throughout |
| Undefined output shapes | Exact nested fields/nullability/disposition enum | v2 schema + vectors |
| Open state/kind matrix | Inventory-derived four-kind / observed-value matrix | schema conditionals + preflight contract |
| Open rule semantics | v2 rule enum, order, and iff emission rules | schema uniqueness + audit |
| Unsupported whitespace | Exact TAB/LF/CR blocked disposition | contract, schema, vectors |
| Ambiguous record ordering | `sourceRecordOrdinal` from exact JSONL sequence | metadata inventory + serialization test |

The metadata-only inventory observed A01 19,442 and A02 17,072 records, no blank lines, unique observation IDs, only four observation kinds and only `observed_value`; it reports no text values or lexical results. V2 freezes strict JSONL/pretty serialization including final LF, three fixed stable-ID known answers, and failure-atomic future execution behavior.

Design-side audit passes, but v2 is not independently accepted. S4 remains authorized at stage level and entry boundary v2 remains frozen; real-data S4 execution is `NOT_AUTHORIZED_PENDING_V2_CONTRACT_REVIEW` and `NOT_STARTED`.

Next task: **Batch-001 Wave 1 S4 Normalization Contract v2 Independent Review and Execution Gate**.

No real S4 normalization, S5--S7, GT, benchmark, OCR, CSV, MOF, Wave 2, source replacement, frozen/historical mutation, canonical integration, history rewrite, or production adaptation occurred.
