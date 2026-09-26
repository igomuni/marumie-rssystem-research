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
  closeCjkWrapSpaces,
} from './common.mjs';

function reconstructRow(row, nameField, lines) {
  const { joinedSuffix, consumedLineIndexes } = joinWrappedLabel(lines, row.lineIndex);
  const fragment = row[nameField];
  const assembled = joinedSuffix ? `${fragment}${joinedSuffix}` : fragment;
  return {
    ...row,
    // See common.mjs's closeCjkWrapSpaces: pdfjs-dist's line reconstruction
    // has been observed inserting a space between adjacent CJK characters
    // specifically for header/total-style rows rendered with wide letter-
    // spacing in the source (case-002, case-003); PyMuPDF's own
    // reconstruction never does this, so applying the rule here is a no-op
    // for its already-clean text. Applied to the fully-assembled name
    // (after any wrap-join) so both single-line and wrapped labels are
    // covered uniformly, matching normalize-docling.mjs's own scope.
    [nameField]: closeCjkWrapSpaces(assembled),
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

// Standalone-execution convenience only (e.g. `node normalize.mjs case-002
// pdfjs-baseline`). Guarded the same way as normalize-docling.mjs's
// equivalent block (see there for why this matters): this module must not
// re-run normalize() as an import-time side effect merely because run.mjs
// imports it. This block currently requires two argv positions
// (caseId + engine), which already does not collide with run.mjs's own
// single-argument invocation (`node src/run.mjs <caseId>`) -- the explicit
// guard is added anyway for defense-in-depth and consistency with
// normalize-docling.mjs, so this safety property does not silently depend on
// run.mjs's argv shape never changing.
const isDirectlyExecuted = process.argv[1] && import.meta.url === new URL(process.argv[1], 'file://').href;
if (isDirectlyExecuted) {
  const [, , caseIdArg, engineArg] = process.argv;
  if (caseIdArg && engineArg) {
    const out = normalize(caseIdArg, engineArg);
    console.log(`NORMALIZED ${caseIdArg}/${engineArg} -> ${normalizedArtifactPath(caseIdArg, engineArg)}`);
    console.log(JSON.stringify(out.result, null, 2));
  }
}
