# Batch-001 Wave 1 S3 Structural Repair Design Report

## Decision

The repair design is frozen as `wave-1-s3-structural-repair-spec.json`. It selects **text-anchor plus geometry grouping with explicit ambiguity**, not a repair of the old token/57%-width heuristic and not a new S2 observation method.

Both A01 and A02 receive `REPAIR_DESIGN_FROZEN_WITH_EXPLICIT_AMBIGUITY`. S4 remains unauthorized.

## Diagnostics

All retained S2 pages were inventoried without modifying them. The known baseline heuristic reproduces its prior page pattern: A01 pages 6–32 and A02 pages 6–35 have all four loose header tokens; this is recorded only as a baseline signal, not a validated partition. A01 has raw `千円` declaration observations on pages 4 and 6. A02 has 25 raw unit-declaration lines and 46 `百万円` occurrences on pages 14–22 and 35. The diagnostic JSON preserves the page, observation ID, source order, geometry, raw text, containing-block reference, and treatment for every A02 `百万円` occurrence.

The previously reviewed pages were re-used as source-review evidence: A01 4/5/6/11/19/32 and A02 4/5/6/17/20/35. All ten A02 pages with local-unit anchors were visually reviewed only to confirm the design conclusion: the material is visibly bounded but Poppler S2 does not expose PDF frame paths. The design therefore requires independently supported text/geometry groups and labels incomplete cases as ambiguous rather than manufacturing a frame.

## Alternatives

| Strategy | Result | Reason |
| --- | --- | --- |
| Repair loose tokens plus 57% threshold | Rejected | Neither page-wide token co-occurrence nor right-side position identifies a structural boundary. |
| Geometry/locality only | Rejected | Geometry alone cannot distinguish an outer amount column from a nested/local grammar. |
| Text-anchor plus geometry with explicit ambiguity | Selected | Uses retained raw evidence, requires local support for each inference, and preserves cases S2 cannot justify. |
| Add drawing/grid observation now | Deferred | Would be required only to promote representation-limited groups beyond the conservative contract; the existing S2 supports a safe ambiguity-preserving repair. |

## Rule and provenance consequences

`outerLedger` now requires a localized ordered header group plus repeated below-header column pattern. A bounded local table requires a same-page independent header/pattern; A02 also requires a local `百万円` anchor. No fixed page-width split is allowed.

All inferred records require direct S2 support IDs, source/file/page locator, rule/profile versions, rule inputs, `ambiguityState`, and separately represented structural status. This directly repairs the baseline's empty membership support and missing profile/ambiguity provenance. A repaired output receives a new `s3r1` namespace, so it cannot be confused with the baseline graph.

## Integrity and next task

Baseline S2/raw XML/current S3/profile artifacts remain immutable. Frozen profiles and the common protocol are unchanged; neither needs amendment. No repaired graph was executed, and no S4–S7, GT, benchmark, OCR, CSV, MOF, Wave 2, source replacement, or production adaptation occurred.

Recommended next task: **Batch-001 Wave 1 S3 Structural Interpretation Repair Execution**.
