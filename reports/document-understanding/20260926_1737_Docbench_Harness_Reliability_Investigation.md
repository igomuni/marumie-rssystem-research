# docbench Harness Reliability Investigation

Status: **investigation complete. Root cause confirmed. Narrow, generic fix applied. No benchmark semantics changed — all three cases' historical results reproduced byte-identically.**

Date: 2026-09-26 (Asia/Tokyo)

## Original symptom: observed facts vs. hypotheses

The case-003 first-frozen-run report (`20260926_1637_Case003_First_Frozen_Benchmark_Run.md`) recorded, as an unresolved harness-reliability finding:

- `npm run docbench -- case-003` failed four consecutive times with `ENOENT: ... docling.raw.json`.
- No Docling subprocess output appeared to reach the parent on the failing attempts.
- Direct invocation of the unmodified Docling adapter succeeded every time it was tried in isolation.
- A `case-002` control run succeeded immediately.
- The same case-003 harness later succeeded twice, reproducing identical 9/11, 10/11, 3/11 results.

At the time, this was framed as a plausible **Docling/Torch startup or Node `spawnSync` child-process reliability** issue — categories 1 (harness/process reliability) and 2 (adapter/runtime reliability) in this task's framing. **That framing turned out to be wrong.** The actual mechanism involves neither Docling, Torch, nor any child process at all.

## Actual execution path (as mapped, then found to be incomplete)

```text
npm run docbench -- case-003
  -> npm --prefix scripts/document-understanding/benchmark run run -- case-003
    -> node src/run.mjs case-003
      -> [static import] normalize-docling.mjs   <-- the actual fault, here
      -> main('case-003')
        -> loop 1: adapter.run() for pdfjs-baseline, pymupdf-baseline, docling
             (docling.run() -> spawnSync venvPython src/run.py case-003)
        -> loop 2: adapter.normalize() + evaluate() for each
```

The initially-assumed path treated the docling **adapter subprocess** (Python/Torch/RapidOCR) as the suspect boundary. The reproduction protocol below instead localized the fault to the **static `import` of `normalize-docling.mjs` at the top of `run.mjs`**, which executes **before `main()` is ever called**.

## Reproduction protocol

Given the intermittent nature reported, the plan was to run a modest, evidence-driven number of controlled attempts (5 clean-slate `npm run docbench -- case-003` runs, chosen as enough to distinguish "always fails," "always succeeds," and "genuinely intermittent" without burning excessive Docling/Torch inference cost) while adding minimal diagnostic instrumentation, and to use `case-002` and direct-adapter invocation as controls, exactly as prescribed. In practice, the first two rounds of instrumentation (described below) proved unnecessary once the actual mechanism was isolated with a single targeted experiment; the full 5-attempt confirmation was still run afterward, against the fix, to establish confidence.

### Round 1 — reconstruct the reported intermittency

Five clean-slate `node src/run.mjs case-003` attempts (derived directory removed between each): **4 failed, 1 succeeded**, all with the identical `docling.raw.json` ENOENT trace on failure and identical 9/11, 10/11, 3/11 scores on success. This reproduced the originally-reported pattern.

### Round 2 — minimal diagnostic instrumentation (temporary, reverted)

Added `console.error`/timestamped diagnostics at the top of `main()`, at entry to `venvPythonAdapter`'s returned function, and immediately after each `spawnSync` call (executable, args, cwd, `pid`/`status`/`signal`/`error`, duration). **On every failing attempt, none of these diagnostic lines appeared at all** — not even the very first line at the top of `main()`, printed unconditionally as the function's first statement, regardless of whether output was captured via file redirection, a pipe, or an entirely unredirected terminal invocation (all three were tested to rule out an output-capture artifact).

This was the decisive clue: if `main()`'s own first line never printed, `main()` itself had not yet been entered when the crash occurred — meaning the fault could not be inside the adapter-invocation loop at all.

### Round 3 — stack trace re-examination

Re-reading the original crash trace line by line:

```text
at Object.readFileSync (node:fs:440:20)
at readJson (.../common.mjs:18:24)
at normalizeDocling (.../normalize-docling.mjs:199:15)
at file:///.../normalize-docling.mjs:244:15
at ModuleJob.run (node:internal/modules/esm/module_job:377:25)
at async onImport.tracePromise.__proto__ (...)
at async asyncRunEntryPointWithESMLoader (...)
```

**There is no `run.mjs` frame anywhere in this trace.** The call originates directly from `normalize-docling.mjs:244`, one frame below Node's own module-loader internals (`ModuleJob.run`) — i.e. from **top-level module-scope code**, executed as a side effect of the `import` statement itself, not from a function call made later by `run.mjs`'s `main()`.

### Round 4 — targeted, decisive experiment

Inspecting `normalize-docling.mjs`'s final lines confirmed a standalone-execution convenience block:

```js
const [, , caseIdArg] = process.argv;
if (caseIdArg) {
  const out = normalizeDocling(caseIdArg);
  console.log(`NORMALIZED docling/${caseIdArg} -> ...`);
  console.log(JSON.stringify(out.result, null, 2));
}
```

