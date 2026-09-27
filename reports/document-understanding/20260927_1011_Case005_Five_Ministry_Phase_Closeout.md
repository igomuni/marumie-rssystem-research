# Case-005 / Five-Ministry Phase Closeout

Status: **closeout/audit only. No new research, no schema, no linkage experiment, no case-006. PR opened, left OPEN, not merged.**

Date: 2026-09-27 (Asia/Tokyo)

## 1. Scope

This task audits, and prepares for PR review, the research accumulated on `research/case-005-mlit-source-survey` since it branched from `main@34c9424`: the case-005 MLIT source survey through first-frozen benchmark, the five-ministry interim synthesis, and the Case Package v0 concept-design candidate. No new PDF inspection, row selection, Ground Truth change, benchmark rerun, schema prototype, MOF linkage experiment, or case-006 work was performed.

## 2. Branch chronology

Fresh-fetched baseline: branch `research/case-005-mlit-source-survey`, pre-task `HEAD` `7fe3ce9`, `origin/main` `34c9424`, `merge-base` = `34c9424` (clean linear branch, no divergence), working tree clean — all matching expected values exactly.

Commit order verified via `git log 314da39..7fe3ce9 --reverse`:

1. `314da39` — MLIT source survey
2. `9b292c0` — selection protocol freeze
3. `bab422f` — deterministic row selection freeze
4. `e1ed08e` — Ground Truth freeze
5. `6d16324` — first frozen benchmark
6. `7a41cea` — five-ministry interim synthesis
7. `7fe3ce9` — Case Package v0 concept design candidate

Order is correct: selection follows protocol freeze; GT freeze follows selection; first benchmark follows GT freeze; synthesis and design follow the benchmark. No production adaptation commit appears anywhere in this sequence (`git diff --stat origin/main...HEAD -- scripts/` is empty — zero `scripts/` changes on the entire branch).

## 3. Frozen artifact integrity

Diffed each frozen artifact between its freeze commit and current `HEAD` — all byte-identical (zero diff output):

| Artifact | Freeze commit | Result |
|---|---|---|
| Selection protocol | `9b292c0` | identical |
| Selection record | `bab422f` | identical |
| Ground Truth (`ground-truth.json` + evidence) | `e1ed08e` | identical |
| First frozen benchmark (report + evidence + evaluation) | `6d16324` | identical |

## 4. Source integrity

`sources/source-lock.json` entry for `mlit-fy2024-general-account-expenditure-request`: SHA-256 `4eebb84cec72a4b3b11a2b89c41093550bef5a07095d5c7b178e238406b08217` — matches expected exactly. Registry row confirms 1,097 pages. Raw PDF (`sources/raw/mlit-fy2024-general-account-expenditure-request.pdf`) exists locally, confirmed `git check-ignore`d, not tracked. No PDF file is tracked anywhere in the repository (`git ls-files | grep '\.pdf$'` is empty).

## 5. First-frozen benchmark preservation

`evidence/document-understanding/case-005-results.json` (unchanged since `6d16324`) confirms: `pdfjs-baseline` 10/11, `pymupdf-baseline` 10/11, `docling` 10/11. Sole shared FAIL across all three engines: `item_name_exact_match`. No `scripts/` change exists anywhere on the branch, so no adaptation could have occurred before or after this freeze; two-run reproducibility and no-adaptation claims in the original report are consistent with the commit history. Not rerun in this task.

## 6. Five-ministry synthesis consistency audit

Re-verified the synthesis report's own score tables against live evidence, not against the report's own claims:

**Current scores** (from `evidence/document-understanding/case-NNN-results.json`, all cases): case-001 8/8/9, case-002 4/4/3, case-003 10/10/3, case-004 7/7/5, case-005 10/10/10 — matches the report's §4/§9 tables exactly, and matches this task's own expected matrix.

