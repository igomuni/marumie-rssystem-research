#!/usr/bin/env node
// Orchestrator: runs each registered engine adapter for a case, normalizes,
// evaluates, and writes a compact evidence file + Markdown report.
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { ROOT, EVIDENCE_DIR, REPORTS_DIR, writeJson, ensureDir } from './common.mjs';
import { normalize } from './normalize.mjs';
import { normalizeDocling } from './normalize-docling.mjs';
import { evaluate } from './evaluate.mjs';

const ADAPTERS_DIR = path.join(ROOT, 'scripts', 'document-understanding', 'adapters');

function venvPythonAdapter(dirName, scriptName, setupHint) {
  return function run(caseId) {
    const dir = path.join(ADAPTERS_DIR, dirName);
    const venvPython = path.join(dir, '.venv', 'bin', 'python3');
    if (!fs.existsSync(venvPython)) {
      console.log(`SKIP ${dirName}: .venv not found. Set up with:\n${setupHint}`);
      return false;
    }
    const r = spawnSync(venvPython, [scriptName, caseId], { cwd: dir, stdio: 'inherit' });
    if (r.status !== 0) throw new Error(`${dirName} adapter failed (exit ${r.status})`);
    return true;
  };
}

const ENGINES = [
  {
    engine: 'pdfjs-baseline',
    normalize,
    run(caseId) {
      const r = spawnSync('node', ['src/run.mjs', caseId], {
        cwd: path.join(ADAPTERS_DIR, 'pdfjs-baseline'),
        stdio: 'inherit',
      });
      if (r.status !== 0) throw new Error(`pdfjs-baseline adapter failed (exit ${r.status})`);
    },
  },
  {
    engine: 'pymupdf-baseline',
    normalize,
    run: venvPythonAdapter(
      'pymupdf-baseline',
      'src/run.py',
      '  cd scripts/document-understanding/adapters/pymupdf-baseline\n' +
      '  python3 -m venv .venv && ./.venv/bin/pip install -r requirements.txt'
    ),
  },
  {
    engine: 'docling',
    // Docling's raw artifact is table-cell structured, not flat text lines,
    // so it uses its own normalizer (normalize-docling.mjs) rather than the
    // shared regex-over-lines one. evaluate.mjs is unchanged either way: it
    // only consumes the common { result, candidates } shape both normalizers
    // produce.
    normalize: (caseId) => normalizeDocling(caseId),
    run: venvPythonAdapter(
      'docling',
      'src/run.py',
      '  cd scripts/document-understanding/adapters/docling\n' +
      '  python3 -m venv .venv && ./.venv/bin/pip install -r requirements.txt'
    ),
  },
];

function renderReport(caseId, evaluations) {
  const lines = [];
  lines.push(`# Document Understanding Benchmark — ${caseId}`);
  lines.push('');
  lines.push(`Generated: ${new Date().toISOString()}`);
  lines.push('');
  lines.push('| engine | passed | failed | total |');
  lines.push('|---|---|---|---|');
  for (const e of evaluations) {
    lines.push(`| ${e.engine} (${e.engineVersion}) | ${e.summary.passed} | ${e.summary.failed} | ${e.summary.total} |`);
  }
  lines.push('');
  lines.push('The score alone is not the main result — see which *specific* checks differ below.');
  lines.push('');

  // Compact cross-engine comparison matrix: one row per check id (in the
  // order the first engine reports them), one column per engine. This is
  // meant to be scanned for *which capability* differs, not just tallied.
  if (evaluations.length > 0) {
    const checkIds = evaluations[0].checks.map(c => c.id);
    lines.push('## Comparison matrix');
    lines.push('');
    lines.push(`| check | ${evaluations.map(e => e.engine).join(' | ')} |`);
    lines.push(`|---|${evaluations.map(() => '---').join('|')}|`);
    for (const id of checkIds) {
      const cells = evaluations.map(e => {
        const c = e.checks.find(x => x.id === id);
        return c ? (c.pass ? 'PASS' : 'FAIL') : 'n/a';
      });
      lines.push(`| ${id} | ${cells.join(' | ')} |`);
    }
    lines.push('');
  }

  for (const e of evaluations) {
    lines.push(`## ${e.engine}`);
    lines.push('');
    lines.push('| check | pass | actual | expected | note |');
    lines.push('|---|---|---|---|---|');
    for (const c of e.checks) {
      const actual = JSON.stringify(c.actual);
      const expected = JSON.stringify(c.expected);
      lines.push(`| ${c.id} | ${c.pass ? 'PASS' : 'FAIL'} | \`${actual}\` | \`${expected}\` | ${c.note ?? ''} |`);
    }
    lines.push('');
  }
  return lines.join('\n') + '\n';
}

function main(caseId) {
  const ran = [];
  for (const adapter of ENGINES) {
    const didRun = adapter.run(caseId);
    if (didRun !== false) ran.push(adapter);
  }

  const evaluations = [];
  for (const adapter of ran) {
    adapter.normalize(caseId, adapter.engine);
    evaluations.push(evaluate(caseId, adapter.engine));
  }

  ensureDir(EVIDENCE_DIR);
  writeJson(path.join(EVIDENCE_DIR, `${caseId}-results.json`), {
    schemaVersion: 1,
    caseId,
    generatedAt: new Date().toISOString(),
    evaluations,
  });

  ensureDir(REPORTS_DIR);
  fs.writeFileSync(path.join(REPORTS_DIR, `${caseId}-evaluation.md`), renderReport(caseId, evaluations), 'utf8');

  console.log('\n=== Summary ===');
  for (const e of evaluations) {
    console.log(`${e.engine}: ${e.summary.passed}/${e.summary.total} checks passed`);
  }
}

const [, , caseIdArg = 'case-001'] = process.argv;
main(caseIdArg);
