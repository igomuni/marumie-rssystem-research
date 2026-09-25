import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export const ROOT = path.resolve(__dirname, '..', '..', '..', '..');
export const CASES_DIR = path.join(ROOT, 'fixtures', 'document-understanding');
export const DERIVED_DIR = path.join(ROOT, 'derived', 'document-understanding');
export const EVIDENCE_DIR = path.join(ROOT, 'evidence', 'document-understanding');
export const REPORTS_DIR = path.join(ROOT, 'reports', 'document-understanding');

export function ensureDir(p) {
  fs.mkdirSync(p, { recursive: true });
}

export function readJson(p) {
  return JSON.parse(fs.readFileSync(p, 'utf8'));
}

export function writeJson(p, value) {
  ensureDir(path.dirname(p));
  fs.writeFileSync(p, JSON.stringify(value, null, 2) + '\n', 'utf8');
}

export function readGroundTruth(caseId) {
  return readJson(path.join(CASES_DIR, caseId, 'ground-truth.json'));
}

export function rawArtifactPath(caseId, engine) {
  return path.join(DERIVED_DIR, caseId, `${engine}.raw.json`);
}

export function normalizedArtifactPath(caseId, engine) {
  return path.join(DERIVED_DIR, caseId, `${engine}.normalized.json`);
}

// --- Generic, engine-agnostic row parsing ------------------------------
//
// This mirrors the amount-triple conventions already established in
// scripts/request-ingestion/src/ingest.mjs and scripts/pdf-extraction, applied
// to a *different* structural pattern: an item-code (項) header row, optionally
// wrapped across lines, followed by a request-number + expense-code (目) row,
// also optionally wrapped, ending in a three-column amount row that may carry
// a leading "△" (decrease) glyph on the final (delta) column.
//
// This parser does NOT know any case's expected values. It extracts every
// candidate row it can find on the given page; the caller (normalize.mjs)
// picks the row matching the case's itemCode/expenseCode for evaluation.

const DELTA_GLYPH = '△';

export function parseAmountToken(token) {
  if (token == null) return null;
  const isDelta = token.includes(DELTA_GLYPH);
  const digits = token.replace(DELTA_GLYPH, '').replace(/[,\s]/g, '');
  if (!/^\d+$/.test(digits)) return null;
  const magnitude = Number(digits);
  return { raw: token.trim(), magnitude, isDelta, signed: isDelta ? -magnitude : magnitude };
}

// Matches a trailing "prev, request, delta" triple where delta may carry a
// leading delta glyph (possibly separated by whitespace, as raw extraction
// sometimes emits it as its own token).
const TRIPLE_RE = /([0-9][0-9,]*)\s+([0-9][0-9,]*)\s+(△\s*[0-9][0-9,]*|[0-9][0-9,]*)\s*$/;

export function splitTrailingTriple(text) {
  const m = text.match(TRIPLE_RE);
  if (!m) return null;
  const previous = parseAmountToken(m[1]);
  const current = parseAmountToken(m[2]);
  const delta = parseAmountToken(m[3]);
  if (!previous || !current || !delta) return null;
  return {
    label: text.slice(0, m.index).trim(),
    previous,
    current,
    delta,
    matchedText: m[0],
  };
}

const ITEM_CODE_RE = /^(\d{3})\s+(.+)$/;
const EXPENSE_ROW_RE = /^(\d{1,2})\s+(\d{2}-\d{2})\s+(.+)$/;

export function findItemCodeRows(lines) {
  const rows = [];
  for (const line of lines) {
    const m = line.text.match(ITEM_CODE_RE);
    if (!m) continue;
    const triple = splitTrailingTriple(m[2]);
    rows.push({
      lineIndex: line.lineIndex,
      itemCode: m[1],
      itemNameFragment: triple ? triple.label : m[2].trim(),
      triple,
      rawText: line.text,
    });
  }
  return rows;
}

export function findExpenseRows(lines) {
  const rows = [];
  for (const line of lines) {
    const m = line.text.match(EXPENSE_ROW_RE);
    if (!m) continue;
    const triple = splitTrailingTriple(m[3]);
    rows.push({
      lineIndex: line.lineIndex,
      requestNo: m[1],
      expenseCode: m[2],
      expenseNameFragment: triple ? triple.label : m[3].trim(),
      triple,
      rawText: line.text,
    });
  }
  return rows;
}

// A wrapped label continues on the immediately following line when that line
// contains no digits-led structural marker of its own (no item code, no
// expense-row prefix, no amount triple) — i.e. it looks like bare
// continuation text. maxLinesAhead defaults to 1 because every other wrapped
// item/expense name on this document's pages wraps across exactly one
// continuation line (e.g. "036 公金受取口座登録業務支" + "援経費"); this is
// the general pattern observed across the page, not a value tuned to fit any
// single benchmark case. Increasing it would risk pulling in unrelated
// multi-column text that happens to share a reconstructed line's baseline —
// a real limitation this benchmark is meant to surface, not paper over.
export function joinWrappedLabel(lines, startLineIndex, maxLinesAhead = 1) {
  const byIndex = new Map(lines.map(l => [l.lineIndex, l]));
  let joined = '';
  let consumed = [];
  for (let i = 1; i <= maxLinesAhead; i++) {
    const next = byIndex.get(startLineIndex + i);
    if (!next) break;
    const t = next.text.trim();
    if (!t) break;
    if (ITEM_CODE_RE.test(t) || EXPENSE_ROW_RE.test(t) || splitTrailingTriple(t)) break;
    if (/^[─-╿]/.test(t)) break; // box-drawing table (国庫債務負担行為 etc.)
    joined += t;
    consumed.push(next.lineIndex);
  }
  return { joinedSuffix: joined, consumedLineIndexes: consumed };
}
