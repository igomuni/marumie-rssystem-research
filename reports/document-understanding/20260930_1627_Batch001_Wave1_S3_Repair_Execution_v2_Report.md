# Batch-001 Wave 1 S3 Repair Execution v2

Status: `EXECUTION_V2_COMPLETE_WITH_REPRESENTATION_LIMITATIONS_AWAITING_REVIEW`
S4 authorization: `NOT_AUTHORIZED_PENDING_INDEPENDENT_V2_REVIEW`

## Scope and inputs

This execution started from reviewed commit `97bce801b1e069fd075d275cadd2aca0bf47a688`, under frozen specification `batch-001-wave-1-s3-repair-v1` and semantic namespace `s3r1`. It consumes only the retained S2 observations and creates a separate execution-revision boundary, `s3-repaired-v2`; it does not change the v1 execution evidence.

The immutable baseline and all reviewed v1 outputs were SHA-256 audited before and after execution. Both audits passed. The frozen repair specification, authority profiles, common protocol, source locks, and registry are unchanged.

## v2 corrections

- Every `evidenceLocator` now copies the cited S2 `sourceOrder` object and engine-emitted bbox object verbatim. The independent audit found zero locator source-order/bbox failures across 1,455 A01 and 3,476 A02 locator entries.
- Synthetic document-to-page containment was removed from the page-scoped structural graph. Endpoint-derived counts are zero cross-page, zero cross-file, zero document-membership, and zero outer/local direct edges for each authority.
- Local/nested evidence now constructs word-level x-clusters inside each source-observed row band. Every supported group retains header-anchor observations, cluster membership/x-ranges, two repeating row bands, and direct header-to-row matches. The independent audit checked 1 A01 nested group and 23 A02 bounded-local-table groups; no cluster-evidence failure was found.
- Inferred edge IDs now use the frozen direct tuple with primitive `edge:contains`, excluding endpoint IDs. The audit reconstructed all 68 A01 and 118 A02 inferred record IDs with zero failure and no collision.

## Output and ambiguity preservation

| Authority | Nodes | Edges | Supported outer ledger | Supported local/nested | Unclassified |
| --- | ---: | ---: | ---: | ---: | ---: |
| A01 Kunaicho | 67 | 34 | 20 | 1 nested structure | 13 |
| A02 Shugiin | 95 | 59 | 15 | 23 bounded local tables | 21 |

A02's 46 immutable S2 text-line occurrences containing `百万円` were all reconciled. Only 2 are uniquely members of a supported bounded-local-table; the other 44 remain `not_structurally_grouped_representation_limited`. This is intentional uncertainty preservation, not an extraction failure or a unit inheritance assertion. No outer `千円`/local `百万円` inheritance or financial ownership was created.

The v1/v2 comparison is retained separately. The v2 graph has fewer edges because document scope is no longer emitted as page-scoped structural containment; the only page-partition changes are A01 page 30 and A02 pages 15 and 24, where the frozen header-and-row-cluster rule now closes direct evidence. This comparison is not an acceptance claim.

## Determinism and validation

An independent scratch-root rerun produced byte-identical `nodes.jsonl`, `edges.jsonl`, and structural manifests for both authorities. Core output hashes are recorded in the machine-readable review input. The review-only audit is independent from the executor and checks baseline/v1 preservation, support resolution, exact locator equality, direct-tuple IDs, endpoint-derived boundaries, cluster evidence, and the A02 reconciliation.

Repository validation and source tests remain required final checks before commit. This execution does not authorize S4; the next task is **Batch-001 Wave 1 S3 Repair v2 Review and S4 Authorization Gate**.

## Deliberate non-actions

No S4 normalization, S5 semantic candidate derivation, S6 financial association, S7 canonical freeze, Ground Truth, benchmark, OCR, CSV, MOF work, Wave 2 activity, source acquisition/replacement, v1 mutation, frozen-contract amendment, canonical-parent merge, or production adaptation occurred.
