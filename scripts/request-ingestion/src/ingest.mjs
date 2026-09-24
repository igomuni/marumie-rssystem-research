#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const FIXTURES = path.join(ROOT, 'fixtures');
const OUT = path.join(ROOT, 'out');
const manifest = JSON.parse(fs.readFileSync(path.join(ROOT, 'source_manifest.json'), 'utf8'));

function ensureDir(p) { fs.mkdirSync(p, { recursive: true }); }
function sha256(text) { return crypto.createHash('sha256').update(text).digest('hex'); }
function parseNumber(s) { return Number(s.replaceAll(',', '')); }

function parseTaggedLines(text) {
  return text.split(/\r?\n/)
    .filter(line => line.trim() && !line.trim().startsWith('#'))
    .map(line => {
      const m = line.match(/^L(\d+)@P(\d+):\s*(.*)$/);
      if (!m) throw new Error(`Unrecognized fixture line: ${line}`);
      return { sourceLine: Number(m[1]), sourcePage: Number(m[2]), text: m[3] };
    });
}

function splitTrailingTriple(text) {
  const m = text.match(/^(.*?)(?:\s+)([0-9][0-9,]*)(?:\s+)([0-9][0-9,]*)(?:\s+)([0-9][0-9,]*)$/);
  if (!m) return { label: text.trim(), amounts: null };
  return {
    label: m[1].trim(),
    amounts: {
      previousThousandYen: parseNumber(m[2]),
      requestThousandYen: parseNumber(m[3]),
      deltaThousandYen: parseNumber(m[4]),
    }
  };
}

function ministryFromSystemLabel(label) {
  const exactMap = new Map([
    ['内閣官房システム', '内閣官房'],
    ['内閣本府システム', '内閣府'],
    ['金融庁システム', '金融庁'],
    ['警察庁システム', '警察庁'],
    ['会計検査院システム', '会計検査院'],
    ['内閣法制局システム', '内閣法制局'],
    ['人事院システム', '人事院'],
    ['宮内庁システム', '宮内庁'],
    ['公正取引委員会システム', '公正取引委員会'],
    ['個人情報保護委員会システム', '個人情報保護委員会'],
    ['消費者庁システム', '消費者庁'],
  ]);
  if (exactMap.has(label)) return exactMap.get(label);
  const m = label.match(/^(.+省)システム$/);
  if (m) return m[1];
  const agency = label.match(/^(.+庁)システム$/);
  if (agency) return agency[1];
  return null;
}

function moneyToYen(amounts) {
  if (!amounts) return null;
  return {
    previousYen: amounts.previousThousandYen * 1000,
    requestYen: amounts.requestThousandYen * 1000,
    deltaYen: amounts.deltaThousandYen * 1000,
  };
}

