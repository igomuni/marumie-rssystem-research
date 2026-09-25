#!/usr/bin/env node
// Unit tests for the generic, case-blind row-parsing rules in common.mjs.
// These test the parser in isolation from any adapter or ground truth, using
// synthetic lines shaped like the real document's patterns.
import assert from 'node:assert/strict';
import {
  parseAmountToken,
  splitTrailingTriple,
  findItemCodeRows,
  findExpenseRows,
  joinWrappedLabel,
} from './common.mjs';

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
