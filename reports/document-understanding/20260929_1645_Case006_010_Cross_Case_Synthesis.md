# Case-006–010 Cross-Case Synthesis / Batch Transition Analysis

Date: 2026-09-29 (Asia/Tokyo)
Basis: committed frozen evidence on `main@10cd45a29a080f64280ab46fb05763adb31e41b3`

## 1. Executive summary

This synthesis audits the completed Case-006–010 individual pilot sequence without adding a source inspection, Ground Truth, benchmark, OCR experiment, or adaptation. The five cases are purposive stress cases, not a random or prevalence-representative sample.

The evidence supports **GO WITH GUARDRAILS** toward a future Batch Experiment Protocol, with a first batch aimed at **benchmark comparability**, not broad semantic coverage. The shared stage order, provenance controls, deterministic selection discipline, NULL preservation, Ground Truth independence, unchanged engine set, and per-authority reproducibility artifacts are ready to be proposed as global rules. Source representation, package topology, grammar universe, context resolution, unit scope, and embedded-structure boundaries remain authority-specific preflight inputs.

Case-007 is the decisive counterexample to treating the existing single-row C1–C4 model as universal: its request/expense row is not the printed amount-bearing row, and a variable-depth descendant subtree cannot be silently summed or arbitrarily selected. It is therefore a first-class NULL result, not missing benchmark data.

## 2. Scope and non-goals

This is a read-only synthesis of committed Case-006–010 artifacts plus new synthesis/report/state artifacts. It does not freeze a Batch Protocol, select Batch-001 authorities, acquire or render sources, create or change Ground Truth, run extraction or `docbench`, run OCR, modify parser/normalizer/evaluator code, or begin Case-011.

## 3. Pilot-selection caveat

The Case-006–010 Selection Freeze deliberately selected different stress axes: representation (006), file-scoped/deep hierarchy (007), multi-grammar (008), extreme package split (009), and scale (010). Counts below always use the five-pilot or four-benchmarked-pilot denominator. They do not estimate the prevalence of any property across Japanese authorities.

## 4. Artifact and provenance inventory

| Case | Committed chain | GT / benchmark status | Closeout or equivalent |
|---|---|---|---|
| 006 MOJ | survey `b4a9cd2` → protocol `7ef2250` → selection `e2253ee` → GT `952a0c1` → benchmark `91b6b51` | GT + benchmark present | `20260928_0827_Case006_MOJ_Closeout.md` |
| 007 CAS | survey `211213c` → protocol `2cc0821` → NULL selection `f530846` → structural review `3402173` | no GT; `not_benchmarked` | `20260928_1755_Case007_NULL_Result_Structural_Review.md` |
| 008 Courts | survey `e10d56c` → protocol `3cf4a4f` → selection `0ccea62` → GT `55bda23` → benchmark `ec69188` | GT + benchmark present | `20260928_2019_Case008_Closeout.md` |
| 009 CAO | survey `e640dc2` → protocol `d42b7b8` → selection `985f77e` → GT `0d238d2` → benchmark `199ef50` | GT + benchmark present | `20260928_2220_Case009_Closeout.md` |
| 010 MHLW | survey `cc5115b` → protocol `2f910f2` → selection `4b98ace` → GT `ce98519` → benchmark `e6d17e` | GT + benchmark present | `20260929_0824_Case010_Closeout.md` |

All named artifacts were read directly. The accompanying [machine-readable synthesis evidence](../../evidence/document-understanding/case-006-010-cross-case-synthesis.json) retains case facts separately from cross-case inference. Case-007 has no GT/result JSON by design, not by omission.

## 5. Cross-case master matrix

| Case | Source / package / representation | Grammar and context | Selection / GT | Benchmark and earliest demonstrated issue |
|---|---|---|---|---|
| 006 MOJ | Locked 737-page single PDF; exhaustive zero text; sampled vector paths, no fonts/images | ledger + summary + staffing; page-level `千円` on target | first standard-ledger row after two aggregates; visual GT, arithmetic PASS | pdf.js 2/11 / PyMuPDF 2/11: representation/text extraction; Docling 2/11: OCR signal then table/grid association |
| 007 CAS | Locked detail file within official split package; native text | organization file-scoped; item blocks can continue; deep hierarchy | all 14 rows in 2 pages assessed; NULL | not benchmarked; request/expense rows fail same-row triple, descendants are not source-uniquely attributable |
| 008 Courts | Locked 127-page single native-text PDF | ledger + staffing + policy sections; section/local units | standard-ledger-only physical row; visual GT, arithmetic PASS | pdf.js 10/11 / PyMuPDF 10/11: candidate resolution; Docling 3/11: grid/row association |
| 009 CAO | 51-PDF official package / 394 pages; native-text detail starts | file-opening division scope; file identity context-bearing; order not shown necessary | existing locked `1.pdf` only; visual GT, arithmetic PASS | pdf.js 10/11 / PyMuPDF 10/11: candidate resolution; Docling 8/11: item/table-row association |
| 010 MHLW | Locked 1,723-page single native-text PDF | summary + large ledger; remarks-side embedded structures/local units | main-ledger-only row; visual GT, arithmetic PASS | pdf.js 10/11 / PyMuPDF 10/11: candidate resolution; Docling 3/11: table/row association |

