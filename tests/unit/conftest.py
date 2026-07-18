"""Unit test specific fixtures and configurations."""

from __future__ import annotations

from typing import Any, Generator
from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture(autouse=True)
def _mock_external_services() -> Generator[None, None, None]:
    """Automatically mock all external services for unit tests.

    Prevents accidental network calls or database access during unit tests.
    """
    patches = [
        patch("src.services.catalyst.CatalystDataStore"),
        patch("src.services.catalyst.CatalystStratus"),
        patch("src.services.catalyst.CatalystAuth"),
        patch("src.services.catalyst.CatalystQuickML"),
    ]
    for p in patches:
        p.start()
    yield
    for p in patches:
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
