#!/usr/bin/env node
// Unit tests for the generic, case-blind row-parsing rules in common.mjs.
// These test the parser in isolation from any adapter or ground truth, using
// synthetic lines shaped like the real document's patterns.
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import {
  parseAmountToken,
  splitTrailingTriple,
  findItemCodeRows,
  findExpenseRows,
  joinWrappedLabel,
} from './common.mjs';
import {
  closeCjkWrapSpaces,
  reconstructNumericToken,
  findRows,
} from './normalize-docling.mjs';
import { deltaSignEvidenceMatches } from './evaluate.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

function t(name, fn) {
  try {
    fn();
    console.log(`PASS ${name}`);
  } catch (err) {
    console.error(`FAIL ${name}`);
    console.error(err);
    process.exitCode = 1;
  }
}

t('parseAmountToken: plain magnitude', () => {
  const r = parseAmountToken('481,188,232');
  assert.equal(r.magnitude, 481188232);
  assert.equal(r.isDelta, false);
  assert.equal(r.signed, 481188232);
});

t('parseAmountToken: delta glyph flips sign', () => {
  const r = parseAmountToken('△ 32,920,906');
  assert.equal(r.magnitude, 32920906);
  assert.equal(r.isDelta, true);
  assert.equal(r.signed, -32920906);
});

t('parseAmountToken: missing digits returns null', () => {
  assert.equal(parseAmountToken('not-a-number'), null);
});

t('splitTrailingTriple: tolerates wide padding (PyMuPDF-style columns)', () => {
  const r = splitTrailingTriple('情報通信技術調達等適正                481,188,232     448,267,326                         △     32,920,906');
  assert.equal(r.label, '情報通信技術調達等適正');
  assert.equal(r.previous.magnitude, 481188232);
  assert.equal(r.current.magnitude, 448267326);
  assert.equal(r.delta.signed, -32920906);
});

t('splitTrailingTriple: no delta glyph is not silently signed negative', () => {
  const r = splitTrailingTriple('001 財務省システム 108,761,287 102,935,743 5,825,544');
  assert.equal(r.delta.isDelta, false);
  assert.equal(r.delta.signed, 5825544, 'a missing glyph must never be inferred as negative from context');
});

t('findItemCodeRows: matches 3-digit-code + name rows', () => {
  const lines = [
    { lineIndex: 0, text: '020 情報通信技術調達等適正' },
    { lineIndex: 1, text: '・効率化推進費' },
    { lineIndex: 2, text: 'not a code row' },
  ];
  const rows = findItemCodeRows(lines);
  assert.equal(rows.length, 1);
  assert.equal(rows[0].itemCode, '020');
});

t('findExpenseRows: matches reqNo + expenseCode + trailing triple', () => {
  const lines = [
    { lineIndex: 0, text: '4 01-95 情報通信技術調達等適正 481,188,232 448,267,326 △ 32,920,906' },
  ];
  const rows = findExpenseRows(lines);
  assert.equal(rows.length, 1);
  assert.equal(rows[0].requestNo, '4');
  assert.equal(rows[0].expenseCode, '01-95');
  assert.equal(rows[0].triple.delta.signed, -32920906);
});

t('joinWrappedLabel: joins exactly one continuation line by default', () => {
  const lines = [
    { lineIndex: 0, text: '020 情報通信技術調達等適正' },
    { lineIndex: 1, text: '・効率化推進費' },
    { lineIndex: 2, text: '041 デジタル推進委員等環境' },
  ];
  const { joinedSuffix, consumedLineIndexes } = joinWrappedLabel(lines, 0);
  assert.equal(joinedSuffix, '・効率化推進費');
  assert.deepEqual(consumedLineIndexes, [1]);
});

t('joinWrappedLabel: stops at a line that is itself a structural row', () => {
  const lines = [
    { lineIndex: 0, text: '046 デジタル臨時行政調査会' },
    { lineIndex: 1, text: '041 デジタル推進委員等環境' }, // looks like another item-code row, must not be swallowed
  ];
  const { joinedSuffix } = joinWrappedLabel(lines, 0);
  assert.equal(joinedSuffix, '', 'must not join a line that matches the item-code pattern itself');
});

// --- normalize-docling.mjs -------------------------------------------
// These use synthetic table-cell data with DIFFERENT numbers than any real
// case's ground truth, specifically to demonstrate the logic is general
// (engine-behavior-driven) rather than fitted to a known expected answer.

t('closeCjkWrapSpaces: removes a wrap-induced space between two CJK characters', () => {
  assert.equal(closeCjkWrapSpaces('情報通信技術調達等適正 ・効率化推進費'), '情報通信技術調達等適正・効率化推進費');
});

