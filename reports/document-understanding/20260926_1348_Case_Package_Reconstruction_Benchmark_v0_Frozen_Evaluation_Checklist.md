# Case Package Reconstruction Benchmark v0 — Frozen Evaluation Checklist

Status: **frozen before inspecting any reconstruction output.**

Date: 2026-09-26 (Asia/Tokyo)

This checklist is Artifact 2 of the benchmark. It was built from canonical repository evidence (fixture READMEs, selection protocol/record, Ground Truth evidence documents, benchmark reports, `state/CHANGELOG.md`, Git history) available to the evaluator, not to the reconstruction model. It is frozen before either reconstruction run's output is inspected, and is not edited afterward based on what the model did or did not say. Ground Truth (target-row amount/name/delta values) is deliberately excluded from this checklist — this benchmark evaluates reconstruction of *research history*, not target-row value extraction.

Each item has a checklist ID, a research-question dimension (1 Identity, 2 Method, 3 Result, 4 Temporal, 5 Epistemic, 6 Open-work), and the exact fact expected. "Supported by" cites which supplied-file element should let a faithful reconstruction recover it, for later grading of A/B/C/D/E representation diagnosis.

## case-001 checklist

| ID | Dim | Expected fact | Supported by |
|---|---|---|---|
| C1-01 | 1 | Source is `digital-r6-request-table-01`, デジタル庁 (Digital Agency), FY2024 request-stage document | identity block |
| C1-02 | 1 | Target location: PDF page index 11, printed page label "8" | identity block |
| C1-03 | 1 | Total page count, PDF producer, orientation are NOT recorded in the supplied files | sourceSafeProfile `pageCount`/`pdfProducer`/`pageOrientation` = not_recorded |
| C1-04 | 2 | Three engines were used/tried: pdfjs-baseline, pymupdf-baseline, docling | engineDerivedProfile `rawExtractionSucceeded`, case001-e03/e05 |
| C1-05 | 2 | A dedicated Docling-specific normalizer was added, with two named general rules (CJK wrap-space closing, numeric-token reversal) | case001-e05 |
| C1-06 | 3 | Important success: Docling's table-cell separation resolved the expense-name two-column conflation that both flat-text engines failed | case001-e06, engineDerivedProfile `doclingCellSeparationResolvedExpenseNameConflation` |
| C1-07 | 3 | Important failure: header-row hierarchy ambiguity — item_name_exact_match FAILs for all 3 engines | case001-e04/e11, sourceSafeProfile `headerRowHierarchyAmbiguityPresent` |
| C1-08 | 3 | Important failure: page-level unit label ('千円') absent on target page — unit_exact_match FAILs for all 3 engines | case001-e04/e13, sourceSafeProfile `pageLevelUnitLabelPresentOnTargetPage=false` |
| C1-09 | 3 | Docling failed to recover requestNo for this row (null) | case001-e12, engineDerivedProfile `requestNoRecoveredByDocling=false` |
| C1-10 | 4 | Two distinct historical scores exist for the same underlying benchmark: pre-Docling (pdfjs 8/11, pymupdf 8/11) and post-Docling-integration (pdfjs 8/11, pymupdf 8/11, docling 9/11) — reconstructions are not required to separate these two but must not claim only one engine set existed throughout | case001-e04 vs case001-e06 |
| C1-11 | 4 | The evaluator's glyph check was renamed twice: `raw_delta_glyph_preserved` → `delta_glyph_observed_and_associated` (case001-e07, superseded) → `delta_sign_evidence_matches_source` (case001-e09, current) | case001-e07/e09, relatedEvents supersedes/superseded_by |
| C1-12 | 4 | case-001's final scores (8/11, 8/11, 9/11) are UNCHANGED by the evaluator correction — this must be reported as "unchanged," not omitted or misreported as "improved" | case001-e10, engineDerivedProfile `finalScores` |
| C1-13 | 5 | The correction is classified as a `methodology_correction`, not an extraction/normalization bug — reconstruction should not conflate it with case001-e05/e06's engine-behavior findings | case001-e09 |
| C1-14 | 5 | case001-e07 has `status: superseded`; case001-e09 has `status: current` — reconstruction should reflect this status distinction, not present both as equally live | case001-e07/e09 |
| C1-15 | 6 | Three open/unresolved items exist: header-row hierarchy ambiguity, Docling requestNo recovery, page-level unit-label lookup — none should be presented as resolved | case001-e11/e12/e13, all `status: open` |
| C1-16 | 6 | No `case-003`, no strategy-selection system, and no LLM-retrieval mechanism exists yet for case-001 — a faithful reconstruction must not claim these exist | absence in both files |

## case-002 checklist

