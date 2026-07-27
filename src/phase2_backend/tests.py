"""Tests for Phase 2 Backend — domain logic, authorization, and repositories.

Run with: pytest src/phase2_backend/tests.py -v
"""

from __future__ import annotations

from collections.abc import AsyncGenerator
from datetime import datetime, timedelta, timezone

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.models.auth_models import Permission, User
from src.models.base import Base
from src.models.src_models import (
    CaseCategory,
    CaseStatusMaster,
    CrimeHead,
    District,
    State,
)
from src.phase2_backend.authorization import AuthContext, filter_district_scoped
from src.phase2_backend.domain import (
    BriefFactsTooLongError,
    CrimeNo,
    FIRDomainService,
    FutureIncidentDateError,
    InvalidCoordinatesError,
    InvalidCrimeNoError,
    InvalidDateRangeError,
    MissingRequiredFieldError,
)
from src.phase2_backend.repositories import AuthRepository, FIRRepository, LookupRepository

# ── Fixtures ──────────────────────────────────────────────────────────────


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async with session_factory() as session:
        yield session

    await engine.dispose()


@pytest_asyncio.fixture
async def seeded_session(db_session: AsyncSession) -> AsyncSession:
    state = State(StateID=1, StateName="Karnataka", Active=True)
    district = District(DistrictID=1, DistrictName="Bengaluru Urban", StateID=1, Active=True)
    status = CaseStatusMaster(CaseStatusID=1, CaseStatusName="Under Investigation", Active=True)
    cat = CaseCategory(CaseCategoryID=1, LookupValue="Cognizable", Active=True)
    crime_head = CrimeHead(CrimeHeadID=1, CrimeGroupName="Property Offences", Active=True)

    db_session.add_all([state, district, status, cat, crime_head])
    await db_session.commit()
    return db_session


# ── Domain Tests ──────────────────────────────────────────────────────────


class TestCrimeNoValueObject:
    def test_parse_valid(self):
        cn = CrimeNo.parse("CR-2026-0421")
        assert cn.prefix == "CR"
        assert cn.year == 2026
        assert cn.sequence == 421
        assert str(cn) == "CR-2026-0421"

    def test_parse_invalid_prefix(self):
        with pytest.raises(InvalidCrimeNoError):
            CrimeNo.parse("XX-2026-0421")

    def test_parse_invalid_year(self):
        with pytest.raises(InvalidCrimeNoError):
            CrimeNo.parse("CR-AB-0421")

    def test_parse_invalid_sequence(self):
        with pytest.raises(InvalidCrimeNoError):
            CrimeNo.parse("CR-2026-ABCD")

    def test_parse_empty(self):
        with pytest.raises(InvalidCrimeNoError):
            CrimeNo.parse("")

    def test_parse_wrong_format(self):
        with pytest.raises(InvalidCrimeNoError):
            CrimeNo.parse("2026-0421")

    def test_parse_year_out_of_range(self):
        with pytest.raises(InvalidCrimeNoError):
            CrimeNo.parse("CR-1999-0001")

    def test_str_representation(self):
        cn = CrimeNo(prefix="CR", year=2026, sequence=42)
        assert str(cn) == "CR-2026-0042"


