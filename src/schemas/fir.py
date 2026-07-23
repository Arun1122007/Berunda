from __future__ import annotations

from datetime import date, datetime

from pydantic import Field

from src.schemas.base import APIBase


class FIRCreate(APIBase):
    CrimeNo: str
    CaseNo: str | None = None
    CrimeRegisteredDate: date | None = None
    PolicePersonID: int | None = None
    PoliceStationID: int | None = None
    CaseCategoryID: int | None = None
    GravityOffenceID: int | None = None
    CrimeMajorHeadID: int | None = None
    CrimeMinorHeadID: int | None = None
    CaseStatusID: int | None = None
    IncidentFromDate: datetime | None = None
    IncidentToDate: datetime | None = None
    BriefFacts: str | None = None
    Latitude: float | None = None
    Longitude: float | None = None


class FIRUpdate(APIBase):
    CaseStatusID: int | None = None
    IncidentToDate: datetime | None = None
    BriefFacts: str | None = None


class FIRResponse(APIBase):
    CaseMasterID: int
    CrimeNo: str
    CaseNo: str | None = None
    CrimeRegisteredDate: date | None = None
    PoliceStationID: int | None = None
    CaseStatusID: int | None = None
    CrimeMajorHeadID: int | None = None
    CrimeMinorHeadID: int | None = None
    IncidentFromDate: datetime | None = None
    IncidentToDate: datetime | None = None
    Latitude: float | None = None
    Longitude: float | None = None
    BriefFacts: str | None = None


class FIRListResponse(APIBase):
    items: list[FIRResponse]
    total: int
    page: int
    page_size: int


class ComplainantResponse(APIBase):
    ComplainantID: int
    CaseMasterID: int
    ComplainantName: str
    AgeYear: int | None = None
    OccupationID: int | None = None
    ReligionID: int | None = None
    CasteID: int | None = None
    GenderID: int | None = None


class VictimResponse(APIBase):
    VictimMasterID: int
    CaseMasterID: int
    VictimName: str
    AgeYear: int | None = None
    GenderID: int | None = None
    VictimPolice: bool | None = None


class AccusedResponse(APIBase):
    AccusedMasterID: int
    CaseMasterID: int
    AccusedName: str
    AgeYear: int | None = None
    GenderID: int | None = None
    PersonID: int | None = None


class ActSectionResponse(APIBase):
    CaseMasterID: int
    ActID: str
    SectionID: str
    ActOrderID: int | None = None
    SectionOrderID: int | None = None


class FIRDetailResponse(FIRResponse):
    complainants: list[ComplainantResponse] = Field(default_factory=list)
    victims: list[VictimResponse] = Field(default_factory=list)
    accused: list[AccusedResponse] = Field(default_factory=list)
    act_sections: list[ActSectionResponse] = Field(default_factory=list)
