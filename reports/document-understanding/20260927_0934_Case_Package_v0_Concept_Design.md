# Case Package v0 — Concept Design / Architecture Review Candidate

Status: **design candidate for review. Not an ADR. No schema, migration, or implementation in this task.**

Date: 2026-09-27 (Asia/Tokyo)

## 1. Executive summary

This document designs, at the concept/requirements level only, a "Case Package v0" that formalizes what five cases' worth of research (case-001 through case-005, plus the five-ministry interim synthesis) has actually shown to matter. It is explicitly **not** a fresh invention: this repository already has a real, partially-implemented predecessor — a `schemaVersion: 0` `document-profile.json` + `research-history.jsonl` pair, backfilled for case-001 and case-002 only, under the design proposed in `reports/document-understanding/20260926_1316_Case_Based_Document_Understanding_and_LLM_Strategy_Selection_Research_Architecture.md` (ADR-010/011/012). This task's job is to relate to that existing work explicitly, identify what three more cases and four rounds of anomaly/context/normalization research have taught that the Phase-1 design could not have known, and produce a reviewable concept — not to silently supersede or ignore what already exists.

The central, load-bearing idea carried through every section below: **Ground Truth isolation, source-safe/engine-derived provenance, and first-frozen-history preservation are not implementation details to add later — they are the reason a Case Package exists at all**, and every object/layer/lifecycle decision below is evaluated against whether it protects or threatens those three invariants.

## 2. Scope / non-goals

This task performs architecture/requirements/dependency-boundary design only. No JSON Schema, no TypeScript/JavaScript implementation, no migration script, no benchmark/evaluator/normalization/extraction change, no new PDF inspection, no new source acquisition, no benchmark rerun, no Ground Truth change, no case-001–005 migration, no generated Case Package files, no Strategy Selection implementation, no MOF linkage, no anomaly-detector work, no case-006, no ADR finalization, no PR, no merge. This document is a **design candidate for review**, not a decision.

## 3. Evidence base

Read in full or in relevant part before design work began: the five-ministry interim synthesis (`7a41cea`); all five cases' source surveys, selection protocols, selection records, and Ground Truth evidence; all five cases' first-frozen benchmark reports and current evaluation reports; the CJK-spacing normalization study (`bac939b`, `df2d1c3`); case-004's context diagnostics (`187a8e9`, `aedea1c`) and four anomaly-channel studies (`075474e`, `a9c0092`, `acaf550`, `22d50df`); `reports/document-understanding/20260926_1316_...Architecture.md` and ADR-010/011/012 in `protocol/DECISIONS.md`; `sources/source-lock.json`/`sources/source-registry.csv`; the current fixture/evidence/report directory structure; and, critically, the **actual existing** `fixtures/document-understanding/case-001/document-profile.json`, `case-001/research-history.jsonl`, `case-002/document-profile.json`, and `case-002/research-history.jsonl` files, read in full to establish the real prior schema rather than the architecture report's own illustrative sketch of it.

**Existing Case Package concept found and explicitly related to, not overwritten**: the Phase-1 backfill already implements a working `schemaVersion: 0` structure — `identity{}`, `sourceSafeProfile{features:[{key,value,provenance,note,evidence}]}`, `engineDerivedProfile{features:[...]}}`, and a separate `research-history.jsonl` with `{eventId, kind, status, layers, date, commit, summary, evidence, relatedEvents}` per line, where `kind ∈ {observation, hypothesis, intervention, result, conclusion, unresolved_question}` (per ADR-010's own layer vocabulary reused directly, e.g. `"layers": ["document_family_layout_interpretation"]`). **This was never extended to case-003, case-004, or case-005** — each of those three cases' own tasks explicitly deferred Case Package creation ("Not done, by design: no Case Package created"). This gap, not a design flaw in the Phase-1 schema itself, is the primary evidence motivating this task's own work: three more cases, an entire context-diagnostic research line, and four anomaly-channel studies exist with no Case Package representation at all.

## 4. Design principles (evidence-backed, not invented for this task)

- **Ground Truth is read only by evaluation** (already an absolute invariant across all five cases, re-verified at every Ground Truth freeze and every packaging-review task).
- **A feature is source-safe only if this repository actually established it before running any compared engine** — ADR-011's own decision, already tested against a real boundary case (case-002's annotation-column placement) and re-confirmed relevant by case-004's Docling channel producing the *same* signal value from both a genuine source anomaly and a pure engine-segmentation artifact (§8 below).
- **A rule's validity layer is classified by where its assumption actually breaks, not by which file it happens to live in** — ADR-010's own finding, re-confirmed by the five-ministry synthesis's own `item_name_exact_match` analysis (heterogeneous mechanism, uniform outcome).
- **First-frozen results are preserved, never silently overwritten by a later adaptation** — demonstrated concretely at every one of case-002/003's own normalization improvements, and explicitly required again here for any future Case Package history model.
- **Isolation claims must be stated at their true strength** — ADR-012's own "behavioral, not sandboxed" disclosure rule, directly relevant to any future use of a Case Package for LLM strategy selection.
- **`unknown != zero`, and absence of a recorded fact is not evidence of its non-existence** — already the explicit convention in case-001's own Phase-1 `document-profile.json` (`"value": "not_recorded"`, with the note "unknown != zero: this is an absence of a recorded fact, not evidence the document has 0 pages") and in this program's own `protocol/RESEARCH_PROTOCOL.md`.

## 5. Case Package role

### 5.1 What a Case Package should be

