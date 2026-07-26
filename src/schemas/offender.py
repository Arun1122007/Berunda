from __future__ import annotations

from datetime import date
from src.schemas.base import APIBase


class OffenderSummaryResponse(APIBase):
    id: int
    name: str
    alias: str | None = None
    age: int | None = None
    gender: str | None = None
    primary_mo: str | None = None
    jurisdiction: str | None = None
    case_count: int = 1
    risk_status: str = "Moderate"
    last_active: str | None = None


class OffenderProfileResponse(OffenderSummaryResponse):
    fingerprint_id: str | None = None
    aadhaar_status: str | None = None
    first_arrest_date: str | None = None
    co_offenders: list[dict] = []
    linked_cases: list[dict] = []


class OffenderQuery(APIBase):
    search: str | None = None
    min_cases: int = 1
    jurisdiction: str | None = None
    page: int = 1
    page_size: int = 20
