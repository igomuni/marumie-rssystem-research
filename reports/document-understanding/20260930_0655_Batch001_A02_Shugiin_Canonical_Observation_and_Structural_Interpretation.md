# Batch-001 A02 Shugiin: Canonical Observation and Structural Interpretation

## Scope

This authority-isolated execution completed S2 source observation and S3 structural interpretation only. It used locked `kaikei-saishutsugaisan6.pdf` (`30d0dfc363a1f4f7e37b64a0059b48c2f03f13f997eb251e7ef5acaabd37c435`; 36 pages) under the frozen A02 preflight profile.

The historical landing-page caveat is retained: locked byte identity and official-domain direct/internal FY2024 evidence are confirmed, while the current landing page alone did not establish historical FY2024 direct-link placement.

## Method and raw-evidence preservation

The authority-local, non-production procedure `s2_s3_observation_procedure.py` used Poppler 26.09.0 `pdftotext -bbox-layout` without a reading-order sort option. It retains native XML separately under `raw/poppler-bbox-layout.xml` and emits page/block/line/word S2 records in engine emission order with Poppler coordinates. No OCR, rendering, or external source was used for machine extraction.

All 36 pages were processed. S2 produced 17,072 observations: 3,341 blocks, 4,990 lines, and 8,705 words, with zero replacement characters. Page/block/line/word geometry is retained where emitted. The XML output is engine-native evidence, while the JSONL S2 observations only reference it; neither field is normalized.

## S3 structural result

S3 produced 8,437 nodes and 10,361 edges. Of the nodes, 8,368 are source-observed and 69 are structurally inferred under the documented geometry/header rules. The run identifies 30 outer-ledger pages and retains 6 pages as `unclassifiedStructure`; no unclassified page was forced into a grammar family.

Remarks-side material is retained through separately inferred geometry-bounded regions containing source-observed blocks. The raw S2 observations retain distinct source-visible `千円` and `百万円` declarations; S3 retains bounded partitions only and never normalizes either unit or lets a local-table unit inherit into the outer grid. No cross-page or cross-file relation was produced (both counts are zero).

## Validation and reproducibility

Initial pre-completion validation found that Poppler split some header glyphs, so the provisional literal compound-token rule classified all pages as unclassified. The authority-local procedure was corrected before completion to use the documented split-header token set, then both complete runs were repeated. This was not a shared implementation or profile change.

The two corrected runs are byte-identical for raw XML, source observations, nodes, edges, and manifests; their deterministic IDs and counts match. The reproducibility record is `evidence/document-understanding/batch-001/authority-02-shugiin-s2-s3-reproducibility.json`. Visual checks of `pdfPageIndex` 6, 17, and 35 confirmed outer-grid/local-table separation and the local `百万円` boundary.

## Deliberate non-actions and next boundary

No S4 normalization, S5 semantic candidates, S6 financial association, S7 canonical freeze, GT, benchmark, OCR, CSV, MOF work, source-lock change, or shared-code change occurred. Next: authority-local artifact integration and structural review before any S4 decision.
