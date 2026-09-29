# Batch-001 Wave 1 S3 Structural Repair Execution

## Scope and status

This execution mechanically applied frozen repair specification
`batch-001-wave-1-s3-repair-v1` at design commit
`8d9867e742bfd3e1b17f57a6626b5e4ec59c1ff2`. It produced separately
versioned `s3-repaired-v1` graphs for A01/Kunaicho and A02/Shugiin.
Execution status is `EXECUTION_COMPLETE_WITH_REPRESENTATION_LIMITATIONS_AWAITING_REVIEW`.
It is not an S4 authorization or an acceptance review.

## Immutable-input audit

Before and after execution, the repair procedure verified every frozen hash
listed in `wave-1-s3-structural-repair-spec.json`: raw Poppler XML, S2
observations, experimental S3 nodes/edges and manifests, source manifest,
authority profile, and the original S2/S3 procedure. All matched. The frozen
repair specification, frozen authority profiles, and common protocol were not
modified.

## Mechanical implementation

The research-only procedure is
`fixtures/document-understanding/batch-001/s3_repaired_v1_execution.py`.
It reads only retained page, text-block, text-line, and word observations with
their raw engine-native text, geometry, source order, and source identity.

For `localized-outer-ledger-header`, raw glyphs are tested in a same-page,
localized header window. The window is anchored to an observed line band and
extends only by that page's maximum observed line height; it cannot chain
through an entire table. Required header groups and two below-header repeated
row bands are recorded as direct S2 support. No page-wide token rule or
page-width split is used.

For `same-page-bounded-structural-group`, a source-emitted text block must
provide its own header band and at least two repeated multi-cluster row bands.
A02 additionally requires raw `（単位：百万円）` and `総額及び計画年次` evidence in
the same block. Source-emitted box glyphs are evidence of a bounded text group,
not an inferred PDF frame or cell model. A01's one qualifying group is kept as
`nestedStructure`; A02's qualifying groups are kept as `boundedLocalTable`.

Every inferred record includes direct non-empty S2 support, locator bboxes and
source-order paths, rule input, rule/profile versions, ambiguity state, and a
separate structural status. `s3r1` IDs hash the frozen spec version, source
identity, page, primitive, rule, and sorted support IDs. Core JSONL uses
sorted keys, stable-ID ordering, UTF-8, and LF newlines.

## Outputs

| Authority | Nodes | Edges | Supported outer ledgers | Separate local/nested groups | Unclassified page partitions |
| --- | ---: | ---: | ---: | ---: | ---: |
| A01 Kunaicho | 68 | 67 | 19 | 1 nested structure | 14 |
| A02 Shugiin | 96 | 95 | 13 | 23 bounded local tables | 23 |

The outputs are under each authority's
`fixtures/document-understanding/batch-001/authorities/.../s3-repaired-v1/`
directory. The baseline experimental S3 remains alongside them unchanged and
is not represented as repaired evidence.

All 46 A02 `百万円` **text-line** occurrences counted by the frozen design
diagnostic are reconciled in the repaired structural manifest; all are members
of source-supported bounded local tables. This is structural grouping only:
no `百万円` value is normalized, associated with an outer row, or inherited
outside its local group. Outer `千円` and local `百万円` have zero inheritance
edges.

## Evidence and boundary audits

The deterministic audit confirmed unique node/edge IDs, resolved endpoints,
resolved support references, required provenance on every inferred record, and
zero old 57%-width or page-wide-token-only rule uses. There are zero
cross-page edges, cross-file edges, or outer/local unit-inheritance edges.

The output intentionally retains 14 A01 and 23 A02 unclassified page
partitions. These are representation-limited/insufficient-evidence outcomes,
not empty source claims and not failures repaired by guesswork.

## Deterministic rerun

An independent second run wrote into a fresh temporary output root. The core
nodes, edges, and structural manifests were byte-identical for both
authorities. Their hashes are recorded in
`evidence/document-understanding/batch-001/wave-1-s3-repair-execution-review-input.json`.

## Non-actions and next gate

No source acquisition, replacement, S2 replacement run, S4 normalization,
S5 candidate derivation, S6 financial association, S7 canonical freeze,
Ground Truth, benchmark, OCR, CSV, MOF, Wave 2, frozen-contract amendment,
canonical-parent merge, or production adaptation occurred.

The exact next task is **Batch-001 Wave 1 S3 Structural Repair Review and S4
Authorization Gate**. S4 remains unauthorized pending that independent review.
