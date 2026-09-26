#!/usr/bin/env node
// Browser-based source acquisition, for sources that a plain fetch() cannot
// reach (e.g. AWS WAF JavaScript bot challenges). Uses a real, isolated
// Chromium instance (Playwright) purely to retrieve the binary a human would
// get by visiting the page in a browser — it does not interact with any
// document-understanding engine and does not read the PDF's content.
//
// This is deliberately a separate, explicit tool from scripts/source-acquisition/
// src/acquire.mjs (the plain-fetch lock/verify/fetch mechanism used for sources
// that don't need a browser). It follows the same lock-file schema and the same
// "lock is explicit, reviewable, never silently overwritten" discipline (see
// protocol/DECISIONS.md ADR-009), with two additions:
//   - it also verifies the downloaded bytes start with the PDF magic number
//     (%PDF-) before accepting them as a successful acquisition — plain
//     acquire.mjs does not currently do this, and a WAF challenge page can
//     return a 2xx/202-range status with an HTML body, which acquire.mjs would
//     otherwise silently accept as if it were the real file (see
//     state/CHANGELOG.md's case-002 preregistration entry for how this was
//     found);
//   - it records acquisitionMethod/playwrightVersion/landingPageUrl in the
//     lock entry for provenance, since "how" this source had to be acquired
//     is itself a fact worth preserving.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { chromium } from 'playwright';

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..', '..', '..', '..');
const LOCK_PATH = path.join(ROOT, 'sources', 'source-lock.json');
const RAW_DIR = path.join(ROOT, 'sources', 'raw');

export function sha256(buffer) {
  return crypto.createHash('sha256').update(buffer).digest('hex');
}

function ensureDir(p) {
  fs.mkdirSync(p, { recursive: true });
}

function loadLock(lockPath) {
  if (!fs.existsSync(lockPath)) return { schemaVersion: 1, sources: [] };
  return JSON.parse(fs.readFileSync(lockPath, 'utf8'));
}

function writeLock(lockPath, lock) {
  fs.writeFileSync(lockPath, JSON.stringify(lock, null, 2) + '\n', 'utf8');
}

// Pure decision function: given the current lock and a freshly-fetched
// sourceId/sha256 pair, decide what MAY be written, without touching the
// filesystem. This is the policy this file's header comment promises
// ("lock is explicit, reviewable, never silently overwritten") — kept as a
// standalone, unit-testable function so the mutation policy can be verified
// without a real browser/network fetch. See applyAcquisition() below for how
// this decision is turned into (or deliberately withheld from) filesystem
// writes.
export function decideLockAction(lock, sourceId, newSha256) {
  const existingIndex = lock.sources.findIndex((s) => s.sourceId === sourceId);
  if (existingIndex < 0) return { action: 'new', existingIndex: -1, existing: null };
  const existing = lock.sources[existingIndex];
  if (existing.sha256 === newSha256) return { action: 'identical', existingIndex, existing };
  return { action: 'mismatch', existingIndex, existing };
}

// Applies decideLockAction()'s decision to the filesystem. Mutation-safe
// ordering: the caller must have already computed newSha256 (from an
// already-validated, already-in-memory buffer) BEFORE this function is
// called, so a mismatch is detected and reported without ever having written
// the new bytes over the existing canonical raw file or lock entry.
//   - 'new'       -> writes the raw file and appends a new lock entry.
//   - 'identical' -> writes nothing; the existing lock entry and raw file are
//                    left exactly as they were (no fetchedAt/finalUrl/
//                    playwrightVersion refresh either — a re-fetch that
//                    reproduces the same bytes is not new information).
//   - 'mismatch'  -> writes nothing and throws; the existing lock entry and
//                    raw file are left exactly as they were. The caller is
//                    responsible for a non-zero process exit.
export function applyAcquisition({ lockPath, rawDir, sourceId, buffer, isPdf, record }) {
  const lock = loadLock(lockPath);
  const newSha256 = record.sha256;
  const decision = decideLockAction(lock, sourceId, newSha256);

  if (decision.action === 'mismatch') {
    throw new Error(
      `Refusing to overwrite the existing lock entry for "${sourceId}": it is locked at ` +
      `sha256=${decision.existing.sha256}, but this fetch retrieved a different binary ` +
      `(sha256=${newSha256}). The existing lock entry and its raw source file were NOT modified. ` +
      `If the upstream source has genuinely changed and the lock should be updated, that is a ` +
      `deliberate, reviewable decision this tool does not make automatically — re-lock manually ` +
      `after confirming the change is intentional.`
    );
  }

  if (decision.action === 'identical') {
    return { action: 'identical', record: decision.existing };
  }

  // action === 'new'
  ensureDir(rawDir);
  const rawPath = path.join(rawDir, `${sourceId}${isPdf ? '.pdf' : '.bin'}`);
  fs.writeFileSync(rawPath, buffer);
  lock.sources.push(record);
  writeLock(lockPath, lock);
  return { action: 'new', record };
}

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i += 2) {
    const key = argv[i]?.replace(/^--/, '');
    args[key] = argv[i + 1];
  }
  return args;
}

