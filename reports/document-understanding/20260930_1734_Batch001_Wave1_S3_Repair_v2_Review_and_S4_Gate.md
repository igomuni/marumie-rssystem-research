# Batch-001 Wave 1 S3 Repair v2 Review and S4 Authorization Gate

Review base: `8d8baec47b551bfb3c9077ae1dab93fffd694984`  
Frozen repair specification: `batch-001-wave-1-s3-repair-v1`  
Global S4 decision: `NOT_AUTHORIZED`

## Scope

This is an independent acceptance review of the separate `s3-repaired-v2` execution. It did not alter v2, v1, baseline S2/S3, raw XML, frozen protocol/specification/profiles, sources, or production code. The review-only procedure is independent of the executor and the execution audit.

## Preservation and mechanical blocker retest

The immutable baseline hashes and all reviewed-v1 hashes pass. Frozen specification, profiles, and common protocol are unchanged. V2 core artifacts were not modified during review.

All four v1 mechanical blockers are closed:

- Every inferred-record locator exactly matches its cited immutable S2 source-order object and bbox; A01 and A02 have zero exceptions.
- Endpoint-derived graph checks find zero unresolved endpoints, cross-page edges, cross-file edges, document-membership edges, or direct outer/local edges.
- Direct word-level header-to-row x-cluster evidence is present and independently range-reconstructible for A01's one nested structure and A02's 23 bounded local tables.
- Inferred node and edge IDs reconstruct from the frozen direct tuple with zero failures or collisions; edges consistently use `edge:contains` without endpoint IDs as hash inputs.

An independent scratch-root rerun reproduced both authorities' core nodes, edges, and structural manifests byte-for-byte.

## Acceptance findings

### A01 Kunaicho

V2 has 67 nodes and 34 edges: 20 supported outer-ledger partitions, one supported nested structure, and 13 unclassified partitions. The local/nested cluster rule is evidence-closed.

However, all 20 supported outer-ledger nodes cite source-observed *line* bands and derived match indices, but do not retain the concrete S2 **word** observations needed to reproduce the required repeated header x-range relation. A line bbox can span several printed columns and cannot substitute for word-level column evidence. One outer header also fails the review's literal local-band reconstruction. This is insufficient for the frozen outer-ledger contract.

Verdict: `REPAIR_REQUIRED_BEFORE_S4`.

### A02 Shugiin

V2 has 95 nodes and 59 edges: 15 supported outer-ledger partitions, 23 supported bounded local tables, and 21 unclassified partitions. The local-table geometry has no same-page overlap and no shared local-unit anchors; all 46 source `百万円` text-line observations fall within exactly one supported-table bbox.

The same outer-ledger evidence-closure defect remains: 15 supported outer-ledger nodes omit the direct row-word evidence required for repeated header x-range reconstruction, and one outer header fails literal band reconstruction.

There is also a graph/manifest certainty mismatch. The reconciliation records two `百万円` occurrences as supported-table members and 44 as representation-limited, yet 21 of the latter are direct local-unit-anchor observations used by nodes asserted as `structurally_supported`. This is not coherent occurrence-level uncertainty: an observation cannot simultaneously be the direct local-unit basis for a supported table and be recorded as not structurally grouped. The required next execution must either align reconciliation with the graph's direct evidence or downgrade the conflicting groups to an allowed ambiguous/representation-limited structural outcome.

Verdict: `REPAIR_REQUIRED_BEFORE_S4`.

## Changed-page and delta review

V2's A01 page 30 and A02 pages 15 and 24 outer-ledger promotions are not accepted merely because locator or ID evidence was repaired. They remain subject to the same missing word-level outer row-pattern evidence. The v1-to-v2 edge reductions are explainable by removing synthetic document containment, but that provenance improvement does not repair the outer-structure acceptance gap.

## Decision and next task

The frozen repair specification and authority profiles remain sound; the remaining failures are execution/evidence-closure defects. Do not amend the frozen contract and do not integrate the reviewed chain into the canonical parent.

The exact next task is **Batch-001 Wave 1 S3 Repair Execution v3**. It must preserve v1/v2, add direct row-word supports and literal local-band evidence to every outer-ledger inference, and reconcile A02 local-unit-anchor claims with graph structural status before another independent S4 gate.

## Deliberate non-actions

No S4 normalization, S5 semantic candidate derivation, S6 financial association, S7 canonical freeze, Ground Truth, benchmark, OCR, CSV, MOF work, Wave 2 execution, source replacement, v1/v2 graph mutation, frozen-contract mutation, canonical-parent merge, or production adaptation occurred.
