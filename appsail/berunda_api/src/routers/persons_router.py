from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from src.dependencies import get_fir_repo
from src.middleware.auth import get_current_user
from src.repositories.core import FIRRepository
from src.schemas.fir import AccusedResponse, ComplainantResponse, VictimResponse
from src.services.fir_service import FIRService

router = APIRouter(prefix="/api/v1/fir", tags=["Persons"])


@router.get("/{case_master_id}/complainants", response_model=list[ComplainantResponse])
async def list_complainants(
    case_master_id: int,
    repo: FIRRepository = Depends(get_fir_repo),
    user: dict = Depends(get_current_user),
):
    service = FIRService(repo)
    case = await service.get_fir(case_master_id)
    if case is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="FIR not found")
    return [ComplainantResponse.model_validate(c) for c in (case.complainants or [])]


@router.get("/{case_master_id}/victims", response_model=list[VictimResponse])
async def list_victims(
    case_master_id: int,
    repo: FIRRepository = Depends(get_fir_repo),
    user: dict = Depends(get_current_user),
):
    service = FIRService(repo)
    case = await service.get_fir(case_master_id)
    if case is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="FIR not found")
    return [VictimResponse.model_validate(v) for v in (case.victims or [])]


@router.get("/{case_master_id}/accused", response_model=list[AccusedResponse])
async def list_accused(
    case_master_id: int,
    repo: FIRRepository = Depends(get_fir_repo),
    user: dict = Depends(get_current_user),
):
    service = FIRService(repo)
    case = await service.get_fir(case_master_id)
    if case is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="FIR not found")
    return [AccusedResponse.model_validate(a) for a in (case.accused or [])]


@router.get("/{case_master_id}/act-sections", response_model=list)
async def list_act_sections(
    case_master_id: int,
    repo: FIRRepository = Depends(get_fir_repo),
    user: dict = Depends(get_current_user),
):
    from src.schemas.fir import ActSectionResponse
    service = FIRService(repo)
    case = await service.get_fir(case_master_id)
    if case is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="FIR not found")
    return [ActSectionResponse.model_validate(s) for s in (case.act_sections or [])]
