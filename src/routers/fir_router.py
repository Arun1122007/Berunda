from __future__ import annotations

from fastapi import APIRouter, BackgroundTasks, Depends, Form, HTTPException, Query, UploadFile, status

from src.dependencies import get_fir_repo, get_file_storage
from src.middleware.auth import get_current_user, require_role
from src.repositories.core import FIRRepository, FileStorage
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
    repo: FIRRepository = Depends(get_fir_repo),
    user: dict = Depends(get_current_user),
):
    if user.get("role") != "admin":
        district_id = user.get("district_id")

    service = FIRService(repo)
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
    repo: FIRRepository = Depends(get_fir_repo),
    user: dict = Depends(get_current_user),
):
    service = FIRService(repo)
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
    repo: FIRRepository = Depends(get_fir_repo),
    user: dict = Depends(require_role(["admin", "officer"])),
):
    service = FIRService(repo)
    user_id = user.get("id") or user.get("user_id") if isinstance(user, dict) else None
    case = await service.create_fir(data, user_id=user_id)
    case_id = case.CaseMasterID
    background_tasks.add_task(_trigger_post_fir_tasks, case_id)
    return FIRResponse.model_validate(case)


def _trigger_post_fir_tasks(case_master_id: int) -> None:
    try:
        from src.tasks import (
            compute_risk_score_task,
            request_ai_extraction_task,
            run_anomaly_detection_task,
        )

        compute_risk_score_task(case_master_id)
        run_anomaly_detection_task(case_master_id)
        request_ai_extraction_task(case_master_id)
    except Exception:
        import logging

        logging.getLogger(__name__).exception(
            "Failed to dispatch background tasks for FIR %s", case_master_id
        )


@router.put("/{case_master_id}", response_model=FIRResponse)
async def update_fir(
    case_master_id: int,
    data: FIRUpdate,
    repo: FIRRepository = Depends(get_fir_repo),
    user: dict = Depends(require_role(["admin", "officer"])),
):
    service = FIRService(repo)
    user_id = user.get("id") or user.get("user_id") if isinstance(user, dict) else None
    case = await service.update_fir(case_master_id, data, user_id=user_id)
    if case is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="FIR not found")
    return FIRResponse.model_validate(case)


@router.delete("/{case_master_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_fir(
    case_master_id: int,
    repo: FIRRepository = Depends(get_fir_repo),
    user: dict = Depends(require_role(["admin"])),
):
    service = FIRService(repo)
    user_id = user.get("id") or user.get("user_id") if isinstance(user, dict) else None
    deleted = await service.delete_fir(case_master_id, user_id=user_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="FIR not found")


@router.post("/{case_master_id}/evidence", status_code=status.HTTP_201_CREATED)
async def upload_evidence(
    case_master_id: int,
    file: UploadFile,
    description: str | None = Form(None),
    repo: FIRRepository = Depends(get_fir_repo),
    storage: FileStorage = Depends(get_file_storage),
    user: dict = Depends(require_role(["admin", "officer"])),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required")

    if ".." in file.filename or "/" in file.filename or "\\" in file.filename:
        raise HTTPException(status_code=400, detail="Invalid filename — path traversal detected")

    content = await file.read()
    if len(content) == 0:
        raise HTTPException(status_code=400, detail="Empty file — cannot upload zero-byte attachment")

    allowed_types = {
        "application/pdf",
        "image/jpeg",
        "image/png",
        "image/tiff",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "text/plain",
        "text/csv",
        "application/zip",
    }
    if file.content_type and file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail=f"Unsupported MIME type: {file.content_type}")

    if len(content) > 50 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File exceeds maximum size of 50 MB")

    service = FIRService(repo, storage=storage)
    user_id = user.get("id") or user.get("user_id") if isinstance(user, dict) else None
    try:
        result = await service.upload_evidence(
            case_master_id=case_master_id,
            filename=file.filename,
            content=content,
            mime_type=file.content_type or "application/octet-stream",
            description=description,
            user_id=user_id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return result


@router.get("/{case_master_id}/evidence")
async def list_evidence(
    case_master_id: int,
    repo: FIRRepository = Depends(get_fir_repo),
    user: dict = Depends(get_current_user),
):
    service = FIRService(repo)
    return await service.get_evidence(case_master_id)
