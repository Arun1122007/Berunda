from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.middleware.auth import get_current_user
from src.schemas.rag import RAGQuery, RAGResponse
from src.services.rag_service import RAGService

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from fastapi import Request

limiter = Limiter(key_func=get_remote_address)
router = APIRouter(prefix="/api/v1/rag", tags=["RAG"])


@router.post("/query", response_model=RAGResponse)
@limiter.limit("5/minute")
async def query_rag(
    request: Request,
    data: RAGQuery,
    session: AsyncSession = Depends(get_session),
    user: dict = Depends(get_current_user),
):
    service = RAGService(session)
    return await service.query(data, user)
