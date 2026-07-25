"""Unit tests for FIRService — uses mocked session."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from src.schemas.fir import FIRCreate
from src.services.fir_service import FIRService


class AsyncMockSession:
    def __init__(self):
        self.execute = AsyncMock()
        self.get = AsyncMock()
        self.flush = AsyncMock()
        self.commit = AsyncMock()
        self.refresh = AsyncMock()
        self.add = MagicMock()
        self.delete = AsyncMock()

    def _make_scalar_result(self, items=None, scalar_one_val=0):
        m = MagicMock()
        m.scalars.return_value.all.return_value = items or []
        m.scalar_one.return_value = scalar_one_val
        m.scalar_one_or_none.return_value = items[0] if items else None
        return m


@pytest.fixture
def mock_case():
    case = MagicMock()
    case.CaseMasterID = 1
    case.CrimeNo = "CR-2026-TEST-001"
    case.CaseNo = None
    case.PoliceStationID = None
    case.CrimeMajorHeadID = None
    return case


@pytest.mark.unit
class TestFIRService:
    @pytest.mark.asyncio
    async def test_list_firs_empty(self):
        session = AsyncMockSession()
        session.execute.return_value = session._make_scalar_result(items=[], scalar_one_val=0)

        service = FIRService(session)
        items, total = await service.list_firs()
        assert items == []
        assert total == 0

    @pytest.mark.asyncio
    async def test_get_fir_not_found(self):
        session = AsyncMockSession()
        session.execute.return_value = session._make_scalar_result(items=None)

        service = FIRService(session)
        case = await service.get_fir(99999)
        assert case is None

    @pytest.mark.asyncio
    async def test_delete_fir_not_found(self):
        session = AsyncMockSession()
        session.get.return_value = None

        service = FIRService(session)
        deleted = await service.delete_fir(99999)
        assert deleted is False
