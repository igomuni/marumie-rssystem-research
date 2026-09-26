# Case Package Reconstruction Benchmark v0 — Frozen Reconstruction Prompt and Output Schema

Status: **frozen before any reconstruction run. Not modified after seeing model output.**

Date: 2026-09-26 (Asia/Tokyo)

Case Package input commit (verified via `git diff f7b0b75 -- <the 4 files>` = empty immediately before this benchmark): `f7b0b75`

This document is Artifact 1 of the Case Package Reconstruction Benchmark v0 (see the benchmark report for the full artifact list). It exists so the exact prompt/schema used can be independently verified never to have changed between case-001's run and case-002's run, and never to have been edited after seeing either output.

## Reconstruction prompt (v1, used verbatim for both cases)

```text
You are given exactly two files describing one research "Case" from a Document
Understanding benchmark research project. You have NOT been given anything else
about this project: no README, no evaluation report, no source PDF, no other
case, no Git history, no repository access, and no other context. Do not use
any tools, do not browse, do not read any files other than the two blocks of
text supplied below in this prompt, and do not rely on any general knowledge
about "typical" Japanese government budget documents, "typical" PDF extraction
research, or any other case you might otherwise know about. Treat the two
supplied files as the complete and only source of truth for this task.

FILE 1: document-profile.json
<<<PASTE EXACT FILE CONTENTS HERE>>>

FILE 2: research-history.jsonl
<<<PASTE EXACT FILE CONTENTS HERE>>>

Your task: reconstruct, as completely and accurately as the two files above
support, the research state of this Case. Follow these rules strictly:

1. Use only the two supplied files. Do not invent repository paths, commit
   hashes, values, engine names, scores, or evidence that is not present in
   the supplied text.
2. Distinguish HISTORICAL state from CURRENT state. If a value or result was
   later corrected or superseded, report both the original and the corrected
   value, and say which is current. Do not silently drop a superseded result.
3. Distinguish the following epistemic categories precisely, using the
   "kind" field in research-history.jsonl as your primary signal, and do not
   blur them: observation, hypothesis, intervention, experiment, result,
   methodology_correction, conclusion, unresolved_question. A "hypothesis" is
   not a "conclusion." An "observation" is not a "result."
4. If the two files do not support an answer to some part of the reconstruction
   schema below, output "unknown" (or an empty array, as appropriate) for that
   field. Do not guess, and do not fill a gap with plausible-sounding domain
   knowledge.
5. For every reconstructed claim of substance, attach the specific eventId(s)
   from research-history.jsonl and/or feature key(s) from document-profile.json
   that support it, using only IDs/keys that literally appear in the supplied
   files. Do not invent IDs.
6. Output strict JSON matching exactly the schema given to you separately,
   with no prose outside the JSON, no markdown code fences, and no additional
   top-level keys.

Produce your answer now as a single JSON object matching the supplied schema.
```

## Fixed output schema (v1, used unchanged for both cases)

```json
{
  "caseId": "string or unknown",
  "identity": {
    "sourceId": "string or unknown",
    "organization": "string or unknown",
    "fiscalYear": "number or unknown",
    "documentTitle": "string or unknown",
    "documentStage": "string or unknown",
    "targetLocation": "string or unknown (page/printed-label locator)",
    "evidence": ["eventId or feature key, ..."]
  },
  "methodsAndEngines": [
    { "name": "string", "description": "string", "evidence": ["..."] }
  ],
  "experimentsAndInterventions": [
    { "summary": "string", "kind": "intervention|experiment", "date": "string or unknown", "commit": "string or unknown", "evidence": ["..."] }
  ],
  "importantSuccesses": [
    { "summary": "string", "evidence": ["..."] }
  ],
  "importantFailures": [
    { "summary": "string", "evidence": ["..."] }
  ],
  "historicalBenchmarkResults": [
    {
      "summary": "string",
      "isSuperseded": true,
      "supersededBy": "eventId or unknown",
      "date": "string or unknown",
      "evidence": ["..."]
    }
  ],
  "currentBenchmarkResults": [
    {
      "summary": "string",
      "supersedes": "eventId or unknown",
      "date": "string or unknown",
      "evidence": ["..."]
    }
  ],
  "methodologyCorrections": [
    { "summary": "string", "correctedEventId": "string or unknown", "evidence": ["..."] }
  ],
  "currentSupportedConclusions": [
    { "summary": "string", "evidence": ["..."] }
  ],
  "hypotheses": [
    { "summary": "string", "status": "string or unknown", "evidence": ["..."] }
  ],
  "unresolvedQuestions": [
    { "summary": "string", "evidence": ["..."] }
  ],
  "proposedNextInvestigation": {
    "summary": "string or unknown",
    "rationale": "string or unknown",
    "evidence": ["..."]
  },
  "explicitUnknowns": ["list of schema fields or facts the supplied files did not support"]
}
```

## Freezing statement

This prompt and schema were written and committed to this repository before either reconstruction run was executed, and were not edited after seeing case-001's or case-002's output. The only per-case substitution permitted is the literal file contents pasted into the two `<<<PASTE EXACT FILE CONTENTS HERE>>>` placeholders — no other wording differs between the two runs.
