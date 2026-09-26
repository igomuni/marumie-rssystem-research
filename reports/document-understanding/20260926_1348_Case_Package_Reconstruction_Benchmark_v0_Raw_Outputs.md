# Case Package Reconstruction Benchmark v0 — Raw Reconstruction Outputs

Status: **raw model output, verbatim, unedited. Distinct from evaluation/interpretation (see the separate evaluation-result and benchmark-report artifacts).**

Date: 2026-09-26 (Asia/Tokyo)

## Runtime metadata (actually available; nothing fabricated)

- Both reconstructions were run as separate `Agent` tool invocations, `subagent_type: general-purpose`, each a fresh context with no memory of this conversation or of each other.
- Model/provider/version: not exposed to the orchestrating session by the tooling used; not fabricated here. Both runs used the same subagent type and the same orchestrating session, so any model/version is presumed identical across the two runs, but the exact model identifier string was not returned by the tool and is recorded as unknown rather than guessed.
- Execution date: 2026-09-26 (Asia/Tokyo), same session, sequential tool calls issued in the same message (run in parallel by the harness).
- Prompt version: v1, exactly as frozen in `20260926_1348_Case_Package_Reconstruction_Benchmark_v0_Frozen_Prompt_And_Schema.md`, with only the two per-case file blocks substituted into the placeholders.
- Sampling configuration (temperature, top_p, etc.): not exposed/controllable via the `Agent` tool interface used; recorded as unknown, not fabricated.
- Tool/web/repository-access state: each subagent was launched inside the same working directory (`/Users/igomuni/MyGitHub/marumie-rssystem-research`) and, per its agent-type definition, had the same tool access as a general-purpose agent (including Read/Bash/Grep/WebFetch) — i.e., a hard sandbox disabling those tools was NOT available with this session's tooling. Isolation was therefore behavioral/instructional (explicit "do not use any tools" instruction in the prompt), not enforced. Observed evidence of compliance: each agent's usage summary reports exactly `tool_uses: 1` — consistent with the single required hand-back/report call and no repository-access tool call. This is suggestive but not airtight proof of zero repository access (see the benchmark report's "Experimental validity" section for the full caveat).

## case-001 raw output (verbatim, as returned by the subagent)

```json
{
  "caseId": "case-001",
  "identity": {
    "sourceId": "digital-r6-request-table-01",
    "organization": "デジタル庁",
    "fiscalYear": 2024,
    "documentTitle": "令和6年度歳出概算要求書",
    "documentStage": "request",
    "targetLocation": "PDF page index 11 / PDF page number 12 / printed page label \"8\"; target row: item code 020, expense 01-95",
    "evidence": ["identity", "case001-e03"]
  },
  "methodsAndEngines": [
    {
      "name": "pdfjs-baseline",
      "description": "Flat-text/coordinate extraction baseline built on scripts/pdf-extraction's deterministic pdfjs-dist-based glyph/text/coordinate extraction.",
      "evidence": ["case001-e02", "case001-e03", "rawExtractionSucceeded"]
    },
    {
      "name": "pymupdf-baseline",
      "description": "Second flat-text extraction baseline, registered alongside pdfjs-baseline for the Document Understanding Benchmark.",
      "evidence": ["case001-e03", "rawExtractionSucceeded"]
    },
    {
      "name": "docling",
      "description": "Table-structure-aware engine integrated with a dedicated normalizer (normalize-docling.mjs) that preserves native table-cell structure rather than flattening it; includes closeCjkWrapSpaces and reconstructNumericToken rules.",
      "evidence": ["case001-e05", "rawExtractionSucceeded", "doclingTableGridDimensions", "doclingCellSeparationResolvedExpenseNameConflation", "doclingNumericTokenReversalObserved"]
    }
  ],
  "experimentsAndInterventions": [
    {
      "summary": "Source PDFs (including digital-r6-request-table-01) acquired via plain fetch and SHA-256-locked per ADR-009.",
      "kind": "intervention",
      "date": "2026-09-25",
      "commit": "64913ae",
      "evidence": ["case001-e01"]
    },
    {
      "summary": "Deterministic page-aware PDF extraction layer (scripts/pdf-extraction) added, later reused by pdfjs-baseline.",
      "kind": "intervention",
      "date": "2026-09-25",
      "commit": "9a6c0dd",
      "evidence": ["case001-e02"]
    },
    {
      "summary": "Document Understanding Benchmark layer created; case-001 defined with Ground Truth frozen by manual visual verification; pdfjs-baseline and pymupdf-baseline adapters registered.",
      "kind": "intervention",
      "date": "2026-09-26",
      "commit": "4ee301e",
      "evidence": ["case001-e03"]
    },
    {
      "summary": "Docling adapter integrated with dedicated normalizer adding closeCjkWrapSpaces and reconstructNumericToken rules.",
      "kind": "intervention",
      "date": "2026-09-26",
      "commit": "b75bee5",
      "evidence": ["case001-e05"]
    }
  ],
  "importantSuccesses": [
    {
      "summary": "Docling's native table-cell separation resolved expense_name_exact_match_after_line_join, which both flat-text baselines (pdfjs-baseline, pymupdf-baseline) failed due to an unrelated annotation column contaminating the reconstructed wrapped label.",
      "evidence": ["case001-e04", "case001-e06", "doclingCellSeparationResolvedExpenseNameConflation"]
    },
    {
      "summary": "reconstructNumericToken deterministically corrected Docling's reversed numeric comma-group assembly, verified across multiple independent cells on this page.",
      "evidence": ["case001-e05", "doclingNumericTokenReversalObserved"]
    },
    {
      "summary": "All three engines (pdfjs-baseline, pymupdf-baseline, docling) succeeded at raw text extraction for case-001.",
      "evidence": ["rawExtractionSucceeded"]
    }
  ],
  "importantFailures": [
    {
      "summary": "item_name_exact_match FAILed for engines due to header-row hierarchy ambiguity: multiple NNN <name>-shaped rows (item codes 036, 041, 046, and target 020) at different hierarchy levels; correct row was present among candidates but not uniquely resolved.",
      "evidence": ["case001-e04", "headerRowHierarchyAmbiguityPresent", "case001-e11"]
    },
    {
      "summary": "unit_exact_match FAILed for all three engines because the '千円' unit label appears only on an earlier summary page, not on the target page itself.",
      "evidence": ["case001-e04", "pageLevelUnitLabelPresentOnTargetPage", "case001-e13"]
    },
    {
      "summary": "expense_name_exact_match_after_line_join FAILed for pdfjs-baseline and pymupdf-baseline (though resolved for docling) due to an unrelated annotation column contaminating the reconstructed wrapped expense-name label.",
      "evidence": ["case001-e04", "tableRegion_multiLineWrap"]
    },
    {
      "summary": "Docling produced no cell for the target row's request-number column; requestNo recovered as null for docling on case-001 — an unresolved per-engine limitation.",
      "evidence": ["requestNoRecoveredByDocling", "case001-e12"]
    }
  ],
  "historicalBenchmarkResults": [
    {
      "summary": "First benchmark run (pre-Docling, then-current check set including raw_delta_glyph_preserved): pdfjs-baseline 8/11, pymupdf-baseline 8/11.",
      "isSuperseded": true,
      "supersededBy": "case001-e10",
      "date": "2026-09-26",
      "evidence": ["case001-e04"]
    },
    {
      "summary": "After Docling integration: pdfjs-baseline 8/11, pymupdf-baseline 8/11, docling 9/11, under the check set as it existed before the evaluator correction (i.e. still including the superseded raw_delta_glyph_preserved / delta_glyph_observed_and_associated check).",
      "isSuperseded": true,
      "supersededBy": "case001-e10",
      "date": "2026-09-26",
      "evidence": ["case001-e06"]
    }
  ],
  "currentBenchmarkResults": [
    {
      "summary": "Under the corrected evaluator (delta_sign_evidence_matches_source, commit 519ce28): pdfjs-baseline 8/11, pymupdf-baseline 8/11, docling 9/11 — scores unchanged from the pre-correction run, because case-001's Ground Truth deltaRaw genuinely carries a △ glyph and every engine's own output genuinely contained one.",
      "supersedes": "case001-e06",
      "date": "2026-09-26",
      "evidence": ["case001-e10", "finalScores"]
    }
  ],
  "methodologyCorrections": [
    {
      "summary": "raw_delta_glyph_preserved's name/description overstated what was measured (for Docling, deltaRaw could be a normalizer-constructed concatenation of two separate raw cells, not a literal single raw token); renamed to delta_glyph_observed_and_associated with corrected note language distinguishing 'genuinely present in engine output' from 'literal raw token'. This correction was itself later superseded.",
      "correctedEventId": "unknown",
      "evidence": ["case001-e07"]
    },
    {
      "summary": "delta_glyph_observed_and_associated (which hardcoded expected: 'contains △' regardless of Ground Truth) was replaced with delta_sign_evidence_matches_source, which derives the expected glyph state from Ground Truth's own deltaRaw field. Discovered via case-002's out-of-sample run, whose correctly glyph-free Ground Truth could never have passed the old hardcoded check.",
      "correctedEventId": "case001-e07",
      "evidence": ["case001-e09"]
    }
  ],
  "currentSupportedConclusions": [
    {
      "summary": "For case-001, preserving native table-cell structure (Docling) rather than flattening to plain text resolves the expense-name line-join/column-conflation failure that both flat-text baselines exhibit, yielding a higher score (9/11 vs 8/11).",
      "evidence": ["case001-e06", "doclingCellSeparationResolvedExpenseNameConflation", "finalScores"]
    },
    {
      "summary": "case-001's evaluator-corrected score is stable across the delta-sign evaluation methodology correction, because its Ground Truth deltaRaw genuinely contains a decrease glyph (△) and all three engines genuinely reproduced glyph-bearing output.",
      "evidence": ["case001-e10", "finalScores"]
    },
    {
      "summary": "Two document-family-level structural gaps (header-row hierarchy ambiguity; page-level unit-label lookup) are not resolved by any of the three engines tested on case-001, since they are layout/semantic-interpretation problems rather than raw-extraction or table-structure problems.",
      "evidence": ["case001-e11", "case001-e13", "headerRowHierarchyAmbiguityPresent", "pageLevelUnitLabelPresentOnTargetPage"]
    }
  ],
  "hypotheses": [],
  "unresolvedQuestions": [
    {
      "summary": "Header-row hierarchy ambiguity (multiple NNN <name>-shaped rows at different 項/目 levels) is unresolved for all three engines; item_name_exact_match cannot resolve to a single row without an indentation/hierarchy-level detection mechanism not yet built.",
      "evidence": ["case001-e11", "headerRowHierarchyAmbiguityPresent"]
    },
    {
      "summary": "Docling produced no cell for case-001's target row's request-number column (requestNo null) — an unresolved per-engine limitation, not yet investigated.",
      "evidence": ["case001-e12", "requestNoRecoveredByDocling"]
    },
    {
      "summary": "A general per-page/document-level unit-label lookup mechanism is unimplemented; unit_exact_match correctly fails for all three engines because '千円' lives only on an earlier summary page, not the target page.",
      "evidence": ["case001-e13", "pageLevelUnitLabelPresentOnTargetPage"]
    },
    {
      "summary": "Whether case-001's own reconstructed lines exhibit the pdfjs-dist CJK-wrap-space-closing artifact (discovered via case-002's header row) was not checked in the backfill task.",
      "evidence": ["cjkWrapSpaceArtifactPresent_pdfjs"]
    },
    {
      "summary": "Whether the target row's own △ delta glyph reflects a page-wide convention (vs. only the target row's own state) was not independently confirmed via cross-row comparison.",
      "evidence": ["deltaGlyphConventionObservedOnPage"]
    }
  ],
  "proposedNextInvestigation": {
    "summary": "unknown",
    "rationale": "The two supplied files record open questions (header-row hierarchy ambiguity, docling's null requestNo, unimplemented unit-label lookup, unchecked CJK-wrap-space artifact, unconfirmed delta-glyph convention) but do not state a prioritized or recommended next investigation for case-001 specifically.",
    "evidence": ["case001-e11", "case001-e12", "case001-e13", "cjkWrapSpaceArtifactPresent_pdfjs", "deltaGlyphConventionObservedOnPage"]
  },
  "explicitUnknowns": [
    "pageCount (not_recorded in document-profile.json)",
    "pdfProducer (not_recorded)",
    "pageOrientation (not_recorded)",
    "textLayerPresence (not_recorded)",
    "deltaGlyphConventionObservedOnPage as a page-wide convention (not_independently_confirmed)",
    "cjkWrapSpaceArtifactPresent_pdfjs for case-001 (not_checked)",
    "The exact commit that case001-e07's correction was itself corrected at, beyond being superseded by case001-e09 (commit 519ce28)",
    "Any pre-registered selection protocol for case-001 (explicitly absent per backfillNote; unlike case-002)",
    "A named/prioritized 'next investigation' recommendation specific to case-001",
    "Full content of case-001/README.md and case-001-evaluation.md (only referenced, not included in supplied files)"
  ]
}
```

## case-002 raw output (verbatim, as returned by the subagent)

```json
{
  "caseId": "case-002",
  "identity": {
    "sourceId": "meti-fy2024-general-account-request",
    "organization": "経済産業省",
    "fiscalYear": 2024,
    "documentTitle": "令和6年度歳出概算要求書（一般会計）",
    "documentStage": "request",
    "targetLocation": "PDF page index 8 / PDF page number 9, printed label 経(本) 5; target row = item 010 経済産業本省共通費, expense code 01-95, first 目-level expense-coded row in the document's detail table (明細表)",
    "evidence": ["identity", "case002-e04"]
  },
  "methodsAndEngines": [
    {"name": "pdfjs-baseline", "description": "Flat-text extraction baseline engine; one of three compared engines in the benchmark.", "evidence": ["rawExtractionSucceeded", "case002-e07", "case002-e09"]},
    {"name": "pymupdf-baseline", "description": "Flat-text extraction baseline engine using PyMuPDF with sort=True reconstruction; one of three compared engines.", "evidence": ["rawExtractionSucceeded", "case002-e07", "case002-e09"]},
    {"name": "docling", "description": "Document-understanding engine using TableFormer for table/grid reconstruction; one of three compared engines.", "evidence": ["rawExtractionSucceeded", "doclingTableGridDimensions", "doclingSilentWrongRowSelection", "case002-e10"]},
    {"name": "playwright_chromium (browser-fetch)", "description": "Source-acquisition tool (Playwright 1.63.0) built to satisfy an AWS WAF Bot Control JS challenge that blocked plain fetch(); not an analysis/comparison engine.", "evidence": ["acquisitionMethod", "case002-e02", "case002-e03"]},
    {"name": "pdfinfo (poppler)", "description": "Used only for source-safe profiling (page count, producer, orientation, encryption); explicitly excluded as one of the three compared engines per the selection protocol's tooling rule.", "evidence": ["pageCount", "pdfProducer", "pageOrientation", "encrypted"]}
  ],
  "experimentsAndInterventions": [
    {"summary": "Case-002 selection protocol preregistered (E1-E5 eligibility criteria, engine-blind row enumeration via direct visual inspection, deterministic earliest-eligible-row tie-break) before the source was even acquired.", "kind": "intervention", "date": "2026-09-26", "commit": "4432492", "evidence": ["case002-e01"]},
    {"summary": "Built scripts/source-acquisition/browser-fetch (Playwright/Chromium) to bypass the WAF challenge; acquired and SHA-256-locked the METI PDF (106 pages, A4 landscape, Producer 'List Creator', not encrypted).", "kind": "intervention", "date": "2026-09-26", "commit": "d53cb80", "evidence": ["case002-e03"]},
    {"summary": "Preregistered selection protocol applied via direct visual inspection (pdftoppm render, no compared engine used); target row frozen.", "kind": "intervention", "date": "2026-09-26", "commit": "b8c5674", "evidence": ["case002-e04"]},
    {"summary": "Ground Truth frozen by direct visual inspection (400dpi pdftoppm renders) before any engine was run; delta observed as positive (4,556,824, no △ glyph), cross-checked against six neighboring rows that do carry △.", "kind": "intervention", "date": "2026-09-26", "commit": "5a2eb32", "evidence": ["case002-e06"]},
    {"summary": "First frozen out-of-sample benchmark run against the unchanged, case-001-derived pipeline (no code changed after seeing the result).", "kind": "experiment", "date": "2026-09-26", "commit": "379043d", "evidence": ["case002-e07"]}
  ],
  "importantSuccesses": [
    {"summary": "All three engines (pdfjs-baseline, pymupdf-baseline, docling) succeeded at raw extraction/reconstruction of the target line/cells; observed failures occur at the structure-recovery/normalization stage, not raw extraction.", "evidence": ["rawExtractionSucceeded"]},
    {"summary": "unit_exact_match passed for all 3 engines on case-002, supporting hypothesis H4 (unit-label recovery is page-context-dependent, not a fundamental extraction gap) since case-002's target page carries a printed unit label unlike case-001's.", "evidence": ["case002-e11", "pageLevelUnitLabelPresentOnTargetPage"]},
    {"summary": "Ground Truth delta sign (positive, no glyph) was corroborated by comparison against six neighboring rows on the same page that do visibly carry the △ glyph, ruling out a rendering artifact suppressing a faint glyph.", "evidence": ["case002-e06", "deltaGlyphConventionObservedOnPage"]}
  ],
  "importantFailures": [
    {"summary": "common.mjs's splitTrailingTriple regex requires the amount triple to be the literal end of the line; broke for both flat-text engines because case-002's annotation column （要求要旨） follows the triple on the same reconstructed line.", "evidence": ["case002-e08", "splitTrailingTripleFailed_flatTextEngines"]},
    {"summary": "common.mjs lacks a CJK wrap-space-closing normalization step (unlike normalize-docling.mjs); pdfjs-dist's letter-spacing artifact on header rows flipped item_name_present_among_candidates between pdfjs (FAIL) and pymupdf (PASS), unrelated to amounts/signs.", "evidence": ["case002-e09", "cjkWrapSpaceArtifactPresent_pdfjs"]},
    {"summary": "Docling produced a coarser, misaligned 23x12 table grid (vs. case-001's 21x14), merging logical rows and splitting the target row's amount triple across grid rows; 1 of 322 cells dropped.", "evidence": ["case002-e10", "doclingTableGridDimensions"]},
    {"summary": "Docling silently selected the wrong row (itemCandidateCount: 1, implying no ambiguity) — matching an unrelated, deeper-hierarchy row ('001 人件費...') because the expense code and its label landed in different, unpaired grid cells; a more concerning failure mode than the flat-text baselines' honest nulls.", "evidence": ["case002-e10", "doclingSilentWrongRowSelection"]},
    {"summary": "Both flat-text engines found the same 4 item-code-shaped candidates (010, 010, 001, 001) with no disambiguation, mirroring case-001's header-row hierarchy ambiguity finding, discovered via engine output rather than pre-engine inspection.", "evidence": ["case002-e11", "headerRowHierarchyAmbiguityPresent"]},
    {"summary": "The evaluator's delta_glyph_observed_and_associated check hardcoded an expectation of 'contains △' regardless of Ground Truth, making it impossible for any engine to pass on a document (like case-002) whose correct delta has no glyph — an evaluation-methodology defect, invisible with only case-001.", "evidence": ["case002-e12", "evaluatorGlyphCheckOverfitDiscovered"]}
  ],
  "historicalBenchmarkResults": [
    {"summary": "First frozen benchmark run (pre-correction): pdfjs-baseline 2/11, pymupdf-baseline 3/11, docling 2/11 — a severe regression from case-001's 8-9/11. Preserved permanently, never amended.", "isSuperseded": true, "supersededBy": "case002-e14", "date": "2026-09-26", "evidence": ["case002-e07"]}
  ],
  "currentBenchmarkResults": [
    {"summary": "Corrected-evaluator scores (current): pdfjs-baseline 3/11, pymupdf-baseline 4/11, docling 3/11 — exactly +1 per engine over the first frozen run, since no engine had fabricated a false glyph; every other check's PASS/FAIL outcome was confirmed identical before and after.", "supersedes": "case002-e07", "date": "2026-09-26", "evidence": ["case002-e14", "finalScores"]}
  ],
  "methodologyCorrections": [
    {"summary": "delta_glyph_observed_and_associated was replaced with delta_sign_evidence_matches_source, which derives the expected glyph state from Ground Truth's own deltaRaw field instead of hardcoding it; classified as evaluator overfit to case-001's specific source condition, not an extraction/normalization bug and not Ground Truth contamination.", "correctedEventId": "case002-e12", "evidence": ["case002-e13"]}
  ],
  "currentSupportedConclusions": [
    {"summary": "A single-fixture benchmark's checks can encode implicit assumptions from that fixture even when explicit Ground-Truth-isolation discipline is followed perfectly; checks need re-examination against a second, independently-selected case before being trusted as fixture-independent. This is a distinct failure category from extraction/normalization bugs.", "evidence": ["case002-e15"]}
  ],
  "hypotheses": [
    {"summary": "H1: Docling's table-cell separation generalizes across ministries.", "status": "NOT SUPPORTED by this single contrasting case", "evidence": ["case002-e11"]},
    {"summary": "H4: Unit-label recovery is page-context-dependent, not a fundamental extraction gap.", "status": "SUPPORTED (unit_exact_match passed for all 3 engines here, unlike case-001)", "evidence": ["case002-e11"]},
    {"summary": "H6: Header-row hierarchy ambiguity persists.", "status": "SUPPORTED for the flat-text engines; Docling's version manifested differently (a wrongly-confident wrong-row match, not a flagged ambiguity)", "evidence": ["case002-e11"]}
  ],
  "unresolvedQuestions": [
    {"summary": "Whether splitTrailingTriple's trailing-anchor assumption can be relaxed to tolerate non-numeric trailing content (like this case's same-line annotation) without reintroducing amount-similarity-as-selection-evidence risk.", "evidence": ["case002-e16"]},
    {"summary": "Whether adding a closeCjkWrapSpaces-equivalent step to common.mjs/normalize.mjs fixes the item_name_present_among_candidates asymmetry without regressing case-001.", "evidence": ["case002-e17"]},
    {"summary": "Why Docling's TableFormer produced a coarser, misaligned grid for this specific page, and whether itemCandidateCount: 1 should carry a lower-confidence signal when the winning cell's row position looks structurally inconsistent with neighboring cells.", "evidence": ["case002-e18"]},
    {"summary": "Whether the annotation-on-same-line-as-triple pattern found here is common or rare across ministries — proposed as a reason for a future case-003, not executed by this backfill task.", "evidence": ["case002-e19"]}
  ],
  "proposedNextInvestigation": {
    "summary": "Investigate whether splitTrailingTriple's trailing-anchor assumption can be relaxed to tolerate non-numeric trailing content (e.g., same-line annotations like （要求要旨）) without reintroducing amount-similarity-as-selection-evidence risk.",
    "rationale": "Recommended as the single next follow-up experiment in both the first-frozen-run report and the evaluator-correction report.",
    "evidence": ["case002-e16"]
  },
  "explicitUnknowns": [
    "Full ground-truth.json contents beyond the delta value (4,556,824, positive, no glyph) and the general row identity — previous-budget and FY2024-request amounts of the triple are not given.",
    "Whether the case002-e17 (CJK wrap-space normalization fix) or case002-e19 (case-003 investigation) follow-ups have been executed — both are 'open' status with no resolving event in the supplied data.",
    "textLayerPresence source-safe feature is explicitly recorded as 'not_recorded' / provenance 'not_recorded'.",
    "Any content of case-001's own case package (only comparative references to it appear in these two files, e.g. its 21x14 Docling grid, its 8-9/11 scores, its glyph-bearing Ground Truth, its plain-digit request-number convention) — no case-001 file was supplied.",
    "Exact contents/text of README, START_HERE.md, protocol files, or any other repository file — none were supplied for this task."
  ]
}
```

## Technical execution notes

Both runs completed on the first attempt with valid, schema-conforming JSON (verified separately in the evaluation-result artifact). No retry was needed; no output was discarded or regenerated after inspection.
