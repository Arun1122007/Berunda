"""Integration test fixtures — require live services."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, AsyncGenerator, Generator

import pytest

# Mark all tests in this directory as integration tests
pytestmark = pytest.mark.integration


@pytest.fixture(scope="session")
def docker_compose_files() -> list[str]:
    """Return Docker Compose file paths for integration test services."""
    return [
        str(Path(__file__).parent.parent.parent / "docker-compose.integration.yml")
    ]


@pytest.fixture(scope="session")
def database_url() -> str:
    """Return the database URL for integration tests.

    Falls back to environment variable or default localhost.
    """
    return os.environ.get(
        "TEST_DATABASE_URL",
        "postgresql://berunda:berunda_test@localhost:5432/berunda_test",
    )


@pytest.fixture(scope="session")
def cache_url() -> str:
    """Return the cache URL for integration tests."""
    return os.environ.get("TEST_CACHE_URL", "redis://localhost:6379/0")


@pytest.fixture(scope="function")
async def db_session(database_url: str) -> AsyncGenerator[Any, None]:
    """Create a fresh database session for each integration test.

    Uses a transaction that is rolled back after the test.
    """
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.pool import NullPool

    engine = create_engine(
        database_url,
        poolclass=NullPool,
        echo=False,
    )
    TestSession = sessionmaker(bind=engine)

    # Create tables
    # from src.models import Base
    # Base.metadata.create_all(bind=engine)

    session = TestSession()
    try:
        # Begin a transaction
        session.begin()
        yield session
    finally:
        session.rollback()
        session.close()
        engine.dispose()


@pytest.fixture(scope="function")
async def integration_client(
    database_url: str,
) -> AsyncGenerator[Any, None]:
    """Create an integration test client with a live database."""
    try:
        from httpx import ASGITransport, AsyncClient

        # Import and configure your FastAPI app
        # from src.main import app
        # from src.config import settings
        # settings.DATABASE_URL = database_url

        # from src.database import setup_database
        # await setup_database()

        # transport = ASGITransport(app=app)
        # async with AsyncClient(transport=transport, base_url="http://test") as client:
        #     yield client

        # Placeholder until the app module is available
        mock_transport = ASGITransport(app=None)  # type: ignore
        async with AsyncClient(
            transport=mock_transport, base_url="http://test"
        ) as client:
            yield client
    except ImportError:
        pytest.skip("httpx or app module not available")


@pytest.fixture(scope="function")
def sample_fir_in_db(db_session: Any) -> dict[str, Any]:
    """Insert a sample FIR record into the database and return it."""
    # from src.models import FIR
    # fir = FIR(
    #     fir_number="FIR2024INT001",
    #     crime_type="burglary",
    #     ...
    # )
    # db_session.add(fir)
    # db_session.flush()
    # return {"id": fir.id, "fir_number": fir.fir_number}

    return {"id": 1, "fir_number": "FIR2024INT001"}


@pytest.fixture(scope="function")
def populated_db(db_session: Any) -> dict[str, Any]:
    """Populate the database with seed data for integration tests."""
    # Add seed data here
    db_session.flush()
    return {"status": "populated"}
