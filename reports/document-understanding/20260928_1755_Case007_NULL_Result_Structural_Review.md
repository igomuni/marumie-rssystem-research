# Case-007 NULL Result Structural Review — 内閣官房 (Cabinet Secretariat, CAS)

Status: **review only. No row selection was re-run. No Ground Truth. No benchmark run or OCR experiment. No amendment artifact was created — evidence supports closing this line of inquiry as a null research result (Option D), not amending the protocol.**

Date: 2026-09-28 (Asia/Tokyo)

## 1. Executive summary

The Case-007 Selection Record (`f530846`) found zero rows in `detail-01` satisfying the frozen Selection Protocol's own C1–C4 jointly: the only two request/expense-code-bearing rows (`①/01-95`, `2/06-95`) have visually blank amount cells, with the actual amount figures living in deeper child rows instead. This review investigated whether that gap is a `detail-01`-specific accident (H1), a convention common across CAS's own detail files (H2), or a mixed pattern (H3), via a minimal structural check of 4 files (`detail-01`, `detail-05`, `detail-07`, `detail-17`). **All 4 files show the identical structural pattern**: the request/expense-code row never itself carries a printed amount; the amount is always attached to one or more deeper child rows, at variable depth, and — critically — **the mapping from a request/expense-code row to "its own" amount is not a single, source-unique row**. In every sampled instance, either (a) a chain of 2+ nested breakdown levels sits between the request-code row and any printed amount, or (b) the nearest amount-bearing child is itself an aggregate over 2+ further object-code children, meaning "the amount for `①/01-95`" only exists as an *unprinted sum* over a variable-shaped set of descendant rows, never as a single explicit figure. Per the originating instructions' own decision rule ("parent-child associationがsourceから一意でない → D"), this supports **Option D: close Case-007's detail-ledger row-selection line of inquiry as a null research result.** No amendment protocol was written.

## 2. Frozen null result (unchanged, re-cited)

- Selection Protocol: `fixtures/document-understanding/case-007/20260928_1207_Case007_Selection_Protocol.md`, commit `2cc0821` — **not modified in this task.**
- Selection Record: `fixtures/document-understanding/case-007/20260928_1244_Case007_Selection_Record.md`, commit `f530846` — **not modified in this task.**
- Re-verified both byte-identical to their own freeze commits before this task's first edit (§13).
- Restated finding: universe = `detail-01`, 2 pages, all 14 rows exhaustively enumerated; zero rows pass C1–C4 jointly; the two request/expense-code rows pass C1+C2 but fail C3 (own amount cells blank); all other rows fail C1 (no request-number entry).

## 3. Exposed assumption

The original protocol's C1/C3, inherited in substance from case-002–006, implicitly assumed the request/expense-code row is **itself** the amount-bearing unit — true in every prior case (002–006), where that exact row always carried its own previous-year/current-year/delta triple directly. `detail-01`'s own null result exposed that this assumption does not hold for CAS: the request/expense-code row is a **label-only semantic header**, and the amount lives in a **variable-depth descendant subtree** below it.

## 4. Hypotheses (H1/H2/H3)

- **H1 — `detail-01`-specific.** The gap is an idiosyncrasy of this one file.
- **H2 — common CAS convention.** Every CAS detail file places the amount below the request/expense-code row, not on it.
- **H3 — mixed.** Some CAS files use the flat (case-002–006-style) convention; others use the deep convention.

## 5. Minimal cross-file structural check — inspection performed

4 files sampled, chosen to span official order and re-use existing evidence where possible (per the instruction to avoid enumerating all 16 files):

