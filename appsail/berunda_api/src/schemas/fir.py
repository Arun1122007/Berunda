from __future__ import annotations

from datetime import date, datetime

from pydantic import Field

from src.schemas.base import APIBase


class FIRCreate(APIBase):
    CrimeNo: str = Field(examples=["CR-2026-0421"])
    CaseNo: str | None = Field(None, examples=["42/2026"])
    CrimeRegisteredDate: date | None = Field(None, examples=["2026-07-15"])
    PolicePersonID: int | None = Field(None, examples=[101])
    PoliceStationID: int | None = Field(None, examples=[5])
    CaseCategoryID: int | None = Field(None, examples=[1])
    GravityOffenceID: int | None = Field(None, examples=[3])
    CrimeMajorHeadID: int | None = Field(None, examples=[12])
    CrimeMinorHeadID: int | None = Field(None, examples=[45])
    CaseStatusID: int | None = Field(None, examples=[1])
    IncidentFromDate: datetime | None = Field(None, examples=["2026-07-14T20:30:00"])
    IncidentToDate: datetime | None = Field(None, examples=["2026-07-14T23:45:00"])
    BriefFacts: str | None = Field(None, examples=["Unknown person(s) broke into the complainant's residence by forcing open the rear door and stole gold jewellery worth ₹5,00,000 and cash ₹50,000."])
    Latitude: float | None = Field(None, examples=[12.9716])
    Longitude: float | None = Field(None, examples=[77.5946])


class FIRUpdate(APIBase):
    CaseStatusID: int | None = Field(None, examples=[2])
    IncidentToDate: datetime | None = Field(None, examples=["2026-07-15T02:00:00"])
    BriefFacts: str | None = Field(None, examples=["Updated facts after preliminary investigation."])


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
