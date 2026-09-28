# Case-007 Selection Protocol (Preregistration) — 内閣官房 (Cabinet Secretariat, CAS) FY2024 General-Account Expenditure Request

Status: **frozen protocol. Row NOT yet selected. No candidate row enumerated, compared, or inspected in this task. No Ground Truth. No benchmark engine or OCR run against CAS.**

Date: 2026-09-28 (Asia/Tokyo)

This document defines, in advance of examining any specific candidate row, how the Case-007 target row will eventually be selected from the already-locked CAS source package. It is committed before any row is identified so the choice cannot be influenced — consciously or not — by which file was inspected most during the source survey, by the cross-file item-splitting pattern's own amount values (already incidentally seen for several files), or by resemblance to case-002–006's own selected rows. Actual row selection is a **separate, later task** that applies this protocol; this task does not perform it. This task also does **not** settle CAS's "true semantic record identity" across files — its scope is limited to freezing a **reproducible, deterministic, source-safe method for choosing one comparable row**.

## 1. Purpose

> Which row should become the single Case-007 target, chosen from a source-defined CAS universe using only source-visible structure — never amount values, cross-file amount comparison, expected engine behavior, or resemblance to already-seen rows — so that the eventual Ground Truth exercises the same document-understanding capabilities already tested in case-002–006, on a package whose primary axis is **file-scoped organization context plus same-page item context**, with a newly documented **cross-file item-splitting** complication that must not be resolved by inference?

This protocol freezes, in order: frozen source facts → package/source preconditions → candidate file comparison → frozen selection universe → file identity/provenance rule → cross-file splitting handling → eligibility-criteria critique → final criteria → context resolution order → tie-break → multi-grammar exclusions → ambiguity handling → explicit non-criteria → prior-exposure disclosure → inspection performed → stop rule → next task.

## 2. Frozen source facts

