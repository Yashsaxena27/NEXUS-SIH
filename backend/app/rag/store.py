import json
import math
from typing import List, Dict, Any, Optional
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.db.models import RAGDocument
from backend.app.core.config import settings

try:
    import google.generativeai as genai
except ImportError:
    genai = None

class RAGStore:
    """Lightweight SQLite-based Vector Store using Python for cosine similarity."""
    
    def __init__(self):
        self.embedding_model = "models/gemini-embedding-001"
        if not genai or not settings.GEMINI_API_KEY:
            self._use_mock = True
        else:
            self._use_mock = False
            genai.configure(api_key=settings.GEMINI_API_KEY)
        
    def _cosine_similarity(self, v1: List[float], v2: List[float]) -> float:
        if len(v1) != len(v2):
            return 0.0
        
        dot_product = sum(a * b for a, b in zip(v1, v2))
        norm_a = math.sqrt(sum(a * a for a in v1))
        norm_b = math.sqrt(sum(b * b for b in v2))
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
            
        return dot_product / (norm_a * norm_b)
        
    async def get_embedding(self, text: str) -> List[float]:
        """Generates an embedding vector for a given text."""
        if self._use_mock:
            import hashlib
            h = hashlib.sha256(text.encode('utf-8')).digest()
            # Generate a 32-dim deterministic vector from hash
            return [(b / 128.0) - 1.0 for b in h]
            
        result = genai.embed_content(
            model=self.embedding_model,
            content=text,
            task_type="retrieval_document"
        )
        return result['embedding']

    async def search(self, db: AsyncSession, query: str, top_k: int = 2) -> List[Dict[str, Any]]:
        """Search the database for the most semantically similar documents."""
        try:
            query_embedding = await self.get_embedding(query)
            
            # Fetch all documents
            result = await db.execute(select(RAGDocument))
            documents = result.scalars().all()
            
            if not documents:
                return []
                
            scored_docs = []
            for doc in documents:
                sim = self._cosine_similarity(query_embedding, doc.embedding_json)
                scored_docs.append((sim, doc))
                
            # Sort by descending similarity
            scored_docs.sort(key=lambda x: x[0], reverse=True)
            
            top_docs = []
            for sim, doc in scored_docs[:top_k]:
                # We can enforce a minimum threshold if we want, e.g. 0.4
                if sim > 0.4:
                    top_docs.append({
                        "source_id": doc.source_id,
                        "title": doc.title,
                        "authority": doc.authority,
                        "control": doc.control,
                        "text": doc.text,
                        "score": sim
                    })
            return top_docs
            
        except Exception as e:
            print(f"RAG Retrieval error: {e}")
            return []
