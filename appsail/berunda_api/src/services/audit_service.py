from __future__ import annotations

from datetime import datetime

from sqlalchemy import func, select

from src.models.gov_models import AuditLog
from src.services.base import BaseService


class AuditService(BaseService):
    async def get_entries(
        self,
        user_id: int | None = None,
        action: str | None = None,
        entity_type: str | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        page: int = 1,
        page_size: int = 50,
    ) -> tuple[list[AuditLog], int]:
        query = select(AuditLog)
        count_query = select(func.count(AuditLog.AuditLogID))

        if user_id is not None:
            query = query.where(AuditLog.UserID == user_id)
            count_query = count_query.where(AuditLog.UserID == user_id)
        if action is not None:
            query = query.where(AuditLog.Action == action)
            count_query = count_query.where(AuditLog.Action == action)
        if entity_type is not None:
            query = query.where(AuditLog.EntityType == entity_type)
            count_query = count_query.where(AuditLog.EntityType == entity_type)
        if start_date is not None:
            query = query.where(AuditLog.Timestamp >= start_date)
            count_query = count_query.where(AuditLog.Timestamp >= start_date)
        if end_date is not None:
            query = query.where(AuditLog.Timestamp <= end_date)
            count_query = count_query.where(AuditLog.Timestamp <= end_date)

        total_result = await self.session.execute(count_query)
        total = total_result.scalar_one()

        query = query.order_by(AuditLog.Timestamp.desc())
        query = query.offset((page - 1) * page_size).limit(page_size)

        result = await self.session.execute(query)
        items = list(result.scalars().all())
        return items, total

    async def log(
        self,
        user_id: int | None,
        action: str,
        entity_type: str | None = None,
        entity_id: int | None = None,
        old_value: str | None = None,
        new_value: str | None = None,
        ip_address: str | None = None,
    ) -> AuditLog:
        entry = AuditLog(
            UserID=user_id,
            Action=action,
            EntityType=entity_type,
            EntityID=entity_id,
            OldValue=old_value,
            NewValue=new_value,
            Timestamp=datetime.utcnow(),
            IPAddress=ip_address,
        )
        self.session.add(entry)
        await self.session.commit()
        await self.session.refresh(entry)
        return entry
