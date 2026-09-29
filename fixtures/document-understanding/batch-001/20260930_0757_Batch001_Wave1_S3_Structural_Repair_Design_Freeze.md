# Batch-001 Wave 1 S3 Structural Repair Design

Status: **FROZEN DESIGN**
Scope: A01 Kunaicho and A02 Shugiin S3 repair only; this is not a repaired-S3 execution.

## Scope and immutable evidence

This design starts from parent `bb86311499ab2183bff12389dfe78e9308ccdb2c`. It preserves the accepted S2 observations/raw XML and the reproducible failed experimental S3 graphs byte-for-byte. The baseline procedure and manifests are historical evidence and must not be relabeled as repaired output.

No source acquisition, S2 replacement, repaired S3 execution, normalization, semantic candidate derivation, financial association, canonical freeze, Ground Truth, benchmark, OCR, CSV, MOF work, Wave 2, source-lock mutation, or production adaptation is authorized here.

## Baseline defects addressed

The baseline page-wide `要求`/`番号`/`備`/`考` token test does not establish a local ledger header. The 57%-width rule does not establish a remarks boundary and captures ordinary outer-ledger columns. A02 local `百万円` tables are not represented as bounded structures. Inferred membership edges lack direct evidence, profile versions, and ambiguity states. The repair does not conceal these results; it creates a distinct `s3r1` output namespace for a later execution.

## Available evidence and limits

The retained S2 supports raw source-native text plus page/block/line/word bboxes, source order, raw XML, and locked file identity. It does not expose PDF drawing paths, true cell boundaries, or explicit blank cells. Accordingly, an inferred geometry union is an auditable structural group, not a claim that a PDF frame/cell was observed.

## Frozen structural contract

The repair uses a text-anchor plus geometry hybrid with explicit ambiguity.

1. `outerLedger` requires a same-page localized, geometrically ordered header-anchor group: 要求+番号, 事+項, 前年度予算額, 概算要求額, 備考; and two below-header row bands that repeat header x-ranges. Page-wide token presence, a generic x split, and cross-page inheritance are prohibited.
2. A nested/local structure must be a same-page bounded group with its own header anchor and two repeated x-cluster row bands. A02 `boundedLocalTable` additionally needs a raw local `（単位：百万円）` anchor and a local multi-column header. Right-side position, nearby outer content, or a unit string alone never suffice.
3. A01 structures that lack enough independent source support remain `ambiguousStructuralGroup`; A02 candidate local groups without the complete evidence remain structurally ambiguous. Neither is flattened into an outer ledger, semantic candidate, or financial owner.
4. Outer and local/nested groups are separate page-contained grammar partitions. There is no cross-page or cross-file inheritance and no outer/local unit inheritance.

## Evidence closure

Every inferred node and edge must carry `evidenceClass`, a versioned inference rule, frozen profile version, `ambiguityState`, source/file/page identity, direct supporting S2 observation IDs, a source-order/geometry evidence locator, and the rule inputs. Membership edges must cite the child observations and the parent anchor/group observations that caused the membership. Empty support lists and broad page-line lists are invalid where block or word geometry is decisive.

`state` is not overloaded: observation state remains separate from `structuralStatus` and `ambiguityState`.

## Manifest and ID boundaries

Future S2 manifests contain only S2 facts/statistics. Future S3 manifests contain all partitions and structural summaries. The existing mixed S2 manifests remain unchanged as baseline evidence.

Future repaired S3 records use namespace `s3r1`, deterministically derived from the source identity, page, primitive/rule, and sorted S2 support IDs. S2 IDs and all baseline S3 IDs remain unchanged. A repaired run writes separate `s3-repaired-v1` artifacts and must prove collision-free, byte-deterministic reruns.

## Readiness decisions

| Authority | Decision |
| --- | --- |
| A01 Kunaicho | `REPAIR_DESIGN_FROZEN_WITH_EXPLICIT_AMBIGUITY` |
| A02 Shugiin | `REPAIR_DESIGN_FROZEN_WITH_EXPLICIT_AMBIGUITY` |

Retained S2 is sufficient for the conservative repair design. This does not promise that every visibly framed source structure will receive an authoritative table label: where S2 cannot support the group, the required output is ambiguity or representation limitation. Neither frozen authority profile nor the common protocol requires amendment.

## Next execution gate

The only next authorized task is **Batch-001 Wave 1 S3 Structural Interpretation Repair Execution**. It must consume `wave-1-s3-structural-repair-spec.json`, preserve the baseline, create separate repaired artifacts, run deterministic reruns, and undergo another structural review before S4 can be considered.
