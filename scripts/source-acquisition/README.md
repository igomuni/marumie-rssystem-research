# Source Acquisition

Node.js-only tooling (no external dependencies; uses built-in `fetch`, `crypto`, `fs`) that makes this boundary reproducible:

```text
primary source URL
    ↓
downloaded binary
    ↓
SHA-256 lock
```

This does not implement PDF text extraction. It only acquires and hashes the raw source binaries currently registered for the request-ingestion PoC in `scripts/request-ingestion/source_manifest.json`.

## Commands

From the repository root:

```bash
npm run sources:lock    # download the registered sources, save raw binaries locally, write/update sources/source-lock.json
npm run sources:verify  # re-download each locked source and compare its SHA-256 against the committed lock
```

Or from this directory:

```bash
npm run lock
npm run verify
```

## Lock vs. verify

- **`lock`** is an explicit, intentional operation. It downloads the currently registered source URLs, computes their SHA-256, records HTTP status/content-type/size/redirect target, saves the raw binary under `sources/raw/` (git-ignored, not committed), and writes `sources/source-lock.json` (committed — this is the reproducibility anchor).
- **`verify`** never writes or updates the lock file. It re-downloads each source listed in the committed lock, computes its SHA-256, and compares it against the locked hash. It exits non-zero and reports `FAIL <sourceId>` with the expected/actual hashes on any mismatch.

## Why binaries are not committed

Downloaded PDFs are saved under `sources/raw/`, which is git-ignored. The repository is public and these are large, third-party binaries; instead, `sources/source-lock.json` records their SHA-256 so anyone can verify a freshly downloaded copy matches the one this research was based on.

## Source mutation

```text
same URL != same source binary
```

A government site can replace the file behind an unchanged URL. `sources:verify` is designed to catch this: a mismatch is reported, not silently accepted, and the locked hash is never overwritten by `verify`. Updating the lock to a new binary requires explicitly re-running `sources:lock`, which is itself a reviewable Git change. See ADR-009 in `protocol/DECISIONS.md`.
