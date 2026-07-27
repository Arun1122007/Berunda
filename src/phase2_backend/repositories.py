"""Concrete repository adapters — SQLAlchemy implementations of domain repository interfaces.

Layering: persistence interface → infrastructure adapter (SQLAlchemy)
"""

from __future__ import annotations

from typing import Any, Generic, TypeVar

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.auth_models import Permission, Session, User
from src.models.src_models import (
    Act,
    CaseCategory,
    CaseMaster,
    CaseStatusMaster,
    CrimeHead,
    CrimeSubHead,
    District,
    Employee,
    GravityOffence,
    InvOccuranceTime,
    Unit,
)

T = TypeVar("T")


def _get_pk_column(model_class: type) -> Any:
    """Get the first primary key column of a model."""
    try:
        insp = model_class.__table__.primary_key  # type: ignore[attr-defined]
        return next(iter(insp.columns))
    except (AttributeError, IndexError, KeyError):
        return None


class Repository(Generic[T]):
    """Base repository with common CRUD operations."""

    def __init__(self, session: AsyncSession, model_class: type[T]) -> None:
        self._session = session
        self._model = model_class
        self._pk = _get_pk_column(model_class)

    async def get_by_id(self, id_val: Any) -> T | None:
        return await self._session.get(self._model, id_val)

    async def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        filters: dict[str, Any] | None = None,
        order_by: Any | None = None,
    ) -> tuple[list[T], int]:
        query = select(self._model)
        count_query = select(func.count(self._model.get_primary_key_column()))  # type: ignore[attr-defined]

        if filters:
            for key, value in filters.items():
                column = getattr(self._model, key, None)
                if column is not None and value is not None:
                    query = query.where(column == value)

        total_result = await self._session.execute(count_query)
        total = total_result.scalar_one()

        if order_by is not None:
            query = query.order_by(order_by)
        elif self._pk is not None:
            query = query.order_by(self._pk.desc())

        query = query.offset(skip).limit(limit)

        result = await self._session.execute(query)
        items = list(result.scalars().all())
        return items, total

    async def create(self, data: dict[str, Any]) -> T:
        instance = self._model(**data)
        self._session.add(instance)
        await self._session.flush()
        await self._session.refresh(instance)
        return instance

    async def update(self, id_val: Any, data: dict[str, Any]) -> T | None:
        instance = await self.get_by_id(id_val)
        if instance is None:
            return None
        for key, value in data.items():
            if value is not None:
                setattr(instance, key, value)
        await self._session.flush()
        await self._session.refresh(instance)
        return instance

    async def delete(self, id_val: Any) -> bool:
        instance = await self.get_by_id(id_val)
        if instance is None:
            return False
        await self._session.delete(instance)
        await self._session.flush()
        return True


