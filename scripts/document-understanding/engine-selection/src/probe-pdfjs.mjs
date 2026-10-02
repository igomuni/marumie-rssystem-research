// Engine-selection probe: pdf.js getTextContent native items for the probe page set.
// Usage: node src/probe-pdfjs.mjs <pdfjs-dist module dir> <label>
// Writes derived/document-understanding/engine-selection/pdfjs-<label>/<probeId>.<mode>.json
// Records native items as produced (no merge/repair). Modes: normalized (disableNormalization:false,
// research baseline) and raw (disableNormalization:true, marumie-rssystem PoC setting).
import { createHash } from 'node:crypto';
import { readFile, mkdir, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../../..');
const [pdfjsDir, label] = process.argv.slice(2);
if (!pdfjsDir || !label) throw new Error('usage: probe-pdfjs.mjs <pdfjs-dist dir> <label>');
const pdfjs = await import(pathToFileURL(path.join(pdfjsDir, 'legacy/build/pdf.mjs')).href);
const pkg = JSON.parse(await readFile(path.join(pdfjsDir, 'package.json'), 'utf8'));
const cfg = JSON.parse(await readFile(path.join(root, 'fixtures/document-understanding/engine-selection/probe-pages.json'), 'utf8'));
const outDir = path.join(root, 'derived/document-understanding/engine-selection', `pdfjs-${label}`);
await mkdir(outDir, { recursive: true });

const docs = new Map();
async function openDoc(sourceId, sha) {
  if (docs.has(sourceId)) return docs.get(sourceId);
  const bytes = await readFile(path.join(root, 'sources/raw', `${sourceId}.pdf`));
  const got = createHash('sha256').update(bytes).digest('hex');
  if (got !== sha) throw new Error(`sha mismatch ${sourceId}`);
  const t0 = performance.now();
  const doc = await pdfjs.getDocument({ data: new Uint8Array(bytes), cMapUrl: path.join(pdfjsDir, 'cmaps') + path.sep, cMapPacked: true, standardFontDataUrl: path.join(pdfjsDir, 'standard_fonts') + path.sep, isEvalSupported: false, verbosity: 0 }).promise;
  const entry = { doc, openMs: performance.now() - t0 };
  docs.set(sourceId, entry);
  return entry;
}

const summary = { engine: 'pdfjs-dist', version: pkg.version, label, pages: [] };
for (const p of cfg.pages) {
  const { doc, openMs } = await openDoc(p.sourceId, p.sourceSha256);
  const page = await doc.getPage(p.pdfPageIndex + 1);
  const viewport = page.getViewport({ scale: 1 });
  for (const [mode, disableNormalization] of [['normalized', false], ['raw', true]]) {
    const t0 = performance.now();
    const tc = await page.getTextContent({ disableNormalization, includeMarkedContent: false });
    const ms = performance.now() - t0;
    const items = tc.items.map((it, i) => ({ i, str: it.str, dir: it.dir, transform: it.transform, width: it.width, height: it.height, fontName: it.fontName, hasEOL: it.hasEOL }));
    const out = { probeId: p.probeId, pdfPageIndex: p.pdfPageIndex, mode, pdfjsVersion: pkg.version, viewBox: viewport.viewBox, styles: tc.styles, items };
    const json = JSON.stringify(out);
    await writeFile(path.join(outDir, `${p.probeId}.${mode}.json`), json);
    summary.pages.push({ probeId: p.probeId, mode, items: items.length, textContentMs: Math.round(ms), docOpenMs: Math.round(openMs), sha256: createHash('sha256').update(json).digest('hex') });
  }
  page.cleanup();
}
summary.rssMB = Math.round(process.memoryUsage().rss / 1048576);
await writeFile(path.join(outDir, '_summary.json'), JSON.stringify(summary, null, 2));
console.log(JSON.stringify(summary.pages.map((x) => [x.probeId, x.mode, x.items, x.textContentMs])), 'rssMB', summary.rssMB);
