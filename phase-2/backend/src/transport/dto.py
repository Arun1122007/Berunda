from __future__ import annotations
import uuid
from datetime import datetime, date
from decimal import Decimal
from typing import Optional, Sequence
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class CamelCaseModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class FIRCreateRequest(CamelCaseModel):
    crime_no: str
    police_station_id: str
    case_category_id: str
    gravity_offence_id: str
    crime_major_head_id: str
    crime_minor_head_id: str
    case_status_id: str
    district_id: str
    case_no: Optional[str] = None
    incident_from_date: Optional[date] = None
    incident_to_date: Optional[date] = None
    brief_facts: Optional[str] = None
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None


class FIRUpdateRequest(CamelCaseModel):
    crime_no: Optional[str] = None
    police_station_id: Optional[str] = None
    case_category_id: Optional[str] = None
    gravity_offence_id: Optional[str] = None
    crime_major_head_id: Optional[str] = None
    crime_minor_head_id: Optional[str] = None
    case_status_id: Optional[str] = None
    district_id: Optional[str] = None
    case_no: Optional[str] = None
    incident_from_date: Optional[date] = None
    incident_to_date: Optional[date] = None
    brief_facts: Optional[str] = None
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None


class FIRDetailResponse(CamelCaseModel):
    id: uuid.UUID
    crime_no: str
    case_no: Optional[str] = None
    registered_date: datetime
    police_station_id: str
    case_category_id: str
    gravity_offence_id: str
    crime_major_head_id: str
    crime_minor_head_id: str
    case_status_id: str
    incident_from_date: Optional[date] = None
    incident_to_date: Optional[date] = None
    brief_facts: Optional[str] = None
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None
    district_id: str
    created_by: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class FIRListResponse(CamelCaseModel):
    items: Sequence[FIRDetailResponse]
    total: int
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)


class LoginRequest(CamelCaseModel):
    email: str
    password: str


class RegisterRequest(CamelCaseModel):
    email: str
    password: str
    full_name: str
    role: str = "officer"
    district_id: Optional[str] = None


class RefreshRequest(CamelCaseModel):
    refresh_token: str


class TokenResponse(CamelCaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: "UserResponse"


class UserResponse(CamelCaseModel):
    id: uuid.UUID
    email: str
    full_name: str
    role: str
    district_id: Optional[str] = None
    is_active: bool = True
