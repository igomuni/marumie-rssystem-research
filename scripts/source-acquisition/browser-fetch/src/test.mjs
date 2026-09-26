#!/usr/bin/env node
// Regression tests for browser-fetch's lock-immutability policy
// (decideLockAction / applyAcquisition). These exercise the lock-decision
// and filesystem-mutation logic in isolation from Playwright/network, using
// a fixture-based temporary directory for the lock file and raw source dir.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { sha256, decideLockAction, applyAcquisition } from './browser-fetch.mjs';

function t(name, fn) {
  try {
    fn();
    console.log(`PASS ${name}`);
  } catch (err) {
    console.error(`FAIL ${name}`);
    console.error(err);
    process.exitCode = 1;
  }
}

function makeTmpDirs() {
  const base = fs.mkdtempSync(path.join(os.tmpdir(), 'browser-fetch-test-'));
  const lockPath = path.join(base, 'source-lock.json');
  const rawDir = path.join(base, 'raw');
  return { base, lockPath, rawDir };
}

function writeInitialLock(lockPath, sources) {
  fs.writeFileSync(lockPath, JSON.stringify({ schemaVersion: 1, sources }, null, 2) + '\n', 'utf8');
}

function baseRecord(sourceId, buffer, overrides = {}) {
  return {
    sourceId,
    url: `https://example.test/${sourceId}.pdf`,
    finalUrl: `https://example.test/${sourceId}.pdf`,
    fetchedAt: '2026-01-01T00:00:00.000Z',
    httpStatus: 200,
    mimeType: 'application/pdf',
    sizeBytes: buffer.length,
    sha256: sha256(buffer),
    etag: null,
    lastModified: null,
    acquisitionMethod: 'playwright-chromium',
    playwrightVersion: '1.63.0',
    landingPageUrl: null,
    ...overrides,
  };
}

t('decideLockAction: unknown sourceId -> new', () => {
  const lock = { schemaVersion: 1, sources: [] };
  const decision = decideLockAction(lock, 'foo', 'abc123');
  assert.equal(decision.action, 'new');
});

t('decideLockAction: same sourceId + same sha256 -> identical', () => {
  const lock = { schemaVersion: 1, sources: [{ sourceId: 'foo', sha256: 'abc123' }] };
  const decision = decideLockAction(lock, 'foo', 'abc123');
  assert.equal(decision.action, 'identical');
});

t('decideLockAction: same sourceId + different sha256 -> mismatch', () => {
  const lock = { schemaVersion: 1, sources: [{ sourceId: 'foo', sha256: 'abc123' }] };
  const decision = decideLockAction(lock, 'foo', 'def456');
  assert.equal(decision.action, 'mismatch');
  assert.equal(decision.existing.sha256, 'abc123');
});

t('applyAcquisition: new source -> raw file written and lock entry appended', () => {
  const { lockPath, rawDir } = makeTmpDirs();
  const buffer = Buffer.from('%PDF-1.4 fixture body A');
  const record = baseRecord('case-new', buffer);

  const result = applyAcquisition({ lockPath, rawDir, sourceId: 'case-new', buffer, isPdf: true, record });

  assert.equal(result.action, 'new');
  const lock = JSON.parse(fs.readFileSync(lockPath, 'utf8'));
  assert.equal(lock.sources.length, 1);
  assert.equal(lock.sources[0].sourceId, 'case-new');
  assert.equal(lock.sources[0].sha256, record.sha256);
  const rawPath = path.join(rawDir, 'case-new.pdf');
  assert.ok(fs.existsSync(rawPath));
  assert.equal(fs.readFileSync(rawPath).toString(), buffer.toString());
});

t('applyAcquisition: existing source + identical bytes/sha256 -> success, lock unchanged', () => {
  const { lockPath, rawDir } = makeTmpDirs();
  const buffer = Buffer.from('%PDF-1.4 fixture body B');
  const existing = baseRecord('case-existing', buffer, { fetchedAt: '2020-01-01T00:00:00.000Z' });
  writeInitialLock(lockPath, [existing]);
  const lockBefore = fs.readFileSync(lockPath, 'utf8');

  const newRecord = baseRecord('case-existing', buffer, { fetchedAt: '2026-09-26T00:00:00.000Z' });
  const result = applyAcquisition({ lockPath, rawDir, sourceId: 'case-existing', buffer, isPdf: true, record: newRecord });

  assert.equal(result.action, 'identical');
  // Lock file bytes must be byte-for-byte unchanged, including fetchedAt --
  // a re-fetch that reproduces the same sha256 must not refresh timestamps.
  const lockAfter = fs.readFileSync(lockPath, 'utf8');
  assert.equal(lockAfter, lockBefore);
  const lock = JSON.parse(lockAfter);
  assert.equal(lock.sources[0].fetchedAt, '2020-01-01T00:00:00.000Z');
  // Raw dir/file must not have been (re)created for the identical case.
  assert.equal(fs.existsSync(rawDir), false);
});

t('applyAcquisition: existing source + different bytes/sha256 -> throws, lock and raw file unchanged', () => {
  const { lockPath, rawDir } = makeTmpDirs();
  const oldBuffer = Buffer.from('%PDF-1.4 original canonical body');
  const existing = baseRecord('case-mismatch', oldBuffer);
  writeInitialLock(lockPath, [existing]);
  fs.mkdirSync(rawDir, { recursive: true });
  const rawPath = path.join(rawDir, 'case-mismatch.pdf');
  fs.writeFileSync(rawPath, oldBuffer);
  const lockBefore = fs.readFileSync(lockPath, 'utf8');
  const rawBefore = fs.readFileSync(rawPath);

  const newBuffer = Buffer.from('%PDF-1.4 a DIFFERENT upstream body entirely');
  const newRecord = baseRecord('case-mismatch', newBuffer);

  assert.throws(
    () => applyAcquisition({ lockPath, rawDir, sourceId: 'case-mismatch', buffer: newBuffer, isPdf: true, record: newRecord }),
    (err) => {
      assert.match(err.message, /case-mismatch/);
      assert.match(err.message, new RegExp(existing.sha256));
      assert.match(err.message, new RegExp(newRecord.sha256));
      return true;
    }
  );

  // Neither the lock file nor the canonical raw file may have been touched.
  assert.equal(fs.readFileSync(lockPath, 'utf8'), lockBefore);
  assert.deepEqual(fs.readFileSync(rawPath), rawBefore);
});

t('applyAcquisition: mismatch error message identifies sourceId and both sha256 values', () => {
  const { lockPath, rawDir } = makeTmpDirs();
  const oldBuffer = Buffer.from('%PDF-1.4 v1');
  const existing = baseRecord('case-msg', oldBuffer);
  writeInitialLock(lockPath, [existing]);

  const newBuffer = Buffer.from('%PDF-1.4 v2, definitely different bytes');
  const newRecord = baseRecord('case-msg', newBuffer);

  try {
    applyAcquisition({ lockPath, rawDir, sourceId: 'case-msg', buffer: newBuffer, isPdf: true, record: newRecord });
    throw new Error('expected applyAcquisition to throw');
  } catch (err) {
    assert.ok(err.message.includes('case-msg'));
    assert.ok(err.message.includes(existing.sha256));
    assert.ok(err.message.includes(newRecord.sha256));
  }
});
