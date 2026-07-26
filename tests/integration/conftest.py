"""Integration test fixtures — manage Docker Compose lifecycle for a real PostgreSQL DB."""

from __future__ import annotations

import os
import subprocess
import time
from collections.abc import AsyncGenerator
from pathlib import Path
from typing import Any

import pytest

pytestmark = pytest.mark.integration


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _run_docker_compose(
    action: str,
    project_name: str,
    compose_file: Path,
    *,
    extra_args: str = "",
    timeout: int = 120,
) -> None:
    """Run ``docker compose <action> [extra_args]`` and raise on failure."""
    cmd = [
        "docker",
        "compose",
        "--project-name",
        project_name,
        "-f",
        str(compose_file),
        action,
    ]
    if extra_args:
        cmd.extend(extra_args.split())
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        pytest.fail(f"docker compose {action} timed out after {timeout}s:\n{exc}")
    except subprocess.CalledProcessError as exc:
        pytest.fail(
            f"docker compose {action} failed (exit {exc.returncode}):\n"
            f"stdout: {exc.stdout}\n"
            f"stderr: {exc.stderr}"
        )


@pytest.fixture(scope="session")
def docker_compose_files() -> list[str]:
    return [str(Path(__file__).parent.parent.parent / "docker-compose.integration.yml")]


@pytest.fixture(scope="session")
def docker_project_name() -> str:
    return "berunda-integration"


@pytest.fixture(scope="session")
def database_url() -> str:
    return os.environ.get(
        "TEST_DATABASE_URL",
        "postgresql+asyncpg://berunda:berunda_test@localhost:5432/berunda_test",
    )


@pytest.fixture(scope="session")
def cache_url() -> str:
    return os.environ.get("TEST_CACHE_URL", "redis://localhost:6379/0")


# ---------------------------------------------------------------------------
# Docker Compose lifecycle (session-scoped)
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def docker_services(
    docker_compose_files: list[str],
    docker_project_name: str,
    tmp_path_factory: pytest.TempPathFactory,
) -> None:
    """Start integration services once per session; tear down at session end."""
    import shutil
    if not shutil.which("docker") or os.environ.get("SKIP_DOCKER_TESTS", "1") == "1":
        pytest.skip("Docker not installed or SKIP_DOCKER_TESTS=1 set")
    compose_file = Path(docker_compose_files[0])
    if not compose_file.exists():
        pytest.fail(f"Docker Compose file not found: {compose_file}")

    # Write a minimal .env so compose can resolve variables if needed
    env_dir = tmp_path_factory.mktemp("docker")
    env_file = env_dir / ".env"
    env_file.write_text(f"COMPOSE_PROJECT_NAME={docker_project_name}\n")

    _run_docker_compose("up", docker_project_name, compose_file, extra_args="-d")

    # Wait for the health check to pass
    _wait_for_postgres(docker_project_name, compose_file, timeout=90)

    yield

    _run_docker_compose("down", docker_project_name, compose_file, extra_args="--volumes")


def _wait_for_postgres(
    project_name: str,
    compose_file: Path,
    timeout: int = 90,
) -> None:
    """Poll pg_isready until the DB accepts connections."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            subprocess.run(
                [
                    "docker",
                    "compose",
                    "--project-name",
                    project_name,
                    "-f",
                    str(compose_file),
                    "exec",
                    "-T",
                    "integration-db",
                    "pg_isready",
                    "-U",
                    "berunda",
                ],
                check=True,
                capture_output=True,
                text=True,
                timeout=15,
            )
            return
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            time.sleep(2)
    pytest.fail(f"Postgres not ready after {timeout}s")


# ---------------------------------------------------------------------------
# Engine & session fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def engine(database_url: str) -> Any:
    """Create a shared SQLAlchemy async engine for the test session."""
    from sqlalchemy.ext.asyncio import create_async_engine

    engine = create_async_engine(
        database_url,
        pool_pre_ping=True,
        echo=False,
    )
    return engine


@pytest.fixture(scope="session")
async def tables(engine: Any) -> AsyncGenerator[None, None]:
    """Create all tables once per session; drop on teardown."""
    from src.models.base import Base

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def db_session(
    engine: Any,
    tables: None,
) -> AsyncGenerator[Any, None]:
    """Yield a fresh session wrapped in a transaction that rolls back after the test.

    Tables are created once per session (see ``tables`` fixture).  Each test
    gets a clean session whose changes are rolled back automatically.
    """
    from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

    factory = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    async with factory() as session:
        try:
            yield session
        finally:
            await session.rollback()
            await session.close()


# ---------------------------------------------------------------------------
# Integration HTTP client wired to the live DB
# ---------------------------------------------------------------------------


@pytest.fixture(scope="function")
async def integration_client(
    db_session: Any,
) -> AsyncGenerator[Any, None]:
    """Yield an ``httpx.AsyncClient`` wired to the real database session.

    Depends on ``db_session`` so each test gets a clean transaction.
    """
    try:
        from httpx import ASGITransport, AsyncClient

        from src.database import get_session
        from src.main import app

        async def _override_session():
            yield db_session

        app.dependency_overrides[get_session] = _override_session

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            yield client
    except ImportError as exc:
        pytest.skip(f"Required module not available: {exc}")
    finally:
        app.dependency_overrides.clear()


# ---------------------------------------------------------------------------
# Seed-data helpers
# ---------------------------------------------------------------------------


@pytest.fixture(scope="function")
async def sample_fir_in_db(db_session: Any) -> dict[str, Any]:
    """Insert a sample CaseMaster record and return its identity."""
    from src.models.src_models import CaseMaster

    fir = CaseMaster(
        CrimeNo="FIR2024INT001",
        CaseNo="CASE001",
    )
    db_session.add(fir)
    await db_session.flush()
    await db_session.refresh(fir)
    return {"id": fir.CaseMasterID, "fir_number": fir.CrimeNo}


@pytest.fixture(scope="function")
async def populated_db(db_session: Any) -> dict[str, Any]:
    """Insert seed lookup rows needed by integration tests."""
    from src.models.src_models import CaseStatusMaster, CrimeHead, GravityOffence, State

    state = State(StateName="Karnataka", NationalityID=1)
    db_session.add(state)
    await db_session.flush()

    db_session.add_all(
        [
            CaseStatusMaster(CaseStatusName="Under Investigation", Active=True),
            CaseStatusMaster(CaseStatusName="Charge Sheet Filed", Active=True),
            CrimeHead(CrimeGroupName="Property Crime", Active=True),
            CrimeHead(CrimeGroupName="Violent Crime", Active=True),
            GravityOffence(LookupValue="Low", Active=True),
            GravityOffence(LookupValue="Medium", Active=True),
            GravityOffence(LookupValue="High", Active=True),
        ]
    )
    await db_session.flush()
    return {"status": "populated"}
