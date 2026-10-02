// Engine-selection analysis over native probe outputs (derived/, not committed).
// Reads the hierarchy ground truth for evaluation only; nothing here feeds back into any engine.
// Usage: node src/analyze.mjs > derived/.../analysis.json
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../../..');
const D = path.join(root, 'derived/document-understanding/engine-selection');
const cfg = JSON.parse(await readFile(path.join(root, 'fixtures/document-understanding/engine-selection/probe-pages.json'), 'utf8'));
const gt = JSON.parse(await readFile(path.join(root, 'fixtures/document-understanding/engine-selection/mhlw-hierarchy-ground-truth.json'), 'utf8'));
const load = async (p) => JSON.parse(await readFile(path.join(D, p), 'utf8'));

const GLYPHS = { triangle: '△', blackTriangle: '▲', nbHyphen: '‑', hyphen: '‐', ascii: '-', minus: '−', fullwidthHyphen: '－', fullwidthDigit: /[０-９]/g };
const HY = /[‐‑‒–−]/g;
const squash = (s) => s.replace(/\s+/g, '');
const unify = (s) => squash(s).replace(HY, '-');
const count = (s, g) => (g instanceof RegExp ? (s.match(g) || []).length : s.split(g).length - 1);
const NUM = /△?\d{1,3}(?:,\d{3})+/g;

// Units: ordered native units with text and top-left bbox [x0,y0,x1,y1] (null when engine gives none).
function pdfjsUnits(doc) {
  const H = doc.viewBox[3];
  return doc.items.filter((it) => it.str.trim() !== '').map((it) => {
    const [a, , , d, e, f] = it.transform; const st = doc.styles[it.fontName] || {};
    const asc = (st.ascent ?? 0.8) * Math.abs(d), desc = (st.descent ?? -0.2) * Math.abs(d);
    return { text: it.str, bbox: [e, H - f - asc, e + it.width, H - f - desc] };
  });
}
const pymupdfSpans = (doc) => doc.dict.blocks.filter((b) => b.type === 0).flatMap((b) => b.lines.flatMap((l) => l.spans.filter((s) => s.text.trim() !== '').map((s) => ({ text: s.text, bbox: s.bbox }))));
const pymupdfWords = (doc) => doc.words.map((w) => ({ text: w[4], bbox: w.slice(0, 4) }));
const pymupdfLines = (doc) => doc.dict.blocks.filter((b) => b.type === 0).flatMap((b) => b.lines.map((l) => ({ text: l.spans.map((s) => s.text).join(''), bbox: l.bbox })));
const pymupdfChars = (doc) => doc.rawdict.blocks.filter((b) => b.type === 0).flatMap((b) => b.lines.flatMap((l) => l.spans.flatMap((s) => s.chars.map((c) => c.c)))).join('');
function doclingUnits(doc) {
  const d = doc.document; const H = Object.values(d.pages || {})[0]?.size?.height ?? 0;
  const tb = (b) => (b.coord_origin === 'BOTTOMLEFT' ? [b.l, H - b.t, b.r, H - b.b] : [b.l, b.t, b.r, b.b]);
  const texts = (d.texts || []).map((t) => ({ text: t.text, bbox: t.prov?.[0] ? tb(t.prov[0].bbox) : null, kind: t.label }));
  const cells = (d.tables || []).flatMap((t, ti) => t.data.table_cells.map((c) => ({ text: c.text, bbox: c.bbox ? tb(c.bbox) : null, kind: 'cell', table: ti, row: c.start_row_offset_idx, col: c.start_col_offset_idx })));
  return { texts, cells, all: [...texts, ...cells] };
}

