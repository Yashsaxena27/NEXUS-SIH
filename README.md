# NEXUS — AI-Driven Multi-Vendor Network Security Compliance Auditor

> **AI interprets. Deterministic rules decide.**

NEXUS transforms heterogeneous network configurations into a common security model,
continuously validates them against security standards, and learns to interpret
previously unseen vendor configurations through human-guided AI adaptation.

## Architecture

```
Raw Configuration → Vendor Detection → Parsing → Vendor-Neutral IR → Compliance Engine → PASS/FAIL/UNKNOWN → Risk Scoring → AI Explanation → Remediation → Report
```

## Supported Vendors

| Vendor | Platform | Device Type | Config Format |
|--------|----------|-------------|---------------|
| Cisco | IOS / IOS-XE | Router, Switch | Hierarchical CLI |
| Juniper | Junos | Firewall, Router | Brace-delimited hierarchy |
| Fortinet | FortiOS | Firewall | config/end blocks |
| Palo Alto | PAN-OS | Firewall | Flat `set` commands |

## Quick Start

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt

# Run tests
python -m pytest tests/ -v

# Start API server
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Project Structure

```
├── backend/           # Python FastAPI backend
│   ├── app/
│   │   ├── schemas/   # Pydantic models (Security IR)
│   │   ├── normalization/  # Vendor adapters
│   │   ├── compliance/     # Deterministic rule engine
│   │   ├── vendors/        # Vendor detection
│   │   ├── risk/           # Risk scoring
│   │   ├── ai/             # LLM abstraction
│   │   ├── rag/            # Knowledge retrieval
│   │   ├── training/       # Adaptive learning
│   │   └── reporting/      # PDF reports
│   └── tests/
├── frontend/          # React + TypeScript dashboard
├── dataset/           # Sample configs + ground truth
├── compliance/        # Compliance control definitions (YAML)
├── evaluation/        # Benchmark scripts
└── docs/              # Documentation
```

## Core Principle

The compliance engine operates on a **vendor-neutral security intermediate representation**.
Different vendor configurations map into the SAME schema, and the SAME deterministic rules
evaluate them all. AI is used only for interpretation and explanation — never for compliance decisions.

## Team

Built for SIH 2026 — Problem Statement 26155 (NTRO)
