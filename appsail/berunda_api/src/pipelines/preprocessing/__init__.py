from __future__ import annotations

import re
from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class PreprocessorConfig:
    """Configuration for preprocessing pipeline."""

    date_columns: list[str] | None = None
    categorical_columns: list[str] | None = None
    text_columns: list[str] | None = None
    fill_strategy: str = "mean"  # mean, median, mode, zero


class PreprocessingPipeline:
    """Data preprocessing pipeline with configurable steps."""

    def __init__(self, config: PreprocessorConfig | None = None):
        self.config = config or PreprocessorConfig()

    def run(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()

        if self.config.date_columns:
            df = self._parse_dates(df)

        if self.config.categorical_columns:
            df = self._encode_categorical(df)

        if self.config.text_columns:
            df = self._clean_text(df)

        if self.config.fill_strategy:
            df = self._fill_missing(df)

        return df

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
        text = re.sub(r"<[^>]+>", "", text)  # HTML tags
        text = re.sub(r"http\S+", "", text)  # URLs
        text = re.sub(r"[^\w\s]", " ", text)  # Punctuation
        text = re.sub(r"\s+", " ", text)  # Extra spaces
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
    """Convenience function for Pipeline compatibility."""
    config = PreprocessorConfig(**state.get("preprocessor_config", {}))
    pipeline = PreprocessingPipeline(config)
    data = state.get("data", pd.DataFrame())
    if isinstance(data, dict):
        data = pd.DataFrame(data)
    return {"preprocessed_data": pipeline.run(data)}
