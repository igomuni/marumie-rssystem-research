# AGENTS.md

Working contract for AI agents (Claude/Sonnet, Codex, ChatGPT-based coding agents, and future automated agents) operating in this repository. This file is a routing/guardrail document, not a replacement for the detailed protocol. When in doubt, the linked canonical documents win.

## Start Here

- GitHub repository files are the canonical project state. Chat history is not.
- Begin every task with `START_HERE.md` — it defines the read order (`protocol/RESEARCH_PROTOCOL.md` → `state/CURRENT_STATE.json` → `protocol/DECISIONS.md` → `state/TODO.md`) and the resume process. This file does not redefine that order; it only adds itself to the front of it.
- Load only the evidence/reports/snapshots relevant to the current `nextAction` — do not read the whole repository "just in case."
- Do not infer missing historical facts from chat memory when a repository file already answers the question.

## Non-Negotiable Research Rules

These apply everywhere in this repository, not just to budget-figure research:

- `unknown != zero`, `blank != explicit zero`, `no explicit label found != zero`. Never fill a missing value with `0`, a guess, or an arithmetic reconstruction, unless a documented transformation stage explicitly calls for a derived value **and** its provenance/derivation rule is recorded alongside it.
- Amount/value similarity alone is never selection evidence (it may only validate an already-established link).
- Preserve the layer boundaries below — do not silently collapse them so a wrong answer can be traced to the layer that produced it.

Full methodology, ADRs, and the budget/RS-specific invariants: `protocol/RESEARCH_PROTOCOL.md`, `protocol/DECISIONS.md`.

## Data and Provenance

```text
source acquisition -> raw source -> text/glyph extraction -> document understanding
  -> normalization -> semantic interpretation/transformation -> evaluation -> evidence -> report
```

- Source identity is the acquired binary's SHA-256, not its URL (`same URL != same source binary` — ADR-009). Verify against `sources/source-lock.json` before reproducibility-sensitive processing. Never substitute a different downloaded file just because a filename or URL matches.
- Raw engine/extraction output must remain distinguishable from normalized output, and normalized output from semantic interpretation. A deterministic normalizer may transform raw output, but the raw artifact stays available and the transform rule is documented or versioned — never imply a normalized recovery was present in the raw output.
- **Ground truth may only be used by evaluation/scoring code.** It must never be used to select a target row/candidate, repair extraction output, infer a missing sign, reconstruct a missing value, resolve ambiguity, or normalize a result toward the expected answer. If a value is missing or ambiguous, record the miss/ambiguity — do not turn an extraction failure into an apparent success via expected-value knowledge.
- Large raw government files normally stay uncommitted (see `.gitignore`); reference them by URL + SHA-256 instead.

## PDF / Document Understanding

- `scripts/pdf-extraction/` = deterministic glyph/text/coordinate extraction. `scripts/document-understanding/` = layout/table/reading-order/structure recovery. These measure different things — do not treat text-extraction accuracy and document-understanding accuracy as the same metric.
- Preserve an engine's native structured output (tables, cells, blocks) where available; do not flatten it to plain text prematurely just to reuse existing code. See `scripts/document-understanding/README.md` for the current architecture and `scripts/pdf-extraction/README.md` for the extraction boundary.

## Benchmark Integrity

- Use the same evaluator and ground truth across engines when the benchmark design requires comparability (`scripts/document-understanding/benchmark/src/evaluate.mjs` is engine-agnostic by design — do not fork it per engine).
- Engine-specific normalizers are allowed only to deterministically represent an engine's native output (e.g. `normalize-docling.mjs`), never to fit an expected answer.
- A failure is a research result. Do not optimize for a perfect score, do not hand-tune logic to one case's expected values, and do not conceal a capability gap by narrowing what you test.
- Record regressions and unexpected behavior explicitly; distinguish "raw engine quality" from "raw engine + normalizer quality" when reporting results.

## Artifact Naming

Every **newly created** Markdown file uses an Asia/Tokyo creation-time prefix: `YYYYMMDD_HHMM_<descriptive-name>.md` (e.g. `20260926_0752_Docling_Benchmark_Report.md`). Use the actual creation time, not a placeholder.

Exceptions (do not rename these, and do not prefix new instances of them):
- `README.md`, `AGENTS.md`
- Established canonical protocol/state files already in the repository (`START_HERE.md`, files under `protocol/`, `state/`, and existing `reports/`/`evidence/` files)
- Any filename a tool or convention requires to be exact (e.g. `package.json`, `.gitignore`, `ground-truth.json`)

Do not retroactively rename existing Markdown files to apply this convention.

## Repository Safety

This repository is public.

- Never commit secrets, credentials, API keys, tokens, `.env` files, private business data, or personal data.
- Inspect staged files (`git status`, `git diff`) before every commit — not just the files you meant to touch.
- Virtualenvs, model caches, node_modules, large generated outputs, and raw source binaries follow `.gitignore`; do not commit them even transiently. See `protocol/DECISIONS.md` ADR-008.

## Git and Validation

This section summarizes `protocol/RESEARCH_PROTOCOL.md`'s Git / Commit Policy — that file is authoritative if anything here reads differently.

- Inspect the working tree (`git status`) before editing anything; do not overwrite or discard work you didn't create.
- Run the validation relevant to what you changed before committing (at minimum `npm run validate`; add `npm run extraction:test` / `npm run docbench:test` / `npm run docbench` etc. when those subsystems are touched).
- Run `git diff --check` and review the actual diff/staged filenames for secrets, binaries, or unexpected generated files.
- Never force-push or rewrite validated history unless explicitly requested.
- Commit and push only when the user has authorized it for the current task/workflow; do not merge to `main` unless explicitly authorized.

## Handoff

- Preserve failed experiments and negative results when they are scientifically meaningful — do not delete evidence of what didn't work.
- When completing a research or workspace phase (not every trivial edit), update `state/CURRENT_STATE.json`, `state/TODO.md`, and `state/CHANGELOG.md`.
- End a task by reporting: commands run, results, unresolved issues, and the recommended next action.

## Detailed References

- Methodology, invariants, ADRs: `protocol/RESEARCH_PROTOCOL.md`, `protocol/DECISIONS.md`
- Reproducibility boundary: `protocol/REPRODUCIBILITY.md`
- Current state / next action: `state/CURRENT_STATE.json`, `state/TODO.md`, `state/CHANGELOG.md`
- PDF extraction layer: `scripts/pdf-extraction/README.md`
- Document Understanding benchmark: `scripts/document-understanding/README.md`
- Source provenance: `sources/source-lock.json`, `sources/source-registry.csv`
