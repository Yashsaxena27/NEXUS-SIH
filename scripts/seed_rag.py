import asyncio
import json
from pathlib import Path
from backend.app.rag.store import RAGStore
from backend.app.db.models import RAGDocument
from backend.app.db.session import engine, AsyncSessionLocal

KB_PATH = Path(__file__).parent.parent / "backend" / "app" / "rag" / "knowledge_base.json"

async def seed_rag():
    print("Initializing RAG DB Seed...")
    store = RAGStore()
    
    with open(KB_PATH, "r") as f:
        knowledge_base = json.load(f)
        
    async with engine.begin() as conn:
        from backend.app.db.models import Base
        await conn.run_sync(Base.metadata.create_all)
        
    async with AsyncSessionLocal() as db:
        for item in knowledge_base:
            # Check if it already exists
            from sqlalchemy.future import select
            existing = await db.execute(select(RAGDocument).where(RAGDocument.source_id == item["source_id"]))
            if existing.scalars().first():
                print(f"Skipping {item['source_id']} - already exists.")
                continue
                
            print(f"Generating embedding for {item['source_id']}...")
            embedding = await store.get_embedding(item["text"])
            
            doc = RAGDocument(
                source_id=item["source_id"],
                title=item["title"],
                authority=item["authority"],
                control=item.get("control"),
                text=item["text"],
                embedding_json=embedding
            )
            db.add(doc)
            
        await db.commit()
    print("Seed complete.")

if __name__ == "__main__":
    asyncio.run(seed_rag())
