# Case-009 Cabinet Office (CAO) Selection Protocol

Status: **FROZEN before candidate-row enumeration**

Created: 2026-09-28 21:22 Asia/Tokyo
Branch: `research/case-009-cao-source-survey`
Source Survey dependency: `e640dc21c5bf536ab5ca40b20ed4b3ea8b2b3c11`

## 1. Purpose

This protocol freezes a source-admissible Case-009 selection universe and the rules for a later, separate row-selection task. It does not enumerate candidates, select a row, transcribe amounts, create Ground Truth, run a benchmark or OCR experiment, or change source registration or production behavior.

The primary decision is source admissibility, not which file or row seems interesting. The package contains many official PDFs, but only a locked binary can be a reproducible selection/GT source without a preceding canonicalization task.

## 2. Frozen source/package facts

The Source Survey establishes an official FY2024 CAO package of 51 PDFs (`0.pdf`–`50.pdf`; 394 total pages): `0.pdf` is cover/TOC and 50 detail files have standard-ledger starts, each with a `千円` declaration and a file-opening organization/division scope. The detail grammar is homogeneous at inspected starts, but the contextual partitions are heterogeneous.

Only `0.pdf` and `1.pdf` were already locked repository sources. The survey’s other 49 official downloads were temporary, unregistered snapshots. File boundaries are context-bearing scope partitions/locators; numeric package order was not demonstrated necessary for local scope recovery. Sampled boundary checks did not show predecessor-dependent continuation, but did not exhaustively disprove it package-wide.

## 3. Source-admissibility comparison

| option | canonical bytes and provenance | reproducibility / auditability | package coverage | protocol consequence | decision |
|---|---|---|---|---|---|
| A — locked-detail-only | Existing locked raw binary for `1.pdf`; hash, URL, registry, and lock already agree | High; later GT can verify identical bytes without a lock mutation | Narrow: one of 50 detail files | A clear file-bounded universe can be frozen now | **Chosen** |
| B — choose one of all 50, then lock it | 49 detail files are only temporary survey snapshots | Potentially high only after a separate canonicalization/lock procedure | Broad | Requires a distinct source-canonicalization decision before protocol/selection; not performed here | Not chosen for this task |
| C — use all temporary snapshots directly | 49 binaries have official survey provenance but no repository lock/registry identity | Insufficient for a frozen selection/GT chain | Broad | Would promote temporary survey material to canonical use without the required reproducibility control | Rejected |

Option A is selected because `1.pdf` is the **only already-locked detail source**, not because of its row content, amount values, visual salience, expected eligibility, or expected benchmark behavior. This is a source-admissibility decision, not a package-wide representativeness claim. Option B remains a possible future prerequisite only if a later task explicitly chooses package-wide canonicalization; it is not silently substituted here.

## 4. Canonical source identity

| field | frozen value |
|---|---|
| package | CAO FY2024 official expenditure-request package |
| repository source ID | `cao-fy2024-general-account-expenditure-request-detail-01` |
| official filename / package member | `1.pdf` |
| official URL | `https://www.cao.go.jp/yosan/soshiki/r06/pdf/1.pdf` |
| SHA-256 | `7b5de5dbd397c7067cab4ea527ef02681e91265914057651ee5b886174de7f4e` |
| bytes / pages | 12,180 bytes / 3 pages |
| PDF representation | native text; A4 landscape; List Creator; permission-only AES encryption (print/copy permitted) |
| locked-source status | existing lock and registry entry; no changes made by this task |

The SHA-256 was re-verified directly against the local locked raw file during this protocol task and matches the lock.

## 5. Selection unit and frozen universe

The selection unit is **one physical standard-ledger, amount-bearing row** in the canonical `1.pdf`, with provenance comprising package + file identity + section/grammar + page locator.

