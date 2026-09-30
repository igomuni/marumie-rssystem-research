# Batch-001 Wave 1 S3 Repair v3 Review and S4 Gate

## Verdict

The independent acceptance gate rejects both repaired v3 graphs for S4.

| Authority | S3 verdict | Outer ledgers emitted / independently accepted | Local/nested review |
| --- | --- | ---: | --- |
| A01 Kunaicho | `REPAIR_REQUIRED_BEFORE_S4` | 20 / 0 | 1 / 1 passes |
| A02 Shugiin | `REPAIR_REQUIRED_BEFORE_S4` | 15 / 1 | 23 / 23 pass |

Global S4 authorization is `NOT_AUTHORIZED`.

## Review independence and inputs

Review base: `3c7eb223089f84b39527a84339c53d8562d3172e`, on a new isolated review branch. The reviewer procedure is `evidence/document-understanding/batch-001/review-wave-1-s3-repair-v3-s4-gate.py`. It does not import or call the v1, v2, or v3 executors or their execution audits. It reads immutable S2 observations, the frozen repair specification, and v3 graph artifacts as the object under test.

The frozen baseline hash set passes for both authorities. The reviewed v1/v2 core node and edge hashes also pass. The repair specification, authority profiles, protocol, source lock, and registry are unchanged. No prior graph artifact was modified.

## Effective-procedure provenance

The v3 execution manifests pin the v3 procedure hash but do not pin the imported `s3_repaired_v2_execution.py` helper hash, although v3 imports and relies on that module. This is `INCOMPLETE_EFFECTIVE_PROCEDURE_PROVENANCE`: a future reader cannot reconstruct the effective procedure solely from the v3 manifest without consulting branch history. This is recorded as a required provenance repair alongside the structural defects; it is not a reason to alter historical v3 evidence.

## Mechanical checks that pass

For all inferred v3 nodes and edges, independent checks found:

- exact S2 support/locator source-order and bbox failures: 0;
- support source/file/page identity failures: 0;
- frozen direct-tuple ID reconstruction failures and duplicate IDs: 0;
- unresolved endpoints and cross-page/cross-file/cross-authority edges: 0;
- local/nested word-cluster failures: 0.

The clean-scratch v3 rerun is byte-identical for both authorities' nodes, edges, structural manifests, and execution manifests. This establishes determinism, but does not cure the acceptance defects below.

## Outer-ledger failure

The frozen rule requires direct source **line** evidence for one local header band, defined by overlap/touch using the page maximum observed line height, and direct row **word** evidence for two repeated header x-ranges in each qualifying row band.

The v3 graph's header-band field does not retain every actual S2 text line containing the header words. On 19 of A01's 20 emitted outer ledgers and 14 of A02's 15, the independent review resolved header words to source lines absent from `literalHeaderBand.memberLineObservationIds`. Consequently the required source-line overlap/touch relation cannot be audited from the v3 record. The graph's retained broad window is not a substitute for the missing source-line membership.

A01 page index 6 is the remaining special failure: its retained header lines close, but its first qualifying row has only one strict observed x-range overlap. Its second claimed match exists only after the executor's max-line-height x expansion. The frozen rule requires repeated header x-ranges and does not authorize that expansion as a replacement for strict observed overlap.

A02 page index 6 is the sole emitted outer ledger that independently closes both literal-band provenance and strict row-word x-range checks. It is insufficient to accept the A02 graph as a whole.

The full-page matrix in the machine-readable review record classifies all non-emitted pages conservatively as unclassified because no complete page-local header-plus-strict-row-word evidence pack was independently reconstructed. Agreement is 13/33 pages for A01 and 22/36 for A02; every disagreement is an emitted v3 outer ledger rejected for the evidence defects above.

Special-page results:

| Page | Result |
| --- | --- |
| A01 p6 | Rejected: one tolerance-dependent-only row-header match. |
| A01 p30 | Rejected: missing actual header source-line membership. |
| A02 p6 | Individually accepted outer-ledger reconstruction. |
| A02 p15 | Rejected: missing actual header source-line membership. |
| A02 p24 | Rejected: missing actual header source-line membership. |

## A02 local-unit audit

Immutable S2 independently yields 46 `百万円` text-line occurrences. The v3 reconciliation contains all 46: 23 `member_of_supported_boundedLocalTable` direct anchors and 23 `not_structurally_grouped_representation_limited` non-anchors. Direct supported-anchor/treatment contradictions are zero, shared direct anchors are zero, and same-page supported-table bbox overlaps are zero. This fixes the v2 graph/manifest certainty conflict, but does not compensate for the failed outer-ledger gate.

## Required repair scope and next task

The narrowest next task is **Batch-001 Wave 1 S3 Repair Execution v4**. It must preserve all historical evidence and repair only the rejected v3 acceptance boundary:

1. Retain the actual S2 source-line IDs/bboxes that contain every header word, and encode auditable overlap/touch/locality relations rather than a broad header window.
2. Do not call a row pattern satisfied if a required header-range match depends solely on an uncontracted x expansion; downgrade where strict source geometry does not close.
3. Pin the imported v2 helper and every behavior-affecting dependency in the effective-procedure provenance.

S4 has not started and remains unauthorized.

## Deliberate non-actions

This review did not modify v3 or any earlier graph, raw XML, S2, frozen specification/profile/protocol, source lock/registry, or canonical parent. It performed no S4--S7 work, candidate derivation, financial association, Ground Truth, benchmark, OCR, CSV, MOF, Wave 2, source replacement, or production adaptation.