function ingestNormalRequest(text, sourceMeta) {
  const lines = parseTaggedLines(text);
  const staging = [];
  const systems = [];
  let currentGroup = null;
  let currentSystem = null;
  let currentComponent = null;

  for (const line of lines) {
    const raw = line.text.trim();
    const coded = raw.match(/^(\d{3})\s+(.+)$/);

    if (coded) {
      const code = coded[1];
      const rest = splitTrailingTriple(coded[2]);
      const label = rest.label;

      if (label.includes('係')) {
        currentGroup = { code, label, amounts: rest.amounts, ...line };
        currentSystem = null;
        currentComponent = null;
        staging.push({
          schemaVersion: 1,
          sourceDocumentId: sourceMeta.sourceDocumentId,
          ...line,
          recordKind: 'group',
          code,
          rawText: raw,
          label,
          rawAmountsThousandYen: rest.amounts,
          parseStatus: 'parsed',
        });
        continue;
      }

      if (label.includes('システム')) {
        currentSystem = {
          systemLocalId: `${sourceMeta.sourceDocumentId}:P${line.sourcePage}:L${line.sourceLine}`,
          code,
          label,
          headerAmounts: rest.amounts,
          group: currentGroup,
          components: [],
          expenses: [],
          evidence: [line],
        };
        systems.push(currentSystem);
        currentComponent = null;
        staging.push({
          schemaVersion: 1,
          sourceDocumentId: sourceMeta.sourceDocumentId,
          ...line,
          recordKind: 'system',
          code,
          rawText: raw,
          label,
          groupCode: currentGroup?.code ?? null,
          groupLabel: currentGroup?.label ?? null,
          ministryHint: ministryFromSystemLabel(label),
          rawAmountsThousandYen: rest.amounts,
          parseStatus: 'parsed',
        });
        continue;
      }
    }

    const component = raw.match(/^(01|05)\s+(通常分|特殊要因分)(?:\s+(.*))?$/);
    if (component) {
      const tail = component[3] ?? '';
      const tripleOnly = tail.match(/^([0-9][0-9,]*)\s+([0-9][0-9,]*)\s+([0-9][0-9,]*)$/);
      const rest = tripleOnly ? { label: '', amounts: { previousThousandYen: parseNumber(tripleOnly[1]), requestThousandYen: parseNumber(tripleOnly[2]), deltaThousandYen: parseNumber(tripleOnly[3]) } } : splitTrailingTriple(tail);
      currentComponent = {
        code: component[1],
        label: component[2],
        amounts: rest.amounts,
        expenses: [],
        evidence: [line],
      };
      if (currentSystem) {
        currentSystem.components.push(currentComponent);
        currentSystem.evidence.push(line);
      }
      staging.push({
        schemaVersion: 1,
        sourceDocumentId: sourceMeta.sourceDocumentId,
        ...line,
        recordKind: 'component',
        code: component[1],
        rawText: raw,
        label: component[2],
        groupLabel: currentGroup?.label ?? null,
        systemLabel: currentSystem?.label ?? null,
        rawAmountsThousandYen: rest.amounts,
        parseStatus: currentSystem ? 'parsed' : 'orphan',
      });
      continue;
    }

    const expense = raw.match(/^(\d{5}-[0-9-]+)\s+(.+?)\s+([0-9][0-9,]*)\s+([0-9][0-9,]*)\s+([0-9][0-9,]*)$/);
    if (expense) {
      const amounts = {
        previousThousandYen: parseNumber(expense[3]),
        requestThousandYen: parseNumber(expense[4]),
        deltaThousandYen: parseNumber(expense[5]),
      };
      const e = { code: expense[1], label: expense[2].trim(), amounts, ...line };
      if (currentSystem) {
        currentSystem.expenses.push(e);
        currentSystem.evidence.push(line);
      }
      if (currentComponent) currentComponent.expenses.push(e);
      staging.push({
        schemaVersion: 1,
        sourceDocumentId: sourceMeta.sourceDocumentId,
        ...line,
        recordKind: 'expense',
        code: expense[1],
        rawText: raw,
        label: expense[2].trim(),
        groupLabel: currentGroup?.label ?? null,
        systemLabel: currentSystem?.label ?? null,
        componentLabel: currentComponent?.label ?? null,
        rawAmountsThousandYen: amounts,
        parseStatus: currentSystem ? 'parsed' : 'orphan',
      });
      continue;
    }

    staging.push({
      schemaVersion: 1,
      sourceDocumentId: sourceMeta.sourceDocumentId,
      ...line,
      recordKind: 'unparsed',
      rawText: raw,
      groupLabel: currentGroup?.label ?? null,
      systemLabel: currentSystem?.label ?? null,
      parseStatus: 'unparsed',
    });
  }

  const normalized = systems.map(s => {
    const componentAmounts = s.components.filter(c => c.amounts);
    const expenseSum = s.expenses.reduce((acc, e) => {
      acc.previousThousandYen += e.amounts.previousThousandYen;
      acc.requestThousandYen += e.amounts.requestThousandYen;
      acc.deltaThousandYen += e.amounts.deltaThousandYen;
      return acc;
    }, { previousThousandYen: 0, requestThousandYen: 0, deltaThousandYen: 0 });

    const componentSum = componentAmounts.reduce((acc, c) => {
      acc.previousThousandYen += c.amounts.previousThousandYen;
      acc.requestThousandYen += c.amounts.requestThousandYen;
      acc.deltaThousandYen += c.amounts.deltaThousandYen;
      return acc;
    }, { previousThousandYen: 0, requestThousandYen: 0, deltaThousandYen: 0 });

    let chosen;
    let amountResolution;
    if (s.headerAmounts) {
      chosen = s.headerAmounts;
      amountResolution = 'system_header';
    } else if (componentAmounts.length > 0) {
      chosen = componentSum;
      amountResolution = 'component_sum';
    } else {
      chosen = expenseSum;
      amountResolution = 'expense_sum';
    }

    const m = moneyToYen(chosen);
    return {
      schemaVersion: 1,
      recordType: 'request_system',
      requestYear: sourceMeta.requestPublishedYear,
      fiscalYear: manifest.fiscalYear,
      requestType: 'normal',
      sourceDocumentId: sourceMeta.sourceDocumentId,
      budgetItem: sourceMeta.targetBudgetItem,
      groupCode: s.group?.code ?? null,
      groupLabel: s.group?.label ?? null,
      systemCode: s.code,
      systemLabel: s.label,
      ministryHint: ministryFromSystemLabel(s.label),
      ministryHintMethod: ministryFromSystemLabel(s.label) ? 'system_label' : 'unknown',
      amountResolution,
      ...m,
      sourceEvidence: s.evidence.map(e => ({ page: e.sourcePage, line: e.sourceLine })),
      confidence: ministryFromSystemLabel(s.label) && m ? 'high' : 'medium',
    };
  });

  return { staging, normalized, systems };
}

