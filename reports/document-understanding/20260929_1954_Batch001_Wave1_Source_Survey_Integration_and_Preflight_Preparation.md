# Batch-001 Wave 1 Source Survey Integration and Preflight Preparation

Date: 2026-09-29 (Asia/Tokyo)

## 1. Scope and separation

This report integrates the completed A01/A02 authority-local source surveys into the frozen Batch parent and prepares, but does not freeze, authority-specific preflight decision spaces. Survey-observed facts, proposed decisions, and future frozen decisions remain separate.

## 2. Audited integration

The parent began at `d103e802f0cff13cd98ceba24afbacff1c7591ba`. A01 survey commit `e095bda4231d472ac88df02477e026c3988e9f9a` and A02 survey commit `022aff3c866d64dcd93efee0df86fb0c19098bc1` were each audited before integration: each changed only its expected authority-local JSON and Markdown survey artifacts. Their shared-input, source-lock/registry, and script paths were unchanged. The authority commits were cherry-picked individually, not branch-merged.

After integration, each JSON and Markdown artifact was byte-identical to its authority commit. The selection manifest, sampling procedure, Batch design/template, Canonical Semantic Extraction Protocol, source lock/registry, and Cases 001–010 remain unchanged.

## 3. Source identity and admissibility

| Authority | Locked source | Pages | Survey status | Lock match | Caveat |
|---|---|---:|---|---|---|
| A01 kunaicho | `r06-02.pdf`, `ffab15073beb2411d9396f7ca0cbb1ce33ccdf99be05e6d0d88e29366912e261` | 33 | `ADMISSIBLE_FOR_PREFLIGHT` | PASS | none reported |
| A02 shugiin | `kaikei-saishutsugaisan6.pdf`, `30d0dfc363a1f4f7e37b64a0059b48c2f03f13f997eb251e7ef5acaabd37c435` | 36 | `ADMISSIBLE_WITH_CAVEATS` | PASS | current landing page alone did not establish historical FY2024 direct-link placement |

The A02 caveat remains bounded: the official-domain direct PDF, its internal FY2024 title, and locked byte identity are confirmed; the current landing-page historical placement is not claimed.

## 4. Observed comparison, not a shared profile

Both surveys observed a single canonical PDF, native text, unencrypted A4 landscape pages, no reported raster image objects, opening detailed-ledger `千円`, standard-ledger material, and remarks-side nested structures. These common observations do not justify one shared profile.

A01 has a single-file 皇室費 source with sampled `皇（皇）` prefix and nested remarks-side material. A02 has a separately caveated direct-file provenance pathway, sampled `国（衆）` prefix, and later local `百万円` tables in its remarks-side structures. Exact grammar boundaries, safe context lookback, and unit inheritance have not been established for either authority.

## 5. Preflight preparation matrix

| Decision area | A01 proposal status | A02 proposal status |
|---|---|---|
| canonical source/file scope | supported by survey | supported by survey; retain provenance caveat |
| native-text/OCR handling | native text; no default OCR escalation | native text; no default OCR escalation |
| grammar partitions | targeted structural inspection needed | targeted structural inspection needed |
| context inheritance | cross-page/file prohibited unless evidenced | cross-page/file prohibited unless evidenced |
| unit handling | main `千円` distinct from nested material | main `千円` distinct from local `百万円` tables |
| ambiguity and provenance | governed conservative defaults | governed conservative defaults |

Both authorities are **`READY_WITH_TARGETED_INSPECTION`**, not profile-frozen. The next task may perform only predeclared structural boundary/context/unit inspection before freezing the two authority profiles; it must not enumerate candidates.

## 6. Non-actions and next task

No new source acquisition, PDF inspection, candidate enumeration, canonical extraction, GT, benchmark, OCR experiment, CSV, MOF, parser/normalizer/evaluator change, or Wave 2 work was performed in this integration task. No source-lock/registry mutation was needed because both survey SHA values match existing locks.

Recommended next task: **Batch-001 Wave 1 Authority Preflight Profile Freeze — A01 and A02**, with the narrowly stated targeted structural inspection needs from the two preparation artifacts.
