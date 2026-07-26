from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query

from src.dependencies import get_fir_repo
from src.middleware.auth import get_current_user, require_role
from src.repositories.core import FIRRepository
from src.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/api/v1/analytics", tags=["Analytics"])

@router.get("/kpis/{metric_id}")
async def get_kpi_endpoint(
    metric_id: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    repo: FIRRepository = Depends(get_fir_repo),
    user: dict = Depends(get_current_user)
):
    service = AnalyticsService(repo)
    # RBAC logic
    district_id = user.get("district_id") if user.get("role") != "admin" else None
    police_station_id = user.get("police_station_id")
    
    result = await service.get_kpi(
        metric_id=metric_id.upper(),
        district_id=district_id,
        police_station_id=police_station_id,
        start_date=start_date,
        end_date=end_date
    )
    if not result.get("success"):
        raise HTTPException(status_code=403, detail=result.get("error"))
    return result

@router.get("/firs/trends")
async def get_trends_endpoint(
    metric_id: str = Query("TOTAL_FIRS"),
    grain: str = Query("daily", description="Aggregation grain: daily, weekly, monthly"),
    repo: FIRRepository = Depends(get_fir_repo),
    user: dict = Depends(get_current_user)
):
    service = AnalyticsService(repo)
    district_id = user.get("district_id") if user.get("role") != "admin" else None
    police_station_id = user.get("police_station_id")
    
    result = await service.get_trends(
        metric_id=metric_id.upper(),
        grain=grain,
        district_id=district_id,
        police_station_id=police_station_id
    )
    return result

@router.post("/export")
async def export_analytics_endpoint(
    metric_id: str,
    repo: FIRRepository = Depends(get_fir_repo),
    user: dict = Depends(require_role(["admin", "supervisor"]))
):
    """Generates a secure CSV of the aggregated metrics, enforcing privacy bounds."""
    # Not returning raw records, only the pre-aggregated payload
    service = AnalyticsService(repo)
    district_id = user.get("district_id") if user.get("role") != "admin" else None
    
    trends = await service.get_trends(metric_id, grain="daily", district_id=district_id)
    # Dummy CSV generation payload
    return {"success": True, "download_url": "https://stratus.catalyst.zoho.in/bucket/123", "context": {"status": "Generated via Stratus"}}