| ID | Dim | Expected fact | Supported by |
|---|---|---|---|
| C2-01 | 1 | Source is `meti-fy2024-general-account-request`, 経済産業省 (METI), FY2024 request-stage document | identity block |
| C2-02 | 1 | Target location: PDF page index 8, printed page label "経(本) 5" | identity block |
| C2-03 | 1 | Source-safe PDF metadata IS recorded: 106 pages, Producer "List Creator", A4 landscape, not encrypted | sourceSafeProfile `pageCount`/`pdfProducer`/`pageOrientation`/`encrypted` |
| C2-04 | 2 | Acquisition required a two-step chronology: plain fetch failed (AWS WAF JS challenge, HTTP 202) → a Playwright/Chromium-based tool was built and succeeded | case002-e02 → case002-e03, relatedEvents "resolves" |
| C2-05 | 2 | Selection was preregistered (protocol frozen) BEFORE the source was even acquired — a stronger discipline than case-001, which had no such protocol | case002-e01 |
| C2-06 | 2 | Ground Truth was frozen by direct visual inspection, still before any of the three engines was run | case002-e06 |
| C2-07 | 3 | The first frozen benchmark run scored pdfjs-baseline 2/11, pymupdf-baseline 3/11, docling 2/11 | case002-e07 |
| C2-08 | 3 | Important failure: the flat-text triple-parsing regex broke because an annotation column followed the amount triple on the SAME line (unlike case-001, where it only ever appeared on continuation lines) | case002-e08 |
| C2-09 | 3 | Important failure: Docling produced a coarser/misaligned grid and silently selected a wrong row with no ambiguity signal (`itemCandidateCount: 1`) — a worse failure mode than the flat-text engines' honest nulls | case002-e10 |
| C2-10 | 3 | Important success/contrast: the page-level unit label ('千円') WAS present and WAS recovered by all 3 engines here, unlike case-001 | case002-e05, sourceSafeProfile `pageLevelUnitLabelPresentOnTargetPage=true`, engineDerivedProfile `finalScores` context |
| C2-11 | 4 | **Critical temporal test**: the ORIGINAL first-frozen scores were 2/11, 3/11, 2/11 (case002-e07) | case002-e07 |
| C2-12 | 4 | **Critical temporal test**: the CORRECTED/current scores are 3/11, 4/11, 3/11 (case002-e14), exactly +1 per engine over the original | case002-e14, engineDerivedProfile `finalScores` |
| C2-13 | 4 | **Critical temporal test**: both scores must be preserved — a reconstruction reporting ONLY 3/11-4/11-3/11 without noting the original 2/11-3/11-2/11 is incomplete; a reconstruction treating 2/11-3/11-2/11 as still currently valid (without the correction) is also incomplete | case002-e07 (status: current, historical) vs case002-e14 (status: current, supersedes scoring of e07) |
| C2-14 | 5 | The defect (case002-e12, `status: resolved`) is an `observation` about the evaluator, and the fix (case002-e13) is a `methodology_correction` — not the same event, linked via `resolved_by`/`resolves` | case002-e12/e13 |
| C2-15 | 5 | case002-e15 is explicitly a `conclusion` (methodological, about single-fixture overfit risk in general) — distinct from and broader than the specific correction itself | case002-e15 |
| C2-16 | 5 | case002-e11 contains explicit hypothesis labels (H1 not supported, H4 supported, H6 supported) — these are hypotheses/mixed findings from one experiment, not established conclusions about all future documents | case002-e11 |
| C2-17 | 6 | Four open/unresolved items exist (trailing-triple generalization, CJK-space-closing port, Docling grid investigation, ministry-generality of the annotation pattern) — none resolved yet | case002-e16/e17/e18/e19, all `status: open` |
| C2-18 | 6 | No case-003 has actually been created — case002-e19 only proposes it as a reason for a *future* case-003, and a faithful reconstruction must not claim case-003 already exists | case002-e19 wording ("proposed... not executed") |
| C2-19 | 1/5 | `annotationColumnPlacementRelativeToAmountTriple` is explicitly flagged in the supplied file itself as discovered via engine output, not independent visual inspection, despite being plausibly source-observable — a strong reconstruction might surface this nuance if asked about methodology caveats, though the fixed schema does not explicitly prompt for it | engineDerivedProfile `annotationColumnPlacementRelativeToAmountTriple` note field |

## Grading categories (applied per checklist item during evaluation)

- **correctly_reconstructed** — the fact is present, accurate, and not misattributed to the wrong epistemic category or temporal state.
- **partially_reconstructed** — the fact is present but incomplete, vague, or has a minor category/temporal slip.
- **omitted** — the fact is simply absent from the model's output.
- **contradicted** — the model's output states something inconsistent with this checklist item.
- **hallucinated_unsupported** — not a checklist item per se, but tracked separately: any claim in the model's output not traceable to the supplied files or this checklist, counted once per distinct instance, independent of the above per-item grades.

## Freezing statement

This checklist was written before either reconstruction prompt was sent to a model, and is not edited after seeing case-001's or case-002's output. Any defect discovered in this checklist during evaluation (e.g. an item found to be ambiguous) is documented as a limitation in the final benchmark report, not silently corrected in this file.
