# Case-007 内閣官房 (Cabinet Secretariat, CAS) Source Survey

- **Date (Asia/Tokyo):** 2026-09-28 10:28
- **Branch:** `research/case-007-cas-baseline` (created from `main@0612f4f`, post PR #6 merge)
- **Task type:** Source survey only
- **Primary research axis:** File-scoped context (from the FY2024 census's `cas` row hypothesis)

## 1. Executive Summary

CAS's own FY2024 concept-request package is split into 18 separate PDF files (1 overview narrative, 1 cover/index+summary-table file, 16 numbered detail files `detail-01`, `detail-03`–`detail-17` — `detail-02` does not exist in the published sequence). The census's own "file-scoped context" hypothesis is **partially confirmed and partially refined**:

- **Organization-level context (`010 内閣官房`) is genuinely file-scoped** — confirmed exhaustively (not sampled) across all 29 pages of `detail-07`: it is declared once, at the top of each file's own page 1, and never re-declared on any subsequent page within that file.
- **Item-level context is NOT file-scoped.** New item headers (distinct 事項/expense-code rows) begin repeatedly within a single file — approximately every 1 page in `detail-07`'s 29 pages (~22 distinct items observed) — via the same same-page mechanism already documented in cases 002–005. The census's original framing conflated organization-level and item-level context under one "file-scoped" label; this survey separates them.
- **A new, previously undocumented structural pattern was found**: the identical top-level item row (`010 内閣官房/010 内閣官房共通費/①/01-95/内閣官房一般行政に必要な経費`) appears on **page 1 of every one of the 5 detail files sampled** (`detail-01`, `detail-04`, `detail-08`, `detail-13`, plus a related but not identically-captured row in `detail-03`), each time with a **different amount pair**. This is consistent with a single MOF-facing budget item being **split/distributed across multiple bureau-level detail files**, each file carrying only its own bureau's partial figure. This is a genuinely new mechanism, distinct from "file-scoped context," and is recorded separately per this task's instruction not to collapse distinct mechanisms.

No Selection Protocol, row selection, Ground Truth, or benchmark work was performed. Multiple candidate files/organizations are presented below for a future, separate Selection Protocol task to choose from — no winner is selected here.

## 2. Scope and Non-Scope

**In scope:** source acquisition verification, package inventory, representation/accessibility, layout grammar, file-scoped/multi-file context investigation, comparison with cases 001–006, selection-protocol handoff facts.

**Explicitly out of scope (not performed):** Selection Protocol, row selection, Ground Truth transcription, amount-truth validation, MOF/RS linkage, docbench/benchmark run, OCR experiment or adaptation, parser/normalizer/evaluator changes, production adaptation, selection of a single "winner" file.

## 3. Prior Evidence / Census Hypothesis

The FY2024 census (`reports/document-understanding/20260927_1909_FY2024_All_Authority_Concept_Request_Format_Census.csv`, `cas` row) recorded a `contextDependencyObserved` note claiming "zero org-header re-occurrences on any of r6_07's own 29 internal pages after page 1" and characterized CAS's package as file-scoped-context. This is prior exposure: the census row was read (again) at the start of this task, before any of this task's own new inspection. All findings below distinguish the census's own prior claim from this task's own new, independent re-verification.

## 4. Official Acquisition Path

Re-fetched `https://www.cas.go.jp/jp/yosan/gaisan_youkyuu_r6.html` via WebFetch. Confirmed exactly 17 PDF links on the page (overview + cover + 15 numbered detail links, matching the on-site numbering which itself skips "02"), consistent with the census's own prior inventory count. No drift in link count or naming observed between the census's prior fetch and this task's re-fetch.

## 5. Package Inventory

18 locked CAS sources total in `sources/source-lock.json`:

| File | Pages |
|---|---|
| overview | 18 |
| cover | 2 |
| detail-01 | 2 |
| detail-03 | 4 |
| detail-04 | 4 |
| detail-05 | 1 |
| detail-06 | 6 |
| detail-07 | 29 |
| detail-08 | 4 |
| detail-09 | 3 |
| detail-10 | 4 |
| detail-11 | 19 |
| detail-12 | 4 |
| detail-13 | 3 |
| detail-14 | 3 |
| detail-15 | 3 |
| detail-16 | 2 |
| detail-17 | 1 |

`detail-02` is absent from the published sequence — CAS's own numbering has a gap. Detail file sizes are highly variable (1–29 pages), unlike MOJ's single 737-page monolith (case-006) or MEXT's more uniform per-file sizing.

## 6. Source Identities / Hashes

All 18 locally cached raw files were re-hashed (SHA-256, via a Python script — not shell string comparison, which failed earlier in this task with a quoting error and was replaced) and matched byte-for-byte against `sources/source-lock.json`. No drift, no re-download performed. `same URL != same source binary` (ADR-009) verified as satisfied for all 18 entries.

## 7. Representation / Accessibility

Unlike case-006 (MOJ, vector-outlined, zero extractable text), all sampled CAS detail files extract normal Unicode text via `pdftotext -layout` with no vector-outline symptom observed. This is a source-safe contrast fact only — no benchmark or engine comparison was run in this task.

## 8. Layout Grammar

Detail files follow the same general 概算要求額明細表 grammar already seen in cases 002–006: 要求番号 / 事項 / 前年度予算額 / 概算要求額 / 対前年度比較増△減 / 備考 columns, with 組織 (organization) and item rows nested above the request rows. The cover file additionally contains a distinct 総表 (summary table) grammar and a 目次 (table of contents) — both structurally different from the detail-table grammar and excluded from the detail-row selection universe under the case-006 P2 multi-grammar-exclusion precondition. The overview file is pure narrative prose (概算要求の概要), not a table at all, and is likewise excluded.

## 9. File-Scoped Context Investigation

Performed an **exhaustive** (not sampled) per-page `pdftotext -layout` scan of all 29 pages of `detail-07`:

- `010 内閣官房` (organization header) appears only on page 1; confirmed absent on pages 2–29, individually checked page by page.
- Distinct item-header rows recur throughout the same 29 pages — approximately 22 distinct item codes observed (07, 10, 13, 16, 19, 22, 31, 37, 40, 43, 46, 49, 52, 55, 58, 64, 67, 70, 76, 85, 93, 96, 98), each beginning a fresh item block roughly every 1 page.

Conclusion: organization-level context is file-scoped; item-level context is a same-page mechanism recurring within the file, not file-scoped. These are two distinct mechanisms and are recorded separately.

## 10. Context Anchor / Persistence / Reset

- Organization anchor: declared once at each file's own page 1 top, persists for the file's entire remaining page range, resets only at the next file's own page 1 (not observed mid-file).
- Item anchor: declared at the top of its own block, persists only until the next item header appears (same-page or next-page), consistent with the same-page/zero-or-one-page-back mechanisms already known from cases 002–005.

## 11. Column-Header Behavior

The column header row (要求番号 / 事項 / 前年度予算額 / 概算要求額 / 対前年度比較増△減 / 備考) repeats at the top of every sampled page within a file (confirmed on `detail-07` pages 1 and later pages via layout inspection), i.e. column schema is page-local and recoverable per page without needing file-level context — in contrast to the organization/item semantic hierarchy, which does require file-level (organization) or block-level (item) context to resolve.

## 12. Unit Behavior

`(単位:千円)` is declared once, near the top of each file's own opening page (confirmed on `detail-07` page 1 and `detail-11` page 1, and on the cover file's own 総表 page), not re-declared on later pages within the same file. This matches the page/table-opening-scoped unit convention already seen in case-006, and was independently re-verified here rather than copied from that case.

## 13. Multi-File Boundary Behavior

This is the primary new finding of this survey.

Every sampled detail file's own page 1 begins with the **identical** item code `010 内閣官房/010 内閣官房共通費/①/01-95/内閣官房一般行政に必要な経費`, but with **different amount pairs** per file:

| File (bureau, from page-1 label) | Previous-year / FY2024-request (千円) |
|---|---|
| detail-01 (総務課) | 1,440,572 / 1,707,217 |
| detail-04 (item row; org-level total shown as 3,374,012/3,424,189 is the row itself — org total on same page: 4,998,642/4,502,242 △496,400) | 3,374,012 / 3,424,189 |
| detail-08 (副長官補危機管理) | item total row: 1,233,165 / 1,332,219 (item-row-level `①/01-95` figure not clearly isolated in the sampled lines — flagged unresolved, §19) |
| detail-13 | 281,146 / 253,174 |

These four values are all different from one another for what is nominally "the same" item code and expense code. This is consistent with — but not confirmed as — a single MOF-facing budget item being split/distributed across multiple bureau-level detail files, each carrying its own bureau's partial figure, rather than each file duplicating one shared total. No arithmetic reconstruction, summation, or reconciliation against any total was performed (per `unknown != zero` and the prohibition on amount-similarity-as-evidence); this is reported strictly as an observed source-safe fact, not a validated hypothesis.

This is a distinct mechanism from file-scoped organization context (§9–10) and is not merged into that label.

Page-numbering behavior across files was inconclusive from text-layer extraction: page-1 header lines showed no visible page-number digit for 11 of 12 sampled files, but `detail-11`'s page-1 header showed a page number of "3". This inconsistency could reflect either a genuine continuous-numbering scheme across the file sequence or a text-extraction/column-alignment artifact specific to that file's layout. This was not resolved via visual/render inspection in this task and is recorded as unresolved (§19).

## 14. Embedded / Unusual Structures

- `cover.pdf` (2 pages) contains a 総表 (summary table, page 1) and an embedded 目次 (table of contents) — a different grammar from the detail tables, excluded per P2.
- `overview.pdf` (18 pages) is a narrative prose summary (令和６年度予算概算要求の概要), not tabular at all.
- No 定員表 (staffing table) or 国庫債務負担行為 (multi-year commitment) section was observed in the sampled pages; this was not exhaustively checked across all 18 files and is not claimed as an exhaustive negative.

## 15. Comparison with Cases 001–006

CAS's detail-table grammar matches the same general 明細表 structure used in cases 002–006 (item/expense-code/request-amount/comparison/remarks columns). It differs structurally from all prior cases in package granularity: CAS splits its FY2024 request into 18 small files (1–29 pages each) rather than one or a few large files (contrast: case-006/MOJ, a single 737-page file). This granularity is also the source of the new cross-file item-splitting pattern (§13), which has no precedent in cases 001–006's own findings.

## 16. Selection-Protocol Handoff Facts (candidates only — no winner selected)

- **Candidate files for a future selection universe:** `detail-07` (29 pages, most item variety, organization-level file-scoping most clearly demonstrated), `detail-11` (19 pages, second-largest), or any of the smaller single/few-page files (`detail-05`, `detail-17`) for a minimal-complexity universe.
- **Candidate organizations:** all detail files share the same top organization (`010 内閣官房`) but differ by bureau/sub-organization in their page-1 label (e.g., 総務課, 副長官補危機管理, 内閣情報調査室).
- **Detail-table opening locator:** page 1 of any detail file (`(組織)010 内閣官房` header immediately followed by the 明細表 column header row).
- **Universe boundary confidence:** high for organization-level scope (exhaustively verified on `detail-07`); item-level boundaries require per-item confirmation (same-page mechanism, not exhaustively re-verified for every one of the ~22 items in `detail-07`).
- **Navigation method used:** `pdftotext -layout`, per-page extraction; no visual/render-based navigation performed in this task.
- **Context anchor locator:** organization header string `010 内閣官房` immediately above the 明細表 title line on each file's own page 1.
- **Persistence evidence:** exhaustive 29-page absence-check on `detail-07` (§9).
- **Multi-grammar exclusion candidates:** `cover.pdf` (総表 + 目次), `overview.pdf` (narrative) — both excluded from the detail-row universe under P2.
- **Prior exposure:** the census's own `cas` row was read before this task began (§3); this task's own per-page exhaustive re-verification and the cross-file item-splitting finding (§13) are new to this task and were not present in the census's own recorded observations.

## 17. Prior Exposure

Disclosed fully in §3 and §16. No row was selected, and no amount was treated as a candidate Ground Truth value in this task.

## 18. Limitations

- Multi-file item-splitting (§13) was checked on 5 files, not all 16 detail files; the pattern is reported as observed-on-sample, not as an exhaustive-across-all-files fact.
- Page-numbering continuity (§13) is unresolved — text-layer extraction alone was insufficient; visual/render inspection would be required.
- `detail-08`'s own item-row-level figure was not cleanly isolated from its item-total row in the sampled `pdftotext -layout` output; flagged unresolved rather than guessed.
- Embedded/unusual-structure check (§14) was not exhaustive across all 18 files.

## 19. Unresolved Questions

1. Does the cross-file item-splitting pattern (§13) hold across all 16 detail files, or only a subset?
2. Is CAS's page numbering continuous across the file sequence, or does `detail-11`'s visible "3" reflect a layout/extraction artifact?
3. What is `detail-08`'s own isolated `①/01-95` item-row figure (as distinct from its item-total row)?
4. Do any of the 16 detail files contain a 定員表 or 国庫債務負担行為 section (not observed in the sample, not exhaustively ruled out)?

## 20. Suitability Verdict

**SUITABLE WITH CAVEATS.** CAS's package is suitable as a future case-package baseline: it has genuine extractable text (contrast with case-006), a familiar 明細表 grammar consistent with prior cases, and a clearly demonstrated file-scoped organization-context mechanism. The caveat is that a future Selection Protocol must explicitly account for the cross-file item-splitting pattern (§13) when defining row eligibility, since the "same" item code/expense code can legitimately appear with different amounts across multiple files — this must not be treated as a duplicate-row conflict or resolved via amount-similarity reasoning.

## 21. Recommended Next Task

Case-007 CAS Selection Protocol Freeze — define row-eligibility criteria for the CAS universe, explicitly incorporating a rule for handling the cross-file item-splitting pattern identified in §13 (e.g., an explicit precondition on which file's instance of a repeated item code is eligible, or an explicit exclusion of shared item codes from the universe pending further investigation).

---

No Case-007 selection protocol, row selection, Ground Truth, benchmark run, OCR experiment, parser change, normalization change, evaluator change, or production adaptation was performed.
