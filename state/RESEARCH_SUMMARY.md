# Research Summary (through Phase 15)

This is a concise, information-dense summary of the FY2024 Digital Agency / MOF / RS investigation completed prior to Phase 1A of this repository. It is not a reproduction of every historical detail — see `protocol/RESEARCH_PROTOCOL.md` and `protocol/DECISIONS.md` for the durable rules this research established.

## Core research subject

FY2024 / R6 Digital Agency:

```text
情報通信技術調達等適正・効率化推進費
```

Investigated across:

- Digital Agency request documents
- important-policy request documents
- enacted budget
- supplemental budget
- MOF settlement
- RS System data
- ministry-side request documents
- Administrative Review topology

## Major confirmed totals

Recorded as validated research facts (all figures in thousand yen unless noted):

```text
Digital Agency normal request                448,267,326
system-related important-policy request       118,772,628
effective/system-related request total        567,039,954
initial enacted budget                        480,327,293
supplement net                                205,412,304
budget after supplement                       685,739,597
MOF current appropriation                     896,995,541
MOF paid/executed                             636,331,790
next-year carryover                           238,316,675
unused                                          22,347,075
transfer to ministries                        509,690,849
```

Also:

- Digital Agency retained amount: approximately 176,048,747 thousand yen
- Transfer share: approximately 74.3%

## Strong parent-project proof

RS parent PID:

```text
000004
情報システムの整備（情報通信技術調達等適正・効率化推進費）
```

Key observation:

```text
予備費等 = -509,690,849,950 yen
```

This nearly matches the MOF transfer amount. The parent execution also closely matches the Digital Agency MOF paid amount.

Interpretation: strong evidence that the RS parent functions as a budget container, and that the generic `予備費等` field contains transfer-related adjustment in this case.

## Child-project observation

- 239 child projects were identified under the target phrase.
- 198 had FY2024 2-1 rows.
- All 198 had FY2024 current appropriation zero.
- 167 had positive execution.
- Their execution total was approximately 562.298 billion yen.

Interpretation: child ReviewProjects may show execution while having no independently allocated child budget. This is not automatically an accounting anomaly (see ADR-006).

## MHLW golden case

MHLW Digital Agency normal request:

```text
16,653,821 thousand yen
```

Exact bucket decomposition:

```text
026     89,088
027     72,051
028  7,738,305
029  5,425,940
030  2,477,089
031     30,241
032    821,107
```

Phase 12 strict normal-like RequestComponent coverage:

```text
6,471.662m / 16,653.821m = 38.86%
```

Important-policy direct evidence subtotal identified later:

```text
2,488m
```

Do not imply full ministry allocation from these figures.

## Review topology finding

Administrative Review topology changes across years. Review-2024 and Review-2025 do not contain identical project sets. Review-2025 can expose FY2024 execution that was absent from the earlier snapshot.

Therefore:

```text
latest snapshot != historical truth
```

Snapshot metadata must be versioned (see ADR-005).

## Canonical conceptual model

```text
Concept / Request
    ↓
Budget Item
    ↓
Ledger Bucket
    ↓
Request Component
    ↓
Budget Container / Transfer / Account
    ↓
System Entity
    ↓
Review Project Version
    ↓
Settlement / Execution
    ↓
Payment / Contract / Re-subcontract
```

Not every budget item requires every layer.

## Phase 15 generalization

Three observed budget-allocation patterns:

```text
010 Digital Agency Common Cost           -> common_cost_nonallocation
015 Digital Society Formation Promotion  -> policy_portfolio
020 ICT Procurement Optimization         -> central_pool_transfer
```

Proposed conceptual `allocationMode` candidates:

```text
direct_partition
policy_portfolio
common_cost_nonallocation
central_pool_transfer
partial_allocation
umbrella_with_children
```

This classification is a research hypothesis / design direction, not yet a production schema.
