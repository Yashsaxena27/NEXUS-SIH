# NEXUS Phase 2 Code ↔ Documentation Alignment

## Overview
This document details the adjustments made to align project documentation with the actual capabilities of the NEXUS codebase. The purpose is to ensure all claims are truthful and transparent for the SIH demo.

## Feature Status Classification

### Implemented
- Deterministic compliance engine using a YAML-based rule system.
- Parsing and normalization for Cisco, Juniper, Fortinet, and Palo Alto.
- Basic API backend with upload/scan functionalities and SQLite database.
- AI integration for explaining compliance findings and providing remediation (without overriding Pass/Fail).
- Basic Server-Side API Authentication.
- Config Redaction for basic sensitive data.

### Partially Implemented
- Risk Scoring: The models and basic scoring mechanisms exist but lack the deeper "risk intelligence" capabilities claimed in earlier documents.

### Planned (Future Roadmap)
- RAG (Retrieval-Augmented Generation)
- Adaptive Learning (Human confirm, unknown command mapping)
- PDF Reports Export
- Enterprise RBAC
- Fleet Management
- Continuous Compliance
- PostgreSQL (pgvector-ready) migration

### Not Implemented
- Blockchain features or fully autonomous compliance correction.

## Documentation Updates
1. **README.md**:
   - Updated the architecture flow diagram to reflect the current SQLite-based storage and the removal of RAG/Adaptive learning from the "Currently implemented" path.
   - Accurately labeled directory structure with "(Implemented)", "(Partially Implemented)", and "(Planned)".
2. **architecture.md**:
   - Separated the architecture into `CURRENT ARCHITECTURE` and `FUTURE ARCHITECTURE`.
   - Replaced "PostgreSQL" with "Database (SQLite)" in the current architecture block.
   - Moved Advanced AI features (RAG, Continuous Compliance, Adaptive Learning) to the planned section.

## Conclusion
The documentation now accurately mirrors the ground truth of the `NEXUS-SIH` repository. Future phases can reference this document to understand what is currently available versus what requires active development.
