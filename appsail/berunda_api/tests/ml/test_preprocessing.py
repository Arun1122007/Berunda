"""Tests for ml.preprocessing module."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src.ml.preprocessing import (
    DataValidator,
    FeatureScaler,
    Preprocessor,
    PreprocessingPipeline,
    clean_dataframe,
)


class TestCleanDataframe:
    def test_cleans_whitespace_in_columns(self):
        df = pd.DataFrame({" col A ": [1], "col B": [2]})
        result = clean_dataframe(df)
        assert list(result.columns) == ["col_A", "col_B"]

    def test_replaces_na_variants(self):
        df = pd.DataFrame({"a": ["None", "null", "NA", np.nan, 1]})
        result = clean_dataframe(df)
        assert result["a"].isna().sum() == 4

    def test_deduplicates_columns(self):
        df = pd.DataFrame({"a": [1], "b": [2], "a": [3]})
        result = clean_dataframe(df)
        assert len(result.columns) == 2


class TestDataValidator:
    def test_check_schema_valid(self):
        df = pd.DataFrame({"name": ["alice"], "age": [30]})
        validator = DataValidator(schema={"name": "categorical", "age": "numeric"})
        result = validator.check_schema(df)
        assert result["valid"] is True

    def test_check_schema_missing_columns(self):
        df = pd.DataFrame({"name": ["alice"]})
        validator = DataValidator(schema={"name": "categorical", "age": "numeric"})
        result = validator.check_schema(df)
        assert result["valid"] is False
        assert "age" in result["missing_columns"]

    def test_check_null_ratios_passes(self):
        df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
        validator = DataValidator()
        result = validator.check_null_ratios(df)
        assert result["passed"] is True

    def test_check_null_ratios_fails(self):
        df = pd.DataFrame({"a": [1, np.nan, np.nan]})
        validator = DataValidator()
        result = validator.check_null_ratios(df, thresholds={"a": 0.3})
        assert result["passed"] is False

    def test_check_value_ranges(self):
        df = pd.DataFrame({"age": [150, 25, -5]})
        validator = DataValidator()
        result = validator.check_value_ranges(df, {"age": (0, 120)})
        assert result["passed"] is False


class TestPreprocessor:
    def test_normalize(self):
        data = np.array([[1.0], [2.0], [3.0], [4.0], [5.0]])
        p = Preprocessor()
        result = p.normalize(data)
        assert abs(result.mean()) < 1e-10
        assert abs(result.std() - 1.0) < 1e-10

    def test_minmax_scale(self):
        data = np.array([[1.0], [2.0], [3.0]])
        p = Preprocessor()
        result = p.minmax_scale(data)
        assert result.min() == 0.0
        assert result.max() == 1.0

    def test_encode_categorical(self):
        s = pd.Series(["a", "b", "a"])
        p = Preprocessor()
        result = p.encode_categorical(s)
        assert result.tolist() == [0, 1, 0]


class TestFeatureScaler:
    def test_fit_transform_and_transform(self):
        scaler = FeatureScaler()
        data = np.array([[1.0], [2.0], [3.0]])
        fitted = scaler.fit_transform(data)
        transformed = scaler.transform(np.array([[1.5]]))
        assert transformed.shape == (1, 1)

    def test_transform_unfitted_raises(self):
        scaler = FeatureScaler()
        with pytest.raises(ValueError, match="not fitted"):
            scaler.transform(np.array([[1.0]]))


class TestPreprocessingPipeline:
    def test_fit_transform(self):
        df = pd.DataFrame({
            "date": ["2024-01-01", "2024-06-15"],
            "cat": ["a", "b"],
            "num": [10.0, 20.0],
        })
        pipeline = PreprocessingPipeline({
            "date_columns": ["date"],
            "categorical_columns": ["cat"],
            "numeric_columns": ["num"],
        })
        result = pipeline.fit_transform(df)
        assert "num" in result.columns
        assert "cat_encoded" in result.columns or "cat" not in result.columns

    def test_run_without_fit(self):
        df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
        pipeline = PreprocessingPipeline()
        result = pipeline.run(df)
        assert len(result) == 2
