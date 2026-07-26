from __future__ import annotations

from datetime import datetime
from typing import Any

from src.repositories.core import AuditRepository, FIRRepository
from src.services.base import BaseService


class AuditService(BaseService):
    def __init__(self, repo_or_session: FIRRepository | AuditRepository | Any):
        super().__init__()
        if isinstance(repo_or_session, (FIRRepository, AuditRepository)) or hasattr(repo_or_session, "create_audit_entry"):
            self.repo = repo_or_session
        else:
            from src.repositories.sqlite_adapter import SQLiteAuditRepository
            self.repo = SQLiteAuditRepository(repo_or_session)

    async def get_entries(
        self,
        user_id: int | None = None,
        action: str | None = None,
        entity_type: str | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        page: int = 1,
        page_size: int = 50,
    ):
        if isinstance(self.repo, AuditRepository):
            return await self.repo.get_entries(
                user_id=user_id,
                action=action,
                entity_type=entity_type,
                start_date=start_date,
                end_date=end_date,
                page=page,
                page_size=page_size,
            )
        return [], 0

    async def log(
        self,
        user_id: int | None,
        action: str,
        entity_type: str | None = None,
        entity_id: int | None = None,
        old_value: str | None = None,
        new_value: str | None = None,
        ip_address: str | None = None,
    ):
        entry = await self.repo.create_audit_entry(
            {
                "ActorUserID": user_id,
                "Action": action,
                "EntityType": entity_type,
                "EntityID": entity_id,
                "OldValue": old_value,
                "NewValue": new_value,
                "CreatedAt": datetime.utcnow(),
                "IPAddress": ip_address,
            }
        )
        return entry
