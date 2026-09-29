# Batch-001 Authority Selection Manifest Freeze

Status: **FROZEN**
Date: 2026-09-29 (Asia/Tokyo)

## 1. Task boundary

This task mechanically applied the already-frozen Batch-001 authority-sampling procedure to the committed FY2024 Population Freeze. It freezes the six primary authority identities, order, batch IDs, waves, and initial statuses only. No authority source work begins here.

## 2. Canonical inputs

- Batch design protocol: `fixtures/document-understanding/batch-001/20260929_1826_Semantic_Data_Batch001_Design_Protocol.md`
- Frozen procedure: `fixtures/document-understanding/batch-001/authority-sampling-procedure.json` at `974140124c715fbe37514e65d43e1d13c2692ede`
- Execution template: `fixtures/document-understanding/batch-001/authority-execution.template.json`
- Population: `fixtures/document-understanding/fy2024-format-census/20260927_1909_FY2024_Population_Freeze.md`, SHA-256 `e3ecf03042e41c862b66625b124c9deabebab1bc2c8bc63b87a1eb7f6955db81`

The procedure was byte-identical to its design-freeze version and was not changed before, during, or after selection.

## 3. Mechanical procedure and audit

The procedure used Population Freeze numbered order, excluded the ten Case-001–010 authority IDs solely for prior research exposure, retained one complete record per authority ID, and selected the first six remaining eligible records. There were 33 population records, 10 prior-exposure exclusions, zero duplicate exclusions, zero missing-required-metadata exclusions, and 23 eligible records. No representation, grammar, package, context, score, amount, source-quality, or convenience criterion was applied.

An independent second implementation of the same frozen filter produced the same six IDs and order. There was no ambiguity and no protocol block.

## 4. Frozen primary manifest

| Rank | Batch ID | Population order | Authority ID | Authority name | Wave | Initial status |
|---:|---|---:|---|---|---:|---|
| 1 | `batch-001-authority-01` | 1 | `kunaicho` | 皇室費 | 1 | `SELECTED_NOT_STARTED` |
| 2 | `batch-001-authority-02` | 2 | `shugiin` | 衆議院 | 1 | `SELECTED_NOT_STARTED` |
| 3 | `batch-001-authority-03` | 3 | `sangiin` | 参議院 | 2 | `SELECTED_NOT_STARTED` |
| 4 | `batch-001-authority-04` | 4 | `ndl` | 国立国会図書館 | 2 | `SELECTED_NOT_STARTED` |
| 5 | `batch-001-authority-05` | 5 | `sotsui` | 裁判官訴追委員会 | 3 | `SELECTED_NOT_STARTED` |
| 6 | `batch-001-authority-06` | 6 | `dangai` | 裁判官弾劾裁判所 | 3 | `SELECTED_NOT_STARTED` |

The wave assignment is mechanical: ranks 1–2 are Wave 1, 3–4 are Wave 2, and 5–6 are Wave 3. Wave is not a priority, difficulty, or source-suitability label.

## 5. No reserve, replacement, or source inference

The frozen procedure specifies six primaries, zero reserve authorities, and no replacement. No seventh-or-later candidate list is created. Nothing about a selected authority's source availability, official page, PDF, canonical bytes, representation, grammar, package, context, unit, row, or semantic suitability was checked or inferred.

## 6. Reproducibility and next boundary

The machine-readable manifest records the exact input SHA-256 values, exclusion counts, filter outcome, fixed ranks, and wave mapping. It can be reproduced from the named committed inputs without a network call or source/content inspection.

No authority branch or worktree was created and Batch execution has not started. The next task is **Batch-001 Wave 1 Source Survey / Source Admissibility — authorities 01 and 02**. It may create the isolated authority workspaces and begin source work, but it must not enumerate candidates before each authority's preflight-profile freeze.

## 7. Integrity and explicit non-actions

The sampling procedure, design protocol, execution template, canonical semantic protocol, reframe, synthesis, Cases 001–010, source lock/registry, scripts, parser, normalizer, evaluator, OCR configuration, and production code are unchanged. No web search, source discovery/acquisition, PDF inspection, representation/grammar/context classification, preflight, canonical extraction, GT, benchmark, OCR, CSV, MOF work, or production change occurred.

**Batch-001 authority selection was frozen by mechanically applying the previously frozen deterministic sampling procedure to the committed FY2024 population, with Cases 001–010 excluded solely for prior research exposure. Six primary authorities were selected with no reserve or replacement list. No authority source was searched, acquired, inspected, classified, or processed, and Batch-001 execution has not started.**
