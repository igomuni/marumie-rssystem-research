# case-004 MEXT PR Packaging Review

Status: **packaging/audit artifact. Not a new benchmark result. No new research produced in this task.**

Date: 2026-09-27 (Asia/Tokyo)

This document audits the already-committed `research/case-004-mext-preregistration` branch for internal consistency, freeze integrity, and review-readiness, and records the minimal packaging decisions made before opening a PR. It reproduces no experiment and adjudicates no open research question; where a later report supersedes an earlier one's optimistic framing, that supersession is recorded here rather than by editing the earlier, historical report.

## 1. Git / branch / merge-base

- Branch: `research/case-004-mext-preregistration`
- Pre-task `HEAD`: `22d50df` (confirmed, working tree clean)
- `main` (local and `origin/main`, freshly fetched): `3b29ebd` — **exactly matches** the expected checkpoint from the current handoff; no drift to report.
- `git merge-base origin/main HEAD` = `3b29ebd` — a clean, linear ancestor relationship; this branch has never been rebased against a moving `main`.
- `git log --oneline --decorate --graph origin/main..HEAD` shows exactly 11 commits, linear, no merge commits, no gaps:

```
22d50df research: validate MEXT Docling anomaly signal broadly
acaf550 research: survey MEXT Docling table anomalies
a9c0092 research: survey MEXT text grammar anomalies
075474e research: survey MEXT structural anomaly signals
aedea1c research: replicate MEXT context diagnostic in org 020
187a8e9 research: diagnose MEXT pagination context
49f5ca6 research: record MEXT case-004 first frozen benchmark
f9b2f35 research: freeze MEXT case-004 ground truth
fa82c13 research: select MEXT case-004 target row
c2b2c28 research: freeze MEXT case-004 selection protocol
d4449dd research: survey MEXT case-004 source
```

No rebase, squash, or history rewrite was performed or is planned.

## 2. Chronology audit

The Git history reproduces the required dependency order exactly, with no out-of-order or missing checkpoint:

```
source survey/acquisition (d4449dd)
  → selection protocol freeze (c2b2c28)
    → row selection freeze (fa82c13)
      → Ground Truth freeze (f9b2f35)
        → first frozen benchmark (49f5ca6)
          → post-hoc diagnostics (187a8e9, aedea1c)
          → post-hoc anomaly research (075474e, a9c0092, acaf550, 22d50df)
```

All 11 expected checkpoints listed in the originating task are present at exactly the commit SHAs given; no extra or missing commit was found on this branch.

## 3. Source provenance audit

