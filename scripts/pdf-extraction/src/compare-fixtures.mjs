#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import {
  ROOT,
  OUTPUT_DIR,
  FIXTURE_DIR,
  normalizeText,
  compactText,
  compactTextIgnoringDeltaGlyph,
  budgetCode,
  numericTokens,
  parseHistoricalFixture,
  readJsonl,
  stableJson,
} from './common.mjs';

const cases = [
  {
    sourceId: 'digital-r6-request-table-01',
    fixture: path.join(FIXTURE_DIR, 'digital_r6_normal_extract.txt'),
  },
  {
    sourceId: 'digital-r6-important-policy',
    fixture: path.join(FIXTURE_DIR, 'digital_r6_policy_extract.txt'),
  },
];

function sameStructuredRow(expected, candidate) {
  const expectedCode = budgetCode(expected);
  if (!expectedCode || budgetCode(candidate) !== expectedCode) return false;
  const stripCode = (text, code) => String(text).replace(code, '');
  const eNums = numericTokens(stripCode(expected, expectedCode));
  const cNums = numericTokens(stripCode(candidate, expectedCode));
  if (eNums.length < 3 || cNums.length < 3) return false;
  return eNums.slice(0, 3).join('|') === cNums.slice(0, 3).join('|');
}

function windows(lines, maxSize = 5) {
  const out = [];
  for (let start = 0; start < lines.length; start++) {
    for (let size = 1; size <= maxSize && start + size <= lines.length; size++) {
      const group = lines.slice(start, start + size);
      out.push({
        start,
        size,
        lines: group,
        text: group.map(x => x.text).join(' '),
      });
    }
  }
  return out;
}

function chooseOrdered(matches, minLineIndex) {
  const eligible = matches.filter(x => {
    const start = x.lineIndex ?? x.lines?.[0]?.lineIndex ?? -1;
    return start > minLineIndex;
  });
  if (!eligible.length) return null;
  eligible.sort((a, b) => {
    const ai = a.lineIndex ?? a.lines?.[0]?.lineIndex ?? -1;
    const bi = b.lineIndex ?? b.lines?.[0]?.lineIndex ?? -1;
    return ai - bi;
  });
  return { chosen: eligible[0], eligibleCount: eligible.length };
}

function classify(expected, pageLines, minLineIndex = -1) {
  const normExpected = normalizeText(expected);
  const compactExpected = compactText(expected);

  const compactExpectedNoDelta = compactTextIgnoringDeltaGlyph(expected);

  const methods = [
    ['exact', pageLines.filter(x => x.text === expected)],
    ['normalized_match', pageLines.filter(x => normalizeText(x.text) === normExpected)],
    ['curated_prefix', pageLines.filter(x => normalizeText(x.text).startsWith(normExpected))],
    ['structured_row_match', pageLines.filter(x => sameStructuredRow(expected, x.text))],
  ];

  for (const [matchMethod, matches] of methods) {
    const ordered = chooseOrdered(matches, minLineIndex);
    if (ordered) {
      return {
        matchMethod,
        candidates: [ordered.chosen],
        orderedCandidateCount: ordered.eligibleCount,
      };
    }
  }

  const ws = windows(pageLines, 5);
  const windowMethods = [
    ['contiguous_reconstruction', ws.filter(w => compactText(w.text) === compactExpected)],
    ['contiguous_delta_glyph_normalized', ws.filter(w => compactTextIgnoringDeltaGlyph(w.text) === compactExpectedNoDelta)],
    ['contiguous_curated_prefix', ws.filter(w => compactText(w.text).startsWith(compactExpected))],
    ['contiguous_structured_row_match', ws.filter(w => sameStructuredRow(expected, w.text))],
  ];
  for (const [matchMethod, matches] of windowMethods) {
    const ordered = chooseOrdered(matches, minLineIndex);
    if (ordered) {
      return {
        matchMethod,
        windows: [ordered.chosen],
        orderedCandidateCount: ordered.eligibleCount,
      };
    }
  }

  return { matchMethod: 'not_found' };
}

const output = {
  schemaVersion: 1,
  comparisonVersion: 'v1',
  note: 'Historical fixture P values are compared as zero-based PDF page indexes; legacy L values are retained as metadata only.',
  sources: [],
};

for (const c of cases) {
  const fixtureRows = parseHistoricalFixture(c.fixture);
  const lineFile = path.join(OUTPUT_DIR, `${c.sourceId}.lines.jsonl`);
  if (!fs.existsSync(lineFile)) throw new Error(`Missing extraction output: ${lineFile}; run npm run extract first.`);
  const lines = readJsonl(lineFile);
  const byPage = new Map();
  for (const line of lines) {
    if (!byPage.has(line.pdfPageIndex)) byPage.set(line.pdfPageIndex, []);
    byPage.get(line.pdfPageIndex).push(line);
  }
  for (const pageLines of byPage.values()) {
    pageLines.sort((a, b) => a.lineIndex - b.lineIndex);
  }

  const observations = [];
  const lastMatchedLineByPage = new Map();
  for (const row of fixtureRows) {
    const pageLines = byPage.get(row.legacyPageIndex) ?? [];
    const minLineIndex = lastMatchedLineByPage.get(row.legacyPageIndex) ?? -1;
    const match = classify(row.text, pageLines, minLineIndex);
    const candidates = match.candidates ?? [];
    const ws = match.windows ?? [];
    const matchedStart = candidates[0]?.lineIndex ?? ws[0]?.lines?.[0]?.lineIndex ?? null;
    const matchedEnd = candidates[0]?.lineIndex ?? ws[0]?.lines?.at(-1)?.lineIndex ?? null;
    if (matchedEnd !== null) lastMatchedLineByPage.set(row.legacyPageIndex, matchedEnd);
    observations.push({
      sourceId: c.sourceId,
      legacySourceLine: row.legacySourceLine,
      expectedPageIndex: row.legacyPageIndex,
      historicalFixtureText: row.text,
      matchMethod: match.matchMethod,
      candidateCount: match.orderedCandidateCount ?? (candidates.length || ws.length),
      matchedExtractedText: candidates[0]?.text ?? ws[0]?.text ?? null,
      matchedPdfPageIndex: candidates[0]?.pdfPageIndex ?? ws[0]?.lines?.[0]?.pdfPageIndex ?? null,
      matchedLineIndexes: candidates.length
        ? candidates.map(x => x.lineIndex)
        : ws[0]?.lines?.map(x => x.lineIndex) ?? [],
    });
  }

  const stats = observations.reduce((acc, x) => {
    acc.total += 1;
    acc[x.matchMethod] = (acc[x.matchMethod] ?? 0) + 1;
    return acc;
  }, { total: 0 });

  output.sources.push({
    sourceId: c.sourceId,
    fixture: path.relative(ROOT, c.fixture),
    stats,
    observations,
  });
}

const evidencePath = path.join(ROOT, 'evidence', 'pdf-extraction-fixture-comparison.json');
fs.mkdirSync(path.dirname(evidencePath), { recursive: true });
fs.writeFileSync(evidencePath, stableJson(output), 'utf8');

for (const s of output.sources) {
  console.log(`${s.sourceId}: ${JSON.stringify(s.stats)}`);
}
console.log(`WROTE ${path.relative(ROOT, evidencePath)}`);
