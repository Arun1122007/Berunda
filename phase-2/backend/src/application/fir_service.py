from __future__ import annotations

import logging
import uuid
from datetime import datetime
from typing import Optional, Sequence

from src.domain.errors import AuthorizationError, ConflictError, NotFoundError, ValidationError
from src.domain.models import FIR
from src.domain.rules import CrimeNumberRule, DistrictScopeRule, GravityOffenceRule, RoleHierarchyRule
from src.persistence.interfaces import FIRRepository, UserRepository

logger = logging.getLogger(__name__)


class FIRService:
    def __init__(self, fir_repo: FIRRepository, user_repo: UserRepository) -> None:
        self._fir_repo = fir_repo
        self._user_repo = user_repo

    async def list_firs(
        self,
        user_id: uuid.UUID,
        district_id: Optional[str] = None,
        police_station_id: Optional[str] = None,
        case_status_id: Optional[str] = None,
        crime_major_head_id: Optional[str] = None,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        offset: int = 0,
        limit: int = 20,
    ) -> tuple[Sequence[FIR], int]:
        user = await self._user_repo.get_by_id(user_id)
        if user is None:
            raise NotFoundError("User not found")

        effective_district = district_id
        if not RoleHierarchyRule.is_admin(user.role):
            if not DistrictScopeRule.can_access(effective_district or "", user.district_id, user.role):
                raise AuthorizationError("You do not have access to FIRs in this district")
            effective_district = user.district_id

        return await self._fir_repo.list(
            district_id=effective_district,
            police_station_id=police_station_id,
            case_status_id=case_status_id,
            crime_major_head_id=crime_major_head_id,
            from_date=from_date,
            to_date=to_date,
            offset=offset,
            limit=limit,
        )

    async def get_fir(self, fir_id: uuid.UUID, user_id: uuid.UUID) -> FIR:
        user = await self._user_repo.get_by_id(user_id)
        if user is None:
            raise NotFoundError("User not found")

        fir = await self._fir_repo.get_by_id(fir_id)
        if fir is None:
            raise NotFoundError("FIR not found")

        if not DistrictScopeRule.can_access(fir.district_id, user.district_id, user.role):
            raise AuthorizationError("You do not have access to this FIR")

        return fir

    async def create_fir(self, fir_data: FIR, user_id: uuid.UUID) -> FIR:
        user = await self._user_repo.get_by_id(user_id)
        if user is None:
            raise NotFoundError("User not found")

        error = CrimeNumberRule.validate(fir_data.crime_no)
        if error:
            raise ValidationError(error)

        existing = await self._fir_repo.get_by_crime_no(fir_data.crime_no)
        if existing is not None:
            raise ConflictError(f"FIR with crime number '{fir_data.crime_no}' already exists")

        error = GravityOffenceRule.validate(fir_data.gravity_offence_id)
        if error:
            raise ValidationError(error)

        if GravityOffenceRule.requires_supervisory_approval(fir_data.gravity_offence_id):
            if not RoleHierarchyRule.has_role(user.role, "analyst"):
                raise AuthorizationError("Supervisory approval required for serious offences")

        if not DistrictScopeRule.can_access(fir_data.district_id, user.district_id, user.role):
            raise AuthorizationError("You cannot create FIRs outside your district")

        new_fir = fir_data.model_copy(update={"created_by": str(user.id)})
        created = await self._fir_repo.create(new_fir)
        logger.info("FIR created: id=%s crime_no=%s district=%s", created.id, created.crime_no, created.district_id)
        return created

    async def update_fir(self, fir_id: uuid.UUID, fir_data: FIR, user_id: uuid.UUID) -> FIR:
        user = await self._user_repo.get_by_id(user_id)
        if user is None:
            raise NotFoundError("User not found")

        existing = await self._fir_repo.get_by_id(fir_id)
        if existing is None:
            raise NotFoundError("FIR not found")

        if not DistrictScopeRule.can_access(existing.district_id, user.district_id, user.role):
            raise AuthorizationError("You do not have access to this FIR")

        if not RoleHierarchyRule.has_role(user.role, "officer"):
            raise AuthorizationError("You do not have permission to update FIRs")

        if fir_data.crime_no != existing.crime_no:
            conflict = await self._fir_repo.get_by_crime_no(fir_data.crime_no)
            if conflict is not None:
                raise ConflictError(f"Crime number '{fir_data.crime_no}' is already in use")

        updated = fir_data.model_copy(update={"id": fir_id, "updated_at": datetime.utcnow()})
        result = await self._fir_repo.update(updated)
        logger.info("FIR updated: id=%s crime_no=%s", result.id, result.crime_no)
        return result

    async def delete_fir(self, fir_id: uuid.UUID, user_id: uuid.UUID) -> None:
        user = await self._user_repo.get_by_id(user_id)
        if user is None:
            raise NotFoundError("User not found")

        existing = await self._fir_repo.get_by_id(fir_id)
        if existing is None:
            raise NotFoundError("FIR not found")

        if not DistrictScopeRule.can_access(existing.district_id, user.district_id, user.role):
            raise AuthorizationError("You do not have access to this FIR")

        if not RoleHierarchyRule.is_admin(user.role):
            raise AuthorizationError("Only administrators can delete FIRs")

        await self._fir_repo.delete(fir_id)
        logger.info("FIR deleted: id=%s crime_no=%s", fir_id, existing.crime_no)
