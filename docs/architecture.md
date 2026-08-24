# Architecture

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend (React)                        │
│  Dashboard │ Devices │ Findings │ Training │ Reports │ Copilot  │
└──────────────────────────────┬──────────────────────────────────┘
                               │ REST API (FastAPI)
┌──────────────────────────────┴──────────────────────────────────┐
│                          API Layer                              │
│  /configs/upload  /scans  /findings  /training  /reports        │
└──────────────────────────────┬──────────────────────────────────┘
                               │
    ┌──────────────────────────┼──────────────────────────┐
    │                          │                          │
    ▼                          ▼                          ▼
┌─────────┐          ┌──────────────┐          ┌──────────────┐
│Ingestion│          │  Compliance  │          │   AI / RAG   │
│         │          │   Engine     │          │              │
│ Upload  │          │ Deterministic│          │ Explanation  │
│ Detect  │          │ PASS/FAIL/UNK│          │ Remediation  │
│ Parse   │          │ Risk Scoring │          │ Copilot      │
└────┬────┘          └──────┬───────┘          └──────┬───────┘
     │                      │                         │
     ▼                      ▼                         ▼
┌──────────────────────────────────────────────────────────────┐
│              Vendor-Neutral Security IR (Pydantic)           │
│                                                              │
│  DeviceInfo │ ManagementConfig │ AuthConfig │ LoggingConfig  │
│  SNMPConfig │ TimeConfig │ ServicesConfig │ AccessControl    │
└──────────────────────────────────────────────────────────────┘
     ▲                      ▲
     │                      │
┌────┴────────┐    ┌────────┴────────┐
│   Vendor    │    │    Adaptive     │
│  Adapters   │    │   Learning     │
│             │    │                │
│ Cisco       │    │ Unknown detect │
│ Juniper     │    │ AI hypothesis  │
│ Fortinet    │    │ Human confirm  │
│ PaloAlto    │    │ Store mapping  │
└─────────────┘    └────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                     PostgreSQL (pgvector-ready)               │
│  devices │ scans │ findings │ training_mappings │ audit_logs  │
└──────────────────────────────────────────────────────────────┘
```

## Key Design Decisions

### 1. Deterministic Compliance, AI Explanation
The compliance engine uses deterministic rules (YAML-defined controls) to produce
PASS/FAIL/UNKNOWN verdicts. The LLM explains WHY, never decides IF.

### 2. Vendor-Neutral IR
All vendor configs map to a single NormalizedConfig schema. This decouples vendor
parsing from compliance evaluation — new vendors only need an adapter.

### 3. Three-Valued Logic
Every compliance check has three outcomes: PASS, FAIL, UNKNOWN.
UNKNOWN means insufficient evidence — no guessing.

### 4. Evidence Chain
Every normalized property carries provenance: source line, confidence score,
extraction method, raw evidence. This enables auditable compliance.

### 5. Provider-Agnostic AI
The AI layer abstracts over LLM providers (Gemini/OpenAI/Claude).
Switching providers requires zero code changes.

### 6. Human-in-the-Loop Learning
Unknown configurations are flagged for human review, not silently ignored
or auto-classified. The system learns from human feedback without retraining.

## Module Boundaries

| Module | Input | Output | Dependencies |
|--------|-------|--------|-------------|
| Ingestion | Raw file/text | Raw config string | None |
| Vendor Detection | Raw config | VendorDetectionResult | None |
| Normalization | Raw config + vendor | NormalizationResult | Security IR schema |
| Compliance Engine | NormalizedConfig + Controls | ComplianceReport | Security IR, Controls YAML |
| Risk Scoring | ComplianceFindings | Risk score | Compliance models |
| AI Explanation | Finding + Evidence | Explanation text | LLM provider |
| RAG | Query | Relevant documents | Vector DB |
| Adaptive Learning | Unknown commands | Training mappings | LLM + human |
| Reporting | ComplianceReport | PDF file | All above |
