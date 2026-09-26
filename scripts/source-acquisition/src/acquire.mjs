#!/usr/bin/env node
// Plain-fetch() source acquisition/verification for sources that don't need
// a browser (see scripts/source-acquisition/browser-fetch/ for sources
// protected by a JS bot challenge). The immutable lock-decision/mutation
// policy is shared, acquisition-method-independent code -- see
// ./lock-policy.mjs -- so "once a source identity is locked, different
// bytes never silently replace it" (protocol/DECISIONS.md ADR-009) holds the
// same way here as it does for the Playwright-based tool.
import fs from 'node:fs';
import path from 'node:path';
import { sha256, applyAcquisition } from './lock-policy.mjs';

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..', '..', '..');
const MANIFEST_PATH = path.join(ROOT, 'scripts', 'request-ingestion', 'source_manifest.json');
const LOCK_PATH = path.join(ROOT, 'sources', 'source-lock.json');
const RAW_DIR = path.join(ROOT, 'sources', 'raw');

function ensureDir(p) { fs.mkdirSync(p, { recursive: true }); }

function loadManifestSources() {
  const manifest = JSON.parse(fs.readFileSync(MANIFEST_PATH, 'utf8'));
  return manifest.sources.map(s => ({ sourceId: s.sourceDocumentId, url: s.url }));
}

function loadLock() {
  if (!fs.existsSync(LOCK_PATH)) return { schemaVersion: 1, sources: [] };
  return JSON.parse(fs.readFileSync(LOCK_PATH, 'utf8'));
}

function extensionForMimeType(mimeType) {
  if (mimeType && mimeType.includes('pdf')) return '.pdf';
  return '.bin';
}

function rawFilePath(sourceId, mimeType) {
  return path.join(RAW_DIR, `${sourceId}${extensionForMimeType(mimeType)}`);
}

// Every current manifest source is a PDF; a WAF/bot-challenge interstitial
// can return a 2xx (or 202-range) status with an HTML body in its place
// (see state/CHANGELOG.md's case-002 preregistration entry for how this was
// discovered for a different acquisition path). Checking the magic number
// here closes that gap for the plain-fetch path too, mirroring
// browser-fetch.mjs's existing check.
export function isPdfBuffer(buffer) {
  return buffer.subarray(0, 5).toString('latin1') === '%PDF-';
}

export async function downloadSource(sourceId, url) {
  const res = await fetch(url);
  const buffer = Buffer.from(await res.arrayBuffer());
  const mimeType = res.headers.get('content-type')?.split(';')[0]?.trim() ?? null;
  return {
    sourceId,
    url,
    finalUrl: res.url,
    fetchedAt: new Date().toISOString(),
    httpStatus: res.status,
    mimeType,
    sizeBytes: buffer.length,
    sha256: sha256(buffer),
    etag: res.headers.get('etag') ?? null,
    lastModified: res.headers.get('last-modified') ?? null,
    buffer,
  };
}

// Mutation-safe per-source acquisition: download into memory -> validate
// HTTP status -> validate PDF representation -> SHA-256 already computed by
// downloadSource() -> applyAcquisition() looks up the existing lock and only
// THEN decides whether to write anything. No raw file or lock write happens
// before that comparison, so a mismatched re-fetch can never clobber the
// existing canonical raw bytes or lock entry. `download` is injectable so
// this can be unit-tested without a real network fetch (see test.mjs).
export async function acquireAndLock({ sourceId, url, lockPath, rawDir, download = downloadSource }) {
  const acquired = await download(sourceId, url);
  if (acquired.httpStatus < 200 || acquired.httpStatus >= 300) {
    throw new Error(`Acquisition failed for ${sourceId}: HTTP ${acquired.httpStatus}`);
  }
  const isPdf = isPdfBuffer(acquired.buffer);
  if (!isPdf) {
    throw new Error(
      `Downloaded content for ${sourceId} does not start with the PDF magic number (%PDF-). ` +
      `This usually means a bot-challenge/interstitial page was captured instead of the real file. ` +
      `Refusing to lock it. First 200 bytes: ${acquired.buffer.subarray(0, 200).toString('utf8')}`
    );
  }
  const { buffer, ...record } = acquired;
  const result = applyAcquisition({ lockPath, rawDir, sourceId, buffer, isPdf, record });
  return { sourceId, ...result };
}

