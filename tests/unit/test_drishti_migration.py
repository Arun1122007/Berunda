"""Unit tests for newly migrated Drishti intelligence services."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from src.schemas.ingestion import IngestionPreviewRequest
from src.services.ai_assistant_service import AIAssistantService
from src.services.ingestion_service import IngestionService
from src.services.offender_service import OffenderService
from src.services.socioeconomic_service import SocioeconomicService


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
        m.scalar_one_or_none.return_value = items[0] if (items and isinstance(items, list)) else scalar_one_val
        return m


@pytest.mark.unit
class TestDrishtiMigrationServices:
    @pytest.mark.asyncio
    async def test_offender_service_empty_db_fallback_seed(self):
        session = AsyncMockSession()
        session.execute.return_value = session._make_scalar_result(items=[])

        service = OffenderService(session)
        offenders, total = await service.get_offenders(min_cases=1)
        assert total > 0
        assert any("Blinking Ramu" in o.alias for o in offenders if o.alias)

    @pytest.mark.asyncio
    async def test_offender_profile_lookup(self):
        session = AsyncMockSession()
        session.get.return_value = None

        service = OffenderService(session)
        profile = await service.get_offender_profile(1001)
        assert profile is not None
        assert profile.id == 1001
        assert "FP-IND-KA" in (profile.fingerprint_id or "")

    @pytest.mark.asyncio
    async def test_socioeconomic_service(self):
        session = AsyncMockSession()
        service = SocioeconomicService(session)
        records = await service.get_indicators()
        assert len(records) == 10
        assert records[0].crime_rate_per_100k >= records[1].crime_rate_per_100k

    @pytest.mark.asyncio
    async def test_ingestion_service_preview(self):
        session = AsyncMockSession()
        service = IngestionService(session)
        req = IngestionPreviewRequest(
            file_name="test_crimes.csv",
            file_type="csv",
            rows=[
                {"crimeNo": "CR-01", "district": "Bangalore", "offense": "Theft", "date": "2026-07-01"},
                {"crimeNo": "", "district": "Mysore", "offense": ""},  # invalid
            ],
            dry_run=True,
        )
        res = await service.preview_file(req)
        assert res.total_rows == 2
        assert res.valid_rows == 1
        assert res.error_rows == 1
        assert res.ready_for_commit is False

    @pytest.mark.asyncio
    async def test_ai_assistant_service(self):
        session = AsyncMockSession()
        session.execute.return_value = session._make_scalar_result(scalar_one_val=100)

        service = AIAssistantService(session)
        stats = await service.get_database_stats()
        assert stats["total_cases"] == 100

        ans = await service.answer_query("How many cases are there?")
        assert "100 total registered FIR cases" in ans["answer"]
