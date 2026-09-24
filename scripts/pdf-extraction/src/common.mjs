import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export const ROOT = path.resolve(__dirname, '..', '..', '..');
export const LOCK_PATH = path.join(ROOT, 'sources', 'source-lock.json');
export const RAW_DIR = path.join(ROOT, 'sources', 'raw');
export const OUTPUT_DIR = path.join(ROOT, 'derived', 'pdf-extraction');
export const FIXTURE_DIR = path.join(ROOT, 'scripts', 'request-ingestion', 'fixtures');

export function ensureDir(p) {
  fs.mkdirSync(p, { recursive: true });
}

export function sha256(data) {
  return crypto.createHash('sha256').update(data).digest('hex');
}

export function readJson(p) {
  return JSON.parse(fs.readFileSync(p, 'utf8'));
}

export function readLock() {
  const lock = readJson(LOCK_PATH);
  if (!Array.isArray(lock.sources)) throw new Error('Invalid sources/source-lock.json: sources must be an array');
  return lock;
}

export function extensionForMimeType(mimeType) {
  if (mimeType?.includes('pdf')) return '.pdf';
  return '.bin';
}

export function rawFilePath(source) {
  return path.join(RAW_DIR, `${source.sourceId}${extensionForMimeType(source.mimeType)}`);
}

export function verifyLockedRaw(source) {
  const file = rawFilePath(source);
  if (!fs.existsSync(file)) {
    throw new Error(
      `Missing locked raw source: ${file}\n` +
      `Run \`npm run sources:fetch\` to materialize the exact locked binary without changing the lock.`
    );
  }
  const data = fs.readFileSync(file);
  const actualHash = sha256(data);
  if (actualHash !== source.sha256) {
    throw new Error(
      `Locked-source hash mismatch for ${source.sourceId}\n` +
      `expected: ${source.sha256}\nactual:   ${actualHash}`
    );
  }
  if (Number.isFinite(source.sizeBytes) && data.length !== source.sizeBytes) {
    throw new Error(
      `Locked-source size mismatch for ${source.sourceId}: expected ${source.sizeBytes}, actual ${data.length}`
    );
  }
  return { file, data };
}

export function stableJson(value) {
  return JSON.stringify(value, null, 2) + '\n';
}

export function writeJsonl(file, rows) {
  fs.writeFileSync(file, rows.map(r => JSON.stringify(r)).join('\n') + '\n', 'utf8');
}

export function readJsonl(file) {
  return fs.readFileSync(file, 'utf8')
    .split(/\r?\n/)
    .filter(Boolean)
    .map(line => JSON.parse(line));
}

export function normalizeText(s) {
  return String(s)
    .normalize('NFKC')
    .replace(/\u00a0/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

export function compactText(s) {
  return normalizeText(s).replace(/\s+/g, '');
}

// U+25B3 WHITE UP-POINTING TRIANGLE: the standard Japanese government budget-document
// convention marking a decrease immediately before an amount (e.g. "△ 5,825,544").
// It is a presentation-only sign glyph, not part of the digits themselves; some historical
// curated fixtures omit it while others encode the decrease differently. Comparison logic
// treats its presence/absence as immaterial to whether the amount content matches; the raw
// extraction output is never altered.
const DELTA_DECREASE_GLYPH = /△/g;

export function compactTextIgnoringDeltaGlyph(s) {
  return compactText(s).replace(DELTA_DECREASE_GLYPH, '');
}

export function numericTokens(s) {
  return (String(s).match(/(?<![\d-])\d[\d,]*(?![\d-])/g) ?? []).map(x => x.replace(/,/g, ''));
}

export function budgetCode(s) {
  const m = String(s).match(/\b\d{5}-\d{4}-\d{2}-\d{4}\b/);
  return m?.[0] ?? null;
}

export function parseHistoricalFixture(file) {
  const rows = [];
  for (const raw of fs.readFileSync(file, 'utf8').split(/\r?\n/)) {
    if (!raw || raw.trimStart().startsWith('#')) continue;
    const m = raw.match(/^L(\d+)@P(\d+):\s*(.*)$/);
    if (!m) throw new Error(`Unexpected fixture line in ${file}: ${raw}`);
    rows.push({
      legacySourceLine: Number(m[1]),
      legacyPageIndex: Number(m[2]),
      text: m[3],
      rawFixtureLine: raw,
    });
  }
  return rows;
}
