from __future__ import annotations

from datetime import date

from src.schemas.base import APIBase


class HotspotLayerResponse(APIBase):
    HotspotLayerID: int
    DistrictID: int | None = None
    TileX: int | None = None
    TileY: int | None = None
    DensityScore: float | None = None
    WeekStart: date | None = None
    WeekEnd: date | None = None


class HotspotQuery(APIBase):
    district_id: int | None = None
    week_start: date | None = None
    week_end: date | None = None
    page: int = 1
    page_size: int = 50
