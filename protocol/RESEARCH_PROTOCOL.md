# Research Protocol

## Purpose

This protocol defines how research for the `marumie-rssystem` project is conducted, recorded, and handed off between sessions so that work is reproducible and does not depend on chat history.

### Research Phase vs. Workspace Phase

Two separate phase-numbering systems exist in this repository, and they must not be conflated:

- **Research Phase** — a substantive investigation phase in the FY2024 Digital Agency / MOF / RS study. Currently completed through Phase 15. See `state/RESEARCH_SUMMARY.md`. Historical research phases are not renumbered.
- **Workspace Phase** — repository/reproducibility bootstrap work on this research workspace itself (e.g. `0`, `1A`, `1B`, ...). Tracked informally in `state/CHANGELOG.md` and, where useful, as a `workspacePhase` field in `state/CURRENT_STATE.json`.

`state/CURRENT_STATE.json`'s `lastCompletedPhase` field refers to the Research Phase, not the Workspace Phase.

## Canonical State

- Files committed to this repository are the canonical project state.
- `state/CURRENT_STATE.json` reflects the current phase and next action.
- GitHub/main will eventually represent validated checkpoints.

## Source Provenance

- Every primary source used in research must be recorded in `sources/source-registry.csv`.
- Record URL, checksum (sha256), fetch timestamp, and a persistent storage reference for each source.
- `/mnt/data`, temporary VM directories, and local scratch files are not canonical persistent storage.

## Evidence Levels

- Primary-source evidence should be preferred over secondary summaries.
- Distinguish primary sources, secondary summaries, and derived interpretations explicitly in reports.

## Derived Data

- Keep factual source data separate from derived interpretations.
- Derived outputs must identify their upstream source/evidence where practical.
- Store derived data under `derived/`.

## Uncertainty

- Never silently convert an unknown value into zero.
- Preserve fiscal year, accounting stage, funding route, and scope for every figure.
- Do not use amount similarity alone as linkage evidence.

## Rejected Hypotheses

- Record rejected hypotheses in `protocol/DECISIONS.md` or a dedicated log when they may prevent future repeated mistakes.

## Phase Lifecycle

- Research proceeds in discrete phases.
- Each phase should produce a reproducible checkpoint (evidence, report, or snapshot) before moving to the next.

## Handoff Requirements

- At the end of a phase, update `state/CURRENT_STATE.json`, `state/CHANGELOG.md`, and `state/TODO.md`.

## Git / Commit Policy

- AI sessions may prepare, validate, commit, and push workspace changes when the user has explicitly authorized commit/push for the task or workflow.
- Before committing, validation and repository safety checks must pass.
- Never force-push or rewrite validated history unless explicitly requested.
- If validation fails or unexpected files/secrets are present, do not commit or push.
- GitHub/main represents the canonical validated checkpoint after a successful push.

---

## Validated Invariants (imported from FY2024 Digital Agency / MOF / RS investigation)

These rules were established through the completed FY2024 IT-budget investigation and are durable methodological constraints for all future research in this repository.

### Budget lifecycle invariants

```text
request != enacted_budget != settlement
```

Amounts from one stage must not be silently reused for another stage.

```text
supplemental evidence != initial request evidence
final budget != request
execution != request
```

A later-stage value may be used only as validation evidence unless there is direct same-stage evidence.

### Scope invariants

```text
same fiscal year alone is insufficient
```

Any numeric linkage must preserve, where relevant:

- fiscal year
- budget/request stage
- accounting scope
- funding route
- beneficiary scope
- system/project identity
- source precision

```text
general account != special account != mixed scope
```

Use at least the following conceptual account scopes: `general`, `special`, `mixed`, `unknown`.

### Linkage invariants

```text
amount proximity != evidence
same number alone != linkage evidence
```

An amount match may validate an already-established linkage, but must not select the target by itself.

```text
coefficient heading != beneficiary
```

A MOF coefficient / 係 heading cannot automatically be interpreted as the ministry, bureau, project, or system beneficiary.

```text
beneficiary total != category allocation
```

A ministry-level total cannot automatically be assigned to one system category.

```text
semantic domain != numeric allocation
```

Organizational or topical similarity may narrow candidates but does not authorize numeric allocation.

### Missing / zero invariants

```text
no explicit label found != zero
unknown != zero
blank != explicit zero
```

The research model must distinguish at least conceptually between: `normal`, `explicit_zero`, `unallocated`, `parent_item_only`, `unknown`.

Do not convert blank or unresolved values to zero.

### Parent / child invariants

```text
parent Budget Container + child ReviewProject must not be summed blindly
```

The FY2024 Digital Agency IT-budget case demonstrated near-complete economic overlap between the parent project and child projects.

```text
ReviewProject ID is not a permanent System Entity ID
```

Review topology may change across years.

```text
later ReviewProject split != historical project structure
```

Do not backcast later independent Review Projects into earlier fiscal years without direct evidence.

### Transfer / payment-flow invariants

```text
RS 5-1 is a flow graph, not an accounting total
```

It may contain: transfer, expenditure delegation, direct payment, subcontract, subsidy, grant, special-account blocks.

Do not sum graph blocks mechanically. Do not infer transfer only from block position. Classification must use explicit role / contract / transfer wording where possible.

### Source / provenance rules

Every source-derived record should preserve, where practical:

```text
sourceDocumentId
sourceUrl
sourceSha256
sourcePage
sourceLocator
rawText
sourcePrecision
transformRuleId
confidence
```

Primary source should be preferred over summary documents. Derived data must remain distinguishable from direct observations.

A derived value should record, where relevant: `isDerived`, `sourceResolution`, `derivationRule`.

### Reproducibility rules

```text
raw primary source
-> extraction
-> staging
-> normalization
-> transformation / reconciliation
-> validation
-> evidence
-> report
```

Each phase should preserve enough information to reconstruct this chain.

- `/mnt/data` is scratch space.
- Chat history is not canonical.
- GitHub/main is the intended canonical validated state.
- AI sessions may commit/push directly once authorized for the task, per the Git / Commit Policy above.

```text
same URL != same source binary
```

A government website may replace a document while keeping the same URL. Reproducible source identity requires the SHA-256 of the acquired binary, not the URL alone (see ADR-009 and `sources/source-lock.json`).

### Public repository policy

This repository is public.

- Only public-source research information may be committed.
- Never commit API keys, tokens, credentials, secrets, private business data, or personal information.
- Large raw government files should normally be referenced through URL/hash/manifest rather than committed.
- Review `git diff` before every commit.
