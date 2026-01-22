import os
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=False, future=True)
AssyncSessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False # prevents "greenlet" errors
    )

class Base(DeclarativeBase):
    pass

async def get_async_db():
    async with AssyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()