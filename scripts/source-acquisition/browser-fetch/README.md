# Browser-based source acquisition

Node.js + Playwright (pinned `1.63.0`, isolated `node_modules`) tooling for the small number of sources that `scripts/source-acquisition/src/acquire.mjs`'s plain `fetch()` cannot reach — specifically, sources protected by a JavaScript bot challenge (e.g. AWS WAF Bot Control) that requires executing real browser JS to pass.

## When to use this instead of `acquire.mjs`

Use `acquire.mjs` (`npm run sources:lock`) by default. Only reach for this tool when a source genuinely fails under a plain HTTP client with a bot-challenge response (verify this first — see `state/CHANGELOG.md`'s case-002 preregistration entry for how the METI source's AWS WAF challenge was diagnosed before this tool was written).

## Setup

```bash
cd scripts/source-acquisition/browser-fetch
npm install
npx playwright install chromium
```

`node_modules/` and the Playwright browser cache are git-ignored.

## Run

```bash
node src/browser-fetch.mjs --source-id <id> --url <url> [--landing-page <url>] [--mime-type <type>]
```

- `--landing-page` is optional but was necessary for the METI source: visiting the HTML landing page first (in the same browser context) satisfies the bot-challenge state before the PDF request; requesting the PDF URL directly, cold, did not.
- The downloaded content's first 5 bytes are checked against the PDF magic number (`%PDF-`) before anything is written to `sources/source-lock.json`. If a challenge/interstitial page is captured instead of the real file, the tool refuses to lock it and exits non-zero, rather than silently locking a hash of the wrong content. `acquire.mjs`'s `lock` command performs the same check now (it originally only checked the HTTP status was in `[200, 300)`, which a `202` challenge response satisfies; fixed together with the lock-immutability issue below).
- Writes the raw binary to `sources/raw/<sourceId>.pdf` (git-ignored, same convention as `acquire.mjs`) and adds a new entry in `sources/source-lock.json`, with two extra provenance fields not present in plain-fetch entries: `acquisitionMethod: "playwright-chromium"` and `playwrightVersion`, plus `landingPageUrl` if one was used.
- **The lock is immutable for a `sourceId` that already exists.** Re-running this tool for a `sourceId` already in `sources/source-lock.json` compares the freshly-fetched SHA-256 against the existing lock entry *before* writing anything: if they match, the tool reports success and leaves the existing lock entry and raw file completely untouched (no `fetchedAt`/`finalUrl`/`playwrightVersion` refresh, since reproducing the same bytes is not new information); if they differ — e.g. the upstream PDF changed since it was locked — the tool exits non-zero with an error naming the `sourceId` and both SHA-256 values, and does **not** overwrite the existing lock entry or raw file. Updating a lock to a genuinely new upstream binary is a deliberate, reviewable action this tool does not perform automatically (see `protocol/DECISIONS.md` ADR-009). This decision/mutation policy lives in `../src/lock-policy.mjs` and is shared with `acquire.mjs`'s plain-fetch `lock` command, so it behaves identically regardless of which acquisition method retrieved the bytes.

## What this does not do

- It does not run any document-understanding engine, OCR, or text extraction against the downloaded PDF — it only retrieves and hashes the binary.
- It does not attempt to solve or reverse-engineer the bot-challenge's JavaScript itself; it simply uses a real browser engine to load the page the way any human visitor's browser would.