- A reproducible record of one benchmark/research case, sufficient for another researcher (human or LLM) to understand what was done and why, without re-deriving it from prose.
- A stable reference to source provenance (not a copy of the source itself).
- A holding place for source-derived observations, with their actual discovery method preserved (ADR-011).
- An explicit statement of what context a given field required to recover (page-local / neighbor-page / table-metadata — five-ministry synthesis §12).
- A boundary that keeps engine observations comparable across engines and across cases, without conflating one engine's own artifact with another's.
- A boundary that keeps normalization operations traceable back to the rule that produced them (CJK-spacing study, five-ministry synthesis §13).
- A boundary that makes semantic interpretation's own inputs and outputs explicit, so a uniform outcome (e.g. `item_name_exact_match` FAIL in 5/5 cases) does not silently erase a heterogeneous cause (five-ministry synthesis §11).
- A holder of evaluation provenance, including a first-frozen-vs-current history that is never collapsed to "current" alone.

### 5.2 What a Case Package should not automatically be

- **Not** a container that injects Ground Truth into any upstream inference step — the existing isolation invariant must survive the Case Package's own existence, not merely survive despite it.
- **Not** a mechanism that promotes an engine-specific quirk to a source fact merely because it is convenient to store in one place — case-004's own Docling `maxNumCols` finding (the same value from a genuine anomaly and a pure segmentation artifact) is the clearest evidence for why this must be actively guarded against, not assumed away.
- **Not** a substitute for the raw artifact itself — a Case Package should reference, not embed, `derived/document-understanding/<case>/<engine>.raw.json`.
- **Not** a copy of the source PDF.
- **Not** merely a score container — `evidence/document-understanding/<case>-results.json` already exists for that purpose and should remain the compact evaluation-result artifact; the Case Package's own evaluation section (§14) references it, does not duplicate its content.
- **Not** a place where a special/non-ordinary structure's semantic taxonomy gets decided by inference — case-004's own anomaly research explicitly never assigned a confirmed semantic label to the embedded-matrix family it found, and a Case Package must preserve that same restraint (§16).

## 6. Conceptual layers

The originating task's own 8-item list (Source Identity/Acquisition Provenance, Source Observation, Context Requirement/Selection, Engine Observation, Normalization Trace, Semantic Interpretation, Evaluation, Ground Truth) is a **Case-Package-content taxonomy** — what sections a package holds. This is a genuinely different, complementary axis from **ADR-010's own 7-item taxonomy** (engine behavior, raw representation, generic normalization, engine-specific normalization, document-family/layout-specific interpretation, semantic interpretation, evaluation) — which classifies **where a given rule's validity boundary sits**, not what a data object contains. Conflating the two would be a mistake this design explicitly avoids: a single Case Package "Normalization Trace" entry, for instance, must itself be taggable with which ADR-010 rule-layer produced it (engine-specific vs. document-family-specific), since that is precisely the distinction case-002's `splitTrailingTriple` incident showed matters.

Reconciled content layers, each mapped to concrete case-001–005 evidence:

