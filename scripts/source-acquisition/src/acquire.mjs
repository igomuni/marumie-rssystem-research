#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..', '..', '..');
const MANIFEST_PATH = path.join(ROOT, 'scripts', 'request-ingestion', 'source_manifest.json');
const LOCK_PATH = path.join(ROOT, 'sources', 'source-lock.json');
const RAW_DIR = path.join(ROOT, 'sources', 'raw');

function ensureDir(p) { fs.mkdirSync(p, { recursive: true }); }

function sha256(buffer) { return crypto.createHash('sha256').update(buffer).digest('hex'); }

function loadManifestSources() {
  const manifest = JSON.parse(fs.readFileSync(MANIFEST_PATH, 'utf8'));
  return manifest.sources.map(s => ({ sourceId: s.sourceDocumentId, url: s.url }));
}

function loadLock() {
  if (!fs.existsSync(LOCK_PATH)) {
    return { schemaVersion: 1, sources: [] };
  }
  return JSON.parse(fs.readFileSync(LOCK_PATH, 'utf8'));
}

function writeLock(lock) {
  fs.writeFileSync(LOCK_PATH, JSON.stringify(lock, null, 2) + '\n', 'utf8');
}

function extensionForMimeType(mimeType) {
  if (mimeType && mimeType.includes('pdf')) return '.pdf';
  return '.bin';
}

function rawFilePath(sourceId, mimeType) {
  return path.join(RAW_DIR, `${sourceId}${extensionForMimeType(mimeType)}`);
}

async function downloadSource(sourceId, url) {
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

async function lockCommand() {
  ensureDir(RAW_DIR);
  const manifestSources = loadManifestSources();
  const lock = loadLock();
  const results = [];

  for (const { sourceId, url } of manifestSources) {
    const acquired = await downloadSource(sourceId, url);
    if (acquired.httpStatus < 200 || acquired.httpStatus >= 300) {
      throw new Error(`Acquisition failed for ${sourceId}: HTTP ${acquired.httpStatus}`);
    }

    fs.writeFileSync(rawFilePath(sourceId, acquired.mimeType), acquired.buffer);

    const { buffer, ...record } = acquired;
    const existingIndex = lock.sources.findIndex(s => s.sourceId === sourceId);
    if (existingIndex >= 0) {
      lock.sources[existingIndex] = record;
    } else {
      lock.sources.push(record);
    }
    results.push(record);
  }

  writeLock(lock);

  for (const r of results) {
    console.log(`LOCKED ${r.sourceId} sha256=${r.sha256} sizeBytes=${r.sizeBytes} httpStatus=${r.httpStatus}`);
  }
  console.log(`${results.length}/${manifestSources.length} source binaries locked`);
}

async function verifyCommand() {
  if (!fs.existsSync(LOCK_PATH)) {
    console.error('No sources/source-lock.json found. Run `npm run sources:lock` first.');
    process.exitCode = 1;
    return;
  }
  const lock = loadLock();
  let failures = 0;

  for (const locked of lock.sources) {
    const acquired = await downloadSource(locked.sourceId, locked.url);
    if (acquired.sha256 === locked.sha256) {
      console.log(`PASS ${locked.sourceId}`);
    } else {
      failures += 1;
      console.log(`FAIL ${locked.sourceId}`);
      console.log(`expected: ${locked.sha256}`);
      console.log(`actual:   ${acquired.sha256}`);
    }
  }

  console.log(`${lock.sources.length - failures}/${lock.sources.length} source binaries verified`);
  if (failures > 0) process.exitCode = 1;
}

const command = process.argv[2];
if (command === 'lock') {
  lockCommand().catch(err => { console.error(err.message); process.exitCode = 1; });
} else if (command === 'verify') {
  verifyCommand().catch(err => { console.error(err.message); process.exitCode = 1; });
} else {
  console.error('Usage: acquire.mjs <lock|verify>');
  process.exitCode = 1;
}