class TestFIRDomainService:
    def test_validate_crime_no_valid(self):
        cn = FIRDomainService.validate_crime_no("CR-2026-0001")
        assert cn.year == 2026

    def test_validate_crime_no_invalid(self):
        with pytest.raises(InvalidCrimeNoError):
            FIRDomainService.validate_crime_no("BAD")

    def test_validate_incident_dates_valid(self):
        FIRDomainService.validate_incident_dates(
            datetime(2026, 1, 1, tzinfo=timezone.utc),
            datetime(2026, 1, 2, tzinfo=timezone.utc),
        )

    def test_validate_incident_dates_reversed(self):
        with pytest.raises(InvalidDateRangeError):
            FIRDomainService.validate_incident_dates(
                datetime(2026, 1, 5, tzinfo=timezone.utc),
                datetime(2026, 1, 1, tzinfo=timezone.utc),
            )

    def test_validate_incident_dates_none(self):
        FIRDomainService.validate_incident_dates(None, None)

    def test_validate_future_date_past_date(self):
        FIRDomainService.validate_future_date(datetime(2020, 1, 1, tzinfo=timezone.utc))

    def test_validate_future_date_future_date(self):
        with pytest.raises(FutureIncidentDateError):
            FIRDomainService.validate_future_date(datetime.now(timezone.utc) + timedelta(days=30))

    def test_validate_required_fields_present(self):
        FIRDomainService.validate_required_fields(
            {"CrimeNo": "CR-2026-0001", "PSID": 5}, ["CrimeNo"]
        )

    def test_validate_required_fields_missing(self):
        with pytest.raises(MissingRequiredFieldError):
            FIRDomainService.validate_required_fields({"CrimeNo": None}, ["CrimeNo"])

    def test_validate_required_fields_empty_string(self):
        with pytest.raises(MissingRequiredFieldError):
            FIRDomainService.validate_required_fields({"CrimeNo": ""}, ["CrimeNo"])

    def test_validate_brief_facts_within_limit(self):
        FIRDomainService.validate_brief_facts("Short facts")

    def test_validate_brief_facts_exceeds_limit(self):
        with pytest.raises(BriefFactsTooLongError):
            FIRDomainService.validate_brief_facts("x" * 10001)

    def test_validate_brief_facts_none(self):
        FIRDomainService.validate_brief_facts(None)

    def test_validate_coordinates_valid(self):
        FIRDomainService.validate_coordinates(12.9716, 77.5946)

    def test_validate_coordinates_latitude_out_of_range(self):
        with pytest.raises(InvalidCoordinatesError):
            FIRDomainService.validate_coordinates(100.0, 0.0)

    def test_validate_coordinates_longitude_out_of_range(self):
        with pytest.raises(InvalidCoordinatesError):
            FIRDomainService.validate_coordinates(0.0, 200.0)

    def test_validate_coordinates_none(self):
        FIRDomainService.validate_coordinates(None, None)

    def test_validate_fir_create_input_valid(self):
        FIRDomainService.validate_fir_create_input(
            {"CrimeNo": "CR-2026-0001", "BriefFacts": "Robbery"}
        )

    def test_validate_fir_create_input_invalid_crime_no(self):
        with pytest.raises(InvalidCrimeNoError):
            FIRDomainService.validate_fir_create_input({"CrimeNo": "BAD"})

    def test_validate_fir_create_input_missing_crime_no_raises_invalid_format(self):
        with pytest.raises(InvalidCrimeNoError):
            FIRDomainService.validate_fir_create_input({})


# ── Authorization Tests ───────────────────────────────────────────────────


class TestAuthContext:
    def test_admin_has_full_access(self):
        ctx = AuthContext(
            {"user_id": 1, "role": "admin", "district_id": None, "email": "admin@test.com"}
        )
        assert ctx.is_admin
        assert ctx.is_authenticated
        assert ctx.can_access_district(5)
        assert ctx.can_edit_fir(5)
        assert ctx.can_delete_fir()

    def test_analyst_has_read_access(self):
        ctx = AuthContext(
            {"user_id": 2, "role": "analyst", "district_id": None, "email": "analyst@test.com"}
        )
        assert ctx.is_analyst
        assert ctx.can_access_district(5)
        assert ctx.can_edit_fir(5)
        assert not ctx.can_delete_fir()

    def test_officer_scoped_to_district(self):
        ctx = AuthContext(
            {"user_id": 3, "role": "officer", "district_id": 3, "email": "officer@test.com"}
        )
        assert ctx.is_officer
        assert ctx.can_access_district(3)
        assert not ctx.can_access_district(5)
        assert ctx.can_edit_fir(3)
        assert not ctx.can_edit_fir(5)
        assert not ctx.can_delete_fir()

    def test_anonymous_not_authenticated(self):
        ctx = AuthContext({"user_id": None, "role": "anonymous", "district_id": None, "email": ""})
        assert not ctx.is_authenticated
        assert not ctx.is_admin
        assert not ctx.can_access_district(1)
        assert not ctx.can_delete_fir()

    def test_officer_no_district_cannot_access_anything(self):
        ctx = AuthContext(
            {"user_id": 4, "role": "officer", "district_id": None, "email": "officer2@test.com"}
        )
        assert not ctx.can_access_district(1)


