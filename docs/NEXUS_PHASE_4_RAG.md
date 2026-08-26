# NEXUS Phase 4 RAG Architecture & Design

## 1. Objective
To upgrade the AI explanation from generic LLM knowledge to grounded, evidence-based security explanations utilizing curated knowledge sources (NIST, CIS, vendor manuals).

## 2. Architecture Decision: Vector Storage
**Decision:** We will use a standard SQLite table (`rag_documents`) augmented with a JSON column for the vector embedding, alongside a pure Python cosine similarity implementation.
**Reasoning:** The user explicitly warned against an unnecessary PostgreSQL/pgvector migration. A simple SQLite + Python setup is zero-dependency, extremely lightweight, and perfectly handles the O(100s) chunks of curated security knowledge base we are creating. 

## 3. Knowledge Base Scope
The knowledge base will be seeded from a curated `knowledge_base.json` containing:
- **CIS Controls summaries** (e.g., SSH versions, Password policies).
- **NIST Configuration Guidelines**.
- **Vendor Specific recommendations** (e.g., Cisco IOS-XE AAA best practices).

Each chunk will include metadata:
- `source_id`
- `title`
- `authority` (e.g., CIS, NIST)
- `control` (e.g., NET-SSH-001)

## 4. Document Pipeline
1. `seed_rag.py` will read `knowledge_base.json`.
2. It will use `google-genai`'s text-embedding models to generate embeddings for each text chunk.
3. It will store the text, metadata, and embedding vector in SQLite `rag_documents`.

## 5. Retrieval Process
When a finding occurs:
1. `ai.py` will call `RAGRetriever.search(query)` where the query is constructed from the `control_title`, `actual` state, and `device_os`.
2. `RAGRetriever` embeds the query.
3. Python calculates cosine similarity against all stored embeddings and returns the top 2 matches.
4. The retrieved text and citations are injected into the prompt.

## 6. Prompt Engineering
The `EXPLANATION_PROMPT` in `prompts.py` will be updated to include a `[Retrieved Security Knowledge]` section and explicitly instruct the LLM to cite its sources and NOT override the deterministic engine.

## 7. Safety & Fallback
If retrieval fails (e.g., DB locked, API timeout), the system defaults to passing an empty string for the knowledge block. The deterministic compliance engine's verdict (`PASS/FAIL/UNKNOWN`) is NEVER modified by this subsystem.
