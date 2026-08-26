# SIH 2026 Presentation Demo Guide

This guide outlines the perfect flow to demonstrate NEXUS to the Smart India Hackathon judges. It is designed to highlight the core technical achievements and enterprise readiness of the platform.

## Pre-Requisites
1. Ensure both Backend (FastAPI on port 8000) and Frontend (Vite on port 5173) are running.
2. Run `python scripts/seed_demo.py` to populate the dashboard with realistic test scenarios.

## 🎬 Act 1: The Enterprise Dashboard & Multi-Vendor Parsing
**Goal:** Show that the system handles diverse configurations seamlessly.

1.  **Open the Dashboard (`/`):** Point out the clean UI, the aggregated Compliance and Risk Scores, and the list of recent scans.
2.  **Highlight Multi-Vendor:** Show that the list includes Cisco, Juniper, Fortinet, and Palo Alto devices. Explain that the `VendorDetector` automatically identifies the vendor and the `Normalizer` translates them into a common Internal Representation (IR).
3.  **Show "UNKNOWN" Graceful Degradation:** Click on the "Unknown Vendor / Edge Case" scan. Explain how NEXUS doesn't crash when it sees alien configs; it categorizes unmapped lines as `UNKNOWN` to ensure zero data loss.

## 🎬 Act 2: Deterministic Compliance Engine
**Goal:** Prove the system relies on hard truth, not AI hallucinations.

1.  **View Findings:** Click on the "Cisco Core Router" scan.
2.  **Show Evidence:** Expand a `FAIL` finding (e.g., `SSHv2 Not Enforced`). Show the "Actual" vs "Expected" values and the exact extracted line (Evidence Field). Emphasize that this was evaluated *deterministically* without AI.

## 🎬 Act 3: AI Intelligence & Attack Graph
**Goal:** Demonstrate the decoupled AI layer and advanced risk correlation.

1.  **AI Explanation & Remediation:** Click "AI Explain" on a failed control. Show the RAG-backed explanation and remediation steps.
2.  **Attack Path Visualizer:** Navigate to the "Attack Graph" tab (`/scans/{id}/graph`). Show how vulnerabilities (CVEs) and misconfigurations are linked to the asset and exposed to the internet. Mention: *"Demo vulnerability intelligence is backed by a deterministic mock provider to ensure offline reliability."*
3.  **AI Chat:** Go to the AI Chat tab. Ask a question like *"Summarize the critical risks in this config."* Show the contextual, scan-aware response.

## 🎬 Act 4: Security Boundaries & Kill Switch
**Goal:** Win the cybersecurity judges over with defense-in-depth.

1.  **Prompt Injection Defense:** Click on the "Prompt Injection Attack" scan. Show how the deterministic engine flagged the `MOTD Banner` anomaly and refused to let the AI execute the embedded prompt injection.
2.  **The Kill Switch:** 
    *   Navigate to the **Settings** page (`/settings`).
    *   Toggle the **AI Assistance Enabled** switch to OFF.
    *   Return to a scan and click "AI Explain". Show the instant fallback message: *"AI Assistance: OFF. Deterministic rules remain fully operational."* This proves the system is enterprise-safe and air-gap ready.

## 🎬 Act 5: Enterprise Polish
**Goal:** Show that this is a finished product, not just a hack.

1.  **Scan Comparison:** Navigate to the **Compare Scans** page (`/compare`). Select a "Before" and "After" scan. Show the delta highlights in Risk Score and Compliance.
2.  **Export:** Show the Print to PDF and CSV Export functionalities on a scan detail page.