Confirmed fact: all four benchmarked cases preserved first-run evidence and an unchanged-condition reproducibility comparison. Interpretation: this demonstrates an available per-authority reproducibility procedure for these pilots; it is not proof that all future authorities will be deterministic.

## 6. Four-axis model reassessment

The four axes remain necessary and independent:

1. **Document/layout family:** standard-ledger shape can coexist with summary, staffing, policy, or embedded tables (006, 008, 010); CAS shows a deep hierarchy inside a ledger family (007).
2. **Source representation:** MOJ’s vector-outline/no-text condition differs categorically from native-text pilots (006 versus 007–010).
3. **Package model:** one file (006/008/010), a split CAS package, and 51 scoped CAO files (009) require different provenance handling.
4. **Context mechanism:** row/same-page/section/file scope cannot be inferred from layout or package count alone.

**Refinement:** canonical-byte source admissibility is best treated as a cross-cutting methodological constraint, rather than a fifth document-property axis. Case-009 proves why: 49 temporary official survey snapshots supported package facts, but only already-locked `1.pdf` was suitable as the GT-grade selection source. Package membership and canonical-byte eligibility are distinct.

## 7. Selection and GT process findings

The following are strong global-invariant candidates for a benchmark-comparability batch:

- freeze source universe, eligibility, context rules, ambiguity handling, tie-break, and stop rule before candidate enumeration;
- select by document order and stop at the first fully eligible physical row;
- require source-visible association, not arithmetic reconstruction or inherited values;
- preserve ambiguity as FAIL and preserve a NULL result as a result;
- do not transcribe amounts during selection;
- create GT only after selection, from direct source evidence, independently transcribe values/sign, then validate arithmetic;
- keep raw source, raw engine output, normalized output, GT, and evaluation separate.

The C1–C4 single-row profile is not globally established. It worked for 006/008/009/010, but Case-007 demonstrates a structural counterexample: the semantic request/expense header and the amount-bearing descendant are different physical rows; the relation is variable-depth and not source-unique. A future coverage-oriented semantic batch would need a separately designed multi-row GT model, not a relaxed version of the comparability protocol.

## 8. Benchmark matrix and failure taxonomy

| Failure class | Observed evidence-bounded mapping |
|---|---|
| representation / no text signal | Case-006 pdf.js and PyMuPDF |
| OCR/signal then table reconstruction | Case-006 Docling (pre-existing RapidOCR behavior, not a separate experiment) |
| candidate resolution | Cases 008/009/010 pdf.js and PyMuPDF |
| table/grid / row association | Case-008 Docling (3/11), Case-009 Docling (8/11), Case-010 Docling (3/11) |
| structural inapplicability of single-row model | Case-007 NULL before GT/benchmark |

In **3/3 native-text benchmarked pilots** (008–010), both flat-text engines received the target page, retained the correct item among candidates, and recovered target expense/triple data while failing unique item resolution, each scoring 10/11. This is a bounded recurring pattern, not a guarantee for a future authority.

Docling should not be summarized as “weak.” Across the observed pilots it reaches different structural failure states: Case-006 has OCR-recovered signal but malformed grid association; Case-008 forms no usable expense candidate; Case-009 retains expense/triple but not target item relationship; Case-010 fails earlier in target item/expense row formation. The common family is structural association, not an established identical cause.

## 9. Negative findings and evaluator observations

The following are `not_demonstrated`, not falsified general claims:

- Case-008: staffing/policy grammars causally interfered with its frozen ledger target.
- Case-009: the 51-file package/file identity caused its frozen target benchmark failure.
- Case-010: 1,723-page scale caused the benchmark failure.
- Case-010: remarks-side embedded structures caused Docling’s failure.

The 11-check evaluator remains usable for the single-row benchmark-comparability scope: it distinguishes candidate presence from exact unique resolution and records field/relationship misses. It does not encode earliest failure layer, source applicability, section identity, or the Case-007 structural mismatch. These are RED future-design requirements, not changes made here.

## 10. Batch-readiness matrix

