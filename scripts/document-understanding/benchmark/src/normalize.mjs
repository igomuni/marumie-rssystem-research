#!/usr/bin/env node
// Deterministic normalizer: raw engine artifact -> benchmark result schema.
//
// This step is intentionally blind to ground truth *values*. It only reads
// the case's `pdfPageIndex` (which page to look at — case configuration, not
// an answer) from fixtures/document-understanding/<caseId>/ground-truth.json,
// never the nested `result` object. All row detection uses the generic
// parsing rules in common.mjs, which know nothing about this specific case's
// expected numbers or names.
import path from 'node:path';
import {
  readJson,
  writeJson,
  rawArtifactPath,
  normalizedArtifactPath,
  findItemCodeRows,
  findExpenseRows,
  joinWrappedLabel,
} from './common.mjs';

function reconstructRow(row, nameField, lines) {
  const { joinedSuffix, consumedLineIndexes } = joinWrappedLabel(lines, row.lineIndex);
  const fragment = row[nameField];
  return {
    ...row,
    [nameField]: joinedSuffix ? `${fragment}${joinedSuffix}` : fragment,
    joinedFromLineIndexes: [row.lineIndex, ...consumedLineIndexes],
    // Engine-agnostic reading-order key so evaluate.mjs can compare "which
    // row precedes which" across normalizers with different native row
    // shapes (this one keyed by lineIndex; the Docling table-cell normalizer
    // keyed by table row index) without needing to know which engine produced
    // either candidate.
    order: row.lineIndex,
  };
}

export function normalize(caseId, engine) {
  const raw = readJson(rawArtifactPath(caseId, engine));
  const lines = raw.lines;

  const itemRows = findItemCodeRows(lines).map(r => reconstructRow(r, 'itemNameFragment', lines));
  const expenseRows = findExpenseRows(lines).map(r => reconstructRow(r, 'expenseNameFragment', lines));

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
        ? 'Multiple structurally-matching rows found on this page; disambiguation beyond a single-page, single-match assumption is out of scope for this benchmark pass. result reflects the unique match only when exactly one candidate was found for that field group.'
        : null,
    },
    candidates: { itemRows, expenseRows },
    result,
  };

  writeJson(normalizedArtifactPath(caseId, engine), normalized);
  return normalized;
}

const [, , caseIdArg, engineArg] = process.argv;
if (caseIdArg && engineArg) {
  const out = normalize(caseIdArg, engineArg);
  console.log(`NORMALIZED ${caseIdArg}/${engineArg} -> ${normalizedArtifactPath(caseIdArg, engineArg)}`);
  console.log(JSON.stringify(out.result, null, 2));
}
