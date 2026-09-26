# Research Decisions

This file records durable research-method decisions.

## Decision template

### ADR-XXX: Title
Status:
Date:
Decision:
Reason:
Rejected alternatives:
Implications:

---

### ADR-001: Repository files are canonical, chat history is not
Status: Accepted
Date: 2026-09-25
Decision: Durable research state must be serialized into this repository. Chat conversations are execution contexts, not authoritative storage.
Reason: Chat history is not reliably available across sessions or tools, and cannot be verified or diffed. Files in version control can be.
Rejected alternatives: Relying on chat/session memory as the source of truth.
Implications: Every research phase must persist its state, evidence, and decisions to files before being considered complete.

---

### ADR-002: Amount similarity is not target-selection evidence
Status: Accepted
Date: 2026-09-25
Decision: Amounts may be used for post-link validation but not to select a linkage target.
Reason: Multiple projects, stages, and funding scopes may contain similar or identical amounts.
Rejected alternatives: Selecting the most likely linkage target by nearest/matching amount.
Implications: Any proposed linkage must first be established via non-amount evidence (identifiers, explicit references, provenance); amount match may then confirm it.

---

### ADR-003: Budget lifecycle stages remain separate
Status: Accepted
Date: 2026-09-25
Decision: Request, enacted budget, supplemental budget, settlement, and execution must remain separate evidence states.
Reason: Each stage reflects a distinct point in the budget lifecycle and conflating them produces false continuity between numbers that were never the same figure.
Rejected alternatives: Backfilling missing request amounts from later budget/execution figures.
Implications: Missing values at one stage stay missing; they are not inferred from another stage's figure.

---

### ADR-004: Unknown and zero are different states
Status: Accepted
Date: 2026-09-25
Decision: Blank, unresolved, unallocated, parent-only, and explicit zero must not be collapsed.
Reason: Silently converting unknown to zero destroys information and can materially distort totals and comparisons.
Rejected alternatives: Treating any missing/blank value as zero for simplicity.
Implications: Data models and reports must carry an explicit status field distinguishing these states rather than a bare numeric zero.

---

### ADR-005: ReviewProject is versioned, SystemEntity is conceptual
Status: Accepted
Date: 2026-09-25
Decision: RS ReviewProject IDs / yearly review topology cannot be treated as permanent system identity.
Reason: Review topology changes across years; a ReviewProject ID observed in one year's review is not guaranteed to denote the same scope in another year.
Rejected alternatives: Using ReviewProject ID as a stable primary key for a system/project across fiscal years.
Implications: A conceptual System Entity layer, separate from ReviewProject version, is needed for cross-year identity claims.

---

### ADR-006: Parent and child records are not additive by default
Status: Accepted
Date: 2026-09-25
Decision: A parent Budget Container and child ReviewProjects must not be summed without overlap analysis.
Reason: The FY2024 Digital Agency IT-budget case demonstrated near-complete economic overlap between the parent project and its child projects; naive summation double-counts.
Rejected alternatives: Summing parent and child totals directly to estimate combined scope.
Implications: Any aggregate figure spanning parent and child records must document its overlap-handling method.

---

### ADR-007: RS 5-1 is a flow graph
Status: Accepted
Date: 2026-09-25
Decision: Do not interpret RS 5-1 as a single accounting ledger or sum all blocks.
Reason: RS 5-1 mixes transfer, expenditure delegation, direct payment, subcontract, subsidy, grant, and special-account blocks; these are not commensurable as a single total, and block position alone does not indicate transfer relationships.
Rejected alternatives: Mechanically summing all RS 5-1 blocks as if they were line items in one ledger.
Implications: Classification of RS 5-1 entries must use explicit role/contract/transfer wording where possible, not position or aggregate summation.

---

### ADR-008: Public repository contains public research only
Status: Accepted
Date: 2026-09-25
Decision: The canonical GitHub repository remains public and must contain only public-source research material and reproducibility metadata.
Reason: The repository is publicly hosted; committing credentials, private business data, or personal information would be an unrecoverable disclosure.
Rejected alternatives: Making the repository private to allow less careful review before commits.
Implications: Every commit should be reviewed (`git diff`) for secrets/PII before it is made; large raw government files are referenced via URL/hash/manifest rather than committed directly.

---

### ADR-009: Source identity includes binary hash, not URL alone
Status: Accepted
Date: 2026-09-25
Decision: A URL identifies the retrieval location, not immutable content. Reproducible source identity requires the SHA-256 of the acquired binary, committed in `sources/source-lock.json`.
Reason: Government websites may replace a PDF while retaining the same URL (`same URL != same source binary`). Trusting the URL alone as a stable identifier would let a silent upstream content change invalidate prior research without detection.
Rejected alternatives: Treating the URL as sufficient source identity; silently re-locking to whatever the server currently returns whenever verification runs.
Implications: `npm run sources:verify` must fail loudly and exit non-zero on a hash mismatch rather than update the lock; updating a lock to a new binary requires an explicit, reviewable `npm run sources:lock` re-run, preserving the old hash in Git history.

---

### ADR-010: Layout-family adaptation is a distinct layer from generic/engine-specific normalization
Status: Accepted
Date: 2026-09-26
Decision: A parsing/normalization rule must be classified as one of: engine behavior, raw representation, generic normalization, engine-specific normalization, document-family/layout-specific interpretation, semantic interpretation, or evaluation — and rules that are actually document-family-specific must not be written as if they were generic or engine-specific.
Reason: Case-002 showed the same engine/normalizer code (`common.mjs`'s `splitTrailingTriple`) silently encoded a layout-specific assumption (amount triple anchored at line end) as if it were universal, while a genuinely engine-specific gap (missing CJK-wrap-space-closing) was conflated with it in the same file. Neither a single universal parser nor per-ministry parsers matches the observed failure boundary, which is layout/template family, not issuer identity.
Rejected alternatives: One universal normalizer for all documents; one parser per ministry.
Implications: Future normalization work must identify which layer a fix belongs to before writing it, and document-family-specific rules get their own extension point rather than being folded into generic or engine-specific code. Full design: `reports/document-understanding/20260926_1316_Case_Based_Document_Understanding_and_LLM_Strategy_Selection_Research_Architecture.md`.

---

### ADR-011: Document Profile features are classified by how they were actually discovered, not how they theoretically could be
Status: Accepted
Date: 2026-09-26
Decision: A Document Profile feature is source-safe (A) only if this repository actually established it before running any compared engine. A feature this repository only established by inspecting engine output must be recorded as engine-derived (B), even if a human could plausibly have observed the same fact by looking at the page image directly.
Reason: Backfilling `case-002`'s Case Package (`document-profile.json`) found a genuine boundary case: whether the annotation column sits on the same reconstructed line as the amount triple is plausibly a source-observable layout fact, but this repository's actual history only recorded it via the flat-text engines' raw output during the first frozen benchmark run (`reports/document-understanding/20260926_0923_Case002_First_Frozen_Benchmark_Run.md`). Classifying it as source-safe based on what was theoretically possible, rather than what was actually done, would silently misrepresent this Case Package's provenance and could leak an engine-informed fact into a future strategy-selection input believed to be pre-analysis.
Rejected alternatives: Classifying a feature as source-safe whenever it is plausibly re-derivable from the source alone, regardless of how it was actually discovered in this repository's history.
Implications: A Document Profile's `sourceSafeProfile` may only contain features with a `manually_observed` or `source_stated` provenance tag backed by evidence predating any engine run on that case; anything established via `derived_from_repository_analysis` of engine output stays in `engineDerivedProfile`, even where a future task could re-establish the same fact by source-only inspection and move it across.
