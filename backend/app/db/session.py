from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from backend.app.core.config import settings

# Since we are using PostgreSQL in MVP and SQLite is easier for immediate local dev,
# we should allow fallback to SQLite if DB URL is not set or we want to test locally.
# However, user requested PostgreSQL from the beginning, so we stick to it.
# We will use asyncpg.

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

async def get_db():
    """Dependency to provide a database session."""
    async with AsyncSessionLocal() as session:
        yield session