| Topic | Status | Supporting evidence / limitation | Batch Protocol input |
|---|---|---|---|
| canonical source bytes and SHA | GREEN | all pilots relied on locks; 009 separates survey snapshot from canonical source | lock identity and rehash requirement |
| stage order and layer separation | GREEN | every completed chain preserves survey→protocol→selection→GT→benchmark | mandatory stage gate |
| source representation detection | YELLOW | 006 differs categorically | authority preflight classification |
| package discovery / file identity | YELLOW | CAS/CAO prove package-specific scope | authority package profile |
| grammar segmentation | YELLOW | 006/008/010 contain mixed structures | frozen authority universe/exclusions |
| organization and item context | YELLOW | page, section, and file scopes differ | authority context order |
| unit scope | YELLOW | page/section/file-opening/embedded-local forms occur | authority unit rule and boundary rule |
| main row vs embedded structure | YELLOW | 010 and 008 require boundaries | structural profile and exclusions |
| single-row C1–C4 model | RED | 007 counterexample | comparability-only inclusion gate; no semantic extension yet |
| document-order tie-break and stop | GREEN | selected cases stopped at first full pass | global deterministic rule |
| ambiguity and NULL preservation | GREEN | 007 preserved NULL; all protocols reject ambiguity | global failure-safe rule |
| direct visual GT / arithmetic-last | GREEN | GTs 006/008/009/010 | global GT discipline |
| existing engine set and evaluator | GREEN for comparability; RED for semantic coverage | consistent engines/checks; provenance absent from score | fixed baseline plus separate analysis fields |
| per-authority failure isolation | GREEN candidate | case-local artifacts permit NULL/failure without losing other cases | independent authority manifests/results |
| batch summary generation | YELLOW | synthesis evidence provides an initial shape only | stable authority result schema |

## 11. Architecture and Batch-001 goal alternatives

| Architecture | Assessment from pilot evidence |
|---|---|
| Fully uniform protocol | viable only if it intentionally records structural mismatches as NULL; Case-007 prevents treating it as universal semantic coverage |
| Shared framework + authority preflight profile | **recommended**: preserves comparability while freezing source/package/grammar/context/unit facts per authority |
| Structural-family profiles | promising future refinement, but profiles are not yet mature enough to define GT semantics for deep hierarchy |

**Recommended Batch-001 primary goal: A — baseline benchmark comparability.** It maximizes reproducibility, GT independence, cross-authority comparability, and failure diagnosability while retaining NULL as an honest outcome. Goal B requires new semantic record definitions; a two-track design should not be frozen until those definitions and evaluator applicability are separately designed.

## 12. Parallelization, size, and sampling guidance

Authorities may perform Source Surveys in parallel. For each authority, the causal sequence remains serial: `Survey → Protocol → Selection → GT → Benchmark`. Cross-authority aggregation begins only after each included authority has a frozen local artifact. This failure-isolated structure allows one source error, NULL selection, GT ambiguity, or benchmark runtime failure to be preserved without blocking other authorities.

Recommend an initial **5–8 authority operational pilot batch**, not a population-representative sample size. Five is maximally reviewable; eight provides useful failure diversity without weakening direct-GT auditability. Selection should be deterministically stratified using predeclared census representation/package/context factors, not “likely easy” sources. No authority list is selected here.

## 13. GO WITH GUARDRAILS verdict and Batch Protocol inputs

**Verdict: GO WITH GUARDRAILS.** G1 provenance, G3 deterministic selection, G4 NULL preservation, G5 GT independence, G6 unchanged baseline execution, G8 failure isolation, and G9 reproducibility have workable pilot evidence. G2 preflight and G10 reviewability require authority manifests and bounded batch size. G7 must preserve a narrative/structured earliest-failure analysis because score alone is insufficient.

The next Batch Experiment Protocol should propose, but this report does not freeze:

- **Global candidates:** source locking/rehash; stage order; raw/normalized/GT separation; GT after selection and before benchmark; deterministic tie-break/stop; ambiguity→FAIL; NULL preservation; unchanged engine set; artifact provenance and reproducibility comparison.
- **Per-authority parameters:** canonical source/package member; grammar universe/exclusions; organization/item context order; unit scope; structural profile; allowed lookback; representation/applicability status.
- **Do not freeze yet:** deep-hierarchy semantic aggregation; descendant arithmetic; profile-specific GT semantics; evaluator extensions; a claim that one profile covers all authorities.

## 14. Deferred research, integrity, and next task

Deferred: candidate-resolution adaptation, Docling reconstruction studies, a deep-hierarchy semantic-record design, evaluator provenance extensions, and any Batch-001 execution. No frozen artifact was modified. The intended changes in this task are only this report, its JSON evidence, and state files.

Recommended next task: **Batch Experiment Protocol Freeze**, using this synthesis as input and retaining every listed guardrail. Do not select authorities or execute Batch-001 until that protocol is separately frozen.

**Case-006–010 Cross-Case Synthesis is complete. The pilot evidence supports moving toward batch-scale authority processing only with explicit guardrails: source/grammar/context preflight remains per-authority, NULL outcomes remain first-class results, and the Case-007 deep-hierarchy structure must not be silently forced into the single-row benchmark model. No Batch Protocol was frozen and no Batch-001 authority was selected or processed in this task.**
