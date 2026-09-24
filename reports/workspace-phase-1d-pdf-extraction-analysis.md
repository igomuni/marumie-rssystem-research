# Workspace Phase 1D - PDF extraction research package

Status: **research/design completed in ChatGPT; local locked-PDF acceptance pending integration run**

Date: 2026-09-25

Base GitHub checkpoint:

```text
64913ae9a2fd024bcca171593244e9996899a54e
feat: add primary-source acquisition and hash locking
```

## Purpose

Close the next reproducibility gap:

```text
locked PDF binary
    -> deterministic page-aware text extraction
    -> historical fixture provenance comparison
```

The research subject remains the two locked Digital Agency FY2024 PDFs:

- `digital-r6-request-table-01`
  - locked SHA-256: `b77f25b26b5caf82b0b6617fb1af9b3bba9df059a8bf9a8ede63de8d1a8cfe89`
  - 32 pages
- `digital-r6-important-policy`
  - locked SHA-256: `72fb06310b15cc9b1c5a95283a2c60fed567db06e5caefbe48d2f65f215cc070`
  - 1 page

## Important execution limitation in this ChatGPT VM

The container in this session could not resolve `www.digital.go.jp`, so the locked PDF binaries could not be materialized into `/mnt/data` with `curl`.

The public PDF parser available to this chat *could* read the same public PDFs page-by-page. Therefore this phase did two things:

1. performed a page/line-aware provenance audit of the existing historical fixtures against the current public PDFs;
2. generated the deterministic locked-PDF extraction implementation that should be run in the local repository where Phase 1C already succeeded.

**Do not mark PDF extraction itself reproducible until the local repository run passes the acceptance checks below.**

## Historical fixture provenance result

A strong new result emerged.

The legacy markers in the historical fixtures, such as:

```text
L858@P22
L951@P24
L988@P25
```

align with the current public-PDF parser's line numbers and zero-based page indexes.

This indicates the legacy line/page locators are not arbitrary annotations. They came from the same or a closely equivalent page-aware extraction representation.

### Normal-request fixture

22 fixture records were checked.

```text
15 exact parser-line matches
 6 structured-row matches
 1 contiguous logical-row reconstruction
22/22 page-index matches
```

The six structured-row cases are the `情報処理業務庁費` rows. The current public parser exposes the row as `情報処理業務庁` plus the same three amount columns and a trailing explanatory column; the historical fixture restores `費` and removes the trailing explanatory material.

The final fixture row beginning at legacy `L988` is explicitly curated:

```text
historical fixture:
95016-2125-14-6420 情報通信技術調達等適正・効率化推進委託費 1,784,443 1,367,993 416,450
```

Current public parser representation spans four contiguous lines:

```text
L988 情報通信技術調
L989 達等適正・効率
L990 化推進委託費
L991 1,784,443 1,367,993 416,450 ...
```

Therefore the historical fixture is **curated extraction**, not raw parser output.

### Important-policy fixture

All three system-related rows are exact matches on `P0`:

```text
デジタル庁システム等 17,245,103
デジタル庁・各府省共同プロジェクト型システム 51,024,815
各府省システム 50,502,710
```

### Provenance conclusion

The historical fixture is much stronger than an undocumented hand transcription:

```text
public PDF
 -> page-aware extraction
 -> curated row selection / reconstruction
 -> historical fixture
```

However, future canonical provenance should **not** depend on legacy global `Lxxx` numbers.

Use:

```text
source SHA-256
+ zero/one-based PDF page locator
+ raw text item coordinates
+ reconstructed text
+ extractor/version
+ ordering version
```

Legacy `Lxxx@Pyy` stays as historical metadata.

## Additional Phase 1C gap discovered

Phase 1C has `sources:lock` and `sources:verify`, but on a fresh checkout:

- `sources:verify` downloads and verifies bytes, then discards them;
- `sources:lock` materializes bytes, but also rewrites the committed lock.

That means there is no safe command that simply reconstructs `sources/raw/` from the committed lock.

This bundle therefore adds:

```bash
npm run sources:fetch
```

Semantics:

```text
read committed source-lock
 -> download URL
 -> verify HTTP/hash/size
 -> write sources/raw only if it matches
 -> NEVER modify source-lock
```

This is necessary for true clean-checkout reproducibility.

## Proposed deterministic extractor

The bundle adds `scripts/pdf-extraction/` using exact:

```text
pdfjs-dist 4.10.38
```

The extractor preserves two layers.

### Raw item layer

Each PDF.js text item retains:

```text
sourceId
sourceSha256
extractor / version
orderingVersion
pdfPageIndex       (zero-based)
pdfPageNumber      (one-based)
itemIndex
text
x / y / width / height
hasEOL
fontName
```

### Deterministic reconstructed-line layer

Items are grouped by page and baseline Y with a documented geometric tolerance, then ordered by X with original item index as a tie-breaker.

Raw items are never discarded, so reconstruction logic can be revised without losing source-level evidence.

