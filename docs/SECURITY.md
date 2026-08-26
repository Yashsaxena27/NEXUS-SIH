# Security & Threat Model

NEXUS is designed with a defense-in-depth approach, assuming that AI components are inherently untrusted and network configurations are sensitive assets.

## 1. Zero-Trust AI Boundaries

### 1.1 Deterministic Primacy
LLMs have a tendency to hallucinate. To prevent a hallucination from marking a vulnerable network as secure, **AI is never permitted to determine the compliance status of a control**. 
*   Status (`PASS`/`FAIL`), Risk Score, and Compliance Mapping are 100% computed by the deterministic engine.
*   AI is used exclusively for *Explanation* and *Contextual Remediation*.

### 1.2 The AI Kill Switch
In highly sensitive environments, external LLM calls may violate data residency policies. The platform includes a **Global AI Kill Switch** (`ai_enabled`). When flipped, NEXUS falls back to deterministic outputs, completely neutralizing any LLM-related surface area.

### 1.3 Secret Redaction
Network configs often contain passwords, SNMP strings, and API keys. The `ConfigRedactor` module runs *before* any data is sent to the AI, scrubbing:
*   IPv4/IPv6 Addresses
*   Common Secret Keys
*   High-entropy strings
*   Vendor-specific password hashes (e.g., Cisco Type 5/7).

## 2. Prompt Injection Defense

Malicious actors might embed prompt injection payloads inside a network configuration (e.g., in a MOTD banner) hoping the AI will execute it during analysis.
NEXUS implements multiple layers of defense against this:
1.  **Input Sanitization:** Stripping known injection control characters.
2.  **Strict System Prompts:** Bounding the AI's role strictly to network security analysis and explicitly instructing it to ignore contradictory embedded instructions.
3.  **Heuristic Analysis:** The parser detects suspicious structures (e.g., `IGNORE ALL PREVIOUS INSTRUCTIONS`) and flags the payload deterministically before AI processing.

## 3. Data Integrity & Audit

NEXUS incorporates mechanisms to ensure the integrity of scan results:
*   **Cryptographic Hashing:** Findings are hashed using SHA-256.
*   **Tamper Detection:** The audit log detects unauthorized modifications to the database by verifying hash chains.

## 4. ReDoS (Regular Expression Denial of Service)
To prevent ReDoS attacks from maliciously crafted, infinitely looping regex evaluations during parsing, NEXUS enforces strict payload limits:
*   Maximum file size limit (5MB).
*   Maximum line length limits.
