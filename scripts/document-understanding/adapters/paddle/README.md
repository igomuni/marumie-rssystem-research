# PaddleOCR / PP-StructureV3 — investigation notes (not yet integrated)

Status: **not implemented**. Documentation-only investigation.

## Package

- PyPI: `paddleocr` (verified available: latest `3.7.0` at investigation time). PP-StructureV3 is the document-structure-recognition pipeline bundled within PaddleOCR 3.x (layout detection + table recognition + reading order).
- Requires the separate `paddlepaddle` framework as a hard dependency (verified available: latest `3.3.1`) — this is a full deep-learning framework (PaddlePaddle), not a lightweight library, analogous to needing `tensorflow` or `torch` installed as its own large dependency, except it is Baidu's own framework rather than one already present in this repository's toolchain.

## Installation method

```bash
pip install paddlepaddle   # CPU wheel
pip install paddleocr
```

PP-StructureV3's layout/table/OCR models are downloaded on first use.

## Runtime requirements

- CPU-only `paddlepaddle` wheels exist and are the documented path when no CUDA GPU is present.
- Historically, `paddlepaddle`'s official wheel support for Apple Silicon (`arm64`/macOS) has lagged behind its Linux/CUDA and x86 support, with community reports of needing to build from source or use a Docker/x86 emulation workaround on some macOS/ARM configurations in the past. Availability of a working `arm64` macOS wheel at `paddlepaddle==3.3.1` was not independently verified beyond confirming the package version exists on PyPI (`pip index versions` does not confirm wheel platform coverage).

## CPU / Mac M4 feasibility

Least certain of the three:

- Adds an entire second deep-learning framework to the toolchain purely for one benchmark engine, a heavier dependency-surface cost than either alternative.
- Apple Silicon wheel maturity/reliability for `paddlepaddle` needs to be verified empirically (attempted install + smoke test) before committing to this path, not assumed from a PyPI version listing alone.

## Expected outputs

PP-StructureV3 produces structured layout output (text regions, table regions with cell structure, reading order) as JSON, and can render an HTML/Markdown reconstruction of detected tables. Broad multi-language OCR support including Japanese.

## Where it would plug into the benchmark interface

Same adapter shape as Docling/MinerU would: `run.py` reading case config, invoking the PP-StructureV3 pipeline on the locked PDF's target page, emitting structured output into the shared raw-artifact shape.

## Recommendation

Not recommended as the next integration target, mainly on installation-risk grounds: it requires standing up a second full deep-learning framework whose Apple-Silicon reliability is unverified in this environment, for capability (table/layout structure recognition) that Docling already offers with a lighter, better-verified-for-this-platform dependency footprint. Worth reconsidering if Docling's table-structure recognition proves insufficient in practice, or if a project requirement specifically needs PaddleOCR's language/model coverage.
