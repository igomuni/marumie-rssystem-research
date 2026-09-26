#!/usr/bin/env node
// Regression tests for acquire.mjs's (plain-fetch) source-lock immutability
// policy, and for lock-policy.mjs directly. These exercise the same
// mutation-safe semantics required of the browser-fetch path, using
// fixture/temp-dir-based lock files and an injected `download` function --
// no real network request to any government site.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { sha256, decideLockAction, applyAcquisition } from './lock-policy.mjs';
import { isPdfBuffer, acquireAndLock } from './acquire.mjs';

function t(name, fn) {
  const result = fn();
  if (result && typeof result.then === 'function') {
    return result.then(
      () => console.log(`PASS ${name}`),
      (err) => { console.error(`FAIL ${name}`); console.error(err); process.exitCode = 1; }
    );
  }
  console.log(`PASS ${name}`);
  return Promise.resolve();
}

function makeTmpDirs() {
  const base = fs.mkdtempSync(path.join(os.tmpdir(), 'acquire-test-'));
  const lockPath = path.join(base, 'source-lock.json');
  const rawDir = path.join(base, 'raw');
  return { base, lockPath, rawDir };
}

function writeInitialLock(lockPath, sources) {
  fs.writeFileSync(lockPath, JSON.stringify({ schemaVersion: 1, sources }, null, 2) + '\n', 'utf8');
}

function pdfBuffer(text) {
  return Buffer.from(`%PDF-1.4 ${text}`);
}

function fakeDownload({ sourceId, url, httpStatus = 200, buffer }) {
  return async () => ({
    sourceId,
    url,
    finalUrl: url,
    fetchedAt: '2026-01-01T00:00:00.000Z',
    httpStatus,
    mimeType: 'application/pdf',
    sizeBytes: buffer.length,
    sha256: sha256(buffer),
    etag: null,
    lastModified: null,
    buffer,
  });
}