The frozen universe is `1.pdf`, `pdfPageIndex 0–2`, limited to rows in the repeated standard-ledger column grammar. A source-safe structural recheck found the ledger title and `（単位:千円）` at file opening and repeated ledger headers on continuation pages. It also found nested explanatory/breakdown boxes in the remarks region; those are not independent target rows for this protocol.

`0.pdf` (cover/TOC), every other package PDF (not an already-locked selection source), headers, organization/item aggregate lines, blank space, nested non-target boxes, and any page/box whose grammar is ambiguous or non-ledger are outside the universe.

## 6. Grammar identity and exclusions

A candidate must be in the standard-ledger grammar, evidenced together by its ledger column structure (request number; matter/hierarchy; previous, FY2024 request, and delta columns; remarks), repeated header/printed prefix, and consistency with the file-local ledger section. Page index alone is a locator, not sufficient grammar proof.

Exclude a row if it is any of the following:

- a cover/TOC, summary-only, blank/separator, or non-ledger row;
- an organization or item aggregate without the required row-local identifiers;
- a staffing, policy, narrative, or other differing grammar if encountered;
- a nested explanatory, historical, object/breakdown, or other subtable box that does not itself meet the physical standard-ledger row definition; or
- grammar-ambiguous.

The exclusion rule is source-structural, not merely a page-range shortcut.

## 7. Eligibility criteria

All four criteria must pass on one physical row.

| criterion | frozen rule | Case-009 rationale |
|---|---|---|
| C1 — native identifier | The same physical row visibly contains both a request number and the ledger’s expense-code-level identifier. A parent/preceding row’s identifier is not inherited. | Keeps the target source-native and comparable to prior physical-row cases while avoiding an unproven CAS-style parent/child model. |
| C2 — multi-line label | The row’s own expense/project label visibly wraps across at least two printed lines. Extracted-text line breaks alone do not establish it. | Retains the established layout/document-understanding stress and cross-case comparability; the survey structurally observed wrapped labels in this file, without using any row as a selection input. |
| C3 — row-local amount triple | The same physical row visibly and unambiguously carries all three standard-ledger cells: previous budget, FY2024 request, and delta. Blank or uncertain cells fail. | Tests association supplied by the source rather than an aggregate, child row, neighboring row, or arithmetic reconstruction. |
| C4 — section-aware evidence sufficiency | Physical-row identity, item context, file-start organization/division scope, ledger grammar, file identity, and applicable unit must be recoverable through the frozen chain below. | CAO file boundaries partition meaningful local scopes; file identity is required provenance but never replaces source-visible context. |

No criterion may be relaxed to avoid a NULL result.

## 8. Context resolution and file identity

Resolve context only in this order:

1. row-local request number, expense code, and label;
2. same-page item declaration;
3. nearest preceding valid item declaration within **the same `1.pdf`** only, provided visual inspection establishes that no fresh section/grammar boundary intervenes;
4. the file-opening division/organization scope (`19 内閣府所管（官房総務課（総務課））`), with any more-local visible organization/item hierarchy retained separately; and
5. file identity/provenance (package, source ID, official filename/URL, SHA-256, `pdfPageIndex`, and printed page/prefix if present).

Do not inherit context from another PDF, package numeric order, a prior file’s ending, engine output, or a presumed cross-file continuation. If a candidate needs any such inference, C4 fails. File identity is context-bearing as a source-scope partition and mandatory locator; it is not a substitute for source-visible organization or item evidence.

## 9. Unit rule

The applicable unit is `千円`, supported by the file-section-opening declaration in `1.pdf`. It applies only while the candidate is confirmed inside the same standard-ledger section. It is not package-global, and it must not cross a local grammar/embedded-box boundary. If unit applicability cannot be established under this rule, C4 fails.

## 10. Hierarchy, ambiguity, and NULL handling

Aggregate, item, project, object-code, and child/breakdown lines are not assumed equivalent. A request/expense-code row with blank amount cells does not acquire values from descendants; an amount-bearing child does not acquire a parent identifier. No arithmetic reconstruction, roll-up, or semantic parent/child association is allowed.

