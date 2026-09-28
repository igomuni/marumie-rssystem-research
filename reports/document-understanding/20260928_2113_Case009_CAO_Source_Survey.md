# Case-009 Cabinet Office (CAO) Source Survey

Status: **source/package/context survey only**

Date: 2026-09-28 (Asia/Tokyo)

Branch: `research/case-009-cao-source-survey`

Base: `origin/main@d2a5cae610c005967f01fd3181ed8e2bb3fefc8b`

## 1. Executive summary

**SUITABLE WITH CAVEATS.** The actual official FY2024 CAO package has **51 PDFs** (`0.pdf` through `50.pdf`), not an assumed approximate count. It contains one cover/TOC file and 50 separately scoped detail files (394 physical pages total; 369 detail pages). All 50 detail-file starts expose the same standard `歳出概算要求額明細表` grammar and a `千円` declaration, but each also declares a specific organizational/divisional scope at file start. The source therefore combines grammar homogeneity with a heterogeneous partition of contextual scopes.

This is not evidence that the numeric filenames or package order alone carry semantics. Rather, file boundaries delimit explicitly declared scopes, while recurring high-level hierarchy labels make file identity—or the equivalent start-of-file scope declaration—necessary to distinguish context safely. Seven stratified end→start boundary checks found a fresh title/header/scope at the next file, not a continuation dependent on the previous file. This negative finding is sampled, not exhaustive.

The exploratory outcome is a combined **H2/H3** result: file boundaries are context-bearing partition boundaries and the package is heterogeneous by organizational/divisional scope; however the detail grammar is a repeated, known standard-ledger family. The evidence does not support a claim that package order is semantically necessary, nor that CAO is merely a size-scaled, context-free split.

## 2. Scope and non-goals

This task surveyed source acquisition, package topology, representation, grammar, context, unit, and file identity. It did not freeze a selection protocol, choose a file or row, apply eligibility criteria, transcribe target amounts, create Ground Truth, run a benchmark/OCR experiment, or modify parsing, normalization, evaluation, linkage, or production behavior.

## 3. Frozen exploratory question

Case-009's frozen question is whether extreme split packaging produces a new context/source-identity mechanism or only a packaging-scale difference. The symmetric hypotheses were retained:

- H1: packaging-only, with known local grammar/context mechanisms;
- H2: file identity/boundaries are necessary for semantic or context resolution;
- H3: the split package is heterogeneous in section, organization, grammar, or context scope;
- H4: mixed/other.

No hypothesis was treated as the expected outcome, and a no-new-mechanism outcome remains valid.

## 4. Source provenance and acquisition

The official landing page is `https://www.cao.go.jp/yosan/soshiki/r06/yosangaisan_r6.html`. Direct enumeration of its links found every package member from `pdf/0.pdf` through `pdf/50.pdf`.

Two existing locked inputs were re-verified against their raw binaries and the source lock:

| package index | repository source ID | SHA-256 |
|---:|---|---|
| 0 | `cao-fy2024-general-account-expenditure-request-cover` | `315909085871656cc0428feaa5941ed456dd8d024c6511e511e86ab652623b33` |
| 1 | `cao-fy2024-general-account-expenditure-request-detail-01` | `7b5de5dbd397c7067cab4ea527ef02681e91265914057651ee5b886174de7f4e` |

The remaining 49 official PDFs were temporarily acquired only to establish the package census. Their hashes are recorded in the evidence manifest, but they were deliberately **not** added to `sources/source-lock.json`, `sources/source-registry.csv`, or repository raw storage. Thus their survey observations are an unregistered official snapshot, not newly locked canonical source identities.

## 5. Package manifest and census

The complete per-file manifest—package index, official filename/URL, existing-lock versus temporary-snapshot status, bytes, SHA-256, pages, metadata, text signal, first-page scope, printed prefix, grammar, and unit classification—is [case-009-source-survey.json](../../evidence/document-understanding/case-009-source-survey.json).

| package segment | files | pages | source-side classification |
|---|---:|---:|---|
| index 0 | 1 | 25 | cover/TOC / package navigation |
| indices 1–40 | 40 | 244 | standard ledger; generally `内（本）`, with distinct CAO divisions/offices |
| indices 41–50 | 10 | 125 | standard ledger; distinct organization families and printed prefixes |
| total | 51 | 394 | one official package with 50 scoped ledger files |

Detail-file page counts range from 1 to 55. Distribution: 9 one-page files, 16 files of 2–3 pages, 11 of 4–7, 11 of 8–19, and 4 of 20+ pages. This is an exhaustive metadata census across the 51 downloaded files.

