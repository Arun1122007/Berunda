from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, Query

from src.dependencies import get_audit_repo
from src.middleware.auth import require_role
from src.repositories.core import AuditRepository
from src.schemas.audit import AuditEntryResponse
from src.services.audit_service import AuditService

router = APIRouter(prefix="/api/v1/audit", tags=["Audit"])


@router.get("", response_model=list[AuditEntryResponse])
async def get_audit_logs(
    user_id: int | None = Query(None),
    action: str | None = Query(None),
    entity_type: str | None = Query(None),
    start_date: datetime | None = Query(None),
    end_date: datetime | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    repo: AuditRepository = Depends(get_audit_repo),
    user: dict = Depends(require_role(["admin", "analyst"])),
):
    service = AuditService(repo)
    items, _total = await service.get_entries(
        user_id=user_id,
        action=action,
        entity_type=entity_type,
        start_date=start_date,
        end_date=end_date,
        page=page,
        page_size=page_size,
    )
    return [AuditEntryResponse.model_validate(a) for a in items]