- `sourceId`: `mext-fy2024-general-account-expenditure-request-detail`; `sources/source-lock.json`'s own recorded SHA-256 (`6df221dfd22c48e0f32dd59bcf2dbcbaad19720083be43005ce700b984a6bf71`) matches the local raw file's independently recomputed SHA-256 exactly.
- `sources/source-registry.csv` carries one corresponding row with full discovery provenance (two independently agreeing routes: MEXT's own navigation and MOF's cross-ministry link table).
- The raw PDF is correctly **not** Git-tracked (`git ls-files` returns nothing for it) and is correctly matched by `.gitignore`'s `sources/raw/*` rule.
- Source-survey-documented characteristics reconfirmed present in the committed artifacts, not re-investigated in this task: standalone detail-table packaging (one of four separate sibling PDFs, unlike METI/MIC's combined documents); 1,339 pages; permission-only AES-256 encryption (confirmed, across every later task in this branch, never to block `pdftoppm`/`pdfinfo` or any of the three benchmark engines); acquisition via plain `fetch()` (no WAF encountered) using the existing, unmodified shared `lock-policy.mjs` — no source-acquisition code was touched anywhere on this branch.

## 4. Frozen-artifact integrity audit

Every artifact below was diffed between its own freeze commit and current `HEAD` (`22d50df`); **all nine are byte-identical, zero diff**:

| Artifact | Freeze commit | Diff to HEAD |
|---|---|---|
| Selection protocol | `c2b2c28` | empty |
| Selection record | `fa82c13` | empty |
| Ground Truth (`ground-truth.json` + evidence) | `f9b2f35` | empty |
| First frozen benchmark (report + evidence JSON + generated evaluation.md) | `49f5ca6` | empty |
| Organization-010 diagnostic | `187a8e9` | empty |
| Organization-020 replication | `aedea1c` | empty |
| Geometry anomaly survey | `075474e` | empty |
| Text/grammar anomaly survey | `a9c0092` | empty |
| Docling small-sample survey | `acaf550` | empty |

No later diagnostic or anomaly-research task rewrote the Ground Truth, the selection artifacts, or the first frozen benchmark's own historical numbers (7/11, 7/11, 5/11) at any point — the historical result remains recoverable both as a byte-identical current file and via `git show <freeze-sha>:<path>` if ever needed.

## 5. Ground Truth isolation audit

Re-confirmed by direct code reading, not by re-inference:
- `evaluate.mjs` remains the **only** file that reads `ground-truth.json`'s `result` object anywhere in `scripts/document-understanding/benchmark/`; this was independently verified during the first-frozen-benchmark task and re-confirmed here — this file was not touched anywhere on this branch (`git diff --stat origin/main...HEAD -- scripts/` is empty).
- Every adapter (`pdfjs-baseline`, `pymupdf-baseline`, `docling`) reads only `sourceId`/`sourceSha256`/`pdfPageIndex` from Ground Truth — confirmed unchanged, since no adapter file appears in this branch's diff at all.
- No MEXT-specific expected string or amount is hard-coded anywhere in production code — trivially true here, since **zero files under `scripts/` were modified on this entire branch** (confirmed via `git diff --name-only origin/main...HEAD | grep scripts/` returning nothing).
- All four anomaly-research tasks (`075474e`, `a9c0092`, `acaf550`, `22d50df`) explicitly, and by direct inspection of their own committed methodology sections, never read `ground-truth.json` and never used any known-anomaly-page list as a feature-generation or sampling input — each survey's own report documents this as a frozen, audited constraint, and no evidence contradicts it.
- **This isolation is methodological/audited, not technically sandboxed** — no tool in this repository's toolset enforces that a research script cannot open `ground-truth.json`; this packaging review states that limitation plainly rather than implying an enforcement mechanism that does not exist, consistent with this repository's own prior disclosure pattern (e.g. ADR-012's own methodology-not-enforcement framing for LLM reconstruction isolation).

## 6. First frozen benchmark (presented fixed, not re-derived)

| engine | score |
|---|---:|
| pdfjs-baseline | 7/11 |
| pymupdf-baseline | 7/11 |
| docling | 5/11 |

Reconfirmed directly from `reports/document-understanding/20260926_2127_Case004_First_Frozen_Benchmark_Run.md` (unchanged, §4 above), not re-run in this task. Headline findings, restated exactly as that report states them, not reinterpreted: both flat-text engines correctly extract the target expense row and its amount triple; the genuine item-header candidate is entirely absent from the target's own page for all three engines (a document/layout-family-interpretation-layer limitation, explicitly **not** attributed to MEXT's standalone packaging — §3 of that report rules this out directly); the unit label is likewise absent from the target's own page for all three engines, exactly as pre-registered in the Ground Truth evidence; Docling additionally fails both amount fields via a column-fusion table-grid artifact; encryption did not block any engine; two full runs reproduced byte-identical output. This packaging review does not add to, subtract from, or reinterpret any of these findings.

## 7. Context-diagnostic review

**Organization 010** (`187a8e9`): 8 boundaries sampled from the sibling TOC's own page numbers; 4/8 same-page, 4/8 exactly one page back, 0/8 farther; zero repeated/carry-forward item context on any cross-page sample; unit label absent from all 16 sampled local pages.

**Organization 020** (`aedea1c`): the organization's **entire population** of valid item-header boundaries (3, not a sample) was checked; 1/3 same-page, 2/3 one page back, 0/3 farther; zero repeated context; no new organization-level unit declaration found at the `010`→`020` boundary.

**Combined**: across all 11 sampled/complete-population boundaries, item-header context is recoverable by a zero-or-one-page-back model with zero exceptions; unit context requires a categorically different, table-wide-once metadata mechanism, not a wider page window. Both reports explicitly frame this as an **architecture implication for a future context-selection strategy**, not a benchmark adaptation — no benchmark code, evaluator, or normalizer was changed by either diagnostic, confirmed again by this review's own `scripts/` diff check (§5).

## 8. Special-representation / anomaly research chronology (reviewed for evidence-strength accuracy)

This is the area most likely to be misread in a PR review, so each stage's actual, current evidentiary status is restated precisely, per the originating task's own concern:

- **Source-side visual finding** (first documented in `075474e` §4.2): a page containing an ordinary ledger header row with a blank amount triple, immediately adjacent to a differently-shaped, multi-column ruled matrix region, confirmed present at multiple pages across at least three organizations. **Semantic meaning remains explicitly unresolved throughout every subsequent report**: no report in this branch classifies this structure as a MOF-CSV `繰入`/`移替` concept, as a formal cross-tab, or as a confirmed duplicate representation of the resumed ledger's own amounts — this was checked directly against the final text of every anomaly report in this branch and confirmed absent (§ "documentation consistency" check below).
- **Geometry survey** (`075474e`): a pdf.js-coordinate-derived channel; found the flagship page within a top-~5% candidate set (not top-ranked); independently discovered other genuine special-structure instances; explicitly and repeatedly framed as an **engine-derived candidate signal**, never as source truth.
- **Text/grammar survey** (`a9c0092`): a pure-text/order channel, explicitly analytically separate from geometry; its own report states plainly that the flagship page never reached even a top-10% review set on its own signals (weaker than geometry) — this weaker result is preserved in the report, not minimized; it also independently found two new family instances geometry's own inspected sample had missed, and disclosed, without silently fixing, a regex-matching limitation that produced a genuine false positive on an ordinary page.
- **Docling small-sample survey** (`acaf550`): a fixed, non-whole-document 16-page sample; found `maxNumCols ≤9` for baseline and `≥11` for the known family with zero overlap — explicitly and repeatedly caveated in that report's own text as **unproven beyond the 16-page sample**; also found that Docling merges the source's own visually-two-region page into a single wide table object, meaning a high column count there does **not** mean "the source has that many semantic columns."
- **Broad-sample falsification** (`22d50df`): a 120-page, evenly-spaced, machine-selected sample covering the whole document, frozen before evaluation. **This is the single most important result to surface accurately in the PR**: the 16-page survey's clean separation **did not survive** — 59 of 120 (49%) broad-sample pages already exceed the old `≥11` boundary, including two pages directly confirmed, by visual inspection, to be genuinely ordinary. The verdict recorded in that report is **B — partially survives**: the signal's extreme tail (`≥18`, top ~4%) still concentrates genuine special-family pages (three new instances were found there, unplanned), but one of the two known sub-families (per-country/per-region itemization) is not distinguishable from ordinary variation at broad scale at all. `totalSpanningCellCount` was independently judged inconclusive, leaning toward collapse.

**PR-body-level instruction confirmed followed by this review**: nowhere in the final, committed text of any report in this branch is the 16-page result stated as "Docling detects special pages" without its scope qualifier — the `acaf550` report itself already states the qualifier throughout, and the `22d50df` report exists specifically to test and report the falsification. The PR body (§17 below) will state the falsification prominently, not bury it.

## 9. Research conclusions to preserve (as categorized by the originating task)

**Confirmed source/document facts**: standalone detail-table packaging (one of four sibling files, distinct from METI/MIC's combined documents); a table-wide-once, not page-repeated, unit convention; a document/layout-family-interpretation-layer loss of item-header context specifically caused by pagination distance, not packaging; multiple, visually distinct embedded/special structures recurring across at least three organizations, considerably more common than the original small set of known instances suggested.

**Confirmed engine behavior**: the current architecture's page-local context limitation (all three engines); Docling's column-fusion artifact on the flagship target row; Docling's single-wide-table merging of visually-two-region pages; and, critically, confirmed in the broad-sample task, that an engine-derived high-column-count artifact can also occur on a genuinely ordinary source page (dense remarks-text segmentation), not only on genuinely special ones.

**Supported but limited architectural implications**: structural context selection (item-header recovery) and table-wide metadata (unit recovery) are better modeled as two distinct mechanisms, not one wider context window; multiple independent observation channels are complementary, not redundant, for candidate generation; no single engine-derived anomaly metric is source truth on its own; an engine's own segmentation/failure behavior can be useful evidence without ever being accepted as document truth.

**Still unresolved, and explicitly left unresolved in every relevant report**: the semantic taxonomy of the special structures found (project/committee-matrix family, multi-year commitment-schedule family, per-country/per-region itemization family — named descriptively, not semantically classified); their exact relationship, if any, to MOF-CSV concepts; request-scope semantics beyond the 2 checked instances; any production anomaly detector, context-expansion strategy, or provenance-linkage implementation — none was implemented on this branch.

## 10. Diff review against main

```
19 files changed, 2517 insertions(+), 1 deletion(-)
```

Grouped:

1. **MEXT source provenance**: `sources/source-lock.json` (+13 lines, one new entry), `sources/source-registry.csv` (+1 row).
2. **case-004 protocol / selection / GT**: `fixtures/document-understanding/case-004/{20260926_2029_*,20260926_2045_*,20260926_2101_*,20260926_2111_*,ground-truth.json}` (5 new files).
3. **Extraction-derived/evidence/report outputs**: `evidence/document-understanding/case-004-results.json`, `reports/document-understanding/case-004-evaluation.md` (2 new, generated-by-runner files).
4. **First benchmark narrative**: `reports/document-understanding/20260926_2127_Case004_First_Frozen_Benchmark_Run.md`.
5. **Context diagnostics**: `20260927_0459_*`, `20260927_0519_*` (2 new reports).
6. **Anomaly/special-representation research**: `20260927_0619_*`, `20260927_0637_*`, `20260927_0656_*`, `20260927_0719_*` (4 new reports).
7. **State files**: `state/{CURRENT_STATE.json,TODO.md,CHANGELOG.md}` (modified, additive only).
8. **Incidental code/test changes**: **none** — confirmed by direct diff inspection (§5); this branch contains zero changes under `scripts/`.

`git diff --check origin/main...HEAD` reports exactly one line: a trailing blank-line notice at the very end of the auto-generated `reports/document-understanding/case-004-evaluation.md`. This was checked against an already-merged prior case's own equivalent generated file (`case-003-evaluation.md`) and found to be **byte-for-byte the same pre-existing trailing-newline pattern**, produced by the unmodified report-rendering code in `run.mjs` — not a defect introduced by this branch, and not corrected here, per the task's own instruction not to fix runtime/generator behavior as a packaging side effect.

## 11. Repository hygiene

Checked and confirmed absent from the branch diff: raw PDFs, rendered PNG/JPEG scratch files, ZIP archives, `.venv` contents, caches, browser binaries, credentials/`.env` files, local absolute paths (only public URLs and the PDF-encryption term "owner-password" matched a naive secret-pattern search, both benign), temporary diagnostics, and accidentally-staged research scratch. All 19 changed files are Markdown, JSON, or CSV documentation/evidence artifacts plus the additive state files. No large files were introduced (`sources/source-registry.csv`: +1 row; `sources/source-lock.json`: +13 lines).

## 12. Documentation consistency

Checked the current, final text of every report on this branch against each specific stale-claim pattern the originating task named:

- Clean Docling separation stated without its small-sample qualifier: **not found** — `acaf550` states the qualifier throughout, and is directly superseded by `22d50df`.
- `maxNumCols ≥11` described as a classifier/threshold: **not found** — every report describing it explicitly labels it a small-sample-observed boundary, and `22d50df` explicitly falsifies it as a threshold.
- The special matrix assigned an unproven semantic label: **not found** — checked directly; every report keeps semantic interpretation in an explicitly separate, unresolved section.
- Encryption described as an extraction failure: **not found** — every mention states the opposite (did not block/impede).
- Unit described as page-level rather than table-level for case-004: **not found** — correctly and consistently described as table-level with an explicit case-002/003 contrast.
- Item-header absence described as a standalone-packaging consequence: **not found** — the first-run report explicitly rules this out (§8 above, §3 of that report).
- GT isolation described as technical sandboxing: corrected in this review itself (§5) to state plainly that isolation here is methodological/audited, not tool-enforced.
- p1327 described as unique/rare after the broad survey found more instances: **not found** in any final report text; `22d50df` explicitly reframes the family as likely common, not rare.
- Unresolved boundary/context facts presented as resolved: **not found** — every diagnostic explicitly flags its own approximation/limitation (e.g., organization-020's small sample size, the un-inspected `pdfPageIndex` 630 outlier, etc.).

**No documentation-only correction was required or made** — the existing reports were already written with the qualifiers the task was concerned might be missing. No historical timestamped report was edited.

## 13. Validation

```bash
npm run validate         # PASS
npm run extraction:test  # PASS ("pdf extraction assertions PASS")
npm run docbench:test    # PASS (43/43 unit tests)
npm run sources:test     # PASS (8/8 tests)
git diff --check         # 1 pre-existing, harmless trailing-newline notice (§10), not a defect
```

`sources:verify` (live network) was not run, per the task's own instruction that MEXT local source integrity (already independently confirmed, §3) is the relevant check for packaging, not a live re-verification. No benchmark was rerun merely to refresh timestamps; no code/semantics changed on this branch that would require one.

## 14. Review focus (for the PR body)

1. Freeze chronology / Ground Truth isolation (§2, §5).
2. MEXT source provenance (§3).
3. First-run preservation (§4, §6).
4. Target-page context interpretation (§7).
5. Distinction between source anomaly and engine anomaly (§8, §9).
6. Broad-sample falsification (§8, most important single result).
7. Absence of detector overfitting/production adaptation (§5, §10 — zero `scripts/` changes on this entire branch).
8. Repository hygiene (§11).

## 15. Recommended next step

Per the originating task's own explicit stop condition: **open the PR and stop with it in the OPEN state.** No merge, no case-005, no further MEXT detector work. If the PR is approved, the next reasonable step (not executed here) would be to merge and then decide, as a separate scoped task, between beginning case-005's source survey on a new ministry or pursuing one of the still-unresolved architecture proposals recorded in §9.