class TestFilterDistrictScoped:
    def test_admin_returns_empty_filter(self):
        assert filter_district_scoped({"user_id": 1, "role": "admin", "district_id": None}) == {}

    def test_officer_returns_district_filter(self):
        assert filter_district_scoped({"user_id": 2, "role": "officer", "district_id": 5}) == {
            "DistrictID": 5
        }

    def test_officer_no_district_returns_empty(self):
        assert filter_district_scoped({"user_id": 3, "role": "officer", "district_id": None}) == {}

    def test_custom_field_name(self):
        result = filter_district_scoped(
            {"user_id": 2, "role": "officer", "district_id": 5}, "custom_id"
        )
        assert result == {"custom_id": 5}


# ── Repository Tests ──────────────────────────────────────────────────────


class TestFIRRepository:
    @pytest.mark.asyncio
    async def test_create_fir(self, db_session: AsyncSession):
        repo = FIRRepository(db_session)
        case = await repo.create_fir(data={"CrimeNo": "CR-2026-0001", "CaseStatusID": 1})
        assert case.CaseMasterID is not None
        assert case.CrimeNo == "CR-2026-0001"

    @pytest.mark.asyncio
    async def test_get_fir_detail_not_found(self, db_session: AsyncSession):
        repo = FIRRepository(db_session)
        result = await repo.get_fir_detail(999)
        assert result is None

    @pytest.mark.asyncio
    async def test_list_firs_empty(self, db_session: AsyncSession):
        repo = FIRRepository(db_session)
        items, total = await repo.list_firs()
        assert items == []
        assert total == 0

    @pytest.mark.asyncio
    async def test_list_firs_with_data(self, db_session: AsyncSession):
        repo = FIRRepository(db_session)
        await repo.create_fir({"CrimeNo": "CR-2026-0001", "CaseStatusID": 1})
        await repo.create_fir({"CrimeNo": "CR-2026-0002", "CaseStatusID": 1})

        items, total = await repo.list_firs()
        assert total == 2
        assert len(items) == 2

    @pytest.mark.asyncio
    async def test_find_by_crime_no(self, db_session: AsyncSession):
        repo = FIRRepository(db_session)
        await repo.create_fir({"CrimeNo": "CR-2026-0001", "CaseStatusID": 1})

        case = await repo.find_by_crime_no("CR-2026-0001")
        assert case is not None
        assert case.CrimeNo == "CR-2026-0001"

        not_found = await repo.find_by_crime_no("CR-2026-9999")
        assert not_found is None

    @pytest.mark.asyncio
    async def test_delete_fir(self, db_session: AsyncSession):
        repo = FIRRepository(db_session)
        case = await repo.create_fir({"CrimeNo": "CR-2026-0001"})

        assert await repo.delete_fir(case.CaseMasterID) is True  # type: ignore[arg-type]
        assert await repo.delete_fir(999) is False

    @pytest.mark.asyncio
    async def test_count_by_district(self, db_session: AsyncSession):
        repo = FIRRepository(db_session)
        assert await repo.count_by_district(1) == 0

    @pytest.mark.asyncio
    async def test_count_by_status(self, db_session: AsyncSession):
        repo = FIRRepository(db_session)
        assert await repo.count_by_status(1) == 0

    @pytest.mark.asyncio
    async def test_list_firs_pagination(self, db_session: AsyncSession):
        repo = FIRRepository(db_session)
        for i in range(5):
            await repo.create_fir({"CrimeNo": f"CR-2026-{i + 1:04d}", "CaseStatusID": 1})

        items, total = await repo.list_firs(page=1, page_size=3)
        assert total == 5
        assert len(items) == 3

        items2, _ = await repo.list_firs(page=2, page_size=3)
        assert len(items2) == 2


