# NEXUS Phase 5 Adaptive Learning

## 1. Objective
To introduce a Human-in-the-Loop (HITL) capability where security engineers can resolve `UNKNOWN` findings. Once an engineer maps an unknown configuration snippet to a structured control state, the deterministic engine prioritizes this mapping in all future scans.

## 2. Architecture & Design
The Adaptive Learning system sits *before* the Compliance Engine, effectively patching the Vendor Parsers dynamically.

### Database
A new table `adaptive_rules` was added:
- `id` (UUID)
- `vendor` (e.g., cisco, juniper, all)
- `raw_pattern` (e.g., `crypto key rsa 2048`)
- `mapped_control` (e.g., `management.ssh.enabled`)
- `mapped_value_json` (e.g., `True`)
- `status` (APPROVED)

### API Endpoints
- `POST /api/v1/adaptive/submit`: Allows engineers to submit a new rule mapping.
- `GET /api/v1/adaptive/rules`: Returns all stored adaptive rules.

### Normalization Pipeline Injection
When `POST /api/v1/scans/scan` or `/upload` is called:
1. The backend fetches all `APPROVED` adaptive rules.
2. These rules are passed into `normalize_config` and subsequently down to the `BaseVendorAdapter`.
3. The adapter executes its standard parsing first.
4. Then, `_apply_adaptive_rules` is executed. It scans the raw configuration for the `raw_pattern`. If found, it dynamically walks the `NormalizedConfig` tree using the `mapped_control` path (e.g., `management.ssh.enabled`) and overrides the value with `mapped_value_json`.
5. It injects a `PropertyEvidence` record with `method=InterpretationMethod.HUMAN_MAPPED`, ensuring the Compliance Engine treats it with the highest confidence.

## 3. Strict Safety Boundaries
This system adheres to the core architecture principles:
- The LLM is **NOT** generating these rules autonomously.
- The LLM is **NOT** changing the parser logic.
- A human engineer creates the deterministic mapping.
- The mapping is purely deterministic (exact substring match).
- This keeps the system completely predictable and audit-safe.

## 4. Status
- [x] Database Schema implemented
- [x] API Endpoints implemented
- [x] Normalizer integration implemented
- [x] Vendor Adapters updated

**Phase 5 Complete.**
