from __future__ import annotations

from typing import Any

from sqlalchemy import select

from src.repositories.core import FIRRepository, FileStorage
from src.schemas.fir import FIRCreate, FIRUpdate
from src.services.audit_service import AuditService
from src.services.base import BaseService


class FIRService(BaseService):
    def __init__(self, repo: FIRRepository, storage: FileStorage | None = None):
        super().__init__()
        self.repo = repo
        self.storage = storage

    async def list_firs(
        self,
        page: int = 1,
        page_size: int = 20,
        district_id: int | None = None,
        police_station_id: int | None = None,
        status_id: int | None = None,
    ) -> tuple[list, int]:
        cache_key = (
            f"fir:list:{page}:{page_size}:"
            f"{district_id}:{police_station_id}:{status_id}"
        )
        cached = await self._cache.get(cache_key)
        if cached is not None:
            ids, total = cached["ids"], cached["total"]
            if ids:
                items = []
                for cid in ids:
                    case = await self.repo.get_fir(cid)
                    if case:
                        items.append(case)
            else:
                items = []
            return items, total

        items, total = await self.repo.list_firs(
            page=page,
            page_size=page_size,
            district_id=district_id,
            police_station_id=police_station_id,
            status_id=status_id,
        )

        await self._cache.set(cache_key, {"ids": [c.CaseMasterID for c in items], "total": total})
        return items, total

    async def get_fir(self, case_master_id: int):
        cache_key = f"fir:detail:{case_master_id}"
        cached = await self._cache.get(cache_key)
        if cached is not None:
            return await self.repo.get_fir(case_master_id)
        case = await self.repo.get_fir(case_master_id)
        if case is not None:
            await self._cache.set(cache_key, {"id": case_master_id})
        return case

    async def create_fir(self, data: FIRCreate, user_id: int | None = None):
        case = await self.repo.create_fir(data)

        from src.models.src_models import InvOccuranceTime

        if any([data.BriefFacts, data.Latitude is not None, data.Longitude is not None]):
            occurrence = InvOccuranceTime(
                CaseMasterID=case.CaseMasterID,
                BriefFacts=data.BriefFacts,
                Latitude=data.Latitude,
                Longitude=data.Longitude,
            )
            await self.repo.create_occurrence(occurrence)

        await self.repo.commit()
        await self.repo.refresh(case)
        await self._cache.invalidate("fir:list:*")

        audit_srv = AuditService(self.repo)
        await audit_srv.log(
            user_id=user_id,
            action="CREATE_FIR",
            entity_type="CaseMaster",
            entity_id=case.CaseMasterID,
            new_value=str(data.model_dump(exclude_none=True)),
        )
        return case

    async def update_fir(self, case_master_id: int, data: FIRUpdate, user_id: int | None = None):
        case = await self.repo.get_fir(case_master_id)
        if case is None:
            return None
        old_val = str({k: getattr(case, k, None) for k in data.model_dump(exclude_none=True).keys()})
        case = await self.repo.update_fir(case_master_id, data)
        await self.repo.commit()
        await self.repo.refresh(case)
        await self._cache.invalidate("fir:list:*")
        await self._cache.invalidate(f"fir:detail:{case_master_id}")

        audit_srv = AuditService(self.repo)
        await audit_srv.log(
            user_id=user_id,
            action="UPDATE_FIR",
            entity_type="CaseMaster",
            entity_id=case_master_id,
            old_value=old_val,
            new_value=str(data.model_dump(exclude_none=True)),
        )
        return case

    async def delete_fir(self, case_master_id: int, user_id: int | None = None) -> bool:
        case = await self.repo.get_fir(case_master_id)
        if case is None:
            return False

        await self.repo.delete_occurrence(case_master_id)
        await self.repo.delete_fir(case_master_id)
        await self.repo.commit()
        await self._cache.invalidate("fir:list:*")
        await self._cache.invalidate(f"fir:detail:{case_master_id}")

        audit_srv = AuditService(self.repo)
        await audit_srv.log(
            user_id=user_id,
            action="DELETE_FIR",
            entity_type="CaseMaster",
            entity_id=case_master_id,
        )
        return True

    async def upload_evidence(
        self,
        case_master_id: int,
        filename: str,
        content: bytes,
        mime_type: str,
        description: str | None = None,
        user_id: int | None = None,
    ) -> dict[str, Any]:
        from src.models.src_models import EvidenceMaster

        case = await self.repo.get_fir(case_master_id)
        if case is None:
            raise ValueError("FIR not found")

        if not filename or ".." in filename or "/" in filename or "\\" in filename:
            raise ValueError("Invalid filename — path traversal detected")

        storage_path = filename
        if self.storage:
            storage_path = await self.storage.save_file(filename, content, mime_type)

        evidence = EvidenceMaster(
            CaseMasterID=case_master_id,
            EvidenceType=mime_type,
            Description=description or f"Upload: {filename}",
            StoragePath=storage_path,
        )
        self.session.add(evidence)
        await self.repo.commit()
        await self.repo.refresh(evidence)

        audit_srv = AuditService(self.repo)
        await audit_srv.log(
            user_id=user_id,
            action="EVIDENCE_UPLOADED",
            entity_type="EvidenceMaster",
            entity_id=evidence.EvidenceID,
            new_value=f"Evidence {evidence.EvidenceID} uploaded: {filename} ({mime_type})",
        )

        return {
            "evidence_id": evidence.EvidenceID,
            "case_master_id": case_master_id,
            "evidence_type": mime_type,
            "description": evidence.Description,
            "storage_path": storage_path,
            "created_at": (
                evidence.CreatedAt.isoformat() if hasattr(evidence.CreatedAt, "isoformat") else str(evidence.CreatedAt)
            ),
        }

    async def get_evidence(self, case_master_id: int) -> list[dict[str, Any]]:
        from src.models.src_models import EvidenceMaster

        stmt = select(EvidenceMaster).where(EvidenceMaster.CaseMasterID == case_master_id)
        result = await self.session.execute(stmt)
        items = result.scalars().all()
        return [
            {
                "evidence_id": e.EvidenceID,
                "case_master_id": e.CaseMasterID,
                "evidence_type": e.EvidenceType,
                "description": e.Description,
                "storage_path": e.StoragePath,
                "created_at": (
                    e.CreatedAt.isoformat() if hasattr(e.CreatedAt, "isoformat") else str(e.CreatedAt)
                ),
            }
            for e in items
        ]