t('closeCjkWrapSpaces: leaves the space between an item code and its CJK name', () => {
  assert.equal(closeCjkWrapSpaces('020 情報通信技術調達等適正'), '020 情報通信技術調達等適正');
});

t('reconstructNumericToken: reverses Docling-style reversed comma-groups', () => {
  const r = reconstructNumericToken('999 111, 555,');
  assert.equal(r.magnitude, 555111999);
  assert.equal(r.isDelta, false);
});

t('reconstructNumericToken: already-correct single-token cell is unaffected', () => {
  const r = reconstructNumericToken('777');
  assert.equal(r.magnitude, 777);
});

t('reconstructNumericToken: a glyph-only cell is reported distinctly, not as a magnitude of 0', () => {
  const r = reconstructNumericToken('△');
  assert.equal(r.deltaGlyphOnly, true);
});

t('reconstructNumericToken: non-numeric cell text returns null (not force-parsed)', () => {
  assert.equal(reconstructNumericToken('（要求要旨）'), null);
});

t('findRows: sign comes only from an actually-observed separate glyph cell, never inferred', () => {
  const cells = [
    { row: 0, col: 1, text: '030 テスト項目名' },
    { row: 1, col: 1, text: '02-99 テスト費目名' },
    { row: 1, col: 3, text: '111 222,' },   // previous: reversed -> 222,111
    { row: 1, col: 4, text: '333 444,' },   // current: reversed -> 444,333
    { row: 1, col: 6, text: '△' },          // sign cell, observed separately
    { row: 1, col: 7, text: '999 555,' },   // delta magnitude: reversed -> 555,999
  ];
  const { itemRows, expenseRows } = findRows([{ tableIndex: 0, cells }]);
  assert.equal(itemRows.length, 1);
  assert.equal(itemRows[0].itemCode, '030');
  assert.equal(expenseRows.length, 1);
  const e = expenseRows[0];
  assert.equal(e.expenseCode, '02-99');
  assert.equal(e.triple.previous.magnitude, 222111);
  assert.equal(e.triple.current.magnitude, 444333);
  assert.equal(e.triple.delta.magnitude, 555999);
  assert.equal(e.triple.delta.isDelta, true);
  assert.equal(e.triple.delta.signed, -555999);
  assert.ok(itemRows[0].order < expenseRows[0].order, 'item row must be ordered before the expense row nested under it');
});

t('findRows: a triple with no glyph cell anywhere is never signed negative', () => {
  const cells = [
    { row: 0, col: 1, text: '02-99 テスト費目名' },
    { row: 0, col: 3, text: '111,222' },
    { row: 0, col: 4, text: '333,444' },
    { row: 0, col: 7, text: '55,999' },
  ];
  const { expenseRows } = findRows([{ tableIndex: 0, cells }]);
  assert.equal(expenseRows[0].triple.delta.isDelta, false);
  assert.equal(expenseRows[0].triple.delta.signed, 55999, 'no glyph observed anywhere in the row means positive, never guessed negative');
});

t('findRows: missing request-number cell is recorded as null, not guessed', () => {
  const cells = [
    { row: 0, col: 1, text: '02-99 テスト費目名' },
    { row: 0, col: 3, text: '111,222' },
    { row: 0, col: 4, text: '333,444' },
    { row: 0, col: 7, text: '55,999' },
  ];
  const { expenseRows } = findRows([{ tableIndex: 0, cells }]);
  assert.equal(expenseRows[0].requestNo, null);
});

t('findRows: a present request-number cell to the left is used', () => {
  const cells = [
    { row: 0, col: 0, text: '7' },
    { row: 0, col: 1, text: '02-99 テスト費目名' },
  ];
  const { expenseRows } = findRows([{ tableIndex: 0, cells }]);
  assert.equal(expenseRows[0].requestNo, '7');
});

// --- evaluate.mjs: deltaSignEvidenceMatches ----------------------------
// Covers the delta_sign_evidence_matches_source check's core logic in
// isolation, for both directions Ground Truth can express (decrease-glyph
// case-001-style, no-glyph case-002-style), plus the provenance invariant
// that a glyph must come from the engine's own output, never be inferred
// from Ground Truth or from arithmetic.

t('deltaSignEvidenceMatches: glyph expected + glyph observed -> PASS', () => {
  assert.equal(deltaSignEvidenceMatches('△32,920,906', '△ 32,920,906'), true);
});

