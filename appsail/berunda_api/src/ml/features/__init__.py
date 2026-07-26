from __future__ import annotations

from collections import Counter
from datetime import datetime
from typing import Any

import numpy as np
import pandas as pd

from src.shared.logging import get_logger

logger = get_logger(__name__)

_FEATURE_NAMES: list[str] | None = None


def get_feature_names() -> list[str]:
    """Return the canonical list of feature column names."""
    if _FEATURE_NAMES is not None:
        return _FEATURE_NAMES.copy()
    return [
        "hour", "day_of_week", "day_of_month", "month", "season",
        "is_weekend", "is_night", "quarter",
        "district_encoded", "police_station_encoded",
        "crime_category_encoded", "case_status_encoded",
        "text_len", "text_word_count",
        "text_tfidf_0", "text_tfidf_1", "text_tfidf_2", "text_tfidf_3", "text_tfidf_4",
    ]


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """Build feature matrix from raw case DataFrame.

    Creates temporal, spatial, categorical, and text-derived features.
    """
    result = df.copy()

    result = _build_temporal_features(result)

    result = _build_spatial_features(result)

    result = _build_categorical_features(result)

    result = _build_text_features(result)

    result = result.fillna(0)

    global _FEATURE_NAMES
    _FEATURE_NAMES = [c for c in result.columns if c not in ("CrimeNo", "CaseNo", "briefFacts", "BriefFacts")]

    return result


def _build_temporal_features(df: pd.DataFrame) -> pd.DataFrame:
    """Extract temporal features from datetime columns."""
    date_cols = [c for c in df.columns if any(k in c.lower() for k in ("date", "time", "registered", "incident")) and "from" in c.lower() or c.lower() in ("firdate", "crime_date", "incidentfromdate")]
    date_col = None
    for candidate in ("IncidentFromDate", "CrimeRegisteredDate", "firDate", "crime_date", "incident_date", "date"):
        if candidate in df.columns:
            date_col = candidate
            break

    if date_col:
        parsed = pd.to_datetime(df[date_col], errors="coerce")
        df["hour"] = parsed.dt.hour.fillna(0).astype(int)
        df["day_of_week"] = parsed.dt.dayofweek.fillna(0).astype(int)
        df["day_of_month"] = parsed.dt.day.fillna(1).astype(int)
        df["month"] = parsed.dt.month.fillna(1).astype(int)
        df["quarter"] = parsed.dt.quarter.fillna(1).astype(int)
        df["season"] = parsed.dt.month.map(
            {12: 0, 1: 0, 2: 0, 3: 1, 4: 1, 5: 1, 6: 2, 7: 2, 8: 2, 9: 3, 10: 3, 11: 3}
        ).fillna(0).astype(int)
        df["is_weekend"] = (parsed.dt.dayofweek >= 5).fillna(False).astype(int)
        df["is_night"] = ((parsed.dt.hour >= 20) | (parsed.dt.hour < 6)).fillna(False).astype(int)
    else:
        for col in ("hour", "day_of_week", "day_of_month", "month", "quarter", "season", "is_weekend", "is_night"):
            df[col] = 0

    return df


def _build_spatial_features(df: pd.DataFrame) -> pd.DataFrame:
    """Encode spatial columns (district, police station)."""
    for col_candidate, encoded_name in [
        ("DistrictID", "district_encoded"),
        ("districtCode", "district_encoded"),
        ("district", "district_encoded"),
        ("PoliceStationID", "police_station_encoded"),
        ("policeStation", "police_station_encoded"),
    ]:
        if col_candidate in df.columns:
            df[encoded_name] = df[col_candidate].fillna(-1).astype(int)
    if "district_encoded" not in df.columns:
        df["district_encoded"] = -1
    if "police_station_encoded" not in df.columns:
        df["police_station_encoded"] = -1
    return df


def _build_categorical_features(df: pd.DataFrame) -> pd.DataFrame:
    """Encode categorical crime attributes."""
    for col_candidate, encoded_name in [
        ("CrimeMajorHeadID", "crime_category_encoded"),
        ("crimeHead", "crime_category_encoded"),
        ("crime_head", "crime_category_encoded"),
        ("CaseStatusID", "case_status_encoded"),
        ("caseStatus", "case_status_encoded"),
    ]:
        if col_candidate in df.columns:
            df[encoded_name] = df[col_candidate].fillna(-1).astype(int)
    if "crime_category_encoded" not in df.columns:
        df["crime_category_encoded"] = -1
    if "case_status_encoded" not in df.columns:
        df["case_status_encoded"] = -1
    return df


def _build_text_features(df: pd.DataFrame) -> pd.DataFrame:
    """Extract features from text columns (briefFacts)."""
    text_col = None
    for candidate in ("BriefFacts", "briefFacts", "facts", "description", "narrative"):
        if candidate in df.columns:
            text_col = candidate
            break

    if text_col:
        texts = df[text_col].astype(str).fillna("")
        df["text_len"] = texts.str.len().fillna(0).astype(float)
        df["text_word_count"] = texts.str.split().str.len().fillna(0).astype(float)
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            tfidf = TfidfVectorizer(max_features=5, stop_words="english")
            tfidf_matrix = tfidf.fit_transform(texts)
            for i in range(min(5, tfidf_matrix.shape[1])):
                df[f"text_tfidf_{i}"] = tfidf_matrix[:, i].toarray().flatten()
            for i in range(tfidf_matrix.shape[1], 5):
                df[f"text_tfidf_{i}"] = 0.0
        except Exception:
            for i in range(5):
                df[f"text_tfidf_{i}"] = 0.0
    else:
        df["text_len"] = 0
        df["text_word_count"] = 0
        for i in range(5):
            df[f"text_tfidf_{i}"] = 0.0
    return df


class FeatureStore:
    """In-memory cache for computed feature DataFrames."""

    def __init__(self, max_cached: int = 10):
        self._cache: dict[str, pd.DataFrame] = {}
        self._metadata: dict[str, dict[str, Any]] = {}
        self.max_cached = max_cached

    def store(self, key: str, features: pd.DataFrame, metadata: dict[str, Any] | None = None) -> None:
        if len(self._cache) >= self.max_cached:
            oldest = next(iter(self._cache))
            del self._cache[oldest]
            self._metadata.pop(oldest, None)
        self._cache[key] = features
        self._metadata[key] = metadata or {}

    def retrieve(self, key: str) -> pd.DataFrame | None:
        return self._cache.get(key)

    def get_metadata(self, key: str) -> dict[str, Any] | None:
        return self._metadata.get(key)

    def list_keys(self) -> list[str]:
        return list(self._cache.keys())

    def clear(self) -> None:
        self._cache.clear()
        self._metadata.clear()

    def __contains__(self, key: str) -> bool:
        return key in self._cache


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
        now = datetime.now()
        total_weight = 0
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
        case_density = max(district_counts.values()) / len(districts) if districts else 0
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
