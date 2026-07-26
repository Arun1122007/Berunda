"""Tests for ml.features module."""

from __future__ import annotations

import pandas as pd
import pytest

from src.ml.features import (
    CaseFeatureExtractor,
    EntityFeatureExtractor,
    FeaturePipeline,
    FeatureStore,
    GeoFeatureExtractor,
    build_features,
    get_feature_names,
)


class TestBuildFeatures:
    def test_returns_dataframe(self):
        df = pd.DataFrame({"CrimeNo": ["C1"]})
        result = build_features(df)
        assert isinstance(result, pd.DataFrame)

    def test_temporal_features_with_date(self):
        df = pd.DataFrame({"IncidentFromDate": ["2024-06-15 14:30:00"]})
        result = build_features(df)
        for col in ("hour", "day_of_week", "month", "season", "is_weekend"):
            assert col in result.columns

    def test_text_features_with_brief_facts(self):
        df = pd.DataFrame({"BriefFacts": ["Theft of vehicle occurred at night"]})
        result = build_features(df)
        assert "text_len" in result.columns
        assert "text_word_count" in result.columns

    def test_defaults_when_no_columns(self):
        df = pd.DataFrame({"dummy": [1]})
        result = build_features(df)
        assert "district_encoded" in result.columns
        assert result["district_encoded"].iloc[0] == -1


class TestFeatureStore:
    def test_store_and_retrieve(self):
        store = FeatureStore()
        df = pd.DataFrame({"a": [1, 2]})
        store.store("test", df, {"source": "test"})
        retrieved = store.retrieve("test")
        assert retrieved is not None
        assert len(retrieved) == 2

    def test_contains(self):
        store = FeatureStore()
        store.store("key", pd.DataFrame())
        assert "key" in store
        assert "missing" not in store

    def test_clear(self):
        store = FeatureStore()
        store.store("a", pd.DataFrame())
        store.clear()
        assert store.list_keys() == []

    def test_max_cached(self):
        store = FeatureStore(max_cached=2)
        store.store("a", pd.DataFrame())
        store.store("b", pd.DataFrame())
        store.store("c", pd.DataFrame())
        assert "a" not in store

    def test_get_metadata(self):
        store = FeatureStore()
        store.store("x", pd.DataFrame(), {"version": 1})
        assert store.get_metadata("x") == {"version": 1}


class TestFeatureExtractors:
    def test_case_feature_extractor_empty(self):
        extractor = CaseFeatureExtractor()
        result = extractor.extract([])
        assert result["case_count"] == 0

    def test_case_feature_extractor_with_data(self):
        extractor = CaseFeatureExtractor()
        result = extractor.extract([{"crimeHead": "THEFT"}, {"crimeHead": "ASSAULT"}])
        assert result["case_count"] == 2
        assert result["offense_diversity"] == 1.0

    def test_entity_feature_extractor(self):
        extractor = EntityFeatureExtractor()
        result = extractor.extract({"linkedCases": [1, 2], "relationships": [3], "avgRiskScore": 0.5})
        assert result["link_count"] == 2
        assert result["relationship_count"] == 1

    def test_geo_feature_extractor_empty(self):
        extractor = GeoFeatureExtractor()
        result = extractor.extract([])
        assert result["case_density"] == 0

    def test_feature_pipeline(self):
        pipeline = FeaturePipeline()
        result = pipeline.extract_all(cases=[{"crimeHead": "X"}], entity={"linkedCases": []})
        assert "case_count" in result
        assert "risk_history" in result


class TestGetFeatureNames:
    def test_returns_list(self):
        names = get_feature_names()
        assert isinstance(names, list)
        assert len(names) > 0
