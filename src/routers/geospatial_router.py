from fastapi import APIRouter, Depends, HTTPException

from src.dependencies import get_fir_repo
from src.middleware.auth import get_current_user
from src.repositories.core import FIRRepository
from src.services.geospatial_service import GeospatialService

router = APIRouter(prefix="/api/v1/analytics/geography", tags=["Geospatial"])

@router.get("/heatmap")
async def get_heatmap_endpoint(
    repo: FIRRepository = Depends(get_fir_repo),
    user: dict = Depends(get_current_user)
):
    service = GeospatialService(repo)
    district_id = user.get("district_id") if user.get("role") != "admin" else None
    police_station_id = user.get("police_station_id")

    result = await service.get_heatmap_data(
        district_id=district_id,
        police_station_id=police_station_id
    )

    if not result.get("success"):
        raise HTTPException(status_code=403, detail=result.get("error"))
    return result