- Authority: 内閣官房 (Cabinet Secretariat, CAS).
- Source: `reports/document-understanding/20260928_1028_Case007_CAS_Source_Survey.md` (`211213c`) and `evidence/document-understanding/case-007-source-representation.json`. Both re-verified byte-identical to that commit before this task's first edit.
- 18 locked sources total: 1 narrative overview, 1 cover file (総表 + 目次), 16 numbered detail files (`detail-01`, `detail-03`–`detail-17`; `detail-02` does not exist in CAS's own published sequence).
- All 18 SHA-256 hashes re-verified against `sources/source-lock.json` immediately before this task (Python `hashlib`, matching the survey's own method) — no drift, no re-acquisition.
- Branch: `research/case-007-cas-baseline`. Verified via `git fetch`/`git status` immediately before this task's first edit: HEAD at `211213c`, working tree clean, `main` unchanged since the survey.
- This protocol performs **no new source acquisition** and does not modify `sources/source-lock.json` or `sources/raw/`.

## 3. Package/source preconditions (not per-row checks)

- **P0 — Package scope.** The eligible universe is drawn only from CAS's own **detail-ledger files** (`detail-01`, `detail-03`–`detail-17`). The `overview` file (pure narrative prose, no table) and the `cover` file (総表 + embedded 目次, a different grammar from the detail ledger) are excluded from the universe entirely — not merely de-prioritized. This mirrors the multi-grammar exclusion already established as P2 in the Case-006 protocol, applied here at the *package* level rather than within a single combined file, since CAS's own package model splits grammars across files instead of sections of one file.
- **P1 — Correct table.** Every row considered must lie within a detail file's own 明細表 body (below its own column-header row), not within any file-opening title/organization-label region. Confirmed, for the frozen target file (§5), to hold for its own entire page range by direct inspection in this task (§16).
- **P2 — Single-file universe.** The eligible universe for row enumeration is restricted to **one frozen target file** (§5), not the union of all 16 detail files. This is a deliberate simplification, not an evasion of the cross-file question: it removes the cross-file item-splitting complication from row *eligibility* entirely by construction (§7), rather than attempting to adjudicate it during enumeration.

## 4. Candidate file comparison

The Case-007 source survey left multiple candidate detail files, explicitly without selecting a winner. This protocol now compares them using only source-safe criteria, before any row within any file is inspected:

| Criterion | Evaluation |
|---|---|
| Official package/link order | CAS's own published sequence begins at `detail-01` (the numbering gap at `detail-02` does not change that `detail-01` is first). No candidate file precedes it. |
| Stable file identity | All 16 detail files are equally stable — each has its own locked `sourceId` and SHA-256, verified in §2. No file is more or less identity-stable than another. |
| Detail ledger (vs. summary/staffing/narrative) | All 16 detail files are confirmed detail-ledger grammar (§8 of the survey). No file is excluded on this basis alone. |
| Organization-scope/context-anchor clarity | Every sampled file (`detail-01`, `03`, `04`, `07`, `08`, `11`, `13`) shows an unambiguous organization anchor (`010 内閣官房`) at its own page-1 top. `detail-07`'s own anchor persistence was checked *exhaustively* (all 29 pages) only because it was the largest sampled file in the survey — this is an artifact of inspection depth, not a source property that makes `detail-07` more eligible than `detail-01`. Using inspection depth as a selection input would improperly let prior exposure drive the universe choice; this protocol explicitly rejects that reasoning (see §13, non-criteria). |
| Multi-grammar ambiguity within the file | `detail-01` re-inspected in this task (§16): both of its own 2 pages are confirmed pure 明細表 ledger grammar throughout, with no embedded staffing/summary/narrative section. No other candidate file was re-inspected for this property in this task (deferred; not needed once a winner is chosen). |
| Deterministic navigation | Every detail file's own organization anchor sits at the same page-1 top position, immediately above the same column-header row (§11 of the survey) — navigation is equally deterministic across all 16 files. |

**No file was found to be more eligible than any other on these criteria alone** — all 16 detail files pass P0–P2 equally. Per this protocol's own instruction not to let amount values, cross-file splitting, or inspection-depth familiarity break the tie, the deterministic fallback is: **prefer the first eligible detail file in official package/link order.** This does not conflict with any evidence gathered — `detail-01` is confirmed (§16) to be a clean, single-grammar, unambiguous detail ledger, so nothing disqualifies it from serving as the tie-break winner.

## 5. Frozen selection universe

**Frozen target file: `cas-fy2024-general-account-expenditure-request-detail-01`** (bureau label, from its own page-1 header: `05 内閣所管(総務官室（総務課）)`), the first detail file in CAS's own official numbering sequence, per §4.

- SHA-256: re-verified against `sources/source-lock.json` in this task, matching the source survey's own record, unchanged.
- Pages: 2 (confirmed via `pdfinfo`).
- Organization anchor: `010 内閣官房` / `010 内閣官房共通費`, established once at page 1, top of the ledger (confirmed present, §16). Per the source survey's own exhaustive finding on `detail-07`, this anchor is expected — but not independently re-confirmed on every page here beyond the 2 pages this file actually has — to persist for the file's own remaining page(s) without re-declaration.
- `pdfPageIndex` 0 (1-based PDF page 1) is the universe's own lower bound; `pdfPageIndex` 1 (the file's own last page) is the upper bound. Both bounds are exact — this file's own full page range, not an estimate — since the entire 2-page file is the universe, unlike the multi-organization-section universes case-002–006 needed to bound within a larger combined file.
- **Only rows within this one file are eligible.** No row from any other detail file (`detail-03`–`detail-17`), the `cover` file, or the `overview` file participates in enumeration, comparison, or the tie-break for Case-007.

## 6. File identity / provenance rule

Because CAS splits its package across 16 detail files with at least one confirmed instance of an identical-looking item/expense-code/name recurring across files with different amounts (§7), **file identity is treated as a required element of Case-007's own row provenance locator** — not as a claim that file identity is a universal semantic row key across CAS's whole package, but as the minimum information needed to reproducibly distinguish "this row, in this file" from a same-shaped row elsewhere in the package.

The future selection record must record, at minimum, for the selected row:

1. Package identity (authority: CAS; package: FY2024 general-account expenditure request).
2. File identity (`sourceId`: `cas-fy2024-general-account-expenditure-request-detail-01`).
3. Official URL and SHA-256 for that file.
4. `pdfPageIndex` (0-based) and 1-based PDF page number within that file.
5. Printed page label, if legible.
6. Organization code/name (`010 内閣官房`).
7. Item code/name (e.g., `010 内閣官房共通費`).
8. Request number (native, as printed).
9. Expense code (native, as printed).
10. Expense label (native, as printed, wrap-preserving).

This provenance requirement is **additive** to, not a replacement for, the item/expense-code identifiers every prior case's own locator already carried — it exists specifically because, in CAS's package, those identifiers alone are insufficient to uniquely locate a row (§7).

## 7. Cross-file item-splitting: handling rule

The source survey found that the identical `組織/項/要求番号/経費コード/経費名` (`010/010/①.../01-95/内閣官房一般行政に必要な経費`) recurs on page 1 of multiple sampled detail files, each time with a different amount pair. This protocol adopts the following rule, decided **before** any row is enumerated:

- **No duplicate exclusion.** A row is not made ineligible merely because a same-shaped row (same codes/name) exists in another file.
- **No amount-based winner selection.** Amount values — including whether two files' amounts are similar, different, larger, or smaller — are never used to choose among files or rows, at any stage.
- **No merging or aggregation.** This protocol does not sum, reconcile, or otherwise combine the amounts of same-shaped rows across files.
- **No assumption of semantic equivalence.** Two same-shaped rows in different files are not assumed to represent "the same" budget line, nor assumed to represent genuinely different lines — no claim about their relationship is made or needed.
- **No guess at a single "true" row.** This protocol does not attempt to determine which file's instance (if any) is the authoritative or primary one.
- **Resolution by construction, not adjudication.** The single-file universe (§5, P2) is frozen *first*; eligibility and tie-break rules (§9–§10) then apply *only within* that already-frozen file. Cross-file recurrence therefore never has to be adjudicated during enumeration — it is structurally avoided by restricting the universe to one file before any row is examined.

## 8. Critique of prior eligibility criteria (case-002 E1–E5 / case-003 ME1–ME5 / case-004 MX1–MX4 / case-005 C1–C4 / case-006 C1–C4)

| Concept | Prior treatment | Re-evaluation for CAS |
|---|---|---|
| Native request/expense-level identifier | Retained, document-family-independent, in every prior case. | **Retained unchanged.** CAS's own ledger shows the same request-number/expense-code column convention (confirmed on `detail-01`'s own page 1, §16) as every prior case. |
| Multi-line wrap | Retained in every prior case, each time re-justified as a capability test rather than a difficulty choice; case-006 explicitly deferred its *immediate* payoff (no engine could extract any text from MOJ) while retaining it for comparability. | **Reconsidered, then retained.** CAS's own primary research axis (file-scoped organization context, same-page item context, cross-file splitting) does not itself depend on multi-line wrap at all — unlike case-006, this is not a case where the criterion's payoff is deferred for a structural reason. Retained anyway for two reasons: (1) comparability — every prior case (001–006) has tested this same capability, and dropping it here would make Case-007 the first case not to; (2) it is not hypothetical for this file — `detail-01`'s own page 1 (§16) already shows a genuinely wrapped label (`内閣官房一般行政に必要` / `な経費`, 2 printed lines) on what looks like the file's own first eligible row, confirming the criterion is satisfiable here without being engineered to be. |
| Standard amount triple | Retained unchanged in every prior case. | **Retained unchanged.** Confirmed present in the same three-column position on `detail-01`'s own page 1 (§16). |
| Self-contained sufficiency | Retained in every prior case, each time extended for known source-specific complications (page-spanning, embedded relocation, multi-grammar sections). | **Retained, materially redefined for CAS's own primary axis.** See below — this is the criterion requiring the most rework, since a naive "everything on one page" reading would penalize CAS's own genuine, confirmed file-scoped organization mechanism (organization context is *correctly* absent from every page after a file's own page 1 — that absence is the phenomenon under study, not a defect). |
| Correct structural level (row vs. aggregate) | Folded into the native-identifier criterion in every prior case. | **Retained, folded into C1 as before.** |
| Tie-break (earliest `pdfPageIndex`, then topmost row) | Document-family-independent in every prior case. | **Retained, with a package-level prefix added** (§10), since CAS's own package spans multiple files where prior cases' universes lived inside one file. |
| Circularity-avoidance (visual/structural-only enumeration, criteria frozen before inspection) | The central constraint in every prior protocol. | **Retained in full.** |

### 8.1 C2 (multi-line wrap) — explicit freeze decision

**Decision: retained**, per the table above. Rationale restated: (a) preserves comparability with every one of case-001–006's own tested capability; (b) confirmed non-hypothetical for this file (§16); (c) CAS's own primary axis (context/file identity) is orthogonal to wrap behavior — retaining C2 neither helps nor hinders testing that axis, so there is no tension to resolve by dropping it.

### 8.2 C4 (self-contained sufficiency) — explicit freeze decision

**Decision: redefined into three separately evaluated evidence layers**, so that CAS's own confirmed file-scoped organization mechanism is never mistaken for missing evidence:

1. **Row-local evidence** — the candidate row's own native identifier (C1) and amount triple (C3) must be visually present and associated with that row, on the page where the row itself appears.
2. **Same-page (or same-item-block) item evidence** — the item header (項-level code/name, e.g. `010 内閣官房共通費`) governing the candidate row must be resolvable per the context-resolution order (§9): either printed on the same page as the row, or established by the nearest preceding item header within the *same file* if the item's own row block spans onto a later page without re-declaring its header (a pattern independently confirmed to occur within this exact file in this task, §16 — item `2` / `06-95` begins on `detail-01`'s own page 1 and its sub-rows continue onto page 2 without repeating the item header).
3. **File-scoped organization evidence** — the organization anchor (`010 内閣官房`) is resolved from the frozen file's own page-1 declaration (§5), and is **never required to be reprinted on the candidate row's own page** to count as present. A candidate row failing to show the organization label on its own page is **not**, by itself, a C4 failure — that absence is the correctly expected behavior of a file-scoped mechanism, not missing evidence.

