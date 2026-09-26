# CJK Fullwidth-Punctuation Boundary Experiment

Status: **safety experiment complete. Decision: KEEP. No production code changed.**

Date: 2026-09-26 (Asia/Tokyo)

## Research question

> Can `closeCjkWrapSpaces` remove semantically legitimate whitespace around fullwidth punctuation in an otherwise-correct value, and if so, is there enough evidence to narrow the rule now?

## Current rule characterization

`closeCjkWrapSpaces` (`scripts/document-understanding/benchmark/src/common.mjs`) closes any whitespace run strictly between two characters both matching:

```text
CJK_RANGE = '　-ヿ㐀-䶿一-鿿＀-￯'
```

Decoded precisely (verified programmatically, not assumed from the literal's appearance):

| Sub-range | Codepoints | Contents |
|---|---|---|
| 1 | U+3000–U+30FF | Ideographic space, CJK Symbols and Punctuation (`、。「」『』【】〔〕・` etc.), Hiragana, Katakana |
| 2 | U+3400–U+4DBF | CJK Unified Ideographs Extension A |
| 3 | U+4E00–U+9FFF | CJK Unified Ideographs (main block) |
| 4 | U+FF00–U+FFEF | Halfwidth and Fullwidth Forms — **including fullwidth ASCII-equivalents**: fullwidth digits `０-９`, fullwidth Latin letters `Ａ-Ｚ`/`ａ-ｚ`, fullwidth punctuation `（）［］：；～` etc., and halfwidth katakana |

**Explicitly encoded vs. falls out of the character class** (this distinction was not previously stated precisely):

- **Explicitly intended** (per the existing code comments, both before and after the CJK Spacing Strategy Layer Experiment): closing a wrap-induced space between two ordinary CJK ideographs/kana, and leaving a space next to an ASCII digit or ASCII Latin letter (the "item code" case) alone.
- **Falls out of the character class, not previously stated as a deliberate design decision**: fullwidth brackets/quotes (`（）「」『』【】［］`), fullwidth commas/colons/semicolons (`、。：；`), the katakana middle dot (`・`), fullwidth tilde/wave dash (`～〜`), and — the one genuinely new finding this experiment surfaces — **fullwidth digits and fullwidth Latin letters** (`０-９`, `Ａ-Ｚ`, `ａ-ｚ`) are all inside `CJK_RANGE` and therefore all have adjacent whitespace closed, exactly like ordinary kanji. This was never explicitly decided; it is a byproduct of choosing the Halfwidth/Fullwidth Forms block as "the fullwidth range" without narrowing it further.
- **Explicitly, correctly excluded**: `△` (U+25B3, a math/geometric symbol, not in the Halfwidth/Fullwidth Forms block) is never affected — confirmed by direct codepoint testing, not merely assumed. This matters because `△` is this benchmark's decrease-glyph convention; a rule that touched it could have interacted badly with delta-sign evaluation, and it provably does not.

## Corpus evidence (exhaustive, not spot-checked)

Searched every raw line in all six flat-line artifacts (`pdfjs-baseline`/`pymupdf-baseline` × case-001/002/003) for every occurrence of `、。「」『』【】〔〕・（）：；［］～〜` adjacent to whitespace. Complete result set:

| Instance | Classification | Basis |
|---|---|---|
| case-001: `"...必要な （要求要旨）"` (both engines) | **Already-corrupted value; cannot establish safety** | Part of the pre-existing, out-of-scope annotation-contamination artifact (documented in the case-001 report and the CJK Spacing Strategy Layer Experiment) — the field already fails `expense_name_exact_match_after_line_join` before and after closing this space |
| case-002: `"...4,556,824 （要求要旨）"` and `"必要な経費 「経済産業省設置法」..."` (both engines) | **Already-corrupted value; cannot establish safety** | Same root cause as above, confirmed already-failing before and after |
| case-002/case-003: `"経（本） 5"` / `"総（本） 5"` (printed page-label lines, both engines) | **Never exposed to the rule at all** | This line never matches `ITEM_CODE_RE` or `EXPENSE_ROW_RE` (it doesn't start with a 3-digit code or a request-number+expense-code pair), so it is never extracted as an `itemNameFragment`/`expenseNameFragment` and `closeCjkWrapSpaces` is never called on it in practice, regardless of what it contains |

**No instance was found, across an exhaustive search of the entire corpus, where a fullwidth-punctuation-adjacent space appears inside a value that is (a) actually passed through `closeCjkWrapSpaces` in the real pipeline and (b) otherwise correct.** Every real occurrence is either irrelevant (never reaches the function) or already known to be wrong for an unrelated, previously-documented reason.

**A separate, genuinely new real-corpus finding** (not about legitimate-space destruction, but about the fullwidth-digit boundary specifically): every one of the three cases' pdfjs-baseline raw output contains a title/header line of the shape `"令 和 ６ 年 度 歳 出 概 算 要 求 額 明 細 表"` or `"要求 前 年 度 ６ 年 度 対 前 年 度"`, where the fullwidth digit `６` sits inside the same uniformly wide-spaced header run as the surrounding kanji. Because fullwidth digits are inside `CJK_RANGE`, the current rule correctly closes the spaces around `６` along with the surrounding kanji — this is **beneficial, not harmful**, in every real instance found. No instance of an ASCII-digit-adjacent space being incorrectly closed was found (ASCII digits are outside `CJK_RANGE` by construction, confirmed both by the existing item-code test and by direct codepoint testing above).

## Synthetic boundary tests

8 new tests added to `scripts/document-understanding/benchmark/src/test.mjs`, all passing against the **unmodified** rule (documenting current behavior, not proposing new behavior):

1. Closes a space before an opening fullwidth paren — matches the real corpus pattern.
2. Closes spaces padded just inside fullwidth parens — same mechanism, not verbatim-observed but directly analogous.
3. Closes a space before an opening fullwidth quote mark — matches the real corpus pattern.
4. Closes a space adjacent to a fullwidth digit embedded in CJK text — the genuinely new boundary this experiment's corpus search surfaced, confirmed safe by exhaustive search, not assumed.
5. Closes a space adjacent to a fullwidth Latin letter — **synthetic only**; no fullwidth Latin letter was found anywhere in the corpus. Documented as an untested boundary, not a validated real-world need.
6. `△` is never affected — confirms the delta-glyph convention is safe from this rule by construction.
7. **Explicitly marked ambiguous, not certified**: a space after an ideographic comma (`、`) between two short CJK phrases (`国、 地方`). No corpus evidence exists either way for whether such a space could ever be intentional in a stylized document; the test locks in current behavior for regression-tracking only, with an explicit comment that this is not a claim of semantic correctness.

Per the task's instruction, no test invents a "universal expected output" for a case whose intent is genuinely context-dependent — test 7 documents current behavior explicitly as ambiguous rather than asserting it is correct.

## Decision: has the current rule enough context, and is it safe enough?

**Question posed**: can a character-local helper safely distinguish artifact spacing from meaningful punctuation-adjacent spacing?

**Answer, from the evidence above**: yes, well enough for continued use, with one honestly-stated limitation. The rule cannot and does not attempt any structural/semantic reasoning — it is purely character-class-local. In this document family's actual typographic convention (as evidenced by an exhaustive search of all currently-available real data), that turns out to be sufficient: Japanese prose in this document family does not pad whitespace around fullwidth punctuation as a deliberate style choice, so every real occurrence found is unambiguously either an artifact (correctly closed) or irrelevant (never reached). No real occurrence was found where the rule's character-local ignorance of structure caused it to destroy something meaningful.

**Decision: KEEP.** Neither "narrow" nor "defer" is supported by the evidence:

- **Not narrow**: no clearly-unsafe punctuation class was found. Excluding fullwidth digits/letters from the closable range, for instance, would have made the correctly-beneficial `６`-adjacent-space closures (found in every case) stop happening, for a risk that was never observed. That would be optimizing against a hypothetical, not a demonstrated problem — exactly what the task warns against ("Do not compensate for missing context by creating an increasingly elaborate regex fitted to three PDFs").
- **Not defer**: the evidence does not show that *structural* context is currently needed to make this rule safe — the character-local approach has caused zero observed harm across an exhaustive search, not merely a lucky spot-check.
- **Not insufficient evidence**: the corpus search was exhaustive (every fullwidth-punctuation-adjacent-whitespace instance in six raw artifacts), not partial, and produced a clear, decidable answer.

No production code was changed. This is an explicitly valid, complete result, per the task's own framing.

## Pre-registered change

None — no change was implemented, so there is nothing to pre-register. This section is intentionally empty; the decision to keep the current rule was reached *before* any hypothetical new behavior would have needed freezing.

## Implementation

None. `scripts/document-understanding/benchmark/src/common.mjs`, `normalize.mjs`, and `normalize-docling.mjs` are byte-for-byte unchanged from `bac939b`.

## Tests

8 new characterization tests (listed above) plus all 35 pre-existing tests: **43/43 passing**, exit code 0, confirmed via direct log inspection (not just a visual scan of PASS lines).

## Benchmark regression results

**Not rerun, by design.** Per the task's own guidance ("a full expensive rerun is optional when focused tests plus existing evidence are sufficient; explain the decision"): production normalization code is byte-for-byte unchanged from the already-validated `bac939b` state (confirmed via `git diff --stat` returning empty for all three normalizer files), so re-running the benchmark would only re-confirm already-established, unchanged results at the cost of Docling inference time for zero new information. The 43-test suite directly exercises every boundary condition raised by this experiment, and the exhaustive corpus scan already confirms no untested real-world instance exists in the committed evidence.

**Confirmation that the case-002/case-003 strategy benefit remains understood and untouched**: since no code changed, the `bac939b` results stand exactly as committed — case-002 pdfjs-baseline 4/11 (via `item_name_present_among_candidates` PASS), case-003 pdfjs-baseline 10/11 (same), case-001 8/11/8/11/9/11, PyMuPDF and Docling stable across all three cases. Verified by re-reading the currently-committed `evidence/document-understanding/{case-001,case-002,case-003}-results.json` (unchanged on disk, matching state-file records) rather than re-deriving them.

## Architecture implication

The engine-normalization strategy (layer 2, per ADR-010, established in the CJK Spacing Strategy Layer Experiment) has, on the evidence available so far, a **safe enough punctuation boundary for continued experimentation** in this document family. This is a narrower claim than "safe for all Japanese documents": the boundary's safety rests on an empirical property of the three currently-available cases (no deliberate punctuation-adjacent padding in this document family's typesetting convention), not a proof that character-local reasoning is *generally* sufficient for Japanese text. If a future case (e.g. `case-004`, from a different producer/ministry) is found to use a typographic convention with genuinely intentional punctuation-adjacent spacing, that would be new evidence requiring this decision to be revisited — not something this experiment can rule out in advance. This is recorded as a property of layer 2's current safe operating range, not a claim that structural/semantic context (layer 3+) will never be needed.

## Remaining uncertainty

- Fullwidth Latin letters adjacent to CJK text remain synthetically-tested only; no real corpus instance exists yet to confirm the rule's behavior there is beneficial rather than merely untested.
- The single ambiguous case (ideographic comma + space) is documented, not resolved — genuinely context-dependent intent cannot be settled by a character-local rule or by the corpus available.
- This experiment used the same three cases as its evidence base as the strategy it is safety-checking; a fourth, structurally different case is the natural next source of either confirming or falsifying evidence, not assumed here.

## Files changed

- `scripts/document-understanding/benchmark/src/test.mjs` — 8 new characterization tests only. No other file changed.
- `reports/document-understanding/20260926_1935_CJK_Fullwidth_Punctuation_Boundary_Experiment.md` (this file).
- `state/CURRENT_STATE.json`, `state/TODO.md`, `state/CHANGELOG.md`.

No production normalization code, Ground Truth, selection protocol/record, source lock/raw file, evaluator, or Case Package file was modified. No ADR was added: this experiment confirmed an existing decision (ADR-010's engine-specific-normalization placement) remains sound rather than establishing a new one.

## Validation

```bash
npm run validate           # PASS
npm run extraction:test    # PASS
npm run docbench:test      # PASS (43/43)
git diff --check           # clean
```

Ground Truth, selection protocol/record, and `sources/source-lock.json`/`sources/raw/` reverified unchanged for all three cases before commit. No benchmark rerun performed, per the explained decision above; existing committed evidence/report files for all three cases are untouched.

## Recommended next task

Given the current rule is confirmed acceptable and no further normalization experiment is justified by evidence, **case-003 (and this branch's accumulated work) appears mature enough to package for review**: prepare a PR from `research/case-003-mic-preregistration` covering the MIC source acquisition, selection protocol/record, Ground Truth, the harness-reliability fix, and the two CJK-spacing experiments, rather than inventing a further normalization experiment merely to continue research. This is recommended, not executed, per the task's instructions.
