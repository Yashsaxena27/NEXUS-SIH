# NEXUS SIH 2026

**AI-Driven Multi-Vendor Network Security Compliance Auditor**

NEXUS is an enterprise-grade, deterministic-first network security compliance engine designed for the Smart India Hackathon (SIH) 2026. It seamlessly analyzes network configurations across diverse vendors (Cisco, Juniper, Fortinet, Palo Alto) against global cybersecurity frameworks (CIS, NIST, ISO 27001, CERT-In).

## 🚀 Key Features

*   **Deterministic Core:** The compliance engine uses a deterministic, rule-based methodology to ensure 100% reliable, reproducible, and verifiable findings. AI is *strictly* decoupled from decision-making.
*   **Multi-Vendor Support:** Natively parses configurations from Cisco IOS, Juniper Junos, Fortinet FortiOS, and Palo Alto PAN-OS.
*   **Zero-Trust AI Architecture:** 
    *   **Global Kill Switch:** AI can be completely disabled without affecting the core scanning pipeline.
    *   **Provider Abstraction:** Supports Google Gemini, Local LLMs (Ollama/Llama 3), and a fully air-gapped `DisabledProvider`.
    *   **Secret Redaction:** Passwords, hashes, and API keys are automatically redacted *before* any data reaches external APIs.
    *   **Prompt Injection Defense:** Input sanitization and heuristic detection block malicious payloads.
*   **Advanced Intelligence:**
    *   **RAG (Retrieval-Augmented Generation):** Grounded AI explanations using authoritative CIS/NIST documentation stored in an embedded Vector DB (SQLite-based for portability).
    *   **Attack Path Graphing:** Visualizes cascading risks and lateral movement vectors by correlating vulnerabilities with misconfigurations.
    *   **Context-Aware Chat:** Natural language interrogation of scan results.
*   **Enterprise Polish:** CSV Export, PDF Reporting, Delta Comparisons, and Adaptive Learning (Human-in-the-Loop overrides).

## 🏗️ Quick Start

### 1. Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Set up environment variables
# Note: Gemini API key is required if using the Gemini provider. 
# Alternatively, set the provider to 'local' or 'disabled' in the UI settings.
set GEMINI_API_KEY="your_api_key_here"

# Run the FastAPI server
uvicorn backend.app.main:app --reload --port 8000
```

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### 3. Seed Demo Data
To populate the database with comprehensive test scenarios (including clean configs, misconfigurations, multi-vendor examples, and prompt injection attacks), run:
```bash
python scripts/seed_demo.py
```

## 🧪 Testing

NEXUS maintains a robust test suite covering end-to-end lifecycles, compliance mappings, AI kill switches, and security boundaries. Currently at **100/100 tests passing**.

```bash
cd backend
pytest backend/tests/ -v
```

## 📖 Documentation

*   [Architecture Guide](docs/ARCHITECTURE.md)
*   [Security & Threat Model](docs/SECURITY.md)
*   [Demo Guide](docs/DEMO_GUIDE.md)

## 🏆 SIH Readiness
NEXUS is designed to showcase an enterprise-ready posture, balancing cutting-edge LLM capabilities with the rigorous security boundaries demanded by critical infrastructure environments.
