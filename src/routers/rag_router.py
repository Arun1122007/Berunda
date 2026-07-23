from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.middleware.auth import get_current_user
from src.schemas.rag import RAGQuery, RAGResponse
from src.services.rag_service import RAGService

router = APIRouter(prefix="/api/v1/rag", tags=["RAG"])


@router.post("/query", response_model=RAGResponse)
async def query_rag(
    data: RAGQuery,
    session: AsyncSession = Depends(get_session),
    user: dict = Depends(get_current_user),
):
    service = RAGService(session)
    return await service.query(data)