function policyScope(label) {
  if (label === 'デジタル庁システム等') return 'digital_agency_systems';
  if (label === 'デジタル庁・各府省共同プロジェクト型システム') return 'joint_project_systems';
  if (label === '各府省システム') return 'ministry_systems';
  return 'other';
}

function ingestPolicy(text, sourceMeta) {
  const lines = parseTaggedLines(text);
  const staging = [];
  const normalized = [];
  for (const line of lines) {
    const m = line.text.match(/^(.*?)\s+([0-9][0-9,]*)$/);
    if (!m) {
      staging.push({ schemaVersion: 1, sourceDocumentId: sourceMeta.sourceDocumentId, ...line, recordKind: 'unparsed', rawText: line.text, parseStatus: 'unparsed' });
      continue;
    }
    const label = m[1].trim();
    const amountThousandYen = parseNumber(m[2]);
    const scopeKind = policyScope(label);
    staging.push({
      schemaVersion: 1,
      sourceDocumentId: sourceMeta.sourceDocumentId,
      ...line,
      recordKind: 'policy_request',
      rawText: line.text,
      label,
      scopeKind,
      requestAmountThousandYen: amountThousandYen,
      parseStatus: 'parsed',
    });
    normalized.push({
      schemaVersion: 1,
      recordType: 'request_scope',
      requestYear: sourceMeta.requestPublishedYear,
      fiscalYear: manifest.fiscalYear,
      requestType: 'important_policy',
      sourceDocumentId: sourceMeta.sourceDocumentId,
      budgetItem: '情報通信技術調達等適正・効率化推進費',
      scopeKind,
      label,
      requestYen: amountThousandYen * 1000,
      sourceEvidence: [{ page: line.sourcePage, line: line.sourceLine }],
      confidence: 'high',
    });
  }
  return { staging, normalized };
}

function writeJsonl(file, rows) {
  fs.writeFileSync(file, rows.map(r => JSON.stringify(r)).join('\n') + '\n', 'utf8');
}