Generated artifacts are intentionally not committed:

```text
derived/pdf-extraction/*.items.jsonl
derived/pdf-extraction/*.lines.jsonl
derived/pdf-extraction/*.pages.txt
derived/pdf-extraction/run-manifest.json
```

## Fixture comparison implementation

`compare-fixtures.mjs` uses same-page matching only and preserves fixture order to disambiguate repeated labels.

Match classes:

```text
exact
normalized_match
curated_prefix
structured_row_match
contiguous_reconstruction
contiguous_curated_prefix
contiguous_structured_row_match
not_found
```

Amount similarity alone is **not** sufficient. `structured_row_match` requires the same budget code plus the first three amount columns on the expected page.

This is consistent with ADR-002 because the amount columns validate an already constrained source row; they do not select a project/system linkage target.

## Acceptance criteria for local integration

Run from the repository after importing the bundle:

```bash
npm ci --prefix scripts/pdf-extraction
npm run sources:fetch
npm run sources:verify
npm run extract
npm run extraction:test
npm run extraction:determinism
npm run extraction:compare
npm run validate
```

Acceptance requires:

1. both source binaries still match the committed Phase 1C hashes;
2. request PDF page count is 32;
3. important-policy PDF page count is 1;
4. golden page-text assertions pass;
5. two clean extraction runs produce identical canonical output hashes;
6. fixture comparison produces no unexplained `not_found` records;
7. historical fixtures themselves are not modified;
8. no PDFs or generated large extraction dumps are staged.

Only after these pass should `protocol/REPRODUCIBILITY.md` mark PDF extraction as reproducible and `state/CURRENT_STATE.json` move to Workspace Phase `1D`.

## Next research direction after acceptance

If PDF.js comparison confirms the historical fixtures can be recovered with the documented curated transformations, the next step should be:

```text
locked PDF
 -> deterministic extraction
 -> explicit fixture-generation rules
 -> generated fixture
 -> existing ingestion PoC
 -> staging
 -> normalized
 -> validation
```

The historical fixtures should first be preserved as golden references; do not replace them until generated-fixture equivalence is demonstrated.

---

## Integration Validation (local, Sonnet-run)

Date: 2026-09-25
Environment: Node v24.9.0, npm 11.6.0, macOS (Darwin 25.6.0)

### Bundle verification

- Bundle SHA-256 matched the ChatGPT-reported hash exactly.
- All 17 per-file SHA-256/size entries in `MANIFEST.json` verified against the extracted contents.
- Base commit `64913ae9a2fd024bcca171593244e9996899a54e` matched local `HEAD` exactly before integration.

### Corrections required during local integration

Three issues were found and fixed; none required deviating from the pinned extractor version or rewriting historical fixtures.

1. **`package-lock.json` had environment-specific `resolved` URLs.** The bundle's lockfile pointed at `packages.applied-caas-gateway1.internal.api.openai.org` (ChatGPT's own sandboxed npm proxy), which is unreachable from this machine. Per `SONNET_IMPORT.md`'s documented fallback, `package-lock.json` was deleted and regenerated with `npm install --prefix scripts/pdf-extraction`. `pdfjs-dist` still resolves to exactly `4.10.38` (confirmed via `npm ls`), now from the public registry. The extractor version was not changed.
2. **Missing `cMapUrl`/`cMapPacked`.** `scripts/pdf-extraction/src/extract.mjs` called `pdfjs.getDocument()` without `cMapUrl`/`cMapPacked`. The `digital-r6-request-table-01` PDF uses an embedded CJK font requiring external CMap data; without it, PDF.js silently returned 0 text items for the entire 32-page document (only a font-load warning, no thrown error). Fix: point `cMapUrl` at `pdfjs-dist`'s bundled `cmaps/` directory (mirroring the existing `standardFontDataUrl` pattern) and set `cMapPacked: true`. After the fix: 12,683 raw items / 1,226 reconstructed lines across 32 pages (previously 0/0).
3. **Non-portable output paths in the extraction manifest.** `extract.mjs` recorded `outputs.itemsJsonl`/`linesJsonl`/`pagesTxt` as paths relative to `process.cwd()`, but `test.mjs` re-joined them against the absolute `ROOT`. Because `npm --prefix scripts/pdf-extraction run extract` sets `cwd` to that subdirectory, the stored relative path (`../../derived/...`) resolved outside the repository when joined with `ROOT`, causing `ENOENT` in `extraction:test`. Fix: compute those paths relative to `ROOT` instead of `process.cwd()`.

