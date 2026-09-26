# Case-Based Document Understanding and LLM Strategy Selection Research Architecture

Status: **design document only. No implementation in this task.**

Date: 2026-09-26 (Asia/Tokyo)

Basis: `case-001` (digital-r6-request-table-01), `case-002` (meti-fy2024-general-account-request), the evaluator-overfit correction at `519ce28`, and the existing `scripts/pdf-extraction` / `scripts/document-understanding` architecture, all as committed on `research/case-002-meti-preregistration`.

## 1. Research question

Two data points do not justify a grand unified theory, but they are enough to show that the *implicit* question this benchmark has been answering — "which PDF engine best extracts this government PDF?" — is not the question that actually matters for this repository's stated goal (reproducible research across many Japanese government budget documents). The evidence supports reframing it as:

> **Primary:** For a given family of document layouts, which combination of extraction engine, deterministic normalization, and interpretation rules reliably recovers structured budget facts — and can that combination's applicability to a *new, unseen* document be predicted from the document's own observable properties, before Ground Truth exists for it?

> **Secondary (only meaningful once the primary has a real corpus behind it):** Can an LLM, given a library of prior reproducible "Case Packages," select or rank a strategy for a new document more effectively than a fixed default strategy or than undirected trial-and-error — without ever seeing the new document's Ground Truth?

This deliberately separates four capabilities that case-001/case-002 have already shown are *not* the same thing (see §2):

