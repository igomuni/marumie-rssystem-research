# Case-006–010 Selection Freeze

Status: **selection freeze. Authorities, order, and methodology are frozen. Case-006's own source survey has NOT begun — this document freezes the decision, not the research.**

Date: 2026-09-28 (Asia/Tokyo)

Branch: `research/fy2024-all-authority-format-census`.

This freeze follows human review of `20260928_0634_Case006_010_Selection_Rationale_Review.md` (commit `1dd37a8`), which itself followed `20260927_2110_FY2024_Census_Checkpoint_Overview.md` (commit `7ab30e0`). It adopts the review's own recommended five-case set unchanged in composition, with two methodological refinements from the review's own human reader, both recorded below as binding for their respective cases.

## 1. Frozen five-case set

| Case | Authority | Primary purpose | Status |
|---|---|---|---|
| 006 | 法務省 (Ministry of Justice) | Isolate the raster-only (zero-text-layer) representation axis, cleanly, as a single variable | **Adopted** |
| 007 | 内閣官房 (Cabinet Secretariat) | File-scoped context mechanism (context established once per package-split file, never re-derivable by page lookback) | **Adopted** |
| 008 | 裁判所 (Courts) | Embedded multi-grammar structure, promoted from an incidental census observation to a primary research question | **Adopted** |
| 009 | 内閣本府 (Cabinet Office) | Exploratory test of whether extreme split packaging (~50 files) produces a genuinely new context/source-identity mechanism, or is merely a packaging-scale difference | **Adopted, exploratory** |
| 010 | 厚生労働省 (Ministry of Health, Labour and Welfare) | Large-scale stress test of context-recovery architecture at the census's own largest document | **Adopted** |

This composition is unchanged from the selection rationale review's own §14. No additional candidate comparison was performed in this freeze task.

## 2. Rejected/deferred alternatives (frozen, for the record)

