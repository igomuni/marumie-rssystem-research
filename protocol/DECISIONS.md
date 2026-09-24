# Research Decisions

This file records durable research-method decisions.

## Decision template

### ADR-XXX: Title
Status:
Date:
Decision:
Reason:
Rejected alternatives:
Implications:

---

### ADR-001: Repository files are canonical, chat history is not
Status: Accepted
Date: 2026-09-25
Decision: Durable research state must be serialized into this repository. Chat conversations are execution contexts, not authoritative storage.
Reason: Chat history is not reliably available across sessions or tools, and cannot be verified or diffed. Files in version control can be.
Rejected alternatives: Relying on chat/session memory as the source of truth.
Implications: Every research phase must persist its state, evidence, and decisions to files before being considered complete.
