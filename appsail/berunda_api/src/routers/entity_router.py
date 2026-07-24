from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.middleware.auth import get_current_user, require_role
from src.schemas.entity import (
    EntityMergeRequest,
    EntitySearchQuery,
    EntitySearchResponse,
    PersonEntityLinkResponse,
    PersonEntityResponse,
)
from src.services.entity_service import EntityService

router = APIRouter(prefix="/api/v1/entities", tags=["Entities"])


@router.get("", response_model=EntitySearchResponse)
async def search_entities(
    name: str | None = Query(None),
    district_id: int | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    session: AsyncSession = Depends(get_session),
    user: dict = Depends(get_current_user),
):
    if user.get("role") != "admin":
        district_id = user.get("district_id")

    service = EntityService(session)
    query = EntitySearchQuery(name=name, district_id=district_id, page=page, page_size=page_size)
    items, total = await service.search_entities(query)
    return EntitySearchResponse(
        items=[PersonEntityResponse.model_validate(e) for e in items],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{entity_id}", response_model=PersonEntityResponse)
async def get_entity(
    entity_id: int,
    session: AsyncSession = Depends(get_session),
    user: dict = Depends(get_current_user),
):
    service = EntityService(session)
    entity = await service.get_entity(entity_id)
    if entity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entity not found")
    return PersonEntityResponse.model_validate(entity)


@router.get("/{entity_id}/links", response_model=list[PersonEntityLinkResponse])
async def get_entity_links(
    entity_id: int,
    session: AsyncSession = Depends(get_session),
    user: dict = Depends(get_current_user),
):
    service = EntityService(session)
    links = await service.get_entity_links(entity_id)
    return [PersonEntityLinkResponse.model_validate(link) for link in links]


@router.post("/merge", response_model=PersonEntityResponse)
async def merge_entities(
    data: EntityMergeRequest,
    session: AsyncSession = Depends(get_session),
    user: dict = Depends(require_role(["admin"])),
):
    service = EntityService(session)
    result = await service.merge_entities(
        data.source_entity_id, data.target_entity_id, data.reviewed_by
    )
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="One or both entities not found"
        )
    return PersonEntityResponse.model_validate(result)
