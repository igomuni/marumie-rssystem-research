# Five-Ministry Interim Synthesis — case-001 through case-005

Status: **read-only synthesis of already-committed evidence. No new benchmark, Ground Truth, extraction, normalization experiment, source inspection, or production change performed.**

Date: 2026-09-27 (Asia/Tokyo)

## 1. Executive summary

Across five independently surveyed ministries/agencies (デジタル庁, 経済産業省, 総務省, 文部科学省, 国土交通省), this research program has established a repeatable, preregistered methodology for source acquisition, row selection, Ground Truth freezing, and first-frozen benchmarking of three document-understanding engines (`pdfjs-baseline`, `pymupdf-baseline`, `docling`) against Japanese government budget-request PDFs. The single most robust cross-case finding is that `item_name_exact_match` fails for every engine in all five cases — but, contrary to a naive reading, the underlying mechanism is **not uniform** across cases (§11). Four independent, semantic-label-free anomaly-observation channels were developed on case-004 (MEXT) and one was explicitly, deliberately falsified at broader scale rather than allowed to stand as an overstated success (§14). Context-recovery requirements were shown to require at least two genuinely different mechanisms (page-local vs. table-wide-once), not one "look at the previous page" fix (§13). This report synthesizes only what is already committed to the repository; it makes no claim stronger than the underlying evidence supports, and explicitly flags single-case observations as such rather than generalizing them to "all Japanese government documents."

## 2. Scope / non-goals

This task performs **synthesis only**: no new PDF inspection, no new row selection, no Ground Truth creation or change, no benchmark rerun, no extraction rerun, no normalization experiment, no production code change, no evaluator change, no anomaly-detector tuning, no actual MOF CSV matching, no RS 1000× investigation, no case-006 source survey, and no Case Package/Strategy Selection implementation. Every claim below is traced to a specific, already-committed repository artifact; where evidence is genuinely absent, this report says so explicitly (`not established`) rather than filling the gap by inference or memory.

## 3. Evidence base / chronology

This report was written by reading, in this order: `sources/source-lock.json` and `sources/source-registry.csv`; each case's `fixtures/document-understanding/case-NNN/ground-truth.json` and its accompanying selection protocol, selection record, and Ground Truth evidence documents; each case's compact benchmark evidence (`evidence/document-understanding/case-NNN-results.json`) and current evaluation report (`reports/document-understanding/case-NNN-evaluation.md`); every timestamped experiment/diagnostic/anomaly-survey report; `state/CURRENT_STATE.json`, `state/TODO.md`, and `state/CHANGELOG.md`; and `protocol/DECISIONS.md`'s ADR-010 (layer taxonomy) as the canonical architecture vocabulary. Chat/prior-handoff memory was used only as a navigation aid to locate the correct files — every factual claim below was re-confirmed against the committed artifact itself, not asserted from memory.

Branch: `research/case-005-mlit-source-survey`; pre-task `HEAD` `6d16324`; `origin/main` `34c9424` (fresh-fetched, confirmed unchanged). This synthesis is committed on the case-005 branch, per the originating task's own instruction; it is not merged and no PR is created.

## 4. Five-case inventory