class FIRRepository:
    """FIR-specific repository with domain query methods."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_fir_detail(self, case_master_id: int) -> CaseMaster | None:
        query = (
            select(CaseMaster)
            .where(CaseMaster.CaseMasterID == case_master_id)
            .options(
                selectinload(CaseMaster.occurrence),
                selectinload(CaseMaster.complainants),
                selectinload(CaseMaster.victims),
                selectinload(CaseMaster.accused),
                selectinload(CaseMaster.act_sections),
                selectinload(CaseMaster.arrests),
                selectinload(CaseMaster.chargesheets),
            )
        )
        result = await self._session.execute(query)
        return result.scalar_one_or_none()

    async def list_firs(
        self,
        page: int = 1,
        page_size: int = 20,
        district_id: int | None = None,
        police_station_id: int | None = None,
        status_id: int | None = None,
    ) -> tuple[list[CaseMaster], int]:
        query = select(CaseMaster)
        count_query = select(func.count(CaseMaster.CaseMasterID))

        if district_id is not None:
            unit_subq = select(Unit.UnitID).where(Unit.DistrictID == district_id)
            query = query.where(CaseMaster.PoliceStationID.in_(unit_subq))
        if police_station_id is not None:
            query = query.where(CaseMaster.PoliceStationID == police_station_id)
        if status_id is not None:
            query = query.where(CaseMaster.CaseStatusID == status_id)

        total_result = await self._session.execute(count_query)
        total = total_result.scalar_one()

        query = (
            query.order_by(CaseMaster.CaseMasterID.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        result = await self._session.execute(query)
        items = list(result.scalars().all())
        return items, total

    async def create_fir(
        self, data: dict[str, Any], occurrence_data: dict[str, Any] | None = None
    ) -> CaseMaster:
        case = CaseMaster(**data)
        self._session.add(case)
        await self._session.flush()

        if occurrence_data:
            occurrence = InvOccuranceTime(CaseMasterID=case.CaseMasterID, **occurrence_data)
            self._session.add(occurrence)

        await self._session.commit()
        await self._session.refresh(case)
        return case

    async def update_fir(self, case_master_id: int, data: dict[str, Any]) -> CaseMaster | None:
        case = await self.get_fir_detail(case_master_id)
        if case is None:
            return None
        for key, value in data.items():
            if value is not None:
                setattr(case, key, value)
        await self._session.commit()
        await self._session.refresh(case)
        return case

    async def delete_fir(self, case_master_id: int) -> bool:
        case = await self._session.get(CaseMaster, case_master_id)
        if case is None:
            return False
        await self._session.delete(case)
        await self._session.commit()
        return True

    async def find_by_crime_no(self, crime_no: str) -> CaseMaster | None:
        result = await self._session.execute(
            select(CaseMaster).where(CaseMaster.CrimeNo == crime_no)
        )
        return result.scalar_one_or_none()

    async def count_by_district(self, district_id: int) -> int:
        unit_subq = select(Unit.UnitID).where(Unit.DistrictID == district_id)
        result = await self._session.execute(
            select(func.count(CaseMaster.CaseMasterID)).where(
                CaseMaster.PoliceStationID.in_(unit_subq)
            )
        )
        return result.scalar_one()

    async def count_by_status(self, status_id: int) -> int:
        result = await self._session.execute(
            select(func.count(CaseMaster.CaseMasterID)).where(CaseMaster.CaseStatusID == status_id)
        )
        return result.scalar_one()


class AuthRepository:
    """Auth-specific repository for users, sessions, and permissions."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_user_by_email(self, email: str) -> User | None:
        result = await self._session.execute(select(User).where(User.Email == email))
        return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: int) -> User | None:
        return await self._session.get(User, user_id)

    async def create_user(
        self, email: str, hashed_password: str, role: str, district_id: int | None = None
    ) -> User:
        user = User(Email=email, HashedPassword=hashed_password, Role=role, DistrictID=district_id)
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        return user

    async def list_users(self, skip: int = 0, limit: int = 100) -> tuple[list[User], int]:
        result = await self._session.execute(
            select(User).offset(skip).limit(limit).order_by(User.UserID)
        )
        items = list(result.scalars().all())
        count_result = await self._session.execute(select(func.count(User.UserID)))
        total = count_result.scalar_one()
        return items, total

    async def create_session(self, user_id: int, token_hash: str, expires_at: Any) -> Session:
        session = Session(UserID=user_id, TokenHash=token_hash, ExpiresAt=expires_at)
        self._session.add(session)
        await self._session.commit()
        return session

    async def get_session_by_token(self, token_hash: str) -> Session | None:
        result = await self._session.execute(select(Session).where(Session.TokenHash == token_hash))
        return result.scalar_one_or_none()

    async def revoke_session(self, session_id: int) -> None:
        session = await self._session.get(Session, session_id)
        if session:
            from datetime import datetime, timezone

            session.RevokedAt = datetime.now(timezone.utc)  # type: ignore[assignment]
            await self._session.commit()

    async def revoke_all_user_sessions(self, user_id: int) -> None:
        from datetime import datetime, timezone

        result = await self._session.execute(
            select(Session).where(Session.UserID == user_id, Session.RevokedAt.is_(None))
        )
        sessions = result.scalars().all()
        now = datetime.now(timezone.utc)
        for s in sessions:
            s.RevokedAt = now  # type: ignore[assignment]
        await self._session.commit()

    async def get_permissions_for_role(self, role: str) -> list[Permission]:
        result = await self._session.execute(select(Permission).where(Permission.Role == role))
        return list(result.scalars().all())


class LookupRepository:
    """Repository for reference/lookup data."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_district(self, district_id: int) -> District | None:
        return await self._session.get(District, district_id)

    async def list_districts(self) -> list[District]:
        result = await self._session.execute(
            select(District).where(District.Active).order_by(District.DistrictName)
        )
        return list(result.scalars().all())

    async def get_unit(self, unit_id: int) -> Unit | None:
        return await self._session.get(Unit, unit_id)

    async def list_police_stations(self, district_id: int | None = None) -> list[Unit]:
        query = select(Unit).where(Unit.Active)
        if district_id is not None:
            query = query.where(Unit.DistrictID == district_id)
        query = query.order_by(Unit.UnitName)
        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def get_case_status(self, status_id: int) -> CaseStatusMaster | None:
        return await self._session.get(CaseStatusMaster, status_id)

    async def list_case_statuses(self) -> list[CaseStatusMaster]:
        result = await self._session.execute(
            select(CaseStatusMaster).where(CaseStatusMaster.Active)
        )
        return list(result.scalars().all())

    async def list_crime_heads(self) -> list[CrimeHead]:
        result = await self._session.execute(
            select(CrimeHead).where(CrimeHead.Active).order_by(CrimeHead.CrimeGroupName)
        )
        return list(result.scalars().all())

    async def list_crime_sub_heads(self, crime_head_id: int | None = None) -> list[CrimeSubHead]:
        query = select(CrimeSubHead).where(CrimeSubHead.Active)
        if crime_head_id is not None:
            query = query.where(CrimeSubHead.CrimeHeadID == crime_head_id)
        query = query.order_by(CrimeSubHead.CrimeHeadName)
        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def list_case_categories(self) -> list[CaseCategory]:
        result = await self._session.execute(select(CaseCategory).where(CaseCategory.Active))
        return list(result.scalars().all())

    async def list_gravity_offences(self) -> list[GravityOffence]:
        result = await self._session.execute(select(GravityOffence).where(GravityOffence.Active))
        return list(result.scalars().all())

    async def get_act(self, act_code: str) -> Act | None:
        return await self._session.get(Act, act_code)

    async def list_acts(self) -> list[Act]:
        result = await self._session.execute(select(Act).where(Act.Active))
        return list(result.scalars().all())

    async def get_employee(self, employee_id: int) -> Employee | None:
        return await self._session.get(Employee, employee_id)