1. **Extraction capability** — can an engine get the glyphs/coordinates/cells out at all? (`scripts/pdf-extraction`, plus each adapter's raw-artifact stage.)
2. **Document Understanding capability** — given correct extraction, can a normalizer recover structural facts (which amount belongs to which row, sign, hierarchy)? (`normalize.mjs` / `normalize-docling.mjs`.)
3. **Document/layout-family adaptation** — does a rule that worked for one document's layout generalize to a structurally different one, or does it need a family-specific variant?
4. **Strategy selection** — given many prior cases, can the *right* combination of (1)–(3) be chosen for a new, unseen document before running anything expensive?

Case-001 answered questions about (1) and (2) for one layout. Case-002 revealed that (3) is a real, separate axis — the same normalizer code produced a *qualitatively different failure mode* on a structurally different page, not just a lower score. (4) has not been investigated at all yet; this document is about designing how it eventually could be, not building it now.

## 2. Evidence from case-001 / case-002

Concretely, mapped onto the four capabilities above:

| Observation | Layer it actually belongs to | Why it matters for this architecture |
|---|---|---|
| pdf.js/PyMuPDF/Docling all extracted case-001's page correctly at the raw stage | Extraction | Extraction capability was never the bottleneck in either case — worth noting so effort isn't wasted "improving extraction" when the failures are elsewhere |
| Docling's table-cell separation resolved case-001's two-column conflation | Document Understanding (engine-specific) | A genuine per-engine capability, not automatically portable |
| Docling's TableFormer produced a *differently shaped* (coarser, misaligned) grid on case-002's page, merging rows and confidently picking a wrong one | Document/layout-family adaptation | The **same engine, same code, same version** produced a different *kind* of failure on a different layout — this is exactly the "not one universal pipeline" evidence. It is not a bug to patch; it is evidence that Docling's table-structure output is layout-dependent in ways this repository has not yet characterized |
| `common.mjs`'s `splitTrailingTriple` requires the amount triple to be the literal end of a reconstructed line; case-002's annotation column breaks that because it sits on the *same* line as the triple (case-001's equivalent annotation only ever wrapped onto continuation lines) | Generic normalization vs. document-family-specific normalization | A single regex assumption, valid for one layout, silently invalid for another — the central evidence that "generalize into `common.mjs`" and "leave it engine/case-specific" are both too coarse a binary |
| `common.mjs` lacks a CJK-wrap-space-closing step that `normalize-docling.mjs` has | Engine-specific normalization gap, newly exposed by a second case | Shows that even *within* "generic" normalization, per-engine artifacts (pdfjs-dist's letter-spacing insertion) need engine-specific handling — not because the document differs, but because the *engine* differs |
| Page-level unit label was present on case-002's target page (all 3 engines recovered `"千円"`) but absent on case-001's | Document/layout-family characteristic, correctly *not* a selection criterion | Confirms unit-recovery is a page-context property, not a fundamental capability gap — exactly the kind of fact a Document Profile should record |
| `delta_glyph_observed_and_associated` hardcoded an assumption from case-001's specific delta sign | Evaluator methodology (not extraction, not normalization, not Ground Truth contamination) | Demonstrates that even the *evaluation layer* can silently encode single-fixture assumptions — the same "don't universalize from N=1" lesson applies to benchmark code, not just parsers |
| METI PDF acquisition required a browser-capable tool (AWS WAF); Digital Agency PDFs did not | Source acquisition, a precondition to everything else | A property of the *source*, not the document content — belongs in provenance metadata, not a Document Profile feature |

The throughline: **every one of case-002's surprises was a genuine, distinct finding at a different layer**, not a single generic "case-002 is harder." A Case Package framework is valuable precisely because it forces each finding to be attributed to the correct layer instead of collapsing into an undifferentiated score.

## 3. Proposed architecture

### 3.1 Layer taxonomy (extending, not replacing, the current 6-layer pipeline)

The existing pipeline documented in `scripts/document-understanding/README.md` is:

```text
1. source acquisition
2. PDF glyph/text extraction
3. layout/document understanding
4. normalization
5. semantic interpretation
6. evaluation
```

This is a *processing* pipeline. It does not currently distinguish *where a rule's validity boundary is* — which is the actual question case-002 raised. Proposed refinement, as a cross-cutting classification applied to any rule/behavior, not a replacement pipeline:

1. **Engine behavior** — an artifact of the extraction/DU engine itself (e.g. Docling's cell-reversal ordering, pdfjs-dist's letter-spacing). Belongs in that engine's adapter or its dedicated normalizer, never in shared code.
2. **Raw extraction representation** — the engine's untouched output. Never modified by any later layer; always preserved (already enforced today).
3. **Generic normalization** — a rule that is true of *this document corpus's conventions* regardless of engine or ministry (e.g. "△ means decrease" — a national government accounting convention, not a layout artifact). Belongs in shared code (`common.mjs`, or an equivalent shared module for structured engines).
4. **Engine-specific normalization** — a rule that compensates for a specific engine's *known, general* behavior (e.g. `closeCjkWrapSpaces`, `reconstructNumericToken`'s comma-group reversal). Belongs in that engine's normalizer, applied unconditionally whenever that engine is used, regardless of document.
5. **Document-family/layout-specific interpretation** — a rule that is true for a *class* of documents sharing a template/layout convention (e.g. "amount triple is always at the literal end of a reconstructed line" — true for one ministry's template, evidently not universal). This is the layer that currently does not exist as a distinct concept in the codebase; `splitTrailingTriple` is implicitly layer-3-scoped code actually encoding a layer-5 assumption. **This is the architectural gap case-002 exposed.**
6. **Semantic interpretation** — mapping structural facts to domain meaning (item/expense hierarchy, budget-lifecycle stage) — already governed by `protocol/RESEARCH_PROTOCOL.md`'s invariants (e.g. `request != enacted_budget != settlement`).
7. **Evaluation** — scoring against Ground Truth. Must itself be checked against overfitting to N=1, as §2's last row demonstrates.

The key design decision: **a rule is not "generalized into `common.mjs`" or "kept ministry-specific" as a binary choice.** It is classified into one of layers 1/3/4/5/6/7 above, and layer 5 (document-family/layout) is a **new, first-class extension point** that does not exist yet, sitting between layer 4 (engine-specific) and layer 6 (semantic).

### 3.2 Component boundaries

```text
Unknown Document
    ↓
Source Acquisition            (existing: scripts/source-acquisition/)
    ↓
Document Profile              (NEW — §5)
    ↓
Case Package Retrieval        (NEW — §7, not built now)
    ↓
Strategy Selection            (NEW — §6/§7, not built now)
    ↓
Deterministic Analysis Pipeline (existing extraction/normalization, extended with layer-5 adapters)
    ↓
Validation                    (existing arithmetic/consistency checks, e.g. case-002 GT evidence's fy2024Request-previousBudget==delta check)
    ↓
Evaluation                    (existing evaluate.mjs, generalized per §8)
    ↓
New Case Package              (NEW — closes the loop)
```

Everything left of "Deterministic Analysis Pipeline" is genuinely new design surface. Everything from "Deterministic Analysis Pipeline" onward already exists in working form for case-001/case-002 and is *reused*, not replaced.

## 4. Case Package

A Case Package is the unit of reproducible research this repository already produces informally (case-001 and case-002's collection of fixture + evidence + report files) — this section formalizes what's already there plus what's missing.

### 4.1 What already exists, mapped to Case Package concepts

| Case Package concept | Existing artifact (case-001/002) |
|---|---|
| Source identity | `sources/source-lock.json` entry (SHA-256, acquisition method, timestamps) |
| Document Profile | **Does not exist as a distinct artifact.** Currently scattered across `fixtures/.../README.md` prose and the selection protocol/record |
| Methods attempted | `scripts/document-understanding/adapters/*` (shared across cases, not case-scoped) |
| Exact versions/configs | Recorded per-engine in each `*.raw.json`'s `engineVersion` field, and in each adapter's `package.json`/`requirements.txt` |
| Raw output | `derived/document-understanding/<case>/<engine>.raw.json` (git-ignored, regenerable) |
| Normalized output | `derived/document-understanding/<case>/<engine>.normalized.json` (git-ignored, regenerable) |
| Ground Truth | `fixtures/document-understanding/<case>/ground-truth.json` (committed, frozen) |
| Evaluation | `derived/.../<engine>.evaluation.json` (git-ignored) + `evidence/document-understanding/<case>-results.json` (committed, compact) |
| Research history / hypotheses / interventions | **Does not exist as structured data.** Currently only in prose reports (`reports/document-understanding/*.md`) and `state/CHANGELOG.md` |
| What failed / what generalized | **Does not exist as structured data** — currently requires reading the narrative reports in full |

### 4.2 Proposed additions (schema sketch, illustrative only — not implemented)

Two new files per case, added *alongside* the existing fixture files, not replacing them:

**`fixtures/document-understanding/<caseId>/document-profile.json`** (see §5 for the field list) — the source-safe characterization of the document, frozen at the same time as the selection record (before Ground Truth, since it must never depend on Ground Truth or engine output for the source-safe portion).

**`fixtures/document-understanding/<caseId>/research-history.jsonl`** (append-only, one JSON object per entry; see §10) — a structured log of observation/hypothesis/intervention/result/conclusion/unresolved-question entries, distinguished by an explicit `kind` field, so that a future consumer (LLM or otherwise) cannot conflate "we observed X" with "we concluded X" or "we speculated X."

Everything else (raw/normalized/evaluation artifacts, the evidence/report files) keeps its current location and git-ignore/commit split unchanged. **No existing case is migrated in this task.**

### 4.3 Isolation invariant (unchanged, restated)

Ground Truth remains readable only by the evaluator, exactly as today. A Case Package's `document-profile.json` (source-safe features) must be constructible *before* Ground Truth exists and *before* any engine has run — this is what makes it usable for strategy selection on a genuinely unseen document (§9).

## 5. Document Profile

### 5.1 Source-safe features (A) — obtainable without running any analysis engine

These come from the acquisition step, basic file identification (`pdfinfo`-equivalent — already used, unmodified, during case-002's selection), and direct human/visual inspection under the existing case-selection protocol discipline (`fixtures/document-understanding/case-002/20260926_0834_Case002_Selection_Protocol.md`'s "avoid circularity" principle extends naturally here: none of these may come from running one of the compared engines).

- Ministry/organization (from the document's own cover page, not inferred)
- Fiscal year, document purpose (request / settlement / important-policy, etc. — already an axis in `sources/source-registry.csv`'s `documentStage` column)
- Page count, PDF version, producer/metadata (`pdfinfo`-derived)
- Text-layer presence (scanned vs. text-native) — a binary safe to check via `pdfinfo`/basic inspection
- Visually observed: table density on the target region, multi-column structure, wrapped-label prevalence, annotation-column presence and its position (same-line vs. continuation-line — the exact distinction that broke `splitTrailingTriple`), unit-label placement (page-local vs. document-global), glyph conventions observed (e.g. `△` usage) — all obtainable the same way case-002's selection record and Ground Truth evidence document already obtained them: direct visual inspection, no engine

### 5.2 Engine-derived features (B) — require running at least one analysis engine

- Which engines successfully produced any raw output at all
- Detected table grid dimensions/density (Docling-specific — only knowable after running Docling)
- Reconstructed-line count, item/expense-code candidate counts (ambiguity signal — only knowable after running a normalizer)
- Any per-engine failure signature (e.g. Docling's "N of M cells dropped" warning)

### 5.3 Why the split matters

Document Profile (A) is the *only* thing a strategy-selection system may see for a genuinely unseen document before choosing a strategy — using (B) for that purpose would mean "running an engine to decide whether to run an engine," which is circular for anything expensive (Docling) and leaks information a real deployment wouldn't have in advance. (B) is still valuable — as an *outcome* to log in the Case Package once a strategy has run — but must never be fed back into the strategy-selection input for the *same* document.

**Ministry is explicitly not assumed to be the primary classifier.** Case-001 (Digital Agency) and case-002 (METI) already show that document *purpose and layout family* (概算要求書's 明細表 structure, annotation-column placement) matter more directly to which normalization succeeds than which ministry issued it — two ministries could plausibly share a template family, and the same ministry could plausibly change template across years. Layout/template family should be treated as a first-class, independent feature from ministry, not derived from it.

## 6. Analysis Strategy

A **Strategy** is a versioned, named combination of:

- extraction engine + exact pinned version (already tracked per-adapter today)
- engine configuration (e.g. Docling's `page_range`, PyMuPDF's `sort=True` — already fixed choices today, but currently implicit rather than named)
- which normalizer applies (`normalize.mjs` vs. `normalize-docling.mjs` today; a layer-5 document-family adapter would be a new normalizer variant selected *in addition to* the engine-specific one)
- the specific set of layer-3/4/5 rules active (e.g. "trailing-anchor triple regex" vs. a hypothetical "triple-anywhere-before-non-numeric-suffix regex")
- validation rules applied post-normalization (e.g. the arithmetic consistency check already used, informally, during case-002's Ground Truth creation — this should become a named, reusable validation step, not a one-off manual check)

A Strategy identifier should be stable and referenceable, e.g. `pdfjs-baseline@common-v1` vs. a hypothetical `pdfjs-baseline@common-v2+triple-relaxed`, so a future record can state "Strategy `docling@case001-cellmap-v1` was selected for document D because its profile resembled C03/C11/C19" without ambiguity about which exact rule-set that implies. **No strategy beyond the two that already exist implicitly (the current `common.mjs`+engine combinations, and `normalize-docling.mjs`) is defined or implemented in this task.**

## 7. LLM role

### 7.1 Conservative role definition

The LLM should be positioned as a **retrieval-and-reasoning layer over Case Packages**, not as an extraction or Ground Truth engine:

- **Case Package retrieval**: given a new Document Profile, retrieve the most similar prior cases (by profile features, not by running engines on the new document first).
- **Document-family hypothesis**: propose which layout family the new document likely belongs to, with stated uncertainty.
- **Strategy ranking**: propose an ordered list of candidate strategies with a rationale referencing which prior case(s) support each candidate.
- **Failure-mode prediction**: state which *known* failure modes (from research history, §10) are plausible for this document, before running anything expensive.
- **Analysis-plan generation**: produce a plan (which engine, which validation steps) for a human or the deterministic pipeline to execute — not a final structured answer.
- **Confidence/uncertainty explanation**: articulate *why* a ranking was made and how confident it should be treated, especially when profile similarity is weak (no close prior case).

### 7.2 What the LLM must never do

- Never read the target document's Ground Truth, or any information derived from it, at strategy-selection time (this is the leave-one-out discipline in §9).
- Never directly transcribe or invent final structured values (item/expense names, amounts, signs) from the PDF itself as a substitute for the deterministic pipeline — that would collapse layers 2–6 back into an unaudited black box, reversing this repository's entire raw-vs-normalized-vs-semantic discipline.
- Never be the sole judge of whether its own selected strategy succeeded — evaluation against Ground Truth remains deterministic code (`evaluate.mjs`-equivalent), exactly as today.
- Never treat a hypothesis or a single case's finding as an established rule without it being explicitly logged as `hypothesis` rather than `conclusion` (§10) — mirroring the exact lesson case-002 taught about `evaluate.mjs`'s own overfit.

### 7.3 Critical evaluation of the flow diagram in the task prompt

The prompt's proposed flow is directionally reasonable but has two problems worth flagging now rather than discovering later:

1. **"LLM Strategy Selection / Ranking" sitting directly before "Deterministic Analysis Pipeline"** implies a single strategy is chosen before any real signal exists for a genuinely novel layout family with no close prior case. The architecture needs an explicit **"no confident match" outcome** — falling back to a default/baseline strategy plus flagging for human review — rather than forcing a ranked choice when retrieval similarity is low. Silently forcing a choice is exactly the kind of "confidently wrong, no ambiguity signal" failure Docling exhibited on case-002.
2. **"Validation" and "Evaluation / Human Review" as separate late stages** risks the arithmetic-consistency-style checks (used informally in Ground Truth creation today) not being run *before* a strategy's output is trusted for anything beyond scoring. Validation should be a required gate the deterministic pipeline itself enforces (already true in spirit for Ground Truth creation; should be equally true for strategy execution), not merely a downstream evaluation concern.

## 8. Benchmark levels

### Level 1 — Extraction
Metrics: text/glyph presence, coordinate/cell availability, page-identity correctness. Already effectively measured today by comparing raw artifacts across engines (e.g. Docling's cell count, pdfjs/pymupdf line counts) — should be made an explicit, named benchmark level with its own pass/fail criteria distinct from Level 2, so a Level-2 failure is never mistaken for a Level-1 one (case-002's `null` deltas were Level-2 normalization failures on top of successful Level-1 extraction — this distinction was already implicit in the case-002 report and should become a formal benchmark axis).

### Level 2 — Document Understanding
Metrics: exactly the existing `evaluate.mjs` checks (item/expense identity, amount relationships, hierarchy, unit, sign, table relationships) — already well-designed for this purpose, including the corrected `delta_sign_evidence_matches_source`. This level's evaluator must itself be periodically re-examined for single-fixture overfit, per §2's last finding — a standing methodological practice, not a one-time fix.

### Level 3 — Strategy Selection
This is new and harder; do not finalize metrics prematurely. Candidate metrics, with leakage risks noted:

- **Selection accuracy**: did the system pick a strategy that scores within some tolerance of the best-known strategy for that document? *Leakage risk*: computing "best-known" requires having already run all strategies on the held-out document, which is fine for *evaluating* the selector post-hoc but must never be available to the selector itself.
- **Regret vs. oracle**: difference between selected-strategy score and best-possible-strategy score. Same leakage caveat.
- **Trial-and-error cost**: if the system is allowed to try more than one strategy, how many attempts before an acceptable result? Rewards efficient ranking, not just eventual success.
- **Known-failure-mode prediction accuracy**: did the system correctly flag, in advance, a failure mode that research history had already documented for a similar layout family (e.g. "this looks like it may have a same-line annotation column risk")? This is arguably the most valuable and least leakage-prone metric, since it can be checked against *documented* history rather than the held-out document's actual Ground Truth.
- **Calibration**: when the system reports low confidence (no close prior case), does that correlate with actually poor outcomes? A miscalibrated confident-but-wrong system (Docling's case-002 failure mode) is worse than an honestly-uncertain one.

Do not adopt a single scalar "Level 3 score" until enough cases exist to make the choice of metric evidence-based rather than arbitrary (see §16).

## 9. Evaluation protocol — held-out / leakage controls

**Leave-one-case-out (LOCO)** is the right starting protocol given the current corpus size (2): build Case Packages for all cases, hold one out entirely, give the LLM only the *document-profile-A* features (never B, never Ground Truth, never the held-out case's own research-history entries) plus the full Case Packages of the remaining cases, ask for a strategy ranking, execute the top-ranked strategy through the unchanged deterministic pipeline, and *only then* compare against the held-out case's Ground Truth to score the selection.

As the corpus grows, **leave-one-layout-family-out** becomes the more scientifically meaningful protocol: LOCO with only 2–3 cases per family risks the "held-out" case being trivially similar to another case from the *same* family, which doesn't test generalization to a genuinely novel layout — it tests memorization of a near-duplicate. Leave-one-family-out forces the selector to generalize across families using only cross-family reasoning (or honestly report low confidence), which is the harder and more useful question. Recommend **starting with LOCO (feasible immediately, even at N=2–3) and graduating to leave-one-family-out once at least 3 distinct layout families exist** (see §16).

Hard constraints regardless of protocol:
- The held-out case's `ground-truth.json` must never be readable by anything upstream of the final evaluation step.
- The held-out case's `research-history.jsonl` entries dated *after* its own case creation must never leak into another case's retrieval context if this is ever tested with a temporal ordering (see §11) — e.g. a later correction discovered *because of* the held-out case (like the evaluator fix in this very repository) must not be available to a strategy-selection experiment that is supposed to simulate not yet knowing about that case.
- Document-profile-A features are the only permitted input about the held-out document itself.

## 10. Research history as data

Case-001/case-002 already generated exactly the kind of history this section asks to formalize. A minimal, illustrative (not implemented) structured form, distinguishing kinds explicitly:

```jsonc
// fixtures/document-understanding/case-002/research-history.jsonl (illustrative, NOT created in this task)
{"kind": "observation", "date": "2026-09-26", "text": "Docling's TableFormer built a 23x12 grid for this page (case-001 was 21x14); 1 of 322 cells dropped."}
{"kind": "observation", "date": "2026-09-26", "text": "Amount triple and item/expense labels landed in different, misaligned grid cells."}
{"kind": "hypothesis", "date": "2026-09-26", "text": "Docling's table-cell separation advantage from case-001 may not generalize to sparser/differently-dense layouts."}
{"kind": "result", "date": "2026-09-26", "text": "H1 not supported: docling scored 2/11, same tier as flat-text baselines, via a different (silent wrong-row) failure mode."}
{"kind": "intervention", "date": "2026-09-26", "text": "Corrected evaluate.mjs's delta_glyph_observed_and_associated -> delta_sign_evidence_matches_source."}
{"kind": "result", "date": "2026-09-26", "text": "case-002 scores +1 per engine after the evaluator fix; case-001 unchanged."}
{"kind": "conclusion", "date": "2026-09-26", "text": "Evaluator checks can overfit a single fixture even with correct Ground Truth isolation; this is a distinct defect category from extraction/normalization bugs."}
{"kind": "unresolved_question", "date": "2026-09-26", "text": "Does relaxing splitTrailingTriple's trailing-anchor assumption generalize without reintroducing amount-similarity-as-selection-evidence risk?"}
```

The `kind` enum (`observation | hypothesis | intervention | result | conclusion | unresolved_question`) is the load-bearing design element: it prevents a future reader (human or LLM) from treating a `hypothesis` as a `conclusion`, which is precisely the discipline `protocol/RESEARCH_PROTOCOL.md` already demands for research findings generally (`ADR-002`'s "amount similarity may validate, never select" is the same category of discipline applied to a different axis). A machine-readable form is worth pursuing specifically *because* it lets a future strategy-selection system distinguish "this is well-established" from "this was speculated once" when reasoning about which prior findings to trust for a new document — but the schema should stay minimal (kind/date/text, plus optional references to specific commits/artifacts) rather than trying to fully formalize causal relationships prematurely.

## 11. Provenance and versioning

Identities/version references, and where each already exists vs. would need to be added:

| Identity | Status |
|---|---|
| Source binary SHA-256 | Exists (`sources/source-lock.json`) |
| Ground Truth freeze commit | Exists informally (stated in reports, e.g. `5a2eb32`); should become a formal field in `ground-truth.json` itself (currently absent — a documentable gap, not fixed in this task) |
| Engine/version | Exists (`engineVersion` in raw artifacts) |
| Adapter/version | Partially exists (pinned dependency versions); the adapter *code itself* has no explicit version identifier today — would need one once multiple strategy variants of the same adapter coexist |
| Strategy version | Does not exist — new concept (§6) |
| Evaluator version | Does not exist explicitly — the evaluator-correction report (`20260926_1231_...md`) is the closest current analogue, referencing a commit SHA rather than a formal version field. A minimal future step: a `evaluatorVersion` field in evaluation output, bumped whenever a check's semantics change (as happened at `519ce28`) |
| Experiment commit | De facto exists (every research action in this repository is a Git commit) |
| Result artifact | Exists (`evidence/document-understanding/*-results.json`, `derived/.../*.evaluation.json`) |
| Case Package version | Does not exist — new concept; would matter once a Document Profile or research-history entry for an existing case is amended after new findings |

The important discipline (already partially demonstrated by this repository's insistence on preserving `379043d` unamended after the evaluator fix): **a future LLM reasoning "what was known at the time" must be able to reconstruct the state of Case Packages *as of a given commit*, not just their current state.** Since every artifact here is already Git-tracked text/JSON, this is achievable without new infrastructure — by pinning any research-history-based retrieval to a specific commit/ref rather than always reading `HEAD` — but it is worth stating explicitly as a requirement now, before a retrieval system is built that might otherwise default to "latest," silently leaking hindsight into a supposedly historical simulation.

## 12. Testing the architecture against existing evidence

Classifying case-001/case-002's actual findings into the layer taxonomy from §3.1, without altering either case:

| Finding | Layer |
|---|---|
| pdf.js/PyMuPDF/Docling raw extraction succeeded on both cases | 2 (raw representation) |
| Docling's cell separation resolving case-001's conflation | 1 (engine behavior) + 4 (engine-specific normalization consuming it) |
| Docling's grid misalignment on case-002 | 1 (engine behavior) — a *new* engine behavior not previously characterized, not a normalizer bug |
| `splitTrailingTriple`'s trailing-anchor break | 5 (document-family/layout-specific) — currently miscategorized as layer-3 generic code |
| `common.mjs` missing CJK-space-closing | 4 (engine-specific normalization gap, specifically for pdfjs-dist's behavior) |
| Unit label page-locality | 5 (document/layout characteristic) — correctly identified as an *observation* in the case-002 selection record, not a selection criterion |
| `delta_glyph_observed_and_associated` defect | 7 (evaluation methodology) |
| METI WAF acquisition | Precondition, outside the 7-layer taxonomy — belongs in source-acquisition provenance, not a Document Profile feature |

This mapping is more explanatory than the implicit "one pipeline, patch as needed" model in two ways: it correctly separates the `splitTrailingTriple` failure (layer 5 — a layout-family boundary problem) from the CJK-spacing gap (layer 4 — an engine-specific gap unrelated to which document is being processed), which the current flat `common.mjs` file conflates into one module. Under the current model, both would likely be "fixed" by editing the same file, without ever recording *why* one fix is engine-scoped and the other is layout-scoped — exactly the ambiguity that leads to over- or under-generalizing a rule.

## 13. Alternatives considered

| Approach | Advantages | Disadvantages | Verdict |
|---|---|---|---|
| **A. One universal parser/normalizer** | Simplest to reason about; what this repository effectively has today | Case-002 already falsified the "one set of rules generalizes" assumption for something as basic as trailing-triple parsing; forces every new document to either fit the existing rules or silently degrade | Insufficient on current evidence |
| **B. Ministry-specific parsers** | Directly addresses per-issuer template differences | Assumes ministry is the right partition key — evidence suggests layout/template family, not ministry, is the actual driver (a ministry could change template year-to-year; two ministries could share a template vendor/convention); doesn't scale (47+ ministries/agencies × multiple document types each) | Not recommended as the primary axis |
| **C. Document-family/layout-specific adapters** | Matches the actual observed failure boundary (layout, not issuer); reuses engine-specific normalizers underneath | Requires a working Document Profile / family-detection mechanism to know which adapter to use — doesn't solve strategy selection by itself, just narrows what's being selected between | Necessary component, not sufficient alone |
| **D. Case-based strategy selection (this proposal)** | Explicitly reuses C, adds a principled mechanism for choosing among family-specific strategies for *unseen* documents, and turns research history into a reusable asset rather than only prose | Substantial new infrastructure (retrieval, profiling, evaluation-with-leakage-control) before any payoff is visible; payoff unproven until a real corpus exists | Right direction, but must be built incrementally and evidence-gated (§15), not assumed to work |
| **E. LLM directly extracts final structured values** | Fewest moving parts; potentially robust to layout variation an engineered parser hasn't seen | Directly violates this repository's central discipline (raw vs. normalized vs. semantic vs. Ground Truth separation); makes failures unauditable; Ground-Truth-contamination risk is much harder to police than for a deterministic pipeline; case-002's own protocol explicitly prohibits exactly this kind of engine for *selection*, and the same reasoning applies even more strongly to final-value extraction | Rejected as the primary extraction mechanism; LLM's role stays at the retrieval/reasoning layer (§7) |

The evidence does not support jumping straight to D+E combined, nor does it support staying at A. C is a necessary intermediate step this repository has not yet built (only 2 cases, both currently handled by the same "generic" code path with per-engine variants) — before D is worth investing in, C needs to exist for at least a few genuinely distinct layout families.

## 14. Repository evolution (proposed, not migrated)

Conceptual future layout, extending rather than replacing current structure:

```text
fixtures/document-understanding/<caseId>/
  ground-truth.json                    (unchanged — existing convention)
  document-profile.json                (NEW, source-safe features only, frozen pre-Ground-Truth)
  research-history.jsonl               (NEW, append-only)
  <existing selection-protocol/record/README/evidence files>   (unchanged)

scripts/document-understanding/
  adapters/<engine>/                   (unchanged)
  strategies/<engine>/<strategyId>/    (NEW, only once >1 strategy variant per engine exists —
                                         e.g. a layout-family-specific normalizer variant)
  benchmark/                           (unchanged core; extended with Level 1/3 metrics per §8)

evidence/document-understanding/       (unchanged — compact per-case results)
reports/document-understanding/        (unchanged — narrative reports, this document included)
```

- **What stays where:** everything committed today stays committed in the same place; nothing here proposes moving `evidence/` or `reports/` contents.
- **What would eventually move:** nothing is *moved* — `strategies/` is additive, only populated once a document-family adapter is actually written (not in this task).
- **What remains generated/ignored:** `derived/document-understanding/` keeps its current git-ignored, regenerable status; a future retrieval index (if built) would also be generated/ignored, never hand-edited or treated as a source of truth over the committed Case Package files.
- **What should be committed:** `document-profile.json` and `research-history.jsonl` — both are durable, human-reviewable research artifacts in the same spirit as `ground-truth.json`, not generated output.
- **How old cases remain reproducible:** case-001 and case-002 are not touched by this proposal; they remain valid, complete Case Packages under the *current* schema even without a `document-profile.json`/`research-history.jsonl` — those two files are additive fields a future migration task could backfill from the existing prose (README/selection-record/reports), not a breaking schema change.

## 15. Migration plan (incremental, evidence-gated)

| Phase | Content | Gate to proceed to next phase |
|---|---|---|
| **1** | Formalize the Case Package schema (document-profile.json, research-history.jsonl) using case-001/case-002 as the first two instances (backfilled from existing prose) | Schema is expressive enough to represent everything already learned from both cases without loss; reviewed against §12's mapping |
| **2** | Add several more diverse cases (different ministry, different document purpose, at least one scanned/non-text-native if available) — no strategy selection yet, just growing the corpus and exercising the schema | At least 3 genuinely distinct layout families represented (not just 3 more documents that happen to share case-002's template) |
| **3** | Define/document strategy variants explicitly (e.g. a layout-family-specific triple-parsing variant addressing the case-002 finding) — each named/versioned per §6 | At least 2 named strategies exist for the same engine, differing in a documented, principled way (not ad hoc per-case hacks) |
| **4** | Build a Document Profile representation suitable for similarity comparison (even a simple structured-feature match, no embeddings required yet) | Profile similarity computed for at least one pair of cases correlates, on manual review, with actual strategy-applicability overlap |
| **5** | LLM strategy-selection experiment, LOCO protocol (§9), on the corpus from Phase 2–4 | Selection meaningfully outperforms a naive baseline (e.g. "always pick the most recently added strategy") on at least the known-failure-mode-prediction metric (§8) |
| **6** | Held-out evaluation at the layout-family level (leave-one-family-out), once ≥3 families with ≥2 cases each exist | Results are stable enough (not dominated by single-case noise) to draw a generalization conclusion |

Each gate is a **go/no-go based on evidence**, not a calendar date. If Phase 2 reveals that "layout family" itself resists clean categorization (documents don't cluster cleanly), that is itself an important finding requiring the architecture to be revisited before Phase 3, not papered over.

## 16. How many cases?

No statistically justified number exists at N=2. Pragmatic staged targets, organized by diversity dimension rather than raw count:

- **Ministries/organizations:** at least 3–4, chosen to include at least one pair that plausibly shares a document-generation toolchain (both current PDFs were produced by "List Creator," per `pdfinfo` — worth deliberately testing whether that correlates with layout similarity, or whether ministry-level customization dominates regardless of shared tooling)
- **Document purposes:** request (概算要求書, both current cases), plus at least one settlement/execution-stage document (a genuinely different template family per `protocol/RESEARCH_PROTOCOL.md`'s budget-lifecycle invariants) and one summary-table-only case
- **Layout families:** the real target metric — aim for at least 3 *demonstrably distinct* families (distinct enough that a strategy tuned for one measurably underperforms on another, as case-001→case-002 already showed for one pair) before attempting any strategy-selection experiment
- **Fiscal years:** at least 2 different years for the *same* ministry, specifically to test whether a single ministry's template is stable across years (unknown today) — directly relevant to whether "ministry" or "template version" is the more durable classifier
- **Text-native vs. scanned:** at least 1 scanned/OCR-requiring case, since neither current case exercises that axis at all, and it changes which engines are even applicable (MinerU's OCR strength, currently un-integrated, becomes directly relevant here — see `reports/document-understanding/external-engine-survey.md`)
- **Table complexity:** deliberately include at least one visually simple, single-column, non-wrapping case as a "should be easy" control — both current cases were deliberately chosen for wrapping/structural difficulty; a benchmark with no easy cases can't distinguish "engine failed" from "case was hard by design"

A pragmatic near-term target: **6–8 cases covering at least 3 layout families before attempting Phase 5.** The purpose of this specific number is only to ensure LOCO (§9) has more than one same-family neighbor to hold out against per family — not a claim of statistical sufficiency for any general conclusion.

## 17–18. Deliverables / no implementation

This document is the sole deliverable. No parser, adapter, normalizer, LLM workflow, embeddings/retrieval system, or `case-003` was implemented, and no existing case, normalizer, evaluator, or Ground Truth file was modified in this task.

## Open questions

- Does "layout family" cluster cleanly across real documents, or is it a continuum that resists discrete categorization? (Phase 2's real test.)
- Is `pdfinfo`'s `Producer` metadata (`"List Creator"` for both current PDFs) a meaningful family signal, or coincidental (a common government-wide tool with no bearing on internal table layout)?
- How much of `splitTrailingTriple`'s generalization problem would a *structural* (table-aware) parser sidestep entirely, versus how much is genuinely layout-variable even for a good table parser? (Directly relevant to whether Docling-style engines are worth prioritizing over flat-text engines going forward.)
- What is the right unit for "strategy" versioning once document-family adapters exist — one version per (engine × family) pair, or a more compositional scheme? Not resolved here; deferred to Phase 3.
- Should `research-history.jsonl` entries ever be authored automatically (e.g. by the benchmark runner logging a `result` entry per run), or should they remain manually curated to preserve the observation/hypothesis/conclusion discipline? Leaning toward "runner logs `result`/`observation` automatically; `hypothesis`/`conclusion`/`unresolved_question` remain human/LLM-authored and reviewed" — not decided.

## Files changed

- `reports/document-understanding/20260926_1316_Case_Based_Document_Understanding_and_LLM_Strategy_Selection_Research_Architecture.md` (this file, new)
- `protocol/DECISIONS.md` (new ADR — see below)
- `state/CURRENT_STATE.json`, `state/TODO.md`, `state/CHANGELOG.md` (updated to record this design work)

No code, Ground Truth, adapter, normalizer, evaluator, or case fixture file was modified.