| Field | case-001 | case-002 | case-003 | case-004 | case-005 |
|---|---|---|---|---|---|
| Ministry/agency | デジタル庁 (Digital Agency) | 経済産業省 (METI) | 総務省 (MIC) | 文部科学省 (MEXT) | 国土交通省 (MLIT) |
| Fiscal year | 2024 | 2024 | 2024 | 2024 | 2024 |
| Official source | `digital-r6-request-table-01` | `meti-fy2024-general-account-request` | `mic-fy2024-general-account-expenditure-request` | `mext-fy2024-general-account-expenditure-request-detail` | `mlit-fy2024-general-account-expenditure-request` |
| Packaging | `not established` (no packaging-model record exists for this source; page count itself is `not_recorded` in its own Case Package) | Single combined PDF (総表+明細表+定員表) | Single combined PDF (総表+明細表+定員表) | Four separate sibling PDFs (表紙・目次/総表/明細表/定員表), this source = 明細表 only | Single combined PDF (目次+総表+明細表) |
| Page count | `not established` | 106 | 454 | 1,339 | 1,097 |
| Producer / encryption | `not established` | "List Creator" / not encrypted | "List Creator" / not encrypted | no recorded Producer for this specific file / permission-only AES-256 encrypted | "List Creator" / not encrypted |
| Selected organization | n/a (item-level row, not organization-scoped selection) | `010 経済産業本省` | `010 総務本省` | `010 文部科学本省` | `010 国土交通本省` |
| Selected item | `020 情報通信技術調達等適正・効率化推進費` | `010 経済産業本省共通費` | `010 総務本省共通費` | `010 文部科学本省共通費` | `002 国土交通本省共通費` |
| Selected expense/request | req. `4`, code `01-95`, `情報通信技術調達等適正・効率化の推進に必要な経費` | req. `①`→`1`, code `01-95`, `経済産業本省一般行政に必要な経費` | req. `①`→`1`, code `01-95`, `総務本省一般行政に必要な経費` | req. `①`→`1`, code `01-95`, `文部科学本省一般行政に必要な経費` | req. `①`→`1`, code `05-95`, `国土交通本省一般行政に必要な経費` |
| `pdfPageIndex` | 11 | 8 | 8 | 2 | 28 |
| Unit evidence scope | `千円`, scope not independently re-documented in a dedicated GT-evidence file (case-001 predates that convention) | page-level, confirmed on target page | page-level, confirmed on target page | **table-wide, established from the file's own first page**, not present on the target's own page | page-level, confirmed on target page |
| Selection protocol freeze | `not established` (case-001 predates the preregistered-protocol methodology entirely — no selection protocol document exists for it) | `4432492` | `8b65364` | `c2b2c28` | `9b292c0` |
| GT freeze | (backfilled retrospectively; see `document-profile.json`) | `5a2eb32` | `1bc6c4e` | `f9b2f35` | `e1ed08e` |
| First-frozen benchmark point | earliest commit of case-001's own `ground-truth.json`/evaluation, predating this program's "first-frozen-then-current" convention | `379043d` | `aa57caf` | `49f5ca6` | `6d16324` |
| Current score (pdfjs/pymupdf/docling) | 8/11, 8/11, 9/11 | 4/11, 4/11, 3/11 | 10/11, 10/11, 3/11 | 7/11, 7/11, 5/11 | 10/11, 10/11, 10/11 |
| First-frozen score, if different from current | not distinguished as a separate historical event in this program's own convention (never adapted after its own freeze, so first=current: 8/8/9) | **2/11, 3/11, 2/11** (`379043d`) → evaluator fix → 3/11, 4/11, 3/11 (`519ce28`) → CJK fix → **current 4/11, 4/11, 3/11** | **9/11, 10/11, 3/11** (`aa57caf`) → CJK fix → **current 10/11, 10/11, 3/11** | 7/11, 7/11, 5/11 (`49f5ca6`) — **identical to current; no adaptation applied** | 10/11, 10/11, 10/11 (`6d16324`) — **identical to current; no adaptation applied yet** |

Unknown values are recorded as `not established`, not inferred. Case-001's own Case Package (`document-profile.json`) explicitly marks `pageCount`, `pdfProducer`, and `pageOrientation` as `"not_recorded"` with the note "unknown != zero: this is an absence of a recorded fact, not evidence the document has 0 pages" — that same discipline is preserved here rather than silently filled in.

## 5. Source/packaging comparison

