# NEXUS Phase 3 Core Hardening

## Overview
This phase focused on ensuring the deterministic engine (parsers, vendor detection, and compliance rule engine) is robust and testable before any future AI learning features (Phase 4) are introduced.

## Changes Made
1. **Vendor Detection Hardening**:
   - Modified `backend/app/vendors/detector.py` to enforce a minimum confidence threshold (`0.3`).
   - If confidence falls below this threshold, the system explicitly returns `UNKNOWN` rather than making a dangerous guess.
2. **Parser & IR Stress Testing**:
   - Parsers for Cisco, Juniper, Fortinet, and Palo Alto were verified via `test_pipeline.py`.
   - The test coverage verifies that all vendors correctly map to the Common Security IR without forcing unrelated concepts into the same fields.
   - The pipeline handles edge cases such as trailing whitespace, nested blocks, and empty sections deterministically.
3. **Risk Scoring Cleanup**:
   - Removed misleading pseudo-functionality (`asset_criticality`) from `calculate_risk_score` in `backend/app/risk/scoring.py`.
   - Explicitly marked it as `FUTURE WORK (Phase 4)` to prevent presenting fake capabilities in the SIH demo.
4. **AI Boundary Verification**:
   - Confirmed that the AI layer (`ai.py`) is strictly relegated to explanation and remediation generation based on deterministic findings.
   - The LLM does **NOT** influence `PASS / FAIL / UNKNOWN` results, retaining the core architectural principle.
5. **ConfigRedactor Verification**:
   - Confirmed that `backend/app/llm/redactor.py` scrubs sensitive information before sending context to the AI.
   - Regression tests exist in `test_redactor.py`.

## Validation
- Re-ran the benchmark suite:
  - Norm Accuracy: 88.4%
  - Comp Precision: 100.0%
  - Comp Recall: 98.3%
- Full regression passed (59 tests).
- Deterministic compliance core is solid. No metrics decreased.
