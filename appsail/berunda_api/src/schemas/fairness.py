from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import Field

from src.schemas.base import APIBase


class FairnessCheckRequest(APIBase):
    CheckType: str = Field(
        default="feature_audit",
        pattern=r"^(feature_audit|access_control|disparate_impact)$",
    )


class FairnessCheckResult(APIBase):
    FairnessCheckID: int
    CheckType: str
    Timestamp: datetime
    Passed: bool
    Details: str
    CheckedBy: str


class FairnessCheckResponse(APIBase):
    CheckType: str
    Passed: bool
    Details: str
    Findings: list[dict[str, Any]]
    CheckedBy: str
    Timestamp: datetime
