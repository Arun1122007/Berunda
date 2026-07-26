from __future__ import annotations

import re
from typing import Any

import numpy as np
import pandas as pd

from src.shared.logging import get_logger

logger = get_logger(__name__)


class DataValidator:
    """Validate DataFrame schema, null ratios, and value ranges."""

    def __init__(self, schema: dict[str, str] | None = None):
        self.schema = schema or {}

    def check_schema(self, df: pd.DataFrame) -> dict[str, Any]:
        missing = [col for col in self.schema if col not in df.columns]
        extra = [col for col in df.columns if col not in self.schema]
        type_mismatches = []
        for col, expected_type in self.schema.items():
            if col in df.columns:
                actual_dtype = str(df[col].dtype)
                if expected_type == "numeric" and not np.issubdtype(df[col].dtype, np.number):
                    type_mismatches.append({"column": col, "expected": expected_type, "actual": actual_dtype})
                elif expected_type == "categorical" and not (
                    pd.api.types.is_object_dtype(df[col]) or pd.api.types.is_categorical_dtype(df[col])
                ):
                    type_mismatches.append({"column": col, "expected": expected_type, "actual": actual_dtype})
                elif expected_type == "datetime" and not pd.api.types.is_datetime64_any_dtype(df[col]):
                    type_mismatches.append({"column": col, "expected": expected_type, "actual": actual_dtype})
        return {
            "valid": len(missing) == 0 and len(type_mismatches) == 0,
            "missing_columns": missing,
            "extra_columns": extra,
            "type_mismatches": type_mismatches,
        }

    def check_null_ratios(
        self, df: pd.DataFrame, thresholds: dict[str, float] | None = None
    ) -> dict[str, Any]:
        thresholds = thresholds or {}
        violations = []
        for col in df.columns:
            null_ratio = df[col].isna().mean()
            threshold = thresholds.get(col, 0.5)
            if null_ratio > threshold:
                violations.append({"column": col, "null_ratio": float(null_ratio), "threshold": threshold})
        return {"violations": violations, "passed": len(violations) == 0}

    def check_value_ranges(
        self, df: pd.DataFrame, ranges: dict[str, tuple[float, float]]
    ) -> dict[str, Any]:
        violations = []
        for col, (low, high) in ranges.items():
            if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
                out_of_range = df[col][(df[col] < low) | (df[col] > high)]
                if len(out_of_range) > 0:
                    violations.append(
                        {
                            "column": col,
                            "range": [low, high],
                            "out_of_range_count": int(len(out_of_range)),
                            "sample_values": out_of_range.head(5).tolist(),
                        }
                    )
        return {"violations": violations, "passed": len(violations) == 0}

    def validate_all(
        self,
        df: pd.DataFrame,
        null_thresholds: dict[str, float] | None = None,
        value_ranges: dict[str, tuple[float, float]] | None = None,
    ) -> dict[str, Any]:
        results = {
            "schema_check": self.check_schema(df),
            "null_check": self.check_null_ratios(df, null_thresholds),
        }
        if value_ranges:
            results["range_check"] = self.check_value_ranges(df, value_ranges)
        results["passed"] = all(
            r.get("passed", r.get("valid", False)) for r in results.values()
        )
        return results


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Clean a DataFrame: strip whitespace, normalize NA variants, deduplicate columns."""
    df = df.copy()
    df.columns = [str(c).strip().replace(" ", "_") for c in df.columns]
    df = df.replace([None, "None", "null", "", "NA", "N/A", "NaN"], np.nan)
    df = df.loc[:, ~df.columns.duplicated()]
    return df


class Preprocessor:
    """Data preprocessing utilities."""

    def normalize(self, data: np.ndarray) -> np.ndarray:
        from sklearn.preprocessing import StandardScaler
        return StandardScaler().fit_transform(data)

    def minmax_scale(self, data: np.ndarray) -> np.ndarray:
        from sklearn.preprocessing import MinMaxScaler
        return MinMaxScaler().fit_transform(data)

    def encode_categorical(self, data: pd.Series) -> np.ndarray:
        from sklearn.preprocessing import LabelEncoder
        return LabelEncoder().fit_transform(data)

    def one_hot_encode(self, data: pd.Series) -> pd.DataFrame:
        return pd.get_dummies(data, prefix=data.name)

    def train_test_split(self, x, y, test_size=0.2, random_state=42):
        from sklearn.model_selection import train_test_split as tts
        return tts(x, y, test_size=test_size, random_state=random_state)


class FeatureScaler:
    """Feature scaling with fitted transformers."""

    def __init__(self):
        self.scalers: dict[str, Any] = {}

    def fit_transform(self, x: np.ndarray, name: str = "default") -> np.ndarray:
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        self.scalers[name] = scaler
        return scaler.fit_transform(x)

    def transform(self, x: np.ndarray, name: str = "default") -> np.ndarray:
        scaler = self.scalers.get(name)
        if scaler is None:
            raise ValueError(f"Scaler '{name}' not fitted")
        return scaler.transform(x)


class PreprocessingPipeline:
    """Configurable preprocessing pipeline with fitted transformers."""

    def __init__(self, config: dict[str, Any] | None = None):
        self.config = {
            "date_columns": [],
            "categorical_columns": [],
            "numeric_columns": [],
            "text_columns": [],
            "fill_strategy": "mean",
            "drop_columns": [],
            "target_column": None,
        }
        if config:
            self.config.update(config)
        self._encoders: dict[str, Any] = {}
        self._scalers: dict[str, Any] = {}
        self._fitted = False

    def fit(self, df: pd.DataFrame) -> PreprocessingPipeline:
        df = clean_dataframe(df)
        for col in self.config.get("categorical_columns", []):
            if col in df.columns:
                from sklearn.preprocessing import LabelEncoder
                le = LabelEncoder()
                le.fit(df[col].astype(str).fillna("unknown"))
                self._encoders[col] = le
        for col in self.config.get("numeric_columns", []):
            if col in df.columns:
                from sklearn.preprocessing import StandardScaler
                scaler = StandardScaler()
                scaler.fit(df[[col]].fillna(df[col].mean()))
                self._scalers[col] = scaler
        self._fitted = True
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if not self._fitted:
            raise RuntimeError("Pipeline not fitted. Call fit() first.")
        df = clean_dataframe(df)
        return self._apply_transforms(df)

    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        return self.fit(df).transform(df)

    def _apply_transforms(self, df: pd.DataFrame) -> pd.DataFrame:
        result = df.copy()
        for col in self.config.get("drop_columns", []):
            if col in result.columns and col != self.config.get("target_column"):
                result = result.drop(columns=[col])

        for col in self.config.get("date_columns", []):
            if col in result.columns:
                result[col] = pd.to_datetime(result[col], errors="coerce")

        for col in self.config.get("categorical_columns", []):
            if col in result.columns and col in self._encoders:
                le = self._encoders[col]
                result[col] = result[col].astype(str).fillna("unknown")
                result[col + "_encoded"] = le.transform(result[col])
                if col != self.config.get("target_column"):
                    result = result.drop(columns=[col])

        for col in self.config.get("numeric_columns", []):
            if col in result.columns and col in self._scalers:
                fill_val = result[col].mean()
                result[col] = result[col].fillna(fill_val)
                result[col] = self._scalers[col].transform(result[[col]])

        for col in self.config.get("text_columns", []):
            if col in result.columns:
                result[col] = result[col].astype(str).apply(_clean_single_text)

        fill_strategy = self.config.get("fill_strategy", "mean")
        result = _fill_missing(result, fill_strategy)

        return result

    def run(self, data: pd.DataFrame) -> pd.DataFrame:
        if self._fitted:
            return self.transform(data)
        return self.fit_transform(data)


def _clean_single_text(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _fill_missing(df: pd.DataFrame, strategy: str = "mean") -> pd.DataFrame:
    df = df.copy()
    for col in df.columns:
        if df[col].isna().sum() > 0:
            if pd.api.types.is_numeric_dtype(df[col]):
                if strategy == "mean":
                    df[col] = df[col].fillna(df[col].mean())
                elif strategy == "median":
                    df[col] = df[col].fillna(df[col].median())
                elif strategy == "zero":
                    df[col] = df[col].fillna(0)
                elif strategy == "mode":
                    df[col] = df[col].fillna(df[col].mode().iloc[0] if not df[col].mode().empty else 0)
            else:
                df[col] = df[col].fillna("unknown")
    return df
