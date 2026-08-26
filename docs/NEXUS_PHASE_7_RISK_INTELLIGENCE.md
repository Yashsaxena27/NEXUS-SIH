# NEXUS Phase 7: Risk Intelligence & Analytics

## Overview
Phase 7 introduces advanced risk prioritization, explainable scoring, and remediation intelligence to the NEXUS platform. This ensures that when a security vulnerability is identified, it is properly weighted by its severity, exposure, and asset criticality. Furthermore, the AI is now contextually aware of these risk factors.

## Key Changes
1. **Multi-Factor Risk Scoring (`scoring.py`)**
   - Added `calculate_prioritized_risks()` to group findings by category and sort them by severity weight.
   - Introduced `asset_criticality` and `exposure_factor` into the risk calculation loop.

2. **Compliance Engine Updates (`engine.py`, `models.py`)**
   - Augmented `ComplianceReport` with `prioritized_risks` and `correlation_summary`.
   - Engine passes the new risk parameters into the risk calculator.

3. **Explainable Risk Scoring (`prompts.py`, `ai.py`, `gemini_provider.py`)**
   - Updated the LLM explanation prompt to inject `asset_criticality` and `exposure_factor`.
   - Modifed the API route and interfaces to pass these arguments seamlessly to the LLM.

4. **Remediation & Compliance Mapping (`knowledge_base.json`, `network_controls.yaml`)**
   - Added remediation intelligence and guidance directly into the deterministic controls (e.g. `NET-SSH-004`, `NET-SNMP-001`, `NET-HTTP-001`).
   - Added new source text into the RAG knowledge base for enhanced contextual alignment.

5. **Security Posture Dashboards (Frontend)**
   - Correlated risks and priorization displayed elegantly in `ScanResultPage.jsx`.
   - `FindingDetailPage.jsx` effectively isolates deterministic reasoning from the AI explanation.

## Test Validation
The test suite has been updated to cover the new prompt injection scenarios, including mock tests verifying that the risk context is securely passed.
