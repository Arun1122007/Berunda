from __future__ import annotations

from src.schemas.base import APIBase


class SocioeconomicRecord(APIBase):
    district_id: int
    district_name: str
    population: int
    unemployment_rate: float
    urbanization_rate: float
    literacy_rate: float
    crime_rate_per_100k: float
    correlation_coefficient: float | None = None


class SocioeconomicQuery(APIBase):
    district_id: int | None = None
    sort_by: str = "crime_rate_per_100k"
    order: str = "desc"
