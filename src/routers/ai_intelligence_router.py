from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Body
from pydantic import BaseModel

from src.dependencies import get_fir_repo
from src.middleware.auth import get_current_user, require_role
from src.repositories.core import FIRRepository
from src.services.ai_task_service import AITaskService

router = APIRouter(prefix="/api/v1/ai", tags=["AI Intelligence Layer"])

class ReviewPayload(BaseModel):
    status: str
    feedback: Optional[str] = None

@router.post("/firs/{fir_id}/summarize")
async def summarize_fir(
    fir_id: int,
    repo: FIRRepository = Depends(get_fir_repo),
    user: dict = Depends(get_current_user)
):
    service = AITaskService(repo)
    result = await service.execute_task(fir_id, "FIR_SUMMARIZE", user.get("id", 1))
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    return result

@router.post("/firs/{fir_id}/extract-entities")
async def extract_entities(
    fir_id: int,
    repo: FIRRepository = Depends(get_fir_repo),
    user: dict = Depends(get_current_user)
):
    service = AITaskService(repo)
    result = await service.execute_task(fir_id, "FIR_EXTRACT_ENTITIES", user.get("id", 1))
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    return result

@router.post("/outputs/{output_id}/review")
async def review_output(
    output_id: str,
    payload: ReviewPayload,
    repo: FIRRepository = Depends(get_fir_repo),
    user: dict = Depends(require_role(["supervisor", "admin"]))
):
    """
    Human-in-the-loop review endpoint. Requires elevated permissions.
    """
    service = AITaskService(repo)
    result = await service.review_output(
        output_id=output_id,
        reviewer_id=user.get("id", 1),
        status=payload.status,
        feedback=payload.feedback
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=404, detail=result.get("error"))
    return result