t('deltaSignEvidenceMatches: glyph expected + no glyph observed -> FAIL', () => {
  assert.equal(deltaSignEvidenceMatches('△32,920,906', '32,920,906'), false);
});

t('deltaSignEvidenceMatches: glyph expected + nothing observed (null) -> FAIL', () => {
  assert.equal(deltaSignEvidenceMatches('△32,920,906', null), false);
});

t('deltaSignEvidenceMatches: no glyph expected + no glyph observed -> PASS', () => {
  assert.equal(deltaSignEvidenceMatches('4,556,824', '4,556,824'), true);
});

t('deltaSignEvidenceMatches: no glyph expected + glyph incorrectly fabricated -> FAIL', () => {
  assert.equal(deltaSignEvidenceMatches('4,556,824', '△4,556,824'), false,
    'a fabricated glyph must fail even though the magnitude would otherwise match');
});

t('deltaSignEvidenceMatches: no glyph expected + nothing observed (null) -> PASS', () => {
  // A null deltaRaw means the engine extracted nothing at all — that is a
  // real miss, already scored by signed_delta_exact_match /
  // previous_budget_exact_match / fy2024_request_exact_match. This check is
  // narrowly about glyph-fabrication avoidance: no glyph was expected, and
  // none was invented, so it PASSes here even though overall extraction
  // failed. It is not, by itself, evidence of successful delta recovery.
  assert.equal(deltaSignEvidenceMatches('4,556,824', null), true);
});

t('deltaSignEvidenceMatches: expected glyph state comes from deltaRaw, not from case-001 assumptions baked into the function', () => {
  // Symmetry check: swapping which side has the glyph swaps the answer,
  // confirming the function has no hardcoded "glyph must be present" bias.
  assert.equal(deltaSignEvidenceMatches('100', '100'), true);
  assert.equal(deltaSignEvidenceMatches('△100', '△100'), true);
  assert.equal(deltaSignEvidenceMatches('100', '△100'), false);
  assert.equal(deltaSignEvidenceMatches('△100', '100'), false);
});

// Regression tests for the docbench harness-reliability investigation:
// normalize-docling.mjs (and normalize.mjs) each have a standalone-execution
// convenience block at module scope (`node normalize-docling.mjs <caseId>`).
// That block must run ONLY on direct execution, never as a side effect of
// being imported -- run.mjs imports both modules and is itself invoked as
// `node src/run.mjs <caseId>`, sharing the identical process.argv[2]. Before
// the fix, importing normalize-docling.mjs under that argv shape re-ran
// normalizeDocling() at import time, before any adapter had necessarily
// written a raw artifact yet, throwing ENOENT for any case whose raw
// artifact didn't already happen to exist from an earlier run -- this is
// what run.mjs's own crash traced back to, not a Docling/Torch/child-process
// reliability problem. These tests spawn a fresh `node` process (module
// top-level side effects can only be observed on first evaluation, and the
// module is already cached by this test file's own static imports above) and
// assert that importing the module with a run.mjs-shaped argv, for a case
// with no raw artifact on disk, does not throw.
const NORMALIZE_DOCLING_PATH = path.join(__dirname, 'normalize-docling.mjs');
const NORMALIZE_PATH = path.join(__dirname, 'normalize.mjs');

function importDoesNotThrow(modulePath, argv) {
  const script = `
    process.argv = ${JSON.stringify(['node', 'run.mjs', ...argv])};
    import(${JSON.stringify('file://' + modulePath)})
      .then(() => { console.log('IMPORT_OK'); })
      .catch((e) => { console.error('IMPORT_THREW: ' + e.message); process.exitCode = 1; });
  `;
  try {
    const out = execFileSync(process.execPath, ['-e', script], { encoding: 'utf8' });
    return { threw: false, output: out };
  } catch (err) {
    return { threw: true, output: (err.stdout || '') + (err.stderr || '') };
  }
}

t('normalize-docling.mjs: importing with a run.mjs-shaped argv for a nonexistent case does not throw', () => {
  const result = importDoesNotThrow(NORMALIZE_DOCLING_PATH, ['case-does-not-exist-xyz']);
  assert.equal(result.threw, false, `import should not throw; output: ${result.output}`);
  assert.match(result.output, /IMPORT_OK/);
});

t('normalize.mjs: importing with a run.mjs-shaped argv (single caseId arg only) does not throw', () => {
  const result = importDoesNotThrow(NORMALIZE_PATH, ['case-does-not-exist-xyz']);
  assert.equal(result.threw, false, `import should not throw; output: ${result.output}`);
  assert.match(result.output, /IMPORT_OK/);
});
