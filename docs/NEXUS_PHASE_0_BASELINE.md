# NEXUS Phase 0 Baseline Report

## 1. Current Architecture
- **Frontend**: React 19 + Vite + React Router (Client-side rendering). Located in `frontend/`.
- **Backend API**: FastAPI. Located in `backend/app/`.
- **Database**: SQLite (`nexus.db`), despite `architecture.md` claiming PostgreSQL. Uses SQLAlchemy.
- **Upload / Scan Pipeline**: 
  - Raw Config Upload (`/api/v1/scans/upload`, `/api/v1/scans/scan`)
  - Vendor Detection (`backend/app/vendors/detector.py`)
  - Parser / Normalization (`backend/app/normalization/*_adapter.py`)
  - Security IR (`backend/app/schemas/security_ir.py`)
  - Compliance Engine (`backend/app/compliance/`)
- **AI Integration**: Gemini Provider for explanations and remediation (`backend/app/llm/gemini_provider.py`). Configured via `api/endpoints/ai.py`.
- **Redaction**: Present (`backend/app/llm/redactor.py`), intercepts config before AI calls.

## 2. Current Features
- **Implemented & Working**:
  - Cisco, Juniper, Fortinet, Palo Alto basic parsing (via adapters).
  - Deterministic compliance engine using Security IR.
  - Basic SQLite persistence for scans and findings.
  - Gemini AI explanation and remediation (without altering PASS/FAIL).
  - Simple API endpoints for scan upload and result retrieval.
  - ConfigRedactor for scrubbing basic secrets.
- **Missing or Not Implemented (Despite Claims)**:
  - Backend Authentication and Authorization (RBAC).
  - PostgreSQL (using SQLite instead).
  - RAG / Vector DB integration.
  - Adaptive Learning (Human-in-the-loop).
  - PDF Generation within the API (some scripts exist in `sih_report/` but not integrated).
  - Audit logs, user management, fleet/device models.
  - Continuous compliance & drift detection.

## 3. Current Limitations
- **Security**: No authentication on API endpoints. Potential XSS vulnerabilities if frontend doesn't sanitize AI output. Untrusted uploads are handled basically but could lack strict typing/validation.
- **Testing**: `test_upload.py` errors out due to a missing `async_client` fixture in `conftest.py`. No frontend tests exist.
- **Documentation**: `architecture.md` overclaims capabilities (PostgreSQL, RAG, Adaptive Learning).

## 4. Test Results
- **Total Tests**: 56 backend tests (0 frontend tests)
- **Passed**: 52
- **Errors**: 4 (`test_upload.py` due to missing fixture)
- **Failed**: 0

## 5. Benchmark Results
- **Synthetic Benchmark (44 samples)**:
  - Normalization Accuracy: 88.4%
  - Unknown Rate: 9.2%
  - Compliance Precision: 100.0%
  - Compliance Recall: 98.3%

## 6. Security Findings
- No backend authentication (all endpoints are public).
- Secrets and tokens need checking across the repository (e.g. `.env` loading, hardcoded keys).
- AI prompt boundary exists (redaction in place), but frontend rendering of AI output needs verification against XSS.
- Upload limits are enforced (5MB), but further security checks on filenames/paths might be needed.

## 7. Recommended Fixes for Phase 1–3
- **Phase 1**: Add basic JWT authentication. Secure API endpoints. Verify AI output rendering in frontend to prevent XSS. Check for secret leakages. Fix `test_upload.py` error.
- **Phase 2**: Update `README.md` and `architecture.md` to accurately reflect the SQLite database, missing RAG/Adaptive learning, and other missing features. Group them into a "Future Roadmap" section.
- **Phase 3**: Improve parser edge cases. Strengthen vendor detection to prevent false positives. Ensure IR correctly maps concepts. Maintain deterministic evaluation. Re-run benchmark to ensure metrics stay stable or improve.