Apply these rules:

- visually ambiguous amount-cell association: C3 FAIL;
- ambiguous identifier ownership or label continuation: C1/C2 FAIL as applicable;
- unclear grammar identity: outside universe;
- unclear item/organization context, or unit scope: C4 FAIL;
- context requiring another PDF: C4 FAIL;
- uncertainty may be checked with higher-resolution, non-OCR rendering; engine/extractor output may not resolve it.

If no row satisfies C1–C4, preserve a NULL Selection Record after the full frozen universe has been evaluated. Do not amend this protocol to rescue a result.

## 11. Tie-break and stopping rule

Within the one-file universe, the deterministic tie-break is:

1. earliest `pdfPageIndex`; then
2. topmost fully qualifying physical row on that page.

The subsequent task must inspect in document order, stop immediately at the first full C1–C4 pass, and not inspect later rows for a better candidate. It must evaluate the full universe only if no eligible row is found.

## 12. Prior exposure and explicit non-criteria

The Source Survey visually inspected `1.pdf` page 1, and this protocol task re-rendered all three pages only to confirm structural scope, unit, repeated ledger headers, and embedded-box exclusion. Row labels and amount cells were therefore incidentally visible. No candidate was enumerated or compared, no amount was transcribed into this artifact, and no blind-selection claim is made. Prior exposure cannot influence eligibility or tie-break.

The following are explicitly not selection criteria: amount magnitude; delta sign; remarks content; expected benchmark result or engine behavior; Docling suitability; text-extraction quality; MOF/RS correspondence; production usefulness; file page count; unusual organization; visual salience; prior familiarity/exposure; source-survey inspection depth; “Case-009-ness” or novelty; package representativeness; and downstream implementation convenience.

## 13. Requirements for the next Selection Record

A Selection Record must preserve the canonical source identity, package/file identity, SHA-256, `pdfPageIndex`, printed locator if present, standard-ledger grammar proof, source-visible organization/division scope, item context, request number, expense code, label, unit evidence locator/scope, C1–C4 results, rejected predecessor rows/reasons, tie-break, and prior exposure. It must not record amount values or create Ground Truth.

Permitted inspection is direct source-safe visual PDF inspection and high-resolution non-OCR rendering. OCR, benchmark engines, Ground Truth, MOF/RS data, arithmetic reconstruction, parser/normalizer/evaluator changes, and source-lock/registry changes are prohibited.

## 14. Frozen facts and unresolved questions

Frozen: Option A; canonical `1.pdf`; standard-ledger-only 3-page universe; local `千円` scope; file-aware/no-cross-file context; C1–C4; exclusions; ambiguity handling; tie-break; and NULL possibility.

Unresolved but not needed for this task: whether another of the 49 unregistered files should later be canonicalized; exhaustive cross-file continuation/recurrence; and package-wide embedded-grammar coverage. None permits a change to this protocol during selection.

## 15. Frozen-artifact integrity and next task

The Case-009 Source Survey report/evidence remains byte-identical to `e640dc21c5bf536ab5ca40b20ed4b3ea8b2b3c11`. The Case-006–010 Selection Freeze, Cases 001–008, `scripts/`, parser/normalizer/evaluator, source lock/registry, and production code remain unchanged by this task.

Recommended next task: **Case-009 Row Selection** — apply this protocol unchanged to the locked `1.pdf`, select exactly one row if one exists (or preserve a NULL Selection Record), then stop before Ground Truth.

**The Case-009 selection source, universe, eligibility criteria, context rules, unit rules, ambiguity handling, and tie-break were frozen before candidate-row enumeration. The already-locked `1.pdf` was chosen on source-admissibility/provenance grounds, not because of candidate-row content. No row was selected, no Ground Truth was created, and no benchmark or OCR experiment was run.**
