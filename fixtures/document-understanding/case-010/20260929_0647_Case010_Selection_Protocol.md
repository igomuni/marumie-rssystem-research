# Case-010 MHLW — Selection Protocol

Status: **frozen protocol; no candidate row enumerated, selected, or transcribed.**

Created: 2026-09-29 06:47 Asia/Tokyo.
Source Survey dependency: `reports/document-understanding/20260929_0625_Case010_MHLW_Source_Survey.md` at `cc5115b80076159dc58570fb9fa4e7d7267a14f5`.

## 1. Purpose

Freeze a deterministic, source-safe procedure for selecting at most one physical main-standard-ledger row from Case-010 before any candidate-row enumeration. This protocol defines the source, universe, exclusions, C1–C4, context/unit handling, ambiguity policy, tie-break, and stop rule. It does not select a row or create Ground Truth.

## 2. Frozen source identity

| field | frozen value |
| --- | --- |
| Source ID | `mhlw-fy2024-general-account-expenditure-request-summary-detail` |
| URL | `https://www.mhlw.go.jp/wp/yosan/yosan/24syokan/dl/05-1b-01.pdf` |
| Title | `令和６年度歳出概算要求書（一般会計）総表・明細表` |
| SHA-256 | `09d26048b20d1b1dac7aab236ab6da452e482a12f4d97a8f6c28ec7c420eb192` |
| Bytes / pages | 3,444,358 / 1,723 |
| Package model | one combined, unencrypted PDF |
| Representation | native text, CID TrueType fonts, List Creator, A4 landscape |

The raw binary was rehashed in this task and matches the source lock. Source lock and registry are unchanged.

## 3. Source-survey basis

The committed survey establishes these source-safe facts: cover/TOC and separators occupy `pdfPageIndex 0–7`; the cross-reference summary is `8–19`; the main detail section is `20–1722`; and the detail TOC lists eight organizations. The first organization is `010 厚生労働本省`, beginning at index 20/printed 13; the next organization `030 検疫所` begins at index 1227/printed 1220. The detail section is a standard ledger but contains remarks-side explanatory lists and embedded breakdown tables; header repetition is nonuniform in the sampled pages.

No new PDF render, text extraction, candidate inspection, or source acquisition was performed in this task. The only source operation was SHA-256 verification.

## 4. Selection unit

One **physical row of the main standard-ledger grammar**, carrying its own source/file/section/page/context provenance. A selected unit is never an inferred parent-plus-child record, an arithmetic reconstruction, or a row from a remarks-side embedded table.

The eventual Selection Record must retain the source ID, SHA-256, `pdfPageIndex`, printed page/prefix, section identity, organization and item context, request number, expense code, expense label, and applicable unit evidence.

## 5. Universe decision

**Frozen universe:** physical main-standard-ledger rows for the first TOC-declared organization, `010 厚生労働本省`, within `pdfPageIndex 20–1226` inclusive (printed pages 13–1219), subject to the row-level grammar exclusions in §7 and §11.

The start and end are fixed by the cover TOC: main detail begins at printed 13/index 20 and `030 検疫所` begins at printed 1220/index 1227. The universe does not include the boundary organization, the summary, or another file.

## 6. Universe alternatives considered

| option | decision | source-safe rationale |
| --- | --- | --- |
| A — first organization standard-ledger section | **adopted** | `010 厚生労働本省` is first in the source’s explicit TOC order; its exact next-organization boundary is available. It gives a bounded, deterministic universe without candidate-content input. |
| B — all detail organizations (`20–1722`) | rejected | document-order would be deterministic, but needlessly expands a 1,703-page search beyond the first source-declared organization when an exact, comparably conventional organization partition exists. |
| C — another organization/source-safe partition | rejected | selecting a later organization would require an additional preference rule not supplied by source order or protocol comparability. |

This follows the prior-case practice of anchoring a large combined ledger to the first source-declared headquarters organization where an exact boundary exists. It was not chosen because an eligible row was expected to appear early, nor because the survey made its content familiar.

## 7. Grammar exclusions

The following are outside the universe or ineligible even if present on a page otherwise in the index range:

- cover, TOC, and blank/separator pages;
- the cross-reference summary (`pdfPageIndex 8–19`), including its split subcolumns and `明細書頁数` grammar;
- organization/item aggregate or header lines that do not meet C1–C4;
- remarks-side breakdown lists, compact tables, multiyear plans, historical execution/budget tables, and any other nested non-main-ledger structure;
- a row with ambiguous grammar identity.

The exclusion is **substructure-level**, not page-level: a standard-ledger page can contain both main ledger rows and excluded remarks-side material.

## 8. Eligibility criteria

A physical row is eligible only if all four criteria pass after it first passes the main-ledger grammar rule.

| criterion | frozen definition |
| --- | --- |
| C1 — native identifier | The row itself visibly associates a request number with an expense code in the main-ledger request-number/matter structure. An item aggregate, subordinate accounting-code-only line, or inherited identifier does not pass. |
| C2 — visible multi-line label | The row’s expense/matter label visibly wraps across two or more printed lines in the source render. Extraction line breaks do not decide this criterion. |
| C3 — same-row amount triple | The same physical main-ledger row visibly aligns one previous-budget value, one FY2024 request value, and one delta value in the main ledger’s three amount columns. |
| C4 — evidence sufficiency | File, main-section/grammar, organization, item, identifier, amount association, and applicable unit can be resolved under §§11–14 without crossing a prohibited boundary or guessing. |

