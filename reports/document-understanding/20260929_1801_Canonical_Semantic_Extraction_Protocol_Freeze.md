# Canonical Semantic Extraction Protocol Freeze

Date: 2026-09-29 (Asia/Tokyo)

## 1. Decision

The Canonical Semantic Extraction Protocol is frozen at `fixtures/document-understanding/canonical-semantic-extraction/20260929_1801_Canonical_Semantic_Extraction_Protocol.md`. It adopts architecture **C: canonical node/edge records with derived relational/CSV views**. The preflight template is frozen alongside it. No separate machine-readable protocol JSON was created because the protocol Markdown and frozen JSON template are the authoritative, non-duplicative contract pair.

## 2. Evidence basis and scope

The decision uses only the committed canonical-model reframe/draft, Case-006–010 cross-case synthesis/evidence, pilot closeouts/selection artifacts, source lock/registry schema, and existing raw/normalized/evaluator schema examples. It applies only to request-side canonical semantic extraction, through authority canonical freeze. MOF-side work, linkage, production implementation, CSV generation, benchmark execution, GT, source acquisition, and Batch-001 remain excluded.

## 3. Alternatives assessed

| Alternative | Decision | Evidence-bounded reason |
|---|---|---|
| A: flat row-centric canonical protocol | Rejected | Case-007 separates request/expense identity from variable-depth amount descendants; flattening loses ownership or creates a forbidden inference. |
| B: node/edge protocol only | Not selected alone | preserves structure but does not explicitly define auditable downstream relational views. |
| C: node/edge canonical store + derived views | Selected | preserves hierarchy/provenance/ambiguity while allowing CSV/benchmark/linkage projections without declaring those projections canonical. |

## 4. Frozen decisions

- S0–S7 stage order is fixed: admissibility, preflight, observation, structural interpretation, normalization, semantic candidates, financial association, canonical freeze.
- Canonical-byte source admissibility and survey-only/temporary distinction precede all candidate work.
- Raw, inferred, normalized, semantic, GT, benchmark, and future linkage layers are separate.
- The neutral vocabulary `organizationCandidate`, `itemCandidate`, and `requestExpenseCandidate` is frozen; none is declared an MOF term.
- Observation-state vocabulary and financial `ownerNodeId` semantics are frozen.
- Cross-page and cross-file inheritance have conservative profile-only authorization.
- CSV is a derived view; canonical artifact content and authority-level outcomes are frozen before downstream views.

## 5. Case acceptance tests

| Case | Result | Why |
|---|---|---|
| 006 | PASS WITH CAVEAT | native source-text absence and OCR-derived engine observation are separately representable; OCR is not made mandatory. |
| 007 | PASS | parent identity can remain amount-blank while descendants own observations; no arithmetic or arbitrary child promotion is permitted. |
| 008 | PASS | section/grammar/unit locality blocks file-global inheritance. |
| 009 | PASS | file identity and canonicality state preserve split-package provenance/context. |
| 010 | PASS | main ledger and embedded remarks-side structures remain separate node/grammar families. |

## 6. Deferred decisions

Stable-ID exact algorithm, geometry fidelity metrics, authority-specific grammar rules, and candidate completeness measures require targeted validation. MOF mapping/join keys, amount-based linkage, descendant arithmetic, global OCR policy, evaluator redesign, production parser/schema, Batch-001 authority list, and population claims are deliberately not frozen.

## 7. State, integrity, and next task

Only the protocol, template, this report, and state files are changed. Existing pilots, Cross-Case Synthesis, reframe artifacts, source lock/registry, scripts, parser, normalizer, evaluator, OCR configuration, and benchmark artifacts remain unchanged.

Recommended next task: **Semantic-data Batch-001 Design / Authority Sampling Protocol Freeze**. It may set deterministic authority sampling/orchestration but must not start Batch-001 or MOF work.

**The Canonical Semantic Extraction Protocol was frozen using only previously committed research evidence. It defines how request-side source evidence, structure, normalization, semantic candidates, financial ownership, uncertainty, and provenance must be preserved before any MOF linkage or batch-scale execution. No Batch-001 authority was selected or processed, no MOF data was consulted, and no production extraction behavior or prior frozen artifact was changed.**
