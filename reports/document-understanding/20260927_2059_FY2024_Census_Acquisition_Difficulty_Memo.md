# FY2024 Format Census — Acquisition Difficulty Memo

Status: **memo only, summarizing already-committed work. No new acquisition, no row selection, no Ground Truth, no benchmark engine run, no schema/production change.**

Date: 2026-09-27 (Asia/Tokyo)

Branch: `research/fy2024-all-authority-format-census`.

## Purpose

This memo consolidates, in one place, the outcome for every authority in the FY2024 all-authority format census (population frozen in `20260927_1909_FY2024_Population_Freeze.md`, commit `558f7fb`) whose PDF could not be acquired on the first attempt. The full detail for each lives in the census report's own §10.2–§10.2g; this memo is a compact index into that history, not a replacement for it.

## Outcomes, in resolution order

| Authority | Initial problem | How it was resolved | Final status |
|---|---|---|---|
| 防衛省 (MOD) | Landing page HTTP 403 (WAF-consistent) | User provided the exact direct PDF URL (`gaisan/r6/gaisanyoukyu.pdf`), independently confirmed via web search; the direct URL returns HTTP 200 even though the landing page stays blocked | **In scope.** Landing-page-specific block only; 540 pages, standard ledger grammar. |
| 内閣官房 (CAS) | General landing page (`index.html`) surfaced only a narrative overview for the current year | User pointed to the year-specific sub-page `gaisan_youkyuu_r6.html`, which lists a genuine 17-file bureau-split ledger. All 17 files were later exhaustively acquired and inspected on the user's follow-up request | **In scope**, reclassified from "narrative-only" to the List-Creator combined-ledger family (split variant). `familyConfidence` upgraded to high after the exhaustive re-check. |
| 外務省 (MOFA) | Landing page HTTP 403; escalated investigation showed the ENTIRE mofa.go.jp domain (including its own homepage) returns "Access Denied" via curl, WebFetch, and a full Playwright/Chromium session | User downloaded the file from a different network origin and supplied it locally (`incoming/100546568.pdf`); verified as a genuine PDF before locking | **In scope**, via user-provided-out-of-band delivery — the only source in this entire research program acquired this way, disclosed explicitly in `source-lock.json`'s own `acquisitionMethod` field. |
| 衆議院 (Shugiin) | General landing page listed only later fiscal years, no working FY2024 link | Targeted web search found the year-specific direct filename (`kaikei-saishutsugaisan6.pdf`) | **In scope.** |
| 裁判官弾劾裁判所 (Dangai) | Same as Shugiin | Full year-indexed archive listing (`info/report.html`) surfaced `r06_saisyutu-gaisan.pdf` | **In scope**, cross-reference-summary family. |
| 厚生労働省 (MHLW) | Two prior passes' own `WebFetch`-based link enumeration of the authority's sub-pages found only narrative/policy-evaluation files, never the real ledger | User provided the exact URL (`dl/05-1b-01.pdf`) directly | **In scope**, reclassified from "narrative-only" into both the cross-reference-summary family and the List-Creator combined-ledger family. This turned out to be the **largest document in the entire census** (1,723 pages). |
| 参議院 (Sangiin) | 5+ automated web searches and filename-pattern-guessing against both sibling years' conventions found no working URL | User found the exact URL (`r6gaisan-yokyusyo-250905.pdf`) via web search | **In scope.** Verified genuinely FY2024 material via `pdfinfo`'s own `CreationDate` (2023-08-09) before locking, since the filename's own date suffix was misleading. |
| 裁判官訴追委員会 (Sotsui) | An automated search found and acquired a document, but it turned out to be the wrong document *stage* (an enacted-budget `各目明細書`, not the request-stage `概算要求書`) | User identified the exact correct URL (`r6budget_yokyu.pdf`) | **In scope**, via the genuine request-stage document. The originally-acquired wrong-stage document is retained as a separate, still-valid artifact — one authority genuinely hosts both. |
| 国立国会図書館 (NDL) | General landing page lacked a working FY2024 request-stage link | Investigated via the authority's own full page listing: request-stage documents for R7–R9 are retained, but R6's own is not — while R6's own *final-budget*-stage document is | **Confirmed absent**, not resolved — precisely characterized as a request-stage-specific retention window shorter than the final-budget retention window, distinct from a WAF failure. |
| 復興庁 (Fukkocho) | Not part of the original 33-authority population at all — discovered via a *second* MOF index page (`2024gaisangaiyo_link.html`) while investigating a user question about Sotsui | Investigated the authority's own budget page directly | **Categorically out of scope** — this authority publishes no 一般会計 request at all; its entire FY2024 budget runs through the 東日本大震災復興特別会計 (special account), which this census's own scope explicitly excludes. A reference copy was locked but not counted as in-scope. |

## Net effect on the population

- All 33 originally-frozen population authorities now have a closed status: **31 in-scope**, **1 confirmed absent** (NDL).
- A 34th candidate (復興庁) was investigated and found to have no in-scope document at all, by its own design — not an acquisition difficulty.
- No authority remains in an ambiguous, retry-pending, or wrong-stage state.

## Cross-cutting lessons (already recorded in the census report's own §10.7, repeated here for visibility)

1. A general "current" landing page is not guaranteed to surface a past year's own request-stage sub-page — a negative result from one navigation path is not evidence of non-existence (CAS, MHLW's own root cause).
2. A landing-page 403 should be tested against a direct file URL before being generalized to a domain-wide block — only one authority (MOFA) actually warranted that stronger, harder-to-resolve characterization.
3. `WebFetch`'s own link-enumeration summaries are not guaranteed exhaustive, particularly among visually similar, densely-packed file lists differing by a single character (MHLW's own `05-1a` vs `05-1b`).
4. A successfully-acquired, well-formed PDF matching a search query is not itself sufficient evidence of being in-scope — the document's own internal title and table grammar must be checked against the census's explicit scope boundary every time (Sotsui's own two-document situation).
5. When automated tooling is domain-wide blocked with no available workaround, user-provided-out-of-band file delivery is a legitimate, disclosable acquisition method — provided the file is independently verified (magic number, `pdfinfo`, content sampling) before being trusted (MOFA).

## What this memo does not do

It does not re-derive or re-verify any of the above findings — each is already committed, with its own evidence, in the census report's §10.2 through §10.2g and the companion CSV. It does not add any new acquisition, family classification, or case-006+ recommendation beyond what those sections already state. Multi-page/context-carry-over sampling and final format-family/case-006+ determination remain outstanding, as recorded in the census report's own §10.9.

---

**This is a memo consolidating already-committed acquisition-history findings. No new acquisition, inspection, row selection, Ground Truth, or benchmark engine run was performed in producing it.**
