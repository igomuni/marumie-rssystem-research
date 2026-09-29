# Canonical Semantic Extraction Protocol

Status: **FROZEN**
Date: 2026-09-29 (Asia/Tokyo)
Scope: request-side canonical semantic extraction only. This protocol is frozen by the commit that adds it; no history rewrite is used for self-reference.

## 1. Purpose and non-goals

This protocol fixes the common contract for converting an admissible official concept-request PDF into a source-faithful canonical dataset before any batch-scale execution. Its governing principle is:

> **Preserve source evidence and provenance before semantic interpretation.**

It does not authorize MOF acquisition/interpretation/normalization/linkage, linkage GT/evaluation, Batch-001 sampling or processing, CSV generation, source acquisition, OCR, production implementation, benchmark execution, or new GT.

## 2. Frozen stage model

`S0 Source admissibility → S1 authority preflight → S2 source observation → S3 structural interpretation → S4 normalization → S5 request-side semantic candidates → S6 financial association → S7 canonical freeze`.

- **S0:** require official provenance, source/package/file identity, lock status, SHA-256, and explicit `canonical_locked` / `survey_only` / `temporary_snapshot` status. A non-canonical source may support survey facts only; it cannot become a canonical authority artifact without a separately authorized admissibility decision.
- **S1:** freeze an authority preflight profile before candidate derivation.
- **S2:** retain source-visible and engine-observed text/glyphs/cells/blocks, locations, geometry when available, visible blanks, identifiers, labels, headings, units, and boundaries. Do not attach external meaning.
- **S3:** record source-observed versus inferred nodes/edges separately, including hierarchy, membership, context, continuation, unit applicability, and embedded containment.
- **S4:** retain raw values while recording deterministic code/circled-number/numeric/unit/whitespace/line-join normalization and version.
- **S5:** derive neutral request-side candidates only.
- **S6:** associate financial observations to their source-supported owner nodes; do not move them to semantic parents by convenience.
- **S7:** freeze the authority canonical artifact before any derived CSV, benchmark view, or later linkage activity.

## 3. Global invariants

1. Canonical bytes and provenance precede extraction.
2. Raw is never overwritten by normalized; observed is not inferred; inferred is not semantic; semantic is not linked.
3. `unknown != zero`; observed blank is not extraction failure; an engine miss is not source absence.
4. Preserve ambiguity, NULL outcomes, structural mismatch, and representation blocks as first-class states.
5. Preserve package/file/page/section/grammar/source-order boundaries.
6. Do not promote an arbitrary descendant, reconstruct an unprinted value arithmetically, or infer a parent amount from a child.
7. Do not use MOF information to repair or resolve request-side extraction, normalization, or candidates.
8. Source order is not semantic evidence unless the frozen authority profile establishes the relationship.
9. Unit scope is local to its established grammar/context; it must not silently become file-global.
10. Derived CSV views are not canonical storage; financial ownership must be explicit.

## 4. Authority preflight profile

Before S2, freeze one instance of `authority-preflight-profile.template.json`. It must record authority/source/package IDs, canonicality and SHA verification, representation/text/geometry availability, grammar classes and exclusions, package topology, context partitions, organization and unit scope, hierarchy/continuation behavior, embedded structures, ambiguity hazards, allowed/prohibited candidate rules, financial ownership rule, stop/failure rules, and provenance requirements.

The profile may classify but may not enumerate candidates, choose an authority for Batch-001, or use amount/benchmark/MOF outcomes as a design input. Cross-page and cross-file inheritance are prohibited unless explicitly authorized in this frozen profile with source evidence.

## 5. Node, relationship, and candidate contract

Canonical nodes may include organization/division, `organizationCandidate`, `itemCandidate`, `requestExpenseCandidate`, `breakdownNode`, `objectCodeNode`, remarks, embedded table, and other grammar-defined structure. A **candidate** is a source-grounded request-side semantic identity that may later become linkage input; it is not an assertion of a MOF `項` or `事項`.

Candidate minimums:

| Candidate | Minimum source-safe eligibility |
|---|---|
| `organizationCandidate` | visible organization code/name or equivalent scope anchor, grammar/context validity, provenance |
| `itemCandidate` | item-like code/name or structurally supported equivalent, organization/context provenance, structural relationship evidence |
| `requestExpenseCandidate` | available request number and/or expense code under the authority grammar, source-visible label, item/context relationship, provenance |

Missing identifiers do not globally forbid every candidate type; the profile must state the permitted evidence and ambiguity rule. Expense code suffixes, request numbers, item codes, and organization codes are not MOF join keys under this protocol.

