from __future__ import annotations

from datetime import datetime

from src.schemas.base import APIBase


class AuditEntryResponse(APIBase):
    AuditLogID: int
    UserID: int | None = None
    Action: str | None = None
    EntityType: str | None = None
    EntityID: int | None = None
    Timestamp: datetime | None = None
    IPAddress: str | None = None


class AuditQuery(APIBase):
    user_id: int | None = None
    action: str | None = None
    entity_type: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    page: int = 1
    page_size: int = 50
