# Start Here

This document tells a new AI or human session exactly how to resume this research project.

> Chat history is not the canonical project state. Files in this repository are.

## Resume process

1. Read `AGENTS.md` (AI agent working contract: guardrails, provenance rules, artifact naming, Git/validation summary)
2. Read `protocol/RESEARCH_PROTOCOL.md`
3. Read `state/CURRENT_STATE.json`
4. Read `protocol/DECISIONS.md`
5. Read `state/TODO.md`
6. Load only the evidence/reports/snapshots needed for the current `nextAction`
7. Do not infer missing historical facts from chat memory
8. Maintain source provenance for new research
9. At the end of a research phase, update the handoff state
10. Do not commit or push unless the user explicitly performs/authorizes it (see `protocol/RESEARCH_PROTOCOL.md`'s Git / Commit Policy for how authorization currently works)