- `detail-01` — the frozen null-result file itself; evidence re-used from the Selection Record (`f530846`), not re-rendered.
- `detail-05` — a small (1-page) file, new `pdftotext -layout` read of page 1 in this task, for structural classification only.
- `detail-07` — the file most-inspected in the source survey; new re-read of its own page 1 in this task for structural classification (the survey's own prior reading focused on organization/item context, not on amount-cell placement relative to the request-code row, so this is a new observation angle, not a re-citation).
- `detail-17` — the last file in official numbering order, and structurally distinct (it is CAS's own 東日本大震災復興特別会計/reconstruction-special-account sub-package, not the general-account ledger the other three files belong to) — chosen specifically to test the pattern's robustness at the far end of official order and under a different account classification, per the instruction to sample a file "official order上で離れたlater detail file".

Inspection method: `pdftotext -layout` (page-1 text only, for structural classification of row nesting and amount-cell presence/absence — **not** used as a candidate-value transcription or as a substitute for the visual-only discipline used in the original Selection Record; no row was selected, ranked, or treated as a GT candidate here). Digits observed were used only to test a structural hypothesis (does a deeper row's own total equal the sum of its own children, confirming an aggregation relationship) — never recorded as a Ground Truth value or as a basis for selecting any row.

## 6. Structural evidence table

| File | Page locator | Request/expense row | Own amount cells | Deeper amount-bearing child | Hierarchy classification | Coverage | Prior/new inspection |
|---|---|---|---|---|---|---|---|
| `detail-01` | `pdfPageIndex` 0–1 (both pages) | `①/01-95`; `2/06-95` | **Blank** (both rows, confirmed via 2x-zoomed visual crop) | `①`: 2 levels down (`011`→`006`, `006` prints the total); `2`: 1 level down (`011`, which itself sums 2 further object-code children on page 2) | Multi-level, variable depth, child itself sometimes an aggregate | Exhaustive (all 14 rows, both pages) | Re-used from Selection Record (`f530846`); no new inspection |
| `detail-05` | `pdfPageIndex` 0 (1 page) | `1/01-95` | **Blank** | 2 levels down (`011 経常事務費` also blank; `016 厚生管理事務費` prints the total, `61,221`/`61,218`) | Multi-level, variable depth | Page-1 excerpt only (not exhaustive) | New, this task |
| `detail-07` | `pdfPageIndex` 0 (page 1 of 29) | `1/01-95` | **Blank** | 1 level down (`036 内閣官房副長官補経費` prints its own total directly, `2,848,403`/`2,393,889`/△`454,514`; the item-level aggregate `010 内閣官房共通費` above shows a different figure, `3,877,891`/`3,360,751`/△`517,140`, since that item covers more than just request `1`); `036` itself is further broken into `001 一般事務処理費` and other codes below it | Multi-level, child is itself an aggregate over further children | Page-1 excerpt only (not exhaustive; file has 29 pages total) | Partially known from source survey (organization/item context only); new structural observation (amount-cell placement) this task |
| `detail-17` | `pdfPageIndex` 0 (1 page) | `1/01-95` | **Blank** | 1 level down (`016 内閣官房一般行政に必要な経費` prints the total directly, `47,373`/`48,489`/`1,116`) — itself further broken into `001`/`01` object-level codes below | Multi-level, similar pattern, deeper *organizational* path (special-account classification layers precede the request row) | Page-1 excerpt (only page) | New, this task |

**Caveat on `detail-17`**: this file is CAS's own 東日本大震災復興特別会計 (reconstruction special account) sub-package, not the general-account ledger the other three files belong to — the same special-account category this whole census program treats as out of general-account scope elsewhere (see the FY2024 census's own fukkocho/reconstruction-account handling). It is retained here only as a **structural corroboration data point** (does the same request-row/blank-amount pattern appear even in a differently-classified sub-package within the same CAS-hosted file set?), not as a candidate for Case-007's own eventual universe.

## 7. Interpretation

All 4 sampled files show the **identical** structural pattern: the request/expense-code row (`①/01-95`-equivalent) is a label-only semantic header; no sampled instance shows this row carrying its own printed amount triple. This is strong, consistent (4/4) support for **H2** (a common CAS convention), and directly refutes **H1** (a `detail-01`-specific accident). **H3** (mixed) is not supported by this sample — no flat, case-002–006-style instance was found in any of the 4 files — but this is disclosed as a **non-exhaustive** finding (4 of 16 detail files checked); a flat instance could in principle exist in one of the 12 unchecked files, though nothing in this sample suggests it.

More importantly, in every sampled instance the amount-bearing descendant is **not a single, uniquely determined row**: it is either found only after 2+ nested breakdown levels, or it is itself an aggregate over 2 or more further object-code children (confirmed directly for `detail-01`'s own item `2`, where `011`'s own printed total, `25,002`/`25,016`, was checked and found to equal the sum of its own two object-code children below it — a structural verification of the aggregation relationship, not a Ground Truth transcription). This means "the amount associated with a given request/expense-code row" is, in general, an **unprinted sum over a variable-shaped subtree**, not a single explicit figure anywhere in the source — recovering it as a single value would require arithmetic reconstruction, which this research program's own rules (and every prior case's own discipline) explicitly prohibit as a basis for Ground Truth or row selection.

## 8. Option comparison (A/B/C/D)

- **Option A (semantic-parent model)**: rejected. A parent→child association rule could be frozen for the *simple* cases where a single, unambiguous child directly carries the parent's own total (e.g., if `①/01-95` always resolved to exactly one line with no further breakdown) — but the evidence in §6–§7 shows this is not the actual shape of the data: the "child" is frequently itself an aggregate over further children, and the depth is inconsistent even within one file (`detail-01`'s own `①` needs 2 levels; its own `2` needs 1 level but that level is itself an aggregate). Defining a source-safe, non-arbitrary rule for "the one associated child" is not achievable without either picking one row out of several equally-qualifying candidates (an undisclosed, criteria-widening choice) or summing a variable-shaped subtree (forbidden arithmetic reconstruction).
- **Option B (amount-bearing child inherits parent identity)**: rejected for the same underlying reason as A — it still requires uniquely resolving *which* child (or children) inherits the parent's identity, which is exactly the non-unique mapping problem found in §7. The instructions themselves caution B should only be adopted if A is rejected for a reason it doesn't share; here the rejection reason (non-unique association) applies identically to both.
- **Option C (change universe to a different file)**: rejected. All 4 sampled files — spanning near the start of official order, the middle, and the very end (plus a structurally distinct special-account file) — show the identical deep-hierarchy pattern with no flat, case-002–006-compatible structure found anywhere. Continuing to search additional files for a flat structure, having found none in a well-distributed 4-file sample, would risk exactly the "universe shopping" the instructions explicitly forbid — selecting a universe *because* it happens to contain an eligible row, rather than on structural grounds established before candidate inspection.
- **Option D (close as a null research result)**: **selected.** Per the instructions' own decision rule, "parent-child associationがsourceから一意でない → D" applies directly: the association is confirmed non-unique in every sampled instance. No amendment protocol can be written without either inventing an arbitrary tie-break among equally-qualifying descendant rows or introducing arithmetic reconstruction — both foreclosed by this program's own standing rules.

