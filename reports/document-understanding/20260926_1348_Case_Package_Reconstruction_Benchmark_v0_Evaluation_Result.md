# Case Package Reconstruction Benchmark v0 — Evaluation Result

Status: **deterministic checklist comparison, performed by the orchestrating session against the frozen checklist, after both reconstruction outputs were received. The checklist was not altered based on either output.**

Date: 2026-09-26 (Asia/Tokyo)

Method note: per the task's instruction to prefer deterministic/manual checklist comparison over self-judging, this evaluation was performed directly against `20260926_1348_..._Frozen_Evaluation_Checklist.md`, item by item, by the same session that has full canonical repository knowledge (permitted for the evaluator, never for the reconstruction model). No new checklist items were added after seeing the outputs; where an output revealed a checklist wording ambiguity, that is noted below rather than the checklist being edited.

## case-001 — per-item grading

| ID | Grade | Notes |
|---|---|---|
| C1-01 | correctly_reconstructed | Source, organization, FY2024, request stage all correct. |
| C1-02 | correctly_reconstructed | Page index 11 / number 12 / label "8" and target row (020/01-95) all correct. |
| C1-03 | correctly_reconstructed | Listed all four as `not_recorded`/unknown in `explicitUnknowns`; did not guess. |
| C1-04 | correctly_reconstructed | All three engines named with accurate descriptions. |
| C1-05 | correctly_reconstructed | Both named rules (CJK wrap-space closing, numeric-token reversal) captured under case001-e05. |
| C1-06 | correctly_reconstructed | Captured under importantSuccesses, correctly attributes cause (table-cell separation) and effect (resolved line-join check). |
| C1-07 | correctly_reconstructed | Captured under importantFailures and unresolvedQuestions with correct evidence IDs. |
| C1-08 | correctly_reconstructed | Captured, correctly notes label is on a different page. |
| C1-09 | correctly_reconstructed | Captured under importantFailures and unresolvedQuestions. |
| C1-10 | correctly_reconstructed | `historicalBenchmarkResults` explicitly lists BOTH the pre-Docling (8/11, 8/11) and post-Docling-integration (8/11, 8/11, 9/11) states as separate, both marked `isSuperseded: true`, both pointing to case001-e10 as the current state. This is a genuinely careful reconstruction — it did not collapse the two historical states into one. |
| C1-11 | correctly_reconstructed | Both renames captured as two distinct `methodologyCorrections` entries; correctly notes the first correction (case001-e07) was "itself later superseded." |
| C1-12 | correctly_reconstructed | `currentBenchmarkResults` explicitly states scores are "unchanged from the pre-correction run" with the correct reason (glyph genuinely present in both GT and engine output). |
| C1-13 | correctly_reconstructed | Both correction events are `kind: methodology_correction` in the model's structuring, kept separate from engine-behavior findings. |
| C1-14 | partially_reconstructed | The model states case001-e07 "was itself later superseded" (correct substance) but did not explicitly surface the raw `status: superseded` vs `status: current` field values from the source file — the distinction is conveyed in prose, not literally quoted. Minor. |
| C1-15 | correctly_reconstructed | All three listed under `unresolvedQuestions`, none presented as resolved. |
| C1-16 | correctly_reconstructed | No case-003 or strategy-selection claim appears anywhere in the output. `proposedNextInvestigation.summary` is explicitly `"unknown"` with a rationale explaining the supplied files name open questions but no prioritized recommendation — this is exactly the correct behavior (refusing to invent a recommendation not present in the source), and is arguably the single most methodologically impressive moment in this run. |

**case-001 score: 15 correctly_reconstructed, 1 partially_reconstructed, 0 omitted, 0 contradicted, out of 16 items.**

**Hallucination/unsupported-claim count (case-001): 0.** Every evidence ID and feature key cited in the output was checked against the supplied `research-history.jsonl`/`document-profile.json`; all resolve to real entries. No invented commit hashes, paths, or values were found. `historicalBenchmarkResults[1]`'s phrase "check set as it existed before the evaluator correction (i.e. still including the superseded raw_delta_glyph_preserved / delta_glyph_observed_and_associated check)" is an inference beyond a literal one-line summary quote, but it is directly and correctly derivable from case001-e05/e06/e07/e09's content — not counted as unsupported.

## case-002 — per-item grading

