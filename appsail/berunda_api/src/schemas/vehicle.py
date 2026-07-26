from datetime import datetime

from pydantic import Field

from src.schemas.base import APIBase


class VehicleLinkCreate(APIBase):
    VehicleNumber: str = Field(..., min_length=1, max_length=50, examples=["KA-01-AB-1234"])
    Source: str = Field("manual", examples=["manual", "ai_extraction", "witness"])
    Confidence: float = Field(1.0, ge=0.0, le=1.0)


class VehicleLinkResponse(APIBase):
    VehicleLinkID: int
    VehicleNumber: str
    CaseMasterID: int | None = None
    Confidence: float | None = None
    Source: str | None = None
    CreatedAt: datetime | None = None
