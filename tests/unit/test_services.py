from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from src.repositories.sqlite_adapter import (
    SQLiteAuditRepository,
    SQLiteEntityRepository,
    SQLiteFIRRepository,
)
from src.schemas.entity import EntitySearchQuery
from src.services.audit_service import AuditService
from src.services.entity_service import EntityService
from src.services.fir_service import FIRService
from src.services.risk_service import RiskService


class AsyncMockSession:
    def __init__(self):
        self.execute = AsyncMock()
        self.get = AsyncMock(return_value=None)
        self.flush = AsyncMock()
        self.commit = AsyncMock()
        self.refresh = AsyncMock()
        self.add = MagicMock()
        self.delete = AsyncMock()


@pytest.fixture
def mock_session():
    return AsyncMockSession()


def result_with_scalars(items=None, scalar_one_val=0):
    if items is None:
        items = []
    mock = MagicMock()
    mock.scalars.return_value.all.return_value = items
    mock.scalar_one.return_value = scalar_one_val
    mock.scalar_one_or_none.return_value = None
    return mock


class TestFIRService:
    @pytest.mark.asyncio
    async def test_list_firs_empty(self, mock_session):
        mock_session.execute.return_value = result_with_scalars(items=[])
        service = FIRService(SQLiteFIRRepository(mock_session))
        items, total = await service.list_firs()
        assert items == []
        assert total == 0

    @pytest.mark.asyncio
    async def test_get_fir_not_found(self, mock_session):
        mock_session.execute.return_value = result_with_scalars()
        service = FIRService(SQLiteFIRRepository(mock_session))
        result = await service.get_fir(999)
        assert result is None

    @pytest.mark.asyncio
    async def test_delete_fir_not_found(self, mock_session):
        mock_session.execute.return_value = result_with_scalars()
        service = FIRService(SQLiteFIRRepository(mock_session))
        result = await service.delete_fir(999)
        assert result is False


class TestEntityService:
    @pytest.mark.asyncio
    async def test_search_entities_empty(self, mock_session):
        mock_session.execute.return_value = result_with_scalars(items=[])
        service = EntityService(SQLiteEntityRepository(mock_session))
        q = EntitySearchQuery()
        items, total = await service.search_entities(q)
        assert items == []
        assert total == 0

    @pytest.mark.asyncio
    async def test_get_entity_not_found(self, mock_session):
        mock_session.execute.return_value = result_with_scalars()
        service = EntityService(SQLiteEntityRepository(mock_session))
        result = await service.get_entity(999)
        assert result is None


class TestAuditService:
    @pytest.mark.asyncio
    async def test_get_entries_empty(self, mock_session):
        mock_session.execute.return_value = result_with_scalars(items=[])
        service = AuditService(SQLiteAuditRepository(mock_session))
        items, total = await service.get_entries()
        assert items == []
        assert total == 0


class TestRiskService:
    @pytest.mark.asyncio
    async def test_get_scores_empty(self, mock_session):
        mock_session.execute.return_value = result_with_scalars(items=[])
        service = RiskService(mock_session)
        items, total = await service.get_scores()
        assert items == []
        assert total == 0
