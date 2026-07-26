from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from src.dependencies import get_rag_repo
from src.middleware.auth import get_current_user
from src.repositories.core import RAGRepository
from src.schemas.rag import RAGQuery, RAGResponse
from src.services.rag_service import RAGService

limiter = Limiter(key_func=get_remote_address)
router = APIRouter(prefix="/api/v1/rag", tags=["RAG"])


@router.post("/query", response_model=RAGResponse)
@limiter.limit("5/minute")
async def query_rag(
    request: Request,
    data: RAGQuery,
    repo: RAGRepository = Depends(get_rag_repo),
    user: dict = Depends(get_current_user),
):
    service = RAGService(repo=repo)
    return await service.query(data, user)
