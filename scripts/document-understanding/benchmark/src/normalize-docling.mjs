#!/usr/bin/env node
// Docling-specific normalizer: Docling's raw artifact is table-cell structured
// (row/col/text), not flat text lines, so it cannot reuse the regex-over-lines
// approach in common.mjs/normalize.mjs unchanged. This file is the "minimal
// interface change" the integration required: a second normalizer producing
// the SAME normalized-artifact shape (result + candidates.itemRows/expenseRows)
// that evaluate.mjs already consumes generically. evaluate.mjs itself is
// unmodified and does not know or care which normalizer produced its input.
//
// This is intentionally blind to ground truth values, exactly like
// normalize.mjs: it only reads ground-truth.json's pdfPageIndex (case
// configuration), never its `result` object.
import path from 'node:path';
import { readJson, writeJson, rawArtifactPath, normalizedArtifactPath, closeCjkWrapSpaces, CJK_RANGE } from './common.mjs';

const DELTA_GLYPH = '△';

// closeCjkWrapSpaces moved to common.mjs (see there for the full rationale):
// pdfjs-baseline was found to need the identical rule, so both normalizers
// now share one implementation. Re-exported here, unchanged in behavior, so
// existing callers/tests that import it from this file keep working.
export { closeCjkWrapSpaces };

// Docling has been observed (this page, multiple independent rows/values —
// see reports/document-understanding/case-001-evaluation.md) to assemble a
// multi-comma-group numeric cell's text with its whitespace-separated groups
// in reversed order, e.g. the source "481,188,232" comes back as
// "232 188, 481,". Reversing the token order recovers the original grouping
// for every observed instance without needing to know the expected value.
// This is a general, engine-specific, documented deterministic rule — not a
// correction fitted to this benchmark case's numbers.
export function reconstructNumericToken(text) {
  const trimmed = text.trim();
  if (!trimmed) return null;
  const hasDelta = trimmed.includes(DELTA_GLYPH);
  const withoutGlyph = trimmed.replace(new RegExp(DELTA_GLYPH, 'g'), '').trim();
  if (!withoutGlyph) return hasDelta ? { deltaGlyphOnly: true } : null;
  const tokens = withoutGlyph.split(/\s+/);
  const reversedJoined = tokens.slice().reverse().join('');
  if (!/^\d[\d,]*$/.test(reversedJoined)) return null;
  const magnitude = Number(reversedJoined.replace(/,/g, ''));
  return {
    raw: trimmed,
    magnitude,
    isDelta: hasDelta,
    signed: hasDelta ? -magnitude : magnitude,
  };
}

const ITEM_CODE_RE = /^(\d{3})\s+(.+)$/;
const EXPENSE_CODE_RE = /^(\d{2}-\d{2})\s+(.+)$/;

// A general safety guard, not specific to any case: amount/annotation cells
// affected by Docling's reversed-comma-group artifact (e.g. "111 222," or
// "534 34, ( 009 22, )") can incidentally match ITEM_CODE_RE's "three digits,
// whitespace, something" shape purely by coincidence of digit grouping and
// stray punctuation. Every genuine item/expense label in this document is
// Japanese text, so requiring an actual CJK character in the matched name
// portion is a general, domain-appropriate (not case-specific) filter —
// stricter than merely "contains a non-digit character," which parentheses
// alone would satisfy.
const CJK_CHAR_RE = new RegExp(`[${CJK_RANGE}]`, 'u');
function looksLikeName(fragment) {
  return CJK_CHAR_RE.test(fragment);
}

function cellsByRow(cells) {
  const byRow = new Map();
  for (const c of cells) {
    if (!byRow.has(c.row)) byRow.set(c.row, []);
    byRow.get(c.row).push(c);
  }
  for (const rowCells of byRow.values()) rowCells.sort((a, b) => a.col - b.col);
  return byRow;
}

// Scans cells to the right of the label cell in the same row for a
// previous/current/delta amount triple. A cell that is exactly the delta
// glyph marks the following numeric cell as the (possibly-signed) delta; a
// combined "delta-glyph and magnitude in one cell" is also handled by
// reconstructNumericToken. Cells that do not parse as numeric (e.g. the
// unrelated annotation-text column) are skipped, not force-fit.
function findTripleToTheRight(rowCells, labelCol) {
  const numericCandidates = [];
  let pendingDeltaGlyph = false;
  for (const cell of rowCells) {
    if (cell.col <= labelCol) continue;
    const trimmed = cell.text.trim();
    if (trimmed === DELTA_GLYPH) {
      pendingDeltaGlyph = true;
      continue;
    }
    const token = reconstructNumericToken(cell.text);
    if (!token || token.deltaGlyphOnly) continue;
    if (pendingDeltaGlyph && !token.isDelta) {
      // The glyph was genuinely observed in a separate, preceding cell in this
      // same row (not inferred). Folding it into `raw` here just represents,
      // in one string, what this row's magnitude+sign cells actually
      // contained — the same information a flat-text engine would have had
      // in one already-combined line. It does not affect `signed`, which was
      // already correctly negative from the moment the glyph cell was seen.
      token.raw = `${DELTA_GLYPH} ${token.raw}`;
      token.isDelta = true;
      token.signed = -token.magnitude;
      pendingDeltaGlyph = false;
    }
    numericCandidates.push(token);
    if (numericCandidates.length === 3) break;
  }
  if (numericCandidates.length < 3) return null;
  const [previous, current, delta] = numericCandidates;
  return { previous, current, delta };
}

