# Batch-001 Authority-02 Shugiin Source Survey

Date: 2026-09-29 (Asia/Tokyo)
Authority: `batch-001-authority-02` / `shugiin` / 衆議院

## Scope

This authority-isolated task covers official-source provenance, acquisition, package/representation/grammar/context/unit survey, and source admissibility only. It does not freeze a preflight profile or perform candidate enumeration, canonical extraction, Ground Truth, benchmark, OCR, CSV, or MOF work.

## Official source and byte identity

The official 衆議院 landing page, `https://www.shugiin.go.jp/internet/itdb_annai.nsf/html/statics/osirase/kaikei-gaisan.html`, returned HTTP 200 on 2026-09-29 19:30 JST and identifies itself as `概算要求書等の公表について`. The official-domain year-specific direct PDF returned HTTP 200 / `application/pdf`, 68,050 bytes. Its internal cover title is `令和6年度歳出概算要求書`; SHA-256 `30d0dfc363a1f4f7e37b64a0059b48c2f03f13f997eb251e7ef5acaabd37c435` exactly matches existing lock entry `shugiin-fy2024-general-account-expenditure-request`.

The current landing page did not itself establish the historical FY2024 direct-link placement during this survey. The direct official-domain file, its internal FY2024 title, and the pre-existing locked provenance establish a bounded archival-discovery caveat rather than a source-identity failure. The lock and registry were only read and reverified; neither was changed.

## Package decision

The canonical authority-02 source is one 36-page PDF. No cross-file continuation is claimed for this authority.

## Representation and structure

The PDF is unencrypted A4 landscape (842×595 points), PDF 1.3, Producer `List Creator`, with CID TrueType resources and native extractable text. `pdfimages -list` found no raster image objects. A page-by-page text-presence census covered all 36 pages; three separator pages produced only form-feed-sized output.

Visual inspection at 180 dpi covered `pdfPageIndex` 0, 1, 6, 17, and 35. It confirmed cover/contents, a summary table, an opening standard expenditure ledger, continuing ledger pages with printed `国（衆）` prefix/header, and remarks-side explanatory/nested tables. The sampled opening detailed-ledger page visibly declares `（単位：千円）`; sampled later material includes local `百万円` tables. Main-ledger inheritance and grammar-boundary handling remain preflight questions.

## Context and admissibility

The opening detailed page provides authority/ledger context; sampled later pages repeat a printed prefix and ledger heading. Main ledger and remarks-side embedded structures must be separated in preflight. No candidate row was enumerated and no amount was transcribed.

**Admissibility: `ADMISSIBLE_WITH_CAVEATS`.** Official direct-file provenance, FY2024 internal identity, canonical locked bytes, single-file boundary, and inspectable structure are established. The current landing-page historical-link limitation must remain in provenance. This is not an extraction-success or semantic-candidate verdict.

## Coverage and non-actions

Exhaustive checks: SHA-256, PDF metadata, font/image listing, and page-level text presence. Visual checks were sampled only; no all-page visual grammar claim is made. Representative rows and values were incidentally visible during structural inspection but were not selected, recorded, or used as Ground Truth.

No authority-local execution-state JSON was created: the required survey evidence already records B1/B2 facts, while the frozen execution template reserves lifecycle state for a later authority execution/freeze artifact. Global state files were not edited on this isolated branch.

## Preflight handoff

Freeze only after integration: grammar partitions; main-ledger versus remarks-side boundary; context/continuation permissions; main versus local unit scope; and preservation of the archival direct-file provenance caveat.
