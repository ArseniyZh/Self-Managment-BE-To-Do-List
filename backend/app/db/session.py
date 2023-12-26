from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import DATABASE_URL, TEST, TEST_DATABASE_URL

db_url = TEST_DATABASE_URL if TEST else DATABASE_URL

Base: DeclarativeMeta = declarative_base()

async_engine: AsyncEngine = create_async_engine(
    db_url,
    echo=False
)

AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=True,
    autoflush=True,
)


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
