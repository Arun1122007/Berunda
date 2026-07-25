"""Unit tests for FIRService."""

from __future__ import annotations

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.models.base import Base
from src.schemas.fir import FIRCreate
from src.services.fir_service import FIRService


@pytest_asyncio.fixture
async def db_session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        yield session

    await engine.dispose()


@pytest.mark.unit
class TestFIRService:
    async def test_list_firs_empty(self, db_session: AsyncSession):
        service = FIRService(db_session)
        items, total = await service.list_firs()
        assert items == []
        assert total == 0

    async def test_create_fir_basic(self, db_session: AsyncSession):
        service = FIRService(db_session)
        data = FIRCreate(CrimeNo="CR-2026-TEST-001")
        case = await service.create_fir(data)
        assert case.CrimeNo == "CR-2026-TEST-001"
        assert case.CaseMasterID > 0

    async def test_create_fir_with_brief_facts(self, db_session: AsyncSession):
        service = FIRService(db_session)
        data = FIRCreate(
            CrimeNo="CR-2026-TEST-002",
            BriefFacts="Test incident description",
            Latitude=12.9716,
            Longitude=77.5946,
        )
        case = await service.create_fir(data)
        assert case.CrimeNo == "CR-2026-TEST-002"

    async def test_list_firs_after_create(self, db_session: AsyncSession):
        service = FIRService(db_session)
        await service.create_fir(FIRCreate(CrimeNo="CR-2026-TEST-003"))
        items, total = await service.list_firs()
        assert total == 1
        assert items[0].CrimeNo == "CR-2026-TEST-003"

    async def test_get_fir_returns_none_for_missing(self, db_session: AsyncSession):
        service = FIRService(db_session)
        case = await service.get_fir(99999)
        assert case is None

    async def test_get_fir_after_create(self, db_session: AsyncSession):
        service = FIRService(db_session)
        created = await service.create_fir(FIRCreate(CrimeNo="CR-2026-TEST-004"))
        fetched = await service.get_fir(created.CaseMasterID)
        assert fetched is not None
        assert fetched.CrimeNo == "CR-2026-TEST-004"

    async def test_create_fir_with_all_fields(self, db_session: AsyncSession):
        service = FIRService(db_session)
        data = FIRCreate(
            CrimeNo="CR-2026-TEST-005",
            CaseNo="99/2026",
            PoliceStationID=5,
            CaseCategoryID=1,
            GravityOffenceID=2,
            CrimeMajorHeadID=1,
            CrimeMinorHeadID=1,
            CaseStatusID=1,
        )
        case = await service.create_fir(data)
        assert case.CaseNo == "99/2026"
        assert case.PoliceStationID == 5
        assert case.CrimeMajorHeadID == 1

    async def test_pagination(self, db_session: AsyncSession):
        service = FIRService(db_session)
        for i in range(5):
            await service.create_fir(FIRCreate(CrimeNo=f"CR-2026-TEST-P{i:03d}"))
        page1, total = await service.list_firs(page=1, page_size=2)
        assert len(page1) <= 2
        assert total == 5
