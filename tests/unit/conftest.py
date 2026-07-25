"""Unit test specific fixtures and configurations."""

from __future__ import annotations

from collections.abc import Generator
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


@pytest.fixture(autouse=True)
def _mock_external_services() -> Generator[None, None, None]:
    """Automatically mock all external services for unit tests.

    Prevents accidental network calls or database access during unit tests.
    Skips patches for modules that are not yet implemented.
    """
    patch_targets = [
        "src.services.catalyst.CatalystDataStore",
        "src.services.catalyst.CatalystStratus",
        "src.services.catalyst.CatalystAuth",
        "src.services.catalyst.CatalystQuickML",
    ]
    active_patches = []
    for target in patch_targets:
        try:
            p = patch(target)
            p.start()
            active_patches.append(p)
        except (ModuleNotFoundError, AttributeError):
            pass

    # Mock the AI provider factory so no unit test hits a real LLM / API.
    # Both embed() and generate() are async in production providers, so
    # use AsyncMock to make them awaitable.
    try:
        p = patch("src.services.embedding_service.create_provider")
        mock_factory = p.start()
        mock_provider = MagicMock()
        mock_provider.embed = AsyncMock(return_value=[[0.1] * 384])
        mock_provider.generate = AsyncMock(
            return_value={
                "text": "Mocked provider response.",
                "tokens_used": 50,
                "model": "test-model",
            }
        )
        mock_factory.return_value = mock_provider
        active_patches.append(p)
    except (ModuleNotFoundError, AttributeError):
        pass

    yield
    for p in active_patches:
        p.stop()


@pytest.fixture
def mock_db_session() -> MagicMock:
    """Provide a mock database session."""
    session = MagicMock()
    session.commit.return_value = None
    session.flush.return_value = None
    return session


@pytest.fixture
def mock_redis_client() -> MagicMock:
    """Provide a mock Redis/Stratus client."""
    client = MagicMock()
    client.get.return_value = None
    client.set.return_value = True
    client.delete.return_value = True
    return client


@pytest.fixture
def mock_llm_client() -> MagicMock:
    """Provide a mock LLM client for AI tests."""
    client = MagicMock()
    client.generate.return_value = {
        "text": "Mocked LLM response for unit tests.",
        "tokens_used": 50,
        "model": "test-model",
    }
    client.embed.return_value = [0.1] * 384
    return client


@pytest.fixture
def mock_fir_repository() -> MagicMock:
    """Provide a mock FIR repository."""
    repo = MagicMock()
    repo.get_by_id.return_value = {
        "fir_id": "FIR2024001",
        "status": "active",
        "crime_type": "theft",
        "officer_id": "OFF001",
    }
    repo.list.return_value = {
        "items": [],
        "total": 0,
        "page": 1,
        "limit": 20,
    }
    return repo


@pytest.fixture
def mock_entity_repository() -> MagicMock:
    """Provide a mock entity repository."""
    repo = MagicMock()
    repo.get_by_id.return_value = {
        "entity_id": "ENT001",
        "name": "Test Entity",
        "type": "person",
    }
    return repo
