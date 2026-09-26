# CJK Spacing Strategy Layer Experiment

Status: **implemented after evidence-based layer justification. All three cases re-evaluated. No regressions; one disclosed, harmless collateral value change identified and explained.**

Date: 2026-09-26 (Asia/Tokyo)

## Research question

> Is the pdf.js CJK-spacing behavior best treated as extraction representation, engine-specific normalization, document/layout-family interpretation, or semantic matching, and can a deterministic strategy improve generalization without obscuring provenance?

## Pre-change case-001/002/003 evidence

Reference scores confirmed via a fresh, now-reliable `docbench` run (post-`7b905a1`) before any code change:

| Case | pdfjs-baseline | pymupdf-baseline | docling |
|---|---|---|---|
| case-001 | 8/11 | 8/11 | 9/11 |
| case-002 | 3/11 | 4/11 | 3/11 |
| case-003 | 9/11 | 10/11 | 3/11 |

All matched the previously-recorded historical values exactly.

`item_name_present_among_candidates` raw candidate inspection, per engine:

| Case | pdfjs-baseline | pymupdf-baseline |
|---|---|---|
| case-001 | `公金受取口座登録業務支援経費`, `デジタル推進委員等環境整備事業費`, ... — **no spaces**, PASS | same, PASS |
| case-002 | `経 済 産 業 本 省`, `経 済 産 業 本 省 共 通 費`, ... — **spaced**, FAIL | `経 済 産 業 本 省`, `経済産業本省共通費`, ... — target candidate already clean, PASS |
| case-003 | `総 務 本 省`, `総 務 本 省 共 通 費`, ... — **spaced**, FAIL | `総  務  本  省`, `総務本省共通費`, ... — target candidate already clean, PASS |

**Raw reconstructed-line inspection (the actual cause, traced to the source):**

```text
case-001, line 6:  "036 公金受取口座登録業務支"          <- body-text row, NOT spaced
case-002, line 7:  "010 経 済 産 業 本 省 234,599,916 ..." <- 組織-level total row, SPACED
case-002, line 8:  "010 経 済 産 業 本 省 共 通 費 ..."     <- 項-level total row, SPACED
case-002, line 9:  "1 01-95 経済産業本省一般行政に ..."     <- target expense row, NOT spaced
case-003, line 7:  "010 総 務 本 省 010 総 務 本 省 共 通 費 ..." (in Docling's merged cell; pdfjs's own flat line for the same content is spaced identically for the 組織/項 rows)
```

**Control comparison (case-001):** case-001's target page has no `組織`-level total row at all — its item-code rows (`036`, `041`, `046`, `020`) are all body-text-styled expense-detail rows, structurally analogous to case-002/003's *target* rows (which are also never spaced), not to their `組織`/`項`-level header/total rows (which are always spaced). This is not a difference in pdfjs's general behavior across documents; it is the *same* pdfjs behavior applied to a row type case-001's page simply never exercises.

**Conclusion from pre-change evidence:** the artifact is not "pdfjs randomly inserts spaces into CJK text." It is pdfjs-dist's line-reconstruction heuristic reacting consistently to a specific **typographic convention**: `組織`/`項`-level total/header rows in this document family (both produced by "List Creator") are rendered with wider inter-character glyph advances than ordinary body/expense-row text, and pdfjs-dist's gap-threshold word-boundary heuristic inserts a space wherever that wider advance occurs; PyMuPDF's own reconstruction (`sort=True`) does not use a comparable gap-sensitive heuristic and reproduces the same rows without spaces regardless of the underlying glyph advance. This was not derived from Ground Truth — it is a property of the raw reconstructed text, independently confirmed by comparing spaced vs. unspaced rows *within the same raw pdfjs-baseline artifact*.

## Raw-vs-normalized provenance

