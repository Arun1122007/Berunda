from __future__ import annotations

from typing import Any
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.middleware.auth import get_current_user
from src.services.ai_assistant_service import AIAssistantService

router = APIRouter(prefix="/api/v1/assistant", tags=["AI Assistant"])


class AIAssistantRequest(BaseModel):
    question: str
    history: list[dict[str, str]] = []


@router.post("/query", response_model=dict[str, Any])
async def query_ai_assistant(
    request: AIAssistantRequest,
    session: AsyncSession = Depends(get_session),
    user: dict = Depends(get_current_user),
):
    service = AIAssistantService(session)
    return await service.answer_query(request.question, request.history)


@router.get("/stats", response_model=dict[str, Any])
async def get_assistant_stats(
    session: AsyncSession = Depends(get_session),
    user: dict = Depends(get_current_user),
):
    service = AIAssistantService(session)
    return await service.get_database_stats()
