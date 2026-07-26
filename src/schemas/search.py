from datetime import date, datetime

from pydantic import Field

from src.schemas.base import APIBase


class SearchFilters(APIBase):
    query: str | None = Field(None, max_length=500, examples=["vehicle theft near city center"])
    crime_no: str | None = Field(None, max_length=100)
    date_from: date | None = None
    date_to: date | None = None
    status_id: int | None = None
    police_station_id: int | None = None
    assigned_officer_id: int | None = None
    crime_major_head_id: int | None = None
    person_name: str | None = Field(None, max_length=200)
    vehicle_number: str | None = Field(None, max_length=50)
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)
    semantic: bool = Field(False, description="Enable semantic search")


class SearchResultItem(APIBase):
    CaseMasterID: int
    CrimeNo: str | None = None
    CrimeRegisteredDate: date | None = None
    PoliceStationID: int | None = None
    CaseStatusID: int | None = None
    BriefFacts: str | None = None
    Confidence: float | None = None
    MatchReason: str | None = None


class SearchResponse(APIBase):
    items: list[SearchResultItem]
    total: int
    page: int
    page_size: int
    semantic_used: bool = False
