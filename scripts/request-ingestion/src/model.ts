// Proposed V2 upstream request-ingestion contracts.
// The PoC runtime is dependency-free JS (ingest.mjs); these interfaces are the intended TS migration target.

export type ParseStatus = 'parsed' | 'unparsed' | 'orphan';
export type Confidence = 'high' | 'medium' | 'low';

export interface SourceEvidence {
  page: number;
  line: number;
}

export interface RequestStagingRecord {
  schemaVersion: 1;
  sourceDocumentId: string;
  sourcePage: number;
  sourceLine: number;
  rawText: string;
  recordKind: 'group' | 'system' | 'component' | 'expense' | 'policy_request' | 'unparsed';
  parseStatus: ParseStatus;
  label?: string;
  code?: string;
  groupLabel?: string | null;
  systemLabel?: string | null;
  componentLabel?: string | null;
  ministryHint?: string | null;
  rawAmountsThousandYen?: {
    previousThousandYen: number;
    requestThousandYen: number;
    deltaThousandYen: number;
  } | null;
}

export interface RequestSystemRecord {
  schemaVersion: 1;
  recordType: 'request_system';
  requestYear: number;
  fiscalYear: number;
  requestType: 'normal';
  sourceDocumentId: string;
  budgetItem: string;
  groupCode: string | null;
  groupLabel: string | null;
  systemCode: string;
  systemLabel: string;
  ministryHint: string | null;
  ministryHintMethod: 'system_label' | 'unknown';
  amountResolution: 'system_header' | 'component_sum' | 'expense_sum';
  previousYen: number;
  requestYen: number;
  deltaYen: number;
  sourceEvidence: SourceEvidence[];
  confidence: Confidence;
}

export interface RequestScopeRecord {
  schemaVersion: 1;
  recordType: 'request_scope';
  requestYear: number;
  fiscalYear: number;
  requestType: 'important_policy';
  sourceDocumentId: string;
  budgetItem: string;
  scopeKind: 'digital_agency_systems' | 'joint_project_systems' | 'ministry_systems' | 'other';
  label: string;
  requestYen: number;
  sourceEvidence: SourceEvidence[];
  confidence: Confidence;
}