async function browserFetch({ url, landingPageUrl }) {
  const browser = await chromium.launch();
  try {
    const context = await browser.newContext({
      userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
      acceptDownloads: true,
    });
    const page = await context.newPage();

    if (landingPageUrl) {
      // Some sources' bot-challenge state is only satisfied for a session
      // that first navigates a normal HTML page, not a direct binary request.
      await page.goto(landingPageUrl, { waitUntil: 'networkidle', timeout: 30000 });
    }

    const [download] = await Promise.all([
      page.waitForEvent('download', { timeout: 20000 }).catch(() => null),
      page.goto(url, { waitUntil: 'load', timeout: 30000 }).catch(() => null),
    ]);

    let buffer;
    let finalUrl = url;
    if (download) {
      const tmpPath = await download.path();
      buffer = fs.readFileSync(tmpPath);
      finalUrl = download.url();
    } else {
      const resp = await page.goto(url, { timeout: 30000 });
      finalUrl = resp.url();
      buffer = await resp.body();
    }
    return { buffer, finalUrl };
  } finally {
    await browser.close();
  }
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const { 'source-id': sourceId, url, 'landing-page': landingPageUrl, 'mime-type': mimeType = 'application/pdf' } = args;
  if (!sourceId || !url) {
    console.error('Usage: browser-fetch.mjs --source-id <id> --url <url> [--landing-page <url>] [--mime-type <type>]');
    process.exitCode = 1;
    return;
  }

  console.log(`Launching headless Chromium to fetch ${sourceId}...`);
  const { buffer, finalUrl } = await browserFetch({ url, landingPageUrl });

  const isPdf = buffer.subarray(0, 5).toString('latin1') === '%PDF-';
  if (mimeType === 'application/pdf' && !isPdf) {
    throw new Error(
      `Downloaded content for ${sourceId} does not start with the PDF magic number (%PDF-). ` +
      `This usually means a bot-challenge/interstitial page was captured instead of the real file. ` +
      `Refusing to lock it. First 200 bytes: ${buffer.subarray(0, 200).toString('utf8')}`
    );
  }

  // Mutation-safe order: the SHA-256 is computed, and compared against the
  // existing lock, entirely in memory, before anything on disk (the raw file
  // or the lock file) is touched. See applyAcquisition()/decideLockAction()
  // above for why this ordering matters — it is what makes a same-sourceId
  // re-fetch with a genuinely different upstream binary a loud, non-mutating
  // failure instead of a silent lock replacement.
  const record = {
    sourceId,
    url,
    finalUrl,
    fetchedAt: new Date().toISOString(),
    httpStatus: 200,
    mimeType,
    sizeBytes: buffer.length,
    sha256: sha256(buffer),
    etag: null,
    lastModified: null,
    acquisitionMethod: 'playwright-chromium',
    playwrightVersion: (await import('playwright/package.json', { with: { type: 'json' } })).default.version,
    landingPageUrl: landingPageUrl ?? null,
  };

  const result = applyAcquisition({ lockPath: LOCK_PATH, rawDir: RAW_DIR, sourceId, buffer, isPdf, record });

  if (result.action === 'identical') {
    console.log(
      `VERIFIED ${sourceId} sha256=${result.record.sha256}: freshly fetched bytes match the existing ` +
      `locked entry exactly. Lock entry and raw source file were left unchanged (no mutation needed).`
    );
  } else {
    console.log(`LOCKED ${sourceId} sha256=${result.record.sha256} sizeBytes=${result.record.sizeBytes} method=playwright-chromium`);
  }
}

// Only run main() when this file is executed directly (node src/browser-fetch.mjs),
// not when it is imported for its exported functions (e.g. by test.mjs) --
// otherwise importing this module for unit testing would itself trigger a
// real CLI invocation with no arguments.
const isDirectlyExecuted = process.argv[1] && import.meta.url === new URL(process.argv[1], 'file://').href;
if (isDirectlyExecuted) {
  main().catch(err => {
    console.error(err.message);
    process.exitCode = 1;
  });
}
