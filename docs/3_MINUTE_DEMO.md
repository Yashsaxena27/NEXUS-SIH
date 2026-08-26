# NEXUS SIH 2026 - 3-Minute Demo Script

## 0:00 - 0:30: Introduction & The Problem
**Goal:** Hook the judges.
- "Modern enterprise networks are complex, multi-vendor, and prone to misconfigurations. A single missed access control list or default password can lead to a massive breach."
- "Security teams struggle because every vendor uses different syntax, and legacy auditing tools rely on brittle, error-prone regular expressions."

## 0:30 - 1:15: The NEXUS Solution (Phase 1-3)
**Goal:** Show the deterministic engine.
- Open the Dashboard.
- Upload `demo/hero/cisco_vulnerable.cfg`.
- **Show:** The system instantly detects the vendor (Cisco) and parses the configuration deterministically in under 1 millisecond.
- **Highlight:** Secret redaction. Show that the password hash in the raw config was redacted to `<SECRET_REDACTED>` before being analyzed, protecting sensitive data.

## 1:15 - 2:00: AI & Evidence (Phase 4)
**Goal:** Show RAG and explainability without hallucination.
- Click into the "Telnet Enabled" critical finding.
- **Show:** The deterministic engine accurately flagged it, pointing to the exact line (`transport input telnet`).
- Click "Explain with AI".
- **Highlight:** The Gemini LLM explains *why* this is a risk (unencrypted credentials) using RAG knowledge grounded in CIS benchmarks, and provides the exact remediation command (`transport input ssh`). Mention: "AI explains, deterministic rules decide."

## 2:00 - 2:30: Adaptive Learning (Phase 5)
**Goal:** Show human-in-the-loop fallback.
- Point out an `UNKNOWN` finding (e.g. `ip ssh version 1.99`).
- **Show:** The system didn't guess or hallucinate—it safely deferred to UNKNOWN.
- Create an Adaptive Rule mapping `ip ssh version 1.99` to `management.ssh.version = 2`.
- Re-scan the config. The `UNKNOWN` is resolved to a `PASS`, proving the system learns deterministically based on human input.

## 2:30 - 3:00: Conclusion & Architecture
**Goal:** Close strong.
- **Show:** The Scan Comparison page to prove how a configuration improved over time.
- **Summary:** "NEXUS provides 100% deterministic security auditing with 0% AI hallucination risk, while utilizing the latest in LLM technology to empower analysts and automate learning. We are ready to deploy."