| Dimension | case-001 | case-002 | case-003 | case-004 | case-005 |
|---|---|---|---|---|---|
| Combined vs. split | `not established` | Combined | Combined | **Split** (4 sibling files) | Combined |
| Encryption | `not established` | None | None | **Permission-only AES-256** | None |
| Toolchain (Producer) | `not established` | List Creator | List Creator | No recorded Producer for this file; sibling files show List Creator or Acrobat Distiller/PScript5.dll | List Creator |
| Internal organization count (per source's own TOC) | n/a | `not established` beyond target | 5 (総務本省 + 4 external bureaus) | 2+ known (010, 020; further ones un-surveyed) | **12** (widest surveyed) |
| Detail-table 目次 granularity | n/a | `not established` | organization/item-level | organization/item-level | **expense-line-level**, with page cross-references — markedly more granular than any other surveyed case |
| 総表 richness | n/a | `not established` | `not established` | n/a (総表 lives in a separate sibling file, not deeply inspected) | **Already itemized to expense-code level**, with an explicit `明細書頁数` cross-reference column into 明細表 — not documented as present in any other case |

## 6. Common ledger/table structure

Confirmed present, by direct source-evidence citation, in **all five** cases:

- A 組織 (organization) → 項 (item) → 経費 (expense/request) hierarchy.
- A 要求番号 (request number) column, printed as a circled numeral for low numbers (`①`) and as a plain integer for higher numbers (MLIT's `111`-style numbers observed in case-004's later pages; not itself part of any of the five selected rows except as the normalized `"1"`/`"4"` convention).
- An 経費コード (`NN-NN`-format expense code — `01-95` in cases 002/003/004, `05-95` in case-005; case-001 uses the same `NN-NN` shape, `01-95`).
- A three-column 前年度予算額 / 6年度概算要求額 / 対前年度比較増△減 amount structure, with the `△` decrease-glyph convention (confirmed genuinely present and rendering correctly, on some row, in every case's own document — though not necessarily on the *selected* row itself: case-001's own selected row does carry `△`; cases 002/003/004/005's selected rows do not, each independently confirmed via a different row on the same page).
- A 備考 (remarks) column, present as a table column in every case, though populated with contaminating same-line text only in case-002 (§9 of case-002's own evidence) and empty on the selected row in cases 003/004/005.
- A 千円 (thousand-yen) unit label, in every case where a target-page unit label was found at all (cases 002/003/005 directly on-page; case-004 established table-wide from a different page; case-001's own value is `"千円"` in its `ground-truth.json` but the evidence trail establishing its scope was not committed as a separate document, since case-001 predates that convention).
- Organization- and item-level aggregate rows (no native expense code) that must be, and consistently were, excluded from row eligibility across every selection protocol that exists (case-002 onward).
- Deep nested subordinate numbered breakdown lines (the `95016-NNNN-NN-NNNN`-shaped codes) beneath the selected row, confirmed present in cases 002/003/004/005 (case-001's own selected row's own immediate sub-structure was not documented to the same depth).

This list is deliberately not extended further: several near-identical-looking features (e.g. exact code-column widths, exact remarks-column population conventions) are **not** claimed as universal, since they were not independently re-verified across all five cases' own full page structure — only the specific rows and pages actually inspected.

## 7. Ministry/document-family differences

Distinguishing genuine ministry/document-family differences from mere selected-page differences, per the originating task's own caution:

- **Genuine document-family differences** (confirmed to vary at the packaging or document-wide-convention level, not merely because a different page was selected): case-004's four-file split (a packaging fact true of the whole document, not one page); case-004's document-wide encryption; case-005's unusually granular 目次 and richly cross-referenced 総表 (both document-wide structural facts, confirmed by inspecting the 目次/総表 themselves, not merely the selected row's own page); case-002's own known annotation-contamination pattern (confirmed, in case-002's own evidence, to be a property of that specific row's own remarks-column placement — not yet established as a document-wide MET convention, since no other METI row was inspected).
- **Selected-page-specific, not necessarily ministry-wide, differences**: case-004's item-header-on-preceding-page finding is a property of *that specific row's own position* within MEXT's document — the organization-010/020 diagnostics (§13) explicitly confirmed the *opposite* (same-page item context) occurs on roughly half of a sampled set of MEXT's own other rows, so this is not a MEXT-wide packaging consequence, it is a per-row pagination fact (already explicitly disclosed in the original diagnostic, and repeated here to avoid the misattribution the originating task specifically warned against).
- **Unclear / not yet distinguished**: whether case-005's same-page item-context finding (§9) is typical of MLIT's own document family or specific to this one selected row was not investigated — no MLIT-equivalent context diagnostic (of the kind performed for case-004) has been run.

## 8. Selection/GT methodology

The methodology matured over the course of five cases, without ever silently rewriting an earlier case's own already-frozen artifacts:

1. **Source survey** (independent-route discovery, acquisition, immutable SHA-256 locking) — present for every case from case-002 onward; case-001 predates this repository's own current source-acquisition tooling.
2. **Selection protocol freeze** (deterministic, source-structural eligibility criteria, explicit non-criteria, tie-break, all committed *before* any candidate row is inspected) — introduced starting case-002, refined at each subsequent case by *critiquing*, not copying, the prior case's own criteria (e.g. case-004 reclassified "correct table" from a row-level criterion to a source/universe precondition because MEXT's own packaging made that reclassification source-justified; case-005 independently re-derived the same reclassification for a different, source-justified reason — MLIT's own exact TOC-stated 明細表-start page — explicitly not copying case-004's own packaging-based rationale).
3. **Deterministic row selection** (visual-inspection-only enumeration in document order, stopping at the first eligible row, never comparing against later candidates) — consistently applied case-002 through case-005.
4. **Selection freeze** (a separate, committed artifact, before Ground Truth) — consistently applied case-002 through case-005.
5. **Direct-visual Ground Truth** (raw transcription kept separate from normalized value; delta sign read from glyph evidence alone, corroborated — never inferred — via a different row's own glyph on the same document; arithmetic validation performed only *after* independent transcription, never used to backfill a value) — consistently applied, and **progressively more rigorously documented**: case-005's own GT-evidence document explicitly re-verifies the selection record's own locator before any transcription begins, a step not explicitly documented as a discrete task step in earlier cases (though not contradicted by them either).
6. **First benchmark before adaptation** (run once, preserved regardless of outcome, reproducibility-checked via a second run) — consistently applied case-002 through case-005; case-002 and case-003 later received *disclosed, separately-committed* normalization improvements (the evaluator fix and the CJK-spacing rule, respectively) that were explicitly never applied retroactively to silently improve the *historical* first-frozen numbers — those remain preserved, recoverable via `git show`, in the commits cited in §4's table.
7. **Failure preservation**: case-002's first frozen benchmark (2/11, 3/11, 2/11) and case-003's docbench harness-reliability bug were both preserved and investigated as findings in their own right, never quietly patched away before being recorded.

No case's Ground Truth, selection protocol, or selection record was altered by this synthesis task.

## 9. First-frozen vs. current benchmark results

Repeating §4's table in check-matrix form, with first-frozen and current results kept explicitly distinct wherever they differ (per the originating task's own strongest caution):

| Case | First-frozen (pdfjs/pymupdf/docling) | Intervening change(s) | Current (pdfjs/pymupdf/docling) |
|---|---|---|---|
| case-001 | 8/11, 8/11, 9/11 | none recorded | 8/11, 8/11, 9/11 |
| case-002 | **2/11, 3/11, 2/11** | evaluator-overfit fix (`delta_glyph_observed_and_associated` → `delta_sign_evidence_matches_source`) → 3/11, 4/11, 3/11; then shared CJK-spacing normalization → | **4/11, 4/11, 3/11** |
| case-003 | **9/11, 10/11, 3/11** | shared CJK-spacing normalization → | **10/11, 10/11, 3/11** |
| case-004 | 7/11, 7/11, 5/11 | none (post-freeze work was diagnostic/anomaly research only, never a normalization change) | 7/11, 7/11, 5/11 |
| case-005 | 10/11, 10/11, 10/11 | none (freshest case; no adaptation task has run) | 10/11, 10/11, 10/11 |

**It is explicitly false to say "case-003 scored 10/11 from the start"** — it scored 9/11 on pdfjs-baseline at first freeze; the improvement is a disclosed, separately-committed, cross-case-validated normalization change (§11 below), not a re-selection or re-transcription.

## 10. Cross-engine comparison

**pdf.js / PyMuPDF (flat-line engines)**: identical scores in every one of the five cases (8/8, 4/4, 10/10, 7/7, 10/10) — both reconstruct flat text lines from coordinates and are affected identically by every normalization rule tested so far (`closeCjkWrapSpaces`, `reconstructNumericToken`'s flat-engine analog is not needed for them since they don't reverse comma groups). The only documented behavioral *difference* between them across all five cases is cosmetic — pymupdf's own line-reconstruction sometimes produces wider inter-token spacing or fuses a longer run of continuation text onto one line than pdfjs does (observed in case-004's and case-005's own diagnostic candidate outputs) — with **zero observed effect on any PASS/FAIL outcome** in any of the five cases.

**Docling**: shows the most case-to-case variance of the three engines — 9/11 (case-001, its best relative showing), 3/11 (case-002, case-003), 5/11 (case-004), 10/11 (case-005, matching the flat engines for the first time). Four **distinct** underlying mechanisms have been documented for Docling's own failures across these cases, not one general "Docling is worse at tables" finding: case-002's row-under-pairing (silently selecting a wrong, structurally-plausible row), case-003's row-over-merging (collapsing multiple rows into one cell), case-004's column-fusion (an apparently-empty visual column fragmenting two amount cells into one), and case-005's **absence** of any of the above on this specific page. **This variance itself is the finding** — Docling's own table-segmentation behavior is highly sensitive to a given page's specific column/row geometry, not uniformly weaker or stronger than the flat-line engines in general. Averaging Docling's five scores (9,3,3,5,10 → mean 6.0) into a single "Docling scores X on average" statement would actively obscure this — no such average is presented as a conclusion here.

## 11. `item_name_exact_match` cross-case finding

**Confirmed across all 5 cases, all 3 engines (15/15 individual check results): FAIL.** This is the single most consistent outcome-level finding in this program.

**However, the underlying mechanism is heterogeneous, not uniform** — re-confirmed directly from each case's own committed comparison matrix (§9 of this report; full data in each case's own `reports/document-understanding/case-NNN-evaluation.md`):

| Case | `item_name_present_among_candidates` (pdfjs/pymupdf/docling) | Underlying mechanism |
|---|---|---|
| case-001 | PASS/PASS/PASS | The correct item-code candidate is genuinely present and correctly reconstructed by all three engines; `item_name_exact_match` still fails only because more than one item-code-shaped row exists on the page (the `singleItem`-requires-exactly-one-candidate resolution rule cannot disambiguate) — a pure **hierarchy-ambiguity** failure, with the underlying extraction itself fully correct. |
| case-002 | PASS/PASS/**FAIL** | Flat engines: same hierarchy-ambiguity pattern as case-001. Docling: the correct candidate itself was **not** correctly reconstructed among the candidates at all — a genuinely different, engine-extraction-level failure, not merely an ambiguity-resolution failure. |
| case-003 | PASS/PASS/**FAIL** | Same split as case-002 — flat engines fail on ambiguity alone; Docling fails at the candidate-reconstruction level (row-over-merging, per §10). |
| case-004 | **FAIL/FAIL/FAIL** | A **different failure entirely from every other case**: the genuine item-header row is **absent from the target's own page** (it is on the immediately preceding page) — a document/layout-family-interpretation-layer context-availability failure, not a same-page ambiguity or a candidate-reconstruction failure. All three engines fail for the identical reason here, since none can see a page they were never given. |
| case-005 | PASS/PASS/PASS | Same as case-001 — pure hierarchy-ambiguity, with the correct candidate genuinely present and correctly reconstructed by every engine. |

**Conclusion, stated at the correct strength**: the outcome (`item_name_exact_match` FAIL) is a **confirmed-across-all-5-cases outcome**, but its cause is **heterogeneous**: pure same-page hierarchy ambiguity (cases 001, 005, and the flat engines in 002/003), same-page ambiguity *compounded by* a genuine Docling extraction failure (Docling in 002/003), and total context absence (all three engines in case-004). Describing this as "one bug" or "one failure mode" would misrepresent the evidence. What *is* genuinely uniform is the **evaluator's own semantics**: `item_name_exact_match` requires a single, unambiguous, correctly-reconstructed item-code candidate to resolve into `result.itemName`, and no case has yet produced a page where that precondition holds for any engine — this is a property of how demanding the check is relative to real document density (organization/item/subordinate-breakdown codes routinely share the same generic 3-digit-prefix shape), not evidence of one specific, fixable bug.

## 12. Context-scope findings

Following case-004's own organization-010/020 diagnostics (`187a8e9`, `aedea1c`), three genuinely distinct context mechanisms are now documented, not one:

1. **Page-local context**: fields recoverable from the target page alone (expense code, label, amount triple, in every case studied). This is what the current single-page-scope architecture already handles.
2. **Neighbor-page structural context**: item-header recovery, shown (case-004's own combined 8+3=11-sample survey) to require, at most, a **zero-or-one-page lookback** in every instance actually checked — never more than one page back, in 11/11 sampled boundaries across two organizations. This is a categorically different mechanism from #3 below, requiring a bounded, small, page-adjacency-aware context window, not a document-wide search.
3. **Table/document metadata**: unit-label recovery, shown (case-004) to sometimes require reading a single, far-away, table-wide-once declaration (MEXT's own first page, ~2 pages before the target in absolute terms but conceptually "anywhere in the table," not "the previous page") — a fundamentally different retrieval problem from #2, since no fixed page-distance bound was established or would even be the right kind of bound to look for.

**case-005 provides a clean contrast case, not a refutation**: both item-header context (§11) and unit context (§9 of case-005's own GT evidence) were found **directly on the target's own page** — i.e., mechanism #1 sufficed for both, on this specific row. This does not contradict the case-004 findings; it simply demonstrates that a *given* row's own context requirements are a property of that row's specific position, and a real benchmark architecture would need to handle the full range (page-local, neighbor-page, and table-metadata) since different rows within the same or different documents can fall into any of the three.

## 13. CJK-spacing normalization study

Traced across its full documented history, not restated as a single fact:

- **Origin**: first implemented as a Docling-only rule in `normalize-docling.mjs`, because Docling's own cell-text assembly was observed inserting spurious spaces between CJK characters in wide-letter-spaced header/total rows.
- **case-001 control**: never exhibits the artifact on its own target page — used, after the fact, as a zero-artifact control confirming the rule's effect is isolated to the specific rows it was designed for, not a general side effect.
- **case-002/003 effect**: the identical artifact was found, independently, in `pdfjs-dist`'s own flat-line reconstruction of header/total-style rows in both documents (both produced by the "List Creator" toolchain). Before implementing anything, four candidate architectural layers were explicitly compared (extraction, engine-specific normalization, document-family interpretation, semantic-matching tolerance); engine-specific normalization was chosen on evidence (PyMuPDF never exhibits it; the artifact's mechanism — pdfjs-dist's gap-threshold line reconstruction — is engine-specific, not engine-independent, per ADR-010's own definition of the document-family-interpretation layer). The shared implementation was moved to `common.mjs` and pre-registered predictions (case-002 pdfjs 3→4/11, case-003 pdfjs 9→10/11, all else unchanged) matched exactly.
- **Boundary safety check**: a dedicated follow-up experiment exhaustively searched every fullwidth-punctuation-adjacent whitespace instance across all six then-existing flat-line raw artifacts, confirming the rule's Unicode-range boundary (including a previously-undocumented fullwidth-digit inclusion) never destroyed a legitimate space in any real instance — decision: KEEP, unchanged.
- **case-004/005 behavior**: confirmed, in this synthesis's own re-reading of case-005's raw artifacts (§9 of the case-005 first-frozen report), to still correctly close the identical header-row spacing artifact, unmodified, with no new gap exposed. case-004's own first-frozen report likewise confirms the rule operates correctly there.
- **Explicit non-generalization**: this program has never claimed, and this synthesis does not claim, "all Japanese-government PDFs need all internal CJK whitespace removed" — the rule is scoped precisely to the Unicode ranges and structural pattern (wide-letter-spaced header/total rows from specific toolchains) actually observed, with an explicitly-marked-ambiguous edge case (ideographic-comma-adjacent spacing) left as documented-but-not-certified behavior, not resolved into a general rule.

## 14. Special-representation/anomaly study (case-004)

Kept explicitly separate from the benchmark-scoring work above, per the originating task's own instruction:

- **Origin**: a user-observed page (viewer 1327, `pdfPageIndex` 1326) showing an ordinary ledger row with a blank amount triple immediately adjacent to a differently-shaped embedded matrix region, before the page resumes ordinary format.
- **Three independent, semantic-label-free observation channels** were built, each frozen *before* evaluating any known page: a pdf.js-coordinate geometry channel, a pure-text/grammar-transition channel, and a Docling table-region channel.
- **16-page fixed-sample Docling result**: a clean `maxNumCols ≤9` (ordinary) vs. `≥11` (known family) separation, explicitly and repeatedly caveated in its own report as unproven beyond that small, non-whole-document sample.
- **Deliberate 120-page broad-sample falsification test**: the clean separation **did not survive** — 59 of 120 broad-sample pages already exceeded the old boundary, including two pages independently, visually confirmed to be genuinely ordinary (the elevated column count there is a Docling dense-remarks-text segmentation artifact, not a source anomaly). The extreme tail (`≥18`, top ~4%) still concentrated genuine special-family pages, and three entirely new instances of the known family were found there, unplanned — but one of the two known sub-families (per-country/per-region itemization) was **not** distinguishable from ordinary variation at broad scale at all.
- **Source anomaly vs. engine segmentation artifact**: explicitly and repeatedly kept separate throughout — Docling's own single-merged-table representation of the visually-two-region page is an **engine segmentation choice**, not new evidence about the source PDF's own layout; this distinction was concretely demonstrated, not merely asserted, by finding both a genuine anomaly and a genuine ordinary-page false-positive producing the *same* signal value in the same sample.
- **Current position, stated at the correct strength**: these three channels are **candidate-generation signals that require visual or cross-channel confirmation before being trusted**, not a working automatic detector. No claim is made, here or in any of the four source reports, that "special structures can now be automatically found" — the broad-sample task's own explicit finding was the opposite: the cleanest-looking small-sample signal weakened substantially under broader testing, and this weakening was preserved as the primary reported result of that task, not treated as a failure to hide.

## 15. Layered architecture synthesis

Using this repository's own ADR-010 taxonomy, with one concrete example per layer drawn from an actual case, not a hypothetical:

1. **Source acquisition**: case-004's discovery that MEXT packages its request as four separate sibling PDFs, requiring a source-survey-stage decision (which sibling file to lock) before any row-level work could begin.
2. **Extraction representation**: case-005's Docling raw output correctly separating the target row's three amount cells into three distinct, independently-reversible cells (contrast: case-004's Docling output, where an apparently-empty visual column fragmented two amount cells into one, at this same layer).
3. **Engine-specific normalization**: `closeCjkWrapSpaces` (§13) and `reconstructNumericToken` (Docling's reversed-comma-group fix, exercised again correctly in case-005) — both operate entirely within this layer, correcting a specific engine's own known reconstruction artifact without touching document interpretation.
4. **Structural context selection**: case-004's organization-010/020 diagnostics, establishing that item-header recovery needs a bounded, page-adjacency-aware lookback mechanism distinct from unit recovery's own table-wide-once mechanism (§12).
5. **Document/layout-family interpretation**: case-004's item-header-absent-from-target-page finding itself — a fact about how this specific document's layout is organized, not about any engine's own extraction quality (every engine's own page-2 extraction was independently confirmed accurate).
6. **Semantic matching/evaluation**: `evaluate.mjs`'s own `item_name_exact_match` vs. `item_name_present_among_candidates` distinction (§11) — the same underlying extraction can PASS one and FAIL the other depending purely on how the evaluator's own resolution rule is defined, illustrating that this layer's own design choices materially shape which failures are visible.

## 16. Web PDF preliminary-research role

Web/chat-level preliminary observation was used, across multiple cases, to locate candidate official landing pages and PDFs before committed source-survey work began — a genuinely useful discovery aid, never treated as the source of record. The clearest documented instance of the risk this poses: case-005's own selection protocol explicitly records that an earlier, informal web/text-level observation described the target row's request number as plain `1`, while direct visual inspection of the locked PDF confirmed it is actually printed as the circled numeral `①` — a concrete, committed example of "a web page's or chat transcript's textual rendering of a source value is never a substitute for the source's own visual fact," adopted as an explicit methodological rule in that protocol. No finding in this synthesis is sourced from an uncommitted chat-only observation; where web/chat-level pre-observation informed *where to look*, the corresponding committed survey/protocol/selection/GT document is cited as the actual evidence.

## 17. MOF reverse-linkage signals (proposal only, no matching performed)

**Evidence, not proposal**: every one of the five cases' own frozen Ground Truth already records, as source-derived facts, a fiscal year, a ministry/organization identity, an item code/name, a request number, an expense code/name, a full amount triple, a page locator, and an explicit organization→item→expense hierarchy — all read directly from official government PDFs via a reproducible, auditable method. MLIT's own 総表 additionally confirms (existence-only, per case-005's own source survey) the literal presence of `...自動車安全特別会計へ繰入`-shaped expressions, a budget-lifecycle-adjacent vocabulary term not investigated further.

**Proposal, kept separate from the evidence above**: sufficient signals appear to exist to justify a future, separately-scoped linkage experiment testing whether these same PDF-derived keys (ministry, fiscal year, item/expense code, hierarchy) can be aligned against MOF CSV or RS/marumie-rssystem records without amount-magnitude matching alone as the sole evidence (amount-similarity-alone-as-selection-evidence is already an established anti-pattern in this repository's own research protocol). No such matching was attempted, no linkage algorithm was designed, no claim of actual linkability is made, and no semantic equivalence between a PDF-observed `繰入` expression and any specific MOF-CSV category is asserted.

## 18. Case Package / Strategy Selection implications

Candidate observations for a future Case Package, split per the architecture's own source-safe/engine-derived distinction (no schema change implemented here):

**Source-safe / source-derived** (would not require running any engine to establish): packaging model (combined vs. split-file, per case-004 vs. others); page locator conventions (`pdfPageIndex`/printed-label offset, confirmed different formulas per document); organization/item hierarchy depth and TOC granularity (case-005's own unusually granular 目次 as a genuine document-level fact); unit-declaration scope (page-level vs. table-wide-once, a genuine per-document property, confirmed to differ between case-004 and every other case); page-context relation for a specific field (item-header same-page vs. one-page-back, established per-row, not assumed per-document, per §7's own caution).

**Engine-derived** (established only via running a specific engine, and explicitly not to be promoted to a source-safe feature without independent visual confirmation, per this architecture's own already-stated principle): the pdf.js CJK-spacing artifact's presence on a given page (only knowable by comparing raw pdf.js output to the source); Docling's own wide-grid/segmentation signal (§14, confirmed capable of producing the same value from either a genuine anomaly or a pure segmentation artifact — the clearest possible illustration of why this must stay engine-derived, not be promoted); candidate availability counts (`item_name_present_among_candidates`'s own diagnostic list) — a property of a specific engine's own extraction, not the source.

This section proposes candidate content only; no Case Package schema field was added, removed, or renamed by this task.

## 19. Recommended research priorities (case-006 and beyond)

Five options were compared, per the originating task's own instruction, without implementing any of them:

- **A — Proceed to a sixth ministry.** Benefit: expands the corpus and would test whether the context-scope and anomaly findings (§12, §14) generalize to a genuinely new packaging/toolchain combination (none of the five so far has used a Producer other than "List Creator," "no Producer recorded," or MEXT's own Acrobat-Distiller sibling file). Cost: adds another data point without consolidating what five already provide.
- **B — Formalize Case Package / Strategy Selection.** Benefit: converts §18's own candidate list into an actual, reviewable schema, which the architecture's own Phase 2 gate already requires "at least 3 demonstrably distinct layout families" for — a bar this program has now cleared (combined/split packaging, encrypted/unencrypted, varying 目次 granularity). Cost: a design task, not a data-gathering one; risks premature schema lock-in if attempted before a sixth case's own structure is known.
- **C — MOF CSV reverse-linkage experiment.** Benefit: directly tests §17's own proposal with real evidence. Cost: highest risk of amount-magnitude-as-selection-evidence contamination if not designed with the same rigor already applied to row selection in this program; would need its own preregistered protocol before any matching is attempted.
- **D — Context-model prototype.** Benefit: directly operationalizes §12's own three-mechanism finding (page-local / neighbor-page / table-metadata) as a testable design, addressing a concrete, already-well-evidenced architecture gap. Cost: touches the extraction/normalization boundary this program has otherwise kept untouched by exploratory work; would need careful scoping to avoid becoming an unplanned production change.
- **E — RS data-quality line (1000× anomaly).** Out of scope for this synthesis by the originating task's own explicit instruction; noted only because it already exists as a recorded concern — see §20.

**Suggested order, offered as a recommendation only, not a decision**: B (formalize Case Package) before C or D, since both C and D would benefit from a stable schema to record their own findings against; A (a sixth ministry) is valuable at any point but does not by itself resolve any of the open architecture questions this synthesis surfaces. This ordering is not implemented in this task.

## 20. RS 1000× data-quality line (brief, separate mention only)

Per the originating task's own instruction, this is mentioned only as a single paragraph and only because it is understood to already exist as a separate, recorded concern: a candidate 1000×-magnitude unit anomaly in RS/marumie-rssystem data (referenced in this task's own originating instructions as "RS PID 18695") is **not** verified, investigated, or expanded upon in this synthesis. If this is not already recorded in `state/TODO.md` as a distinct future research line, it is **not** added as a new confirmed finding here — this synthesis's own state update (§23) does not introduce it as a new item, consistent with the instruction that unrecorded chat-only claims must not become confirmed findings.

## 21. What has been falsified or weakened

- **Falsified as a general threshold**: the 16-page Docling survey's own `maxNumCols ≥11` boundary — shown, in the very next task, to be met or exceeded by 49% of a broad, unbiased sample (§14).
- **Weakened, not falsified**: the `maxNumCols` signal as a continuous measure — its extreme tail still concentrates genuine anomalies, but with a confirmed sub-family exception (per-country/per-region itemization) that it cannot distinguish from ordinary variation at all.
- **Weakened**: any implicit assumption that "the known special-table family is rare" — the broad-sample task's own unplanned discovery of three new instances suggests it may be a common, recurring convention in at least this document, not a rare anomaly, though this remains a single-document observation, not cross-ministry-confirmed.
- **Not falsified, but never as strong as it might appear from the score alone**: Docling's case-005 10/11 result — explicitly recorded (§10) as evidence that this specific page's own geometry avoided Docling's three previously-documented failure mechanisms, not evidence of general improvement.

## 22. Remaining uncertainty

- Whether case-005's own same-page item/unit context (§12) is typical of MLIT's document family or specific to this one row — no context diagnostic has been run for MLIT.
- Whether the `item_name_exact_match` failure's own root cause (§11) could be resolved by a document/layout-family-interpretation-layer disambiguation rule (e.g. preferring the item-code candidate immediately preceding the selected expense row in document order) — this is a plausible hypothesis, not evidenced or tested here.
- The true population-wide frequency of case-004's own anomaly family, and whether an equivalent family exists in any of case-001/002/003/005's own documents — not investigated for any case other than MEXT.
- Whether MOF CSV / RS reverse linkage (§17) is genuinely feasible with only PDF-derived keys — no linkage attempt has been made.
- Case-001's own missing structural facts (page count, Producer, encryption) — `not established`, and not investigated in this task.

## 23. State update

`state/CURRENT_STATE.json`/`state/TODO.md`/`state/CHANGELOG.md` are updated to record that this synthesis was performed and to point to its report, and to carry forward the recommended-priorities list (§19) as a set of options for a future task to choose among — not as a decision already made. No new "confirmed fact" is added to state beyond what this report's own evidence already supports; in particular, no RS 1000× item is newly added (§20).

## 24. Conclusion

Five ministries into this research program, the methodology itself (preregistered selection, direct-visual Ground Truth, first-frozen preservation, disclosed post-hoc normalization improvements) has proven stable and repeatable. The most valuable findings are not the raw scores but the **mechanism-level distinctions** this program has been careful to preserve: a uniform outcome (`item_name_exact_match` FAIL) with heterogeneous causes; a context-recovery problem that is at least two different mechanisms, not one; an anomaly-detection signal whose clean small-sample appearance did not survive — and was not allowed to be reported as if it had — broader testing. No claim in this document extends beyond five cases' own evidence to a general statement about "Japanese government budget documents" as a class.

---

**This task synthesized only previously committed evidence. No new benchmark, Ground Truth, extraction, normalization experiment, source inspection, or production change was performed.**
