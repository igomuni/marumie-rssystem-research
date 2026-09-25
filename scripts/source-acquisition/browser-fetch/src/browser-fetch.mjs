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

function sha256(buffer) {
  return crypto.createHash('sha256').update(buffer).digest('hex');
}

function ensureDir(p) {
  fs.mkdirSync(p, { recursive: true });
}

function loadLock() {
  if (!fs.existsSync(LOCK_PATH)) return { schemaVersion: 1, sources: [] };
  return JSON.parse(fs.readFileSync(LOCK_PATH, 'utf8'));
}

function writeLock(lock) {
  fs.writeFileSync(LOCK_PATH, JSON.stringify(lock, null, 2) + '\n', 'utf8');
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

  ensureDir(RAW_DIR);
  const rawPath = path.join(RAW_DIR, `${sourceId}${isPdf ? '.pdf' : '.bin'}`);
  fs.writeFileSync(rawPath, buffer);

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

  const lock = loadLock();
  const existingIndex = lock.sources.findIndex(s => s.sourceId === sourceId);
  if (existingIndex >= 0) lock.sources[existingIndex] = record;
  else lock.sources.push(record);
  writeLock(lock);

  console.log(`LOCKED ${sourceId} sha256=${record.sha256} sizeBytes=${record.sizeBytes} method=playwright-chromium`);
}

main().catch(err => {
  console.error(err.message);
  process.exitCode = 1;
});
