import os
import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool
from httpx import AsyncClient, ASGITransport

from main import app
from database import Base, get_async_db


# getting the url prom docker.env
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "postgresql+asyncpg://user:pass@db:5432/test_db")


# setup of test engine that knos how to talk to postresql asyn
@pytest.fixture(scope="session")
async def test_engine():
    """Create engine inside a fixture to tie it to the test loop."""
    engine = create_async_engine(
        TEST_DATABASE_URL, 
        poolclass=NullPool, 
        future=True
    )
    yield engine


    await engine.dispose()


# creates db sessions
@pytest.fixture(scope="session")
def TestingSessionLocal(test_engine):
    """Create the factory using the test_engine fixture."""
    return async_sessionmaker(
        bind=test_engine, 
        class_=AsyncSession, 
        expire_on_commit=False
    )


@ pytest.fixture(scope='session', autouse=True)
async def setup_database(test_engine):
    # protects running test points to the production db
    if "test" not in TEST_DATABASE_URL:
        pytest.exit("CRITICAL: TEST_DATABASE_URL must point to a 'test_db'!")
    
    # start and creates all tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield # test run here
    
    # after tests
    async with test_engine.begin() as conn:
        # Ushield to ensure the drop finishes before the loop starts closing
        await asyncio.shield(conn.run_sync(Base.metadata.drop_all))

@ pytest.fixture
async def db_session(TestingSessionLocal):
    
    async with TestingSessionLocal() as session:
        yield session


@ pytest.fixture
async def client(db_session):
    """ Override the "get_async_db" ependency in FastApi routes. """

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_async_db] = override_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()