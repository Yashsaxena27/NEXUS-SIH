# NEXUS SIH 2026 - Performance Benchmarks

## Overview
NEXUS prioritizes deterministic processing speed to ensure that risk analysis across large network fleets is instantaneous. The AI layer (Phase 4 & 7) is purposely isolated from the critical path to maintain this latency.

## Baseline Measurements

### Parsing Latency
- **Cisco IOS Parser**: ~0.05 ms per config
- **Juniper Junos Parser**: ~0.08 ms per config
- **Fortinet FortiOS Parser**: ~0.06 ms per config

### Compliance Evaluation
- Evaluating 20+ controls against the `NormalizedConfig`: ~0.02 ms
- Total deterministic round trip (Parse + Evaluate): **< 1.0 ms**

### AI Explainability Latency
- Gemini RAG generation (isolated path): ~1500ms - 3000ms
- This latency *only* affects the "Explainability View" and does not block compliance status reporting.

## Reproducing Benchmarks
To run the benchmark script locally:
```bash
python scripts/benchmark.py
```