function multisetCoverage(ref, got) {
  const m = new Map(); for (const ch of ref) m.set(ch, (m.get(ch) || 0) + 1);
  let hit = 0; for (const ch of got) { const n = m.get(ch); if (n) { hit++; m.set(ch, n - 1); } }
  return { refChars: [...ref].length, gotChars: [...got].length, matched: hit, coverage: +(hit / [...ref].length).toFixed(4) };
}
// Measurement reference only: PyMuPDF rawdict characters grouped into visual rows and joined when the
// horizontal gap is <= 1.5pt (touching/overlapping glyph runs). Not a proposed extraction rule.
function referenceNumbers(doc) {
  const chars = doc.rawdict.blocks.filter((b) => b.type === 0).flatMap((b) => b.lines.flatMap((l) => l.spans.flatMap((s) => s.chars))).filter((c) => c.c.trim() !== '');
  const rows = [];
  for (const c of [...chars].sort((a, b) => a.bbox[1] - b.bbox[1])) { const r = rows.find((r) => sameRow(r[0].bbox, c.bbox)); if (r) r.push(c); else rows.push([c]); }
  const runs = [];
  for (const r of rows) { r.sort((a, b) => a.bbox[0] - b.bbox[0]); let cur = ''; let last = null; for (const c of r) { if (last && c.bbox[0] - last.bbox[2] > 1.5) { runs.push(cur); cur = ''; } cur += c.c; last = c; } runs.push(cur); }
  return runs.flatMap((t) => t.match(NUM) || []);
}
function numberFidelity(ref, unitTexts) {
  const whole = new Map(); for (const t of unitTexts) for (const n of squash(t).match(NUM) || []) whole.set(n, (whole.get(n) || 0) + 1);
  let ok = 0; for (const n of ref) { const k = whole.get(n); if (k) { ok++; whole.set(n, k - 1); } }
  // Reversed comma-group order inside one unit (e.g. "623 396, 17," for 17,396,623).
  const rev = ref.filter((n) => { const g = n.replace('△', '').split(','); if (g.length < 2) return false; const r = g.reverse().map((x, i) => (i < g.length - 1 ? x : x)).join(''); return unitTexts.some((t) => { const u = t.replace(/[\s,]/g, ''); return u.includes(r) && !squash(t).includes(n.replace('△', '')); }); }).length;
  return { refNumbers: ref.length, wholeInOneUnit: ok, rate: ref.length ? +(ok / ref.length).toFixed(3) : null, reversedGroupOrderInOneUnit: rev };
}
// Same visual row: vertical centre within half the smaller height.
const sameRow = (a, b) => { const ca = (a[1] + a[3]) / 2, cb = (b[1] + b[3]) / 2; return Math.abs(ca - cb) <= Math.min(a[3] - a[1], b[3] - b[1]) / 2; };

function findUnits(units, needle) { const n = unify(needle); return units.filter((u) => unify(u.text).includes(n)); }

// Hierarchy node evaluation on one page for one engine.
function nodeObs(node, units, opts) {
  const codeStr = node.level === 'request' ? node.code : node.code;
  const nameU = findUnits(units, node.name);
  const res = { present: nameU.length > 0, codeAdjacent: false, requestRowComplete: null, exclusiveUnit: null };
  if (!nameU.length) return res;
  const codeU = units.filter((u) => unify(u.text).split(/[^0-9-]+/).includes(codeStr) || unify(u.text).startsWith(codeStr));
  if (opts.geometry) {
    res.codeAdjacent = nameU.some((n) => codeU.some((c) => sameRow(c.bbox, n.bbox) && c.bbox[0] <= n.bbox[0]));
    if (node.level === 'request' && opts.toc) {
      const no = units.filter((u) => squash(u.text) === node.requestNo);
      const pg = units.filter((u) => squash(u.text) === node.startsPrintedPage);
      res.requestRowComplete = nameU.some((n) => no.some((u) => sameRow(u.bbox, n.bbox)) && pg.some((u) => sameRow(u.bbox, n.bbox)) && codeU.some((u) => sameRow(u.bbox, n.bbox)));
    }
    res.exclusiveUnit = true;
  } else {
    res.codeAdjacent = nameU.some((n) => new RegExp(`(^|\\s)${codeStr}\\s*${unify(node.name).slice(0, 4)}`).test(unify(n.text).replace(/(\d)(?=\D)/, '$1 ')) || unify(n.text).includes(codeStr + unify(node.name)));
    // A unit that also contains a sibling/other GT node name is not exclusive to this node.
    const others = gt.nodes.filter((o) => o !== node && !node.name.includes(o.name) && !o.name.includes(node.name));
    res.exclusiveUnit = nameU.some((n) => !others.some((o) => unify(n.text).includes(unify(o.name))));
    if (node.level === 'request' && opts.toc) {
      res.requestRowComplete = nameU.some((n) => {
        if (n.kind !== 'cell') return false;
        const row = opts.cells.filter((c) => c.table === n.table && c.row === n.row);
        const has = (s) => row.some((c) => c.text.split(/\s+/).includes(s));
        return has(node.requestNo) && has(node.startsPrintedPage) && res.exclusiveUnit;
      });
    }
  }
  return res;
}

// Generic label-stack hierarchy reconstruction for the TOC from an ordered line stream (no GT used):
// "（組織）NNN name" opens an organization, "（項）NNN name" opens an item, "NNN NN-NN name ... page" is a request.
function labelStack(lines) {
  const out = []; let org = null, item = null;
  for (const raw of lines) {
    const t = unify(raw);
    let m;
    if ((m = t.match(/^（組織）(\d{3})(.+)$/))) { org = m[1]; item = null; }
    else if ((m = t.match(/^（項）(\d{3})(.+)$/))) { item = m[1]; }
    else if ((m = t.match(/^(\d{3})(\d{2}-\d{2})(.+?)(\d{3,4})$/))) out.push({ requestNo: m[1], code: m[2], parent: `${org}/${item}` });
  }
  return out;
}
function rowsFromGeometry(units, splitX) {
  // Group units into visual rows per column (split at splitX), ordered top-down, left column first.
  const cols = [units.filter((u) => u.bbox[0] < splitX), units.filter((u) => u.bbox[0] >= splitX)];
  return cols.flatMap((cu) => {
    const rows = [];
    for (const u of [...cu].sort((a, b) => a.bbox[1] - b.bbox[1] || a.bbox[0] - b.bbox[0])) {
      const r = rows.find((r) => sameRow(r[0].bbox, u.bbox)); if (r) r.push(u); else rows.push([u]);
    }
    return rows.map((r) => r.sort((a, b) => a.bbox[0] - b.bbox[0]).map((u) => u.text).join(''));
  });
}
function scoreStack(recs) {
  const reqs = gt.nodes.filter((n) => n.level === 'request');
  return reqs.map((n) => { const r = recs.find((x) => x.requestNo === n.requestNo); return { requestNo: n.requestNo, found: !!r, codeOk: r?.code === n.code, parentOk: r?.parent === n.parent }; });
}
// Reading-order stability: fraction of consecutive native units that stay within one column (TOC split).
function columnSwitches(units, splitX) { let s = 0; for (let i = 1; i < units.length; i++) if ((units[i].bbox[0] < splitX) !== (units[i - 1].bbox[0] < splitX)) s++; return s; }