function csvCell(v) {
  const s = v == null ? '' : String(v);
  return /[",\n]/.test(s) ? `"${s.replaceAll('"', '""')}"` : s;
}
function writeCsv(file, headers, rows) {
  const lines = [headers.join(','), ...rows.map(r => headers.map(h => csvCell(r[h])).join(','))];
  fs.writeFileSync(file, lines.join('\n') + '\n', 'utf8');
}

function validate(normalResult, policyResult, normalMeta, policyMeta) {
  const checks = [];
  const add = (id, ok, actual, expected, note = '') => checks.push({ id, ok, actual, expected, note });

  const policySystemThousand = policyResult.normalized
    .filter(r => ['digital_agency_systems', 'joint_project_systems', 'ministry_systems'].includes(r.scopeKind))
    .reduce((s, r) => s + r.requestYen / 1000, 0);
  add('policy_system_related_total', policySystemThousand === policyMeta.expectedSystemRelatedRequestAmountThousandYen,
      policySystemThousand, policyMeta.expectedSystemRelatedRequestAmountThousandYen,
      '3 system-related important-policy rows');

  const combined = normalMeta.expectedItemRequestAmountThousandYen + policySystemThousand;
  add('combined_request_total', combined === 567039954, combined, 567039954,
      'normal request + system-related important-policy request');

  const finance = normalResult.normalized.find(r => r.systemLabel === '財務省システム');
  add('finance_header_amount', finance?.requestYen === 102935743000, finance?.requestYen ?? null, 102935743000,
      'system-header amount');

  const financeState = normalResult.systems.find(s => s.label === '財務省システム');
  const financeExpenseSum = financeState?.expenses.reduce((s, e) => s + e.amounts.requestThousandYen, 0) ?? null;
  add('finance_expense_sum_reconciles', financeExpenseSum === 102935743, financeExpenseSum, 102935743,
      'normal + special-factor expense rows reconcile to system header');

  const cross = normalResult.normalized.find(r => r.groupLabel === '厚生労働第１係' && r.systemLabel === '総務省システム');
  add('group_is_not_ministry', cross?.ministryHint === '総務省', cross?.ministryHint ?? null, '総務省',
      'ministry is inferred from system label, not the surrounding 係');

  const mhlw2 = normalResult.normalized.find(r => r.groupLabel === '厚生労働第２係' && r.systemLabel === '厚生労働省システム');
  add('component_sum_resolution', mhlw2?.requestYen === 7738305000 && mhlw2?.amountResolution === 'component_sum',
      { requestYen: mhlw2?.requestYen ?? null, resolution: mhlw2?.amountResolution ?? null },
      { requestYen: 7738305000, resolution: 'component_sum' },
      'component header is preferred over detailed expense sum to avoid double counting');

  const parsed = normalResult.staging.filter(r => r.parseStatus === 'parsed').length + policyResult.staging.filter(r => r.parseStatus === 'parsed').length;
  const total = normalResult.staging.length + policyResult.staging.length;

  return {
    schemaVersion: 1,
    generatedAt: new Date().toISOString(),
    status: checks.every(c => c.ok) ? 'pass' : 'fail',
    fixtureCoverage: {
      normalRequest: normalMeta.fixtureCoverage,
      importantPolicy: policyMeta.fixtureCoverage,
      parsedRows: parsed,
      totalRows: total,
      parsedRate: total ? parsed / total : 0,
    },
    knownTotals: {
      normalRequestThousandYen: normalMeta.expectedItemRequestAmountThousandYen,
      importantPolicySystemRelatedThousandYen: policyMeta.expectedSystemRelatedRequestAmountThousandYen,
      combinedThousandYen: 567039954,
    },
    checks,
    limitations: [
      'The normal-request fixture is intentionally partial and does not prove full-document system-level reconciliation.',
      'The PoC starts after text extraction; production should add source download, file hashing, and PDF/Excel extraction adapters.',
      'System Entity identity across fiscal/review years is not resolved in this PoC.',
      'No fuzzy matching is performed; ambiguous/unparsed rows remain explicit.',
    ]
  };
}

function main() {
  ensureDir(OUT);
  const normalMeta = manifest.sources.find(s => s.adapter === 'digital-r6-request');
  const policyMeta = manifest.sources.find(s => s.adapter === 'digital-r6-policy');
  normalMeta.requestPublishedYear = manifest.requestPublishedYear;
  policyMeta.requestPublishedYear = manifest.requestPublishedYear;

  const normalText = fs.readFileSync(path.join(FIXTURES, 'digital_r6_normal_extract.txt'), 'utf8');
  const policyText = fs.readFileSync(path.join(FIXTURES, 'digital_r6_policy_extract.txt'), 'utf8');

  const normal = ingestNormalRequest(normalText, normalMeta);
  const policy = ingestPolicy(policyText, policyMeta);

  const staging = [...normal.staging, ...policy.staging];
  const normalized = [...normal.normalized, ...policy.normalized];
  const validation = validate(normal, policy, normalMeta, policyMeta);

  writeJsonl(path.join(OUT, 'staging.jsonl'), staging);
  writeJsonl(path.join(OUT, 'request-normalized.jsonl'), normalized);
  fs.writeFileSync(path.join(OUT, 'validation.json'), JSON.stringify(validation, null, 2) + '\n');

  writeCsv(path.join(OUT, 'systems.csv'),
    ['requestType','groupLabel','systemLabel','ministryHint','amountResolution','requestYen','confidence','sourceDocumentId'],
    normal.normalized);

  writeCsv(path.join(OUT, 'request-scopes.csv'),
    ['requestType','scopeKind','label','requestYen','confidence','sourceDocumentId'],
    policy.normalized);

  const runManifest = {
    schemaVersion: 1,
    generatedAt: validation.generatedAt,
    inputHashes: {
      normalFixtureSha256: sha256(normalText),
      policyFixtureSha256: sha256(policyText),
      sourceManifestSha256: sha256(JSON.stringify(manifest)),
    },
    counts: {
      stagingRecords: staging.length,
      normalizedRecords: normalized.length,
      systemRecords: normal.normalized.length,
      scopeRecords: policy.normalized.length,
    },
    validationStatus: validation.status,
  };
  fs.writeFileSync(path.join(OUT, 'run-manifest.json'), JSON.stringify(runManifest, null, 2) + '\n');

  console.log(JSON.stringify({ outDir: OUT, ...runManifest.counts, validationStatus: validation.status }, null, 2));
  if (validation.status !== 'pass') process.exitCode = 1;
}

main();
