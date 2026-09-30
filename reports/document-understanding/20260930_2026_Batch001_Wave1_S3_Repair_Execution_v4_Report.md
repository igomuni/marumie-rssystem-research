# Batch-001 Wave 1 S3 Repair Execution v4

## Execution result

V4 generated separate `s3-repaired-v4` graphs from immutable S2 under frozen spec `batch-001-wave-1-s3-repair-v1` and namespace `s3r1`. Execution status is `EXECUTION_V4_COMPLETE_AWAITING_INDEPENDENT_REVIEW`; S4 remains `NOT_AUTHORIZED_PENDING_INDEPENDENT_V4_REVIEW`.

The executor is `fixtures/document-understanding/batch-001/s3_repaired_v4_execution.py` (`4e16cc758d272c8538731d9b18f6e40f382e90ce054b1509843bbd65ff2c996b`). Its complete pinned repository-local helper set is v3 (`0bf74d5f5d8ff14340bd076d922925ea2764a5716077280276351c015efeb4bd`) and transitive v2 (`f682240c3f569ec472969da75a6d8740e96d97bda7f3b31a9b2d6e1bbb22b2b5`). The execution manifest records paths, hashes, roles, Python runtime, deterministic serialization, and exclusion of absolute paths.

## Narrow repairs

Every supported outer ledger now directly retains every immutable S2 source line geometrically containing each retained header word. Those source-line IDs, bboxes, word-to-line memberships, pairwise overlap/touch-with-tolerance relations, maximum line height, connectivity, and non-chained locality diagnostics are direct support and exact locators, not only a broad window.

Outer row-pattern acceptance now uses only strict observed x overlap. Tolerance-expanded proximity is not used by the algorithm. V4 found a different strict immutable-S2 reconstruction for A01 page 6; it remains supported with direct strict row-word evidence rather than a v3 tolerance-only assertion.

## Results

| Authority | Nodes / edges | Supported outer / unclassified | Local/nested |
| --- | ---: | ---: | ---: |
| A01 Kunaicho | 67 / 34 | 20 / 13 | 1 nested |
| A02 Shugiin | 95 / 59 | 15 / 21 | 23 bounded local tables |

Special-page outcomes are A01 p6 and p30 outer-ledger; A02 p6, p15, and p24 outer-ledger. No classification changed from v3; the v4 change is direct evidence/provenance closure and resulting direct-tuple IDs.

The independent execution-side audit reports zero immutable-baseline, locator, support, endpoint, page/file scope, direct-tuple ID, duplicate/collision, header-source-line membership, literal-band, strict row-word, local/nested, or dependency-hash failures.

A02 independently rebuilds 46 `百万円` source text-line occurrences: 23 direct-anchor supported members and 23 representation-limited non-anchor occurrences, with zero direct-anchor/treatment contradictions and zero shared direct anchors. The unchanged 23 supported local tables have zero same-page bbox overlaps.

## Preservation and reproducibility

Raw XML, S2, baseline experimental S3, v1, v2, v3, v3 review evidence, frozen spec/profiles/protocol, and source lock/registry were preserved. A clean-scratch rerun was byte-identical for both authorities' nodes, edges, structural manifests, and execution manifests.

## Next gate

The required next task is **Batch-001 Wave 1 S3 Repair v4 Review and S4 Authorization Gate**. This execution does not authorize or begin S4.

## Deliberate non-actions

No S4--S7 work, candidate derivation, financial association, Ground Truth, benchmark, OCR, CSV, MOF, Wave 2, source replacement, historical-graph mutation, frozen-contract/profile/protocol mutation, canonical-parent merge, or production adaptation occurred.
