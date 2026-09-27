# Case-006–010 Selection Rationale Review

Status: **recommendation only. No source survey, row selection, selection protocol freeze, Ground Truth, benchmark run, engine comparison, parser/normalizer/evaluator change, or MOF/RS linkage was performed. Case-006–010 is not frozen.**

Date: 2026-09-28 (Asia/Tokyo)

Branch: `research/fy2024-all-authority-format-census`, from checkpoint commit `7ab30e0`.

## 1. Executive summary

Comparing seven required candidates (金融庁, 法務省, 内閣官房, 裁判官弾劾裁判所, 裁判官訴追委員会, 内閣本府, 厚生労働省) plus two census-evidence-driven additions (裁判所, and reconsidering 公正取引委員会 as a negative control) against the four independent axes established in the checkpoint (`20260927_2110_...Checkpoint_Overview.md`), this review recommends a five-case set that departs from the checkpoint's own fixed candidate sketch in two material ways, each argued from evidence gathered in this review:

1. **法務省 (MOJ), not 金融庁 (FSA), as the rasterized-family representative** — FSA's own 12-file split confounds the rasterization axis with the extreme-package-split axis in a single case; MOJ isolates rasterization cleanly as a single-file document.
2. **裁判所 (Courts), not 厚生労働省 (MHLW), as the primary embedded-substructure representative** — a minimal, disclosed spot-check performed in this review (§13) found that Courts' own single 127-page combined file contains **at least three** distinct embedded structures (the standard 明細表 ledger, an embedded 定員表 staffing table with an entirely different grammar, and an embedded 重要政策推進枠要望額総表 carrying its own cross-reference-summary mechanism) — a higher information density, at roughly 1/14th the page count, than MHLW's own single confirmed embedded-box instance.

MHLW is retained in the recommended set, but re-justified as the **scale-stress-test representative** (the largest document in the census, 1,723 pages) rather than as the sole embedded-substructure evidence source — its own embedded-box mechanism (confirmed via a second spot-check in this review, §13) is now a *fourth* independently-confirmed instance (after MEXT, MOF, MLIT), corroborating rather than uniquely justifying its selection.

