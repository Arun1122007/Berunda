from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from src.dependencies import get_graph_repo
from src.middleware.auth import get_current_user
from src.repositories.core import GraphRepository
from src.schemas.graph import GraphResponse
from src.services.graph_service import GraphService

router = APIRouter(prefix="/api/v1/graph", tags=["Graph"])


@router.get("", response_model=GraphResponse)
async def get_graph(
    person_entity_id: int | None = Query(None),
    case_id: int | None = Query(None),
    max_depth: int = Query(2, ge=1, le=5),
    min_confidence: float = Query(0.5, ge=0.0, le=1.0),
    repo: GraphRepository = Depends(get_graph_repo),
    user: dict = Depends(get_current_user),
):
    service = GraphService(repo=repo)
    return await service.get_entity_graph(
        person_entity_id=person_entity_id,
        case_id=case_id,
        max_depth=max_depth,
        min_confidence=min_confidence,
    )
