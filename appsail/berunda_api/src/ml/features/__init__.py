"""ML feature engineering utilities."""

from __future__ import annotations

from collections import Counter
from datetime import datetime
from typing import Any


class BaseFeatureExtractor:
    """Abstract base for feature extractors."""

    def extract(self, data: Any) -> dict[str, float]:
        raise NotImplementedError


class CaseFeatureExtractor(BaseFeatureExtractor):
    """Extract features from case data."""

    def extract(self, cases: list[dict]) -> dict[str, float]:
        if not cases:
            return {"case_count": 0, "offense_diversity": 0, "recency_score": 0}

        case_count = len(cases)
        offense_types = [c.get("crimeHead", "") for c in cases]
        offense_diversity = len(set(offense_types)) / max(len(offense_types), 1)

        # Recency: weight more recent cases higher
        now = datetime.now()
        total_weight = 0.0
        for case in cases:
            fir_date = case.get("firDate")
            if fir_date:
                try:
                    days_ago = (now - datetime.fromisoformat(str(fir_date))).days
                    total_weight += max(0, 1 - days_ago / 365)
                except (ValueError, TypeError):
                    total_weight += 0.5
            else:
                total_weight += 0.5
        recency_score = total_weight / len(cases) if cases else 0

        return {
            "case_count": float(case_count),
            "offense_diversity": float(offense_diversity),
            "recency_score": float(recency_score),
        }


class EntityFeatureExtractor(BaseFeatureExtractor):
    """Extract features from entity (person) data."""

    def extract(self, entity: dict) -> dict[str, float]:
        link_count = len(entity.get("linkedCases", []))
        relationship_count = len(entity.get("relationships", []))
        avg_risk = entity.get("avgRiskScore", 0)

        return {
            "link_count": float(link_count),
            "relationship_count": float(relationship_count),
            "risk_history": float(avg_risk),
        }


class GeoFeatureExtractor(BaseFeatureExtractor):
    """Extract spatial features from location data."""

    def extract(self, cases: list[dict]) -> dict[str, float]:
        if not cases:
            return {"case_density": 0, "hotspot_proximity": 0}

        districts = [c.get("districtCode", "") for c in cases]
        district_counts = Counter(districts)

        # Case density: cases per district
        case_density = max(district_counts.values()) / len(districts) if districts else 0

        # Hotspot proximity (simplified)
        hotspot_proximity = sum(1 for c in cases if c.get("isHotspot", False)) / len(cases)

        return {
            "case_density": float(case_density),
            "hotspot_proximity": float(hotspot_proximity),
        }


class FeaturePipeline:
    """Combine multiple feature extractors."""

    def __init__(self):
        self.case_extractor = CaseFeatureExtractor()
        self.entity_extractor = EntityFeatureExtractor()
        self.geo_extractor = GeoFeatureExtractor()

    def extract_all(
        self, cases: list[dict] | None = None, entity: dict | None = None
    ) -> dict[str, float]:
        features = {}
        if cases is not None:
            features.update(self.case_extractor.extract(cases))
            features.update(self.geo_extractor.extract(cases))
        if entity is not None:
            features.update(self.entity_extractor.extract(entity))
        return features
