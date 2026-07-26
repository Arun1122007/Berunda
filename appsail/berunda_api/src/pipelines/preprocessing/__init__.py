from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd

from src.ml.preprocessing import PreprocessingPipeline as MLPreprocessingPipeline, clean_dataframe
from src.pipelines.base import BasePipeline
from src.shared.logging import get_logger

logger = get_logger(__name__)


@dataclass
class PreprocessorConfig:
    """Configuration for preprocessing pipeline."""

    date_columns: list[str] | None = None
    categorical_columns: list[str] | None = None
    text_columns: list[str] | None = None
    fill_strategy: str = "mean"


class PreprocessingPipeline(BasePipeline):
    """Data preprocessing pipeline with configurable steps."""

    def __init__(self, config: PreprocessorConfig | None = None):
        self.config = config or PreprocessorConfig()
        self._status: dict[str, Any] = {"state": "idle", "last_run": None}

    def validate(self, **kwargs: Any) -> dict[str, Any]:
        return {"valid": True, "issues": []}

    def get_status(self) -> dict[str, Any]:
        return dict(self._status)

    async def run(self, data: pd.DataFrame | None = None, **kwargs: Any) -> dict:
        self._status["state"] = "running"
        df = data if data is not None else kwargs.get("data", pd.DataFrame())
        if isinstance(df, dict):
            df = pd.DataFrame(df)

        result = df.copy()

        if self.config.date_columns:
            result = self._parse_dates(result)

        if self.config.categorical_columns:
            result = self._encode_categorical(result)

        if self.config.text_columns:
            result = self._clean_text(result)

        if self.config.fill_strategy:
            result = self._fill_missing(result)

        self._status = {"state": "completed", "last_run": __import__("time").time()}
        return {"preprocessed_data": result, "n_rows": len(result), "n_cols": len(result.columns)}

    def _parse_dates(self, df: pd.DataFrame) -> pd.DataFrame:
        for col in self.config.date_columns or []:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce")
        return df

    def _encode_categorical(self, df: pd.DataFrame) -> pd.DataFrame:
        for col in self.config.categorical_columns or []:
            if col in df.columns:
                df[col] = df[col].astype("category").cat.codes
        return df

    def _clean_text(self, df: pd.DataFrame) -> pd.DataFrame:
        for col in self.config.text_columns or []:
            if col in df.columns:
                df[col] = df[col].astype(str).apply(self._clean_single_text)
        return df

    def _clean_single_text(self, text: str) -> str:
        text = re.sub(r"<[^>]+>", "", text)
        text = re.sub(r"http\S+", "", text)
        text = re.sub(r"[^\w\s]", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def _fill_missing(self, df: pd.DataFrame) -> pd.DataFrame:
        for col in df.columns:
            if df[col].isna().sum() > 0:
                if df[col].dtype in (np.float64, np.float32, np.int64):
                    if self.config.fill_strategy == "mean":
                        df[col] = df[col].fillna(df[col].mean())
                    elif self.config.fill_strategy == "median":
                        df[col] = df[col].fillna(df[col].median())
                    elif self.config.fill_strategy == "zero":
                        df[col] = df[col].fillna(0)
                else:
                    df[col] = df[col].fillna("unknown")
        return df


async def preprocess_data(state: dict) -> dict:
    config = PreprocessorConfig(**state.get("preprocessor_config", {}))
    pipeline = PreprocessingPipeline(config)
    data = state.get("data", pd.DataFrame())
    if isinstance(data, dict):
        data = pd.DataFrame(data)
    return {"preprocessed_data": (await pipeline.run(data=data)).get("preprocessed_data", data)}