- **金融庁 (FSA)**: deferred in favor of 法務省 for the raster axis. Rationale (from the review, re-affirmed in freeze): FSA's own 12-file split confounds rasterization with an extreme-package-split variable in one case; 法務省's own single-file packaging isolates the raster axis as the sole new variable, directly enabling the interpretability the human reviewer specifically endorsed.
- **厚生労働省 as embedded-substructure primary**: deferred; 厚生労働省 is retained in the set, but for scale (§1), not for embedded-substructure primacy, which now belongs to 裁判所.
- **裁判官弾劾裁判所 / 裁判官訴追委員会 (dedicated cross-reference-summary case)**: deferred, not included. Rationale re-affirmed: the mechanism already has 7 confirmed instances across the census (the most-replicated single finding), and 裁判所's own embedded `重要政策推進枠要望額総表` section offers a plausible byproduct route to the same test within Case-008 itself. 裁判官弾劾裁判所 remains the frozen fallback candidate for a future Case-011+ if Case-008's own selection protocol finds that section unsuitable as a primary target.
- **公正取引委員会**: not a candidate; retained only as a cited negative control (shares FSA's own DocuWorks producer but has a text layer, confirming producer identity is never the family boundary).

## 3. Frozen execution order and its dependency rationale

**006 → (close out) → 007 → (close out) → 008 → (close out) → 009 → (close out) → 010**

Per explicit instruction from the human reviewer, this is a **strict one-case-at-a-time discipline**, not a batch: each case's own selection protocol is frozen, executed, and closed out (through at least a first-frozen benchmark run or an equivalent methodological milestone) **before the next case's own protocol work begins**. The five cases are deliberately chosen to test different failure modes; a finding from an earlier case may materially change how a later case's own protocol, Ground Truth methodology, or even the Case Package v0 concept design itself should be written. Freezing all five protocols upfront would risk locking in assumptions that Case-006 itself might overturn.

Dependency rationale (from the review, adopted unchanged):

- **006 first**: resolves a pipeline-applicability-boundary question (§4 below) that should inform how 010's own much-larger-scale case is later evaluated, and potentially how the benchmark's own evaluator handles a null/empty-extraction result at all.
- **007 before 009**: 009's own research value is best interpreted relative to 007's own already-confirmed file-scoped-context baseline; attempting 009 first would leave no comparison point for its own findings.
- **008** has no upstream dependency and could in principle run in parallel with 006/007, but is sequenced third to keep the lower-risk, well-evidenced cases earlier and the two more exploratory/uncertain cases (009, then the largest-scale 010) later.
- **010 last**: benefits from whatever evaluator or methodological refinements 006–009 may have already surfaced, and serves as the final, large-scale stress test.

## 4. Frozen methodology note for Case-006 (法務省) specifically

The human reviewer raised a specific, binding methodological caution for Case-006 that this freeze adopts as a hard constraint on that case's own future execution, distinct from the general case-001–005 methodology:

**The layering to keep distinct**:
```text
source acquisition
      ↓
source representation
      ↓
text extraction applicability
      ↓
document understanding
```

A raster/zero-text-layer source producing a null or empty result from all three currently-compared engines (pdf.js, PyMuPDF, Docling-without-OCR) is **not, by itself, a document-understanding failure** — it may instead be evidence of a **pipeline-applicability boundary**, a layer distinct from and upstream of document understanding. Case-006 must not collapse this distinction by scoring a null result against the existing 11-check matrix as if it were an ordinary low score.

**Frozen execution order for Case-006, once its own source survey begins** (not started in this freeze):

1. Freeze `raster-only` as a **source-safe fact** (established via `pdffonts`/`pdftotext`/visual render, before any row selection — mirroring this census's own already-established method) before any row is selected.
2. Run the **existing, unmodified** benchmark pipeline as the first frozen run — no OCR, no evaluator change, no engine substitution, at this stage.
3. If the result is null/empty across all three engines, **preserve that result as-is**, exactly as every other case-001–005 first-frozen result has been preserved regardless of outcome.
4. Attribute the failure explicitly to the **source-representation / acquisition-to-extraction boundary** layer in the case's own analysis, not to "document understanding" — this is an analytical framing requirement, not a request to alter any score.
5. Any OCR or alternative-extraction experiment is **explicitly deferred to a separate, later, separately-scoped task**, and must **never** be mixed into Case-006's own first frozen run. This preserves direct comparability with case-001–005's own first-frozen results, all of which used the same unmodified three-engine pipeline.

This methodology note applies specifically to Case-006; it does not retroactively alter any existing case-001–005 finding or methodology, and it does not itself constitute starting Case-006's own source survey.

## 5. Frozen framing for Case-009 (内閣本府) specifically

Per the human reviewer's own explicit correction: Case-009 must not be framed, in its own future selection protocol, as "内閣本府 is special because it has ~50 files." It is frozen instead as an **exploratory test of a specific question**:

> Does extreme split packaging (≈50 files) produce a genuinely new context/source-identity mechanism, distinct from the file-scoped mechanism already confirmed in Case-007/内閣官房's own 17-file package — or is it merely a packaging-scale difference with the identical underlying mechanism?

A future Case-009 selection protocol finding **no new mechanism** (i.e., confirming that ~50 files behaves exactly like Case-007's own 17-file file-scoped context, just with more files) is an explicitly legitimate, valuable outcome under this framing — not a failed or wasted case. This framing is binding on how Case-009's own eventual report characterizes its own findings, regardless of which way the evidence turns out.

## 6. What this freeze does not do

- Does not start 法務省's own source survey, row selection, selection protocol, or Ground Truth.
- Does not modify any case-001–005 frozen artifact.
- Does not modify `scripts/`, `sources/source-lock.json`, or `sources/source-registry.csv`.
- Does not implement any Case Package schema, MOF/RS linkage, or benchmark/evaluator change.
- Does not freeze case-007 through case-010's own selection protocols — per §3, each case's own protocol is frozen only when that case's own turn in the execution order arrives, informed by whatever the preceding case(s) in the order have already found.

---

**This document freezes the Case-006–010 authority set, rejected alternatives, execution order, and two case-specific methodology notes (Case-006's pipeline-applicability-boundary framing; Case-009's exploratory reframing). It does not begin any case's own source survey, row selection, or Ground Truth work.**
