# Batch-001 Authority-01 Kunaicho Source Survey

Date: 2026-09-29 (Asia/Tokyo)
Authority: `batch-001-authority-01` / `kunaicho` / 皇室費

## Scope

This authority-isolated task covers official-source provenance, acquisition, package/representation/grammar/context/unit survey, and source admissibility only. It does not freeze a preflight profile or perform candidate enumeration, canonical extraction, Ground Truth, benchmark, OCR, CSV, or MOF work.

## Official source and byte identity

The official 宮内庁 landing page, `https://www.kunaicho.go.jp/kunaicho/kunaicho/gaisanyokyu.html`, returned HTTP 200 on 2026-09-29 19:30 JST. Its FY2024 section labels `r06-02.pdf` as `令和6年度概算要求書（皇室費）`. The direct official PDF returned HTTP 200 / `application/pdf`, 79,919 bytes. Its SHA-256 is `ffab15073beb2411d9396f7ca0cbb1ce33ccdf99be05e6d0d88e29366912e261`, exactly matching the existing source-lock entry `kunaicho-fy2024-imperial-household-expense`.

The existing lock and registry were only read and reverified; neither was changed. The acquired raw PDF is git-ignored in this authority worktree.

## Package decision

The canonical authority-01 source is one 33-page PDF. The same official FY2024 landing section also labels an overview and a separately labelled 宮内庁費 request document. Those are source-side supporting/rejected-candidate references, not part of the canonical 皇室費 file decision. No cross-file continuation is asserted for authority-01.

## Representation and structure

The PDF is unencrypted A4 landscape (842×595 points), PDF 1.3, Producer `List Creator`, with CID TrueType resources and native extractable text. `pdfimages -list` found no raster image objects. A page-by-page text-presence census covered all 33 pages; three separator pages produced only form-feed-sized output.

Visual inspection at 180 dpi covered `pdfPageIndex` 0, 1, 6, 16, and 32. It confirmed cover/contents, a summary table, an opening standard expenditure ledger, continuing ledger pages with printed `皇（皇）` prefix/header, and remarks-side explanatory/nested tables. The sampled opening detailed-ledger page visibly declares `（単位：千円）`. Later inheritance and local nested-table unit behavior remain preflight questions, not frozen rules.

## Context and admissibility

The opening detailed page provides authority/ledger context; sampled later pages repeat a printed prefix and ledger heading. The main ledger and remarks-side embedded structures must be separated in preflight. No candidate row was enumerated and no amount was transcribed.

**Admissibility: `ADMISSIBLE_FOR_PREFLIGHT`.** Official provenance, FY2024 identity, canonical locked bytes, a single-file boundary, and inspectable source structure are established. This is not a claim that extraction will succeed or that any semantic candidate exists.

## Coverage and non-actions

Exhaustive checks: SHA-256, PDF metadata, font/image listing, and page-level text presence. Visual checks were sampled only; no all-page visual grammar claim is made. Representative rows and values were incidentally visible during structural inspection but were not selected, recorded, or used as Ground Truth.

No authority-local execution-state JSON was created: the required survey evidence already records B1/B2 facts, while the frozen execution template reserves lifecycle state for a later authority execution/freeze artifact. Global state files were not edited on this isolated branch.

## Preflight handoff

Freeze only after integration: grammar partitions; main-ledger versus remarks-side boundary; context/continuation permissions; unit scope; and representation-aware observation handling.
