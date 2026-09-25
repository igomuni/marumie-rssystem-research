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
- The downloaded content's first 5 bytes are checked against the PDF magic number (`%PDF-`) before anything is written to `sources/source-lock.json`. If a challenge/interstitial page is captured instead of the real file, the tool refuses to lock it and exits non-zero, rather than silently locking a hash of the wrong content — this is a gap the plain `acquire.mjs` currently has (it only checks the HTTP status is in `[200, 300)`, which a `202` challenge response satisfies).
- Writes the raw binary to `sources/raw/<sourceId>.pdf` (git-ignored, same convention as `acquire.mjs`) and adds/updates the entry in `sources/source-lock.json`, with two extra provenance fields not present in plain-fetch entries: `acquisitionMethod: "playwright-chromium"` and `playwrightVersion`, plus `landingPageUrl` if one was used.

## What this does not do

- It does not run any document-understanding engine, OCR, or text extraction against the downloaded PDF — it only retrieves and hashes the binary.
- It does not attempt to solve or reverse-engineer the bot-challenge's JavaScript itself; it simply uses a real browser engine to load the page the way any human visitor's browser would.
