# Case Package Reconstruction Benchmark v0 — Report

Status: **v0 complete. First valid run; not tuned or rerun after seeing output.**

Date: 2026-09-26 (Asia/Tokyo)

Case Package input commit: `f7b0b75` (verified unchanged immediately before execution)

Artifacts: this report + `20260926_1348_..._Frozen_Prompt_And_Schema.md` + `20260926_1348_..._Frozen_Evaluation_Checklist.md` + `20260926_1348_..._Raw_Outputs.md` + `20260926_1348_..._Evaluation_Result.md`

## What this benchmark tested

Whether `document-profile.json` + `research-history.jsonl` alone — without README, evaluation reports, source PDFs, Ground Truth, Git history, or the other case — let an independent LLM session reconstruct a Case's research state: identity, methods, results, temporal chronology (including a correction), epistemic categories, and open work. This is not strategy selection, not PDF extraction, not Ground Truth recovery.

## Experimental validity

**Isolation was behavioral/instructional, not sandbox-enforced.** No tool in this session's toolset can strip a spawned `general-purpose` agent's tool access down to zero; both reconstruction agents ran in the same working directory with the same nominal tool grants (Read/Bash/Grep/WebFetch) as any other general-purpose agent, and were told, in the prompt, not to use any of them. This is a real limitation, not a rounding error, and the result below should be read with that caveat attached throughout.

Evidence bearing on whether isolation actually held:
- Each agent's usage summary reports exactly `tool_uses: 1` for both runs — consistent with a single required hand-back call and zero repository-access tool calls. This is the strongest available evidence of compliance, but it is a count reported by the harness about the agent's own tool invocations, not an independent audit of memory/context; it does not by itself prove the underlying model had no latent memorized knowledge of this repository from its training data (a different contamination channel than tool use, and one no isolation technique available here can rule out).
- Both outputs are consistent with genuine two-file-only reasoning: case-001's output explicitly flags the *absence* of a preregistered selection protocol as an `explicitUnknown`, rather than either inventing one or wrongly assuming case-002's protocol also applied to case-001 — this is precisely the hallucination risk named in the task (§11, "case-002 preregistration discipline retroactively applied to case-001"), and it did not occur.
- Neither run referenced the other case, the architecture report, README files, or any evidence/report path not literally present in its own two supplied files' `evidence` arrays.

Given these two considerations together, this v0 run is treated as a **valid, if imperfectly isolated, first benchmark** — not aborted, per the task's framing that documenting a limitation is the correct response short of a hard failure. A v1 with a genuinely sandboxed (zero-tool, zero-filesystem) execution environment is the natural methodological upgrade (see Recommended next step).

## Frozen inputs

- Case Package: `fixtures/document-understanding/{case-001,case-002}/{document-profile.json,research-history.jsonl}` at commit `f7b0b75`, diff-verified empty immediately before execution.
- Reconstruction prompt: v1, frozen in `20260926_1348_..._Frozen_Prompt_And_Schema.md`, identical wording for both cases (only the two file-content blocks differ).
- Output schema: v1, same file, 14 top-level keys, applied unchanged to both cases.
- Evaluation checklist: v1, frozen in `20260926_1348_..._Frozen_Evaluation_Checklist.md` (16 items for case-001, 19 for case-002), written from canonical repository evidence before either reconstruction output was inspected.

## Reconstruction runtime

Two separate `Agent` tool calls, `subagent_type: general-purpose`, each a fresh context with no memory of this conversation or of the other run, launched in the same message (parallel). Model/provider/version string and sampling parameters were not exposed by the tooling and are recorded as unknown in the raw-outputs artifact, not fabricated. Both runs produced valid, schema-conforming JSON on the first attempt — no retry, no discarded output.

## case-001 results

15/16 checklist items correctly reconstructed, 1 partially reconstructed (an epistemic-status distinction conveyed correctly in substance but not by literally citing the source's `status` field value), 0 omitted, 0 contradicted, 0 hallucinated/unsupported claims. Notably: the model correctly separated the pre-Docling and post-Docling-integration historical states (something the checklist did not strictly require but the raw file's granularity supported) and correctly returned `"unknown"` for `proposedNextInvestigation.summary` rather than inventing a prioritized recommendation the source files do not state.

## case-002 results

18/19 correctly reconstructed, 0 partial, 1 omitted, 0 contradicted, 0 hallucinated/unsupported claims. The critical temporal test (§10 of the task) passed cleanly: both the original first-frozen scores (2/11, 3/11, 2/11, explicitly marked superseded) and the corrected scores (3/11, 4/11, 3/11, explicitly marked current and linked via `supersedes`) are present, distinct, and correctly ordered. The WAF-failure → Playwright-acquisition → source-lock chronology is fully preserved. The one omission (C2-19) is a meta-level nuance — that one engine-derived feature's own note flags itself as plausibly source-observable but actually engine-discovered — which the frozen schema never explicitly solicited.