## 6. Representation

All 51 temporary/locked binaries are landscape A4, permission-only AES encrypted (print/copy permitted), with Producer `List Creator`. `pdftotext` returned non-empty first-page text for all files; visual renders of the representative strata were legible. Most detail PDFs list two fonts; six list three. This is native text/document representation, not the Case-006 vector-outline/no-text-layer mechanism.

Producer uniformity is reported as metadata only; it is not used as a grammar or context inference.

## 7. Package partition model

`0.pdf` is the package-level cover/TOC and identifies the CAO detail-table family. Every `1.pdf`–`50.pdf` begins a fresh standard-ledger title, standard column header, unit declaration, and a parenthetical division/organization scope. The 50 detail PDFs are not mere arbitrary page chunks: their starts identify distinct units such as internal CAO divisions, policy offices, commissions, and later separately coded organization families.

The filenames are numeric and do not themselves state a division name. The associated source-document start, not numeric order alone, supplies the readable scope declaration.

## 8. Layout and document grammar

The cover is navigation/TOC grammar. All 50 detail files expose the known standard-ledger header structure: request number, matter/hierarchy, previous/FY2024/delta columns, and remarks. Representative visual inspection covered package start (0/1), short and medium files (16/23), largest file (34), the organization-family transition (41/42), and package end (50).

No staffing, policy-framework, or narrative-only detail-file grammar was identified in the exhaustive first-page census. This is a first-page/metadata conclusion, not an exhaustive page-by-page classification of every possible embedded box.

## 9. Organization context

Organization/division context is printed on each detail file's first page. In the `内（本）` group, high-level `010 内閣本府` commonly recurs while the parenthetical division scope differs. Indices 41–50 demonstrate further organization-level partitions and printed-prefix changes, including `内（地）`, `内（知）`, `内（健）`, `内（宇）`, `内（北）`, `内（海）`, `内（平）`, `内（官）`, and `内（沖）`.

The evidence supports a **file-section-opening scope** mechanism. Each inspected file can recover its own scope from its own first page; no file-order lookback was observed as necessary for those starts. Frequency of organization re-declaration inside every internal page was not exhaustively measured.

## 10. Item context

The detail files retain ordinary ledger hierarchy beneath the file-start scope. Recurrent generic parent hierarchy is visible in multiple `内（本）` files, while local division titles distinguish their scope. This establishes that file identity or an equivalent local scope anchor can matter even when a higher-level organization/item-looking label recurs.

This survey did not enumerate physical rows, test exact item recurrence across all 50 files, or decide an item-context lookback rule. Same-page versus nearest-preceding item behavior remains for a later protocol to freeze against a defined source universe.

## 11. Unit behavior

All 50 detail first pages explicitly declare `（単位:千円）`. With the ledger title also occurring at the file opening, the supported scope is **file-section-opening**: the unit governs the file's detail ledger unless a later source-safe inspection identifies an embedded local grammar. It is not assumed to be package-global merely because the observed detail starts share the same unit.

## 12. Source and file identity semantics

File identity is more than an accidental download locator: it marks the boundary of a document that declares one divisional/organizational scope. In the `010 内閣本府` group, that division scope disambiguates recurring parent labels. However, numeric filename/index is not itself demonstrated to be a semantic key; the source title supplies the actual scope.

Accordingly, file identity should be preserved in future provenance as a **semantic context partition plus locator**, while package order should be treated as an official navigation/order attribute, not a proven context-resolution requirement.

## 13. Cross-file continuation and recurrence

Seven predeclared stratified boundaries were checked: 1→2, 15→16, 23→24, 34→35, 40→41, 41→42, and 49→50. Each next file begins with a fresh title/header/unit/scope declaration. No predecessor-dependent continuation was observed in those samples, including transitions inside `内（本）` and to changed printed-prefix/organization families.

The full 50-file first-page census reinforces that every detail file starts a fresh declared scope. It does **not** prove no logical item ever recurs or splits across files; exact recurrence/continuation across every possible end/start pair was not exhaustively evaluated.

## 14. Stratified inspection methodology and coverage

| method | coverage | purpose |
|---|---|---|
| official landing-page link census | all 51 links | actual file count/order |
| download, SHA, bytes, `pdfinfo`, `pdffonts`, first-page text | all 51 files | manifest, representation, title/unit/scope stratification |
| visual first-page render | 0, 1, 16, 23, 34, 41, 42, 50 | cover, early/middle/end, short/large, and changed-scope strata |
| text end→start comparison | 7 predeclared boundaries | continuation versus fresh-start evidence |

