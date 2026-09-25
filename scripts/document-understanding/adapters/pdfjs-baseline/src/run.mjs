#!/usr/bin/env node
// pdfjs-baseline adapter: reuses the already-locked, already-extracted output
// of scripts/pdf-extraction (pdfjs-dist) rather than re-parsing the PDF. This
// keeps the Document Understanding benchmark's first baseline isolated from
// (does not modify) the existing PDF.js extractor, while still exercising a
// real, independently-produced extraction engine.
import fs from 'node:fs';
import path from 'node:path';
import {
  ROOT,
  readGroundTruth,
  writeJson,
  rawArtifactPath,
} from '../../../benchmark/src/common.mjs';

const PDF_EXTRACTION_OUTPUT_DIR = path.join(ROOT, 'derived', 'pdf-extraction');

function findUnitLabel(lines) {
  for (const line of lines) {
    const m = line.text.match(/\(単位[:：]?\s*([^)]+)\)/);
    if (m) return m[1].trim();
  }
  return null;
}

export function run(caseId) {
  const gt = readGroundTruth(caseId);
  const manifestPath = path.join(PDF_EXTRACTION_OUTPUT_DIR, 'run-manifest.json');
  if (!fs.existsSync(manifestPath)) {
    throw new Error(
      `Missing ${manifestPath}. Run \`npm run extract\` (scripts/pdf-extraction) first ` +
      `so this baseline can reuse its already-locked, already-extracted output.`
    );
  }
  const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
  const sourceEntry = manifest.sources.find(s => s.sourceId === gt.sourceId);
  if (!sourceEntry) throw new Error(`No pdf-extraction manifest entry for ${gt.sourceId}`);
  if (sourceEntry.sourceSha256 !== gt.sourceSha256) {
    throw new Error(
      `Source hash mismatch: pdf-extraction manifest has ${sourceEntry.sourceSha256}, ` +
      `case ${caseId} expects ${gt.sourceSha256}`
    );
  }

  const linesPath = path.join(PDF_EXTRACTION_OUTPUT_DIR, `${gt.sourceId}.lines.jsonl`);
  const allLines = fs.readFileSync(linesPath, 'utf8').split(/\r?\n/).filter(Boolean).map(JSON.parse);
  const pageLines = allLines
    .filter(l => l.pdfPageIndex === gt.pdfPageIndex)
    .sort((a, b) => a.lineIndex - b.lineIndex)
    .map(l => ({ lineIndex: l.lineIndex, text: l.text, y: l.baselineY }));

  const raw = {
    schemaVersion: 1,
    caseId,
    engine: 'pdfjs-dist',
    engineVersion: sourceEntry.extractorVersion,
    orderingVersion: sourceEntry.orderingVersion,
    sourceId: gt.sourceId,
    sourceSha256: gt.sourceSha256,
    page: gt.pdfPageIndex,
    unit: findUnitLabel(pageLines),
    lines: pageLines,
    provenance: {
      reusedFrom: path.relative(ROOT, linesPath),
      note: 'This baseline does not re-run PDF.js; it reuses the deterministic line reconstruction already produced and hash-verified by scripts/pdf-extraction.',
    },
  };

  writeJson(rawArtifactPath(caseId, 'pdfjs-baseline'), raw);
  return raw;
}

const [, , caseIdArg] = process.argv;
if (caseIdArg) {
  const raw = run(caseIdArg);
  console.log(`RAW pdfjs-baseline/${caseIdArg}: page=${raw.page} lines=${raw.lines.length} unit=${raw.unit}`);
}
