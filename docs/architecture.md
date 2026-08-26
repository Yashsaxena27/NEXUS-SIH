# NEXUS Architecture Guide

## High-Level Design Principles

NEXUS is built around a single, non-negotiable architectural rule:
**"The deterministic engine is the source of truth. AI is only an explanation/assistance layer."**

This principle dictates the separation of concerns across the platform, ensuring compliance findings are 100% reproducible, verifiable, and free from AI hallucinations.

## System Components

### 1. Data Ingestion & Vendor Detection
*   **Input:** Raw network configuration files (text).
*   **Detector:** A heuristic and keyword-based engine (`VendorDetector`) identifies the vendor (Cisco, Juniper, Fortinet, Palo Alto) or gracefully degrades to `UNKNOWN`.

### 2. Normalization Engine
*   **Process:** Transforms vendor-specific syntax into a standard Internal Representation (IR).
*   **Fallback:** If a feature isn't recognized or the vendor is unknown, the system preserves the raw lines under an `UNKNOWN` category rather than dropping them, ensuring zero data loss during parsing.

### 3. Deterministic Compliance Engine
*   **Engine (`ComplianceEngine`):** Evaluates the normalized IR against hardcoded, verifiable rules (e.g., SSH version, password encryption).
*   **Output:** Generates definitive pass/fail findings with a deterministic risk score.

### 4. Vulnerability Intelligence
*   **Intelligence:** Evaluates known CVEs for the parsed devices. 
*   **Note:** Demo vulnerability intelligence is backed by a deterministic mock provider to ensure offline reliability and reproducibility during demonstrations.

### 5. AI & Intelligence Layer (Decoupled)
*   **Kill Switch:** The entire AI layer sits behind a global kill switch (`ai_enabled` setting). If disabled, the system relies exclusively on deterministic outputs.
*   **Provider Abstraction:** The `BaseLLMProvider` interface allows switching between `GeminiProvider`, `LocalLLMProvider` (Ollama), and `DisabledProvider`.
*   **Redaction (`ConfigRedactor`):** All raw configurations are scrubbed of secrets (passwords, hashes, API keys) via Regex and Entropy checks *before* ever being passed to an LLM.
*   **RAG Engine:** Uses a localized vector store to retrieve authoritative compliance controls (NIST, CIS) and ground AI explanations, drastically reducing hallucinations.

### 5. API & Frontend
*   **Backend:** FastAPI provides robust, typed endpoints.
*   **Frontend:** React/Vite dashboard provides visualization (Attack Graphs, CSV/PDF Export, Compliance posture).

## Persistence Layer
*   **Database:** SQLite using SQLAlchemy + async drivers.
*   **Schema:** Stores Scan Records, Findings, Adaptive Rules (human-in-the-loop overrides), RAG Documents, and App Settings.

## Workflow Execution
1.  User uploads config -> API validates size/format.
2.  `ScannerService` detects vendor -> Normalizes -> Evaluates compliance.
3.  Findings are persisted to DB.
4.  User queries AI (Chat or Explain) -> System redacts config -> Fetches RAG context -> LLM generates response -> Displayed in UI.