Sampling strata were fixed from source-side package position, page-count distribution, and printed-prefix/scope difference before reading boundary content. Amount magnitude, target-row shape, and engine behavior were not selection inputs.

## 15. Comparison with Case-007

Case-007/CAS established file-scoped organization context across its 17-file package. CAO is larger (51 rather than 17 files) and its file-start scope is finer-grained: the same high-level `010 内閣本府` can recur across many separately scoped division files, while later files start distinct organization families. Both cases require file-aware provenance; CAO differs by exposing repeated parent hierarchy plus division-scope partitioning at a larger scale.

This does not import Case-007's selection/amount hierarchy or NULL result into CAO. Nor does it establish that CAO has the same exact context mechanism on every internal page.

## 16. H1–H4 assessment

| hypothesis | assessment | evidence and limit |
|---|---|---|
| H1 packaging-only | supported for grammar, insufficient as complete account | all 50 detail starts share the standard ledger; scope partition cannot be reduced to file count alone |
| H2 file identity context-bearing | supported, bounded | fresh file-start division/organization declarations and recurring high-level hierarchy make file/scope provenance necessary; numeric order alone is not proven semantic |
| H3 heterogeneous split | supported at partition level | 50 scopes and ten printed-prefix families/changes; no alternate first-page grammar found |
| H4 mixed/other | partially applicable | the best account is homogeneous ledger grammar plus heterogeneous scope partitioning; internal-page mechanisms remain incompletely characterized |

## 17. Exploratory verdict

**C. Heterogeneous package, with a bounded H2 context finding.** CAO is not a new layout family merely because it has 51 files. It is a repeated standard-ledger family partitioned into multiple organizational/divisional scopes, with file boundaries carrying source-declared scope. Whether this represents a categorically new mechanism beyond Case-007 rather than a finer-grained variant remains unresolved at internal-page/context-resolution depth.

## 18. Suitability verdict

**SUITABLE WITH CAVEATS.** A future protocol can work from a source-safe package census and a file-aware provenance model. Before it chooses a selection universe, it must address the load-bearing acquisition caveat: only files 0 and 1 are currently hash-locked; any other proposed target file needs an explicit lock/provenance decision rather than treating this temporary survey snapshot as canonical. The protocol must also define whether it targets one file, one scope family, or another deterministic universe before candidate inspection.

## 19. Incidental exposure

First-page text and representative visual inspection necessarily exposed ledger rows and amounts. No candidate rows were enumerated, no criterion was applied, no amount value was transcribed into a selection or Ground Truth artifact, and no file was preferred because of its content. This is not claimed as a blind survey.

## 20. Limitations and unresolved questions

- Internal page-by-page organization/item re-declaration was not exhaustively mapped.
- Exact cross-file recurrence/splitting of every item was not exhaustively tested.
- Seven boundary comparisons cannot prove absence of continuation everywhere.
- The 49 newly downloaded files are temporary official snapshots, not lock entries.
- Whether CAO's file-scoped division context is a new mechanism or a granularity variant of CAS needs a later, pre-frozen protocol inquiry.

## 21. Handoff facts for a Selection Protocol

- Actual package: official `0.pdf`–`50.pdf`, 51 files, 394 pages.
- Cover: index 0; candidate detail grammar begins at index 1, but no target file is selected here.
- Detail grammar: standard ledger on all 50 detail first pages; `千円` file-section-opening unit.
- Provenance: preserve package index/file identity plus first-page scope and printed prefix; do not rely on generic parent labels alone.
- Context: each file begins with a scope declaration; no package-order dependency demonstrated; internal-page lookback remains unresolved.
- Acquisition: lock status is complete only for indices 0/1; do not silently promote temporary hashes to canonical locks.
- Selection universe/file choice, eligibility, tie-break, and ambiguity rules remain unmade.

## 22. Recommended next task

**Case-009 Selection Protocol Freeze**—first define a source-safe, lock-aware file/universe decision and a section/file-scoped context rule before any candidate-row enumeration. It must be a separate task and may conclude that additional explicit source-lock work is required before selection.

---

**Case-009 was investigated only as a source/package/context survey. Extreme split packaging was treated as a hypothesis to test, not as evidence of a new mechanism by itself. No selection protocol, row selection, Ground Truth, benchmark run, OCR experiment, parser/normalizer/evaluator change, MOF linkage, or production adaptation was performed.**