The distinction preserved throughout: `scripts/pdf-extraction`'s raw output and each adapter's `*.raw.json` are never touched by this experiment — they remain the literal, unmodified record of what each engine actually reconstructed, spaces included. The transformation is applied only at the **normalization** stage (`normalize.mjs`'s `reconstructRow`), which already reconstructs a `result`/`candidates` view distinct from the raw artifact by design (this is the same boundary `joinWrappedLabel` already crosses for multi-line wrapping). No transformed candidate is ever described as literally engine-extracted text; `normalize.mjs`'s existing `rawArtifact` field and the separate raw/normalized JSON files continue to make the literal raw text independently recoverable.

## Candidate layer placements considered

| Layer | Provenance clarity | Legitimate-space risk | Engine-specific? | Document-family-specific? | Reuse across 3 cases | Testability | Strategy-selection value |
|---|---|---|---|---|---|---|---|
| **1. Extraction/reconstruction** (modify `scripts/pdf-extraction` itself) | Would blur raw vs. normalized — rejected on principle: raw extraction must remain a faithful, unmodified record (AGENTS.md, ADR-010's raw/normalized boundary) | N/A — not considered further | N/A | N/A | N/A | N/A | N/A |
| **2. Engine-specific normalization** | Clean — applies only where the artifact is engine-specific, leaves raw output untouched | Low, if scoped to CJK-CJK-adjacency only (see rule design below) | **Yes** — this is pdfjs-dist's own reconstruction quirk; PyMuPDF never exhibits it | No — the *trigger* (wide letter-spacing on header rows) is a document-family/producer convention, but the *artifact* (space insertion) is purely a function of which engine reconstructed the text | **Confirmed 2/2** (case-002, case-003); correctly inert on case-001 (nothing to close) | High — pure string function, exhaustively unit-testable | High — flags a specific, engine-derived representation quirk a future strategy could anticipate for pdfjs-dist specifically |
| **3. Document/layout-family interpretation** | Would misrepresent the fault as document-caused when it is engine-caused — rejected | N/A | No (by construction, this layer is meant to be engine-independent per ADR-010) — but the artifact demonstrably differs by engine (PyMuPDF unaffected), so classifying it here would violate ADR-010's own definition | Plausible surface reading, but wrong: this layer is for rules true *regardless of which engine* reads the document; this rule is not that | N/A | N/A | Would incorrectly suggest the fix is needed by every engine, including ones that don't need it |
| **4. Semantic matching tolerance** (e.g. loosen `item_name_present_among_candidates`/`item_name_exact_match` to ignore whitespace) | Poor — would hide a representation defect inside the evaluator, making a real engine-output problem look like a matching-leniency choice | Higher — a whitespace-insensitive match could also silently accept a genuinely wrong candidate that merely lacks the expected internal structure | N/A | N/A | N/A | Testable, but tests the evaluator's tolerance, not the actual representation fix | Low — obscures the very engine/representation signal a future strategy selector would want to see |

**Chosen layer: 2 — engine-specific normalization**, applied to the flat-line engines' shared normalization path (`normalize.mjs`), analogous to how the same rule already exists as Docling's engine-specific normalization. This is chosen from the evidence above (engine-specificity confirmed, document-family-specificity explicitly ruled out per ADR-010's own definition, matching-tolerance rejected as provenance-obscuring), not from the prior report's recommendation being assumed correct in advance.

**Note on the "engine-specific" framing**: `normalize.mjs`'s `normalize()` function is already the *shared* normalizer for both flat-line engines (`pdfjs-baseline` and `pymupdf-baseline`) — they share it because they share the same raw representation shape (`lines: [{lineIndex, text}]`), not because their reconstruction behavior is identical. Applying the rule inside this shared function, rather than only for `pdfjs-baseline`, is consistent with the existing architecture (other rules in `common.mjs`/`normalize.mjs` are already applied uniformly to both engines) and was independently confirmed safe: PyMuPDF's already-clean text passes through the rule as a verified no-op (see tests and the case-002/003 diffs below, where PyMuPDF's target-candidate text is byte-identical before/after).

## Deterministic rule

**No new rule was invented.** The existing, already-tested, already-in-production `closeCjkWrapSpaces` function (previously Docling-only, in `normalize-docling.mjs`) was moved to `common.mjs` as the shared canonical implementation, and applied at one additional call site: `normalize.mjs`'s `reconstructRow`, on the fully-assembled item/expense name (after any wrap-join), for both flat-line engines.

The rule closes a space **only** when it occurs directly between two characters in a CJK/fullwidth-punctuation Unicode range (`　-ヿ㐀-䶿一-鿿＀-￯`), applied repeatedly until no more such gaps remain (handling 3+ character runs). It explicitly does **not** touch:

- CJK ↔ Latin/ASCII (neither side is in the CJK range) — verified by a new negative test.
- CJK ↔ digit (same reasoning; also the pre-existing item-code-prefix test) — verified by a new negative test.
- Already-clean text — verified as an idempotent no-op.

It **does** close a space adjacent to fullwidth punctuation (parentheses, brackets, etc.), since those characters fall inside the same Unicode range — this was already true of the pre-existing Docling-only rule and is not new to this experiment, but its implications were not previously exercised on flat-line text spanning multiple logical columns (see "Unexpected findings" below).

No rule was invented, tuned, or shaped to make any specific Ground Truth value match — the function is byte-for-byte the same one already validated on Docling's independent cell text across case-001 and case-002 before this experiment began.

## Pre-registered expected impact (frozen before re-running)

Recorded here **before** the post-change benchmark was run:

- **case-002, pdfjs-baseline**: `item_name_present_among_candidates` FAIL → PASS (the correct `010`/`経済産業本省共通費` candidate should become byte-identical to Ground Truth once spaces are closed). Score 3/11 → 4/11.
- **case-003, pdfjs-baseline**: same check FAIL → PASS. Score 9/11 → 10/11.
- **case-001**: both flat-line engines unchanged (8/11, 8/11) — no row on case-001's target page currently exhibits the spacing artifact, so the rule should be a pure no-op there.
- **pymupdf-baseline**: unchanged in all three cases — its already-clean text should pass through the rule as a no-op.
- **docling**: byte-identical in all three cases — the refactor is a pure re-export; Docling's own call site and behavior are untouched.
- **`item_name_exact_match` should NOT flip anywhere** — the header-row hierarchy ambiguity (multiple item-code-shaped candidates) is a separate, unresolved problem this experiment does not address; `item_name_present_among_candidates` only checks whether the *correct* candidate is present among several, not that there is a single unambiguous match.
- No other check (amounts, relationships, unit, delta sign) should be affected — the transformation only touches item/expense name text, not numeric fields or codes.
- **Known regression risk flagged in advance**: fullwidth punctuation is included in the closable range: if any raw reconstructed line concatenates two logically-distinct columns (e.g. a name and an adjacent annotation) with a real inter-column space landing next to a fullwidth punctuation mark, that space could be incorrectly closed. This was explicitly anticipated before implementation, not discovered only afterward — see "Unexpected findings" for where it actually manifested.

## Synthetic tests (frozen before the benchmark re-run)

Added to `scripts/document-understanding/benchmark/src/test.mjs`:

1. `closeCjkWrapSpaces: the actual case-002/003 wide-letter-spacing header pattern closes correctly` — the real observed shape (`総 務 本 省 共 通 費` → `総務本省共通費`).
2. `closeCjkWrapSpaces: does NOT close a space between CJK text and an embedded Latin/ASCII word (negative case)` — `政策 IT 推進費` unchanged.
3. `closeCjkWrapSpaces: does NOT close a space between CJK text and a digit (negative case, beyond the item-code prefix)` — `経費 2024 年度` unchanged.
4. `closeCjkWrapSpaces: closes a space adjacent to fullwidth punctuation, matching the existing single-case-002-glyph convention` — documents the pre-existing, not-new behavior explicitly, rather than leaving it implicit.
5. `closeCjkWrapSpaces: already-clean text is unchanged (idempotent no-op)`.
6. `closeCjkWrapSpaces: re-exported from normalize-docling.mjs is the identical function as common.mjs's` — guards against behavioral drift from the refactor.
7. `normalize.mjs pipeline (via findItemCodeRows + reconstructRow): a wide-letter-spaced pdfjs-baseline header line produces a clean itemNameFragment` — end-to-end through the real extraction regex, synthetic numbers unrelated to any case's Ground Truth.
8. `normalize.mjs pipeline: pymupdf-baseline-style already-clean text is unaffected` — confirms the no-op path through the real function.

All 8 new tests, plus all 26 pre-existing tests (including Docling's own `closeCjkWrapSpaces` tests, now exercising the re-exported reference), pass. Full suite: **34/34**.

## Post-change matrices and scores

| Case | pdfjs-baseline (before → after) | pymupdf-baseline | docling |
|---|---|---|---|
| case-001 | 8/11 → **8/11** (unchanged) | 8/11 → 8/11 | 9/11 → 9/11 |
| case-002 | 3/11 → **4/11** | 4/11 → 4/11 | 3/11 → 3/11 |
| case-003 | 9/11 → **10/11** | 10/11 → 10/11 | 3/11 → 3/11 |

Every prediction in the pre-registration matched exactly.

## Exact before/after differences (classified)

- **case-002, pdfjs-baseline, `item_name_present_among_candidates`**: FAIL → PASS. **Expected improvement.**
- **case-003, pdfjs-baseline, `item_name_present_among_candidates`**: FAIL → PASS. **Expected improvement.**
- **case-001, both flat-line engines, all 11 checks**: byte-identical (verified via normalized-JSON diff, timestamps excluded). **Expected no-change.**
- **All three cases, docling, all 11 checks**: byte-identical. **Expected no-change.**
- **case-002, pdfjs-baseline and pymupdf-baseline, `expense_name_exact_match_after_line_join`'s `actual` string**: changed (space removed adjacent to `（要求要旨）`), but **PASS/FAIL outcome unchanged (both remain FAIL)** — the field was already wrong (contaminated by the pre-existing, explicitly out-of-scope annotation/`splitTrailingTriple` interaction) both before and after. Classified as an **unexpected, but harmless, collateral value change** — see below.
- **case-001, pdfjs-baseline and pymupdf-baseline, `expense_name_exact_match_after_line_join`'s `actual` string**: identically affected (space removed adjacent to `（要求要旨）` in case-001's own annotation-contaminated garbled string), **PASS/FAIL outcome unchanged (FAIL before and after)**. Same classification.
- **case-002, pymupdf-baseline, `item_name_present_among_candidates`'s candidate list**: the *non-target* `経 済 産 業 本 省` (組織-level) candidate's text also changed (spaces closed), while the already-PASSing outcome is unchanged. **Unexpected, harmless.**
- No amount, code, unit, or delta-sign field changed in any case, for any engine. No `item_name_exact_match` flipped anywhere (hierarchy ambiguity remains unresolved, as expected — untouched by this experiment).

**No regressions.** Every check that changed, changed in the pre-registered direction; every check that was pre-registered as unchanged remained unchanged at the byte level.

## Unexpected findings (disclosed, not silently absorbed)

The pre-registration explicitly flagged, as a *known risk*, that fullwidth-punctuation adjacency could close a legitimate inter-column space if a raw line concatenates two logically-distinct columns. **This risk materialized**, in exactly one place per affected case: the already-known, already out-of-scope annotation-contamination artifact (`common.mjs`'s `splitTrailingTriple` failing to anchor on case-001's/case-002's same-line or leaked annotation text, documented in the case-001/case-002 reports) produces an already-garbled `expenseNameFragment` string that happens to contain a real inter-column space immediately before the annotation's opening fullwidth parenthesis (`（要求要旨）` / `（要求要旨）`). Closing CJK-adjacent spaces also closed *this* space, since a fullwidth `（` is inside the closable range.

**Why this is not treated as a regression**: the field was wrong before (garbled, containing leaked annotation text — a pre-existing, separately-diagnosed, explicitly out-of-scope defect) and remains wrong after (still garbled, still containing leaked annotation text, merely with one fewer space inside the garbage). The check's PASS/FAIL outcome — and every other check's outcome — is unaffected. No value that was ever *correct* became *incorrect*, and no value that was *incorrect* became *falsely correct*.

**Why this is still worth recording precisely**: it is genuine evidence that the CJK-space-closing rule's "legitimate-space risk" is not zero when applied to a **flat reconstructed line** that may span multiple logical columns concatenated together (unlike a Docling table cell, which is already column-isolated by construction). This is a real architectural distinction between the two representations that this experiment surfaced, not previously stated explicitly: applying the same rule is *safer* on cell-isolated table representations than on flat, multi-column-concatenated line representations, precisely because the latter can accidentally juxtapose CJK/punctuation text from two unrelated columns. In this experiment's three cases, the risk only ever manifested inside values that were *already* wrong for an unrelated reason, so it caused zero observed harm — but a future case where a **correctly-triple-anchored** line still happens to have two adjacent, legitimately-space-separated CJK/punctuation columns concatenated (without the current annotation-contamination bug) could, in principle, have this rule close a real, meaningful space. This is recorded as a genuine, evidence-based caveat for future case-family work, not a reason to withhold this rule (which produced zero actual harm across three real cases and two genuine improvements).

## Architecture conclusion

The evidence supports classifying this as a **stable, engine-specific normalization rule** (layer 2), not a document-family interpretation rule and not a matching-tolerance shortcut:

- It is confirmed engine-specific: PyMuPDF never needs it; Docling already has its own independently-discovered instance of the identical rule.
- It generalizes across two independently-selected ministries (case-002, case-003) with the identical failure/fix shape, and is correctly inert on a third (case-001) that doesn't exercise the triggering row type.
- It required no case-specific tuning — the exact same function, unit-testable against synthetic inputs unrelated to any case's Ground Truth, fixed both cases identically.

**This is evidence for a reusable strategy, not proof of universality across all Japanese government PDFs.** Both confirming cases share the same producer ("List Creator") and the same general `組織`/`項`/`目` hierarchical table convention; whether pdfjs-dist's gap-threshold reconstruction behaves identically against a document produced by a different tool, or against a document using a different header/emphasis typographic convention (bold instead of letter-spacing, for instance), is unknown and untested. The rule is deterministic and safe to keep active by default (it is a verified no-op where the artifact doesn't occur), but its *predictive* value for a future, unseen document should be stated as "worth checking for, not assumed present."

## Strategy-selection implication

This experiment supports a concrete instance of the general pattern:

> `observable representation feature → transformation strategy → expected downstream effect`

Specifically: **"pdfjs-baseline's raw reconstructed text for a `組織`/`項`-level header row contains inter-character spaces" → apply `closeCjkWrapSpaces` → `item_name_present_among_candidates` becomes recoverable for that candidate.**

Two things must stay carefully separated, per the architecture report's leakage-avoidance rule:

- **The trigger fact ("raw pdfjs-dist output for this row contains CJK-internal spaces") is engine-derived, not source-safe** — it can only be observed after running pdfjs-baseline, and must never be represented as a property of the *document* independent of the engine that read it. A future Document Profile must not record "this document has spaced headers" as a document-level fact; at most, it could record "pdfjs-baseline's raw output for this document exhibited CJK-internal spacing" as an engine-derived, post-hoc observation, exactly like this repository's existing `cjkWrapSpaceArtifactPresent_pdfjs` field already does for case-002/003's `document-profile.json` entries.
- **The *typographic* trigger (wide letter-spacing on header rows) may eventually be source-safe** if a future, purely visual/rasterization-based inspection could reliably detect "this row is rendered with unusually wide character pitch" without running pdfjs-dist at all (e.g. via a PDF glyph-position analysis tool that is not one of the compared engines, mirroring this repository's existing `pdfinfo`-is-safe convention). This experiment did not build or test such a detector — it is a plausible future direction, not a current capability.

No Case Package schema was changed in this task. A useful future field, proposed but not implemented: an engine-derived boolean per case, e.g. `pdfjsCjkSpacingArtifactObserved`, recording whether this specific fix's rule was actually exercised (found and closed at least one space) for that case — letting a future strategy-selection experiment measure, across a larger corpus, how often this fix matters versus how often it is a harmless no-op.

## Files changed

- `scripts/document-understanding/benchmark/src/common.mjs` — added `CJK_RANGE` (exported) and `closeCjkWrapSpaces` (canonical implementation, moved from `normalize-docling.mjs`).
- `scripts/document-understanding/benchmark/src/normalize-docling.mjs` — removed the local `CJK_RANGE`/`closeCjkWrapSpaces` definitions; now imports and re-exports both from `common.mjs`. Docling's own call site and behavior are unchanged (verified byte-identical).
- `scripts/document-understanding/benchmark/src/normalize.mjs` — `reconstructRow` now applies `closeCjkWrapSpaces` to the fully-assembled item/expense name.
- `scripts/document-understanding/benchmark/src/test.mjs` — 8 new tests (listed above).
- `evidence/document-understanding/{case-001,case-002,case-003}-results.json`, `reports/document-understanding/{case-001,case-002,case-003}-evaluation.md` — regenerated by the unmodified `run.mjs`, reflecting the new, semantically-changed results for case-002/case-003 and byte-identical (modulo timestamps) content for case-001.
- `reports/document-understanding/20260926_1816_CJK_Spacing_Strategy_Layer_Experiment.md` (this file).
- `state/CURRENT_STATE.json`, `state/TODO.md`, `state/CHANGELOG.md`.

No Ground Truth, selection protocol/record, source lock/raw file, `evaluate.mjs`, any adapter, or Case Package file was modified. No ADR was added: this closes a previously-documented normalization gap (already flagged as a cross-case finding in the case-002 and case-003 reports) using an already-established architectural pattern (engine-specific normalization, per ADR-010), not a new methodological decision.

## Validation

```bash
npm run validate           # PASS
npm run extraction:test    # PASS
npm run docbench:test      # PASS (34/34)
git diff --check           # clean
```

All three cases re-run via the now-reliable `docbench` harness (post-`7b905a1`); Ground Truth (`git diff` on all three cases' `ground-truth.json`), selection protocol/record, and `sources/source-lock.json`/`sources/raw/` all reverified unchanged before commit.

## Remaining uncertainty

- Whether this rule generalizes beyond documents produced by "List Creator" with the same `組織`/`項`/`目` header-styling convention is untested — case-002 and case-003 are the only two confirming instances, and both share that producer.
- The fullwidth-punctuation-adjacency risk identified above has not caused observed harm in three cases, but was only ever tested against pages where it happened to land inside an already-wrong value. A case where it could interact with an otherwise-correct value has not been constructed or observed.
- Whether PyMuPDF's own reconstruction could ever exhibit this artifact under some other document/font combination is unknown — it was never observed to in any of the three cases, but the mechanism (a gap-threshold heuristic) is pdfjs-dist-specific by design, not proven absent from PyMuPDF's algorithm in general.

## Recommended next research task (not executed)

Investigate whether the fullwidth-punctuation-adjacency risk identified in this experiment can manifest against an otherwise-correctly-extracted value — specifically, construct or locate a case where a flat-reconstructed line legitimately concatenates two CJK/punctuation-adjacent columns *without* the pre-existing annotation-contamination bug present, to determine whether `closeCjkWrapSpaces` needs a narrower scope (e.g. excluding fullwidth punctuation, or requiring the closure to occur only within a single already-column-isolated fragment) before it is relied upon more broadly across a larger future case corpus.
