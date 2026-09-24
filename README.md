# marumie-rssystem-research

This repository is the persistent, reproducible research workspace for long-running investigations related to the `marumie-rssystem` project. It is separate from the application repository itself, so that research state, evidence, and provenance can evolve independently of application code and be resumed across sessions and tools without relying on chat history.

## Relationship to marumie-rssystem

`marumie-rssystem` is the application. This repository holds the research that informs it: source documents, extracted evidence, derived data, and reports, along with the protocol and decisions that govern how that research is conducted.

## Why research is stored separately

- Research artifacts (evidence, reports, snapshots) have a different lifecycle than application code.
- Keeping them separate avoids bloating the application repository with large or sensitive source material.
- It lets research state be canonical and machine-readable (see `state/CURRENT_STATE.json`) without being tied to app releases.

## Directory structure

```text
marumie-rssystem-research/
├── START_HERE.md          # How to resume this project in a new session
├── protocol/               # Research protocol and durable decisions
├── state/                  # Machine-readable current state, changelog, TODO
├── sources/                # Source registry (provenance) for primary documents
├── evidence/                # Extracted evidence from sources
├── reports/                 # Research reports
├── scripts/                  # Ingestion / processing scripts
├── snapshots/                # Reproducible phase checkpoints
├── fixtures/                  # Test/reference fixtures
└── derived/                   # Derived/interpreted data (kept separate from source facts)
```

## Canonical state

GitHub/main is the intended canonical persistent store for this research. Chat history is not canonical — see `START_HERE.md`.

## Large files

Large primary-source binaries (PDFs, spreadsheets, archives) should not normally be committed directly. Instead, their URL, checksum, and acquisition metadata are recorded in `sources/source-registry.csv`, with the file kept in separate persistent storage.

## Commits

The user controls all commits and pushes to this repository. AI sessions prepare changes but do not commit or push unless explicitly authorized.
