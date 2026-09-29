# Batch-001 Wave 1 S2/S3 Integration and Structural Review

## Purpose and boundary

This integration gate reviews the independently committed S2 source-observation and experimental S3 structural-interpretation artifacts before S4. It does not normalize values, derive semantic candidates, associate finances, freeze canonical authority data, create Ground Truth, benchmark, run OCR, generate CSV, consult MOF material, or start Wave 2.

## Inputs and integration

The frozen parent was `210a039dc7131bf52e631746d3c4458a36041748`. The review used A01 commit `dab6429025debdb6a4ba64abdd611d87a2ce6d88` and A02 commit `0a9e9cbc458018640ae823907d4030cec65cab1c`. Each commit was audited first: it adds only that authority's S2/S3 evidence, report, and local non-production procedure. Both were then cherry-picked without conflict into an isolated integration-review branch; no shared protocol, profile, state, source lock/registry, production script, GT, benchmark, or unrelated authority artifact changed during integration.

## S2 integrity audit

| Authority | Locked SHA / pages | S2 records | Re-run core artifacts | S2 verdict |
| --- | --- | ---: | --- | --- |
| A01 Kunaicho | `ffab…e261` / 33 | 19,442 | raw XML, observations, nodes, and edges byte-identical | `ACCEPT_WITH_DOCUMENTED_OBSERVATION_GAPS` |
| A02 Shugiin | `30d0…c435` / 36 | 17,072 | raw XML, observations, nodes, and edges byte-identical | `ACCEPT_WITH_DOCUMENTED_OBSERVATION_GAPS` |

For both authorities, source SHA, PDF page count, Poppler XML page count, all-page S2 coverage, JSON/JSONL parsing, observation/node/edge-ID uniqueness, and non-empty evidence-reference resolution passed. Method metadata records source-native `pdftotext -bbox-layout`, `sortApplied: false`, no OCR, no rendering for extraction, and raw XML kept separately. There are no S4–S7 artifacts, GT, benchmark, MOF, or cross-authority fields.

S2 is reusable as a source-native text-and-geometry substrate. It is not a complete representation of every source-visible feature: Poppler bbox-layout preserves page/block/line/word text geometry but does not create explicit source cell boundaries, drawing/grid objects, or visible blank-cell observations. These omissions are engine limitations, not assertions that the source lacks those structures. Replacement-character counts are zero in both observed corpora.

### S2/S3 separation finding

`source-observations.jsonl` is source-observation-only. However, each artifact declared `stage: S2` contains per-page `structuralPartition` and `remarksSideBlockCount`, both calculated by the S3 token/geometry heuristics. This is a **S2 manifest metadata/layering defect only**, not core-observation contamination. A subsequent S3 repair must place such inferred summaries exclusively in S3 output or label them unambiguously as cross-stage run metadata.

## Deterministic structural review

Review pages were selected from manifests before conclusion: populated early unclassified pages, the unclassified-to-classified boundary (5/6), early/middle/late classified pages, maximum right-side count, and—on A02—the local-unit table context. Visual inspection used locked-PDF rendering only and created no new canonical observations.

| Authority | Reviewed `pdfPageIndex` | Result |
| --- | --- | --- |
| A01 | 4, 5, 6, 11, 19, 32 | Page 4 is a summary-style table and pages 5/6 show the transition into the detail ledger. On ledger pages, the right-of-57%-width region includes outer-ledger amount/delta columns as well as the actual remarks-side nested structures. Page 11 has the highest recorded right-side block count (187), visibly demonstrating multiple nested regions rather than a single homogeneous remarks region. |
| A02 | 4, 5, 6, 17, 20, 35 | Page 4 is a summary-style table and pages 5/6 show the detail-ledger boundary. Page 17 visibly contains the outer ledger plus a framed local `百万円` table; the existing graph records only generic right-side blocks/remarksRegion, not that local table as a bounded distinct structure. |

The `outerLedger` rule checks only the co-occurrence of `要求`, `番号`, `備`, and `考` in page text. It can identify a common header signature, but it has no geometry, header adjacency, or grid-boundary test and therefore has unmeasured false-positive and false-negative risk. The review does not treat its 27/33 and 30/36 page counts as structural validation.

The `xMin >= 0.57 * pageWidth` rule is not structurally equivalent to a remarks-side region. It necessarily captures ordinary outer-ledger columns on the reviewed detail pages and collapses potentially multiple structures into a generic `remarksRegion`. This fails the profile requirement to preserve nested/local structures separately. For A02 specifically, raw co-occurrence of `千円` and `百万円` does not establish the mandated separation of outer-ledger and framed local-table unit scopes.

## S3 evidence closure and state audit

All edge endpoints and non-empty observation references resolve. That syntactic result is insufficient. The right-side inference is based on block geometry, but remarks-region nodes and their parent edges cite broad page-line sets rather than the decisive block observations. More critically, the inferred `remarksRegion -> sourceTextBlock` membership edges carry empty `supportingObservationIds`: 3,544 of A01's 3,604 inferred edges and 1,928 of A02's 1,994 inferred edges are unsupported in this required provenance field.

Every inferred edge also omits the frozen protocol's required inferred-edge `profileVersion` and `ambiguityState`; inferred nodes/edges use `state: observed_value`, which does not by itself communicate structural inference or ambiguity. The current experimental S3 output therefore lacks evidence closure even where its endpoints resolve.

Mechanical boundary checks pass: zero cross-page edges, zero cross-file edges, no continuation inference, no financial-ownership output, no arithmetic reconstruction, and no semantic candidates. The A02 historical landing-page caveat remains provenance-only metadata.

## Verdicts and downstream decision

| Authority | S2 | S3 | Can S4 consume S2? | Can S4 use S3 as authoritative input? |
| --- | --- | --- | --- | --- |
| A01 | `ACCEPT_WITH_DOCUMENTED_OBSERVATION_GAPS` | `REPAIR_REQUIRED_BEFORE_S4` | Yes, without reacquiring or rerunning source observation | No |
| A02 | `ACCEPT_WITH_DOCUMENTED_OBSERVATION_GAPS` | `REPAIR_REQUIRED_BEFORE_S4` | Yes, without reacquiring or rerunning source observation | No |

The existing S3 graphs are retained as reproducible, non-production experimental evidence, not deleted or silently corrected. Their defects can be repaired deterministically from the retained S2/raw XML; additional source observation is not demonstrated as necessary. The frozen common protocol and authority profiles already require the distinctions that the current S3 implementation misses, so this is an **implementation/provenance repair requirement**, not a common-protocol or profile amendment.

**S4 is not authorized.** The next task is **Batch-001 Wave 1 S3 Structural Interpretation Repair Design and Freeze**: define a source-supported partition/table-boundary and evidence-closure procedure from the retained raw/S2 artifacts, preserve the present S3 run as a baseline, then conduct any repair in a separately scoped task.

## Integrity and non-actions

The original A01 and A02 branches remain unchanged. No frozen profile/protocol was edited; no source lock/registry, production parser/normalizer/evaluator, or state on authority branches changed. No S4 normalization, S5 semantic candidate derivation, S6 financial association, S7 canonical freeze, GT, benchmark, separate OCR, CSV, MOF work, or Wave 2 work occurred.
