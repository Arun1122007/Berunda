from __future__ import annotations
import uuid
from datetime import datetime, date
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field


class FIR(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
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
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        frozen = True


class Person(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    fir_id: uuid.UUID
    person_type: str
    full_name: str
    father_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    aadhaar_hash: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        frozen = True


class ActSection(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    fir_id: uuid.UUID
    act_name: str
    section_number: str
    description: Optional[str] = None
    is_primary: bool = False

    class Config:
        frozen = True


class User(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    email: str
    password_hash: str
    full_name: str
    role: str
    district_id: Optional[str] = None
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        frozen = True


class Session(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    user_id: uuid.UUID
    token_hash: str
    refresh_token_hash: Optional[str] = None
    issued_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime
    revoked_at: Optional[datetime] = None
    is_revoked: bool = False

    class Config:
        frozen = True