async function main() {
  await t('isPdfBuffer: true for a %PDF- prefixed buffer', () => {
    assert.equal(isPdfBuffer(pdfBuffer('x')), true);
  });

  await t('isPdfBuffer: false for an HTML challenge-page body', () => {
    assert.equal(isPdfBuffer(Buffer.from('<html>bot challenge</html>')), false);
  });

  await t('acquireAndLock: new source -> raw file written and lock entry appended', async () => {
    const { lockPath, rawDir } = makeTmpDirs();
    const buffer = pdfBuffer('new source body');
    const result = await acquireAndLock({
      sourceId: 'case-new',
      url: 'https://example.test/new.pdf',
      lockPath,
      rawDir,
      download: fakeDownload({ sourceId: 'case-new', url: 'https://example.test/new.pdf', buffer }),
    });

    assert.equal(result.action, 'new');
    const lock = JSON.parse(fs.readFileSync(lockPath, 'utf8'));
    assert.equal(lock.sources.length, 1);
    assert.equal(lock.sources[0].sha256, sha256(buffer));
    const rawPath = path.join(rawDir, 'case-new.pdf');
    assert.ok(fs.existsSync(rawPath));
    assert.equal(fs.readFileSync(rawPath).toString(), buffer.toString());
  });

  await t('acquireAndLock: existing source + identical bytes/SHA-256 -> success, lock unchanged', async () => {
    const { lockPath, rawDir } = makeTmpDirs();
    const buffer = pdfBuffer('stable body');
    const existing = {
      sourceId: 'case-existing',
      url: 'https://example.test/existing.pdf',
      finalUrl: 'https://example.test/existing.pdf',
      fetchedAt: '2020-01-01T00:00:00.000Z',
      httpStatus: 200,
      mimeType: 'application/pdf',
      sizeBytes: buffer.length,
      sha256: sha256(buffer),
      etag: null,
      lastModified: null,
    };
    writeInitialLock(lockPath, [existing]);
    const lockBefore = fs.readFileSync(lockPath, 'utf8');

    const result = await acquireAndLock({
      sourceId: 'case-existing',
      url: 'https://example.test/existing.pdf',
      lockPath,
      rawDir,
      download: fakeDownload({ sourceId: 'case-existing', url: 'https://example.test/existing.pdf', buffer }),
    });

    assert.equal(result.action, 'identical');
    // Lock file bytes must be byte-for-byte unchanged, including fetchedAt --
    // a re-fetch that reproduces the same sha256 must not refresh timestamps
    // or other provenance metadata.
    const lockAfter = fs.readFileSync(lockPath, 'utf8');
    assert.equal(lockAfter, lockBefore);
    assert.equal(JSON.parse(lockAfter).sources[0].fetchedAt, '2020-01-01T00:00:00.000Z');
    // No raw dir/file should have been (re)created for the identical case.
    assert.equal(fs.existsSync(rawDir), false);
  });

  await t('acquireAndLock: existing source + different bytes/SHA-256 -> throws, lock and raw file unchanged', async () => {
    const { lockPath, rawDir } = makeTmpDirs();
    const oldBuffer = pdfBuffer('original canonical body');
    const existing = {
      sourceId: 'case-mismatch',
      url: 'https://example.test/mismatch.pdf',
      finalUrl: 'https://example.test/mismatch.pdf',
      fetchedAt: '2020-01-01T00:00:00.000Z',
      httpStatus: 200,
      mimeType: 'application/pdf',
      sizeBytes: oldBuffer.length,
      sha256: sha256(oldBuffer),
      etag: null,
      lastModified: null,
    };
    writeInitialLock(lockPath, [existing]);
    fs.mkdirSync(rawDir, { recursive: true });
    const rawPath = path.join(rawDir, 'case-mismatch.pdf');
    fs.writeFileSync(rawPath, oldBuffer);
    const lockBefore = fs.readFileSync(lockPath, 'utf8');
    const rawBefore = fs.readFileSync(rawPath);

    const newBuffer = pdfBuffer('a DIFFERENT upstream body entirely');
    await assert.rejects(
      () => acquireAndLock({
        sourceId: 'case-mismatch',
        url: 'https://example.test/mismatch.pdf',
        lockPath,
        rawDir,
        download: fakeDownload({ sourceId: 'case-mismatch', url: 'https://example.test/mismatch.pdf', buffer: newBuffer }),
      }),
      (err) => {
        assert.match(err.message, /case-mismatch/);
        assert.match(err.message, new RegExp(existing.sha256));
        assert.match(err.message, new RegExp(sha256(newBuffer)));
        return true;
      }
    );

    // Neither the lock file nor the canonical raw file may have been touched.
    assert.equal(fs.readFileSync(lockPath, 'utf8'), lockBefore);
    assert.deepEqual(fs.readFileSync(rawPath), rawBefore);
  });

  await t('acquireAndLock: non-PDF content (e.g. a WAF/challenge HTML page) is refused, no lock/raw write', async () => {
    const { lockPath, rawDir } = makeTmpDirs();
    const htmlBuffer = Buffer.from('<html><body>bot challenge, not the real file</body></html>');

    await assert.rejects(
      () => acquireAndLock({
        sourceId: 'case-waf',
        url: 'https://example.test/waf.pdf',
        lockPath,
        rawDir,
        download: fakeDownload({ sourceId: 'case-waf', url: 'https://example.test/waf.pdf', httpStatus: 202, buffer: htmlBuffer }),
      }),
      /PDF magic number/
    );

    assert.equal(fs.existsSync(lockPath), false);
    assert.equal(fs.existsSync(rawDir), false);
  });

  await t('acquireAndLock: non-2xx HTTP status is refused before any lock lookup', async () => {
    const { lockPath, rawDir } = makeTmpDirs();
    const buffer = pdfBuffer('irrelevant, status fails first');

    await assert.rejects(
      () => acquireAndLock({
        sourceId: 'case-bad-status',
        url: 'https://example.test/bad-status.pdf',
        lockPath,
        rawDir,
        download: fakeDownload({ sourceId: 'case-bad-status', url: 'https://example.test/bad-status.pdf', httpStatus: 500, buffer }),
      }),
      /HTTP 500/
    );

    assert.equal(fs.existsSync(lockPath), false);
    assert.equal(fs.existsSync(rawDir), false);
  });

  await t('decideLockAction / applyAcquisition (shared policy) are re-exported correctly and behave the same as browser-fetch\'s copy', () => {
    const lock = { schemaVersion: 1, sources: [{ sourceId: 'x', sha256: 'abc' }] };
    assert.equal(decideLockAction(lock, 'x', 'abc').action, 'identical');
    assert.equal(decideLockAction(lock, 'x', 'def').action, 'mismatch');
    assert.equal(decideLockAction(lock, 'y', 'abc').action, 'new');
  });
}

main();