// A short (1-2 digit) purely-numeric cell to the LEFT of the label cell, in
// the same row, is the request-number column in every other row on this
// page's table. If no such cell exists for this row (observed for case-001's
// target expense row — Docling's table structure did not produce a cell for
// that column on that specific row), requestNo is honestly recorded as null,
// not guessed.
function findRequestNoToTheLeft(rowCells, labelCol) {
  for (const cell of rowCells) {
    if (cell.col >= labelCol) continue;
    const trimmed = cell.text.trim();
    if (/^\d{1,2}$/.test(trimmed)) return trimmed;
  }
  return null;
}

export function findRows(tables) {
  const itemRows = [];
  const expenseRows = [];
  for (const table of tables) {
    const byRow = cellsByRow(table.cells);
    for (const [row, rowCells] of byRow) {
      for (const cell of rowCells) {
        const text = closeCjkWrapSpaces(cell.text.trim());
        const itemMatch = text.match(ITEM_CODE_RE);
        if (itemMatch && looksLikeName(itemMatch[2])) {
          const triple = findTripleToTheRight(rowCells, cell.col);
          itemRows.push({
            tableIndex: table.tableIndex,
            row,
            col: cell.col,
            // See normalize.mjs's `order` field: an engine-agnostic reading-order
            // key so evaluate.mjs can compare rows across normalizers without
            // knowing which produced them. Tables are compared before rows
            // within them; within this benchmark's single-page, single-table
            // cases the tableIndex term is inert, but it keeps the key
            // meaningful if a future case has multiple tables on one page.
            order: table.tableIndex * 1_000_000 + row,
            itemCode: itemMatch[1],
            itemNameFragment: itemMatch[2],
            triple,
            rawText: cell.text,
          });
          continue;
        }
        const expenseMatch = text.match(EXPENSE_CODE_RE);
        if (expenseMatch && looksLikeName(expenseMatch[2])) {
          const triple = findTripleToTheRight(rowCells, cell.col);
          const requestNo = findRequestNoToTheLeft(rowCells, cell.col);
          expenseRows.push({
            tableIndex: table.tableIndex,
            row,
            col: cell.col,
            order: table.tableIndex * 1_000_000 + row,
            requestNo,
            expenseCode: expenseMatch[1],
            expenseNameFragment: expenseMatch[2],
            triple,
            rawText: cell.text,
          });
        }
      }
    }
  }
  return { itemRows, expenseRows };
}

export function normalizeDocling(caseId) {
  const engine = 'docling';
  const raw = readJson(rawArtifactPath(caseId, engine));
  const { itemRows, expenseRows } = findRows(raw.tables);

  const singleItem = itemRows.length === 1 ? itemRows[0] : null;
  const singleExpense = expenseRows.length === 1 ? expenseRows[0] : null;

  const result = {
    itemCode: singleItem?.itemCode ?? null,
    itemName: singleItem?.itemNameFragment ?? null,
    requestNo: singleExpense?.requestNo ?? null,
    expenseCode: singleExpense?.expenseCode ?? null,
    expenseName: singleExpense?.expenseNameFragment ?? null,
    previousBudget: singleExpense?.triple?.previous?.magnitude ?? null,
    fy2024Request: singleExpense?.triple?.current?.magnitude ?? null,
    deltaRaw: singleExpense?.triple?.delta?.raw ?? null,
    delta: singleExpense?.triple ? singleExpense.triple.delta.signed : null,
    unit: raw.unit ?? null,
    page: raw.page,
  };

  const normalized = {
    schemaVersion: 1,
    caseId,
    engine: raw.engine,
    engineVersion: raw.engineVersion,
    sourceId: raw.sourceId,
    sourceSha256: raw.sourceSha256,
    rawArtifact: path.relative(process.cwd(), rawArtifactPath(caseId, engine)),
    ambiguity: {
      itemCandidateCount: itemRows.length,
      expenseCandidateCount: expenseRows.length,
      note: itemRows.length > 1 || expenseRows.length > 1
        ? 'Multiple structurally-matching table cells found; Docling\'s table structure did not by itself disambiguate item-code-shaped rows at different hierarchy levels (same limitation as the flat-text baselines). result reflects the unique match only when exactly one candidate was found for that field group.'
        : null,
    },
    candidates: { itemRows, expenseRows },
    result,
  };

  writeJson(normalizedArtifactPath(caseId, engine), normalized);
  return normalized;
}

// Standalone-execution convenience only (e.g. `node normalize-docling.mjs
// case-002`, for manually inspecting one engine's normalized output without
// running the full benchmark). This block must NOT fire merely because this
// module is imported -- run.mjs imports normalizeDocling and calls it
// explicitly at the correct point in its own pipeline (after the docling
// adapter has written its raw artifact). Since run.mjs is invoked as
// `node src/run.mjs <caseId>`, it shares the identical process.argv[2] this
// block reads; without the direct-execution guard below, importing this
// module reruns normalizeDocling as an import-time side effect, before the
// adapter has necessarily produced a raw artifact yet -- see
// protocol/DECISIONS.md for why this was treated as a harness-reliability
// defect (docbench harness reliability investigation), not a Docling/torch
// flakiness issue.
const isDirectlyExecuted = process.argv[1] && import.meta.url === new URL(process.argv[1], 'file://').href;
if (isDirectlyExecuted) {
  const [, , caseIdArg] = process.argv;
  if (caseIdArg) {
    const out = normalizeDocling(caseIdArg);
    console.log(`NORMALIZED docling/${caseIdArg} -> ${normalizedArtifactPath(caseIdArg, 'docling')}`);
    console.log(JSON.stringify(out.result, null, 2));
  }
}
