#!/usr/bin/env node
// Evaluator: compares a normalized engine result against ground truth.
//
// This is the ONLY step permitted to read ground-truth.json's `result` field.
// It never repairs or reinterprets engine output — a missing/incorrect field
// is scored as a failure and recorded verbatim, never silently corrected
// using the ground truth value (see protocol/RESEARCH_PROTOCOL.md:
// "never silently convert an unknown value into zero", applied here as
// "never silently convert an engine miss into a ground-truth-derived value").
import path from 'node:path';
import {
  readGroundTruth,
  readJson,
  writeJson,
  normalizedArtifactPath,
  DERIVED_DIR,
} from './common.mjs';

function check(id, actual, expected, note = '') {
  const pass = JSON.stringify(actual) === JSON.stringify(expected);
  return { id, pass, actual, expected, note };
}

export function evaluate(caseId, engine) {
  const gt = readGroundTruth(caseId);
  const normalized = readJson(normalizedArtifactPath(caseId, engine));
  const r = normalized.result;
  const expected = gt.result;

  const checks = [];

  checks.push(check('item_name_exact_match', r.itemName, expected.itemName,
    'Only passes if the harness resolved a single unambiguous item-code row; see item_name_present_among_candidates for a diagnostic on ambiguous pages.'));

  const itemRows = normalized.candidates.itemRows;
  const matchingItemCandidate = itemRows.find(ir => ir.itemCode === expected.itemCode && ir.itemNameFragment === expected.itemName);
  checks.push({
    id: 'item_name_present_among_candidates',
    pass: Boolean(matchingItemCandidate),
    actual: itemRows.map(ir => ({ itemCode: ir.itemCode, itemName: ir.itemNameFragment })),
    expected: { itemCode: expected.itemCode, itemName: expected.itemName },
    note: 'Diagnostic only: on a page with multiple item-code-shaped rows, this checks whether the correct row was extracted and reconstructed correctly at all, independent of whether the harness\'s single-match selection resolved it into `result`.',
  });
  checks.push(check('expense_name_exact_match_after_line_join', r.expenseName, expected.expenseName,
    'Deterministic line-join only (common.mjs joinWrappedLabel); no semantic repair.'));
  checks.push(check('previous_budget_exact_match', r.previousBudget, expected.previousBudget));
  checks.push(check('fy2024_request_exact_match', r.fy2024Request, expected.fy2024Request));
  checks.push(check('signed_delta_exact_match', r.delta, expected.delta,
    'FAIL here must mean the engine failed to preserve/associate the sign, not that we substituted the ground-truth sign.'));
  checks.push(check('unit_exact_match', r.unit, expected.unit));
  checks.push(check('page_identification', r.page, expected.page));

  const deltaRawHasGlyph = typeof r.deltaRaw === 'string' && r.deltaRaw.includes('△');
  checks.push({
    id: 'raw_delta_glyph_preserved',
    pass: deltaRawHasGlyph,
    actual: r.deltaRaw,
    expected: 'contains △',
    note: 'Checks the RAW extracted token, not the ground truth. A pass here means the engine itself retained the decrease glyph.',
  });

  const expenseRows = normalized.candidates.expenseRows;
  const matchedExpense = expenseRows.find(er => er.expenseCode === r.expenseCode) ?? expenseRows[0] ?? null;
  const precedingItemRow = matchedExpense
    ? itemRows.filter(ir => ir.order < matchedExpense.order).sort((a, b) => b.order - a.order)[0] ?? null
    : null;
  checks.push({
    id: 'item_to_amount_relationship',
    pass: Boolean(precedingItemRow && precedingItemRow.itemCode === expected.itemCode && r.previousBudget === expected.previousBudget),
    actual: { nearestPrecedingItemCode: precedingItemRow?.itemCode ?? null, resultPreviousBudget: r.previousBudget },
    expected: { itemCode: expected.itemCode, previousBudget: expected.previousBudget },
    note: 'The amount triple must belong to the expense row nested under the correct item-code row, not merely appear somewhere on the page.',
  });

  checks.push({
    id: 'expense_to_amount_relationship',
    pass: Boolean(matchedExpense && matchedExpense.triple),
    actual: matchedExpense ? { expenseCode: matchedExpense.expenseCode, hasTriple: Boolean(matchedExpense.triple) } : null,
    expected: { expenseCode: expected.expenseCode, hasTriple: true },
    note: 'The amount triple must be parsed from the same structural row as the expense code, not an adjacent/unrelated row.',
  });

  const summary = {
    total: checks.length,
    passed: checks.filter(c => c.pass).length,
    failed: checks.filter(c => !c.pass).length,
  };

  const result = {
    schemaVersion: 1,
    caseId,
    engine,
    engineVersion: normalized.engineVersion,
    evaluatedAt: new Date().toISOString(),
    summary,
    checks,
  };

  writeJson(path.join(DERIVED_DIR, caseId, `${engine}.evaluation.json`), result);
  return result;
}

const [, , caseIdArg, engineArg] = process.argv;
if (caseIdArg && engineArg) {
  const out = evaluate(caseIdArg, engineArg);
  console.log(`${caseIdArg}/${engineArg}: ${out.summary.passed}/${out.summary.total} checks passed`);
  for (const c of out.checks) {
    if (!c.pass) console.log(`  FAIL ${c.id}: actual=${JSON.stringify(c.actual)} expected=${JSON.stringify(c.expected)}`);
  }
}