| ID | Grade | Notes |
|---|---|---|
| C2-01 | correctly_reconstructed | Source, organization, FY2024, request stage all correct. |
| C2-02 | correctly_reconstructed | Page index 8 / number 9 / label "経(本) 5" and target row correct. |
| C2-03 | correctly_reconstructed | Listed under `methodsAndEngines` (pdfinfo entry) with all four facts (106 pages, List Creator, A4 landscape, not encrypted) implicitly available via feature keys, though the values themselves are not re-stated verbatim in that entry's description — see note below. |
| C2-04 | correctly_reconstructed | WAF failure → Playwright acquisition chronology explicit in `experimentsAndInterventions` and `methodsAndEngines`, with the `resolves` relation implicitly preserved via ordering and description. |
| C2-05 | correctly_reconstructed | Preregistration-before-acquisition point captured explicitly in the first `experimentsAndInterventions` entry. |
| C2-06 | correctly_reconstructed | Ground-Truth-before-engine-run point captured, including the six-neighboring-row cross-check. |
| C2-07 | correctly_reconstructed | 2/11, 3/11, 2/11 captured exactly in `historicalBenchmarkResults`. |
| C2-08 | correctly_reconstructed | Same-line annotation failure captured with correct mechanism (trailing-anchor regex) under `importantFailures`. |
| C2-09 | correctly_reconstructed | Docling wrong-row/no-ambiguity-signal failure captured with correct detail (itemCandidateCount: 1, unpaired cells). |
| C2-10 | correctly_reconstructed | Captured under `importantSuccesses`, correctly ties it to H4 and to case-001 contrast. |
| C2-11 | correctly_reconstructed | 2/11, 3/11, 2/11 explicit, `isSuperseded: true`, `supersededBy: case002-e14`. |
| C2-12 | correctly_reconstructed | 3/11, 4/11, 3/11 explicit, `supersedes: case002-e07`, marked current. |
| C2-13 | correctly_reconstructed | **Both scores appear as separate, linked entries — this is the critical temporal test, and it passed cleanly.** The original is explicitly labeled "preserved permanently, never amended" (quoting case002-e07's own summary) and the corrected one explicitly states "+1 per engine over the first frozen run." Neither state is presented as the only truth. |
| C2-14 | correctly_reconstructed | `methodologyCorrections[0].correctedEventId: "case002-e12"` correctly links the fix to the specific defect-observation event, distinct in kind from the correction event itself. |
| C2-15 | correctly_reconstructed | case002-e15's conclusion reproduced under `currentSupportedConclusions`, correctly kept separate from the specific correction (`methodologyCorrections`) and from the specific re-score (`currentBenchmarkResults`). |
| C2-16 | correctly_reconstructed | All three hypotheses (H1, H4, H6) reproduced with their exact SUPPORTED/NOT SUPPORTED status, not flattened into unconditional conclusions. |
| C2-17 | correctly_reconstructed | All four open questions listed, all under `unresolvedQuestions`, none marked resolved. `case002-e19`'s "proposed... not executed" framing is explicitly preserved almost verbatim. |
| C2-18 | correctly_reconstructed | The output never claims a case-003 exists; case002-e19 is correctly framed as a proposal, not an accomplished fact. |
| C2-19 | omitted | The schema does not have a dedicated slot for "methodology caveats about a feature's own discovery provenance," and the model did not surface the `annotationColumnPlacementRelativeToAmountTriple` note's self-flagged A/B ambiguity anywhere in its output (it does cite the feature key once, under `importantFailures[0].evidence`, but only for the underlying fact, not the meta-point about how it was discovered). This is graded `omitted` rather than a fault of the model, since the fixed schema (frozen before the run, per the task's own instruction) never explicitly asked for this — see Representation Diagnosis below. |

**case-002 score: 18 correctly_reconstructed, 0 partially_reconstructed, 1 omitted, 0 contradicted, out of 19 items.**

**Hallucination/unsupported-claim count (case-002): 0.** All evidence IDs/feature keys resolve to real entries. `methodsAndEngines` includes "pdfinfo (poppler)" and "playwright_chromium (browser-fetch)" as tools distinct from the three compared engines — this is a correct, non-hallucinated inference directly supported by the supplied provenance notes (e.g. `acquisitionMethod`'s note explicitly names Playwright/Chromium 1.63.0; `pageCount`'s note explicitly names pdfinfo/poppler and states it is not one of the three compared engines).

## Cross-case comparison

| Dimension | case-001 | case-002 |
|---|---|---|
| 1. Identity | Full marks | Full marks |
| 2. Method | Full marks | Full marks |
| 3. Result | Full marks | Full marks |
| 4. Temporal (critical) | Full marks, including the harder two-historical-states case-001 also has (pre/post Docling, independent of the evaluator correction) | Full marks, including the explicitly flagged critical test (both 2/11-3/11-2/11 and 3/11-4/11-3/11 preserved and linked) |
| 5. Epistemic | 1 partial (status field not literally quoted) | Full marks |
| 6. Open-work | Full marks, including a correct "unknown" refusal for `proposedNextInvestigation` | Full marks, minus the one omitted meta-provenance nuance (C2-19) |

Neither run produced a single hallucinated claim, invented ID, invented commit, invented Ground-Truth value, or retroactively applied case-002's preregistration discipline to case-001 (case-001's output explicitly lists "Any pre-registered selection protocol for case-001 (explicitly absent... unlike case-002)" as an `explicitUnknown` — the opposite of the hallucination risk named in the task).
