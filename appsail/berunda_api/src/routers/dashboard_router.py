from contextlib import suppress

from fastapi import APIRouter, Depends

from src.dependencies import get_fir_repo
from src.middleware.auth import get_current_user, require_role
from src.repositories.core import FIRRepository
from src.schemas.dashboard import DashboardMetrics, RecentActivityItem, SupervisorDashboardMetrics
from src.services.fir_service import FIRService

router = APIRouter(prefix="/api/v1", tags=["Dashboard"])


@router.get("/dashboard/officer", response_model=DashboardMetrics)
async def officer_dashboard(
    repo: FIRRepository = Depends(get_fir_repo),
    user: dict = Depends(get_current_user),
):
    service = FIRService(repo)
    user_id = user.get("id") or user.get("user_id")
    district_id = user.get("district_id") if user.get("role") != "admin" else None
    police_station_id = user.get("police_station_id")

    metrics = await service.repo.get_dashboard_metrics(
        district_id=district_id,
        police_station_id=police_station_id,
    )

    if user_id:
        assigned_firs, assigned_total = await service.repo.list_firs(
            page=1, page_size=1, assigned_officer_id=user_id,
        )
        metrics["assigned_to_me_count"] = assigned_total

    return DashboardMetrics(**metrics)


@router.get("/dashboard/supervisor", response_model=SupervisorDashboardMetrics)
async def supervisor_dashboard(
    repo: FIRRepository = Depends(get_fir_repo),
    user: dict = Depends(require_role(["admin", "supervisor"])),
):
    service = FIRService(repo)
    district_id = user.get("district_id") if user.get("role") != "admin" else None
    police_station_id = user.get("police_station_id")

    metrics = await service.repo.get_dashboard_metrics(
        district_id=district_id,
        police_station_id=police_station_id,
    )
    return SupervisorDashboardMetrics(**metrics)


@router.get("/dashboard/activity", response_model=list[RecentActivityItem])
async def recent_activity(
    repo: FIRRepository = Depends(get_fir_repo),
    user: dict = Depends(get_current_user),
):
    service = FIRService(repo)
    district_id = user.get("district_id") if user.get("role") != "admin" else None

    items, _ = await service.repo.list_firs(
        page=1, page_size=10, district_id=district_id,
    )
    activities = []
    for c in items:
        ts = None
        with suppress(Exception):
            ts = c.CrimeRegisteredDate.isoformat() if hasattr(c.CrimeRegisteredDate, "isoformat") else str(c.CrimeRegisteredDate)
        activities.append(
            RecentActivityItem(
                CaseMasterID=c.CaseMasterID,
                CrimeNo=c.CrimeNo,
                ActivityType="FIR_REGISTERED",
                Description=f"FIR {c.CrimeNo or c.CaseMasterID} registered",
                Timestamp=ts,
            )
        )
    return activities