## Reconstruction errors

Zero contradictions, zero hallucinations, in either run. The only defects found across both checklists (35 items total) are: one partial epistemic-status citation (case-001) and one omission of a schema-unsolicited meta-nuance (case-002). No engine result, PDF metadata value, layout-family label, Ground Truth value, commit, or report was invented in either run.

## Representation diagnosis

- **case-001's partial item (C1-14):** Category **B (information present but structurally difficult to recover)**. The `status` field (`superseded`/`current`) is present in the raw JSONL, but the schema/prompt did not explicitly ask the model to quote raw field values, so the model paraphrased the same fact in prose instead of citing the literal field. Not a model failure and not missing information — a prompt/schema specificity gap.
- **case-002's omitted item (C2-19):** Category **A (information absent from the reconstruction target, as posed) crossed with D (evaluation-checklist reach exceeding the frozen schema's scope)**. The underlying fact is present in the supplied file's `note` text, but the fixed output schema has no field asking for "meta-commentary on a feature's own discovery-provenance caveat," so a compliant, schema-following model has no natural place to put it. This is arguably a checklist-design overreach (grading against a fact the schema never solicited) as much as a representation gap — flagged honestly rather than silently excluded from the count.
- No item in either checklist is attributable to category **C (model failure despite adequate representation and adequate schema prompting)** or **E (unknown)** — every observed defect traces cleanly to A/B/D above.

## Case Package adequacy

**What v0 supports:** for these two, relatively rich, contemporaneously-and-retrospectively-documented cases, the `document-profile.json` + `research-history.jsonl` pair is sufficient for a fresh LLM session to reconstruct identity, methods, results, the full temporal chronology of a real methodology correction (the hardest test in this experiment), epistemic category distinctions, and open work — with zero hallucination and near-total checklist coverage (33/35 items across both cases).

**What v0 does not support:** any claim about (a) representation adequacy for a case with a genuinely different/impoverished history than these two (both are recent, English/Japanese-mixed, single-domain, single-day cases — no long-running or multi-month case has been tested); (b) representation adequacy under a stricter, sandboxed isolation guarantee; (c) whether the schema's specific field set (chosen for this v0, not derived empirically) is the right one for future cases whose research history has a shape these two don't exhibit (e.g. a case with no methodology correction at all, or with three linked corrections instead of one).

## Files changed

- `reports/document-understanding/20260926_1348_Case_Package_Reconstruction_Benchmark_v0_Frozen_Prompt_And_Schema.md`
- `reports/document-understanding/20260926_1348_Case_Package_Reconstruction_Benchmark_v0_Frozen_Evaluation_Checklist.md`
- `reports/document-understanding/20260926_1348_Case_Package_Reconstruction_Benchmark_v0_Raw_Outputs.md`
- `reports/document-understanding/20260926_1348_Case_Package_Reconstruction_Benchmark_v0_Evaluation_Result.md`
- `reports/document-understanding/20260926_1348_Case_Package_Reconstruction_Benchmark_v0_Report.md` (this file)
- `state/CURRENT_STATE.json`, `state/TODO.md`, `state/CHANGELOG.md` (state updates)

No Case Package input file (`document-profile.json`/`research-history.jsonl` for either case) was modified. No `case-003`, strategy selector, embeddings/vector store, adapter, normalizer, evaluator, or Ground Truth was touched.

## Validation

- `npm run validate`: PASS
- `git diff --check`: clean
- Both raw JSON reconstruction outputs re-extracted from the raw-outputs artifact and strictly `JSON.parse`'d: both valid, both with exactly the 14 frozen top-level schema keys.
- Pre-execution: confirmed via `git diff f7b0b75 -- <4 input files>` = empty (inputs unchanged before the benchmark ran).

## Git

Branch `research/case-002-meti-preregistration`. Commit SHA and push state: recorded after this report is committed (see the commit immediately following this report in repository history). `main` unchanged. No PR opened, no merge performed.

## Recommended next step

Design and run a **v1** of this same benchmark with a genuinely sandboxed reconstruction environment (a tool-free or filesystem-isolated execution context, rather than an instructed-but-not-enforced one) — this directly resolves v0's single most consequential limitation (behavioral, not enforced, isolation) without changing anything else about the Case Package representation itself, which v0 already supports treating as adequate for these two cases. Do not execute this in the current task.