**C4 PASS** requires all three evidence layers resolvable (by the rules above) for the candidate row, entirely within the frozen target file. **C4 FAIL** if any layer is unresolvable within the file (e.g., a row whose amount triple is split across a page boundary within the file; a row whose owning item cannot be traced back to any preceding item header within the same file; here there is no organization-anchor case to fail, since the file's own single organization is fixed by §5).

## 9. Context resolution order

Frozen order in which context is resolved for any candidate row, most row-local first:

1. **Row-local identifiers** — request number, expense code, and amount triple printed directly on the row's own line(s).
2. **Same-page item context** — the item header (項-level code/name) on the same page as the row; if absent from that exact page, the **nearest preceding item header within the same file** (confirmed necessary and sufficient by the `detail-01` page-1→page-2 continuation observed in §16 — no case of an item header appearing more than one page back from any of its own rows was observed, but this protocol does not assume a hard one-page cap either, since it was not exhaustively tested across all 16 files; the rule is "nearest preceding," not "at most N pages back").
3. **Frozen file-level organization anchor** — resolved once, from the target file's own page-1 declaration (§5), applying to every page of that file without requiring re-declaration.
4. **File identity/provenance** — the file itself (§6), establishing which package/file/URL/SHA-256 this entire chain of context belongs to.

No neighbor-page lookback across a *file boundary* is ever performed — organization and item context are resolved only within the single frozen target file (§5, P2); a same-shaped header in a different file is never used to fill in missing context for a row in the target file.

## 10. Deterministic tie-break

> **Package (CAS FY2024 request) → frozen target file (`detail-01`, §5) → earliest `pdfPageIndex` (0-based) within that file → topmost eligible row on that page (top-to-bottom reading order).**

The package-level and file-level components of this tie-break are already fully resolved by §4–§5 (exactly one file is in the universe, chosen deterministically); only the intra-file components (`pdfPageIndex`, then row position) remain live for the future selection task. This matches every prior case's own convention at the row level, extended with an explicit package/file prefix to account for CAS's own multi-file package model — a structural addition, not a substantive change to the underlying philosophy (earliest in document order wins).

## 11. Multi-grammar exclusions

- The `cover` file (総表 + embedded 目次) and the `overview` file (pure narrative) are excluded from the universe entirely (§3, P0) — not merely de-prioritized.
- No other detail file (`detail-03`–`detail-17`) participates in enumeration at all, since the universe is restricted to `detail-01` alone (§5, P2) — this is a package-level exclusion by construction, not a per-row grammar judgment.
- Within `detail-01` itself, both of its own 2 pages were confirmed in this task (§16) to be pure 明細表 ledger grammar throughout, with no embedded staffing table, summary table, or narrative section — so no intra-file multi-grammar exclusion is needed for this specific frozen universe.

## 12. Ambiguity-handling rules

Decided before any candidate is inspected:

- **File identity unresolved** — cannot occur within this protocol's own frozen universe (a single, already-identified file); would only become relevant if a future task needed to re-open the file-selection question, which is out of scope here.
- **Organization anchor unresolved for a candidate row** — cannot occur under this protocol's own C4 redefinition (§8.2): the organization anchor is fixed by the frozen file (§5), never re-derived per row.
- **Item context unresolved** — if no item header can be traced back (nearest preceding, same file) for a candidate row, that row **FAILS** C4; the future selection task must not fill this in by guessing from the filename, the organization label, or any other file's own item structure.
- **Page-spanning association unresolved** — a row whose amount triple is split across a page boundary **FAILS** C4, per §8.2.
- **Blank amount cell** — a candidate row with an apparently blank amount cell is not filled with `0` or any inferred value; it **FAILS** C3 (and therefore C4), per this repository's own `unknown != zero` rule.
- **Relocated values** — if a row's own amounts appear relocated into a differently-shaped embedded region (a pattern already documented elsewhere in this program), the row is treated as eligible only if that association is visually unambiguous under the frozen rules above; otherwise it **FAILS** C4. No such structure was observed in `detail-01` in this task (§16), so this rule is not expected to be exercised, but is recorded for completeness.
- **Same-looking row in another file** — explicitly outside the frozen universe (§5, §7); never merged, compared, or substituted for a row within `detail-01`.

## 13. Explicit non-criteria

The following must **not** influence file-universe selection, row eligibility, context resolution, or the tie-break, now or in the future selection task:

- Amount magnitude, or any similarity/difference between a candidate row's own amounts and any same-shaped row's amounts in another file.
- The delta sign (`△` glyph presence/absence) or delta magnitude.
- Content or population of the 備考 (remarks) column.
- Any prediction or expectation about how `pdfjs-baseline`, `pymupdf-baseline`, or `docling` will perform on the row.
- Docling table-structure/OCR geometry, or any other engine-internal behavior.
- PDF `Producer` metadata or encryption status.
- Similarity or difference to case-001–006's own selected rows (explicitly permitted either way).
- Whether a candidate row, file, or page was already incidentally viewed during the source survey (§14) — prior visibility neither qualifies nor disqualifies it.
- Inspection depth during the source survey (e.g., `detail-07`'s own exhaustive 29-page check) — this reflects how much attention a file received during the survey, not a property of the file itself, and must not be used to prefer that file (§4).
- Any inferred or asserted correspondence between CAS's own budget-line items and MOF-CSV or RS/marumie-rssystem concepts.
- "Representativeness" of a row or file for CAS's package as a whole.
- Normalization convenience for any existing parser/evaluator code.
- Whether two same-shaped rows in different files have equal or different amounts (this is the cross-file-splitting phenomenon itself, §7 — its existence is a research finding, never a selection input).

## 14. Prior-exposure disclosure

The Case-007 source survey (`211213c`) already, necessarily, visually exposed the following before this protocol was written:

- Full page-1 and (partially) page-2 content of `detail-01` was already read during the survey's own cross-file item-splitting investigation, **including its own amount values** (`132,904`/`153,320` at the item-aggregate level, and other sub-item figures visible in the same excerpt) — re-read again in this task (§16) for the same reason (confirming P1/grammar preconditions), not to select a row based on those values.
- Corresponding page-1 excerpts of `detail-03`, `detail-04`, `detail-08`, `detail-11`, and `detail-13` were also read during the survey, each showing a same-shaped `010/010/①.../01-95/内閣官房一般行政に必要な経費` row with its own distinct amount pair.
- The survey's own file-comparison table (§4 of this protocol) was constructed with full knowledge of which file had received the deepest prior inspection (`detail-07`, exhaustive 29-page check) — this protocol explicitly did **not** select `detail-07` as the target file, specifically to avoid letting that inspection depth (a survey-task artifact, not a source property) drive the universe choice (§4, §13).

**This disclosure is made honestly, not minimized.** No technical sandbox exists in this repository's toolset that would have prevented this exposure — exactly as disclosed in every prior case's own protocol. The methodological control is that the file-selection criteria in §4 are written in abstract, source-structural terms (official order, file-identity stability, grammar purity, anchor clarity, navigation determinism) that do not reference any amount value, and that explicitly reject inspection-depth familiarity as a valid input (§13). The eventual tie-break rule (first file in official order) was chosen *because* it required no reference to which file "felt" most examined, not despite that consideration. **No amount value is treated as a candidate Ground Truth figure anywhere in this protocol**, and no row within `detail-01` has been selected, compared, or ranked.

## 15. Contamination controls

- These rules (§3–§12) are frozen **before** any candidate row within `detail-01` is enumerated or compared.
- The universe (§5) is defined from package-level structural facts (official order, file identity, grammar) established in the source survey and re-confirmed in this task (§16), never from any expense row's own content.
- No benchmark output, Ground Truth, or engine behavior exists for CAS at any point in this research program; none is consulted.
- No criterion in §8–§9 was chosen because it is known to produce or avoid a specific outcome for any specific row in `detail-01` — none has been viewed yet beyond the page-1/page-2 excerpts already disclosed in §14, which were read for precondition-confirmation, not row selection.
- The already-disclosed prior exposure (§14) is not used to shape any criterion's substance toward, or away from, any already-seen row or amount.
- Provenance and chronology (this protocol's own commit, preceding any future selection-record commit) are preserved as the audit trail proving the freeze order.

## 16. What was inspected in this task

- Re-verified all 18 CAS source SHA-256 values against `sources/source-lock.json` (Python `hashlib`), matching the survey's own record.
- Re-verified branch/HEAD/working-tree/`main` state before the first edit (§2).
- Re-read the Case-007 source survey (`211213c`) and its companion evidence JSON in full.
- Read the Case-006 selection protocol (`7ef2250`) in full, for methodological comparison (§8).
- Read the Case-006–010 Selection Freeze (`654e3c5`) for continuity of binding methodology notes.
- Performed `pdfinfo` on `detail-01` to confirm its exact page count (2).
- Performed `pdftotext -layout` on **both** of `detail-01`'s own 2 pages in full (§4, §8.2, §9), to confirm: (a) the file is pure 明細表 ledger grammar throughout, with no embedded multi-grammar section (P0/§11); (b) the standard request-number/expense-code/amount-triple/multi-line-wrap conventions are present and visually consistent with prior cases (§8); (c) a concrete instance of item context persisting across a page boundary without header re-declaration (item `06-95`, beginning page 1, continuing onto page 2), directly informing the context-resolution design in §9 and the C4 redefinition in §8.2.

This inspection was limited to **precondition confirmation** (grammar purity, page count, context-persistence mechanism) as explicitly permitted by the originating instructions — it did **not** enumerate, compare, rank, or select any candidate row, and no amount value read during this inspection is treated as a Ground Truth candidate.

## 17. Stop rule for the future selection task

The future selection task must:

1. Begin at `detail-01`'s own `pdfPageIndex` 0 and scan top-to-bottom, then continue to `pdfPageIndex` 1 if needed, applying P0–P2 (already satisfied by construction) and C1–C4 (§8) via direct visual/structural inspection.
2. Stop **immediately** at the first row that fully passes C1–C4 — no comparison against later rows, no ranking, no "better" candidate search.
3. Never scan or consider any file outside the frozen universe (`detail-01` only).
4. Never transcribe or record any amount value as Ground Truth in that task — amounts may be *visually confirmed present* (C3) without being transcribed as GT figures, exactly as in every prior case's own selection-record convention.
5. Create a selection record and **stop before Ground Truth** — Ground Truth remains a separate, later task, per the same two-step sequencing used in every prior case.

## 18. Selection-task handoff

- Branch: `research/case-007-cas-baseline`; pre-task HEAD for the future selection task: this protocol's own freeze commit.
- Frozen target file: `cas-fy2024-general-account-expenditure-request-detail-01` (2 pages, `pdfPageIndex` 0–1).
- Frozen universe: the entire file, no organization-boundary sub-range needed (single organization, single file).
- Eligibility criteria: C1 (native identifier), C2 (multi-line wrap, retained), C3 (standard amount triple), C4 (three-layer redefinition: row-local / same-page-or-nearest-preceding-item / file-scoped-organization).
- Context resolution order: row-local → same-page-or-nearest-preceding item → file-scoped organization anchor → file identity.
- Tie-break: package → frozen file → earliest `pdfPageIndex` → topmost row.
- Cross-file splitting: irrelevant to the future selection task by construction — only `detail-01` is in scope.
- Multi-grammar exclusions: `cover`/`overview` files excluded from the package universe; `detail-01` itself confirmed single-grammar.
- Prior exposure: `detail-01`'s own page-1/page-2 content (including several amount values) has already been read twice (survey + this protocol) for precondition purposes only; no row has been selected or compared.

## 19. Freeze semantics

This protocol is frozen as of this task's own commit. No candidate row within `detail-01` (or any other CAS file) has been enumerated, compared, or selected. No Ground Truth exists for Case-007. No benchmark engine, OCR tool, or `npm run docbench`/`extract` has been run against CAS at any point in this research program. The next task that applies this protocol must perform eligible-row enumeration by direct structural inspection only, record the selected row and any prior/incidental exposure in a new selection-record artifact, and stop before Ground Truth.

## 20. Recommended next task

Apply this frozen protocol to `detail-01`'s own 2 pages to select exactly one row, create a selection record, and stop before Ground Truth. **Not executed in this task.**

---

**No candidate row was selected. No Ground Truth was created. No benchmark engine or OCR experiment was run. The Case-007 selection universe and rules were frozen before row enumeration.**
