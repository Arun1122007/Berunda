from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from src.dependencies import get_ai_assistant_repo
from src.middleware.auth import get_current_user
from src.repositories.core import AIAssistantRepository
from src.services.ai_assistant_service import AIAssistantService

router = APIRouter(prefix="/api/v1/assistant", tags=["AI Assistant"])


class AIAssistantRequest(BaseModel):
    question: str
    history: list[dict[str, str]] = []


@router.post("/query", response_model=dict[str, Any])
async def query_ai_assistant(
    request: AIAssistantRequest,
    repo: AIAssistantRepository = Depends(get_ai_assistant_repo),
    user: dict = Depends(get_current_user),
):
    service = AIAssistantService(repo=repo)
    return await service.answer_query(request.question, request.history)


@router.get("/stats", response_model=dict[str, Any])
async def get_assistant_stats(
    repo: AIAssistantRepository = Depends(get_ai_assistant_repo),
    user: dict = Depends(get_current_user),
):
    service = AIAssistantService(repo=repo)
    return await service.get_database_stats()


@router.get("/suggestions", response_model=list[Any])
async def list_ai_suggestions(
    case_master_id: int | None = None,
    status: str | None = None,
    repo: AIAssistantRepository = Depends(get_ai_assistant_repo),
    user: dict = Depends(get_current_user),
):
    service = AIAssistantService(repo=repo)
    return await service.list_suggestions(case_master_id=case_master_id, status=status)


@router.get("/suggestions/{extraction_id}", response_model=Any)
async def get_ai_suggestion(
    extraction_id: int,
    repo: AIAssistantRepository = Depends(get_ai_assistant_repo),
    user: dict = Depends(get_current_user),
):
    service = AIAssistantService(repo=repo)
    suggestion = await service.get_suggestion(extraction_id)
    if not suggestion:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="AI suggestion not found")
    return suggestion


@router.post("/suggestions/{extraction_id}/apply", response_model=Any)
async def apply_ai_suggestion(
    extraction_id: int,
    request: dict[str, Any] | None = None,
    repo: AIAssistantRepository = Depends(get_ai_assistant_repo),
    user: dict = Depends(get_current_user),
):
    service = AIAssistantService(repo=repo)
    reviewer_id = user.get("id") or user.get("user_id") if isinstance(user, dict) else None
    comments = request.get("comments") if request and isinstance(request, dict) else None
    res = await service.apply_suggestion(extraction_id, reviewer_id=reviewer_id, comments=comments)
    if not res:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="AI suggestion not found")
    return res


@router.post("/suggestions/{extraction_id}/reject", response_model=Any)
async def reject_ai_suggestion(
    extraction_id: int,
    request: dict[str, Any] | None = None,
    repo: AIAssistantRepository = Depends(get_ai_assistant_repo),
    user: dict = Depends(get_current_user),
):
    service = AIAssistantService(repo=repo)
    reviewer_id = user.get("id") or user.get("user_id") if isinstance(user, dict) else None
    comments = request.get("comments") if request and isinstance(request, dict) else None
    res = await service.reject_suggestion(extraction_id, reviewer_id=reviewer_id, comments=comments)
    if not res:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="AI suggestion not found")
    return res
