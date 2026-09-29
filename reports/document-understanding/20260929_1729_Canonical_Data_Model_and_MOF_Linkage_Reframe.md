# Canonical Data Model / Loss-Minimized Extraction Contract / MOF Linkage Reframe

Date: 2026-09-29 (Asia/Tokyo)

## 1. Executive summary

The research target is reframed from selecting one amount-bearing row for benchmark comparability to constructing a **loss-minimized, source-faithful canonical structured dataset** for request PDFs. That dataset must preserve PDF hierarchy, source provenance, raw/normalized values, ambiguity, and the ownership of financial observations. Its derivatives can include CSV views, benchmark/evaluation views, and later independently adjudicated MOF item/matter linkage inputs.

This reframe is required by Case-007: a semantic request/expense identity node can be visibly distinct from its amount-bearing descendants. A canonical model that requires semantic identity and all amounts on one physical row would either discard that hierarchy or invent a value through inheritance/arithmetic. Neither is allowed.

The recommended next design task is **Canonical Semantic Extraction Protocol Freeze**, before a Batch Experiment Protocol. MOF-side source/schema work follows only after the request-side semantic contract is frozen. No MOF linkage, Batch Protocol, Batch-001, source acquisition, extraction, benchmark, or code change is performed here.

## 2. Objective change

Primary objective:

> Extract a canonical structured request-side dataset that preserves, as far as evidence permits, the information, hierarchy, and provenance of FY2024 concept-request PDFs, so that derived CSV views and later MOF item/matter linkage can be audited without rewriting source structure.

Secondary uses are benchmark evaluation, financial analysis, parser improvement, and CSV export. An amount-bearing physical row remains useful for a narrow benchmark profile, but is not the canonical semantic unit.

## 3. Evidence basis and non-goals

This design reads the committed Case-006–010 synthesis/evidence, closeouts, Case-007 protocol/NULL record/review, Cases 008–010 protocol/selection/GT/benchmark artifacts, source lock/registry, and representative raw/normalized/evaluation schemas. The machine-readable companion is [canonical-data-model-draft.json](../../evidence/document-understanding/canonical-data-model-draft.json).

It does not inspect a new source, render a PDF, obtain or search MOF data, generate CSVs, modify an extractor/normalizer/evaluator, create GT, or change a frozen artifact. The draft is a research design artifact, not a production schema or implementation commitment.

## 4. Terminology and canonical principles

- **Canonical store:** the source-faithful, versioned node/edge dataset; not a flat table, engine raw artifact, benchmark result, GT, or external linkage.
- **Node:** a source-located structural/contextual unit such as organization, item candidate, request/expense identity, breakdown, object-code row, remarks region, embedded table, or other grammar-defined structure.
- **Financial observation:** a separately owned observation of previous/request/delta/unit/sign, linked to the node where source evidence places it.
- **Semantic candidate:** a neutral interpretation hypothesis. PDF `item` is not renamed to an official MOF `項` without validated linkage.
- **Loss-minimized / source-faithful:** preserve available source distinctions and disclose unavailable information; do not claim literal layout-perfect losslessness.

Canonical principles: source SHA identifies bytes; raw values are never overwritten by normalized values; observed/inferred/semantic/linked layers remain distinct; blank is not zero; ambiguity is not resolved by desired output; and source order/provenance must permit audit back to the PDF.

## 5. Canonical entity and relationship model

### Source and location

`Source` holds `sourceId`, authority, fiscal year, account type, package ID, file ID, official/final URL, SHA-256, byte size, page count, acquisition provenance, and status (`canonical_locked`, `survey_only`, or `temporary_snapshot`). `Location` holds file identity, `pdfPageIndex`, printed page/prefix, source/reading order, section/grammar identity, and geometry when available.

### Structural nodes and text/identifiers

Each `DocumentNode` has a stable ID, node type, grammar identity, location, source order, and observation state. Types include authority/division/organization, item candidate, request/expense identity, breakdown, object code, remarks, embedded table, and other. Text and identifiers are child observations, retaining raw text/raw lines, normalized text, normalization method/version, raw code, normalized code, and confidence/ambiguity state.

### Relationships