A dedicated cross-reference-summary-as-primary-target case (the checkpoint's own original slot-008 idea, using dangai or sotsui) is **not** included in the final five — §14 argues the opportunity cost is low, since Courts' own 重要政策推進枠 section offers a plausible route to that same test as a byproduct of a single case, and the mechanism already has 7 replicated instances in evidence, unlike the genuinely single-instance gaps (rasterization, file-scoped context, extreme split).

## 2. Evidence base

Read in full for this review: `20260927_2110_FY2024_Census_Checkpoint_Overview.md` (the checkpoint being reviewed); `20260927_1909_FY2024_All_Authority_Concept_Request_Format_Census.csv` (all 33 rows, cross-referenced field-by-field for the compared candidates); `20260927_2059_FY2024_Census_Acquisition_Difficulty_Memo.md`; the Case Package v0 concept design (`20260926_1316_...Architecture.md` and its own successor, referenced for the "context-requirement provenance-class" open review issue this review's own §6 recommendation bears on). No case-001–005 frozen artifact was read for new content beyond what the checkpoint already cites (no re-inspection of case-001–005 sources was performed).

**Minimal additional inspection performed in this review**, per the originating task's own allowance for facts indispensable to candidate comparison: two spot-checks of already-locked, already-downloaded raw PDFs (裁判所's own document, at the specific pages the checkpoint's own header-ratio investigation had already flagged as anomalous; 厚生労働省's own document, at one of its own already-computed unit-declaration page positions). No new source was acquired, no new authority was surveyed, and no row was selected in either case — see §13 for the exact content read and why it was necessary to resolve the embedded-substructure candidate comparison the originating task explicitly requires.

## 3. Existing case coverage (recap, not re-derived)

| Case | Authority | Axis values already covered |
|---|---|---|
| case-001 | デジタル庁 | Standard grammar, single-file, full text (own independent format elements, not re-integrated into this census's own axis language) |
| case-002 | 経済産業省 | Standard grammar, single-file, full text, same-page/one-back-adjacent item context |
| case-003 | 総務省 | Standard grammar, single-file, full text, deeper intermediate breakdown level |
| case-004 | 文部科学省 | Standard grammar, **4-file split, encrypted**, zero-or-one-page-back item context, table-wide-once unit (now understood as the sparse end of the embedded-box mechanism), 3 distinct embedded-anomaly families studied incidentally |
| case-005 | 国土交通省 | Standard grammar + **cross-reference-summary** (observed once, incidentally, within the 明細表-focused row selection — never selected as a primary target), same-page context |

**Not covered by any existing case**: zero-text-layer representation; bureau/division-granularity package splits (17-file, ~50-file); file-scoped context; embedded-substructure as a *primary* selection target (only ever touched incidentally in case-004's own anomaly research and case-005's own 総表 observation); enacted-budget-stage grammar (out of this benchmark's own scope, never a candidate).

## 4. Candidate inventory

Beyond the 7 required candidates, this review adds **裁判所** (found, not assumed, to be a strong embedded-substructure representative via the minimal spot-check in §13) and briefly considers **公正取引委員会** as a *negative control* for the rasterized-family analysis (§8), since it shares FSA's own DocuWorks producer but has a text layer — already established in the census, re-cited here rather than re-derived.

| Candidate | pages | package | representation | encrypted | primary axis candidacy |
|---|---|---|---|---|---|
| 金融庁 (fsa) | 77 | 12-file split | **zero text** | no | rasterized + split (confounded) |
| 法務省 (moj) | 737 | single file | **zero text** | no | rasterized (isolated) |
| 内閣官房 (cas) | 1–29/file, 17 files | 17-file split | full text | yes (all 17) | file-scoped context |
| 裁判官弾劾裁判所 (dangai) | 9 | single file | full text | no | cross-reference-summary (smallest instance) |
| 裁判官訴追委員会 (sotsui) | 8 | single file | full text | no | cross-reference-summary (smallest instance); **has its own request-stage-vs-enacted-budget source-status history** (§5 flags this) |
| 内閣本府 (cao) | 25(cover)+3(sample) of ~50 files | ~50-file split | full text | yes | extreme split (context mechanism **unverified**) |
| 厚生労働省 (mhlw) | 1,723 | single file (coexists with 10+ separate narrative files) | full text | no | scale + confirmed embedded-box instance |
| 裁判所 (courts) — added | 127 | single file | full text | no | **embedded-substructure primary (multiple types in one file)** |

## 5. Candidate-by-candidate analysis

### 5.1 金融庁 (FSA)

- **New axis covered**: zero-text-layer representation.
- **Existing-case overlap**: none directly; standard-grammar-visually is shared with every case-001–005.
- **Expected information gain**: confirms the rasterized family exists as a real benchmark case, not merely a census observation.
- **Falsification value**: high — directly falsifies any implicit assumption that "every authority following the census's own visual grammar is text-extractable."
- **Methodological risk**: **confounds two axes in one case** — FSA is both rasterized AND a 12-file split (the second-most-granular package in the census). A benchmark result from FSA cannot cleanly attribute a finding to "rasterization" vs. "package fragmentation" without a second, non-rasterized 12-file-split case to compare against, which does not exist. Also: Ground Truth remains fully creatable via direct visual transcription (the standard method), but every compared engine (pdf.js, PyMuPDF, Docling-without-OCR) is expected to recover zero text — the resulting benchmark score would be a uniform, uninformative 0/11 across all three engines, providing no *inter-engine* differentiation (a real but disclosed limitation, not a blocker).
- **Feasibility**: fully feasible as a case (selection/GT creation are unaffected; only extraction-engine scoring is affected, and a uniform null result is itself a valid, informative finding).
- **Alternative candidate**: 法務省 — see §5.2 and §8 for the full comparison.

### 5.2 法務省 (MOJ)

- **New axis covered**: zero-text-layer representation, isolated from any package-split confound (single combined file).
- **Existing-case overlap**: none directly.
- **Expected information gain**: identical in kind to FSA's own (§5.1), but attributable specifically to rasterization alone, since MOJ's own package model (single file) matches the majority baseline already well-understood from case-002/003.
- **Falsification value**: same as FSA, with a cleaner attribution.
- **Methodological risk**: same uniform-null-result risk as FSA. Additionally the largest of the two rasterized candidates (737 pages vs. 77) — more content to visually transcribe for Ground Truth, a real but modest added selection-protocol cost, not a blocker.
- **Feasibility**: fully feasible, same reasoning as FSA.
- **Alternative candidate**: FSA, if the package-split-plus-rasterization *interaction* is specifically desired as a future, separately-scoped question — not recommended as this review's own primary choice (§8).

### 5.3 内閣官房 (CAS)

- **New axis covered**: file-scoped context (confirmed this pass across all 17 of its own files, not sampled).
- **Existing-case overlap**: superficial packaging-split similarity to case-004/MEXT (both split, both encrypted), but the *mechanism* is genuinely different — MEXT's own 4 files are each internally large (hundreds of pages) and exhibit page-to-page context lookback within each file; CAS's own 17 files are each small (1–29 pages) and exhibit **zero internal lookback**, because each file corresponds to exactly one bureau/item scope by construction. This is not a duplicate finding.
- **Expected information gain**: directly tests an open architectural question already flagged, unresolved, in the Case Package v0 concept design's own chat-side pre-schema review (context-relation vs. interpretation-requirement provenance split) — specifically whether a third context-requirement value (`file-scoped`) is needed alongside `page-local` and `neighbor-page-bounded`.
- **Falsification value**: falsifies any assumption that "context requirement" is always a page-count-bounded property; a file-scoped case cannot be represented by any finite page-distance value, only by a package-topology-aware rule.
- **Methodological risk**: selection-protocol design must decide *which of the 17 files* constitutes the selection universe (an added protocol decision beyond case-001–005's own single-file universe choice, though structurally analogous to choosing an organization within a combined file). One file (`r6_02`, 総務課) already shows the exact `010 内閣官房/010 内閣官房共通費/①/01-95/...` opening template already observed in case-002–005 — this is disclosed prior exposure that a future selection protocol would need to handle honestly, exactly as case-005's own protocol did for its own prior-exposure disclosure.
- **Feasibility**: fully feasible.
- **Alternative candidate**: none in this census shares the confirmed file-scoped mechanism; CAO (§5.6) is the closest structural analog but its own context mechanism is unverified, not a confirmed alternative.

### 5.4 裁判官弾劾裁判所 (Dangai) and 5.5 裁判官訴追委員会 (Sotsui)

Treated together since both are candidates for the same axis (cross-reference-summary, smallest possible instance) and both are 8–9-page documents.

- **New axis covered**: cross-reference-summary as a *primary* selection target (rather than case-005's own incidental observation).
- **Existing-case overlap**: direct mechanism overlap with case-005/MLIT (both cross-reference-summary), but case-005 never selected a row *from* the cross-reference-summary structure itself — its own selected row is a standard 明細表 row. A dedicated case here would be the first to select a row from within the 総表's own split-subcolumn structure.
- **Expected information gain**: tests whether the current normalizer/evaluator architecture (built around the standard three-column triple) can even represent the cross-reference-summary's own two-part amount split without modification — a genuinely untested question.
- **Falsification value**: moderate — falsifies an implicit assumption that "amount structure" is always a single three-column triple.
- **Methodological risk — 裁判官訴追委員会-specific**: this authority's own source status has a documented, more complex history than any other candidate in this census (§9 and the Acquisition Difficulty Memo): its site hosts **both** an in-scope request-stage document and an out-of-scope enacted-budget-stage document at different URLs, and the request-stage document was only found after an initial wrong-stage acquisition. A future selection protocol for this authority would need to explicitly re-verify and disclose which document is being used, a materially higher provenance-ambiguity risk than 裁判官弾劾裁判所's own single, unambiguous document.
- **Feasibility**: fully feasible for both; 裁判官弾劾裁判所 is the lower-risk of the two given its cleaner acquisition history.
- **Alternative candidate**: neither is included in this review's own final five (§14) — 裁判所's own embedded 重要政策推進枠要望額総表 section (§13) offers a plausible route to the same test as a byproduct of a case already justified on other grounds.

### 5.6 内閣本府 (CAO)

- **New axis covered**: extreme-split package model (~50 files) — **but only the package-model axis is actually confirmed**; the context mechanism at this granularity is explicitly unverified (only 2 of ~50 files have been individually inspected, per the census's own disclosure).
- **Existing-case overlap**: package-split-family overlap with CAS (§5.3), but at roughly 3x the file count.
- **Expected information gain — genuinely uncertain, not merely "high" by assumption**: the real, interesting question this review's own re-examination surfaces is whether CAO's own finer-granularity split still guarantees "exactly one item per file" (as CAS's own 17 files cleanly did) or whether some of CAO's own ~50 files, being smaller divisions, might bundle *multiple* items into one file — which would **reintroduce page-level context within an otherwise file-scoped package**, a genuinely different and currently *unknown* finding. This is a real, well-posed hypothesis, but it is **unverified**, and the originating task's own instruction restricts additional inspection to facts indispensable for *comparison*, not for resolving open empirical questions themselves. This review does not resolve it.
- **Falsification value**: conditionally high (if the "exactly one item per file" assumption breaks down) but currently unconfirmed — the case's own value is speculative until a source survey actually inspects more of the ~50 files.
- **Methodological risk**: **the highest current evidence deficit of any candidate in this review** (`familyConfidence: medium`, package model confirmed but context mechanism explicitly `not yet characterized` in the census's own CSV). Selecting CAO as Case-006+ without further prior inspection risks discovering, only after selection-protocol work has begun, that its own context mechanism is identical to CAS's (making the case redundant) or that its own selection-universe definition is unexpectedly complicated by uneven file granularity.
- **Feasibility**: feasible as a case, but the case's own *research value* is less certain than any other candidate in this review.
- **Alternative candidate**: none directly, but this review recommends treating CAO's own inclusion as **explicitly exploratory / lower-confidence** rather than assuming it a priori deserves a fixed slot (§15).

### 5.7 厚生労働省 (MHLW)

- **New axis covered**: scale (largest document in the census, 1,723 pages) — retained, not dropped.
- **Existing-case overlap**: shares the cross-reference-summary mechanism with case-005/MLIT/6 other authorities (not a novel axis on its own); shares the embedded-box mechanism with MEXT/MOF/MLIT (confirmed via this review's own spot-check, §13 — a **4th** independent confirmation, corroborating rather than uniquely justifying selection).
- **Expected information gain**: primarily a scale stress-test — does the context-recovery architecture (and any future PDF→MOF linkage work) hold at real, maximal document size within this census's own population; secondarily corroborates the embedded-box mechanism at a 4th ministry.
- **Falsification value**: moderate — tests whether findings established on smaller-to-medium documents (case-001–005's own largest is MEXT at 1,339 pages) generalize to a materially larger one.
- **Methodological risk**: this authority also separately hosts 10+ narrative/policy-evaluation files (already acquired) that are NOT the ledger — a future selection protocol must be careful to select from the correct, already-identified ledger file (`05-1b-01.pdf`), not from the narrative files, a risk this census's own acquisition history (§9) already flags explicitly.
- **Feasibility**: fully feasible; the correct file is already identified and locked.
- **Alternative candidate**: none shares MHLW's own combination of scale + confirmed embedded-box presence; 裁判所 (§5.8) is a genuinely different, cheaper candidate for embedded-substructure specifically, not a scale substitute.

### 5.8 裁判所 (Courts) — added candidate

- **New axis covered**: **embedded-substructure as a primary target, with multiple distinct sub-types confirmed in one compact document** — this review's own minimal spot-check (§13) found, within Courts' own single 127-page combined file: (1) the standard 明細表 ledger (the large majority of the document), (2) an embedded `令和６年度概算要求定員表` (staffing/personnel request table, unit `人`, entirely different columns — flanked by 2 blank separator pages), and (3) an embedded `令和６年度重要政策推進枠要望額総表` (a policy-priority-framework summary table carrying its **own** cross-reference-summary mechanism, i.e. a `明細書頁数` column, structurally similar to the family already seen in 7 other authorities but embedded as a *sub-section* here rather than being the document's own primary structure).
- **Existing-case overlap**: the standard-ledger portion overlaps with case-002/003's own coverage; the two embedded sections do not overlap with any existing case.
- **Expected information gain**: the highest per-page information density of any candidate reviewed here for the embedded-substructure question — three structurally distinct grammars confirmed within roughly 1/14th of MHLW's own page count, at zero encryption and a single, simple package model (no split-package confound at all).
- **Falsification value**: high, and cheap to obtain — directly tests whether a selection protocol and evaluator built around one grammar can even correctly *classify* which grammar a given page belongs to, a precondition question this census's own evidence (the header-ratio exceptions in the checkpoint's own §3.4.1) already suggests is non-trivial even before any row is selected.
- **Methodological risk**: lower than MHLW's — smaller document, no package-split confound, single unambiguous source. The main open risk is which of the three embedded sections (or the standard ledger itself) should be the *primary* selection target — this is a genuine, disclosed design decision for a future selection protocol, not resolved here.
- **Feasibility**: fully feasible; the source is already acquired and locked.
- **Alternative candidate**: MHLW remains the alternative if scale-plus-embedded-box (rather than grammar-boundary diversity) is the priority — see §13's own explicit trade-off framing.

## 6. New-axis coverage summary

| New axis | Best-evidenced representative | Confidence |
|---|---|---|
| Zero-text-layer representation | 法務省 (isolated) or 金融庁 (confounded with split) | High for both; MOJ cleaner |
| File-scoped context | 内閣官房 | High — all 17 files checked |
| Extreme-split package (context mechanism unverified) | 内閣本府 | Low — package model only |
| Embedded-substructure, multiple grammars, primary target | 裁判所 | High — directly confirmed this review |
| Scale (largest document) | 厚生労働省 | High |
| Cross-reference-summary as primary target | 裁判官弾劾裁判所 or 裁判官訴追委員会 | Medium — not selected in this review's own final five (§14) |

## 7. Existing-case overlap (consolidated)

No recommended candidate in §15 fully duplicates an existing case-001–005 axis combination. The closest overlaps are: MHLW's own cross-reference-summary presence (shared with case-005, but MHLW is not being selected *for* that mechanism); Courts' own standard-ledger majority content (shared with case-002/003, but Courts is not being selected *for* that portion). Both overlaps are disclosed, not treated as disqualifying, since each candidate's *primary* justification is a genuinely uncovered axis value.

## 8. FSA vs. MOJ — the required re-examination

Both candidates share the rasterized-no-text-layer representation, directly confirmed via `pdffonts`/`pdftotext`/visual render for both. The census's own explicit finding that 公正取引委員会 (jftc) shares FSA's own DocuWorks producer *but has a full text layer* is the reason producer identity must never be treated as the family boundary — this finding applies equally regardless of which of FSA/MOJ is chosen, so it does not itself favor one over the other. The deciding factor is **axis isolation**: FSA is simultaneously rasterized AND a 12-file split (the 2nd-most granular package in the census), so a benchmark result from FSA cannot cleanly attribute any finding to rasterization alone. MOJ is a single combined file, isolating the representation axis without a package-split confound. **This review recommends MOJ** as the primary rasterized-family representative, with FSA retained as a documented alternative for a future, separately-scoped case that specifically wants to study the *interaction* of rasterization and package fragmentation.

## 9. 内閣官房 — required re-examination against zero-or-one-page-back

Already addressed in depth in §5.3 and in the checkpoint's own §3.4.3: CAS's own file-scoped mechanism is categorically different from MEXT's own zero-or-one-page-back mechanism, not a variant of it. The key distinguishing test: within a MEXT-style split file, item-header context can still be *lost* across a page boundary (as case-004's own diagnostics found for ~half of sampled boundaries); within a CAS-style file, item-header context is established once and **cannot** be lost, because the file itself has no further internal item boundary to lose context across. This is a genuinely different failure/success mode for any future extraction/normalization strategy to handle, not a restatement of an existing finding.

## 10. 内閣本府 — required re-examination of whether ~50 files is a real design challenge

Addressed fully in §5.6. This review's own conclusion, stated plainly: **it is not yet known** whether CAO's own extreme split meaningfully differs in mechanism from CAS's own 17-file split, or is simply the same mechanism at a larger file count. The census's own evidence (`familyConfidence: medium`, `contextDependencyObserved: unknown`) does not currently support treating CAO as a *confirmed* new-mechanism case; it supports treating it as a **plausible, unconfirmed** one. This review's own recommendation (§15) reflects that lower confidence explicitly, rather than asserting CAO as a settled priority.

## 11. 厚生労働省 — required re-examination of scale vs. embedded-substructure value

Addressed in §5.7 and reframed by §13's own Courts finding: MHLW's own *scale* value stands on its own evidence (the census's own largest document) independent of the embedded-box question. Its own embedded-box mechanism, now confirmed via this review's own spot-check to be a genuine 4th instance (not merely inferred by analogy), corroborates the census's own broader embedded-box finding but is **not** MHLW's own most distinguishing property once Courts is available as a cheaper, richer embedded-substructure representative. This review's own recommendation retains MHLW specifically *for scale*, not for embedded-substructure primacy.

## 12. Cross-reference-summary — opportunity cost, required assessment

The cross-reference-summary mechanism now has **7 confirmed instances** in the census (mlit, env, caa, dangai, mhlw, sangiin, sotsui) — the most-replicated single finding in the whole census, more so even than the standard ledger grammar's own individual sub-features. Dedicating one of only 5 new-case slots to testing it as a *primary* target (via dangai or sotsui, the cheapest instances) would provide genuinely new information (§5.4/5.5's own analysis stands), but the **opportunity cost is comparatively low to forgo**, for two reasons: (1) the mechanism's own existence and structure is already very well-evidenced across 7 independent authorities, unlike the genuinely single-instance gaps (rasterization has exactly 2 candidates; file-scoped context has exactly 1 confirmed candidate; extreme-split has exactly 1 candidate); (2) Courts' own embedded `重要政策推進枠要望額総表` section (§13) offers a plausible route to testing this same mechanism as a *primary* target, as a byproduct of a case already justified for its own embedded-substructure value — a future selection protocol for Courts could choose to select its own target row from within that section specifically, rather than from the standard 明細表, without requiring a separate case. This review's own recommendation therefore does **not** allocate a dedicated slot to cross-reference-summary-as-primary (§15), while explicitly flagging 裁判官弾劾裁判所 as the cheapest possible Case-011+ candidate should this call prove wrong after Courts' own selection protocol is actually written.

## 13. Embedded-substructure candidate comparison — the required minimal spot-check

This review performed exactly two minimal, disclosed spot-checks against already-downloaded raw PDFs, to resolve the embedded-substructure candidate comparison the originating task explicitly requires (§6 of the originating instructions: "embedded region独自unit declaration等をprimary targetとして扱える候補をcensus evidenceから比較する"):

**Check 1 — Courts, page 116 (scan index) / PDF page 117**: content reads `令和６年度重要政策推進枠要望額総表` with a full `事項/前年度要望額/６年度要望額/対前年度比較増△減/明細書頁数/備考` column set — a cross-reference-summary-family section embedded within the same combined file that also carries the standard ledger and the already-known 定員表 section (from the checkpoint's own §3.4.1 investigation). **Result**: Courts' own single 127-page file contains at minimum three distinct structural sections, not one.

**Check 2 — MHLW, page 44 (scan index) / PDF page 45**: content reads `令和５年度国庫債務負担行為３年計画２年目` immediately preceding an independent `(単位：千円）` re-declaration — directly confirming the embedded-box mechanism already found in MOF and MLIT is also genuinely present in MHLW, not merely inferred from the mechanical unit-count pattern alone.

Both checks used only already-acquired, already-locked raw sources (`sources/raw/courts-fy2024-general-account-expenditure-request.pdf`, `sources/raw/mhlw-fy2024-general-account-expenditure-request-summary-detail.pdf`); no new source was fetched, and neither check selected or scored any row. **Conclusion**: Courts offers a materially cheaper (127 vs. 1,723 pages), unencrypted, single-package, higher-structural-density candidate for embedded-substructure primacy than MHLW; MHLW's own distinguishing value is best understood as scale, with its embedded-box mechanism as independent corroboration rather than unique justification.

## 14. Recommended five-case set

| Case | Authority | Primary axis | Secondary axis | Existing overlap | Information gain | Risk |
|---|---|---|---|---|---|---|
| 006 | 法務省 (MOJ) | Zero-text-layer representation | — | None | High (clean axis isolation) | Uniform-null benchmark result across all 3 engines (disclosed, not a blocker) |
| 007 | 内閣官房 (CAS) | File-scoped context | Bureau-granularity split (17 files) | None | High (open architecture question) | Selection-universe-file choice; disclosed prior exposure (r6_02) |
| 008 | 裁判所 (Courts) | Embedded-substructure, multiple grammars, primary target | Cross-reference-summary (byproduct opportunity) | Standard-ledger portion overlaps case-002/003 (not the selection target) | High (3 structures in 1 compact file) | Primary-target choice among 3 embedded sections; disclosed, not yet resolved |
| 009 | 内閣本府 (CAO) | Extreme-split package (~50 files) | — | Package-split family shared with 007, mechanism unconfirmed | **Speculative** — genuinely unknown until surveyed further | Highest evidence deficit of the five; case may turn out redundant with 007 |
| 010 | 厚生労働省 (MHLW) | Scale (largest document, 1,723 pages) | Embedded-box mechanism (4th confirmed instance) | Cross-reference-summary shared with case-005 (not the selection target) | Medium-high (scale stress-test) | Must select from the correct ledger file, not the authority's own 10+ narrative files |

## 15. Coverage matrix

| Axis | 006 MOJ | 007 CAS | 008 Courts | 009 CAO | 010 MHLW |
|---|---|---|---|---|---|
| Raster representation | ✅ primary | | | | |
| Context lifetime (file-scoped) | | ✅ primary | | ? unconfirmed | |
| Package topology (extreme split) | | ✅ secondary (17-file) | | ✅ primary (~50-file) | |
| Embedded substructure | | | ✅ primary (3 types) | | ✅ secondary (1 confirmed type) |
| Cross-reference summary | | | ✅ possible byproduct | | (present, not selection target) |
| Scale | | | | | ✅ primary |
| Institutional diversity | | ✅ (内閣官房) | ✅ (裁判所, judiciary) | ✅ (内閣府) | |
| Alternate grammar boundary | | | ✅ (定員表 vs. standard) | | |

No axis is left entirely uncovered by the five-case set except "extreme-split's own true context mechanism," which is the explicit, disclosed open question Case-009 itself exists to resolve.

## 16. Recommended execution order

Case numbers here carry a genuine dependency rationale, not merely sequence:

1. **006 (法務省)** first — resolves, before any further selection work, whether the current benchmark's own scoring/evaluation architecture can even represent a "zero engine output" case meaningfully (a pipeline-applicability boundary question). If this reveals the evaluator itself needs a new check category (e.g., distinguishing "engine produced a wrong answer" from "engine produced nothing"), that finding should inform how **010 (MHLW)**'s own much-larger-scale case is evaluated later.
2. **007 (内閣官房)** second — establishes whether the Case Package v0 concept design's own open context-requirement question needs a third value before **009 (内閣本府)** is attempted, since 009's own value depends on comparing against 007's own confirmed file-scoped baseline.
3. **008 (裁判所)** third — a self-contained, low-risk case; its own selection-protocol decision (which embedded section to target) does not depend on 006/007's own outcomes, but completing it before 009/010 keeps the lower-risk cases earlier.
4. **009 (内閣本府)** fourth, explicitly **after** 007 — its own research value is best interpreted relative to 007's own already-confirmed file-scoped mechanism; attempting 009 first would mean not yet having a baseline to compare its own findings against.
5. **010 (厚生労働省)** last — the highest-page-count case, benefiting from whatever evaluator/architecture refinements 006–009 may have already surfaced, and serving as a final, large-scale stress test.

This is not a requirement to complete all five before Ground Truth work begins on any of them — each case still follows its own protocol-then-selection-then-Ground-Truth sequencing independently, per case-001–005's own established methodology.

## 17. Rejected/deferred candidates and why

- **金融庁 (FSA)**: deferred in favor of MOJ (§8) due to the rasterization/package-split confound; retained as a documented alternative for a future, separately-scoped interaction study.
- **裁判官弾劾裁判所 / 裁判官訴追委員会**: deferred from the primary five (§12/§14) given the comparatively low opportunity cost of forgoing a dedicated cross-reference-summary-primary case, and Courts' own byproduct opportunity; 裁判官弾劾裁判所 specifically is flagged as the cheapest possible future Case-011 candidate if this call proves wrong.
- **公正取引委員会**: considered only as a negative-control reference for the FSA/MOJ rasterization comparison (§8), not as a selection candidate — it does not represent any currently-uncovered axis on its own.

## 18. Remaining uncertainty

- **内閣本府's own true context mechanism** at ~50-file granularity remains genuinely unknown; Case-009's own value is contingent on what a future source survey actually finds, not confirmed by this review.
- **Courts' own primary-target choice** among its three identified structural sections (standard ledger, 定員表, 重要政策推進枠要望額総表) is not resolved here — a future selection protocol for Case-008 must make and justify that choice.
- **Whether MOJ's own uniform-null benchmark result would require an evaluator change** (e.g., a new check category distinguishing "no engine output at all" from "wrong output") is a real, open methodological question this review flags but does not resolve.
- **Whether Courts' own embedded 重要政策推進枠 section can actually substitute for a dedicated cross-reference-summary-primary case** (§12's own load-bearing assumption) is itself unverified until Case-008's own selection protocol is actually written — if that section turns out unsuitable as a primary target for some undiscovered reason, the opportunity-cost argument in §12 would need to be revisited, and 裁判官弾劾裁判所 would become the fallback.

## 19. What must be frozen before Case-006 starts

Per the originating task's own explicit deferral: this review recommends, but does not freeze, the five-case set (§14) or the execution order (§16). A future, separate task should freeze: the exact five chosen authorities; the rationale for each (this review's own §5 analysis, or a revised version of it); the rejected alternatives and why (§17); any known prior exposure (e.g., CAS's own `r6_02` template, already disclosed here); and the execution ordering rationale (§16) — mirroring the same freeze discipline already used for every selection protocol in case-001–005.

---

**No Case-006 source survey, row selection, Ground Truth, benchmark run, parser change, MOF linkage, or production adaptation was performed.**
