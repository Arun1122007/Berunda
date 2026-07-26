from datetime import datetime

from src.schemas.base import APIBase


class DashboardMetrics(APIBase):
    total_firs: int = 0
    status_counts: dict[str, int] = {}
    pending_review_count: int = 0
    unassigned_count: int = 0
    assigned_to_me_count: int = 0
    recent_activity_count: int = 0


class SupervisorDashboardMetrics(APIBase):
    total_firs: int = 0
    status_counts: dict[str, int] = {}
    pending_review_count: int = 0
    unassigned_count: int = 0
    active_officer_count: int = 0
    cases_per_officer: dict[str, int] = {}


class RecentActivityItem(APIBase):
    CaseMasterID: int
    CrimeNo: str | None = None
    ActivityType: str
    Description: str | None = None
    Timestamp: datetime | None = None