Use typed edges: `contains`, `parent_of`, `child_of`, `contextualizes`, `amount_belongs_to`, `label_belongs_to`, `continues_on_page`, `embedded_in`, and `source_order_precedes`. Each edge declares whether it is **source-observed** or **structurally inferred**, its rule/version when inferred, and its provenance. A candidate semantic relation or external MOF link is never substituted for a source structural edge.

## 6. Stage boundary contract

```text
source acquisition
  → request raw extraction
  → request structural interpretation
  → request normalization
  → request semantic candidate freeze

MOF acquisition → MOF raw extraction → MOF structural interpretation
  → MOF normalization → MOF semantic record freeze

linkage candidate generation → linkage adjudication / GT → linkage evaluation
```

1. **Source-observed:** visible text/code, cell/row, amount, unit, glyph, page, geometry, heading, file identity.
2. **Structurally inferred:** parent/child, context scope, continuation, unit applicability, row ownership.
3. **Semantically interpreted:** neutral request item/expense candidates; not an asserted MOF mapping.
4. **Externally linked:** a request candidate paired with a MOF record under separately frozen linkage evidence/rules.

Request stages A–E must not use MOF information as extraction truth, normalization repair, or ambiguity resolver. The MOF side likewise has its own acquisition-to-semantic-freeze chain. Linkage is downstream and must preserve rejected/ambiguous alternatives.

## 7. Null, blank, unknown, and ambiguity semantics

Every attribute/relationship needs both a value channel and an observation state. Allowed states include:

| State | Meaning |
|---|---|
| `observed_value` | source visibly supplies a value |
| `observed_blank` | a source-visible field on this node is blank |
| `not_present_on_node` | field belongs elsewhere or does not occur on this node |
| `not_applicable` | concept does not apply to this grammar/node |
| `not_inspected` | task coverage did not inspect it |
| `unknown` | inspection occurred but evidence cannot determine it |
| `ambiguous` | more than one source-supported interpretation remains |
| `not_extracted` | engine/pipeline did not recover it |
| `not_created` | downstream artifact/record does not exist by design |

`0`, `""`, or `null` alone are therefore insufficient semantic encodings. A blank source cell is not a zero, and a benchmark miss is not a source blank.

## 8. Financial observation model

Financial observations are not identity fields:

```text
semantic identity candidate ── label/context/identifier observations
financial observation ─────── ownerNodeId + previous/request/delta + sign evidence + unit + provenance
```

Each amount retains raw text, normalized value when deterministically valid, sign glyph evidence, unit raw/normalized values, unit scope, owner node, and source locator. It must never be copied automatically to an ancestor, sibling, or semantic candidate merely because it is nearby.

## 9. Request-side linkage candidate view

A derived neutral record may expose `sourceId`, package/file/page locator, authority/division, raw+normalized organization/item/request/expense identifiers, raw label lines, normalized label, context provenance, structural node ID, and ambiguity state. Use names such as `requestItemCandidate` and `requestExpenseCandidate` until MOF terminology is externally verified. `01-95`/`05-95`, request number, organization code, and item code are not frozen as MOF join keys.

## 10. Case stress tests

| Case | Contract requirement |
|---|---|
| 006 MOJ | Preserve source location/representation even where native text is absent; keep source-native absence separate from engine OCR-derived signal. Do not delete a visually real node because raw native text is unavailable. |
| 007 CAS | Represent request/expense identity with `observed_blank` amount cells and distinct descendant amount nodes. Prohibit automatic child sum, nearest-descendant inheritance, and arbitrary representative-child selection. |
| 008 Courts | Preserve section/grammar identity, blank separators, and section/embedded-local units. One file cannot imply one grammar or unit. |
| 009 CAO | Preserve package/file identity and distinguish temporary survey snapshots from canonical locked sources. File identity may be context-bearing without numeric file order becoming a semantic key. |
| 010 MHLW | Preserve main ledger versus embedded remarks-side tables as separate structures, including local unit declarations. Do not flatten page content into one row family. |

## 11. CSV as derived views, not the store

