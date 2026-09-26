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

- **`lock`** is an explicit, intentional operation. For a `sourceId` not yet in the lock, it downloads the source, validates it looks like the expected PDF (rejecting an HTML bot-challenge/interstitial page even if the HTTP status is 2xx), computes its SHA-256, saves the raw binary under `sources/raw/` (git-ignored, not committed), and writes `sources/source-lock.json` (committed — this is the reproducibility anchor). **For a `sourceId` already in the lock, `lock` is immutable**: identical bytes report a no-op `VERIFIED` outcome (the existing entry and raw file are left completely unchanged), and different bytes cause `lock` to exit non-zero without writing anything — it never silently replaces an existing entry. This mutation-decision policy is shared with `browser-fetch/` (`src/lock-policy.mjs`), so it behaves the same way regardless of which acquisition method is used.
- **`verify`** never writes or updates the lock file. It re-downloads each source listed in the committed lock, computes its SHA-256, and compares it against the locked hash. It exits non-zero and reports `FAIL <sourceId>` with the expected/actual hashes on any mismatch.

## Why binaries are not committed

Downloaded PDFs are saved under `sources/raw/`, which is git-ignored. The repository is public and these are large, third-party binaries; instead, `sources/source-lock.json` records their SHA-256 so anyone can verify a freshly downloaded copy matches the one this research was based on.

## Source mutation

```text
same URL != same source binary
```

A government site can replace the file behind an unchanged URL. `sources:verify` is designed to catch this: a mismatch is reported, not silently accepted, and the locked hash is never overwritten by `verify`. `sources:lock` no longer silently updates an existing entry either — a genuinely different upstream binary makes `lock` fail loudly, naming the `sourceId` and both SHA-256 values, without writing anything. There is deliberately no `--force`/re-lock-to-new-binary shortcut yet; updating an existing lock entry to a knowingly-changed source is left as a future, explicitly reviewable workflow. See ADR-009 in `protocol/DECISIONS.md`.