const out = { generatedFrom: 'derived/document-understanding/engine-selection', pages: {}, hierarchy: {}, toc: {} };
const pdfjsLabel = 'pdfjs-v5-run1';
for (const p of cfg.pages) {
  const pj = await load(`${pdfjsLabel}/${p.probeId}.raw.json`);
  const pm = await load(`pymupdf-run1/${p.probeId}.json`);
  const dl = await load(`docling-no-ocr-run1/${p.probeId}.json`);
  const U = { pdfjs: pdfjsUnits(pj), pymupdfSpans: pymupdfSpans(pm), pymupdfWords: pymupdfWords(pm) };
  const DL = doclingUnits(dl);
  const refChars = squash(pymupdfChars(pm));
  const refNums = referenceNumbers(pm);
  const stream = { pdfjs: U.pdfjs.map((u) => u.text).join(''), pymupdf: refChars, docling: DL.all.map((u) => u.text).join('') };
  const pg = { units: { pdfjsItems: U.pdfjs.length, pymupdfWords: U.pymupdfWords.length, pymupdfSpans: U.pymupdfSpans.length, doclingTexts: DL.texts.length, doclingCells: DL.cells.length },
    charCoverageVsPyMuPDFRawdict: { pdfjs: multisetCoverage(refChars, squash(stream.pdfjs)), docling: multisetCoverage(refChars, squash(stream.docling)) },
    glyphs: Object.fromEntries(Object.entries(stream).map(([k, s]) => [k, Object.fromEntries(Object.entries(GLYPHS).map(([g, re]) => [g, count(s, re)]))])),
    commaNumbersWholeInOneNativeUnit: { pdfjsItem: numberFidelity(refNums, U.pdfjs.map((u) => u.text)), pymupdfWord: numberFidelity(refNums, U.pymupdfWords.map((u) => u.text)), pymupdfSpan: numberFidelity(refNums, U.pymupdfSpans.map((u) => u.text)), doclingUnit: numberFidelity(refNums, DL.all.map((u) => u.text)) } };
  out.pages[p.probeId] = pg;
  if (p.sourceId === gt.sourceId && ['mhlw-p7-toc', 'mhlw-p19-summary', 'mhlw-p1555', 'mhlw-p1603'].includes(p.probeId)) {
    const toc = p.probeId === 'mhlw-p7-toc';
    out.hierarchy[p.probeId] = {
      pdfjs: gt.nodes.map((n) => ({ node: `${n.level}:${n.requestNo ?? n.code}`, ...nodeObs(n, U.pdfjs, { geometry: true, toc }) })),
      pymupdf: gt.nodes.map((n) => ({ node: `${n.level}:${n.requestNo ?? n.code}`, ...nodeObs(n, U.pymupdfSpans, { geometry: true, toc }) })),
      docling: gt.nodes.map((n) => ({ node: `${n.level}:${n.requestNo ?? n.code}`, ...nodeObs(n, DL.all, { geometry: false, toc, cells: DL.cells }) })),
    };
    if (toc) {
      const W = pm.rect[2] / 2;
      out.toc = {
        splitX: W,
        nativeOrderColumnSwitches: { pdfjs: columnSwitches(U.pdfjs, W), pymupdfSpans: columnSwitches(U.pymupdfSpans, W), doclingTexts: DL.texts.filter((u) => u.bbox).length ? columnSwitches(DL.texts.filter((u) => u.bbox), W) : null },
        labelStackFromGeometryRows: { pdfjs: scoreStack(labelStack(rowsFromGeometry(U.pdfjs, W))), pymupdf: scoreStack(labelStack(rowsFromGeometry(U.pymupdfSpans, W))) },
        labelStackFromDoclingCells: scoreStack(labelStack(DL.cells.flatMap((c) => c.text.split(/(?=（組織）|（項）)|(?<=経費)\s/)))),
      };
    }
  }
}
console.log(JSON.stringify(out, null, 1));
