# Semantic-data Batch-001 Design Protocol

Status: **FROZEN design protocol**
Date: 2026-09-29 (Asia/Tokyo)
Scope: request-side canonical semantic extraction only

## 1. Purpose and non-goals

Batch-001 tests whether the frozen Canonical Semantic Extraction Protocol can be applied reproducibly to several authority-isolated request sources and produce source-faithful canonical artifacts. It is not an engine leaderboard, population-representative accuracy study, full grammar-coverage exercise, or MOF-linkage experiment.

This protocol freezes the sampling procedure and orchestration only. It does not acquire a source, inspect authority content, execute sampling, name selected authorities, create Ground Truth, run a benchmark/OCR experiment, generate CSV, consult MOF material, or change production behavior.

## 2. Evidence basis and governing contract

This protocol is based only on committed evidence: the FY2024 Population Freeze, the Case-006–010 pilot closeouts and selection artifacts, the Cross-Case Synthesis, the canonical-data-model reframe, the frozen Canonical Semantic Extraction Protocol, its authority-preflight template, source registry/lock structure, and state files.

The Canonical Semantic Extraction Protocol remains governing for each authority: `S0 → S7` (source admissibility, preflight, observation, structural interpretation, normalization, semantic candidates, financial association, canonical freeze). This design does not amend it.

## 3. Population and prior-exposure exclusion

The population is the 33 authorities in the committed FY2024 Population Freeze, in the exact numbered order printed by that artifact. The authoritative population source is the MOF FY2024 cross-authority expenditure-link table captured in `fixtures/document-understanding/fy2024-format-census/20260927_1909_FY2024_Population_Freeze.md`; the committed census CSV is its machine-readable companion.

All Case-001–010 authorities are excluded before sampling because of prior research exposure. This is an unseen-authority validation boundary, not an outcome, quality, format, score, or suitability judgment. Duplicate authority IDs are excluded. No unselected authority PDF, landing page, format, package, representation, grammar, or context may be inspected to make this selection.

## 4. Frozen sampling procedure

The companion `authority-sampling-procedure.json` is authoritative for executable details. Its fixed procedure is:

1. Load the committed Population Freeze in its printed numbered order.
2. Retain exactly one record per authority ID in that order.
3. Exclude Case-001–010 exposure IDs and any duplicate ID after its first occurrence.
4. Retain records whose freeze record contains a non-empty authority ID, authority name, and MOF expenditure-link URL. Missing required metadata is a recorded sampling exclusion, never repaired by web lookup.
5. Take the first six remaining eligible records in that frozen order as the primary cohort.

This is content-blind and deterministic. It does not stratify by uninspected representation, package, grammar, context, expected extraction performance, or presumed convenience. The procedure is **not executed in this task**; no authority list is frozen here.

### Exact size: six

Five offers slightly less operational diversity; eight exceeds a prudent first-batch human review and provenance burden. Six is the frozen operational pilot size: it permits three two-authority waves, preserves failure isolation, and gives more protocol-defect discovery opportunity than five without implying statistical representativeness. This is an operational batch-size decision, not a population sample-size estimate.

### No reserve and no replacement

`reserveN = 0`. A primary authority that is unavailable, inadmissible, representation-blocked, ambiguous, structurally mismatched, or otherwise terminal is retained as that authority's result. Batch success is not “six successful authorities”; it is deterministic processing to terminal status without silent substitution. A later targeted batch may be separately designed if this produces a materially different need.

### Option 1 adopted

Only the procedure is frozen now. The next task, **Batch-001 Authority Selection Manifest Freeze**, must mechanically execute this unchanged procedure and freeze only the primary six IDs/names plus the input artifact SHA and execution trace. It must not acquire sources. The sampling procedure has `samplingExecuted: false` in this freeze.

## 5. Authority isolation and lifecycle

Each selected authority is an independent research unit. Its lifecycle is:

`B0 selected authority frozen → B1 source survey/acquisition → B2 source admissibility → B3 preflight profile freeze → B4 observation → B5 structural interpretation → B6 normalization → B7 semantic candidate derivation → B8 financial association → B9 canonical freeze → B10 validation/authority closeout`.