One additional, narrowly-scoped comparison fix (not a fixture rewrite): `scripts/pdf-extraction/src/test.mjs`'s golden-assertion check and `compare-fixtures.mjs`'s classifier both originally used whitespace-collapsing (`normalizeText`) rather than whitespace-stripping (`compactText`) for some comparisons. The source PDF renders certain heading/label rows (係, システム names) with a real embedded space glyph between every CJK character (confirmed via raw item coordinates — these are literal `' '` text items with their own width, not a reconstruction-heuristic artifact). CJK text does not use inter-character spaces as word separators, so `test.mjs` was updated to compare using `compactText` (already defined in `common.mjs` and already used by `compare-fixtures.mjs`'s window-based matching) instead of `normalizeText`. This is a general rule applied uniformly, not a per-fixture patch.

### Golden page-text assertions (`npm run extraction:test`)

PASS. Page counts: `digital-r6-request-table-01` = 32, `digital-r6-important-policy` = 1. All four assertions recovered on their expected zero-based page index: `財務省システム` (page 22), `厚生労働第１係` (page 24), `総務省システム` (page 24), `7,738,305` (page 25); plus the three important-policy rows on page 0.

### Determinism (`npm run extraction:determinism`)

PASS — two clean extraction runs produced byte-identical canonical output hashes:

```text
digital-r6-request-table-01.items.jsonl  403b47cf8df70feec28100cff785f97ed249516e5132df76fa08ae5fb667c1a0
digital-r6-request-table-01.lines.jsonl  bd29feaef177e00558b0e09f6b0866397a0a8956a5411c85a396c5671cdf4d72
digital-r6-request-table-01.pages.txt    80fa4604350a52d0d3a2eb6e8cdb15bf0cee4286905d5bec24f1815c9287c901
digital-r6-important-policy.items.jsonl  76840bb3e352d4722206bb1abc7014c58d36a4fb915d6ae122237758bdf39e53
digital-r6-important-policy.lines.jsonl  3688fcc7942df687cebc81e50b0372cea34ef1a43a6f63991a16732681cf61b6
digital-r6-important-policy.pages.txt    fa9f7cf4a7d3c20e45aaa418fbb772ca97784e43ff202bce7416f610a01f36bb
run-manifest.json                        7e7ca0659c1aabe86b77116c4d22e6b645d27039f8fcf746320275e73886c2bd
```

### Historical fixture comparison (`npm run extraction:compare`)

```text
digital-r6-request-table-01: total 22, contiguous_reconstruction 12, structured_row_match 7, contiguous_delta_glyph_normalized 3
digital-r6-important-policy: total 3, exact 3
```

Zero `not_found`. All 25 fixture rows across both sources have an explainable source path on the expected page.

The 3 `contiguous_delta_glyph_normalized` rows (all in `digital-r6-request-table-01`) are a newly identified, distinct case not present in ChatGPT's own audit sample: they are heading+amount rows where the raw extracted text includes a literal `△` (U+25B3 WHITE UP-POINTING TRIANGLE) immediately before the third amount column — the standard Japanese government budget-document convention marking a decrease — which the historical curated fixture omits entirely (it keeps only the bare digits). Example:

```text
historical fixture:   001 財務省システム 108,761,287 102,935,743 5,825,544
extracted (raw):       001 財 務 省 シ ス テ ム 108,761,287 102,935,743 △ 5,825,544
```

This was verified as the sole difference (confirmed by direct comparison after stripping only the `△` glyph and all whitespace from both sides) and handled with a new, explicitly labeled comparison class (`contiguous_delta_glyph_normalized` / `delta_glyph_normalized_match` in `compare-fixtures.mjs`) rather than silently merging it into `exact` or `contiguous_reconstruction`. It is a general, document-wide rule (any amount preceded by `△`), not a one-off patch for these three rows, and it does not alter the raw extraction output (`items.jsonl`/`lines.jsonl` still contain the `△` glyph) — only the fixture-comparison layer treats its presence/absence as immaterial to content equivalence.

Compared to ChatGPT's own public-parser audit (18 exact + 6 structured + 1 contiguous, no `not_found`), the local PDF.js extractor — because it is a different, independent extractor operating on line-reconstruction from raw coordinates rather than a web-based page renderer — classifies fewer rows as literal `exact` (CJK heading rows contain real embedded space glyphs at the item level, so single-line exact/normalized string comparison fails and the window-based `compactText` comparison takes over instead). Every row still resolves to an explainable, non-fuzzy match class; the match-class distribution differing between extractors is expected and does not indicate a provenance problem — both extractors ultimately confirm the same underlying content.

### Existing pipeline regression check

`npm run validate` (offline, `scripts/request-ingestion`): unaffected — `validationStatus: pass`, unchanged from before this phase. Historical fixtures under `scripts/request-ingestion/fixtures/` were not modified (`git diff` confirms no changes to that directory).

### Conclusion

All acceptance criteria (A. source identity, B. extraction succeeds, C. page awareness, D. golden assertions, E. determinism, F. fixture comparison with a conservative, documented classification) pass. PDF page-aware extraction is now marked reproducible in `protocol/REPRODUCIBILITY.md`. Historical fixture *generation* remains explicitly marked partial/curated — recovering the fixture content from the extractor is not the same as mechanically generating the fixture from the extractor, and that transformation has not been attempted in this phase.
