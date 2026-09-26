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

const DELTA_GLYPH = '△';
function hasDeltaGlyph(value) {
  return typeof value === 'string' && value.includes(DELTA_GLYPH);
}

// Pure, unit-testable core of the `delta_sign_evidence_matches_source` check.
// Exported so tests can exercise both directions (glyph-expected and
// no-glyph-expected) without needing to construct on-disk ground-truth /
// normalized-artifact fixtures for the full evaluate() pipeline.
//
// The expected glyph state is derived from `expectedDeltaRaw` — Ground
// Truth's own raw/visual field — never from the sign of a normalized numeric
// `delta`, so this never infers "the source expects a glyph" from an
// unrelated derived value. `actualDeltaRaw` must come from the engine's own
// (ground-truth-blind) normalized output; a glyph is only ever counted as
// "observed" if it is genuinely present there.
export function deltaSignEvidenceMatches(expectedDeltaRaw, actualDeltaRaw) {
  const expectedHasGlyph = hasDeltaGlyph(expectedDeltaRaw);
  const actualHasGlyph = hasDeltaGlyph(actualDeltaRaw);
  return expectedHasGlyph ? actualHasGlyph : !actualHasGlyph;
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

  // The expected glyph state is derived from Ground Truth's own `deltaRaw` —
  // the most direct source-derived raw/visual evidence available — never from
  // the sign of `expected.delta` (that would be inferring source condition
  // from a normalized/derived numeric value rather than the raw observation
  // that produced it). Both of this repository's current cases (case-001:
  // deltaRaw contains △; case-002: deltaRaw does not) express this
  // unambiguously; there is currently no "unknown/unreadable glyph state" in
  // any frozen Ground Truth (the Ground Truth creation process — see
  // fixtures/document-understanding/case-002/20260926_0908_Case002_Ground_Truth_Evidence.md
  // — never freezes an ambiguous value in the first place), so this check
  // does not yet need a third UNKNOWN outcome. If a future case's Ground
  // Truth ever needs to express that, this check must be revisited rather
  // than silently treating that unknown as "no glyph".
  // `deltaSignEvidenceMatches` computes `actualHasGlyph` purely from the
  // engine/normalizer's own `deltaRaw` — never from Ground Truth — preserving
  // the existing provenance invariant: a △ counted as "observed" must
  // originate from engine raw output / deterministic association, never be
  // conjured from expected values.
  const expectedHasGlyph = hasDeltaGlyph(expected.deltaRaw);
  checks.push({
    id: 'delta_sign_evidence_matches_source',
    pass: deltaSignEvidenceMatches(expected.deltaRaw, r.deltaRaw),
    actual: r.deltaRaw,
    expected: expectedHasGlyph
      ? 'contains △ (source-derived Ground Truth deltaRaw carries the decrease glyph)'
      : 'does not contain △ (source-derived Ground Truth deltaRaw carries no decrease glyph)',
    note: 'Checks whether the ground-truth-blind normalizer output\'s observed sign evidence agrees with the source-derived Ground Truth\'s own deltaRaw glyph state — in either direction, not only "glyph present". This check is narrowly about glyph-fabrication avoidance, not overall delta-extraction completeness (see signed_delta_exact_match / previous_budget_exact_match / fy2024_request_exact_match for that): when Ground Truth expects no glyph, a null deltaRaw (nothing extracted, nothing fabricated) also PASSes this specific check, because no false decrease indicator was introduced — it is not evidence that the engine successfully recovered the delta value. A PASS when a glyph IS expected still requires the glyph to be genuinely present in the engine\'s own raw output and associated with this delta value by the deterministic normalizer, exactly as before. For a flat-line engine (pdfjs-baseline, pymupdf-baseline), a present deltaRaw is a single literal raw-line substring. For a table-cell engine (docling), a present deltaRaw may instead be a normalizer-constructed concatenation of two separate raw cells (a glyph-only cell and a magnitude cell) that the same table row placed together — still traceable to genuine raw engine output, never to the ground truth, but not necessarily one literal raw token.',
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
