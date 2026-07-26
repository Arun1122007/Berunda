from fastapi import APIRouter, Depends, HTTPException, status

from src.dependencies import get_fir_repo
from src.middleware.auth import get_current_user, require_role
from src.repositories.core import FIRRepository
from src.schemas.report import ReportContent, ReportRequestCreate, ReportRequestResponse
from src.services.fir_service import FIRService

router = APIRouter(prefix="/api/v1/reports", tags=["Reports"])


@router.post("", response_model=ReportRequestResponse, status_code=status.HTTP_201_CREATED)
async def request_report(
    data: ReportRequestCreate,
    repo: FIRRepository = Depends(get_fir_repo),
    user: dict = Depends(require_role(["admin", "officer", "supervisor", "analyst"])),
):
    service = FIRService(repo)
    user_id = user.get("id") or user.get("user_id")
    return await service.request_report(
        requested_by_user_id=user_id,
        report_type=data.ReportType,
        parameters=data.Parameters,
        file_format=data.FileFormat,
    )


@router.get("", response_model=list[ReportRequestResponse])
async def list_reports(
    repo: FIRRepository = Depends(get_fir_repo),
    user: dict = Depends(get_current_user),
):
    service = FIRService(repo)
    user_id = user.get("id") or user.get("user_id")
    return await service.list_reports(user_id=user_id)


@router.get("/{report_id}", response_model=ReportRequestResponse)
async def get_report(
    report_id: str,
    repo: FIRRepository = Depends(get_fir_repo),
    user: dict = Depends(get_current_user),
):
    service = FIRService(repo)
    report = await service.get_report(report_id)
    if report is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    return report


@router.post("/{report_id}/generate", response_model=ReportContent)
async def generate_report(
    report_id: str,
    repo: FIRRepository = Depends(get_fir_repo),
    user: dict = Depends(require_role(["admin", "officer", "supervisor", "analyst"])),
):
    service = FIRService(repo)
    try:
        return await service.generate_report_content(report_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