## 9. Criterion rationale and retained comparability

C1 preserves the source-native request/expense identity used by Cases 002–006, 008, and 009. C2 is retained for cross-case document-reconstruction comparability: it tests visible layout reconstruction rather than a predicted engine score. The survey’s incidental exposure of wrapped labels did not decide this rule. C3 retains the direct physical-row amount requirement that Case-007 showed must not be silently relaxed: a label-only parent or a variable-depth child/subtree is not an eligible replacement. C4 is widened only to name Case-010’s known grammar, organization, unit, and embedded-substructure provenance requirements; it does not authorize inference.

## 10. Explicit non-criteria

No decision under this protocol may use amount magnitude, delta sign, remarks content, arithmetic convenience, expected extraction/benchmark behavior, expected score, visual familiarity, perceived cleanliness, source representation convenience, MOF/RS correspondence, Ground Truth availability, prior-case amount similarity, candidate novelty, or prior exposure.

## 11. Main-row versus embedded-substructure rule

A row is a main-ledger row only when visual/source cues jointly show that it:

1. occupies the main table’s request-number, matter, and three amount-column alignment;
2. is not wholly inside a boxed or indented structure placed in the remarks-side area;
3. does not rely on an alternate local header or a locally redeclared unit as its amount grammar; and
4. is part of the continuous main-ledger grid rather than a nested list or subtable.

An embedded table/list is excluded when it is confined to remarks-side placement, has its own border/header/local unit, has distinct columns, or otherwise lacks the main-ledger alignment. If cues conflict or cannot be resolved by direct non-OCR visual inspection, classify it `ambiguous grammar -> ineligible`.

## 12. Context lookup and safe lookback

Allowed resolution order:

1. row-local request number, expense code, label, and triple;
2. same-page main-ledger item context directly above or enclosing the row in the continuous main grid;
3. frozen organization anchor `010 厚生労働本省`, proven by the TOC/start boundary and confined to `pdfPageIndex 20–1226`;
4. detail-section identity and file identity.

**No cross-page item lookback is permitted.** The survey observed continuation risk but did not establish an exact safe item-lookback rule for the full 1,703-page detail section. A candidate requiring item context from a preceding page therefore fails C4 rather than receiving an inferred association. Context must not cross an organization boundary, a grammar boundary, the summary, or a remarks-side embedded structure.

## 13. Unit rule

The target grammar’s unit is `千円`, supported by the main-detail section-opening declaration at `pdfPageIndex 20`. It applies only after the row is confirmed as a main-ledger row within this frozen universe. A locally declared unit in a remarks-side embedded table neither changes nor supplies the main-ledger unit. A candidate whose main-ledger unit applicability cannot be established under this section-scoped rule fails C4.

## 14. Amount association rule

C3 requires direct visual same-row alignment in the main amount columns. The following are prohibited: inheriting values from a child, borrowing a value from an embedded table, treating a blank as zero, using a subtotal, summing a subtree, or reconstructing a value arithmetically. Any uncertain row/column association fails C3 (and therefore eligibility).

## 15. Ambiguity and continuation handling

- grammar ambiguous -> ineligible;
- identifier association ambiguous -> C1 fail;
- label-wrap boundary ambiguous -> C2 fail;
- triple association ambiguous or blank -> C3 fail;
- organization/item/unit context ambiguous -> C4 fail;
- cross-page continuation required -> C4 fail under §12;
- high-resolution non-OCR rendering is permitted only to resolve a source-visible ambiguity, never to introduce OCR or inferred values.

## 16. Tie-break

After the frozen universe and criteria, tie-break is: earliest eligible `pdfPageIndex`, then topmost eligible physical row on that page. No second organization order is needed because the organization is already fixed by the universe. No amount or content property may alter the tie-break.

## 17. Stop rule

The next task scans the frozen universe in document order and stops immediately at the first row passing main-grammar verification and C1–C4. It must not inspect later rows/pages to compare quality. If no row passes after the complete frozen universe is evaluated, it records a NULL Selection Record and stops.

## 18. Prior exposure

The Source Survey visually inspected representative pages and saw rows, figures, and remarks-side structures incidentally. It did not enumerate candidate order, apply C1–C4, select a row, or transcribe a value as Ground Truth. This exposure is disclosure only, is an explicit non-criterion, and supports no blind-selection or sandbox claim.

## 19. NULL-result handling

NULL is a valid result. It must preserve the evaluated scope/count and first-failing criteria patterns without relaxing this protocol, widening the universe, selecting a later organization, importing context from a different grammar, or creating an inferred parent/child amount record.

## 20. Integrity constraints

The Source Survey report/evidence remain byte-identical to `cc5115b`. Cases 001–009, the Case-006–010 Selection Freeze, scripts, source lock/registry, parser/normalizer/evaluator, OCR configuration, and production code must remain unchanged. The Selection task may create only its Selection Record and necessary state updates after applying this protocol.

## 21. Handoff to Row Selection

Use direct non-OCR visual inspection only. Begin at `pdfPageIndex 20`; operate only through index 1226; apply §11 before C1–C4; record rejected rows without amount values; freeze exactly one winner or a NULL record; and stop before Ground Truth.

**The Case-010 selection universe, grammar exclusions, eligibility criteria, context/unit rules, ambiguity handling, tie-break, and stop rule were frozen before candidate-row enumeration. Embedded remarks-side tables were explicitly separated from the main-ledger grammar. No row was selected, no Ground Truth was created, and no benchmark or separate OCR experiment was run.**