Each edge records relationship type, `source_observed` or `structurally_inferred`, evidence locator, rule/profile version when inferred, and ambiguity state. Allowed types include `contains`, `parent_of`, `child_of`, `contextualizes`, `amount_belongs_to`, `label_belongs_to`, `continues_on_page`, `embedded_in`, and `source_order_precedes`.

## 6. Observation states and normalization

| State | Definition | Candidate/CSV behavior |
|---|---|---|
| `observed_value` | source shows a value | normalize only with recorded deterministic method; project value and state |
| `observed_blank` | source-visible field is blank | do not normalize to zero; project explicit state |
| `not_present_on_node` | field belongs elsewhere | preserve owner distinction; no implicit lookup |
| `not_applicable` | concept does not apply | project explicit state |
| `not_inspected` | outside coverage | no candidate assertion relying on it |
| `unknown` | inspected but indeterminate | no resolving normalization |
| `ambiguous` | multiple source-supported readings | preserve alternatives or block affected candidate |
| `not_extracted` | engine did not recover source evidence | do not recast as source blank |
| `not_created` | downstream artifact absent by design | project explicit state |

Normalization is allowed only for source-observed values and keeps raw text/lines/glyphs plus method/version. It may normalize circled `①` to `1`, numeric punctuation, a unit string, or visual line wrapping; it may not perform external linkage or create unobserved hierarchy.

## 7. Financial ownership and context

Every financial observation requires `ownerNodeId`, raw/normalized previous-request-delta fields where available, sign evidence, unit raw/normalized values, unit scope, provenance, and state. The three values may be one observation or separate observations when the source structure requires it. Arithmetic validation belongs to a later GT/validation layer, not S2–S6.

Context distance is explicit: same-node, same-row/block, same-page, same-section, same-file, cross-file. Default is conservative: cross-page/cross-file continuation requires frozen profile authorization, an evidence locator, direction/source order, and ambiguity handling. Grammar boundaries cannot be crossed for context, candidate relation, or unit inheritance without profile evidence.

## 8. Required Case-006–010 acceptance tests

| Case | Acceptance result | Contract test |
|---|---|---|
| 006 | PASS WITH CAVEAT | represent source-native text absence independently from engine/OCR-derived observation; retain source location/node possibility |
| 007 | PASS | represent request/expense candidate with `observed_blank` own amount and separate descendant financial owners; prohibit sum/inheritance/representative child |
| 008 | PASS | keep multi-grammar sections and local units separate |
| 009 | PASS | retain file identity as provenance/context partition and distinguish temporary survey from canonical locked source |
| 010 | PASS | retain main ledger and remarks-side embedded structures/local units as separate node/grammar families |

## 9. Canonical artifact and derived boundaries

At S7 freeze: source manifest/provenance; frozen preflight profile; nodes; edges; financial observations; candidates; unresolved/ambiguous states; and extraction/normalization/interpretation version metadata. Keep separate: engine raw output, derived CSV, benchmark result, all GT forms, and all future MOF linkage artifacts.

Permitted later CSV views are `source_files`, `document_nodes`, `document_edges`, `request_item_candidates`, `request_expense_candidates`, and `financial_observations`. Every projection retains node/owner IDs, raw/normalized pairing where relevant, provenance, and observation/ambiguity state. It must not claim to replace node-edge hierarchy.

## 10. Failure, batch, and readiness rules

Authority outcomes may be `SUCCESS`, `PARTIAL`, `NULL_SEMANTIC_CANDIDATE`, `STRUCTURAL_MISMATCH`, `REPRESENTATION_BLOCKED`, `SOURCE_INADMISSIBLE`, `AMBIGUOUS`, or `EXTRACTION_FAILURE`. These are not collapsed to zero records. One authority outcome cannot revise another authority’s frozen earlier stages.

Authorities may preflight and process in parallel only with independent artifacts. Within an authority, S0→S7 is strictly ordered; downstream results cannot retroactively modify source observations or prior frozen stages.

Semantic-data Batch-001 is not authorized until the protocol, artifact shape, preflight template, observation-state semantics, financial ownership rule, candidate vocabulary, provenance requirements, and the five acceptance tests are frozen. Exact stable-ID algorithm, geometry fidelity metric, authority grammar rules, and candidate-completeness metric may remain targeted validation. MOF mappings, join keys, amount linkage, descendant arithmetic, evaluator redesign, OCR policy, production architecture, Batch list, and population claims remain out of scope.

## 11. Next task

The next recommended task is **Semantic-data Batch-001 Design / Authority Sampling Protocol Freeze**. It may define deterministic sampling and orchestration using this protocol, but must not acquire MOF sources or execute Batch-001.

**This protocol is frozen from prior committed evidence only. It preserves request-side source evidence, structure, normalization, candidates, financial ownership, uncertainty, and provenance before any MOF linkage or batch execution.**