Useful derived views are `source_files.csv`, `document_nodes.csv`, `document_edges.csv`, `request_item_candidates.csv`, `request_expense_candidates.csv`, and `financial_observations.csv`. They are auditable projections with stable IDs and provenance columns.

CSV cannot be called canonical or lossless: one row cannot naturally preserve a hierarchy, multiple parents/children, source versus inferred edges, multiple raw lines, or competing semantic candidates without opaque JSON stuffing. JSON/JSONL node-edge records or an equivalent relational graph are recommended for the canonical store; CSV is a versioned output view.

## 12. Provenance, IDs, and versioning

Stable node IDs should derive from source SHA-256 plus package/file identity, page locator, structural location/order, and interpretation version—not normalized labels alone. Preserve source SHA, printed/page locators, geometry when available, engine/version for raw output, normalization version, structural interpretation rule/version, and linkage version separately from GT version.

Geometry, exact typography, cell merge evidence, reading order, line wraps, blank cells, repeated headers, local units, remarks, and glyph forms are classified as follows:

| Treatment | Information |
|---|---|
| preserve exactly when emitted | raw text, raw lines, identifiers, numeric/glyph strings, source/file/page IDs |
| preserve structurally | nodes, edges, source order, hierarchy, grammar, blank cells, local units, embedded structures |
| preserve as provenance when available | geometry, merged cells, engine-native table/cell objects, extraction/normalization versions |
| optionally preserve | typography, whitespace fidelity, footnote rendering, exact layout snapshots |
| currently unavailable | source-native text for MOJ vector-outline pages; exact structure where an engine did not extract it |
| intentionally not inferred | unprinted parent totals, MOF mappings, stable join-key meaning, arbitrary descendant ownership |

## 13. Evaluation implications

The existing 11-check evaluator remains valid for its narrow single-row benchmark-comparability purpose. It is not the primary success definition for canonical semantic extraction. Future metrics may separately assess identity candidates, raw label preservation, hierarchy/context/unit recovery, financial owner association, provenance completeness, ambiguity preservation, false-link avoidance, and external-link adjudication. No evaluator change is made by this design.

## 14. Batch implications and decision table

The Cross-Case findings that remain valid are per-authority preflight, canonical locking, Survey→Protocol ordering, ambiguity/NULL preservation, failure isolation, and authority-parallel survey work. The single-row amount-triple selection profile, GT definition, evaluator, and output schema require redesign for semantic-data work.

| Decision | Classification |
|---|---|
| source/file/page provenance; raw+normalized pairing; node/edge preservation; financial owner separation; unit scope; derived CSV role | Freeze-candidate now |
| stable structural IDs; geometry fidelity; authority-profile rules; semantic candidate vocabulary; provenance completeness metrics | Needs targeted validation |
| MOF item/matter mapping; amount-based linkage; descendant arithmetic; evaluator extension; production schema | Deferred |

## 15. Future path recommendation

Option A (run the prior benchmark-comparability Batch-001 first) preserves useful baseline evidence but postpones the dataset needed for the stated MOF goal. Option C (parallel tracks) risks mixing incompatible semantic and benchmark contracts before either is frozen.

**Recommend Option B:** freeze a Canonical Semantic Extraction Protocol first, then design a semantic-data Batch-001 from that contract. The old benchmark remains a derived evaluation view when an authority fits its narrow profile; it is not discarded. After request-side semantic candidates are frozen, a separately scoped **MOF Item/Matter Source & Schema Survey** should establish the other side before any linkage protocol.

## 16. Integrity, validation, and next task

Only this report, its non-production machine-readable draft, and state files are changed. Cases 001–010 frozen artifacts, Cross-Case Synthesis, locks/registry, scripts, parser, normalizer, evaluator, OCR configuration, and production code remain untouched.

Recommended next task: **Canonical Semantic Extraction Protocol Freeze**. It should freeze contract semantics and authority preflight requirements without selecting Batch-001 authorities, extracting data, or beginning MOF linkage.

**This task redefined the research target from row-level benchmark comparability toward a source-faithful canonical dataset that can support later MOF item/matter linkage and derived CSV views. No MOF linkage was performed, no Batch Protocol was frozen, and no production extraction behavior or frozen research artifact was changed.**
