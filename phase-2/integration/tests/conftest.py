import sys
from pathlib import Path

_root = str(Path(__file__).parent.parent.parent.parent)
if _root not in sys.path:
    sys.path.insert(0, _root)

import asyncio
import uuid

import bcrypt
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.database import get_session
from src.main import app
from src.models.auth_models import User
from src.models.base import Base
from src.models.src_models import (
    CaseMaster,
)

TEST_ENGINE = None
TEST_FACTORY = None

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="session")
async def in_memory_db():
    global TEST_ENGINE, TEST_FACTORY
    TEST_ENGINE = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with TEST_ENGINE.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    TEST_FACTORY = async_sessionmaker(TEST_ENGINE, class_=AsyncSession, expire_on_commit=False)
    yield TEST_FACTORY
    await TEST_ENGINE.dispose()

@pytest_asyncio.fixture
async def db_session(in_memory_db):
    async with in_memory_db() as session:
        yield session

@pytest_asyncio.fixture
async def async_client(in_memory_db):
    async def override_get_session():
        async with in_memory_db() as session:
            yield session
    app.dependency_overrides[get_session] = override_get_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()

@pytest_asyncio.fixture
async def admin_token(async_client):
    from src.services.auth_service import AuthService
    async with TEST_FACTORY() as session:
        hashed = bcrypt.hashpw(b"admin123", bcrypt.gensalt()).decode()
        user = User(Email="admin@berunda.gov", HashedPassword=hashed, Role="admin")
        session.add(user)
        await session.commit()
        await session.refresh(user)
        svc = AuthService(session)
        _, access, _ = await svc.authenticate("admin@berunda.gov", "admin123")
        return access

@pytest_asyncio.fixture
async def auth_headers_admin(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}

@pytest_asyncio.fixture
async def sample_case(db_session):
    case = CaseMaster(CrimeNo=f"CR-2026-{uuid.uuid4().hex[:8].upper()}")
    db_session.add(case)
    await db_session.commit()
    await db_session.refresh(case)
    return case