## 9. Decision

**Option D.** Case-007's detail-ledger row-selection line of inquiry, as scoped by the original Selection Protocol (a single physical row bearing its own native identifier and its own printed amount triple, directly comparable to case-002–006's own selected rows), is closed with a **null result**: CAS's own detail-ledger convention does not contain a row matching that shape. This is preserved as a genuine, disclosed research finding, not a defect requiring further engineering.

## 10. Amendment summary

**No amendment artifact was created.** No new `Case007_Selection_Protocol_Amendment_01.md` exists. This is a deliberate outcome of applying the decision rule, not an oversight — see §8.

## 11. Comparability implications

This finding is itself a genuine, disclosable structural difference between CAS's own detail-ledger convention and every prior case (002–006): in those cases, the request/expense-code row was always the single unit carrying both the native identifier and the amount triple together, making it directly usable as a one-row Ground Truth target. CAS's own convention separates "which item/request this is" (the label-only header row) from "what it costs" (a variable-depth subtree of children, often itself further aggregated) — a genuinely different document-understanding challenge that no prior case's own selection framework was built to represent as a single comparable row. This is recorded as a new finding for a possible future case-package design discussion, not resolved or acted upon here.

## 12. Provenance / chronology

`original hypothesis (Selection Protocol, `2cc0821`) → null result (Selection Record, `f530846`) → structural investigation (this report) → decision: close as null, no amended hypothesis produced`. All three earlier artifacts remain unmodified (§13).

## 13. Integrity verification

- Selection Protocol `2cc0821`: re-verified byte-identical via `git diff 2cc0821 HEAD -- fixtures/document-understanding/case-007/20260928_1207_Case007_Selection_Protocol.md` — no diff.
- Selection Record `f530846`: re-verified byte-identical via `git diff f530846 HEAD -- fixtures/document-understanding/case-007/20260928_1244_Case007_Selection_Record.md` — no diff.
- Source Survey `211213c` and its evidence JSON: re-verified byte-identical.
- Case-006–010 Selection Freeze: unchanged.
- Case-001–006 frozen artifacts: unchanged.
- `scripts/`: unchanged.
- `sources/source-lock.json` / `sources/source-registry.csv`: unchanged (no new acquisition; all inspection reused already-locked raw files).
- No Ground Truth or benchmark evidence generated at any point in this task.

## 14. Limitations

- Only 4 of 16 CAS detail files were checked; H3 (a mixed population) is not ruled out with certainty for the remaining 12 files, though nothing in this sample suggests it exists.
- `detail-17`'s own special-account classification makes it a lower-confidence corroboration point than the 3 general-account files; its inclusion strengthens but does not solely establish the H2 verdict.
- The aggregation-relationship check (`25,002` = `3,754` + `21,248`, etc.) was performed only for `detail-01`'s own item `2`; it was not repeated for every deeper node in every sampled file, since the qualitative pattern (blank parent row, populated/aggregated descendant) was already visually unambiguous without it.

## 15. Unresolved questions

1. Do any of the remaining 12 unchecked CAS detail files use a flat, case-002–006-compatible convention (H3)? Not investigated further, per the decision to stop once H1 was refuted and H2 was well-supported.
2. Is this deep-hierarchy convention unique to CAS among the Case-006–010 candidate set, or does it also appear in MHLW (Case-010, not yet started) or other authorities? Not investigated; out of scope for this review.
3. Would a future, explicitly-scoped Case Package design discussion (not this task) find value in a "multi-row semantic record" concept that could represent CAS's own convention without arithmetic reconstruction? Left open, not decided here.

## 16. Recommended next task

Per the frozen Case-006–010 execution order, proceed to **Case-008 (裁判所/Courts)** source survey, treating Case-007 as closed with this null result. Alternatively, if the research program's own priorities call for it, a separate, explicitly-scoped task could test H3 more exhaustively across CAS's remaining 12 detail files — but this is not recommended as the default next step, since the 4-file sample already found a consistent, well-distributed negative result for the flat convention.

---

**The original Case-007 protocol and its zero-selection result remain preserved as frozen research evidence. Any amendment was derived only after that null result and was frozen before any renewed row selection. No Ground Truth, benchmark run, or OCR experiment was performed.**
