from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import get_db, get_fir_repo
from src.middleware.auth import get_current_user
from src.repositories.core import FIRRepository
from src.schemas.search import SearchFilters, SearchResponse, SearchResultItem
from src.services.fir_service import FIRService
from src.services.mo_similarity_service import MOSimilarityService
from src.services.search_service import SearchService

router = APIRouter(prefix="/api/v1", tags=["Search"])


@router.post("/search", response_model=SearchResponse)
async def search_firs(
    filters: SearchFilters,
    repo: FIRRepository = Depends(get_fir_repo),
    user: dict = Depends(get_current_user),
):
    service = FIRService(repo)
    district_id = user.get("district_id") if user.get("role") != "admin" else None

    items, total = await service.repo.list_firs(
        page=filters.page,
        page_size=filters.page_size,
        district_id=district_id,
        police_station_id=filters.police_station_id,
        status_id=filters.status_id,
        assigned_officer_id=filters.assigned_officer_id,
        date_from=filters.date_from,
        date_to=filters.date_to,
        crime_major_head_id=filters.crime_major_head_id,
    )

    result_items = []
    for c in items:
        match_reason = None
        confidence = None

        crime_no = getattr(c, "CrimeNo", None)
        if filters.crime_no and crime_no and filters.crime_no.lower() in crime_no.lower():
            match_reason = "Crime number match"
            confidence = 1.0
        elif filters.vehicle_number:
            vehicles = await service.repo.list_vehicles(getattr(c, "CaseMasterID", 0))
            for v in vehicles:
                if filters.vehicle_number.lower() in getattr(v, "VehicleNumber", "").lower():
                    match_reason = f"Vehicle match: {v.VehicleNumber}"
                    confidence = getattr(v, "Confidence", None)
                    break

        brief_facts = getattr(c, "BriefFacts", None)
        if not brief_facts:
            occ = c.__dict__.get("occurrence") or await service.repo.get_occurrence(getattr(c, "CaseMasterID", 0))
            if occ:
                brief_facts = getattr(occ, "BriefFacts", None)
        result_items.append(
            SearchResultItem(
                CaseMasterID=getattr(c, "CaseMasterID", 0),
                CrimeNo=crime_no,
                CrimeRegisteredDate=getattr(c, "CrimeRegisteredDate", None),
                PoliceStationID=getattr(c, "PoliceStationID", None),
                CaseStatusID=getattr(c, "CaseStatusID", None),
                BriefFacts=brief_facts,
                Confidence=confidence,
                MatchReason=match_reason,
            )
        )

    return SearchResponse(
        items=result_items,
        total=total,
        page=filters.page,
        page_size=filters.page_size,
        semantic_used=filters.semantic,
    )

@router.post("/search/hybrid")
async def search_hybrid(
    query: str = Query(..., min_length=3),
    page_size: int = Query(20, ge=1, le=100),
    session: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """Phase 5 Hybrid Semantic Search endpoint."""
    service = SearchService(session)
    try:
        results = await service.search_hybrid(query, user, page_size=page_size)
        return results
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/firs/{fir_id}/similar")
async def search_similar_firs(
    fir_id: int,
    top_k: int = Query(5, ge=1, le=20),
    min_score: float = Query(0.4, ge=0.0, le=1.0),
    session: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """Phase 5 Similar-FIR detection endpoint via vector embeddings."""
    service = MOSimilarityService(session)
    try:
        results = await service.find_similar_cases(fir_id, top_k, min_score)
        return {"items": results, "total": len(results)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
