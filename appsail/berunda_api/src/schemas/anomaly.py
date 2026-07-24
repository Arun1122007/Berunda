from __future__ import annotations

from datetime import date, datetime

from src.schemas.base import APIBase


class AnomalyAlertResponse(APIBase):
    AnomalyAlertID: int
    DistrictID: int | None = None
    CrimeHeadID: int | None = None
    WeekStart: datetime | None = None
    ObservedCount: int | None = None
    BaselineMean: float | None = None
    StdDev: float | None = None
    ZScore: float | None = None
    AlertLevel: int | None = None


class AnomalyQuery(APIBase):
    district_id: int | None = None
    alert_only: bool = True
    week_start: date | None = None
    page: int = 1
    page_size: int = 20
