from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends

from src.dependencies import get_ingestion_repo
from src.middleware.auth import get_current_user
from src.repositories.core import IngestionRepository
from src.schemas.ingestion import (
    IngestionCommitRequest,
    IngestionPreviewRequest,
    IngestionPreviewResponse,
)
from src.services.ingestion_service import IngestionService

router = APIRouter(prefix="/api/v1/ingest", tags=["Ingestion"])


@router.post("/preview", response_model=IngestionPreviewResponse)
async def preview_ingestion(
    request: IngestionPreviewRequest,
    repo: IngestionRepository = Depends(get_ingestion_repo),
    user: dict = Depends(get_current_user),
):
    service = IngestionService(repo=repo)
    result = await service.preview_file(request)
    return IngestionPreviewResponse.model_validate(result)


@router.post("/commit", response_model=dict[str, Any])
async def commit_ingestion(
    request: IngestionCommitRequest,
    repo: IngestionRepository = Depends(get_ingestion_repo),
    user: dict = Depends(get_current_user),
):
    service = IngestionService(repo=repo)
    return await service.commit_batch(request)
