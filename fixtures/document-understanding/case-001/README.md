# case-001

Source: `digital-r6-request-table-01` (令和6年度歳出概算要求書), locked SHA-256 `b77f25b26b5caf82b0b6617fb1af9b3bba9df059a8bf9a8ede63de8d1a8cfe89` — same locked binary used by `scripts/pdf-extraction` and `scripts/request-ingestion`.

## What this case tests

The item-level (項 020) detail row for `情報通信技術調達等適正・効率化推進費`, found on PDF page index 11 (one-based page 12; the document's own printed page label there is "8"):

```text
020 情報通信技術調達等適正
    ・効率化推進費
4 01-95 情報通信技術調達等適正 481,188,232 448,267,326 △ 32,920,906
  ・効率化の推進に必要な
  経費
```

This row is a good Document Understanding test case because:

- the item name and expense name both wrap across two printed lines (multi-line cell reconstruction);
- the three amount columns (previous budget / FY2024 request / delta) must be associated with the correct expense row, not a neighboring row;
- the delta is prefixed with `△` (U+25B3), the standard Japanese government convention for a decrease — an engine that drops this glyph will silently lose the sign;
- the same numbers (`481,188,232` / `448,267,326`) also appear, differently formatted, in the page 5 (index 4) summary table — an engine must not confuse the summary-table row with the item-detail row.

## Ground truth provenance

`ground-truth.json` was produced by manual visual verification against the locked PDF binary (`groundTruthSource: manual_visual_verification_against_locked_pdf`), not derived from any engine's output. It is stored separately from every engine's raw and normalized artifacts so that evaluation never leaks into extraction.

## Why this is not the same row as the page-22-style ministry breakdown

Earlier benchmark/comparison work (Workspace Phase 1D, `scripts/pdf-extraction`) worked with ministry-level system rows (e.g. `財務省システム` on page index 22). `case-001` instead targets the item-level (項) aggregate row that precedes all ministry breakdowns — a different structural pattern (item code + wrapped item name, then request-number + expense-code + wrapped expense name + amount triple) that a Document Understanding engine must recognize independently.