async function lockCommand() {
  const manifestSources = loadManifestSources();
  const results = [];

  for (const { sourceId, url } of manifestSources) {
    const result = await acquireAndLock({ sourceId, url, lockPath: LOCK_PATH, rawDir: RAW_DIR });
    results.push(result);
  }

  for (const r of results) {
    if (r.action === 'identical') {
      console.log(
        `VERIFIED ${r.sourceId} sha256=${r.record.sha256}: freshly fetched bytes match the existing ` +
        `locked entry exactly. Lock entry and raw source file were left unchanged.`
      );
    } else {
      console.log(`LOCKED ${r.sourceId} sha256=${r.record.sha256} sizeBytes=${r.record.sizeBytes} httpStatus=${r.record.httpStatus}`);
    }
  }
  console.log(`${results.length}/${manifestSources.length} source binaries locked/verified`);
}

async function verifyCommand({ materialize = false } = {}) {
  if (!fs.existsSync(LOCK_PATH)) {
    console.error('No sources/source-lock.json found. Run `npm run sources:lock` first.');
    process.exitCode = 1;
    return;
  }
  if (materialize) ensureDir(RAW_DIR);
  const lock = loadLock();
  let failures = 0;

  for (const locked of lock.sources) {
    const acquired = await downloadSource(locked.sourceId, locked.url);
    const statusOk = acquired.httpStatus >= 200 && acquired.httpStatus < 300;
    const hashOk = acquired.sha256 === locked.sha256;
    const sizeOk = !Number.isFinite(locked.sizeBytes) || acquired.sizeBytes === locked.sizeBytes;

    if (statusOk && hashOk && sizeOk) {
      if (materialize) {
        fs.writeFileSync(rawFilePath(locked.sourceId, locked.mimeType ?? acquired.mimeType), acquired.buffer);
        console.log(`FETCHED ${locked.sourceId}`);
      } else {
        console.log(`PASS ${locked.sourceId}`);
      }
    } else {
      failures += 1;
      console.log(`FAIL ${locked.sourceId}`);
      if (!statusOk) console.log(`httpStatus expected 2xx, actual ${acquired.httpStatus}`);
      if (!hashOk) {
        console.log(`expected: ${locked.sha256}`);
        console.log(`actual:   ${acquired.sha256}`);
      }
      if (!sizeOk) console.log(`size expected ${locked.sizeBytes}, actual ${acquired.sizeBytes}`);
    }
  }

  const verb = materialize ? 'fetched and verified' : 'verified';
  console.log(`${lock.sources.length - failures}/${lock.sources.length} source binaries ${verb}`);
  if (failures > 0) process.exitCode = 1;
}

// Only run a CLI command when this file is executed directly, not when it is
// imported for its exported functions (e.g. by test.mjs).
const isDirectlyExecuted = process.argv[1] && import.meta.url === new URL(process.argv[1], 'file://').href;
if (isDirectlyExecuted) {
  const command = process.argv[2];
  if (command === 'lock') {
    lockCommand().catch(err => { console.error(err.message); process.exitCode = 1; });
  } else if (command === 'verify') {
    verifyCommand().catch(err => { console.error(err.message); process.exitCode = 1; });
  } else if (command === 'fetch') {
    verifyCommand({ materialize: true }).catch(err => { console.error(err.message); process.exitCode = 1; });
  } else {
    console.error('Usage: acquire.mjs <lock|verify|fetch>');
    process.exitCode = 1;
  }
}
