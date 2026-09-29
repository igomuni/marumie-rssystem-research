# Batch-001 A01 Kunaicho: Canonical Observation and Structural Interpretation

## Scope

This authority-isolated execution completed S2 source observation and S3 structural interpretation only. It used locked `r06-02.pdf` (`ffab15073beb2411d9396f7ca0cbb1ce33ccdf99be05e6d0d88e29366912e261`; 33 pages) under the frozen A01 preflight profile.

## Method and raw-evidence preservation

The authority-local, non-production procedure `s2_s3_observation_procedure.py` used Poppler 26.09.0 `pdftotext -bbox-layout` without a reading-order sort option. It retains native XML separately under `raw/poppler-bbox-layout.xml` and emits page/block/line/word S2 records in engine emission order with Poppler coordinates. No OCR, rendering, or external source was used for machine extraction.

All 33 pages were processed. S2 produced 19,442 observations: 4,886 blocks, 5,514 lines, and 9,009 words, with zero replacement characters. Page/block/line/word geometry is retained where emitted. The XML output is engine-native evidence, while the JSONL S2 observations only reference it; neither field is normalized.

## S3 structural result

S3 produced 10,497 nodes and 14,037 edges. Of the nodes, 10,434 are source-observed and 63 are structurally inferred under the documented geometry/header rules. The run identifies 27 outer-ledger pages and retains 6 pages as `unclassifiedStructure`; no unclassified page was forced into a grammar family.

Remarks-side material is retained through separately inferred geometry-bounded regions containing source-observed blocks. It was not flattened into outer-ledger rows. The source-visible opening `（単位：千円）` remains raw S2 text; S3 records only its partition boundary, not a normalized or financial unit. No cross-page or cross-file relation was produced (both counts are zero).

## Validation and reproducibility

Initial pre-completion validation found that Poppler split some header glyphs, so the provisional literal compound-token rule classified all pages as unclassified. The authority-local procedure was corrected before completion to use the documented split-header token set, then both complete runs were repeated. This was not a shared implementation or profile change.

The two corrected runs are byte-identical for raw XML, source observations, nodes, edges, and manifests; their deterministic IDs and counts match. The reproducibility record is `evidence/document-understanding/batch-001/authority-01-kunaicho-s2-s3-reproducibility.json`. Visual checks of `pdfPageIndex` 6, 16, and 32 confirmed outer-grid/remarks separation and the absence of a basis for cross-page inheritance.

## Deliberate non-actions and next boundary

No S4 normalization, S5 semantic candidates, S6 financial association, S7 canonical freeze, GT, benchmark, OCR, CSV, MOF work, source-lock change, or shared-code change occurred. Next: authority-local artifact integration and structural review before any S4 decision.