Candidate enumeration is prohibited before B3. Later-authority observations must not rewrite an earlier authority's frozen artifact. A per-authority terminal result never erases or blocks another authority's evidence.

## 6. Parallelism and Git model

Run at most two authorities concurrently, in three waves of two. Within an authority the lifecycle is strictly ordered. A wave begins only after the batch coordinator confirms that each preceding wave authority has either reached a terminal status or a documented batch pause applies.

Use model C: each authority receives an independent branch and worktree from the same frozen Batch-001 base, then audited integration commits are made by the batch coordinator. Authority branches must not concurrently edit shared `state/*`; the coordinator alone maintains a future batch status index after review. This prevents state-file conflicts while retaining authority-level chronology and auditability.

## 7. Artifact and output contract

Batch-level artifacts are this design/procedure/template, the later selection manifest, a future execution/status index, amendment records if needed, and final synthesis. No batch-wide mutable canonical data file is permitted.

Each authority has its own directory and immutable canonical freeze boundary, containing at minimum:

- `source-manifest.json`
- `authority-preflight.json`
- `nodes.jsonl`
- `edges.jsonl`
- `financial-observations.jsonl`
- `semantic-candidates.jsonl`
- `canonical-manifest.json`
- authority validation/closeout report

Engine-native raw output remains separate from canonical output. CSV is derived only after canonical freeze; a CSV failure does not invalidate an authority's canonical outcome. No MOF data, identifiers, hints, or linkage feedback may enter B0–B10.

## 8. Terminal statuses and stop semantics

An authority must end in one preserved terminal status: `COMPLETE`, `PARTIAL`, `NULL_SEMANTIC_CANDIDATE`, `STRUCTURAL_MISMATCH`, `REPRESENTATION_BLOCKED`, `SOURCE_UNAVAILABLE`, `SOURCE_INADMISSIBLE`, `AMBIGUOUS`, `EXTRACTION_FAILURE`, or `PROTOCOL_BLOCKED`. These states are not coerced to empty data or zero.

Authority-local stops include unavailable/inadmissible source, representation block, ambiguity, NULL candidate, structural mismatch, and extraction failure. Batch-wide pause is required for a protocol contradiction, an observed structure that the canonical model cannot represent, provenance/lock failure, GT or MOF leakage, or a shared implementation change. A pause is not a silent fix: preserve current results, create a defect record, design and freeze an amendment, decide rerun scope, then resume only under the amended protocol.

## 9. Review, amendment, and success criteria

Required review checkpoints are: sampling-manifest freeze; each authority preflight-profile freeze; each authority canonical freeze; and batch synthesis. Mid-batch amendment sequence is: stop affected authority; record defect; do not patch silently; freeze amendment; decide whether earlier authorities require rerun; preserve pre-amendment results.

Batch success requires deterministic sampling compliance; a terminal result for every primary authority; preserved provenance and stage boundaries; canonical artifacts where allowed; retained NULL/failure evidence; no silent replacement; reproducible lifecycle traces; and sufficient evidence for a later Batch-002/MOF-side decision. It does not require six successes or establish population accuracy.

## 10. MOF-readiness and statistical boundary

Future authority closeouts may separately assign request-side readiness labels such as `READY_FOR_MOF_SCHEMA_SURVEY`, `REQUEST_SIDE_AMBIGUOUS`, `REQUEST_SIDE_STRUCTURAL_BLOCK`, or `REQUEST_SIDE_INCOMPLETE`; none is assigned in this task. Batch-001 makes no MOF linkage claim.

The cohort is not population-representative. Permitted conclusions concern protocol viability, observed authority outcomes, operational reviewability, canonicalization feasibility, and isolated failure modes only.

## 11. Integrity, non-actions, and handoff

No source/PDF inspection, authority selection execution, GT, benchmark, OCR, CSV generation, MOF work, parser/normalizer/evaluator change, source-lock/registry change, or production adaptation occurred while freezing this design.

Next task: **Batch-001 Authority Selection Manifest Freeze**. It must execute the frozen procedure mechanically, freeze the six primary authorities, and stop before source acquisition.
