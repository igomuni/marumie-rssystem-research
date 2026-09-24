# Task: Initialize `marumie-rssystem-research`

You are working inside the already-created local folder:

`marumie-rssystem-research`

The purpose of this repository is to become the persistent, reproducible research workspace for long-running investigations related to the `marumie-rssystem` project.

This repository is separate from the application repository itself.

## Goal

Create the minimal research-workspace structure needed so that:

* a new ChatGPT / Claude / human session can resume research without relying on prior chat history
* research rules are persistent
* current research state is machine-readable
* source provenance can be tracked
* future research phases can produce reproducible checkpoints
* GitHub can act as the canonical persistent state
* the user remains responsible for Git commit / push

Do NOT yet migrate existing research artifacts.
Do NOT yet build the full PDF ingestion pipeline.
Do NOT modify any other repository.

---

# 1. Create repository structure

Create:

```text
marumie-rssystem-research/
├── START_HERE.md
├── README.md
├── .gitignore
├── protocol/
│   ├── RESEARCH_PROTOCOL.md
│   └── DECISIONS.md
├── state/
│   ├── CURRENT_STATE.json
│   ├── CHANGELOG.md
│   └── TODO.md
├── sources/
│   └── source-registry.csv
├── evidence/
├── reports/
├── scripts/
├── snapshots/
├── fixtures/
└── derived/
```

Use `.gitkeep` where necessary so empty directories are tracked.

---

# 2. `.gitignore`

Use a conservative ignore policy.

Ignore:

```text
.DS_Store

node_modules/
.npm/
dist/
.tmp/
.cache/

.env
.env.*
!.env.example

raw/
downloads/

*.zip
*.7z
*.tar
*.tar.gz

*.pdf
*.xlsx
*.xls

tmp/
work/

*.log
```

Important:

* Do not ignore CSV, JSON, Markdown, TypeScript, JavaScript, or manifest files.
* Large primary-source binaries will not normally be stored directly in Git.
* Their URL, checksum, acquisition metadata, and persistent storage reference will be stored instead.

---

# 3. `state/CURRENT_STATE.json`

Create valid JSON with this initial state:

```json
{
  "schemaVersion": 1,
  "project": "marumie-rssystem research",
  "status": "initializing",
  "lastCompletedPhase": 0,
  "currentTopic": "research workspace setup",
  "nextAction": "bootstrap existing research artifacts",
  "latestReport": null,
  "latestSnapshot": null,
  "unresolved": []
}
```

Do not add speculative fields yet unless clearly necessary.

---

# 4. `sources/source-registry.csv`

Create the header:

```csv
sourceId,title,url,mimeType,fiscalYear,documentStage,publisher,fetchedAt,sha256,localRef,notes
```

No data rows yet.

---

# 5. `START_HERE.md`

Keep this concise.

Its purpose is to tell a new AI/human session exactly how to resume the project.

Include approximately this process:

```text
1. Read protocol/RESEARCH_PROTOCOL.md
2. Read state/CURRENT_STATE.json
3. Read protocol/DECISIONS.md
4. Read state/TODO.md
5. Load only the evidence/reports/snapshots needed for current nextAction
6. Do not infer missing historical facts from chat memory
7. Maintain source provenance for new research
8. At the end of a research phase, update the handoff state
9. Do not commit or push unless the user explicitly performs/authorizes it
```

Also explicitly state:

> Chat history is not the canonical project state. Files in this repository are.

---

# 6. `protocol/RESEARCH_PROTOCOL.md`

For now create the framework, not the full historical rule set.

Include sections:

```text
# Research Protocol

## Purpose
## Canonical State
## Source Provenance
## Evidence Levels
## Derived Data
## Uncertainty
## Rejected Hypotheses
## Phase Lifecycle
## Handoff Requirements
## Git / Commit Policy
```

Add these baseline rules:

* Primary-source evidence should be preferred over secondary summaries.
* Never silently convert an unknown value into zero.
* Keep factual source data separate from derived interpretations.
* Preserve fiscal year, accounting stage, funding route, and scope.
* Do not use amount similarity alone as linkage evidence.
* Record rejected hypotheses when they may prevent future repeated mistakes.
* Derived outputs must identify their upstream source/evidence where practical.
* `/mnt/data`, temporary VM directories, and local scratch files are not canonical persistent storage.
* GitHub/main will eventually represent validated checkpoints.
* AI sessions prepare changes; the user performs commit/push.

Leave a clearly marked section:

```text
TODO: Import validated invariants from FY2024 IT budget investigation.
```

---

# 7. `protocol/DECISIONS.md`

Use an ADR-like format.

Create:

```text
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
```

Then add only one initial decision:

```text
ADR-001: Repository files are canonical, chat history is not
```

Decision:

* durable research state must be serialized into this repository
* chat conversations are execution contexts, not authoritative storage

Do not import all previous research decisions yet.

---

# 8. `state/TODO.md`

Create:

```text
# TODO

## Next

- Bootstrap existing FY2024 Digital Agency / MOF / RS research artifacts
- Import validated research invariants into RESEARCH_PROTOCOL.md
- Import durable decisions into DECISIONS.md
- Restore the existing request-ingestion PoC under scripts/
- Define a reproducible phase manifest schema
- Define handoff generation workflow
- Add source acquisition / SHA-256 workflow
- Add validation command
```

---

# 9. `state/CHANGELOG.md`

Initialize:

```text
# Research Workspace Changelog

## Unreleased

- Initialized research workspace structure.
```

---

# 10. `README.md`

Explain briefly:

* what this repository is
* relationship to `marumie-rssystem`
* why research is stored separately
* high-level directory structure
* GitHub is the intended canonical persistent store
* large raw government files should not normally be committed
* user controls commits/pushes

Keep README relatively short.

---

# 11. Validate

After creating everything:

1. Show the resulting directory tree.
2. Validate `CURRENT_STATE.json`.
3. Confirm `source-registry.csv` has the expected header.
4. Check `git status`.
5. Check for accidentally created large files.
6. Check for secrets.
7. Do NOT commit.
8. Do NOT push.

If Git is not initialized yet, initialize it and rename the default branch to `main`, but still do not commit.

---

# 12. Final response

Report:

* files created
* validation results
* `git status`
* anything unexpected
* recommended commit message

Recommended commit message:

```text
chore: initialize research workspace
```

Do not perform the commit.
