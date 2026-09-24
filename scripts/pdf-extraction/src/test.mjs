#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import {
  ROOT,
  OUTPUT_DIR,
  readJsonl,
  readLock,
  verifyLockedRaw,
  sha256,
  compactText,
} from './common.mjs';

const expected = {
  'digital-r6-request-table-01': {
    pageCount: 32,
    assertions: [
      { pageIndex: 22, contains: '財務省システム' },
      { pageIndex: 24, contains: '厚生労働第1係', alternate: '厚生労働第１係' },
      { pageIndex: 24, contains: '総務省システム' },
      { pageIndex: 25, contains: '7,738,305' },
    ],
  },
  'digital-r6-important-policy': {
    pageCount: 1,
    assertions: [
      { pageIndex: 0, contains: 'デジタル庁システム等' },
      { pageIndex: 0, contains: '17,245,103' },
      { pageIndex: 0, contains: '51,024,815' },
      { pageIndex: 0, contains: '50,502,710' },
    ],
  },
};

for (const source of readLock().sources) {
  if (!(source.sourceId in expected)) continue;
  verifyLockedRaw(source);
}

const manifestPath = path.join(OUTPUT_DIR, 'run-manifest.json');
if (!fs.existsSync(manifestPath)) throw new Error('No extraction run-manifest.json; run npm run extract first.');
const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));

for (const [sourceId, exp] of Object.entries(expected)) {
  const m = manifest.sources.find(x => x.sourceId === sourceId);
  if (!m) throw new Error(`No extraction manifest entry for ${sourceId}`);
  if (m.pageCount !== exp.pageCount) {
    throw new Error(`${sourceId}: expected ${exp.pageCount} pages, got ${m.pageCount}`);
  }
  const lineFile = path.join(OUTPUT_DIR, `${sourceId}.lines.jsonl`);
  const lines = readJsonl(lineFile);
  for (const assertion of exp.assertions) {
    const pageText = compactText(
      lines
        .filter(x => x.pdfPageIndex === assertion.pageIndex)
        .map(x => x.text)
        .join('\n')
    );
    const targets = [assertion.contains, assertion.alternate].filter(Boolean).map(compactText);
    if (!targets.some(t => pageText.includes(t))) {
      throw new Error(`${sourceId}: pageIndex ${assertion.pageIndex} missing expected text: ${targets.join(' OR ')}`);
    }
  }
}

for (const m of manifest.sources) {
  const paths = {
    itemsJsonlSha256: path.join(ROOT, m.outputs.itemsJsonl),
    linesJsonlSha256: path.join(ROOT, m.outputs.linesJsonl),
    pagesTxtSha256: path.join(ROOT, m.outputs.pagesTxt),
  };
  for (const [field, p] of Object.entries(paths)) {
    const actual = sha256(fs.readFileSync(p));
    if (actual !== m.outputHashes[field]) {
      throw new Error(`${m.sourceId}: output hash mismatch for ${field}`);
    }
  }
}

console.log('pdf extraction assertions PASS');
