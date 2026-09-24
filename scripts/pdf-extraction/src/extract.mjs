#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import * as pdfjs from 'pdfjs-dist/legacy/build/pdf.mjs';
import {
  ROOT,
  OUTPUT_DIR,
  ensureDir,
  readLock,
  verifyLockedRaw,
  sha256,
  stableJson,
  writeJsonl,
} from './common.mjs';

const require = createRequire(import.meta.url);
const pdfjsPackagePath = require.resolve('pdfjs-dist/package.json');
const pdfjsPackage = JSON.parse(fs.readFileSync(pdfjsPackagePath, 'utf8'));
const standardFontDataUrl = path.join(path.dirname(pdfjsPackagePath), 'standard_fonts') + path.sep;
const cMapUrl = path.join(path.dirname(pdfjsPackagePath), 'cmaps') + path.sep;

function median(values) {
  if (!values.length) return 0;
  const xs = [...values].sort((a, b) => a - b);
  const mid = Math.floor(xs.length / 2);
  return xs.length % 2 ? xs[mid] : (xs[mid - 1] + xs[mid]) / 2;
}

function lineJoin(items) {
  const sorted = [...items].sort((a, b) => a.x - b.x || a.itemIndex - b.itemIndex);
  let out = '';
  for (let i = 0; i < sorted.length; i++) {
    const cur = sorted[i];
    if (!cur.text) continue;
    if (!out) {
      out = cur.text;
      continue;
    }
    const prev = sorted[i - 1];
    const prevRight = prev.x + prev.width;
    const gap = cur.x - prevRight;
    const h = Math.max(1, Math.min(prev.height || 1, cur.height || 1));
    out += gap > h * 0.35 ? ` ${cur.text}` : cur.text;
  }
  return out.replace(/\s+/g, ' ').trim();
}

function reconstructLines(rawItems) {
  const items = rawItems.filter(x => x.text.trim().length > 0);
  const typicalHeight = median(items.map(x => x.height).filter(x => Number.isFinite(x) && x > 0)) || 10;
  const yTolerance = Math.max(0.75, typicalHeight * 0.35);

  const sorted = [...items].sort((a, b) =>
    b.y - a.y || a.x - b.x || a.itemIndex - b.itemIndex
  );

  const groups = [];
  for (const item of sorted) {
    let group = groups.at(-1);
    if (!group || Math.abs(group.baselineY - item.y) > yTolerance) {
      group = { baselineY: item.y, items: [] };
      groups.push(group);
    }
    group.items.push(item);
    group.baselineY = group.items.reduce((sum, x) => sum + x.y, 0) / group.items.length;
  }

  return groups
    .map((g, idx) => ({
      lineIndex: idx,
      baselineY: Number(g.baselineY.toFixed(4)),
      text: lineJoin(g.items),
      itemIndexes: g.items.map(x => x.itemIndex).sort((a, b) => a - b),
    }))
    .filter(x => x.text.length > 0);
}

async function extractSource(source) {
  const { data } = verifyLockedRaw(source);
  const loadingTask = pdfjs.getDocument({
    data: new Uint8Array(data),
    standardFontDataUrl,
    cMapUrl,
    cMapPacked: true,
    disableWorker: true,
  });
  const doc = await loadingTask.promise;
  const allItems = [];
  const allLines = [];
  const pageText = [];

  for (let pageNumber = 1; pageNumber <= doc.numPages; pageNumber++) {
    const pageIndex = pageNumber - 1;
    const page = await doc.getPage(pageNumber);
    const tc = await page.getTextContent({ disableNormalization: false });

    const pageItems = tc.items
      .map((it, itemIndex) => {
        if (!('str' in it)) return null;
        const transform = it.transform ?? [1, 0, 0, 1, 0, 0];
        return {
          sourceId: source.sourceId,
          sourceSha256: source.sha256,
          extractor: 'pdfjs-dist',
          extractorVersion: pdfjsPackage.version,
          orderingVersion: 'v1',
          pdfPageIndex: pageIndex,
          pdfPageNumber: pageNumber,
          itemIndex,
          text: it.str,
          x: Number((transform[4] ?? 0).toFixed(4)),
          y: Number((transform[5] ?? 0).toFixed(4)),
          width: Number((it.width ?? 0).toFixed(4)),
          height: Number((it.height ?? Math.hypot(transform[2] ?? 0, transform[3] ?? 0)).toFixed(4)),
          hasEOL: Boolean(it.hasEOL),
          fontName: it.fontName ?? null,
        };
      })
      .filter(Boolean);

    const reconstructed = reconstructLines(pageItems).map(line => ({
      sourceId: source.sourceId,
      sourceSha256: source.sha256,
      extractor: 'pdfjs-dist',
      extractorVersion: pdfjsPackage.version,
      orderingVersion: 'v1',
      pdfPageIndex: pageIndex,
      pdfPageNumber: pageNumber,
      ...line,
    }));

    allItems.push(...pageItems);
    allLines.push(...reconstructed);
    pageText.push(
      `===== PDF PAGE ${pageNumber} / INDEX ${pageIndex} =====\n` +
      reconstructed.map(x => x.text).join('\n')
    );
  }

  ensureDir(OUTPUT_DIR);
  const itemPath = path.join(OUTPUT_DIR, `${source.sourceId}.items.jsonl`);
  const linePath = path.join(OUTPUT_DIR, `${source.sourceId}.lines.jsonl`);
  const textPath = path.join(OUTPUT_DIR, `${source.sourceId}.pages.txt`);

  writeJsonl(itemPath, allItems);
  writeJsonl(linePath, allLines);
  fs.writeFileSync(textPath, pageText.join('\n\n') + '\n', 'utf8');

  const outputHashes = {
    itemsJsonlSha256: sha256(fs.readFileSync(itemPath)),
    linesJsonlSha256: sha256(fs.readFileSync(linePath)),
    pagesTxtSha256: sha256(fs.readFileSync(textPath)),
  };

  return {
    sourceId: source.sourceId,
    sourceSha256: source.sha256,
    extractor: 'pdfjs-dist',
    extractorVersion: pdfjsPackage.version,
    orderingVersion: 'v1',
    pageCount: doc.numPages,
    rawItemCount: allItems.length,
    reconstructedLineCount: allLines.length,
    outputs: {
      itemsJsonl: path.relative(ROOT, itemPath),
      linesJsonl: path.relative(ROOT, linePath),
      pagesTxt: path.relative(ROOT, textPath),
    },
    outputHashes,
  };
}

const lock = readLock();
ensureDir(OUTPUT_DIR);
const results = [];
for (const source of lock.sources) {
  if (source.mimeType !== 'application/pdf') continue;
  results.push(await extractSource(source));
}

const manifest = {
  schemaVersion: 1,
  extractor: 'pdfjs-dist',
  extractorVersion: pdfjsPackage.version,
  orderingVersion: 'v1',
  generatedAtIncludedInCanonicalOutput: false,
  sources: results,
};
fs.writeFileSync(path.join(OUTPUT_DIR, 'run-manifest.json'), stableJson(manifest), 'utf8');

for (const r of results) {
  console.log(
    `EXTRACTED ${r.sourceId} pages=${r.pageCount} items=${r.rawItemCount} lines=${r.reconstructedLineCount} ` +
    `linesSha256=${r.outputHashes.linesJsonlSha256}`
  );
}
