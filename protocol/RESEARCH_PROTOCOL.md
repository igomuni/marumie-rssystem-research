# Research Protocol

## Purpose

This protocol defines how research for the `marumie-rssystem` project is conducted, recorded, and handed off between sessions so that work is reproducible and does not depend on chat history.

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

- AI sessions prepare changes; the user performs commit/push.
- Do not commit or push unless the user explicitly performs/authorizes it.

---

TODO: Import validated invariants from FY2024 IT budget investigation.
