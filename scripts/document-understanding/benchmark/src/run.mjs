#!/usr/bin/env node
// Orchestrator: runs each registered engine adapter for a case, normalizes,
// evaluates, and writes a compact evidence file + Markdown report.
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { ROOT, EVIDENCE_DIR, REPORTS_DIR, writeJson, ensureDir } from './common.mjs';
import { normalize } from './normalize.mjs';
import { evaluate } from './evaluate.mjs';

const ADAPTERS_DIR = path.join(ROOT, 'scripts', 'document-understanding', 'adapters');

const ENGINES = [
  {
    engine: 'pdfjs-baseline',
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
    run(caseId) {
      const dir = path.join(ADAPTERS_DIR, 'pymupdf-baseline');
      const venvPython = path.join(dir, '.venv', 'bin', 'python3');
      const python = fs.existsSync(venvPython) ? venvPython : null;
      if (!python) {
        console.log(
          'SKIP pymupdf-baseline: .venv not found. Set up with:\n' +
          '  cd scripts/document-understanding/adapters/pymupdf-baseline\n' +
          '  python3 -m venv .venv && ./.venv/bin/pip install -r requirements.txt'
        );
        return false;
      }
      const r = spawnSync(python, ['src/run.py', caseId], { cwd: dir, stdio: 'inherit' });
      if (r.status !== 0) throw new Error(`pymupdf-baseline adapter failed (exit ${r.status})`);
      return true;
    },
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
    if (didRun !== false) ran.push(adapter.engine);
  }

  const evaluations = [];
  for (const engine of ran) {
    normalize(caseId, engine);
    evaluations.push(evaluate(caseId, engine));
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
