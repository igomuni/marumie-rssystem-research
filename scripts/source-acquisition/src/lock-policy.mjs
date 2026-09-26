// Shared, acquisition-method-independent lock-decision/mutation policy.
//
// Both scripts/source-acquisition/src/acquire.mjs (plain fetch()) and
// scripts/source-acquisition/browser-fetch/src/browser-fetch.mjs (Playwright)
// acquire bytes for a sourceId in their own, method-specific way, but once
// bytes and a SHA-256 are in hand, the question "may this be written to
// sources/source-lock.json and sources/raw/?" must have exactly one answer,
// independent of which method fetched the bytes (see protocol/DECISIONS.md
// ADR-009: source identity is the acquired binary's hash, not the URL or the
// method used to retrieve it).
//
// Policy (mutation-safe -- callers must compute newSha256 from an
// already-validated, already-in-memory buffer BEFORE calling
// applyAcquisition, so a mismatch is detected and reported without ever
// writing the new bytes over an existing canonical raw file or lock entry):
//   - unknown sourceId              -> 'new': writes raw file + lock entry.
//   - existing sourceId, same sha256   -> 'identical': writes nothing (no
//     fetchedAt/provenance-field refresh either -- reproducing the same
//     bytes is not new information).
//   - existing sourceId, different sha256 -> 'mismatch': writes nothing and
//     throws, naming the sourceId and both SHA-256 values. Updating a lock
//     to a genuinely new upstream binary is a deliberate, reviewable action
//     this module does not perform automatically.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

export function sha256(buffer) {
  return crypto.createHash('sha256').update(buffer).digest('hex');
}

function ensureDir(p) {
  fs.mkdirSync(p, { recursive: true });
}

export function loadLock(lockPath) {
  if (!fs.existsSync(lockPath)) return { schemaVersion: 1, sources: [] };
  return JSON.parse(fs.readFileSync(lockPath, 'utf8'));
}

export function writeLock(lockPath, lock) {
  fs.writeFileSync(lockPath, JSON.stringify(lock, null, 2) + '\n', 'utf8');
}

// Pure decision function: given the current lock and a freshly-fetched
// sourceId/sha256 pair, decide what MAY be written, without touching the
// filesystem.
export function decideLockAction(lock, sourceId, newSha256) {
  const existingIndex = lock.sources.findIndex((s) => s.sourceId === sourceId);
  if (existingIndex < 0) return { action: 'new', existingIndex: -1, existing: null };
  const existing = lock.sources[existingIndex];
  if (existing.sha256 === newSha256) return { action: 'identical', existingIndex, existing };
  return { action: 'mismatch', existingIndex, existing };
}

// Applies decideLockAction()'s decision to the filesystem.
//   - 'new'       -> writes the raw file and appends a new lock entry.
//   - 'identical' -> writes nothing; the existing lock entry and raw file are
//                    left exactly as they were.
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
      `deliberate, reviewable decision this tool does not make automatically -- re-lock manually ` +
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