class TestAuthRepository:
    @pytest.mark.asyncio
    async def test_create_and_get_user(self, db_session: AsyncSession):
        repo = AuthRepository(db_session)
        user = await repo.create_user("test@test.com", "hashed_pwd", "officer")
        assert user.UserID is not None

        fetched = await repo.get_user_by_email("test@test.com")
        assert fetched is not None
        assert fetched.Email == "test@test.com"

        by_id = await repo.get_user_by_id(user.UserID)  # type: ignore[arg-type]
        assert by_id is not None
        assert by_id.Role == "officer"

    @pytest.mark.asyncio
    async def test_get_user_not_found(self, db_session: AsyncSession):
        repo = AuthRepository(db_session)
        assert await repo.get_user_by_email("nobody@test.com") is None
        assert await repo.get_user_by_id(999) is None

    @pytest.mark.asyncio
    async def test_list_users(self, db_session: AsyncSession):
        repo = AuthRepository(db_session)
        await repo.create_user("a@test.com", "hash1", "admin")
        await repo.create_user("b@test.com", "hash2", "officer")

        users, total = await repo.list_users()
        assert total == 2
        assert len(users) == 2

    @pytest.mark.asyncio
    async def test_create_and_get_permissions(self, db_session: AsyncSession):
        permission = Permission(Role="admin", Resource="fir", Action="write")
        db_session.add(permission)
        await db_session.commit()

        repo = AuthRepository(db_session)
        perms = await repo.get_permissions_for_role("admin")
        assert len(perms) == 1
        assert perms[0].Resource == "fir"

    @pytest.mark.asyncio
    async def test_get_permissions_empty_role(self, db_session: AsyncSession):
        repo = AuthRepository(db_session)
        perms = await repo.get_permissions_for_role("nonexistent")
        assert perms == []

    @pytest.mark.asyncio
    async def test_revoke_session(self, db_session: AsyncSession):
        user = User(Email="test@test.com", HashedPassword="hash", Role="officer")
        db_session.add(user)
        await db_session.commit()

        repo = AuthRepository(db_session)
        session = await repo.create_session(
            user_id=user.UserID,  # type: ignore[arg-type]
            token_hash="abc123",
            expires_at=datetime.now(timezone.utc) + timedelta(days=1),
        )

        await repo.revoke_session(session.SessionID)  # type: ignore[arg-type]
        updated = await repo.get_session_by_token("abc123")
        assert updated is not None
        assert updated.RevokedAt is not None


class TestLookupRepository:
    @pytest.mark.asyncio
    async def test_list_districts(self, seeded_session: AsyncSession):
        repo = LookupRepository(seeded_session)
        districts = await repo.list_districts()
        assert len(districts) >= 1
        assert any(d.DistrictName == "Bengaluru Urban" for d in districts)

    @pytest.mark.asyncio
    async def test_get_district(self, seeded_session: AsyncSession):
        repo = LookupRepository(seeded_session)
        d = await repo.get_district(1)
        assert d is not None
        assert d.DistrictName == "Bengaluru Urban"

    @pytest.mark.asyncio
    async def test_list_case_statuses(self, seeded_session: AsyncSession):
        repo = LookupRepository(seeded_session)
        statuses = await repo.list_case_statuses()
        assert len(statuses) >= 1

    @pytest.mark.asyncio
    async def test_list_crime_heads(self, seeded_session: AsyncSession):
        repo = LookupRepository(seeded_session)
        heads = await repo.list_crime_heads()
        assert len(heads) >= 1
