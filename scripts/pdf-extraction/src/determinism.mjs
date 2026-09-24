#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { OUTPUT_DIR, sha256 } from './common.mjs';

function cleanOutput() {
  fs.rmSync(OUTPUT_DIR, { recursive: true, force: true });
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

function runExtract() {
  const r = spawnSync(process.execPath, [path.join(path.dirname(new URL(import.meta.url).pathname), 'extract.mjs')], {
    stdio: 'inherit',
  });
  if (r.status !== 0) process.exit(r.status ?? 1);
}

function snapshot() {
  const files = fs.readdirSync(OUTPUT_DIR)
    .filter(name => fs.statSync(path.join(OUTPUT_DIR, name)).isFile())
    .sort();
  return Object.fromEntries(files.map(name => [
    name,
    sha256(fs.readFileSync(path.join(OUTPUT_DIR, name))),
  ]));
}

cleanOutput();
runExtract();
const first = snapshot();

cleanOutput();
runExtract();
const second = snapshot();

if (JSON.stringify(first) !== JSON.stringify(second)) {
  console.error('determinism FAIL');
  console.error('run1', JSON.stringify(first, null, 2));
  console.error('run2', JSON.stringify(second, null, 2));
  process.exit(1);
}

console.log('determinism PASS');
for (const [name, hash] of Object.entries(second)) {
  console.log(`${hash}  ${name}`);
}