**First-frozen scores** (re-derived from `git show` at each case's own freeze commit — `379043d` for case-002, `aa57caf` for case-003, `9b292c0`-lineage for case-005): case-002 2/3/2, case-003 9/10/3 — both match the synthesis report's §9 table and this task's own expected matrix exactly. case-001, case-004, case-005 first-frozen = current (no adaptation), also confirmed.

**`item_name_exact_match`**: re-checked directly against all five `results.json` files — FAIL for all 3 engines in all 5 cases (15/15), confirming the report's own headline claim with zero discrepancy.

Additional claims spot-checked and confirmed present, correctly qualified, and not contradicted by canonical evidence: the heterogeneous-mechanism argument for `item_name_exact_match` (§11); context-scope claims explicitly bounded to case-004's own sampled evidence, with case-005 recorded as a contrast case, not a refutation (§12); the MEXT Docling broad-sample falsification retained as the primary, un-softened result (§14, §21); no claim of five-case universality anywhere in the document; MOF linkage kept strictly in evidence-vs-proposal form with no matching performed (§17). **No factual correction was required** — the synthesis report's claims are consistent with the underlying repository evidence as re-verified in this audit.

## 7. Case Package concept-design candidate status

Confirmed the document's own opening line: "design candidate for review. Not an ADR. No schema, migration, or implementation in this task," and its §2 scope statement explicitly excluding schema/implementation/migration/finalization. Confirmed presence of all required invariants: Ground Truth isolation (§7 of the design doc, with an explicit embedded-vs-external-reference comparison), source-safe vs. engine-derived provenance (§8, `observationOrigin` concept), raw/normalized separation (§9), the six-state unknown/absent/ambiguous distinction (§10), the three-mechanism context model (§11), first-frozen history preservation (§14, §21), the Strategy Selection boundary (§18), and six explicitly unresolved open questions (§26). No rewrite was performed.

## 8. Two open pre-schema review issues (recorded, not resolved)

Per this task's own instruction, the following two issues are recorded here and in `state/TODO.md` as **open, unresolved, pending a future schema-prototype task** — the Case Package v0 concept-design document's own body was **not** rewritten to address them:

- **Context semantics**: treating `Context Requirement` uniformly as source-safe may be too strong; a future schema should consider distinguishing `sourceContextRelation` (a source-safe fact about where context physically sits) from `interpretationContextRequirement` (an engine/strategy-dependent fact about what a specific pipeline actually needed and used).
- **Evaluation dependencies**: allowing Evaluation unrestricted read access to every lower layer (§19 of the design doc) may be broader than necessary; a future schema should consider distinguishing ordinary semantic checks from representation/provenance diagnostic checks, with an explicit allowed-evidence-layer declared per check.

## 9. No new experiment statement

No schema was created. No PDF→MOF linkage experiment was started. No case-006 source survey was started. No RS 1000× anomaly scan was performed. No benchmark was rerun. No Ground Truth was changed. No production/normalization/evaluator code was modified.

## 10. Next-phase candidates (recorded as future direction only, not decided)

**Phase 1 (this program to date)**: source acquisition, reproducible selection, GT methodology, first-frozen benchmarking, normalization, context diagnostics, anomaly/falsification research, architecture synthesis — complete for five cases.

**Candidate Phase 2 (not started, not decided)**: provenance/linkage feasibility (PDF→MOF, later MOF→RS). This PR does not begin Phase 2. A schema-prototype task, a linkage-feasibility experiment, case-006, and an RS anomaly scan are all separate, future, unstarted tasks.

## 11. Validation

`npm run validate` — PASS. `git diff --check` — clean (no whitespace/trailing-newline issues introduced by this task). `git diff --stat origin/main...HEAD` reviewed — no `scripts/` file touched anywhere on the branch; no raw PDF, PNG/render scratch, secrets, temporary scripts, generated schema, or migration artifact present in the changed-file list.

## 12. PR readiness verdict

**READY.** Chronology is correct and linear; every frozen artifact is byte-identical to its freeze point; source identity is verified; the first-frozen benchmark is preserved untouched; the five-ministry synthesis and Case Package concept design are both internally consistent with canonical repository evidence and correctly self-identify as non-final; repository hygiene is clean; validation passes.

---

**This task performed only chronology/integrity audit and closeout documentation. No schema prototype, PDF→MOF linkage experiment, case-006 work, benchmark rerun, Ground Truth change, or production adaptation was performed.**