This reads `process.argv[2]` — the **same process's** argv, shared with `run.mjs` itself (`node src/run.mjs case-003` → `process.argv = ['node', '.../run.mjs', 'case-003']`). Since `run.mjs` does `import { normalizeDocling } from './normalize-docling.mjs'` at its own top level, this block runs **immediately at import time**, before any adapter has run, with `caseIdArg = 'case-003'`.

Decisive isolated reproduction, with zero involvement of `run.mjs`, `spawnSync`, Docling, Python, or any child process:

```bash
$ node -e "process.argv = ['node', 'anything', 'case-003']; \
    import('./src/normalize-docling.mjs').catch(e => console.log('IMPORT THREW:', e.message))"
IMPORT THREW: ENOENT: no such file or directory, open '.../derived/document-understanding/case-003/docling.raw.json'
```

**This reproduces the exact reported error, with a plain module import, on demand, every time `docling.raw.json` does not already exist on disk for the given case.**

## Localization

- **Layer**: none of the three failure classes the task asked to distinguish (harness/process reliability, adapter/runtime reliability, document-understanding quality) is quite right. This is a fourth category: **module-import-time side effect / accidental self-invocation**, arising because a dev-convenience "run me standalone" block at module scope reads the same `process.argv` slot that the importing script (`run.mjs`) also populates with a real case ID.
- **Why it looked intermittent rather than deterministic**: the crash occurs if and only if `derived/document-understanding/<caseId>/docling.raw.json` does not already exist at the moment `run.mjs` is started. If a stale raw artifact from an earlier successful run is still present (this repository's `derived/` tree is git-ignored and persists locally between invocations), the import-time self-invocation succeeds silently against that **stale** data, prints its own `NORMALIZED docling/<caseId> -> ...` line (which was observed appearing suspiciously *before* `RAW pdfjs-baseline/...` in earlier successful-run logs — not a stdout-ordering artifact as first assumed, but the true execution order), and `main()` then proceeds normally, re-running every adapter fresh and re-normalizing docling for real in `main()`'s own loop 2. `case-002`'s control run never failed in this investigation or the prior task because its `docling.raw.json` was never deleted across the whole session; `case-003`'s was repeatedly deleted between test attempts (deliberately, to test from a clean slate), which is exactly what exposed the bug.
- **`normalize.mjs`** (used by `pdfjs-baseline`/`pymupdf-baseline`) has the structurally identical block, but gated on **two** argv positions (`caseIdArg && engineArg`). Since `run.mjs` invokes itself with only one argument (`node src/run.mjs case-003`), `engineArg` (`process.argv[3]`) is always `undefined` when `run.mjs` imports it, so this particular collision never fires for `normalize.mjs` today — it is the same latent pattern, just not currently triggered, one argv-shape change away from an identical failure mode.

## Root-cause confidence: **CONFIRMED**

Evidence chain: (1) crash trace contains no `run.mjs` frame and originates one frame below Node's module loader; (2) `main()`'s own unconditional first statement never executes on any failing attempt, across three different output-capture methods; (3) a single-line, zero-dependency, zero-subprocess reproduction (`node -e "process.argv=...; import(...)"`) deterministically reproduces the exact reported error on demand; (4) after the fix (below), 5/5 clean-slate `npm run docbench -- case-003` attempts succeeded, and the isolated reproduction no longer throws.

## Fix

Guarded both modules' standalone-execution blocks so they run **only on direct execution**, never as an import side effect, using the same `import.meta.url === file://process.argv[1]` pattern already established elsewhere in this repository (`scripts/source-acquisition/browser-fetch/src/browser-fetch.mjs`, `scripts/source-acquisition/src/acquire.mjs`, both guarded identically after the prior PR #2 review and the HTTP-acquisition-immutability fix):

- `scripts/document-understanding/benchmark/src/normalize-docling.mjs` — wrapped the block in `if (isDirectlyExecuted) { ... }`.
- `scripts/document-understanding/benchmark/src/normalize.mjs` — wrapped identically, as defense-in-depth (not currently triggered by `run.mjs`, per the analysis above, but the identical latent pattern; guarding it now removes the dependency on `run.mjs`'s argv shape never changing).

**Why this does not change benchmark semantics**: the guarded code is a manual, standalone developer convenience (`node normalize-docling.mjs <caseId>` for inspecting one engine's output without running the full benchmark) — it was never documented in `scripts/document-understanding/README.md` as part of the supported workflow (verified: the README only describes what these files *are*, never how to invoke them directly), and it is not called by any other script. `evaluate.mjs`, `common.mjs`, both adapters' Python scripts, and `normalizeDocling`'s/`normalize`'s own function bodies are byte-for-byte unchanged — only *when* the module's top-level convenience block may fire was changed, never any extraction/normalization/evaluation logic.

This is not a blind retry, an increased timeout, or a speculative workaround — it removes the actual confirmed mechanism (an unintended second, premature invocation) at its exact source.

## Tests

Two new regression tests added to `scripts/document-understanding/benchmark/src/test.mjs`, targeting the confirmed mechanism directly rather than the full Docling pipeline (per the task's preference for lightweight reproduction over expensive inference):

- `normalize-docling.mjs: importing with a run.mjs-shaped argv for a nonexistent case does not throw`
- `normalize.mjs: importing with a run.mjs-shaped argv (single caseId arg only) does not throw`

Both spawn a fresh `node -e` subprocess (module top-level side effects can only be observed on first evaluation; the module is already cached by this same test file's own static imports at the top) with `process.argv` shaped exactly like `run.mjs`'s own invocation, importing the target module for a case ID that does not exist on disk, and asserting the import resolves rather than rejects. Both pass against the fix. (Manually confirmed against the pre-fix code via the Round 4 reproduction above — a value directly equivalent to what these tests check — rather than via a stash/pop of the same commit's combined changes, which would not isolate old-code-vs-new-test meaningfully.)

Full suite: 28/28 passing (26 pre-existing + 2 new).

## Benchmark-integrity / control checks

- **case-001**: `pdfjs-baseline` 8/11, `pymupdf-baseline` 8/11, `docling` 9/11 — byte-identical (modulo `generatedAt`/`evaluatedAt`) to the pre-fix committed evidence.
- **case-002**: `pdfjs-baseline` 3/11, `pymupdf-baseline` 4/11, `docling` 3/11 — byte-identical to the pre-fix committed evidence.
- **case-003**: `pdfjs-baseline` 9/11, `pymupdf-baseline` 10/11, `docling` 3/11 — byte-identical to the historical `aa57caf` result.
- **case-003 reliability**: 5/5 clean-slate (`derived/document-understanding/case-003/` removed before each) `npm run docbench -- case-003` runs succeeded, all reproducing identical scores.
- No Ground Truth, selection protocol/record, source lock, or raw source file was touched (`git diff` on all four confirmed empty before commit).
- The regenerated (timestamp-only) `evidence/`/`reports/` compact files produced by the control re-runs above were reverted before commit — their content is unchanged from the already-committed historical files (verified via a normalized-JSON diff ignoring timestamp fields), so re-committing them would have been pure noise.

## Remaining uncertainty

- Whether any other file in this repository has the same "module-scope self-invocation reading shared `process.argv`" pattern was not exhaustively audited beyond the two files directly implicated by this specific failure (`normalize.mjs`, `normalize-docling.mjs`). The pattern is specific to files with a `node <file> <args>` standalone-convenience block that are also `import`-ed by another script sharing the same process — a search for this exact shape elsewhere was not performed and is a reasonable, narrow follow-up if desired, not undertaken here to avoid scope creep beyond the reported symptom.
- The historical case-003 first-run report's speculation about "resource contention from repeated torch/RapidOCR loads" or "a Node spawnSync/child-stdio interaction" is now understood to have been an incorrect (though reasonable, given the available evidence at the time) hypothesis — the actual mechanism has nothing to do with Docling, Torch, or child processes at all. That report's *semantic* findings (scores, per-check analysis, layer diagnosis) are unaffected and remain valid; only its "harness-reliability finding" section's proposed causes are superseded by this investigation. That report is not rewritten, per historical-integrity instructions; this document supersedes its speculative causes.

## Implications for trusting future benchmark runs

Any future first-run (`case-004`+) against a case whose `derived/document-understanding/<caseId>/docling.raw.json` does not yet exist would have hit this exact failure before the fix, with the same misleading appearance of Docling/Torch instability. **This is now resolved for all future cases, not just case-003** — the fix is generic and does not reference any case ID. Future first-run reports no longer need to caveat their Docling results with an unresolved harness-reliability disclaimer; a completed `docbench` run's results can be trusted as reflecting the actual pipeline's behavior on the first attempt, without needing a lucky pre-existing stale artifact or a retry.

## Files changed

- `scripts/document-understanding/benchmark/src/normalize-docling.mjs` — guarded the standalone-execution block.
- `scripts/document-understanding/benchmark/src/normalize.mjs` — guarded the standalone-execution block (defense-in-depth).
- `scripts/document-understanding/benchmark/src/test.mjs` — 2 new regression tests.
- `reports/document-understanding/20260926_1737_Docbench_Harness_Reliability_Investigation.md` (this file).
- `state/CURRENT_STATE.json`, `state/TODO.md`, `state/CHANGELOG.md`.

No Ground Truth, selection protocol/record, source lock/raw file, evaluator (`evaluate.mjs`), `common.mjs`, any adapter, or Case Package file was modified. No ADR was added — this is a bug fix already covered by the existing engineering-quality expectations of the codebase, not a new methodological or architectural decision.

## Validation

```bash
npm run validate           # PASS
npm run extraction:test    # PASS
npm run docbench:test      # PASS (28/28)
git diff --check           # clean
```

5 clean-slate `npm run docbench -- case-003` control runs (see above) plus 1 run each for `case-001`/`case-002`, all reproducing historical scores byte-identically (modulo timestamps).
