"""Root pytest configuration and shared fixtures for Berunda tests."""

from __future__ import annotations

import json
import os
import sys
import uuid
from collections.abc import AsyncGenerator, Generator
from pathlib import Path
from typing import Any

# Add project root to path so imports like 'from src.main import app' work
_root_path = str(Path(__file__).parent.parent)
if _root_path not in sys.path:
    sys.path.insert(0, _root_path)

import pytest  # noqa: E402

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def load_fixture(name: str) -> Any:
    """Load a JSON fixture file from the fixtures directory."""
    path = FIXTURES_DIR / name
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Pytest configuration hooks
# ---------------------------------------------------------------------------


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--runslow",
        action="store_true",
        default=False,
        help="Run slow tests",
    )
    parser.addoption(
        "--run-e2e",
        action="store_true",
        default=False,
        help="Run end-to-end tests",
    )


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "e2e: End-to-end tests")
    config.addinivalue_line("markers", "slow: Slow tests")
    config.addinivalue_line("markers", "performance: Performance tests")
    config.addinivalue_line("markers", "security: Security tests")


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    skip_slow = not config.getoption("--runslow")
    skip_e2e = not config.getoption("--run-e2e")
    for item in items:
        if skip_slow and "slow" in item.keywords:
            item.add_marker(pytest.mark.skip(reason="Use --runslow to run slow tests"))
        if skip_e2e and "e2e" in item.keywords:
            item.add_marker(pytest.mark.skip(reason="Use --run-e2e to run e2e tests"))


# ---------------------------------------------------------------------------
# Fixtures: Sample data
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def sample_fir_data() -> list[dict[str, Any]]:
    """Load sample FIR records."""
    return load_fixture("sample-fir.json")


@pytest.fixture(scope="session")
def sample_entities_data() -> list[dict[str, Any]]:
    """Load sample entity data."""
    return load_fixture("sample-entities.json")


@pytest.fixture(scope="session")
def crime_type_codes() -> list[dict[str, str]]:
    """Load crime type codes."""
    import csv

    path = FIXTURES_DIR / "crime-types.csv"
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


# ---------------------------------------------------------------------------
# Fixtures: Database
# ---------------------------------------------------------------------------


@pytest.fixture
def test_db_path(tmp_path: Path) -> Path:
    """Return a temporary path for an in-memory SQLite database."""
    return tmp_path / "test.db"


@pytest.fixture
async def in_memory_db() -> AsyncGenerator[Any, None]:
    """Create an in-memory SQLite database for testing.

    Yields a database engine/connection that is torn down after the test.
    """
    try:
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker

        engine = create_engine("sqlite:///:memory:", echo=False)
        session_local = sessionmaker(bind=engine)

        # Create all tables (import your models here)
        # from src.models import Base
        # Base.metadata.create_all(bind=engine)

        yield session_local()

        engine.dispose()
    except ImportError:
        pytest.skip("SQLAlchemy not installed")


# ---------------------------------------------------------------------------
# Fixtures: Test client (FastAPI / httpx)
# ---------------------------------------------------------------------------


@pytest.fixture
def app() -> Any:
    """Return the FastAPI application instance.

    Override this fixture in your conftest or test module.
    """
    try:
        from src.main import app as _app

        return _app
    except ImportError:
        pytest.skip("FastAPI app module not found")


@pytest.fixture
async def async_client(app: Any) -> AsyncGenerator[Any, None]:
    """Provide an async HTTP client for testing API endpoints."""
    try:
        from httpx import ASGITransport, AsyncClient

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            yield client
    except ImportError:
        pytest.skip("httpx not installed")


@pytest.fixture
def client(app: Any) -> Generator[Any, None, None]:
    """Provide a synchronous test client."""
    try:
        from fastapi.testclient import TestClient

        with TestClient(app) as c:
            yield c
    except ImportError:
        pytest.skip("FastAPI TestClient not available")


# ---------------------------------------------------------------------------
# Fixtures: Authentication
# ---------------------------------------------------------------------------


@pytest.fixture
def auth_headers_admin() -> dict[str, str]:
    """Return auth headers for an admin user."""
    token = _generate_test_token("admin", ["admin", "analyst", "viewer"])
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def auth_headers_analyst() -> dict[str, str]:
    """Return auth headers for an analyst user."""
    token = _generate_test_token("analyst", ["analyst", "viewer"])
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def auth_headers_viewer() -> dict[str, str]:
    """Return auth headers for a viewer-only user."""
    token = _generate_test_token("viewer", ["viewer"])
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def auth_headers_no_role() -> dict[str, str]:
    """Return auth headers for an unauthenticated request."""
    return {}


def _generate_test_token(sub: str, roles: list[str]) -> str:
    """Generate a test JWT token (synchronous, no external service)."""
    import time

    import jwt

    payload = {
        "sub": sub,
        "roles": roles,
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600,
        "iss": "berunda-test",
        "jti": str(uuid.uuid4()),
    }
    secret = os.environ.get("AUTH_JWT_SECRET", "test-secret")
    return jwt.encode(payload, secret, algorithm="HS256")


# ---------------------------------------------------------------------------
# Fixtures: Mock Catalyst services
# ---------------------------------------------------------------------------


@pytest.fixture
def mock_catalyst_datastore(mocker: Any) -> Any:
    """Mock Catalyst DataStore for testing."""
    return mocker.patch("src.services.catalyst.CatalystDataStore")


@pytest.fixture
def mock_catalyst_stratus(mocker: Any) -> Any:
    """Mock Catalyst Stratus (cache) for testing."""
    cache_store: dict[str, Any] = {}

    def mock_get(key: str) -> Any:
        return cache_store.get(key)

    def mock_set(key: str, value: Any, ttl: int = 300) -> None:
        cache_store[key] = value

    mock = mocker.patch("src.services.catalyst.CatalystStratus")
    mock.get.side_effect = mock_get
    mock.set.side_effect = mock_set
    return mock


@pytest.fixture
def mock_catalyst_auth(mocker: Any) -> Any:
    """Mock Catalyst Authentication for testing."""
    return mocker.patch("src.services.catalyst.CatalystAuth")


# ---------------------------------------------------------------------------
# Fixtures: Entity resolution
# ---------------------------------------------------------------------------


@pytest.fixture
def sample_entity_match() -> dict[str, Any]:
    """Return a pair of entities that should be resolved as a match."""
    return {
        "entity_a": {
            "name": "Rajesh Kumar",
            "age": 35,
            "gender": "Male",
            "city": "Bengaluru",
        },
        "entity_b": {
            "name": "Rajesh K.",
            "age": 36,
            "gender": "Male",
            "city": "Bangalore",
        },
        "expected_similarity": 0.92,
        "expected_match": True,
    }


@pytest.fixture
def sample_entity_non_match() -> dict[str, Any]:
    """Return a pair of entities that should NOT be resolved as a match."""
    return {
        "entity_a": {
            "name": "Priya Sharma",
            "age": 28,
            "gender": "Female",
            "city": "Delhi",
        },
        "entity_b": {
            "name": "Amit Singh",
            "age": 42,
            "gender": "Male",
            "city": "Mumbai",
        },
        "expected_similarity": 0.15,
        "expected_match": False,
    }
