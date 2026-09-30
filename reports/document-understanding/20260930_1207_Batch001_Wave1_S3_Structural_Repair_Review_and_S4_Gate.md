# Batch-001 Wave 1 S3 Structural Repair Review and S4 Gate

## Decision

This independent review rejects both repaired S3 graphs for downstream S4
use. A01/Kunaicho and A02/Shugiin are each
`REPAIR_REQUIRED_BEFORE_S4`; global S4 authorization is `NOT_AUTHORIZED`.
The frozen repair specification and authority profiles are not contradicted,
so the next task is **Batch-001 Wave 1 S3 Repair Execution v2**, not a spec or
profile amendment.

## Inputs and independent method

The review branch starts at execution commit
`509cc4236a410d4434a5c500cea464e73db9f787`, built from frozen design commit
`8d9867e742bfd3e1b17f57a6626b5e4ec59c1ff2`. The canonical parent remains
`bb86311499ab2183bff12389dfe78e9308ccdb2c` and was not merged.

The review-only procedure
`evidence/document-understanding/batch-001/review-wave-1-s3-repair-s4-gate.py`
does not import the executor. It recomputes immutable hashes, parses every S2
and repaired JSONL record, reconstructs IDs, resolves evidence locators, and
derives endpoint page/file boundaries and structural-rule evidence directly
from retained S2 data.

All frozen baseline hashes matched the repair specification. The frozen
specification, profiles, common protocol, source lock, registry, baseline S2,
and baseline experimental S3 were unchanged.

## Evidence-closure finding

The central defect is reproducible for every inferred record:

| Authority | Inferred records | Nonempty/resolved S2 support | Matching locator bboxes | Matching locator source-order paths |
| --- | ---: | ---: | ---: | ---: |
| A01 | 101 | 101 | 101 | 0 |
| A02 | 154 | 154 | 154 | 0 |

The executor stores each `evidenceLocator.sourceOrder` as the observation ID,
not the immutable S2 `sourceOrder` object. Thus a reviewer can find a cited
observation and its bbox but cannot use the repaired locator as the promised
source-order path. This violates the frozen evidence-closure contract; it is
an execution defect, not a source-evidence gap.

## Independently derived graph boundaries

All graph endpoints resolve and no edge crosses files or joins authorities.
However, the review derived 32 A01 and 35 A02 cross-page endpoint pairs.
They are `document -> page` edges emitted as `structurally_inferred`, where
the document node is assigned page 0. These are not semantic continuation
claims, but they contradict the execution artifact's reported zero
cross-page-edge counts and conflate document containment with a page-scoped
inference. The v2 execution must represent document scope separately or
exclude document-to-page membership from a page-context metric with an
explicit, frozen-consistent classification.

There are zero direct outer-ledger/local-table edges and no unit-inheritance
relationship. That does not cure the local-structure evidence defect below.

## Rule-fidelity findings

### Outer-ledger rule

The review reconstructed all 19 A01 and 13 A02 supported outer-ledger inputs.
Each has required glyph sets, left-to-right group geometry, and two recorded
below-header row bands. The raw glyph sequences are columnar rather than
literal horizontal strings on all 32 pages (for example, a budget header's
glyphs are arranged across two visual rows). That can be consistent with the
frozen raw-glyph rule, but the implementation must record an explicit geometry
and reading rationale rather than make character-multiset consumption itself
appear to establish phrase identity. This limitation is not by itself the
blocking result; the locator defect makes the necessary evidence audit
incomplete.

The equality-y vertical bands plus later header window are not a documented
literal implementation of the frozen overlapping/touching-band language.
The emitted inputs can be inspected from S2, but v2 must preserve the actual
header-band membership and its page-local tolerance calculation as evidence.

### Nested/local structures and repeated x-clusters

The review independently finds two row bands with at least two repeated
x-clusters for A01's one nested structure and all 23 A02 bounded local tables.
But the executor did not enforce or record that comparison: it accepted a band
when it had at least two words, then stored only one header-anchor line. No
emitted local/nested node carries two directly cited header x-clusters that
can be compared to its row bands. Consequently the frozen requirement for an
own header-anchor group plus repeated x-cluster row bands is not evidence
closed, even where the source geometry appears compatible.

All 24 emitted groups contain immutable source-emitted `┌` and `│` glyphs.
This is an acceptable conservative text filter so long as it remains a filter,
not a claim of observed PDF drawing/cell boundaries. For all 23 A02 groups,
the immutable source block also contains the raw `（単位：百万円）` anchor and
`総額及び計画年次` local header literal. The literal is source-observed and
adequate for these emitted groups, but it is not a globally frozen synonym for
every possible local multi-column header.

## A02 unit accounting

The review independently counted 46 immutable S2 `textLine` occurrences of
`百万円`; all have one resolved treatment and are assigned to supported local
table nodes. The count is complete, but the groups cannot be accepted while
their header/x-cluster and locator provenance remain defective. No amount is
normalized or inherited into the outer `千円` ledger.

## ID and determinism

Node IDs uniquely reconstruct from the frozen direct tuple. Edge IDs are
unique and deterministic under the executor's parent/child-ID derivation, but
that derivation is not the frozen direct source/file/page/primitive tuple.
This is an execution defect requiring v2 correction or an explicitly scoped
future spec clarification; it does not justify modifying the frozen spec in
this review.

## Required v2 repair boundary

The next execution must preserve the existing repaired graph as reviewed
evidence and write a new versioned output. It must, at minimum:

1. retain actual S2 `sourceOrder` objects in each locator;
2. distinguish document membership from page-scoped structural inference and
   recompute cross-page counters from endpoints;
3. encode direct header-column observations and the deterministic
   header-to-row x-cluster comparison for every nested/local group;
4. make outer-header band membership/tolerance auditable; and
5. construct edge IDs from the frozen direct ID tuple.

No repaired artifact was changed in this review. No S4 normalization, S5
semantic candidates, S6 financial associations, S7 canonical freeze, Ground
Truth, benchmark, OCR, CSV, MOF, Wave 2, source replacement, frozen-contract
change, canonical-parent merge, or production adaptation occurred.