| Layer | Responsibility | Allowed inputs | Produced information | Provenance requirement | Raw preserved? | Unknown allowed? | Prohibited dependencies | Evidence |
|---|---|---|---|---|---|---|---|---|
| **1. Source Identity / Acquisition Provenance** | Stable reference to the locked binary and how it was obtained | Acquisition tooling output only | URL, SHA-256, acquisition method, WAF/challenge history | `source_stated` (from the lock/registry itself) | n/a (references, doesn't hold bytes) | Yes (e.g. case-001's own Producer/page-count `not_recorded`) | Must not depend on any later layer | `sources/source-lock.json`, case-002's WAF-then-browser-fetch history |
| **2. Source Observation** | Source-safe facts about the document's own structure, discoverable without running a compared engine | Direct visual/`pdfinfo` inspection only, per the same circularity-avoidance discipline already governing every selection protocol | Packaging model, hierarchy, printed-label conventions, unit-declaration scope, page-context relation for a *specific* field | `manually_observed` or `source_stated`, backed by evidence predating any engine run (ADR-011) | n/a | Yes, extensively (case-001's own multiple `not_recorded` fields) | Must not depend on Engine Observation, Semantic Interpretation, or Ground Truth | case-004's standalone-packaging finding; case-005's granular 目次 finding |
| **3. Context Requirement / Context Selection** | What context a given field actually needed to resolve, and whether that requirement was met for this specific row | Source Observation (for what context *exists*) + Engine Observation (for what an engine actually *used* or *lacked*) | A classification per field: page-local / neighbor-page (bounded) / table-metadata (unbounded-distance, once-only) | Mixed — the *requirement* is source-safe; the *acquisition result* (whether it was actually recovered by a given engine) is engine-derived | n/a | Yes — "requirement not yet characterized" is a valid state | Context *requirement* must not depend on Ground Truth; context *acquisition result* may depend on Engine Observation only | case-004's item-header-absent-from-page-2 finding vs. case-005's item-header-present-on-page-28 finding |
| **4. Engine Observation** | What a specific engine, at a specific version, actually produced from the raw source, before any normalization | Raw source + engine's own configuration | Raw text/lines/cells, per-engine metadata (grid dimensions, candidate counts) | `derived_from_repository_analysis`, tagged with engine identity/version | **Must be preserved unmodified** (already enforced today via `derived/.../*.raw.json`) | Yes (an engine may simply fail to produce a field) | Must never read Ground Truth; must never be adjusted post-hoc to fit an expected value | Docling's `doclingTableGridDimensions` field already in case-002's own Phase-1 profile |
| **5. Normalization Trace** | What deterministic rule transformed a given raw representation into what output, and why that rule's ADR-010 layer classification is what it is | Engine Observation only | Input representation, rule/operation identity (e.g. `closeCjkWrapSpaces`, `reconstructNumericToken`), output representation, ADR-010 layer tag, reversibility note | `derived_from_repository_analysis`, tagged with the specific rule's code/commit reference | Must preserve the pre-transformation input alongside the output (already true today: raw vs. normalized artifacts are separate files) | Not applicable (a normalization step either ran or did not) | Must never read Ground Truth; must never branch on case identity | CJK-spacing study's own layer-comparison table (4 candidate layers explicitly compared before choosing engine-specific normalization) |
| **6. Semantic Interpretation** | Candidate generation, hierarchy association, row-to-amount association, and the specific interpretation chosen, kept separate from whether that choice was correct | Normalization Trace output | Candidate set, chosen interpretation, ambiguity note | `derived_from_repository_analysis` | Candidate set must be preserved even when a single interpretation is chosen (already true today via `item_name_present_among_candidates`'s own diagnostic-vs-`result` split) | Yes — "no confident single interpretation" is itself a valid, informative outcome | Must never read Ground Truth | Five-ministry synthesis §11's own finding that collapsing this layer into "final value only" would erase the case-001/002/004 mechanism distinction entirely |
| **7. Evaluation** | Scoring the chosen semantic interpretation against Ground Truth | Semantic Interpretation output + Ground Truth (the **only** layer permitted to read it) | Per-check PASS/FAIL, score, first-frozen-vs-current history | `derived_from_repository_analysis`, tagged with evaluator version | The specific check definitions active at evaluation time must be identifiable (evaluator-overfit correction precedent) | No — every check must resolve to PASS or FAIL, though the *value being checked* may itself be `null`/unknown | Nothing may depend on this layer except a future Case Package's own history entry | case-002's own evaluator-overfit discovery and correction, preserved as two distinct historical evaluation events |
| **8. Ground Truth** | The frozen, source-visually-transcribed expected values | Direct visual source inspection only, per the existing selection-then-GT sequencing | `result` object (per-field expected values), raw-to-normalized mapping, delta-sign evidence | `manually_observed`, frozen before any engine run | n/a | No — a GT field is either transcribed or the row was not eligible; ambiguity is resolved by not selecting the row, not by a `null` GT value | **Must never be read by layers 1–6** | Every one of the five cases' own Ground Truth evidence documents |

## 7. Ground Truth isolation

**Same-package-embedded GT vs. external-reference GT, compared explicitly:**

| Dimension | Embedded in the same package object | External reference (separate file/artifact, package holds only a pointer) |
|---|---|---|
| Logical isolation | Weaker by default — a consumer reading "the Case Package" gets GT unless a field is explicitly excluded at read time | **Stronger by construction** — a consumer must take a separate, explicit step to dereference GT, matching the existing `ground-truth.json`-is-a-separate-file convention already used in all five cases |
| Accidental leakage risk | Higher — any future tool that naively serializes "the whole package" for an LLM prompt would include GT unless the tool itself is GT-aware | **Lower** — a tool that reads only "the package" structurally cannot see GT without a second, separately-authorized read |
| Reproducibility | Equivalent either way, since both are Git-tracked | Equivalent |
| Ergonomics | Slightly better for a human reading one file | Slightly worse (one more file to open) — but this cost is already paid today and has not caused friction across five cases |
| Auditability | Equivalent (both are committed, versioned) | Equivalent |
| Future automation | **Materially worse** — an automated Strategy Selection retrieval step would need to actively strip GT from an embedded structure every time, a repeated, error-prone task; a reference model makes "don't fetch this file" the default safe behavior | **Materially better** — the existing five-case convention (separate `ground-truth.json`) already demonstrates this works |

**v0 recommendation (design-level, not implemented)**: keep Ground Truth as a **separate, externally-referenced artifact**, exactly as the existing `ground-truth.json` convention already does. A Case Package's own `groundTruthRef` field (§20) should hold a stable reference (file path + freeze commit SHA) and nothing else — never a copy of `result`. This is not a new decision; it is a recommendation to **keep doing what already works**, made explicit as a Case Package design requirement so it cannot be silently relaxed later.

## 8. Source-safe vs. engine-derived observations

Directly reflecting case-004's anomaly research, which is the single strongest piece of evidence for why this boundary must be actively enforced, not merely documented:

- **Source-safe candidate fields**: source URL/SHA, page locator (`pdfPageIndex`/printed-label offset formula, itself sometimes non-trivial — case-004's `+9`-then-different offset within one file, case-005's own confirmed-at-three-points offset), packaging model, native hierarchy (組織/項/経費), visual unit declaration (and its scope — page-level vs. table-wide, itself a source-safe fact once actually visually confirmed), context relation for a specific field (*if and only if* established by direct visual inspection, per ADR-011), printed page label, native table/region shape *if a human directly confirmed it by rendering the page* (e.g. "this page visually shows an ordinary ledger row adjacent to a differently-shaped matrix region" — case-004's own §4.2 finding, itself source-safe because it was established by direct visual inspection before any engine ran).
- **Engine-derived candidate fields**: pdf.js's own line-ordering/reconstruction, the CJK-spacing artifact's *presence on a specific page* (only knowable by comparing raw pdf.js output against the source — the artifact's *general existence as a phenomenon* is now well-established research knowledge, but whether page N of case-006 exhibits it is engine-derived until independently visually confirmed), Docling's `maxNumCols`/spanning-cell counts, engine candidate sets, engine table segmentation shape.
- **The concrete case for why this must never collapse**: case-004's broad-sample Docling validation found the *identical* `maxNumCols` value produced by (a) a genuine source-side embedded matrix and (b) a purely Docling-side dense-remarks-text segmentation artifact on a genuinely ordinary page. If a Case Package's design allowed "this page has an unusual table shape" to be written once, as a single boolean or enum, without provenance, a future consumer (human or LLM) would have **no way to tell these two cases apart** — exactly the failure mode this program's own anomaly research exists to warn against.

**Proposed concept, not implemented**: an `observationOrigin` provenance class per field, directly generalizing the Phase-1 schema's own already-working `provenance` enum (`manually_observed` / `source_stated` / `derived_from_repository_analysis`) — this is not a new invention, it is a recognition that the existing Phase-1 field already does most of this job, and v0's job is to apply it consistently to the new categories of observation (context requirements, anomaly-channel signals, normalization traces) that Phase-1 never had to classify.

## 9. Raw preservation

Already-correct existing convention, restated as a Case Package design requirement rather than left implicit: a Case Package must **never embed** the raw source PDF, raw engine extraction output, or normalized engine representation. It holds **stable identifiers, content hashes, and artifact references** — exactly the pattern `sources/source-lock.json` (SHA-256 + acquisition metadata, not the PDF bytes) and `derived/document-understanding/<case>/<engine>.raw.json` (git-ignored, regenerable, referenced by path from the compact `evidence/.../results.json`) already establish. "Raw is preserved" and "raw is embedded in the Case Package JSON" are explicitly **not** the same requirement — the first is already satisfied by this repository's existing file layout; the second is explicitly rejected as a design goal.

## 10. Unknown/absent/ambiguous semantics

Formalizing, not inventing, the discipline already practiced across five cases and stated in `protocol/RESEARCH_PROTOCOL.md`:

| State | Meaning | Example from case-001–005 |
|---|---|---|
| `unknown` / not observed | No attempt has been made to establish this fact yet | case-001's own `pageCount: "not_recorded"` |
| Known absent | Actively confirmed the fact does not exist here | case-005's "no unit label found on the target page itself" (confirmed by inspection, then resolved to a table-level scope from a different page — a case of "known absent *at this specific location*," not "unknown") |
| Not applicable | The field's own precondition does not hold for this case | A `doclingColumnFusionArtifact` field would be "not applicable" for a case where Docling was never run |
| Observed but intentionally not interpreted | The fact is seen, recorded, but its meaning is deliberately left open | case-004's own embedded-matrix shape — visually confirmed to exist, never assigned a semantic taxonomy label |
| Ambiguous | Multiple plausible readings exist and were not resolved by further evidence | The text/grammar anomaly survey's own explicitly-marked ideographic-comma-adjacent spacing test case |
| Unavailable because context was not acquired | The context mechanism needed to resolve this field was never invoked (distinct from "known absent," which means the mechanism *was* invoked and found nothing) | A hypothetical future engine limited to single-page scope, asked about a neighbor-page fact it was never given access to |

**Absolute rule, restated as a design requirement**: `0` must never represent any of the above states. Case-004's own `20260926_2111_Case004_Ground_Truth_Evidence.md` and every prior Ground Truth evidence document already demonstrate this in practice (e.g. a genuinely zero-valued amount, confirmed by visual transcription, is recorded as the integer `0`, distinct from a field that was never checked). A Case Package schema must make these six states **structurally distinguishable**, not collapsed into a single `null`/`0`/empty-string convention.

## 11. Context model

Five-ministry synthesis §12's own three-mechanism finding, restated as a Case Package design requirement:

- **Page-local context**: recoverable from the target page alone.
- **Neighbor-page structural context**: requires a *bounded* lookback (confirmed, across 11 sampled MEXT boundaries, never more than one page).
- **Table/document metadata context**: requires locating a *once-only*, table-wide declaration whose distance from the target is not a fixed page-count at all.

**A single `contextPages: N` field cannot represent this** — it would either overfit to the bounded neighbor-page case (implying a fixed-distance model that case-004's own unit-recovery finding directly contradicts) or force an arbitrarily large number to cover the table-metadata case, defeating the purpose of a bounded-context model entirely.

**What should be stored — proposed as multiple, not one**: (a) the **context requirement** for a given field (a source-safe classification: page-local / neighbor-page-bounded / table-metadata-once, established once a case's own row is understood well enough to say so); (b) the **context acquisition result** for a given engine run (did this specific engine, with its actual single-page-scope architecture, successfully recover this field, or not — engine-derived, tied to a specific run); (c) **provenance** for both (a) and (b) separately, since (a) is source-safe and (b) is engine-derived, and conflating them would repeat exactly the mistake §8 warns against.

## 12. Normalization trace

Reflecting the CJK-spacing and numeric-token-reversal research: a Normalization Trace entry needs, at minimum, an **input representation** (the pre-transformation raw fragment), an **operation/rule identity** (e.g. `closeCjkWrapSpaces`, referenced by function name and the commit that introduced or last modified it — not embedded source code), an **output representation**, a **transformation provenance** (which ADR-010 layer this rule belongs to — engine-specific vs. document-family-specific, the exact distinction case-002's `splitTrailingTriple` incident showed matters), a **lossiness/reversibility note** (e.g. "closing a CJK-adjacent space is not reversible; this was accepted only after an exhaustive corpus search found zero counter-examples," per the boundary-safety experiment), and an **engine-applicability scope** (pdfjs-dist-specific vs. Docling-specific vs. shared). Code/version/commit references are sufficient; the rule's own implementation need not be embedded.

## 13. Semantic interpretation trace

The five-ministry synthesis's own §11 is the direct evidence for why this layer cannot collapse to "final value only": five cases produce the *same* outcome (`item_name_exact_match` FAIL) via at least three *different* mechanisms (pure ambiguity; ambiguity plus genuine extraction failure; total context absence). A Case Package that recorded only `itemName: null` for all five cases would make this heterogeneity **invisible** — exactly the failure this design must prevent. A Semantic Interpretation entry should therefore distinguish, at minimum: the **candidate set** generated (even when empty or singular), the **hierarchy association** attempted, the **row-to-amount association** attempted, the **page/context association** used, any **ambiguity** encountered and how it was resolved (or left unresolved), and the **chosen interpretation** ultimately passed to evaluation. This is not a new invention — it is already partially implemented today via `evaluate.mjs`'s own `item_name_present_among_candidates` diagnostic check, which exists precisely to prevent this collapse; the proposal here is to recognize that pattern as a first-class Case Package concept, not merely an evaluator side-check.

## 14. Evaluation / history model

Evaluation is the **only** layer permitted a Ground Truth reference (§7). A Case Package's evaluation section should record: evaluator identity/version (a currently-missing formal field, per the original architecture report's own §11 gap list — `evaluatorVersion`, not implemented there either), a reference to the Ground Truth freeze commit used, a reference to the semantic-interpretation output evaluated, the complete check list with PASS/FAIL, the resulting score, and evidence/provenance for each check.

**History/versioning concept, not implemented**: evaluation results must be modeled as an **append-only sequence of historical events**, never a single mutable "current score" field with no memory of what came before. This is not a new requirement — it is a direct formalization of what case-002 and case-003 already required in practice (their own first-frozen results, `379043d` and `aa57caf` respectively, remain permanently recoverable via `git show`, distinct from their current, post-normalization-improvement scores). A future Case Package's evaluation section should record each such event with its own commit reference and an explicit `supersededBy`/`supersedes` relationship (mirroring the Phase-1 `research-history.jsonl`'s own `relatedEvents` field, e.g. `{"eventId": ..., "relation": "resolves"}`), never overwriting an earlier event's own recorded numbers.

## 15. Selection/freeze provenance

The case-004/005 chronology (source survey → protocol freeze → deterministic selection → selection freeze → GT freeze → first benchmark) is now mature and consistent enough to reference structurally, without duplicating its own content into the Case Package. A Case Package should hold: the selection protocol's own artifact path + freeze commit SHA (not its full text); the selection record's own path + freeze commit SHA + the row's own locator (page index, organization/item/expense identity — all already source-safe per §8); a **prior-exposure disclosure** field (directly reflecting case-005's own protocol, which explicitly disclosed and then explained why an already-glimpsed row's identity did not shape the eligibility criteria); and the chronological ordering itself (protocol commit precedes selection commit precedes GT commit precedes first-benchmark commit), verifiable structurally rather than only by narrative claim.

## 16. Special/non-ordinary structure

Directly reflecting case-004's own anomaly research and its own explicit restraint: a Case Package must be able to record that a page/region has an **observed, non-ordinary shape** (e.g. "this page contains an ordinary ledger row adjacent to a visually distinct, differently-shaped region") as a **source observation** (§8), entirely separate from any **engine anomaly signal** (a specific engine's own `maxNumCols`/segmentation output on that same page — a different layer, per §6's own Context Requirement/Engine Observation split), and entirely separate again from any **semantic taxonomy label**. A field like `specialStructure: true` is explicitly **not recommended as a v0 primitive** — it collapses "a human saw something visually unusual," "an engine produced an unusual signal," and "we have decided what this structure semantically is" into one boolean, which is precisely the conflation case-004's own research spent four separate tasks carefully avoiding. The v0 design should instead permit an **open-ended, unnamed-taxonomy shape description** (e.g. a free-text or lightly-structured note describing what was visually observed, tagged with `observationOrigin: manually_observed`) that can later be classified, once enough cases exist to support a real taxonomy, without ever having forced a premature label at collection time.

## 17. MOF reverse-linkage readiness

Not implemented, and not required for v0 — but the design should not accidentally discard the identifiers a future linkage experiment would need. Every one of the five cases' own frozen Ground Truth already records fiscal year, ministry/organization, item code/name, request number, expense code/name, a full amount triple, and a page locator — all of which naturally live in the Source Identity (§6, layer 1), Source Observation (layer 2), and Ground Truth (layer 8) sections already designed above; no new field is required to preserve them. The only new concept proposed here is a **future extension point**, not a current requirement: an `externalLinkage` section, left entirely empty/undefined in v0, reserved for a later, separately-scoped linkage experiment to populate — explicitly not designed further here, per the originating task's own instruction.

## 18. Strategy Selection boundary

The original architecture report's own boundary — Case Package holds evidence/provenance/context/observations; Strategy Selection consumes that information to choose an extraction/context/interpretation strategy — remains sound and is not revised here. Three dependency rules, directly motivated by five cases' worth of evidence:

1. **Source-safe features (§8) are legitimate Strategy Selection inputs** for a genuinely unseen document, since they exist before any engine runs.
2. **Engine-derived observations may be used as Strategy Selection inputs only with their origin preserved** — e.g. a future selector could legitimately use "Docling's `maxNumCols` was found unusually high on a structurally similar prior case" as a *hint*, but must never treat that as equivalent to a source-safe fact about the *new* document, since it has not yet run Docling on the new document at all (this is the same circularity the existing selection protocols' own "avoid running a compared engine before selection" rule already guards against, one layer higher up).
3. **Ground Truth and evaluation results must never feed production Strategy Selection** for the document currently being processed — they may only be used, under the already-established Leave-One-Case-Out protocol (§9 of the original architecture report), to *evaluate* a selector's own historical performance on already-completed cases, per ADR-012's own isolation-disclosure requirement.

## 19. Dependency matrix

| Consumer ↓ / Provider → | Source Identity | Source Obs. | Context Req. | Engine Obs. | Norm. Trace | Semantic Interp. | Ground Truth | Evaluation |
|---|---|---|---|---|---|---|---|---|
| **Source Identity** | — | prohibited | prohibited | prohibited | prohibited | prohibited | prohibited | prohibited |
| **Source Observation** | allowed | — | prohibited | prohibited | prohibited | prohibited | prohibited | prohibited |
| **Context Requirement** | allowed | allowed | — | conditional¹ | prohibited | prohibited | prohibited | prohibited |
| **Engine Observation** | allowed | prohibited² | prohibited | — | prohibited | prohibited | **prohibited (GT leakage risk)** | prohibited |
| **Normalization Trace** | allowed | prohibited | prohibited | allowed | — | prohibited | **prohibited (GT leakage risk)** | prohibited |
| **Semantic Interpretation** | allowed | conditional³ | allowed | allowed | allowed | — | **prohibited (GT leakage risk)** | prohibited |
| **Ground Truth** | allowed | prohibited⁴ | prohibited | prohibited | prohibited | prohibited | — | prohibited |
| **Evaluation** | allowed | allowed | allowed | allowed | allowed | allowed | **allowed (sole consumer)** | — |
| **Strategy Selection (external)** | allowed | allowed | allowed⁵ | conditional⁶ | prohibited | prohibited | **prohibited (GT leakage risk)** | conditional⁷ |

Notes: ¹ the *acquisition result* half of Context Requirement (§11) may read Engine Observation for the specific run being described, but the *requirement* half must not. ² Source Observation must never be backfilled or "corrected" using engine output, even to fill an `unknown` — this is the ADR-011 boundary itself. ³ Semantic Interpretation may use Source Observation (e.g. known hierarchy structure) as a hint but must not treat it as a substitute for its own candidate generation. ⁴ Ground Truth transcription must never be adjusted using Source Observation collected after the fact, only using direct source re-inspection under the existing selection-then-GT sequencing. ⁵ Strategy Selection may use a Context Requirement classification from a *prior, already-completed* case as a hint for a new document, never the new document's own not-yet-established requirement. ⁶ conditional exactly as §18's rule 2 states — allowed only with origin preserved and never for the document currently being selected for. ⁷ allowed only under the Leave-One-Case-Out historical-evaluation protocol, never for the document currently being processed.

**GT leakage is visually concentrated in one column** (the Ground Truth row) and one direction (only Evaluation, and historical-only Strategy Selection under LOCO, may read it) — by design, so a future schema reviewer can check this matrix visually rather than re-deriving the rule from prose each time.

## 20. Conceptual object model

Building on, and renaming/restructuring where five cases' evidence justifies it, the original architecture report's own illustrative sketch:

```text
CasePackage
  identity              — caseId, ministry/org, fiscal year, document stage (purpose = identity, ownership = fixed at case creation, immutable)
  sourceRef             — sourceId, SHA-256, acquisition method/history reference (ownership = source-acquisition step, immutable once locked)
  sourceObservations[]  — packaging model, hierarchy, unit-declaration scope, printed-label conventions, each tagged observationOrigin (ownership = source-survey/selection-protocol authors, append-only, pre-GT)
  contextRequirements[] — per-field classification (page-local/neighbor-bounded/table-metadata), tagged observationOrigin (ownership = context-diagnostic tasks when they exist, else "not yet characterized"; append-only)
  selectionRef          — protocol path+commit, record path+commit, row locator, prior-exposure disclosure (ownership = selection tasks, immutable once frozen)
  groundTruthRef         — path + freeze commit SHA only, never embedded result values (ownership = GT-freeze task, immutable once frozen)
  engineRuns[]          — one per (engine, engineVersion, runDate): raw artifact reference, engine-derived observations, tagged observationOrigin (ownership = benchmark-run tasks, append-only across reruns, each run its own immutable entry)
  normalizationTraces[] — one per applied rule per engine run: input/output representation refs, rule identity, ADR-010 layer tag (ownership = benchmark-run tasks, tied 1:1 to the engineRun that produced it)
  interpretations[]     — one per engine run: candidate set, chosen interpretation, ambiguity note (ownership = benchmark-run tasks, tied 1:1 to the engineRun that produced it)
  evaluations[]         — one per (engineRun, evaluatorVersion): checks, score, GT reference, supersedes/supersededBy (ownership = evaluation tasks, append-only, each historical event immutable)
  specialObservations[] — open-ended, unnamed-taxonomy shape descriptions, tagged observationOrigin, explicitly not a boolean (ownership = anomaly/diagnostic tasks when they exist; append-only)
  history[]             — the existing Phase-1 research-history.jsonl content, generalized: kind/eventId/status/layers/date/commit/summary/evidence/relatedEvents (ownership = every task that touches this case; strictly append-only)
  externalLinkage       — reserved, empty in v0 (future MOF/RS extension point only)
```

Compared to the architecture report's own sketch: `sourceObservations`/`contextRequirements`/`normalizationTraces`/`interpretations`/`specialObservations` are new or split out from the original's single `sourceSafeProfile`/`engineDerivedProfile` pair, directly because five cases' worth of evidence (context mechanisms, normalization-layer classification, semantic-interpretation heterogeneity, anomaly observations) showed that pair was too coarse to prevent exactly the kind of collapse §13/§16 warn against. `groundTruthRef` replaces any notion of an embedded `groundTruth` object, per §7's own recommendation. `history[]` is not new — it is the existing, already-working Phase-1 `research-history.jsonl` format, generalized to also carry `evaluations[]`-style supersession relationships.

## 21. Lifecycle / immutability

Reconstructing the case-004/005 chronology as an explicit lifecycle, without inventing a stage that evidence does not support:

1. Source acquired and locked → `sourceRef` written, immutable from this point.
2. Selection protocol frozen → `selectionRef.protocol` written, immutable.
3. Row selected → `selectionRef.record` and the row locator written, immutable; `sourceObservations` accumulated up to this point become immutable as of this commit (later tasks may *add* new, separately-dated `sourceObservations` entries — e.g. case-004's own later context diagnostics added genuinely new source observations about organization `020` — but must never edit an already-committed entry).
4. GT frozen → `groundTruthRef` written, immutable.
5. First engine run → one `engineRuns[]` entry, one `normalizationTraces[]` set, one `interpretations[]` entry, one `evaluations[]` entry — **all immutable as a first-frozen historical set**, per §14's own requirement.
6. Later adaptation (e.g. a normalization improvement) → a **new** `evaluations[]` entry referencing the changed normalizer/evaluator version, explicitly marked as superseding the prior one via `relatedEvents`, never overwriting it.
7. Additional engine run (e.g. this program's own reproducibility-check convention) → a new `engineRuns[]` entry if the run is semantically distinct, or a note confirming byte-identical reproduction of an existing entry if not — never silently discarded.
8. Architecture reinterpretation (e.g. this very synthesis/design pair) → new `history[]` entries referencing the relevant commits, never editing an earlier stage's own already-frozen sections.

**Immutability strength differs genuinely by section**: `sourceRef`, `selectionRef`, and `groundTruthRef` are **freeze-point immutable** (a new value requires an explicit, reviewable re-freeze, exactly like `sources/source-lock.json`'s own re-lock discipline) — these are the sections where silent mutation would be a genuine research-integrity violation. `engineRuns[]`, `evaluations[]`, and `history[]` are **append-only, not edit-in-place** — new entries are added freely (this is expected, healthy research activity), but no existing entry's own recorded content is ever altered after the fact.

## 22. Minimal v0

**Required for v0** (needed for the reproducibility/comparability/GT-isolation that all five existing cases already depend on): `identity`, `sourceRef`, `selectionRef`, `groundTruthRef` (reference only), `engineRuns[]` + `evaluations[]` with first-frozen-vs-current history, and the existing `history[]`/research-history concept generalized from Phase-1.

**Useful but optional** (currently needed by only a subset of cases): `contextRequirements[]` (only case-004 has the diagnostic depth to populate this meaningfully today); `normalizationTraces[]` at the granularity described in §12 (currently only the CJK-spacing/numeric-token rules would populate it; most cases have no other traceable rule yet); `specialObservations[]` (only case-004 has anomaly-research content to populate it).

**Deferred extension** (explicitly out of scope for v0): `externalLinkage` (§17); any production Strategy Selection consumption of this schema (§18, design only, no implementation); any formal anomaly-taxonomy enum (§16, deliberately left open-ended).

## 23. Existing repository mapping

| Case Package concept | Existing repository artifact | Canonical owner |
|---|---|---|
| `sourceRef` | `sources/source-lock.json` entry + `sources/source-registry.csv` row | Source-acquisition tooling (unchanged) |
| `selectionRef` | `fixtures/document-understanding/<case>/YYYYMMDD_HHMM_Case*_Selection_Protocol.md` + `..._Selection_Record.md` | Selection-protocol/selection tasks (unchanged) |
| `groundTruthRef` | `fixtures/document-understanding/<case>/ground-truth.json` + its own evidence document | GT-freeze tasks (unchanged) |
| `engineRuns[]` (raw) | `derived/document-understanding/<case>/<engine>.raw.json` (git-ignored) | Benchmark runner (unchanged) |
| `normalizationTraces[]` | implicit in `<engine>.normalized.json` (git-ignored) + the CJK-spacing/numeric-token rule implementations themselves | Benchmark runner + normalizer code (unchanged) |
| `evaluations[]` | `derived/.../<engine>.evaluation.json` (git-ignored) + `evidence/document-understanding/<case>-results.json` (committed, compact) + `reports/document-understanding/<case>-evaluation.md` (committed, current) | Evaluator (unchanged) |
| `history[]` | `fixtures/document-understanding/<case>/research-history.jsonl` (exists for case-001/002 only) + every timestamped narrative report | Every task that touches the case |
| `sourceObservations[]`/`contextRequirements[]`/`specialObservations[]` | Currently only prose, scattered across selection protocols, GT evidence, and (for case-004) the four anomaly/context reports | **Does not yet exist as structured data** — this is v0's actual new contribution |

**Canonical ownership conclusion**: a Case Package would **not** duplicate the git-ignored `derived/` artifacts (it references them by path, which is already how `evidence/.../*.json` behaves today) and would **not** duplicate the committed narrative reports (it references them by path in `history[]`'s own `evidence` field, exactly as Phase-1's `research-history.jsonl` already does). The only genuinely new, structured (not prose-only) content a Case Package would introduce is `sourceObservations[]`, `contextRequirements[]`, and `specialObservations[]` — everything else is a structured *index* over already-existing, already-canonical files, not a second copy of their content.

## 24. Five-case migration thought experiment (not performed)

| Case | Straightforward | Missing source evidence | Ambiguous | Requires optional extension |
|---|---|---|---|---|
| case-001 | `groundTruthRef`, basic `identity` | `sourceRef`'s own page count/Producer/encryption (`not_recorded`, must stay `not_recorded`, never guessed) | Whether its own selection was ever "protocol-frozen" in the current sense (it predates that convention — would need an explicit `selectionRef: not_established` state, not a fabricated protocol) | none needed beyond the above |
| case-002 | `sourceRef`, `selectionRef`, `groundTruthRef`, `engineRuns[]`/`evaluations[]` with genuine first-frozen-vs-current history (already exists in Phase-1 form) | none significant | The annotation-column-placement feature's own A/B boundary (ADR-011's own worked example) — already correctly resolved as engine-derived, a template for future ambiguous cases | none |
| case-003 | `sourceRef`, `selectionRef`, `groundTruthRef` | `sourceObservations[]`/`contextRequirements[]` (never populated — no context diagnostic was run for MIC) | none new | `normalizationTraces[]` would need the CJK-spacing rule's own case-003-specific effect recorded, straightforward but not yet done |
| case-004 | Every layer — the richest existing case by far (context diagnostics, four anomaly channels, full first-frozen-vs-current history) | none | `specialObservations[]`'s own eventual taxonomy (deliberately left open per §16) | `contextRequirements[]` and `specialObservations[]` would need real content, not merely placeholders — the most extension-dependent of the five |
| case-005 | `sourceRef`, `selectionRef`, `groundTruthRef`, `engineRuns[]`/`evaluations[]` (first-frozen = current, no adaptation yet) | `contextRequirements[]`/`specialObservations[]` (no context diagnostic or anomaly survey has been run for MLIT) | none | none required for v0-minimal; both optional sections would start empty, honestly, not fabricated |

**No case's own `not_established`/absent fields are proposed to be filled by this thought experiment** — this table is itself evidence that the "required for v0" set (§22) is achievable losslessly for all five cases today, while the "useful but optional" set would legitimately start empty for two to four of them, which is the correct, honest outcome, not a design flaw.

## 25. Acceptance criteria for a future schema-prototype task

- GT dependency prohibition is structurally explicit (§19's own matrix, not merely prose).
- Raw/normalized separation is explicit and raw is never embedded (§9).
- Source/engine observation origin is explicit per field, generalizing the already-working Phase-1 `provenance` enum (§8).
- The six unknown/absent/ambiguous states (§10) are each structurally distinguishable, not collapsed into `null`/`0`.
- At least the three context types (§11) are each representable, not flattened into one page-count field.
- First-frozen history is preserved and referenceable independently of current state (§14, §21).
- All five existing cases can be represented losslessly under the "required for v0" fields, with every currently-`not_established` fact remaining `not_established` (§24) — no schema field may force an invented value.
- No mandatory field requires data that does not already exist for at least case-002 through case-005 (case-001's own genuine gaps must remain representable as gaps, not disqualify the whole schema).

## 26. Open questions (deliberately unresolved)

- **GT same-package vs. external-reference**: resolved as a *recommendation* in §7 (external reference), but whether a future schema should physically enforce this (e.g. via tooling that refuses to co-locate GT values inside a Case Package file) or rely on convention alone is not decided — evidence needed: whether an actual accidental-leakage incident ever occurs under the convention-only approach; not blocking v0's own concept design, since the recommendation itself is actionable without that tooling existing yet.
- **Source visual region's canonical representation**: how to represent "this page visually shows an embedded matrix adjacent to an ordinary row" in a way more structured than free text, without prematurely fixing a taxonomy — evidence needed: more anomaly-channel cases across more ministries before a stable shape vocabulary is justified; **blocking** a full `specialObservations[]` schema, not blocking v0's minimal set.
- **bbox/vector geometry source-safe acquisition**: case-004's own Docling survey confirmed `bbox` is *available* on Docling's own cell objects but never exploited into a feature; whether bounding-box data can ever be source-safe (i.e., independently re-derivable by a human without running Docling) or is inherently engine-derived is unresolved — evidence needed: a dedicated comparison of Docling's own bbox output against manual pixel-coordinate measurement; not blocking v0, since no v0-required field depends on it.
- **Context acquisition policy**: whether a future pipeline should *always* attempt the neighbor-page lookback (§11) or only when a page-local attempt first fails is a Strategy Selection design question, not a Case Package one — explicitly deferred to whichever future task formalizes Strategy Selection, not resolved here.
- **Semantic candidate representation**: how rich a `interpretations[].candidateSet` should be (a flat list, as `item_name_present_among_candidates` already produces, vs. a richer structure capturing why each candidate was rejected) is unresolved — evidence needed: whether a flat list proves insufficient once a real Strategy Selection experiment tries to consume it; not blocking v0's own minimal representation.
- **Package granularity** (one selected row vs. document-level shared metadata, e.g. a document's own packaging model or 目次 granularity, which is a property of the *source*, not the *row*): this design implicitly assumes one Case Package per selected row, with document-level facts (packaging, Producer, page count) living in `sourceRef`/`sourceObservations` and therefore naturally shared if a future document-level index were built — but whether multiple rows from the *same* document should ever share one Case Package, or always get separate packages with duplicated `sourceRef` content, is not decided; evidence needed: whether case-006 or beyond ever selects a second row from an already-used source; not blocking v0, since every case to date has used a distinct source.

None of these open questions blocks the v0 concept design itself; each is recorded as a reason a future schema-prototype task should not attempt to resolve every field's exact shape without first gathering the evidence noted.

## 27. Recommended next step

Per this task's own explicit stop condition: this concept design should be **reviewed** (by the requester, in a separate turn/session) before any schema-prototype task begins. If reviewed and found sound, the natural next step would be a schema-prototype task scoped narrowly to the "required for v0" fields (§22) against case-002 through case-005 only (case-001's genuine gaps make it a useful stress test for the `not_established` discipline, but not a required first target). **Not executed in this task.**

---

**This task produced only a Case Package v0 concept-design candidate. No schema, migration, production code, benchmark change, Ground Truth change, source inspection, or new experiment was performed.**
