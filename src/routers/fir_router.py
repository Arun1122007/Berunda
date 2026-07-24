from __future__ import annotations

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.middleware.auth import get_current_user, require_role
from src.schemas.fir import (
    AccusedResponse,
    ActSectionResponse,
    ComplainantResponse,
    FIRCreate,
    FIRDetailResponse,
    FIRListResponse,
    FIRResponse,
    FIRUpdate,
    VictimResponse,
)
from src.services.fir_service import FIRService

router = APIRouter(prefix="/api/v1/fir", tags=["FIR"])


@router.get("", response_model=FIRListResponse)
async def list_firs(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    district_id: int | None = Query(None),
    police_station_id: int | None = Query(None),
    status_id: int | None = Query(None),
    session: AsyncSession = Depends(get_session),
    user: dict = Depends(get_current_user),
):
    if user.get("role") != "admin":
        district_id = user.get("district_id")

    service = FIRService(session)
    items, total = await service.list_firs(
        page=page,
        page_size=page_size,
        district_id=district_id,
        police_station_id=police_station_id,
        status_id=status_id,
    )
    return FIRListResponse(
        items=[FIRResponse.model_validate(f) for f in items],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{case_master_id}", response_model=FIRDetailResponse)
async def get_fir(
    case_master_id: int,
    session: AsyncSession = Depends(get_session),
    user: dict = Depends(get_current_user),
):
    service = FIRService(session)
    case = await service.get_fir(case_master_id)
    if case is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="FIR not found")
    return FIRDetailResponse(
        **FIRResponse.model_validate(case).model_dump(),
        complainants=[ComplainantResponse.model_validate(c) for c in (case.complainants or [])],
        victims=[VictimResponse.model_validate(v) for v in (case.victims or [])],
        accused=[AccusedResponse.model_validate(a) for a in (case.accused or [])],
        act_sections=[ActSectionResponse.model_validate(s) for s in (case.act_sections or [])],
    )


@router.post("", response_model=FIRResponse, status_code=status.HTTP_201_CREATED)
async def create_fir(
    data: FIRCreate,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session),
    user: dict = Depends(require_role(["admin", "officer"])),
):
    service = FIRService(session)
    case = await service.create_fir(data)
    case_id = case.CaseMasterID
    background_tasks.add_task(_trigger_post_fir_tasks, case_id)
    return FIRResponse.model_validate(case)


def _trigger_post_fir_tasks(case_master_id: int) -> None:
    try:
        from src.tasks import compute_risk_score_task, run_anomaly_detection_task

        compute_risk_score_task(case_master_id)
        run_anomaly_detection_task(case_master_id)
    except Exception:
        import logging

        logging.getLogger(__name__).exception(
            "Failed to dispatch background tasks for FIR %s", case_master_id
        )


@router.put("/{case_master_id}", response_model=FIRResponse)
async def update_fir(
    case_master_id: int,
    data: FIRUpdate,
    session: AsyncSession = Depends(get_session),
    user: dict = Depends(require_role(["admin", "officer"])),
):
    service = FIRService(session)
    case = await service.update_fir(case_master_id, data)
    if case is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="FIR not found")
    return FIRResponse.model_validate(case)


@router.delete("/{case_master_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_fir(
    case_master_id: int,
    session: AsyncSession = Depends(get_session),
    user: dict = Depends(require_role(["admin"])),
):
    service = FIRService(session)
    deleted = await service.delete_fir(case_master_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="FIR not found")
